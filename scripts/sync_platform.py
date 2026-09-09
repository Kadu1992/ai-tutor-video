#!/usr/bin/env python3
"""Utilitário de sincronização entre a skill ai-tutor-video e a plataforma de cursos.

Este módulo realiza chamadas HTTP (GET/POST) com a API do portal (ex: cursos-estudo / PythonWay)
para consultar cursos, obter o progresso gravado no banco SQLite e atualizar o estado do aluno.
Conta com fallback gracioso para não interromper a tutoria caso a API local esteja offline.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


# URL padrão da API local do portal de estudos
DEFAULT_API_URL = "http://localhost:8000"

# Tempo limite em segundos para conexões de rede locais
TIMEOUT_SECONDS = 5.0


# ==============================================================================
# Função: pull_platform
# O que esta parte faz: Realiza requisições GET para a API do portal para obter dados de cursos e progresso.
# Para que serve / Como funciona no fluxo: Permite que o tutor consulte o estado
# atual do aluno registrado no banco SQLite do portal, alinhando a sessão com a plataforma web.
# ==============================================================================
def pull_platform(api_url: str = DEFAULT_API_URL, course_id: str | None = None) -> dict[str, Any]:
    """Consulta cursos e progresso atual na API da plataforma de estudos."""
    base_url = api_url.rstrip("/")
    result: dict[str, Any] = {
        "connected": False,
        "courses": [],
        "progress": None,
        "warning": None,
    }

    try:
        # Consulta catálogo de cursos
        courses_endpoint = f"{base_url}/api/courses"
        req_courses = urllib.request.Request(courses_endpoint, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req_courses, timeout=TIMEOUT_SECONDS) as response:
            if response.status == 200:
                result["courses"] = json.loads(response.read().decode("utf-8"))

        # Consulta progresso registrado
        progress_endpoint = f"{base_url}/api/progress"
        if course_id:
            progress_endpoint += f"?course_id={urllib.request.quote(course_id)}"

        req_progress = urllib.request.Request(progress_endpoint, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req_progress, timeout=TIMEOUT_SECONDS) as response:
            if response.status == 200:
                result["progress"] = json.loads(response.read().decode("utf-8"))

        result["connected"] = True
        return result

    except urllib.error.URLError as exc:
        result["warning"] = (
            f"Plataforma offline ou inacessível em {base_url} ({exc.reason}). "
            "A tutoria continuará normalmente em modo local na IDE."
        )
        return result
    except Exception as exc:  # pylint: disable=broad-except
        result["warning"] = (
            f"Erro ao consultar a plataforma em {base_url}: {exc}. "
            "A tutoria continuará normalmente em modo local na IDE."
        )
        return result


# ==============================================================================
# Função: push_platform
# O que esta parte faz: Envia uma requisição POST com o progresso atualizado do aluno para a API do portal.
# Para que serve / Como funciona no fluxo: Atualiza notas do tutor, status de conclusão
# da aula, último vídeo assistido e playlists completadas diretamente no banco SQLite do portal.
# ==============================================================================
def push_platform(payload: dict[str, Any], api_url: str = DEFAULT_API_URL) -> dict[str, Any]:
    """Envia progresso atualizado para a API da plataforma de estudos."""
    base_url = api_url.rstrip("/")
    endpoint = f"{base_url}/api/progress"

    # Validação mínima de campos obrigatórios
    if not payload.get("course_id"):
        return {
            "connected": False,
            "success": False,
            "error": "Campo 'course_id' é obrigatório no payload de sincronização.",
        }

    data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data_bytes,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            response_body = response.read().decode("utf-8")
            parsed_response = json.loads(response_body) if response_body else {}
            return {
                "connected": True,
                "success": response.status in (200, 201),
                "status_code": response.status,
                "data": parsed_response,
            }
    except urllib.error.URLError as exc:
        return {
            "connected": False,
            "success": False,
            "warning": (
                f"Plataforma offline ou inacessível em {base_url} ({exc.reason}). "
                "Progresso salvo localmente no .ai-tutor/state.json, sincronização remota adiada."
            ),
        }
    except Exception as exc:  # pylint: disable=broad-except
        return {
            "connected": False,
            "success": False,
            "error": f"Falha na sincronização com {base_url}: {exc}",
        }


# ==============================================================================
# Bloco CLI: main
# O que esta parte faz: Interface de linha de comando para puxar ou enviar dados para o portal.
# Para que serve / Como funciona no fluxo: Permite que os workflows /platform-sync
# ou comandos do terminal sincronizem o progresso do aluno sem necessidade de código manual.
# ==============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sincroniza o progresso do AI Tutor Video com a plataforma de cursos local."
    )
    parser.add_argument(
        "--action",
        choices=["pull", "push"],
        default="pull",
        help="Ação a executar: 'pull' (consultar portal) ou 'push' (atualizar portal).",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"URL base da API da plataforma (padrão: {DEFAULT_API_URL}).",
    )
    parser.add_argument(
        "--course-id",
        help="Identificador do curso na plataforma (ex: 'curso-em-video').",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        help="Caminho para arquivo JSON contendo o payload para --action push.",
    )
    parser.add_argument(
        "--data-json",
        help="String JSON contendo o payload para --action push.",
    )
    parser.add_argument(
        "--status",
        help="Status do curso a enviar no push (ex: 'in-progress', 'completed').",
    )
    parser.add_argument(
        "--notes",
        help="Anotações do tutor sobre o progresso e domínio atingido.",
    )
    parser.add_argument(
        "--last-watched",
        help="Descrição do último vídeo assistido com timestamp de pausa.",
    )

    args = parser.parse_args()

    if args.action == "pull":
        resultado = pull_platform(api_url=args.api_url, course_id=args.course_id)
        if resultado.get("warning"):
            print(f"AVISO: {resultado['warning']}", file=sys.stderr)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0

    if args.action == "push":
        payload: dict[str, Any] = {}
        if args.data_file:
            if not args.data_file.is_file():
                print(f"ERRO: Arquivo de payload não encontrado: {args.data_file}", file=sys.stderr)
                return 1
            payload = json.loads(args.data_file.read_text(encoding="utf-8"))
        elif args.data_json:
            payload = json.loads(args.data_json)
        else:
            if not args.course_id:
                print("ERRO: Para --action push, forneça --data-file, --data-json ou --course-id.", file=sys.stderr)
                return 1
            payload = {
                "course_id": args.course_id,
                "status": args.status or "in-progress",
                "notes": args.notes or "Progresso atualizado pelo AI Tutor Video.",
                "lastWatched": args.last_watched or "",
            }

        resultado = push_platform(payload, api_url=args.api_url)
        if resultado.get("warning"):
            print(f"AVISO: {resultado['warning']}", file=sys.stderr)
        if resultado.get("error"):
            print(f"ERRO: {resultado['error']}", file=sys.stderr)
            return 1
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
