#!/usr/bin/env python3
"""Testes unitários para o analisador de transcrições parse_transcript.py."""

import unittest

from scripts.parse_transcript import (
    extract_code_blocks,
    extract_metadata,
    extract_topics,
    parse_transcript,
    seconds_to_timestamp,
    timestamp_to_seconds,
)


SAMPLE_TRANSCRIPT = """# Python POO - Aula 01: O que é Objeto?
- Canal: Curso em Vídeo
- Duração: 28:45
- URL: https://www.youtube.com/watch?v=PLHz_AreHm4dn
- Publicado em: 2024-01-15

[00:00] Introdução e Apresentação do Curso
Olá pessoal, sejam bem-vindos ao curso de Programação Orientada a Objetos.

[05:10] O que é uma Classe e um Objeto
Uma classe é o molde, e o objeto é a instância criada a partir desse molde.
Imagine uma caneta esferográfica como objeto: tem cor, ponta, carga e tampa.

```python
class Caneta:
    def __init__(self, modelo, cor):
        self.modelo = modelo
        self.cor = cor
        self.tampada = True

    def tampar(self):
        self.tampada = True
```

[18:20] Métodos de Ação e Estados
Agora vamos entender como os métodos alteram os estados dos atributos.

[25:00] Desafio Prático da Aula
Crie uma classe Garrafa com capacidade e método encher.
"""


class ParseTranscriptTests(unittest.TestCase):
    def test_timestamp_conversions(self):
        self.assertEqual(timestamp_to_seconds("00:00"), 0)
        self.assertEqual(timestamp_to_seconds("05:10"), 310)
        self.assertEqual(timestamp_to_seconds("28:45"), 1725)
        self.assertEqual(timestamp_to_seconds("01:15:30"), 4530)
        self.assertEqual(timestamp_to_seconds("[18:20]"), 1100)

        self.assertEqual(seconds_to_timestamp(0), "00:00")
        self.assertEqual(seconds_to_timestamp(310), "05:10")
        self.assertEqual(seconds_to_timestamp(1725), "28:45")
        self.assertEqual(seconds_to_timestamp(4530), "01:15:30")

    def test_extract_metadata(self):
        metadata = extract_metadata(SAMPLE_TRANSCRIPT)
        self.assertEqual(metadata["title"], "Python POO - Aula 01: O que é Objeto?")
        self.assertEqual(metadata["channel"], "Curso em Vídeo")
        self.assertEqual(metadata["duration"], "28:45")
        self.assertEqual(metadata["duration_seconds"], 1725)
        self.assertEqual(metadata["video_id"], "PLHz_AreHm4dn")
        self.assertIn("watch?v=PLHz_AreHm4dn", metadata["video_url"])

    def test_extract_code_blocks(self):
        code_blocks = extract_code_blocks(SAMPLE_TRANSCRIPT)
        self.assertEqual(len(code_blocks), 1)
        self.assertEqual(code_blocks[0]["language"], "python")
        self.assertIn("class Caneta:", code_blocks[0]["code"])
        self.assertIn("def tampar(self):", code_blocks[0]["code"])

    def test_extract_topics(self):
        topics = extract_topics(SAMPLE_TRANSCRIPT)
        self.assertEqual(len(topics), 4)

        self.assertEqual(topics[0]["timestamp"], "00:00")
        self.assertEqual(topics[0]["seconds"], 0)
        self.assertEqual(topics[0]["title"], "Introdução e Apresentação do Curso")

        self.assertEqual(topics[1]["timestamp"], "05:10")
        self.assertEqual(topics[1]["seconds"], 310)
        self.assertIn("molde", topics[1]["summary"])

        self.assertEqual(topics[2]["timestamp"], "18:20")
        self.assertEqual(topics[2]["seconds"], 1100)

        self.assertEqual(topics[3]["timestamp"], "25:00")
        self.assertEqual(topics[3]["seconds"], 1500)

    def test_full_parse_transcript(self):
        result = parse_transcript(SAMPLE_TRANSCRIPT, transcript_path="transcripts/aula01.md")
        self.assertEqual(result["video_metadata"]["transcript_path"], "transcripts/aula01.md")
        self.assertEqual(len(result["topics"]), 4)
        self.assertEqual(len(result["code_blocks"]), 1)
        self.assertIn("Introdução e Apresentação do Curso", result["concepts"])
        self.assertIn("O que é uma Classe e um Objeto", result["concepts"])


if __name__ == "__main__":
    unittest.main()
