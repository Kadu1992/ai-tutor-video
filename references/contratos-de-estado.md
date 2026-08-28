# Contratos de Estado

Este arquivo é a fonte de verdade para `progress.json`, `session-log.md`, `curriculum.md` e `flashcards.md`. Skills que alteram estado devem citar esta referência e não criar critérios próprios.

## 1. Domínio, evidências e erros

`dominio` só pode usar: **0, 20, 40, 60, 80 ou 100**.

| Domínio | Significado observável |
| --- | --- |
| 0 | Ainda não há evidência do aluno. |
| 20 | Reconhece termos ou acompanha uma demonstração com ajuda intensa. |
| 40 | Resolve parte de uma tarefa conhecida com ajuda; ainda confunde passos ou conceitos centrais. |
| 60 | Produz uma explicação ou aplicação padrão de forma autônoma e correta. |
| 80 | Resolve de forma autônoma e transfere o conceito para um contexto novo, justificando as decisões. |
| 100 | Repete o desempenho de 80 em contextos variados, detecta limites e corrige erros sem ajuda. |

Para registrar **60 ou mais**, são necessárias duas evidências independentes, recentes e registradas: uma explicação Feynman e uma aplicação. Para **80 ou mais**, uma das duas deve ser uma transferência para contexto novo. Resposta, código ou solução fornecida pelo tutor não conta como evidência; a nova tentativa autônoma posterior é a evidência.

Na escada de ajuda, uma resposta que exige os degraus 5–6 fica no máximo em 20; uma que exige os degraus 3–4 fica no máximo em 40. Domínio 60+ exige as duas tentativas sem ajuda, depois de o aluno receber apenas o enunciado.

Classifique a principal lacuna encontrada como: `conceitual` (ideia/fato errado), `procedimental` (passos/uso de ferramenta), `aplicacao` (não transfere para um caso), `precisao` (explicação vaga ou incompleta) ou `execucao` (código/teste não funciona). Registre tipo e exemplo em `evidencias[]` ou em `pontos_fracos`.

## 2. Estrutura mínima de tópico

Cada tópico em `progress.json` contém `dominio`, `status`, `ultima_pratica`, `observacoes` e `evidencias[]`. Cada evidência registra `data`, `tipo`, `resultado`, `autonoma`, `erro` e `referencia` (sessão, lição ou projeto).

Use `nao_iniciado` para 0, `em_andamento` para 20–60 e `dominado` para 80–100. Não infira uma data, evidência ou domínio ausentes.

## 3. Sessões

Uma sessão tem `status` igual a `em_andamento`, `concluida` ou `interrompida`. Em `historico_sessoes`, use `duracao_min` e `topicos_tocados`; toda sessão encerrada também registra `passo_atual`, evidências, dificuldades, próximos passos e quais arquivos de estado foram atualizados. Ao retomar, a sessão mais recente em andamento orienta o primeiro passo; uma sessão não pode permanecer em andamento depois de uma saída explícita.

## 4. Ciclo de pontos fracos

Um ponto fraco entra quando o mesmo erro reaparece em duas evidências/sessões ou bloqueia uma evidência de domínio. Enquanto ativo, deve aparecer no próximo foco ou na revisão. Ele sai somente após duas evidências autônomas corretas, em ocasiões diferentes; se o domínio for 60 ou mais, uma delas deve ser transferência. Registre a data de entrada, a causa e a condição de saída.

## 5. Checklist do currículo

Um item só muda de `- [ ]` para `- [x]` quando há: domínio **≥ 80**, evidências exigidas nesta referência, entrada correspondente no `session-log.md` e, para trabalho com código, commit do aluno no projeto. A marcação deve citar a evidência ou o commit. Se qualquer requisito faltar, o item permanece aberto.

## 6. Repetição espaçada

A escada fixa de intervalos, em dias, é **1 → 3 → 7 → 16 → 35 → 60**. Todo card tem `Degrau` de 1 a 6. Card novo inicia no degrau 1; `Acertei` avança um degrau (até 6), `Quase` mantém o degrau e `Errei` volta ao degrau 1. A próxima revisão é a data da revisão mais o intervalo do degrau resultante.

## 7. Regra do gabarito e ajuda

O aluno deve tentar de forma independente antes de ver uma solução. A escada de ajuda é: 1) reformular o enunciado; 2) recuperar pré-requisito; 3) pergunta direcional; 4) pista parcial; 5) esqueleto/pseudocódigo incompleto; 6) solução explicada. No degrau 6, a solução não é evidência: agende uma tarefa equivalente e nova tentativa autônoma.
