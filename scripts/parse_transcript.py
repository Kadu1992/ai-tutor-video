#!/usr/bin/env python3
"""Utilitário para análise e extração estruturada de transcrições de vídeo.

Este módulo processa arquivos Markdown gerados pelo yt-tool ou fontes similares,
extraindo metadados, marcações temporais (timestamps), tópicos e blocos de código.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path
from typing import Any

# Forçar saída UTF-8 no Windows para evitar falhas com caracteres especiais e notas musicais
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# Expressões regulares para captura de metadados no cabeçalho do Markdown
RE_TITLE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
RE_CANAL = re.compile(r"^[-*]\s*(?:Canal|Channel):\s*(.+)$", re.MULTILINE | re.IGNORECASE)
RE_DURACAO = re.compile(r"^[-*]\s*(?:Dura[cç][aã]o|Duration):\s*(.+)$", re.MULTILINE | re.IGNORECASE)
RE_URL = re.compile(r"^[-*]\s*(?:URL|Link):\s*(.+)$", re.MULTILINE | re.IGNORECASE)
RE_DATA = re.compile(r"^[-*]\s*(?:Publicado\s+em|Published):\s*(.+)$", re.MULTILINE | re.IGNORECASE)

# Expressão para capturar timestamps no formato [MM:SS] ou [HH:MM:SS] ou soltos no início da linha
RE_TIMESTAMP_LINE = re.compile(
    r"^(?:\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?)\s*(?:[-–:]\s*)?(.*)$",
    re.MULTILINE,
)

# Expressão para capturar blocos de código com linguagem
RE_CODE_BLOCK = re.compile(r"```([a-zA-Z0-9_-]*)\n(.*?)```", re.DOTALL)

# Expressão para extrair ID de vídeo do YouTube a partir de URL
RE_YOUTUBE_ID = re.compile(r"(?:v=|\/embed\/|\/watch\?v=|\/youtu\.be\/|\/v\/|shorts\/)([a-zA-Z0-9_-]+)")


# ==============================================================================
# Função: timestamp_to_seconds
# O que esta parte faz: Converte uma string de tempo (MM:SS ou HH:MM:SS) em segundos inteiros.
# Para que serve / Como funciona no fluxo: Permite que o tutor compare posições
# numéricas de vídeo, calcule checkpoints precisos e ordene os tópicos cronologicamente.
# ==============================================================================
def timestamp_to_seconds(timestamp_str: str) -> int:
    """Converte 'MM:SS' ou 'HH:MM:SS' para quantidade total de segundos."""
    partes = timestamp_str.strip().strip("[]").split(":")
    if len(partes) == 2:
        minutos, segundos = partes
        return int(minutos) * 60 + int(segundos)
    if len(partes) == 3:
        horas, minutos, segundos = partes
        return int(horas) * 3600 + int(minutos) * 60 + int(segundos)
    return 0


# ==============================================================================
# Função: seconds_to_timestamp
# O que esta parte faz: Converte um número de segundos em formato legível de timestamp (MM:SS ou HH:MM:SS).
# Para que serve / Como funciona no fluxo: Usado para formatar dados para o aluno
# e para gerar anotações de checkpoint humanamente legíveis no state.json e Markdown.
# ==============================================================================
def seconds_to_timestamp(total_seconds: int) -> str:
    """Converte segundos inteiros para string 'MM:SS' ou 'HH:MM:SS'."""
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    segundos = total_seconds % 60
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    return f"{minutos:02d}:{segundos:02d}"


# ==============================================================================
# Função: extract_metadata
# O que esta parte faz: Extrai dados descritivos da aula (título, canal, duração, URL e ID do vídeo).
# Para que serve / Como funciona no fluxo: Garante a rastreabilidade do vídeo que originou
# o conteúdo no estado persistente do tutor (.ai-tutor/state.json).
# ==============================================================================
def extract_metadata(text: str) -> dict[str, Any]:
    """Extrai cabeçalhos e metadados informados na transcrição."""
    title_match = RE_TITLE.search(text)
    canal_match = RE_CANAL.search(text)
    duracao_match = RE_DURACAO.search(text)
    url_match = RE_URL.search(text)
    data_match = RE_DATA.search(text)

    video_url = url_match.group(1).strip() if url_match else ""
    video_id = ""
    if video_url:
        id_match = RE_YOUTUBE_ID.search(video_url)
        if id_match:
            video_id = id_match.group(1)

    duration_str = duracao_match.group(1).strip() if duracao_match else ""
    duration_seconds = timestamp_to_seconds(duration_str) if duration_str else 0

    return {
        "video_id": video_id,
        "video_url": video_url,
        "title": title_match.group(1).strip() if title_match else "",
        "channel": canal_match.group(1).strip() if canal_match else "",
        "duration": duration_str,
        "duration_seconds": duration_seconds,
        "published_at": data_match.group(1).strip() if data_match else None,
    }


# ==============================================================================
# Função: extract_code_blocks
# O que esta parte faz: Localiza blocos cercados por três crases (fenced code blocks) no texto.
# Para que serve / Como funciona no fluxo: Permite que o tutor identifique exemplos de código
# demonstrados pelo instrutor para formular lições e desafios autônomos ancorados no vídeo.
# ==============================================================================
def extract_code_blocks(text: str) -> list[dict[str, str]]:
    """Extrai blocos de código com linguagem e conteúdo da transcrição."""
    code_blocks: list[dict[str, str]] = []
    for match in RE_CODE_BLOCK.finditer(text):
        lang = match.group(1).strip() or "text"
        code = match.group(2).strip()
        code_blocks.append({
            "language": lang,
            "code": code,
        })
    return code_blocks


# ==============================================================================
# Função: extract_topics
# O que esta parte faz: Segmenta o texto da transcrição por marcas de tempo cronológicas.
# Para que serve / Como funciona no fluxo: Cria a lista granular de tópicos e conceitos
# ensinados na aula, possibilitando que o tutor saiba o que já foi visto e o que está pendente.
# ==============================================================================
def extract_topics(text: str) -> list[dict[str, Any]]:
    """Identifica tópicos baseados em linhas de timestamp e seus conteúdos associados."""
    lines = text.splitlines()
    topics: list[dict[str, Any]] = []
    current_topic: dict[str, Any] | None = None
    content_lines: list[str] = []

    for line in lines:
        match = RE_TIMESTAMP_LINE.match(line.strip())
        if match:
            if current_topic:
                current_topic["summary"] = "\n".join(content_lines).strip()
                topics.append(current_topic)
                content_lines = []

            ts_raw = match.group(1)
            title_part = match.group(2).strip() or f"Tópico em {ts_raw}"
            seconds = timestamp_to_seconds(ts_raw)
            current_topic = {
                "timestamp": ts_raw,
                "seconds": seconds,
                "title": title_part,
                "summary": "",
            }
        else:
            if current_topic is not None and not line.startswith("```"):
                content_lines.append(line)

    if current_topic:
        current_topic["summary"] = "\n".join(content_lines).strip()
        topics.append(current_topic)

    return topics


# ==============================================================================
# Função: parse_transcript
# O que esta parte faz: Função principal de análise que orquestra a extração completa.
# Para que serve / Como funciona no fluxo: Ponto de entrada programático para que
# workflows ou scripts do tutor processem o arquivo e retornem a estrutura unificada.
# ==============================================================================
def parse_transcript(content: str, transcript_path: str = "") -> dict[str, Any]:
    """Processa o conteúdo da transcrição e retorna o resumo estruturado completo."""
    metadata = extract_metadata(content)
    if transcript_path:
        metadata["transcript_path"] = transcript_path

    topics = extract_topics(content)
    code_blocks = extract_code_blocks(content)

    # Identifica conceitos principais a partir dos títulos de tópicos detectados
    concepts: list[str] = []
    for topic in topics:
        title = topic.get("title", "").strip()
        if title and title not in concepts:
            concepts.append(title)

    return {
        "video_metadata": metadata,
        "concepts": concepts,
        "topics": topics,
        "code_blocks": code_blocks,
    }


# ==============================================================================
# Bloco CLI: main
# O que esta parte faz: Executa o utilitário a partir da linha de comando com argumentos.
# Para que serve / Como funciona no fluxo: Permite invocar `python scripts/parse_transcript.py`
# passando arquivos de transcrição obtidos via `yt-tool` e gerando saídas JSON legíveis.
# ==============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analisa transcrições de vídeo do yt-tool e extrai tópicos estruturados."
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Caminho do arquivo Markdown da transcrição a ser analisada.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Caminho opcional do arquivo JSON para salvar o resultado estruturado.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Formata o JSON de saída com indentação de 2 espaços.",
    )

    args = parser.parse_args()

    if args.file:
        if not args.file.is_file():
            print(f"ERRO: Arquivo não encontrado: {args.file}", file=sys.stderr)
            return 1
        content = args.file.read_text(encoding="utf-8")
        file_path_str = str(args.file)
    else:
        # Lê da entrada padrão (stdin) se nenhum arquivo for passado
        content = sys.stdin.read()
        file_path_str = ""

    if not content.strip():
        print("ERRO: Conteúdo vazio para análise.", file=sys.stderr)
        return 1

    result = parse_transcript(content, transcript_path=file_path_str)
    indent = 2 if args.pretty or not args.output else None
    json_text = json.dumps(result, ensure_ascii=False, indent=indent)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json_text + "\n", encoding="utf-8")
        print(f"Resultado salvo em: {args.output}")
    else:
        print(json_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
