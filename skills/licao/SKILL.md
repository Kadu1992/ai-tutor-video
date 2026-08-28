---
name: licao
description: Use when the curriculum has an eligible completed lesson and the student needs the next structured lesson, or requests /licao.
---

# Lição

Os caminhos abaixo são relativos à raiz do estudo. Crie uma lição somente depois de confirmar no `session-log.md` que a lição anterior está `concluida`. Se estiver `interrompida`, retome-a com `session` e não avance. Para a primeira lição, confirme que `curriculum.md` e os quatro arquivos de estado copiados pelo `setup` existem.

Use o nome `lessons/NN-slug-do-topico.md`, com `NN` sequencial de duas casas e o mesmo slug em minúsculas, com hífens, usado no item do currículo. Cada lição contém, nesta ordem:

1. objetivo observável e pré-requisitos;
2. fonte(s) com nome/URL e ligação explícita ao título e item do `curriculum.md`;
3. explicação curta, exemplo concreto e prática guiada;
4. tarefa autônoma, incluindo transferência se o objetivo puder elevar domínio para 60 ou mais;
5. critérios de evidência, erros esperados e atualização de estado.

Não gere a lição seguinte enquanto a atual estiver `em_andamento` ou `interrompida`. A solução dada pelo tutor é material de estudo, não evidência de conclusão. Ao terminar a lição, registre as evidências conforme `references/contratos-de-estado.md` (a partir da raiz do estudo); em programação, direcione o código para `projects/<slug>/` e peça o commit do aluno conforme `references/projetos-e-codigo.md`.
