#!/usr/bin/env python3
"""Utilitário autônomo para busca e formatação de transcrições do YouTube.

Este módulo permite que a skill ai-tutor-video funcione de forma 100% autônoma
e portável em qualquer computador, mesmo quando o usuário não tiver o utilitário
yt-tool instalado previamente no sistema.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


# Expressão regular para captura de IDs de vídeos do YouTube em qualquer formato de URL
RE_YOUTUBE_ID = re.compile(
    r"(?:v=|\/embed\/|\/watch\?v=|\/youtu\.be\/|\/v\/|shorts\/|^)([a-zA-Z0-9_-]{11})(?:[?&]|$)"
)


# ==============================================================================
# Função: ensure_dependencies
# O que esta parte faz: Verifica se a biblioteca `youtube_transcript_api` está instalada
# e, caso não esteja, realiza a instalação automática e silenciosa via `pip install`.
# Para que serve / Como funciona no fluxo: Permite que novos usuários que instalaram
# a skill via Hub ou `npx` utilizem a transcrição de vídeos imediatamente, sem precisar
# configurar ambientes ou rodar comandos manuais no terminal.
# ==============================================================================
def ensure_dependencies() -> None:
    """Verifica e instala dependências necessárias em tempo de execução sob demanda."""
    try:
        import youtube_transcript_api  # noqa: F401
    except ImportError:
        print("[ai-tutor-video] Instalando biblioteca youtube-transcript-api para transcrição nativa...", file=sys.stderr)
        cmd = [sys.executable, "-m", "pip", "install", "youtube-transcript-api", "--quiet"]
        try:
            subprocess.run(cmd, check=True)
            print("[ai-tutor-video] Dependência instalada com sucesso!", file=sys.stderr)
        except Exception as exc:
            print(f"[ERRO] Falha ao instalar dependência 'youtube-transcript-api': {exc}", file=sys.stderr)
            print("Por favor, execute manualmente: pip install youtube-transcript-api", file=sys.stderr)
            sys.exit(1)


# ==============================================================================
# Função: extract_video_id
# O que esta parte faz: Extrai o identificador único de 11 caracteres de um vídeo do YouTube.
# Para que serve / Como funciona no fluxo: Trata URLs variadas (comuns, encurtadas do youtu.be,
# embeds ou shorts) e retorna apenas o ID limpo necessário para as consultas da API.
# ==============================================================================
def extract_video_id(url_or_id: str) -> str:
    """Extrai o ID do vídeo a partir de uma URL do YouTube ou valida um ID direto."""
    url_or_id = url_or_id.strip()
    match = RE_YOUTUBE_ID.search(url_or_id)
    if match:
        return match.group(1)
    if len(url_or_id) == 11 and re.match(r"^[a-zA-Z0-9_-]+$", url_or_id):
        return url_or_id
    return ""


# ==============================================================================
# Função: clean_filename
# O que esta parte faz: Sanitiza uma string para que ela seja usada com segurança como nome de arquivo.
# Para que serve / Como funciona no fluxo: Remove caracteres proibidos no Windows/Linux
# e acentos para gerar nomes de arquivos consistentes como `transcripts/<id>_<slug>.md`.
# ==============================================================================
def clean_filename(text: str) -> str:
    """Remove caracteres inválidos e acentos para criar nomes de arquivos seguros."""
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("ASCII")
    text = re.sub(r"[^a-zA-Z0-9\s_-]", "", text)
    text = re.sub(r"[\s_]+", "_", text).strip("_")
    return text[:60].lower()


# ==============================================================================
# Função: format_seconds
# O que esta parte faz: Converte uma quantidade de segundos em uma string formatada (MM:SS ou HH:MM:SS).
# Para que serve / Como funciona no fluxo: Formata as marcas de tempo (timestamps) de cada bloco
# da transcrição de maneira legível tanto para o aluno quanto para o analisador sintático.
# ==============================================================================
def format_seconds(seconds: float | int) -> str:
    """Converte segundos em string de timestamp formatada 'MM:SS' ou 'HH:MM:SS'."""
    total_sec = int(round(seconds))
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    secs = total_sec % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


# ==============================================================================
# Função: fetch_video_metadata_oembed
# O que esta parte faz: Obtém metadados públicos (título e canal/autor) via endpoint oficial oEmbed do YouTube.
# Para que serve / Como funciona no fluxo: Não exige chave de API do Google Cloud nem yt-dlp,
# operando através de uma requisição HTTP simples e rápida com a biblioteca padrão do Python.
# ==============================================================================
def fetch_video_metadata_oembed(video_id: str) -> dict[str, str]:
    """Obtém título e autor do vídeo via oEmbed oficial do YouTube sem autenticação."""
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    req = Request(oembed_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "title": data.get("title", f"Vídeo {video_id}"),
                "channel": data.get("author_name", "Canal do YouTube"),
            }
    except (URLError, Exception):
        return {
            "title": f"Aula do YouTube ({video_id})",
            "channel": "YouTube",
        }


# ==============================================================================
# Função: fetch_transcript_segments
# O que esta parte faz: Conecta-se à API de legendas do YouTube e obtém os trechos falados com tempo.
# Para que serve / Como funciona no fluxo: Prioriza faixas em Português (`pt`), com fallback para
# legendas em Inglês (`en`), legendas automáticas ou qualquer idioma primário disponível.
# ==============================================================================
def fetch_transcript_segments(video_id: str) -> tuple[list[dict[str, Any]], str]:
    """Obtém a lista de trechos da transcrição e o idioma selecionado."""
    ensure_dependencies()
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    # Tentativa de priorização: Português -> Inglês -> Gerada automaticamento -> Primeira disponível
    transcript = None
    lang_code = "desconhecido"

    try:
        transcript = transcript_list.find_transcript(["pt", "pt-BR"])
        lang_code = "pt"
    except Exception:
        try:
            transcript = transcript_list.find_transcript(["en"])
            lang_code = "en"
        except Exception:
            try:
                transcript = transcript_list.find_generated_transcript(["pt", "pt-BR", "en"])
                lang_code = transcript.language_code
            except Exception:
                transcript = next(iter(transcript_list))
                lang_code = getattr(transcript, "language_code", "auto")

    data = transcript.fetch()
    segments = []
    for item in data:
        # Suporta tanto objetos FetchedTranscriptSnippet quanto dicionários legados
        text = getattr(item, "text", item.get("text", "") if isinstance(item, dict) else "")
        start = getattr(item, "start", item.get("start", 0.0) if isinstance(item, dict) else 0.0)
        duration = getattr(item, "duration", item.get("duration", 0.0) if isinstance(item, dict) else 0.0)
        segments.append({
            "text": text.replace("\n", " ").strip(),
            "start": float(start),
            "duration": float(duration),
        })

    return segments, lang_code


# ==============================================================================
# Função: group_segments_into_chunks
# O que esta parte faz: Agrupa pequenas frases de legendas em blocos coerentes com timestamp de início.
# Para que serve / Como funciona no fluxo: Evita linhas fragmentadas de 2 segundos, gerando parágrafos
# ricos e contextuais a cada ~60 segundos ou ~120 palavras, iniciando com `[MM:SS]`.
# ==============================================================================
def group_segments_into_chunks(segments: list[dict[str, Any]], min_words: int = 80, max_interval_sec: float = 60.0) -> list[tuple[str, str]]:
    """Agrupa segmentos curtos em blocos formatados com timestamp inicial [MM:SS]."""
    if not segments:
        return []

    chunks: list[tuple[str, str]] = []
    current_words: list[str] = []
    chunk_start_sec = segments[0]["start"]

    for seg in segments:
        text = seg["text"].strip()
        if not text:
            continue

        if current_words:
            total_words = sum(len(w.split()) for w in current_words)
            time_diff = seg["start"] - chunk_start_sec
            if total_words >= min_words or time_diff >= max_interval_sec:
                ts_label = format_seconds(chunk_start_sec)
                chunks.append((ts_label, " ".join(current_words)))
                current_words = []
                chunk_start_sec = seg["start"]

        current_words.append(text)

    if current_words:
        ts_label = format_seconds(chunk_start_sec)
        chunks.append((ts_label, " ".join(current_words)))

    return chunks


# ==============================================================================
# Função: generate_markdown_transcript
# O que esta parte faz: Monta o documento final em Markdown com metadados e blocos temporais.
# Para que serve / Como funciona no fluxo: Gera a estrutura exata esperada pelo `parse_transcript.py`,
# viabilizando a extração automática de tópicos, minutagens e checkpoints para a aula.
# ==============================================================================
def generate_markdown_transcript(video_id: str, title: str, channel: str, lang: str, segments: list[dict[str, Any]]) -> str:
    """Gera o texto completo da transcrição em formato Markdown estruturado."""
    duration_sec = 0.0
    if segments:
        last = segments[-1]
        duration_sec = last["start"] + last["duration"]

    duration_str = format_seconds(duration_sec)
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    chunks = group_segments_into_chunks(segments)
    body_lines: list[str] = []
    for ts, text in chunks:
        body_lines.append(f"[{ts}] {text}")

    body_text = "\n\n".join(body_lines)

    return f"""# Transcrição: {title}

## 📊 Metadados do Vídeo
- **Título**: {title}
- **Canal**: {channel}
- **URL**: [{video_url}]({video_url})
- **Duração**: {duration_str}
- **Idioma Identificado**: {lang}
- **Data de Transcrição**: {now_str}

---

## 📝 Transcrição Completa

{body_text}
"""


# ==============================================================================
# Bloco CLI: main
# O que esta parte faz: Ponto de entrada CLI para execução no terminal ou por agentes de IA.
# Para que serve / Como funciona no fluxo: Permite que a IA ou o usuário chame
# `python fetch_transcript.py "<URL>" --output transcripts/<id>_<slug>.md`.
# ==============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Baixa e formata transcrições do YouTube em Markdown estruturado com timestamps."
    )
    parser.add_argument("url", help="URL do YouTube ou ID do vídeo.")
    parser.add_argument("--output", "-o", type=Path, help="Caminho opcional do arquivo Markdown para salvar.")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suprime mensagens informativas no stderr.")

    args = parser.parse_args()
    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"[ERRO] URL ou ID do YouTube inválido: '{args.url}'", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"[ai-tutor-video] Buscando metadados para vídeo {video_id}...", file=sys.stderr)

    meta = fetch_video_metadata_oembed(video_id)
    title = meta["title"]
    channel = meta["channel"]

    if not args.quiet:
        print(f"[ai-tutor-video] Extraindo legendas ({channel} - {title})...", file=sys.stderr)

    try:
        segments, lang = fetch_transcript_segments(video_id)
    except Exception as exc:
        print(f"[ERRO] Não foi possível obter legendas para o vídeo {video_id}: {exc}", file=sys.stderr)
        return 1

    markdown_content = generate_markdown_transcript(video_id, title, channel, lang, segments)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown_content, encoding="utf-8")
        if not args.quiet:
            print(f"[ai-tutor-video] Transcrição salva com sucesso em: {args.output}", file=sys.stderr)
    else:
        print(markdown_content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
