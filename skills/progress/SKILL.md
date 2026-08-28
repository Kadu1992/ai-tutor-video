---
name: progress
description: Use when updating measured study progress, diagnosing weak points, or receiving the /progress command.
---

# Progress

Você é responsável por manter o histórico de progresso do aluno e orientar o próximo passo com base em dados reais.

## Quando ativada

1. Leia `references/contratos-de-estado.md`.
2. Leia o arquivo `progress.json` (se existir), o `curriculum.md` e o `session-log.md`.
3. Atualize o status de domínio dos tópicos com base no desempenho recente.
4. Identifique:
   - Tópicos dominados
   - Tópicos em andamento
   - Pontos fracos (lacunas recorrentes)
   - Próximo foco recomendado

## Estrutura recomendada do `progress.json`

```json
{
  "tema": "Programação com Python + FastAPI",
  "ultima_atualizacao": "2026-08-28",
  "nivel_geral": "iniciante",
  "topicos": {
    "python_basico": {
      "dominio": 80,
      "status": "dominado",
      "ultima_pratica": "2026-08-27",
      "observacoes": "Boa fluência em loops e funções"
    },
    "http_e_apis": {
      "dominio": 40,
      "status": "em_andamento",
      "ultima_pratica": "2026-08-28",
      "observacoes": "Ainda confunde status codes; falta evidência de aplicação autônoma"
    }
  },
  "pontos_fracos": ["status codes", "tratamento de erros"],
  "proximo_foco": "Criar endpoint GET com tratamento de erro"
}
```

## Regras

- Atualize `dominio` somente para 0, 20, 40, 60, 80 ou 100 e apenas quando as evidências da seção 1 do contrato existirem. Não rebaixe nem aumente por impressão subjetiva.
- Mantenha `evidencias[]` em cada tópico e `historico_sessoes` com `duracao_min` e `topicos_tocados`.
- Priorize os pontos fracos nas recomendações.
- Aplique o ciclo de entrada, atividade e saída de `pontos_fracos` definido na seção 4 do contrato.
- Quando for programação, conecte o progresso aos projetos reais.
- Sempre termine com uma recomendação clara e motivadora do próximo passo.

## Formato de resposta ao aluno

Mostre de forma clara e visual:

- Nível geral atual
- Tópicos dominados
- Pontos fracos
- Próximo foco recomendado
- Progresso no projeto atual (se houver)
