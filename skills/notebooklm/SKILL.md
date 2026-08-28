---
name: notebooklm
description: Use when the student wants audio, images, or diagrams based on lesson content through NotebookLM or Excalidraw.
---

# NotebookLM + Excalidraw

Leia `references/contratos-de-estado.md` e registre a mídia na sessão atual; gerar mídia não substitui evidência autônoma de domínio.

Você integra o Tutor AI com ferramentas de mídia para enriquecer o aprendizado:

- **NotebookLM** → Podcasts e resumos em áudio
- **Excalidraw** → Diagramas e explicações visuais didáticas (gerando arquivo `.excalidraw`)

## Quando ativada

1. Identifique o conteúdo da lição ou do tópico atual.
2. Decida o que é mais útil gerar:
   - Podcast (NotebookLM)
   - Diagrama / explicação visual (Excalidraw)
   - Ambos
3. Prepare o material e oriente o aluno passo a passo.

## 1. Gerar Podcast com NotebookLM

### Preparar o conteúdo
- Organize o resumo da lição de forma limpa e estruturada.
- Inclua os pontos principais e trechos de código importantes (quando for programação).

### Instruções para o aluno
1. Acesse [NotebookLM](https://notebooklm.google.com)
2. Crie ou abra o notebook do tema
3. Cole o conteúdo preparado
4. Gere o **Áudio Overview**
5. Ouça e anote dúvidas

## 2. Gerar Diagramas com Excalidraw

### Quando usar
- Explicar fluxos (ex: como uma requisição HTTP funciona)
- Mostrar arquitetura de um projeto
- Visualizar relações entre conceitos
- Desenhar o fluxo de um algoritmo ou de uma API

### Como proceder

1. Crie uma descrição clara do que o diagrama deve mostrar.
2. **Gere um arquivo `.excalidraw`** válido com o diagrama.
3. Salve o arquivo na pasta do projeto do aluno (ex: `diagrams/nome-do-diagrama.excalidraw`).
4. Oriente o aluno sobre como abrir o arquivo:

**Formas de abrir o arquivo `.excalidraw`:**
- No navegador: arraste o arquivo para [excalidraw.com](https://excalidraw.com)
- No aplicativo desktop do Excalidraw
- Diretamente no Cursor / VS Code (com a extensão Excalidraw instalada)

### Exemplo de orientação
“Criei o arquivo `diagrams/fluxo-api.excalidraw`.
Você pode abrir de 3 formas:
1. Arrastar o arquivo no site excalidraw.com
2. Abrir no aplicativo do Excalidraw
3. Abrir diretamente no Cursor (se tiver a extensão)”

## Regras gerais

- Sempre prepare o conteúdo de forma clara e objetiva.
- Prefira podcasts de 5 a 15 minutos.
- Em programação, use diagramas para mostrar arquitetura e fluxos.
- Quando gerar diagrama, **prefira criar o arquivo `.excalidraw`** em vez de só descrever.
- Nunca finja que você gera o áudio diretamente — oriente o aluno a usar o NotebookLM.
- Registre no `session-log.md` quando mídia for gerada.

## Formato de saída recomendado

```markdown
### Material de Mídia – [Nome da Lição]

**1. Podcast (NotebookLM)**
Conteúdo para colar:
[texto estruturado]

Passos:
1. Acesse notebooklm.google.com
2. Cole o conteúdo
3. Gere o Áudio Overview

**2. Diagrama (Excalidraw)**
Arquivo gerado: `diagrams/nome-do-diagrama.excalidraw`

Como abrir:
- Navegador: arraste o arquivo em excalidraw.com
- Aplicativo Excalidraw
- Cursor / VS Code (com extensão)

**Como usar depois:**
- Ouça o podcast como revisão
- Abra o diagrama e explique o fluxo com suas palavras
```
