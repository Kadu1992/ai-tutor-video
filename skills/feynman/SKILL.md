---
name: feynman
description: Use when the student requests /feynman or needs to explain an important concept in their own words to verify understanding.
---

# Feynman

Leia `references/contratos-de-estado.md` antes de registrar qualquer domínio.

Você aplica a Técnica de Feynman para garantir que o aluno realmente entendeu o conceito.

## Como aplicar

1. Peça ao aluno que explique o conceito **como se estivesse ensinando para uma criança de 12 anos** (ou para alguém que não sabe nada sobre o assunto).
2. Avalie a explicação com estes critérios:
   - Clareza
   - Precisão
   - Completude
   - Uso de exemplos concretos
3. Se a explicação estiver boa, peça também uma aplicação autônoma; para domínio ≥ 60, peça transferência para contexto novo:
   - Elogie o que ficou claro
   - Aponte pequenos refinamentos (se houver)
   - Registre a explicação e a aplicação como evidências independentes. Só use os níveis e condições do contrato; “boa” não é um status numérico por si só.
4. Se a explicação tiver lacunas:
   - Aponte exatamente onde está a confusão (sem dar a resposta pronta)
   - Classifique o erro (`conceitual`, `procedimental`, `aplicacao`, `precisao` ou `execucao`)
   - Faça perguntas guiadas para o aluno descobrir o erro
   - Só explique de novo depois que o aluno tentar corrigir
5. Ao final, peça uma nova versão da explicação (mais curta e clara).

## Regras

- Nunca aceite uma explicação superficial.
- Prefira que o aluno use analogias e exemplos do próprio projeto (especialmente em programação).
- Seja paciente, mas firme: o objetivo é o entendimento real, não a memorização.
- Atualize o `progress.json` e o `session-log.md` após a aplicação da técnica, incluindo `evidencias[]`; a solução dada pelo tutor nunca conta como evidência.

## Formato de interação recomendado

1. “Explique [conceito] como se estivesse ensinando para alguém que nunca ouviu falar disso.”
2. Avalie e dê feedback.
3. Peça a versão melhorada.
4. Confirme o domínio somente se as duas evidências exigidas pelo contrato estiverem presentes; caso contrário, registre o nível atual e a próxima evidência necessária.
