$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
& python "$root/scripts/validate_skill.py" $root
if ($LASTEXITCODE -ne 0) { throw "Skill validation failed with exit code $LASTEXITCODE" }
