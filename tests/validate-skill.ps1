$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$checks = @()

function Check([string]$name, [scriptblock]$test) {
  $result = & $test | Select-Object -Last 1
  if (-not [bool]$result) { throw "FAIL: $name" }
  $script:checks += $name
  Write-Output "PASS: $name"
}

Check 'contratos normativos' {
  (Test-Path "$root/references/contratos-de-estado.md") -and
  (Test-Path "$root/references/projetos-e-codigo.md") -and
  ((Get-Content -Raw "$root/references/contratos-de-estado.md") -match '0, 20, 40, 60, 80 ou 100')
}

Check 'retomar e encerrar' {
  $s = Get-Content -Raw "$root/skills/session/SKILL.md"
  $s -match '## 0\. Retomar' -and $s -match '## 6\. Encerrar' -and
  $s -match 'progress\.json.*session-log\.md.*curriculum\.md'
}

Check 'roteamento completo' {
  $s = Get-Content -Raw "$root/SKILL.md"
  $missing = @('/setup','/curriculum','/progress','/review','/feynman','/flashcards','/licao','/sources','/notebooklm') |
    ForEach-Object { $s -match [regex]::Escape($_) } | Where-Object { -not $_ }
  $missing.Count -eq 0
}

Check 'schemas sincronizados' {
  $p = Get-Content -Raw "$root/templates/progress-template.json" | ConvertFrom-Json
  ($p.topicos.exemplo_topico.PSObject.Properties.Name -contains 'evidencias') -and
  ((Get-Content -Raw "$root/references/contratos-de-estado.md") -match 'duracao_min') -and
  ((Get-Content -Raw "$root/references/contratos-de-estado.md") -match 'topicos_tocados')
}

Check 'escada espacada' {
  $s = Get-Content -Raw "$root/references/contratos-de-estado.md"
  $s -match '1.*3.*7.*16.*35.*60' -and
  (Get-Content -Raw "$root/templates/flashcards-template.md") -match '\*\*Degrau:\*\*'
}

Check 'projetos e revisão' {
  $s = Get-Content -Raw "$root/references/projetos-e-codigo.md"
  ($s -match 'projects/<slug>/') -and ($s -match 'git commit') -and (($s -split "`n" | Where-Object { $_ -match '^\d+\. ' }).Count -eq 7)
}

Check 'skills novas e frontmatter' {
  (Test-Path "$root/skills/review/SKILL.md") -and (Test-Path "$root/skills/licao/SKILL.md") -and
  ((Get-ChildItem "$root/skills" -Recurse -Filter SKILL.md | ForEach-Object { (Get-Content -Raw $_.FullName) -match 'description: Use when' } | Where-Object { -not $_ }).Count -eq 0)
}

Write-Output "VALIDAÇÃO: $($checks.Count)/7"
