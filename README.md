# AI Tutor

[![Validate](https://github.com/14lucas-mendes/ai-tutor-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/14lucas-mendes/ai-tutor-skill/actions/workflows/validate.yml)

Uma skill do Codex para criar e conduzir programas de aprendizagem persistentes, baseados em evidências observáveis e progresso validável.

## Por que esta skill foi criada

Ferramentas de IA explicam conteúdos rapidamente, mas uma explicação recebida não prova que a pessoa aprendeu. O AI Tutor foi criado para transformar o uso de IA em um processo de estudo contínuo: o aluno tenta, aplica, recebe feedback e acumula evidências autônomas em um estado persistente.

O projeto também existe como um laboratório educacional para evoluir práticas de engenharia de IA, contratos de estado, validação, documentação e integração responsável com ferramentas externas.

## Objetivos

- Criar um programa de estudo durável, com currículo, sessões, lições e revisões.
- Medir domínio por comportamentos demonstrados, e não por consumo de material.
- Manter o estado estruturado consistente, migrável e recuperável.
- Usar projetos e aplicações transferidas para aproximar estudo e prática profissional.
- Produzir materiais multimodais com finalidade pedagógica explícita, sem confundi-los com evidência.
- Melhorar continuamente a skill por meio de testes, cenários comportamentais e revisão humana.

## O que a skill faz

O entrypoint [SKILL.md](SKILL.md) roteia a intenção para workflows especializados:

| Necessidade | Atalho conversacional | Resultado |
| --- | --- | --- |
| Iniciar um programa | `/setup` | Configuração confirmada e estudo inicializado |
| Planejar ou revisar o currículo | `/curriculum` | Objetivos observáveis e checklist |
| Criar a próxima lição | `/licao` | Lição elegível vinculada ao estado |
| Revisar pontos fracos | `/review` | Prática priorizada por retenção e dificuldade |
| Testar uma explicação | `/feynman` | Explicação autônoma avaliada |
| Criar ou revisar cards | `/flashcards` | Recuperação espaçada com confiança separada |
| Ver progresso | `/progress` | Domínio, retenção, evidências e próximo foco |
| Pesquisar fontes | `/sources` | Fontes verificáveis e justificadas |
| Criar mídia de estudo | `/media` | Artefato local ou integração externa com fallback |

Para continuar uma sessão, use uma mensagem como “continue de onde paramos”. O tutor retoma a sessão interrompida mais recente quando ela for recuperável.

## Como funciona

### Duas raízes com responsabilidades diferentes

- `skill_root`: instalação da skill, contendo instruções, referências, scripts e templates. Deve ser tratado como somente leitura.
- `study_root`: diretório escolhido explicitamente para um programa de estudo. É onde ficam o currículo, sessões, lições, projetos e estado canônico.

O estado estruturado vive em `.ai-tutor/*.json`. Os arquivos Markdown são projeções legíveis e carregam IDs que permitem reconciliá-los com o estado canônico.

### Domínio demonstrado

| Nível | Evidência mínima |
| --- | --- |
| 20 | Reconhecimento ou tentativa com ajuda intensa |
| 40 | Aplicação parcial com pista ou ajuda direcional |
| 60 | Explicação Feynman e aplicação padrão, autônomas e independentes |
| 80 | Requisitos de 60 mais uma aplicação transferida para contexto novo |
| 100 | Desempenho de 80 repetido em duas sessões e contextos, com limite ou autocorreção |

Conteúdo fornecido pelo tutor, cards gerados e mídia não são evidência de domínio. Uma nova tentativa autônoma pode ser registrada conforme o nível de ajuda utilizado.

### Avaliação das respostas

O tutor avalia ideia central, contexto, justificativa observável, limites relevantes, autocorreção após feedback e leitura literal. Não exige palavras exatas, não transforma omissões opcionais em erros e não infere afirmações que o aluno não fez. A regra normativa completa está em [references/learning-contract.md](references/learning-contract.md).

## Quick start

### Pré-requisitos

- Python 3.11 ou superior.
- Git para contribuir com o código-fonte.
- Um ambiente de chat/agente que carregue a skill `ai-tutor`.

### Inicializar um estudo

No PowerShell, a partir da raiz deste repositório:

```powershell
$config = @'
{
  "topic": "Fundamentos de Python",
  "goal": "Construir automações pequenas com testes",
  "deadline": "sem prazo rígido",
  "weekly_hours": 3,
  "preferred_times": ["flexível"],
  "initial_level": "básico",
  "language": "pt-BR",
  "accessibility": {},
  "source_policy": {"mode": "official_primary"}
}
'@

python .\scripts\init_study.py `
  --study-root 'C:\Estudos\meu-ai-tutor' `
  --config-json $config

python .\scripts\validate_study.py 'C:\Estudos\meu-ai-tutor'
```

Depois, carregue a skill no seu ambiente de chat e peça para iniciar ou continuar o estudo. O diretório de estudo pode ficar fora do repositório da skill.

## Estrutura do projeto

```text
ai-tutor-skill/
├── SKILL.md                         # entrypoint descobrível
├── agents/openai.yaml               # metadados de invocação
├── references/                      # contratos e workflows
├── assets/templates/                # templates sem estado fictício
├── scripts/                         # inicialização, validação e migração
├── tests/                           # testes determinísticos e cenários
├── docs/superpowers/specs/          # decisões arquiteturais
├── README.md                        # esta documentação
├── CONTRIBUTING.md                  # fluxo de contribuição
├── CHANGELOG.md                     # histórico de mudanças
└── VERSION                          # versão SemVer do projeto
```

## Segurança e limites

- A skill não presume acesso irrestrito a arquivos locais: operações dependem do ambiente, das permissões e da autorização aplicável.
- Upload externo exige consentimento específico no momento do envio e identificação dos arquivos.
- Credenciais, cookies e tokens não são manipulados pela skill.
- Links públicos e compartilhamento são ações separadas da geração de material.
- Artefatos externos devem ser revisados antes de entrar no material de estudo.
- O AI Tutor organiza aprendizagem; não certifica competência profissional nem substitui revisão especializada.

## Contribuição e melhoria contínua

Leia [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir uma alteração. Em resumo:

1. Abra uma issue ou descreva claramente o problema.
2. Crie uma branch pequena e focada.
3. Atualize contrato, workflow, teste ou documentação no local correto.
4. Execute a suíte de testes e os validadores.
5. Abra um pull request com evidências e impacto.

Mudanças de comportamento devem incluir um cenário em `tests/scenarios/behavioral.json` quando aplicável. A melhoria contínua deve preservar os limites pedagógicos e de segurança já definidos, em vez de acumular regras específicas para um único exemplo.

## Versionamento e releases

O projeto segue [Semantic Versioning](https://semver.org/). A versão atual está em [VERSION](VERSION), e o histórico fica em [CHANGELOG.md](CHANGELOG.md). O workflow de release valida a tag `vX.Y.Z` contra `VERSION` e só cria a GitHub Release depois de executar os testes.

O procedimento detalhado está em [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Projeto educacional em evolução. A arquitetura v2 está implementada, e novas mudanças devem ser pequenas, testáveis e justificadas por uma necessidade real de aprendizagem, confiabilidade ou manutenção.
