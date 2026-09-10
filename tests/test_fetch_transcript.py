#!/usr/bin/env python3
"""Testes unitários para o utilitário autônomo fetch_transcript.py."""

import unittest
from scripts.fetch_transcript import (
    clean_filename,
    extract_video_id,
    format_seconds,
    generate_markdown_transcript,
    group_segments_into_chunks,
)


class FetchTranscriptTests(unittest.TestCase):
    def test_extract_video_id_formats(self):
        # ID puro de 11 caracteres
        self.assertEqual(extract_video_id("Ej_02ICOIgs"), "Ej_02ICOIgs")

        # URL padrão do YouTube
        self.assertEqual(
            extract_video_id("https://www.youtube.com/watch?v=Ej_02ICOIgs"),
            "Ej_02ICOIgs",
        )

        # URL com parâmetros adicionais
        self.assertEqual(
            extract_video_id("https://www.youtube.com/watch?v=Ej_02ICOIgs&t=120s&list=PL123"),
            "Ej_02ICOIgs",
        )

        # URL encurtada youtu.be
        self.assertEqual(
            extract_video_id("https://youtu.be/Ej_02ICOIgs?t=45"),
            "Ej_02ICOIgs",
        )

        # URL de embed
        self.assertEqual(
            extract_video_id("https://www.youtube.com/embed/Ej_02ICOIgs"),
            "Ej_02ICOIgs",
        )

        # URL de Shorts
        self.assertEqual(
            extract_video_id("https://www.youtube.com/shorts/Ej_02ICOIgs"),
            "Ej_02ICOIgs",
        )

        # Entrada inválida
        self.assertEqual(extract_video_id("https://google.com"), "")
        self.assertEqual(extract_video_id("curto"), "")

    def test_clean_filename(self):
        self.assertEqual(clean_filename("Aula 01: O que é POO?"), "aula_01_o_que_e_poo")
        self.assertEqual(clean_filename("Classes / Objetos & Métodos"), "classes_objetos_metodos")

    def test_format_seconds(self):
        self.assertEqual(format_seconds(0), "00:00")
        self.assertEqual(format_seconds(65), "01:05")
        self.assertEqual(format_seconds(3665), "01:01:05")
        self.assertEqual(format_seconds(7200), "02:00:00")

    def test_group_segments_into_chunks(self):
        segments = [
            {"start": 0.0, "duration": 4.0, "text": "Olá mundo,"},
            {"start": 4.0, "duration": 5.0, "text": "este é um teste de agrupamento."},
            {"start": 70.0, "duration": 6.0, "text": "Agora estamos em outro minuto."},
        ]
        chunks = group_segments_into_chunks(segments, min_words=5, max_interval_sec=50.0)
        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0][0], "00:00")
        self.assertIn("Olá mundo, este é um teste", chunks[0][1])
        self.assertEqual(chunks[1][0], "01:10")

    def test_generate_markdown_transcript(self):
        segments = [
            {"start": 0.0, "duration": 10.0, "text": "Primeiro trecho explicativo sobre classes."},
            {"start": 80.0, "duration": 15.0, "text": "Segundo trecho demonstrando instâncias de objetos."},
        ]
        md = generate_markdown_transcript(
            video_id="Ej_02ICOIgs",
            title="Curso de Python POO",
            channel="Guanabara",
            lang="pt",
            segments=segments,
        )

        self.assertIn("# Transcrição: Curso de Python POO", md)
        self.assertIn("- **Canal**: Guanabara", md)
        self.assertIn("- **URL**: [https://www.youtube.com/watch?v=Ej_02ICOIgs](https://www.youtube.com/watch?v=Ej_02ICOIgs)", md)
        self.assertIn("- **Duração**: 01:35", md)
        self.assertIn("## 📝 Transcrição Completa", md)
        self.assertIn("[00:00]", md)
        self.assertIn("[01:20]", md)


if __name__ == "__main__":
    unittest.main()
