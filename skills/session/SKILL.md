---
name: session
description: Use when conducting or continuing a study session, especially when the student says they want to continue studying.
---

# Session

Conduza uma sessão completa e persistente. Leia `references/contratos-de-estado.md` antes de alterar estado.

## 0. Retomar

Antes de fazer qualquer pergunta, leia `progress.json`, `session-log.md` e `curriculum.md`; depois leia a lição, os flashcards e o projeto relevantes. Encontre a sessão mais recente `em_andamento`, seu próximo passo, `passo_atual`/checkpoint, pontos fracos e o último tópico tocado. Se houver sessão em andamento, retome esse ponto; não reinicie o Probe. Se não houver, abra uma nova sessão e registre seu objetivo.

## 1–5. Conduzir

1. **Probe:** faça uma pergunta por vez para confirmar o estado recuperado.
2. **Plan:** defina um objetivo observável e, em programação, a tarefa em `projects/<slug>/`.
3. **Teach:** ensine uma ideia por vez, do concreto ao abstrato.
4. **Verify:** exija uma tentativa autônoma de explicação, aplicação ou código. Para domínio ≥ 60, inclua transferência a um contexto novo. Classifique erros conforme o contrato.
5. **Review:** registre evidências independentes em `progress.json`/`evidencias[]`, atualize pontos fracos e flashcards, e defina o próximo foco.

### Regra do Gabarito

O aluno tenta antes de receber resposta. Se travar, use a escada de ajuda do contrato, do menor auxílio à solução explicada. Uma solução fornecida pelo tutor nunca conta como evidência; depois dela, peça uma tarefa equivalente com tentativa autônoma.

Em programação, salve o código em `projects/<slug>/`, revise-o com `references/projetos-e-codigo.md` e peça o commit do aluno antes de fechar item curricular.

## 6. Encerrar

Ao concluir ou interromper, atualize o `session-log.md` com status (`concluida` ou `interrompida`), início/fim, `duracao_min`, `topicos_tocados`, `passo_atual`/checkpoint, evidências, dificuldades, próximo passo e arquivos atualizados. Atualize `progress.json` e `historico_sessoes`; atualize currículo e flashcards quando aplicável. Uma sessão interrompida pode ser retomada no passo exato registrado. Nunca deixe uma sessão encerrada como `em_andamento`.

## Se o aluno travar

Reduza a tarefa para o menor passo verificável, mas preserve a tentativa autônoma e a regra do gabarito. Não transforme uma resposta guiada em evidência independente.
