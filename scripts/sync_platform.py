#!/usr/bin/env python3
"""Utilitário de sincronização entre a skill ai-tutor-video e a plataforma de cursos.

Este módulo realiza a leitura e persistência de dados de progresso e catálogo de cursos:
1. Diretamente no banco local SQLite (ex: pythonway.db) via biblioteca padrão sqlite3,
   garantindo funcionamento atômico e instantâneo sem depender de servidor web aberto.
2. Como alternativa/fallback, via chamadas HTTP (GET/POST) com a API do portal.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


# URL padrão da API local do portal de estudos (modo HTTP)
DEFAULT_API_URL = "http://localhost:8000"

# Nome padrão do banco SQLite local
DEFAULT_DB_FILENAME = "pythonway.db"

# Tempo limite em segundos para conexões de rede locais
TIMEOUT_SECONDS = 5.0


# ==============================================================================
# Função: find_sqlite_db
# O que esta parte faz: Localiza o arquivo de banco SQLite no caminho informado ou diretórios pais.
# Para que serve / Como funciona no fluxo: Permite que a skill detecte automaticamente o banco
# pythonway.db tanto a partir da raiz do projeto quanto de subdiretórios de estudo.
# ==============================================================================
def find_sqlite_db(custom_path: str | Path | None = None) -> Path | None:
    """Busca o arquivo de banco SQLite no caminho informado ou nos diretórios pais."""
    if custom_path:
        p = Path(custom_path)
        if p.is_file():
            return p
        return None

    # Tenta no diretório de trabalho atual
    current = Path.cwd()
    if (current / DEFAULT_DB_FILENAME).is_file():
        return current / DEFAULT_DB_FILENAME

    # Tenta nos diretórios pais até 4 níveis acima
    for parent in current.parents:
        if (parent / DEFAULT_DB_FILENAME).is_file():
            return parent / DEFAULT_DB_FILENAME

    return None


# ==============================================================================
# Função: pull_platform_sqlite
# O que esta parte faz: Consulta os dados de cursos e progresso lendo diretamente o banco SQLite.
# Para que serve / Como funciona no fluxo: Permite sincronização instantânea sem necessidade
# de servidor web ativo, garantindo integridade mesmo se o portal estiver fechado.
# ==============================================================================
def pull_platform_sqlite(db_path: Path, course_id: str | None = None) -> dict[str, Any]:
    """Consulta cursos e progresso lendo diretamente as tabelas do SQLite."""
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Obter cursos cadastrados
        courses = []
        try:
            cursor.execute("SELECT * FROM courses")
            for row in cursor.fetchall():
                c = dict(row)
                if c.get("features"):
                    try:
                        c["features"] = json.loads(c["features"])
                    except Exception:
                        c["features"] = []
                else:
                    c["features"] = []

                cursor.execute(
                    "SELECT name, link FROM playlists WHERE course_id = ? ORDER BY display_order ASC",
                    (c["id"],),
                )
                c["playlists"] = [dict(pl) for pl in cursor.fetchall()]
                courses.append(c)
        except sqlite3.OperationalError:
            courses = []

        # Obter progresso gravado
        progress_data: Any = None
        try:
            if course_id:
                cursor.execute("SELECT * FROM user_progress WHERE course_id = ?", (course_id,))
                row = cursor.fetchone()
                if row:
                    p = dict(row)
                    try:
                        p["completedPlaylists"] = json.loads(p.get("completed_playlists", "[]"))
                    except Exception:
                        p["completedPlaylists"] = []
                    p["lastWatched"] = p.get("last_watched", "")
                    progress_data = p
            else:
                cursor.execute("SELECT * FROM user_progress")
                progress_rows = cursor.fetchall()
                progress_dict: dict[str, Any] = {}
                for row in progress_rows:
                    p = dict(row)
                    try:
                        p["completedPlaylists"] = json.loads(p.get("completed_playlists", "[]"))
                    except Exception:
                        p["completedPlaylists"] = []
                    p["lastWatched"] = p.get("last_watched", "")
                    progress_dict[p["course_id"]] = p
                progress_data = progress_dict
        except sqlite3.OperationalError:
            progress_data = None

        conn.close()
        return {
            "connected": True,
            "source": "sqlite",
            "db_path": str(db_path),
            "courses": courses,
            "progress": progress_data,
            "warning": None,
        }
    except Exception as exc:
        return {
            "connected": False,
            "source": "sqlite",
            "db_path": str(db_path),
            "courses": [],
            "progress": None,
            "warning": f"Erro ao acessar banco SQLite em {db_path}: {exc}",
        }


# ==============================================================================
# Função: push_platform_sqlite
# O que esta parte faz: Grava ou atualiza o progresso do aluno diretamente na tabela user_progress do SQLite.
# Para que serve / Como funciona no fluxo: Atualiza notas, status, último vídeo assistido e playlists
# concluídas de forma atômica e persistente, sem depender de servidor HTTP rodando.
# ==============================================================================
def push_platform_sqlite(db_path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Persiste o progresso diretamente na tabela user_progress do SQLite."""
    course_id = payload.get("course_id")
    if not course_id:
        return {
            "connected": False,
            "source": "sqlite",
            "success": False,
            "error": "Campo 'course_id' é obrigatório no payload de sincronização.",
        }

    status = payload.get("status", "in-progress")
    notes = payload.get("notes", "")
    last_watched = payload.get("lastWatched") or payload.get("last_watched") or ""
    completed_playlists = payload.get("completedPlaylists") or payload.get("completed_playlists") or []
    if isinstance(completed_playlists, list):
        completed_playlists_json = json.dumps(completed_playlists)
    else:
        completed_playlists_json = str(completed_playlists)

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Garantir criação da tabela se não existir
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            course_id TEXT PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'not-started',
            notes TEXT NOT NULL DEFAULT '',
            last_watched TEXT NOT NULL DEFAULT '',
            completed_playlists TEXT NOT NULL DEFAULT '[]'
        )
        """)

        cursor.execute("""
        INSERT INTO user_progress (course_id, status, notes, last_watched, completed_playlists)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(course_id) DO UPDATE SET
            status = excluded.status,
            notes = excluded.notes,
            last_watched = excluded.last_watched,
            completed_playlists = excluded.completed_playlists
        """, (course_id, status, notes, last_watched, completed_playlists_json))

        conn.commit()
        conn.close()

        return {
            "connected": True,
            "source": "sqlite",
            "success": True,
            "status_code": 200,
            "db_path": str(db_path),
            "data": {
                "course_id": course_id,
                "status": status,
                "notes": notes,
                "lastWatched": last_watched,
                "completedPlaylists": completed_playlists if isinstance(completed_playlists, list) else [],
            },
        }
    except Exception as exc:
        return {
            "connected": False,
            "source": "sqlite",
            "success": False,
            "error": f"Falha na gravação SQLite em {db_path}: {exc}",
        }


# ==============================================================================
# Função: pull_platform
# O que esta parte faz: Realiza consulta de dados via SQLite direto ou API HTTP.
# Para que serve / Como funciona no fluxo: Puxa o progresso gravado no banco ou endpoint web.
# ==============================================================================
def pull_platform(
    api_url: str = DEFAULT_API_URL,
    course_id: str | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Consulta cursos e progresso atual na plataforma (via SQLite direto ou API HTTP)."""
    if db_path:
        db_file = Path(db_path)
        if db_file.is_file() or db_file.parent.is_dir():
            return pull_platform_sqlite(db_file, course_id=course_id)

    base_url = api_url.rstrip("/")
    result: dict[str, Any] = {
        "connected": False,
        "source": "http",
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
# O que esta parte faz: Envia dados de progresso via SQLite direto ou API HTTP.
# Para que serve / Como funciona no fluxo: Atualiza notas e progresso de forma atômica.
# ==============================================================================
def push_platform(
    payload: dict[str, Any],
    api_url: str = DEFAULT_API_URL,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Envia progresso atualizado para a plataforma (via SQLite direto ou API HTTP)."""
    # Validação mínima de campos obrigatórios
    if not payload.get("course_id"):
        return {
            "connected": False,
            "success": False,
            "error": "Campo 'course_id' é obrigatório no payload de sincronização.",
        }

    if db_path:
        db_file = Path(db_path)
        if db_file.is_file() or db_file.parent.is_dir():
            return push_platform_sqlite(db_file, payload)

    base_url = api_url.rstrip("/")
    endpoint = f"{base_url}/api/progress"

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
                "source": "http",
                "success": response.status in (200, 201),
                "status_code": response.status,
                "data": parsed_response,
            }
    except urllib.error.URLError as exc:
        return {
            "connected": False,
            "source": "http",
            "success": False,
            "warning": (
                f"Plataforma offline ou inacessível em {base_url} ({exc.reason}). "
                "Progresso salvo localmente no .ai-tutor/state.json, sincronização remota adiada."
            ),
        }
    except Exception as exc:  # pylint: disable=broad-except
        return {
            "connected": False,
            "source": "http",
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
        description="Sincroniza o progresso do AI Tutor Video com a plataforma de cursos local (SQLite direto ou HTTP)."
    )
    parser.add_argument(
        "--action",
        choices=["pull", "push"],
        default="pull",
        help="Ação a executar: 'pull' (consultar portal) ou 'push' (atualizar portal).",
    )
    parser.add_argument(
        "--db-path",
        help="Caminho para o banco SQLite local (ex: 'pythonway.db'). Se omitido, busca automaticamente 'pythonway.db'.",
    )
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Desativa o uso direto do SQLite e força o modo HTTP via API.",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"URL base da API da plataforma para modo HTTP (padrão: {DEFAULT_API_URL}).",
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

    # Resolver caminho do banco SQLite (a menos que --no-db seja passado)
    db_file = None if args.no_db else find_sqlite_db(args.db_path)

    if args.action == "pull":
        resultado = pull_platform(api_url=args.api_url, course_id=args.course_id, db_path=db_file)
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

        resultado = push_platform(payload, api_url=args.api_url, db_path=db_file)
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
