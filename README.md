
🎓 AI Tutor Video

Transforme seu agente de IA em um tutor que acompanha seus estudos em sincronia com vídeos e plataformas de cursos.

O **AI Tutor Video** combina o aprendizado baseado em evidências (matriz de domínio 0 a 100, escada de ajuda e Feynman) com ingestão automática de aulas do YouTube (via `yt-tool` nativo ou motor embutido universal com auto-instalação `fetch_transcript.py`), checkpoints de pausa em minutos/segundos e sincronização bidirecional com seu portal de cursos (`cursos-estudo`).

Em vez de apenas explicar um assunto ou assistir passivamente a vídeos, ele sabe exatamente onde você parou, extrai os conceitos e analogias da aula e desafia você a aplicar na prática antes de avançar.

Novas capacidades principais:
- 🎬 **Ingestão Autônoma de Vídeos (`/video-sync`):** Baixa e analisa transcrições do YouTube de forma universal. Se o sistema tiver `yt-tool` ele aproveita nativamente; se não tiver, utiliza o extrator embutido `fetch_transcript.py` com instalação silenciosa e sob demanda de dependências.
- ⏱️ **Checkpoints Granulares:** Registra o ponto exato de pausa (`paused_at: "18:20"`, `paused_at_seconds: 1100`), permitindo links clicáveis no YouTube com `&t=...s` e lembrando na abertura da sessão exatamente de onde você parou.
- 🔄 **Sincronização Nativa com SQLite (`pythonway.db`):** Comunicação direta, atômica e instantânea com o banco de dados do portal `cursos-estudo`, sem depender de servidor web aberto.
- 🔌 **Resiliência a Quedas (Crash Recovery):** Persistência turno a turno que garante retomada no segundo exato caso o computador desligue de repente ou a sessão seja interrompida.
- 🛡️ **Rigor Pedagógico Inviolável:** Preserva 100% da matriz de domínio, escada de ajuda e técnica de Feynman — você só avança demonstrando evidências autônomas.

O AI Tutor Video segue o padrão de Agent Skills e pode ser usado em diferentes ambientes, incluindo:

- OpenAI Codex
- Claude Code
- Cursor
- OpenCode
- Google Antigravity IDE

---

🚀 Comece aqui

Você não precisa entender como a skill funciona por dentro para começar.

O caminho é simples:

1. Instale a skill → 2. Escolha o que quer aprender → 3. Comece a estudar

---

1. O que você precisa

Antes de começar, tenha:

- um ambiente compatível: Codex, Claude Code, Cursor ou OpenCode;
- Python 3.11 ou superior;
- Git, caso queira instalar pelo terminal.

O Python é usado internamente pelo AI Tutor para salvar e validar seu progresso.

Você pode verificar sua versão executando:

python --version

ou:

python3 --version

---

2. Instale o AI Tutor Video

### ⚡ Instalação Rápida Universal (Recomendado para qualquer ambiente)

Se você utiliza **Codex, Claude Code, Cursor, OpenCode ou Antigravity IDE**, pode instalar diretamente com um único comando no terminal:

```bash
npx skills add Kadu1992/ai-tutor-video
```

Ou a partir do nosso catálogo central [Kadu Skills Hub](https://github.com/Kadu1992/kadu-skills-hub):
```bash
npx skills add Kadu1992/kadu-skills-hub --skill ai-tutor-video
```

---

### 🛠️ Instalação Manual por Ambiente (Git Clone)

Caso prefira clonar manualmente no diretório de skills do seu editor favorito, escolha abaixo o ambiente que você utiliza.

---

🤖 Codex

macOS ou Linux

Abra o terminal e execute:

mkdir -p ~/.codex/skills

git clone https://github.com/Kadu1992/ai-tutor-video \
  ~/.codex/skills/ai-tutor

Depois reinicie o Codex.

Para usar:

$ai-tutor

Por exemplo:

$ai-tutor

Quero aprender Python do zero.

---

Windows PowerShell

Execute:

New-Item -ItemType Directory -Force "$HOME\.codex\skills"

git clone https://github.com/Kadu1992/ai-tutor-video `
  "$HOME\.codex\skills\ai-tutor"

Depois reinicie o Codex.

---

🟠 Claude Code

O Claude Code procura skills pessoais dentro de:

~/.claude/skills/

macOS ou Linux

Execute:

mkdir -p ~/.claude/skills

git clone https://github.com/Kadu1992/ai-tutor-video \
  ~/.claude/skills/ai-tutor

Depois abra ou reinicie o Claude Code.

Para usar diretamente:

/ai-tutor

Por exemplo:

/ai-tutor

Quero aprender estatística para uma prova daqui a dois meses.

O Claude também pode ativar a skill automaticamente quando perceber que seu pedido corresponde ao AI Tutor.

---

Windows PowerShell

Execute:

New-Item -ItemType Directory -Force "$HOME\.claude\skills"

git clone https://github.com/Kadu1992/ai-tutor-video `
  "$HOME\.claude\skills\ai-tutor"

Depois abra novamente o Claude Code.

---

🟣 Cursor

O Cursor suporta Agent Skills diretamente.

Você pode instalar o AI Tutor de duas maneiras.

Opção 1 — usando o GitHub pelo próprio Cursor

No Cursor:

1. Abra Customize.
2. Vá até Rules.
3. Clique em Add Rule.
4. Escolha Remote Rule (GitHub).
5. Informe o repositório:

https://github.com/Kadu1992/ai-tutor-video

Depois verifique a área Customize → Skills para confirmar que a skill foi reconhecida.

---

Opção 2 — instalação pelo terminal

No macOS ou Linux:

mkdir -p ~/.cursor/skills

git clone https://github.com/Kadu1992/ai-tutor-video \
  ~/.cursor/skills/ai-tutor

No Windows PowerShell:

New-Item -ItemType Directory -Force "$HOME\.cursor\skills"

git clone https://github.com/Kadu1992/ai-tutor-video `
  "$HOME\.cursor\skills\ai-tutor"

Depois reinicie o Cursor.

Para usar, abra o Agent e digite:

/ai-tutor

Você também pode simplesmente conversar normalmente.

Por exemplo:

Quero começar um programa de estudos de Machine Learning.

Use o AI Tutor.

O Cursor pode carregar a skill automaticamente quando ela for relevante.

---

🟦 OpenCode

O OpenCode também suporta Agent Skills baseadas em "SKILL.md".

A pasta global recomendada é:

~/.config/opencode/skills/

macOS ou Linux

Execute:

mkdir -p ~/.config/opencode/skills

git clone https://github.com/Kadu1992/ai-tutor-video \
  ~/.config/opencode/skills/ai-tutor

Depois abra novamente o OpenCode.

---

Windows PowerShell

Execute:

New-Item -ItemType Directory -Force "$HOME\.config\opencode\skills"

git clone https://github.com/Kadu1992/ai-tutor-video `
  "$HOME\.config\opencode\skills\ai-tutor"

O OpenCode identifica as skills disponíveis e pode carregar o AI Tutor quando seu pedido corresponde à descrição da skill.

Por exemplo:

Use a skill ai-tutor.

Quero aprender SQL para trabalhar com análise de dados.

Você também pode simplesmente pedir:

Quero começar um programa de estudos usando o AI Tutor.

---

💡 Dica: Cursor + OpenCode

Cursor e OpenCode também reconhecem a pasta padrão:

~/.agents/skills/

Portanto, se você utiliza Cursor e OpenCode na mesma máquina, pode instalar o AI Tutor uma única vez:

mkdir -p ~/.agents/skills

git clone https://github.com/Kadu1992/ai-tutor-video \
  ~/.agents/skills/ai-tutor

Assim, os dois ambientes podem descobrir a mesma instalação.

---

3. Comece seu primeiro estudo

Depois que a skill estiver instalada, você não precisa criar arquivos, editar JSON ou configurar um currículo manualmente.

Basta conversar com o AI Tutor.

Por exemplo:

Quero aprender Python do zero para conseguir criar pequenas automações.

Tenho aproximadamente 3 horas por semana para estudar.

O tutor fará algumas perguntas para entender coisas como:

- o que você quer aprender;
- qual é seu objetivo;
- quanto tempo você tem disponível;
- seu nível atual;
- onde deseja salvar seu programa de estudos.

Depois disso, ele cria seu plano inicial.

---

🗺️ Seu caminho com o AI Tutor

Depois da configuração inicial, normalmente você seguirá este ciclo:

Configurar estudo
       ↓
Criar seu plano
       ↓
Fazer uma lição
       ↓
Praticar
       ↓
Receber feedback
       ↓
Revisar pontos fracos
       ↓
Acompanhar progresso
       ↓
Próxima lição

Você não precisa decorar comandos.

Pode simplesmente conversar com o tutor.

Por exemplo:

Continue meus estudos.

ou:

O que devo estudar hoje?

ou:

Quero revisar o que estou esquecendo.

---

💬 Comandos úteis

O AI Tutor reconhece algumas intenções específicas:

Comando| Para que serve
"/setup"| Criar um novo programa de estudos
"/video-sync"| Ingerir aula ou playlist do YouTube via yt-tool e mapear conceitos
"/platform-sync"| Sincronizar manualmente com o banco SQLite / portal de cursos
"/session"| Continuar, retomar ou conduzir uma sessão de estudo
"/curriculum"| Ver ou ajustar seu plano de estudos
"/licao"| Fazer a próxima lição ancorada no conteúdo do vídeo
"/review"| Revisar pontos fracos e repetições espaçadas
"/feynman"| Testar se você consegue explicar o conceito com suas próprias palavras
"/flashcards"| Criar ou revisar flashcards
"/progress"| Ver seu progresso medido na matriz de domínio
"/sources"| Procurar e registrar boas fontes de estudo
"/media"| Criar materiais visuais ou multimídia

«Esses atalhos representam intenções do AI Tutor. Dependendo do ambiente, você pode digitá-los diretamente ou simplesmente pedir a mesma coisa em linguagem natural.»

Por exemplo:

Quero ver meu progresso.

tem a mesma intenção de:

/progress

Outro exemplo:

Quero sincronizar com a plataforma.

tem a mesma intenção de:

/platform-sync

---

🔌 Sincronização Local com SQLite & Resiliência a Quedas

### Sincronização Direta com o Portal de Cursos (`pythonway.db`)
O AI Tutor Video sincroniza o seu progresso diretamente com o banco de dados SQLite local (`pythonway.db`), com independência total de rede:
- **Zero Servidores Ligados:** Você não precisa rodar servidores HTTP ou manter terminais abertos enquanto estuda. A gravação e a leitura no SQLite ocorrem diretamente no arquivo em microssegundos.
- **Automático na Entrada e Saída:** Ao iniciar uma sessão (`/session`), o tutor concilia o estado do banco. Ao encerrar ou atingir novos checkpoints, ele persiste as notas pedagógicas, último vídeo assistido e playlists no SQLite. Quando você abrir o portal web mais tarde, tudo já estará atualizado!
- **Modo Híbrido:** Caso utilize um portal web remoto, o comando suporta alternar para requisições HTTP (`--api-url http://...`).

> 💡 **Nota Importante: O uso de SQLite e de interface visual é 100% opcional!**
> - **Modo Padrão (Leve & Autônomo):** Se você só quer estudar no seu editor de código com a IA, não precisa configurar nada. Todo o seu histórico e checkpoints são salvos diretamente em arquivos Markdown e JSON locais (`.ai-tutor/state.json`).
> - **Quer um portal visual com dashboard?** Você não precisa programar nada na mão. Basta pedir diretamente para o seu agente de IA no chat:
>   > *"Crie para mim uma interface web/portal com dashboard em HTML/CSS/JavaScript para acompanhar meu progresso do AI Tutor Video e sincronize com o SQLite local!"*  
>   A própria IA pode gerar a interface web no seu projeto e conectá-la nativamente ao banco `pythonway.db` e ao `scripts/sync_platform.py`, entregando uma plataforma visual completa sob medida para você!

### Proteção Contra Quedas de Energia e Desligamentos (Crash Recovery)
- **Persistência Atômica Turno a Turno:** A cada resposta sua ou desafio prático concluído, o tutor grava os dados no disco.
- **Retomada Inteligente:** Se o computador desligar de repente, na próxima vez que você abrir a IDE e disser *"vamos continuar"*, o tutor detecta a interrupção inesperada, recupera o minuto/segundo exato do vídeo e os conceitos pendentes, garantindo que nenhum progresso seja perdido.

---

🧠 O que é a Técnica de Feynman no AI Tutor?

Inspirada no físico e ganhador do Nobel **Richard Feynman** ("O Grande Explicador"), essa técnica defende que:
> *"Se você não consegue explicar algo de forma simples para um leigo, você não entendeu de verdade."*

Durante as aulas e revisões (`/feynman`), o tutor desafia você a explicar conceitos com suas próprias palavras, sem copiar jargões técnicos prontos. Quando você explica com clareza ou usa uma analogia própria, a evidência é registrada na matriz de domínio e o aprendizado se torna permanente.

---

🧠 O que torna o AI Tutor diferente?

Muitos assistentes de IA conseguem explicar assuntos.

O AI Tutor tenta fazer algo diferente:

acompanhar se você está realmente aprendendo.

Por isso, durante uma sessão ele pode pedir que você:

- explique algo com suas próprias palavras;
- resolva um problema;
- aplique um conceito;
- tente novamente sem ajuda;
- use o que aprendeu em uma situação diferente.

Receber uma explicação do tutor não significa automaticamente que você aprendeu aquele assunto.

Seu progresso aumenta quando você consegue demonstrar conhecimento por conta própria.

---

📈 Como o progresso funciona?

O AI Tutor mantém um histórico do seu programa de estudos.

Ele acompanha coisas como:

Conteúdos estudados
        ↓
Tentativas
        ↓
Evidências
        ↓
Revisões
        ↓
Domínio

Isso permite continuar seus estudos em sessões futuras.

Por exemplo:

Continue de onde paramos.

O tutor tenta recuperar sua última sessão e indicar o próximo passo.

---

📁 Onde meus estudos ficam salvos?

Durante a primeira configuração, o AI Tutor pergunta onde você quer guardar seu programa de estudos.

Por exemplo, no Windows:

C:\Estudos\python

No macOS ou Linux:

~/estudos/python

Essa pasta passa a ser seu diretório de estudos.

Ela pode conter:

- currículo;
- sessões;
- lições;
- projetos;
- flashcards;
- histórico de progresso.

Você normalmente não precisa editar esses arquivos manualmente.

---

🧭 Posso ter mais de um programa de estudos?

Sim.

Você pode ter, por exemplo:

~/estudos/python
~/estudos/ingles
~/estudos/estatistica

Cada diretório representa um programa de estudos independente.

Assim você pode usar o mesmo AI Tutor para aprender assuntos diferentes sem misturar o progresso.

---

🛠️ Está tendo problemas?

A skill não aparece

Primeiro confirme se existe um arquivo:

ai-tutor/SKILL.md

dentro da pasta correta do seu ambiente.

Os caminhos mais comuns são:

Ambiente| Pasta
Codex| "~/.codex/skills/ai-tutor/"
Claude Code| "~/.claude/skills/ai-tutor/"
Cursor| "~/.cursor/skills/ai-tutor/"
OpenCode| "~/.config/opencode/skills/ai-tutor/"
Cursor + OpenCode| "~/.agents/skills/ai-tutor/"

Depois reinicie seu agente.

---

Python não está disponível

Execute:

python --version

ou:

python3 --version

O AI Tutor espera Python 3.11 ou superior.

---

Git não está disponível

Execute:

git --version

Se o comando não funcionar, instale o Git antes de usar os comandos de instalação pelo terminal.

---

Quero atualizar o AI Tutor

Entre na pasta onde instalou a skill.

Por exemplo:

cd ~/.claude/skills/ai-tutor

Depois execute:

git pull

Use o caminho correspondente ao seu ambiente.

---

Quero começar um estudo novo

Peça:

Quero criar um novo programa de estudos.

ou use a intenção:

/setup

Depois escolha uma nova pasta.

Cada pasta representa um programa separado.

---

🎯 Exemplos de uso

Aprender programação

Quero aprender JavaScript para conseguir criar aplicações web.

Sou iniciante e tenho quatro horas por semana.

---

Estudar para uma prova

Quero estudar estatística para uma prova daqui a dois meses.

Tenho dificuldade principalmente com probabilidade.

---

Aprender um assunto profissional

Quero aprender fundamentos de Machine Learning.

Já sei Python, mas nunca trabalhei com modelos de ML.

Meu objetivo é conseguir construir pequenos projetos.

---

Melhorar em algo que você já conhece

Já trabalho com SQL, mas sinto dificuldade com consultas complexas,
CTEs e window functions.

Quero montar um programa de estudos focado nesses pontos.

---

🔬 Para quem quer entender como funciona por dentro

Você não precisa conhecer esta parte para usar o AI Tutor.

Internamente, a skill separa duas áreas:

AI Tutor
│
├── Skill
│   ├── instruções
│   ├── workflows
│   ├── scripts
│   └── regras de aprendizagem
│
└── Seu programa de estudos
    ├── currículo
    ├── sessões
    ├── lições
    ├── projetos
    └── progresso

A instalação contém as regras e ferramentas do tutor.

Seu programa de estudos contém seus próprios dados e progresso.

Isso significa que você pode atualizar a skill sem precisar apagar seu histórico de estudos.

Para detalhes técnicos, consulte:

- "SKILL.md"
- "references/architecture.md"
- "references/state-contract.md"
- "references/learning-contract.md"
- "references/workflows/"

---

👩‍💻 Desenvolvimento

A estrutura principal do projeto é:

ai-tutor-skill/
├── SKILL.md
├── agents/
├── references/
├── assets/
├── scripts/
├── tests/
└── docs/

O arquivo "SKILL.md" é o ponto de entrada utilizado pelos agentes.

Os workflows e contratos técnicos ficam em "references/".

Os scripts responsáveis por inicialização e validação ficam em "scripts/".

Se você pretende modificar a skill, criar novos workflows ou alterar a forma como o progresso é calculado, consulte primeiro a documentação técnica em:

references/
docs/

---

🌐 Compatibilidade

O AI Tutor foi estruturado como uma Agent Skill baseada em "SKILL.md".

Isso permite que o mesmo projeto seja utilizado por diferentes agentes que suportam esse padrão.

A forma como cada ambiente descobre ou ativa skills pode variar, mas a lógica principal do AI Tutor permanece a mesma.

Ambiente| Skill| Ativação
Codex| ✅| "$ai-tutor"
Claude Code| ✅| "/ai-tutor" ou automática
Cursor| ✅| "/ai-tutor" ou automática
OpenCode| ✅| descoberta automática / skill "ai-tutor"

---

⚠️ Limitações

O AI Tutor ajuda a organizar e acompanhar seu aprendizado, mas não substitui professores, instituições de ensino ou especialistas.

O progresso registrado representa evidências observadas durante as sessões e não deve ser interpretado como certificação profissional.

Integrações externas e envio de materiais dependem das permissões disponíveis no ambiente e devem ser autorizados antes do uso.

O comportamento também pode variar ligeiramente entre Codex, Claude Code, Cursor e OpenCode, porque cada agente possui suas próprias ferramentas, permissões e mecanismos de execução.

---

🌱 Status do projeto

O AI Tutor é um projeto educacional em evolução.

O objetivo é tornar o estudo com agentes de IA mais:

estruturado, contínuo, verificável e útil na prática.

Feedback, testes e contribuições são bem-vindos.

---

## 📜 Créditos e Origem

Este projeto é uma evolução direta do trabalho original de **[Lucas Mendes](https://github.com/14lucas-mendes/ai-tutor-skill)**, preservando integralmente sua metodologia pedagógica baseada em evidências, matriz de domínio e escada de ajuda socrática.

A versão **AI Tutor Video** foi concebida e desenvolvida por **[Kadu Amstetter](https://github.com/Kadu1992)**, introduzindo a ingestão autônoma de vídeo-aulas do YouTube (`yt-tool`), checkpoints de pausa em minutos/segundos, testes automatizados e sincronização bidirecional com o catálogo central [Kadu Skills Hub](https://github.com/Kadu1992/kadu-skills-hub).

