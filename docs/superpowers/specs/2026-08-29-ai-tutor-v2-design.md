# AI Tutor v2 — Design Arquitetural

## Objetivo

Evoluir `ai-tutor` de um conjunto de instruções acoplado ao diretório atual para uma skill Codex portátil, testável e orientada por contratos. A versão 2 deve preservar a pedagogia baseada em evidências, eliminar ambiguidades de estado e oferecer materiais multimodais locais e integrados ao NotebookLM/Gemini sem tratar mídia produzida pelo tutor como evidência de domínio.

## Escopo

Esta evolução inclui:

- empacotamento da skill em um único ponto de entrada descobrível;
- separação explícita entre a instalação da skill e cada ambiente de estudo;
- schema de estado versionado, IDs estáveis, migração v1 → v2 e validação;
- máquina de estados de sessão e protocolo de atualização consistente;
- consolidação dos contratos de domínio, retenção, pontos fracos e conclusão;
- workflows internos com divulgação progressiva;
- formatos de saída para cards, quizzes, imagens, mapas, gráficos, áudio, vídeo, infográficos e slides;
- integração híbrida com NotebookLM e Notebooks no Gemini;
- testes estruturais, semânticos, de migração e cenários comportamentais.

Não faz parte do escopo:

- armazenar ou automatizar credenciais Google;
- contornar login, permissões, cotas, políticas ou controles de compartilhamento;
- depender de uma API não documentada do NotebookLM;
- transformar consumo de mídia em evidência de aprendizagem;
- construir uma aplicação web ou banco de dados externo.

## Princípios

1. O aluno demonstra domínio; o tutor apenas coleta e classifica evidências.
2. A fonte normativa não pode ser contradita por workflows ou exemplos.
3. Estado persistente deve ser validável, migrável e recuperável.
4. Uma operação externa exige consentimento no momento do envio.
5. Artefatos visuais e multimídia devem ter uma finalidade pedagógica explícita.
6. O funcionamento local é obrigatório; integrações externas são aprimoramentos opcionais.
7. O pacote deve funcionar em Windows, macOS e Linux com Python 3.11+ e biblioteca padrão.

## Arquitetura do pacote

```text
ai-tutor/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── architecture.md
│   ├── learning-contract.md
│   ├── state-contract.md
│   ├── output-contract.md
│   ├── media-providers.md
│   ├── programming.md
│   └── workflows/
│       ├── setup.md
│       ├── session.md
│       ├── curriculum.md
│       ├── lesson.md
│       ├── review.md
│       ├── feynman.md
│       ├── flashcards.md
│       ├── progress.md
│       ├── sources.md
│       └── media.md
├── assets/
│   └── templates/
│       ├── study-config.json
│       ├── state.json
│       ├── curriculum.md
│       ├── session-log.md
│       ├── flashcards.md
│       └── media-index.json
├── scripts/
│   ├── init_study.py
│   ├── validate_skill.py
│   ├── validate_study.py
│   └── migrate_state.py
└── tests/
    ├── test_init_study.py
    ├── test_validate_skill.py
    ├── test_validate_study.py
    ├── test_migrate_state.py
    └── scenarios/
```

`SKILL.md` será o único entrypoint descobrível. Os atuais diretórios `skills/*` serão convertidos em workflows de referência, carregados somente quando o modo correspondente for necessário. Termos como `/setup` e `/review` serão tratados como atalhos conversacionais, não como garantia de comandos registrados pelo runtime.

`agents/openai.yaml` manterá invocação implícita habilitada e descreverá a skill como um programa persistente de aprendizagem. Perguntas educacionais pontuais não deverão iniciar setup nem criar estado.

## Raízes e layout do estudo

Dois caminhos terão papéis distintos:

- `skill_root`: diretório de instalação, somente leitura, onde ficam referências, scripts e assets;
- `study_root`: diretório escolhido explicitamente pelo aluno para um programa de estudo.

O inicializador receberá ambos como argumentos absolutos ou resolverá `skill_root` a partir do próprio script. Ele nunca inferirá `study_root` silenciosamente quando a operação puder criar ou sobrescrever arquivos.

Cada estudo usará:

```text
<study_root>/
├── .ai-tutor/
│   ├── study-config.json
│   ├── state.json
│   ├── media-index.json
│   └── migrations/
├── curriculum.md
├── session-log.md
├── flashcards.md
├── lessons/
├── media/
└── projects/
```

Arquivos sob `.ai-tutor/` são canônicos para estado estruturado. Os documentos Markdown são superfícies humanas e devem conter IDs que permitam reconciliá-los com o estado canônico.

## Modelo de estado v2

Todos os documentos JSON terão `schema_version: 2`. Os IDs usarão prefixos semânticos e UUIDs, por exemplo `topic_<uuid>`, `session_<uuid>`, `evidence_<uuid>`, `lesson_<uuid>`, `card_<uuid>`, `weak_<uuid>` e `media_<uuid>`.

`study-config.json` armazenará:

- tema, objetivo e prazo;
- disponibilidade semanal e horários preferidos;
- nível declarado inicialmente;
- idioma e preferências de acessibilidade;
- política de fontes;
- consentimentos externos, sempre revogáveis;
- caminhos lógicos do estudo.

`state.json` armazenará:

- tópicos e seus níveis de domínio/retensão;
- evidências e referências a sessões, lições, projetos ou commits;
- sessões e transições de estado;
- pontos fracos e suas condições de saída;
- lições e relação muitos-para-muitos com sessões;
- projetos, tarefas e commits informados pelo aluno;
- próximo foco e revisão do estado.

`media-index.json` armazenará metadados de artefatos, nunca o conteúdo binário: tipo, provedor, fontes, objetivo pedagógico, caminho ou URL, estado de geração, data, verificação e acessibilidade.

## Domínio, retenção e evidência

`dominio_demonstrado` continuará na escala 0, 20, 40, 60, 80 e 100:

| Nível | Requisito mínimo |
| --- | --- |
| 0 | Nenhuma evidência válida. |
| 20 | Reconhecimento ou tentativa com ajuda intensa. |
| 40 | Aplicação parcial com ajuda direcional ou pista. |
| 60 | Uma explicação Feynman e uma aplicação padrão, autônomas e independentes. |
| 80 | Requisitos de 60, sendo uma aplicação uma transferência para contexto novo. |
| 100 | Desempenho de 80 repetido em pelo menos duas sessões distintas e dois contextos, incluindo identificação de limites ou autocorreção. |

Evidências são independentes quando avaliam comportamentos diferentes ou ocorrem em tarefas substancialmente diferentes. Para 100, as sessões devem ter IDs distintos. “Recente” significa dentro dos últimos 45 dias; evidência mais antiga continua histórica, mas requer reconfirmação para elevar domínio.

`retencao_atual` será `desconhecida`, `baixa`, `media` ou `alta`. Falhas em revisão alteram retenção e agendam prática, mas não apagam automaticamente domínio demonstrado. O domínio só diminui quando duas evidências autônomas recentes mostram perda consistente da capacidade anteriormente demonstrada.

## Pontos fracos

Um ponto fraco entra quando:

- o mesmo tipo de erro ocorre em duas evidências; ou
- um erro bloqueia uma evidência necessária para domínio.

Ele sai após duas evidências autônomas corretas em sessões diferentes. Para tópicos com domínio 80+, uma delas deve ser transferência. Cada ponto fraco terá ID, tópico, categoria, exemplo, data de entrada, evidências de suporte, condição de saída e estado.

## Máquina de sessões e lições

Estados de sessão:

```text
em_andamento → concluida
em_andamento → interrompida
interrompida → retomada
retomada → concluida
retomada → interrompida
```

Ao retomar, o sistema primeiro procura `em_andamento`; se não houver, procura a sessão `interrompida` mais recente que ainda tenha `resumable: true`. Uma sessão encerrada nunca permanece `em_andamento`.

Lições têm estado próprio: `planejada`, `em_andamento`, `bloqueada`, `concluida` ou `arquivada`. Uma sessão pode tocar várias lições, e uma lição pode atravessar várias sessões. Criar a próxima lição depende do estado da lição atual e das evidências, não apenas do estado de uma sessão.

## Atualização consistente

Uma atualização de estudo seguirá:

1. ler e validar todos os arquivos canônicos;
2. preparar a nova versão em memória;
3. verificar IDs, referências, transições e invariantes;
4. escrever arquivos temporários no mesmo volume;
5. substituir os arquivos canônicos atomicamente;
6. atualizar as representações Markdown;
7. validar novamente e registrar a revisão.

Falha antes da substituição não altera o estado. Falha depois da substituição mantém cópia anterior em `.ai-tutor/migrations/` durante migrações; atualizações ordinárias não acumulam backups indefinidos.

## Migração v1 → v2

`migrate_state.py` será idempotente e oferecerá `--dry-run`. Ele:

- lê os arquivos v1 sem alterá-los;
- cria IDs para entidades existentes;
- preserva texto e datas sem inventar evidências;
- transforma placeholders em ausência de dados, não em registros reais;
- registra campos não mapeados em um relatório;
- escreve v2 somente após validação;
- mantém uma cópia recuperável dos arquivos originais.

Uma segunda execução sobre v2 não altera conteúdo.

## Workflows pedagógicos

O entrypoint encaminhará a intenção para apenas um workflow principal. Workflows podem chamar contratos compartilhados, mas não repetir schemas ou matrizes de domínio.

- `setup`: coleta apenas dados persistidos, permite resposta em lote ou uma pergunta por vez e inicializa o estudo.
- `session`: retoma ou abre sessão, ensina uma ideia por vez, coleta evidência e encerra consistentemente.
- `curriculum`: mantém objetivos observáveis e vincula checklist a IDs de evidência.
- `lesson`: cria conteúdo somente para a próxima lição elegível.
- `feynman`: coleta explicação; não eleva domínio sem aplicação independente.
- `review`: prioriza retenção baixa, cards vencidos e pontos fracos.
- `flashcards`: separa correção objetiva de confiança informada pelo aluno.
- `progress`: mostra domínio, retenção, evidências, incerteza e próximo foco.
- `sources`: exige fonte verificável, URL direta, autoria/instituição, data de acesso e justificativa.
- `media`: seleciona o formato adequado e opera o pipeline local/externo.

## Programação

Projetos continuam recomendados para evidência aplicada, mas não são obrigatórios para toda explicação conceitual. O currículo define quando um projeto é necessário.

Git é exigido apenas quando:

- o estudo ocorre em repositório Git gravável; e
- o checklist declara explicitamente um commit como critério.

Em ambientes sem Git, a evidência usa arquivo, teste executado e hash SHA-256 do conteúdo. O tutor nunca cria o commit no lugar do aluno.

Instruções operacionais serão descritas de forma independente de shell. Exemplos poderão incluir PowerShell e shell POSIX, sem tornar nenhum deles requisito.

## Contrato de saídas educacionais

Todo artefato terá:

- `artifact_id` e `lesson_id`;
- objetivo pedagógico;
- tópicos e fontes vinculadas;
- público/nível;
- formato e caminho;
- texto alternativo ou transcrição quando aplicável;
- perguntas de recuperação ou transferência após o consumo;
- indicação explícita de que o artefato não é evidência.

Formatos locais mínimos:

| Formato | Saída canônica | Fallback |
| --- | --- | --- |
| Cards | JSON + Markdown | Markdown |
| Quiz | JSON + gabarito separado | Markdown |
| Mapa conceitual | Mermaid `.mmd` | Lista hierárquica Markdown |
| Gráfico quantitativo | CSV + especificação Mermaid/JSON | Tabela Markdown |
| Imagem didática | Arquivo de imagem + prompt + alt text | Esboço Mermaid/ASCII |
| Infográfico | Brief estruturado + imagem/PDF quando disponível | Markdown diagramado |
| Slides | Outline + PPTX/PDF quando disponível | Markdown |
| Áudio/vídeo | Manifesto + arquivo ou URL + transcrição | Roteiro Markdown |

Um gráfico só será criado a partir de dados identificáveis. Imagens conceituais não serão usadas para representar valores quantitativos. Todo material visual deverá ser verificável contra as fontes antes de ser marcado `ready`.

## NotebookLM e Notebooks no Gemini

A integração será híbrida e baseada em capacidade.

### Pacote local obrigatório

Para cada geração externa, a skill cria:

```text
media/<lesson-id>/notebooklm/
├── source-pack.md
├── prompts.md
├── manifest.json
└── exports/
```

`source-pack.md` contém somente conteúdo e fontes aprovadas. `prompts.md` contém prompts específicos para áudio, vídeo, cards, quiz, mapa mental, infográfico e slides. `manifest.json` registra fontes, hashes, consentimento e artefatos esperados.

### Automação assistida

Quando houver navegador compatível e sessão Google já autenticada, a skill pode:

1. pedir consentimento para enviar o pacote e indicar quais arquivos serão enviados;
2. abrir NotebookLM;
3. criar ou selecionar um notebook;
4. adicionar fontes e solicitar artefatos;
5. aguardar apenas dentro dos limites do ambiente;
6. registrar URLs ou downloads disponíveis.

A skill não digita senha, não altera configurações de conta e não publica notebooks sem pedido explícito.

### Fallback manual

Sem navegador autenticado, recurso disponível ou consentimento, a skill entrega o pacote, links oficiais e passos manuais. Falta de integração externa nunca bloqueia a sessão de estudo.

### Divisão NotebookLM/Gemini

- NotebookLM é usado para respostas fundamentadas exclusivamente nas fontes e para artefatos do Studio.
- Notebooks no Gemini podem ser usados para conversar com o mesmo notebook e combinar ferramentas adicionais.
- Áudio, vídeo, infográficos e slides são solicitados no NotebookLM, pois esses artefatos não são gerados pelo painel do Gemini.

Referências oficiais consultadas:

- https://support.google.com/notebooklm/answer/16164461
- https://support.google.com/notebooklm/answer/16215270
- https://support.google.com/notebooklm/answer/17003757
- https://support.google.com/notebooklm/answer/16212820
- https://support.google.com/notebooklm/answer/16454555

## Privacidade e segurança

- Upload externo exige consentimento específico e lista de arquivos.
- Materiais com dados pessoais, credenciais, trabalhos sigilosos ou restrições autorais não são enviados automaticamente.
- Links públicos e compartilhamento são ações separadas, nunca implícitas na geração.
- O manifesto registra provedor e data, mas não tokens, cookies ou credenciais.
- Conteúdo gerado externamente deve ser revisado por inexatidões antes de entrar no material de estudo.

## Estratégia de testes

### Testes determinísticos

- validação de frontmatter, nomes e referências alcançáveis;
- ausência de placeholders em assets produtivos;
- inicialização em diretório temporário;
- recusa a sobrescrever estudo existente sem opção explícita;
- schema v2 e integridade de IDs/referências;
- transições válidas e inválidas de sessão/lição;
- critérios exatos de domínio 60/80/100;
- migração v1 → v2, `--dry-run` e idempotência;
- artefatos multimídia com campos de acessibilidade;
- proibição de mídia como evidência;
- execução em caminhos com espaços.

### Cenários comportamentais

Os fixtures cobrirão:

- pedido de uma explicação pontual sem criar estudo;
- setup com respostas em lote;
- retomada de sessão interrompida;
- tentativa de elevar domínio 60 exigindo transferência indevida;
- tentativa de registrar resposta fornecida pelo tutor como evidência;
- falha parcial durante atualização;
- pedido de upload contendo dados sensíveis;
- ausência de navegador autenticado;
- NotebookLM indisponível;
- seleção entre mapa, gráfico e imagem conforme o objetivo.

Testes comportamentais futuros com agentes devem comparar uma linha de base sem a skill e a versão com a skill. Os testes determinísticos não substituirão essa validação de comportamento.

## Compatibilidade e transição

Os atalhos conversacionais atuais serão mantidos. Os arquivos v1 permanecerão reconhecíveis pelo migrador. O antigo `tests/validate-skill.ps1` poderá permanecer como wrapper temporário para o validador Python, mas a lógica normativa viverá em um único lugar.

Arquivos antigos só serão removidos depois que seus conteúdos exclusivos forem transferidos e os testes confirmarem que todas as rotas continuam alcançáveis.

## Critérios de aceite

1. A skill possui um único entrypoint descobrível e referências internas alcançáveis.
2. Um estudo pode ser inicializado em caminho externo ao pacote, inclusive com espaços.
3. Todos os arquivos estruturados usam schema v2 e passam no validador.
4. Migração v1 → v2 é recuperável, não inventa evidência e é idempotente.
5. Sessões interrompidas podem ser retomadas sem bloquear a próxima lição.
6. Domínio 60, 80 e 100 segue exatamente a matriz normativa.
7. Retenção não é confundida com domínio demonstrado.
8. Setup não coleta dados que não serão persistidos.
9. Exemplos e templates produtivos não contêm registros fictícios.
10. A integração NotebookLM/Gemini funciona por automação assistida quando possível e sempre oferece fallback local/manual.
11. Cards, quizzes, mapas, gráficos, imagens, infográficos, slides, áudio e vídeo possuem contratos locais e acessíveis.
12. Nenhum artefato de mídia é aceito como evidência sem nova tentativa autônoma do aluno.
13. A suíte de testes falha diante das contradições identificadas na v1 e passa após a implementação.
14. A validação final deixa o repositório sem arquivos temporários ou artefatos de teste.
