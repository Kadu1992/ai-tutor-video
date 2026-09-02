# Contribuindo com o AI Tutor

Obrigado por ajudar a evoluir uma skill que trata aprendizagem como um processo verificável. Este repositório contém instruções, contratos, scripts e testes; não é uma aplicação web nem um diretório de estudos de um aluno.

## Antes de começar

Instale:

- Python 3.11 ou superior.
- Git.
- PowerShell no Windows ou um shell POSIX equivalente.

Clone o repositório e entre nele:

```powershell
git clone https://github.com/14lucas-mendes/ai-tutor-skill.git
Set-Location -LiteralPath .\ai-tutor-skill
```

Não instale dependências globais. Os scripts usam a biblioteca padrão do Python.

## Onde fazer cada mudança

- `SKILL.md`: propósito, limites e roteamento essencial da skill.
- `references/learning-contract.md`: regras normativas de domínio, evidência, retenção e avaliação.
- `references/workflows/`: procedimentos específicos carregados conforme a intenção.
- `scripts/`: operações determinísticas que precisam ser repetíveis.
- `assets/templates/`: arquivos iniciais sem registros de estudo fictícios.
- `tests/`: testes determinísticos e catálogo de cenários comportamentais.
- `docs/superpowers/specs/`: decisões arquiteturais e contratos de alto nível.

Evite duplicar uma regra normativa em vários workflows. Se uma mudança altera o significado de evidência ou domínio, atualize primeiro o contrato correspondente e depois ajuste os consumidores.

## Validação local

Execute da raiz do repositório:

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/validate_skill.py .
python -m compileall -q scripts tests
```

Antes de enviar uma mudança, verifique também:

```powershell
git diff --check
git status --short
```

O GitHub Actions executa os mesmos gates em Ubuntu, Windows e macOS.

## Mudanças de comportamento

Quando a alteração muda como o tutor decide, registra evidência ou escolhe um workflow:

1. Descreva o comportamento esperado e o risco que motivou a mudança.
2. Adicione ou atualize um cenário em `tests/scenarios/behavioral.json`.
3. Crie um teste determinístico para invariantes que possam ser verificadas por código.
4. Faça uma tentativa de linha de base quando a mudança for comportamental e sensível a interpretação.
5. Verifique que a matriz de domínio e a escada de ajuda continuam intactas.

Uma resposta correta não precisa repetir palavras exatas. Não transforme uma omissão opcional em falha e não infira permissões, acesso ou intenções que não aparecem no texto.

## Branches e commits

Use uma branch descritiva e curta:

- `docs/...` para documentação;
- `fix/...` para correções;
- `feat/...` para comportamento novo;
- `test/...` para cobertura;
- `ci/...` para automação.

Prefira mensagens de commit no formato Conventional Commits, por exemplo:

```text
docs: explain study initialization
fix: preserve literal response assessment
ci: validate skill on supported platforms
```

Não inclua em commits arquivos de estudos pessoais, credenciais, tokens, cookies, diretórios `.venv`, `__pycache__` ou artefatos gerados.

## Pull requests

Um pull request deve:

- explicar o problema e a decisão tomada;
- apontar os arquivos normativos afetados;
- informar testes e validadores executados;
- registrar riscos, limites e eventuais incompatibilidades;
- manter o escopo pequeno o suficiente para revisão.

Checklist recomendado:

- [ ] A documentação foi atualizada quando o comportamento mudou.
- [ ] Os testes locais passaram.
- [ ] `validate_skill.py` passou.
- [ ] Não há segredos, caminhos pessoais ou arquivos temporários.
- [ ] A mudança não transforma material fornecido pelo tutor em evidência.

## Releases

1. Atualize `VERSION` com a próxima versão SemVer.
2. Mova as mudanças de `Unreleased` para uma seção numerada em `CHANGELOG.md`.
3. Execute todos os gates locais.
4. Crie um commit com a alteração de versão.
5. Crie e envie uma tag anotada no formato `vX.Y.Z`:

```powershell
git tag -a v0.1.0 -m "release: v0.1.0"
git push origin v0.1.0
```

O workflow `.github/workflows/release.yml` confere a versão e cria a GitHub Release automaticamente após os testes. Nunca reutilize uma tag publicada.

## Segurança e reporte responsável

Não envie credenciais ou dados de estudo em issues e pull requests. Para uma vulnerabilidade que possa expor conteúdo, permissões ou tokens, descreva o problema de forma privada ao mantenedor antes de publicar detalhes.
