# Projetos e Código

Esta referência define o fluxo de programação do tutor.

## Endereço do projeto

Cada projeto do aluno fica em `projects/<slug>/`, com `<slug>` em minúsculas, hífens e sem espaços. Crie apenas a estrutura necessária ao projeto; use `src/` para código de aplicação e `tests/` para testes quando existirem.

No PowerShell:

```powershell
New-Item -ItemType Directory -Force projects/<slug>/src, projects/<slug>/tests
Set-Location projects/<slug>
```

O código submetido pelo aluno deve ser salvo nesse projeto antes de contar como evidência. O tutor registra em qual arquivo e tarefa a evidência ocorreu.

## Git é trabalho do aluno

O repositório de estudo é versionado desde o início. Ao concluir uma tarefa de código, o aluno revisa as mudanças, testa e cria o commit:

```powershell
git status
git add projects/<slug>
git commit -m "feat(<slug>): <tarefa concluída>"
```

O tutor explica e pede o commit; não o cria em nome do aluno. Sem o hash ou a confirmação do commit, a tarefa de código não fecha o checklist curricular.

## Revisão de código

Avalie exatamente estes sete pontos, registrando apenas os relevantes:

1. A tarefa e os critérios de aceite foram atendidos.
2. O código executa e produz o comportamento esperado.
3. Testes existem quando cabíveis e passam.
4. Casos de erro e bordas relevantes foram considerados.
5. Nomes, estrutura e legibilidade ajudam manutenção.
6. O código não duplica nem adiciona complexidade desnecessária.
7. A alteração está restrita à tarefa e pronta para commit.

O feedback tem três blocos, com no máximo três itens em cada: **O que funcionou**, **O que ajustar** e **Próximo passo**. Cada ajuste aponta arquivo/trecho, impacto e uma ação verificável.
