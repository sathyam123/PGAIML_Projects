<#
organize_projects.ps1
PowerShell script to organize files into a project folder structure.

Usage:
  - Dry run (default): Right now script runs in dry-run mode showing what would be moved.
      .\organize_projects.ps1

  - Execute moves: pass the -Execute switch to actually move files.
      .\organize_projects.ps1 -Execute

Notes:
  - The script skips this script, README.md and the destination folders themselves.
  - It's conservative: patterns are based on filename keywords and extensions.
#>

param(
    [switch]$Execute
)

$root = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Set-Location -Path $root

# Destination folders (relative)
$dest = @{
    'GenAI\RAG_Project'      = @('rag','rag_project')
    'GenAI\PromptEngineering'= @('prompt','promptengineering')
    'GenAI\Summarization'    = @('summar','summary','summarization')

    'ML\Regression'          = @('regress','regression')
    'ML\Classification'      = @('classif','classification')
    'ML\Ensemble'            = @('ensemble','bagging','boosting')

    'NLP\TextCleaning'       = @('clean','textclean','text_clean')
    'NLP\TFIDF'              = @('tfidf')
    'NLP\ClassicalNLP'       = @('nlp','classical')

    'Datasets'                = @('.csv','.xls','.xlsx','.json','.parquet')
    'Notebooks'               = @('.ipynb')
}

# Exclude these items from processing
$exclude = @('organize_projects.ps1','README.ORGANIZE.md','README.md')

# Build list of files in root (non-recursive)
$items = Get-ChildItem -File -Force | Where-Object { -not ($exclude -contains $_.Name) }

if ($items.Count -eq 0) {
    Write-Host "No files found in root to organize." -ForegroundColor Yellow
    return
}

# Prepare moves
$moves = @()
foreach ($it in $items) {
    $lower = $it.Name.ToLower()
    $moved = $false

    foreach ($kv in $dest.GetEnumerator()) {
        $folder = $kv.Key
        $patterns = $kv.Value

        foreach ($p in $patterns) {
            if ($p.StartsWith('.')) {
                if ($lower.EndsWith($p)) {
                    $moves += [pscustomobject]@{ Source=$it.FullName; Dest=Join-Path -Path $root -ChildPath $folder; FileName=$it.Name }
                    $moved = $true; break
                }
            } else {
                if ($lower -like "*$p*") {
                    $moves += [pscustomobject]@{ Source=$it.FullName; Dest=Join-Path -Path $root -ChildPath $folder; FileName=$it.Name }
                    $moved = $true; break
                }
            }
        }
        if ($moved) { break }
    }

    # Fallback: put unknown CSV-like into Datasets, IPYNB into Notebooks; otherwise leave at root
    if (-not $moved) {
        if ($lower -match '\.ipynb$') {
            $moves += [pscustomobject]@{ Source=$it.FullName; Dest=Join-Path -Path $root -ChildPath 'Notebooks'; FileName=$it.Name }
        } elseif ($lower -match '\.(csv|xls|xlsx|json|parquet)$') {
            $moves += [pscustomobject]@{ Source=$it.FullName; Dest=Join-Path -Path $root -ChildPath 'Datasets'; FileName=$it.Name }
        }
    }
}

if ($moves.Count -eq 0) {
    Write-Host "No matching moves identified by the rules. Review patterns in the script." -ForegroundColor Yellow
    return
}

Write-Host "Planned moves:" -ForegroundColor Cyan
$moves | ForEach-Object { Write-Host ("{0} -> {1}" -f $_.FileName, $_.Dest) }

if (-not $Execute) {
    Write-Host ""
    Write-Host "Dry run mode. No files were moved. To apply changes run:" -ForegroundColor Green
    Write-Host "  .\organize_projects.ps1 -Execute" -ForegroundColor Green
    return
}

# Execute moves
foreach ($m in $moves) {
    if (-not (Test-Path -Path $m.Dest)) { New-Item -ItemType Directory -Path $m.Dest | Out-Null }
    $target = Join-Path -Path $m.Dest -ChildPath $m.FileName
    try {
        Move-Item -Path $m.Source -Destination $target -Force
        Write-Host "Moved: $($m.FileName) -> $m.Dest" -ForegroundColor Green
    } catch {
        Write-Host "Failed to move $($m.FileName): $_" -ForegroundColor Red
    }
}

Write-Host "Organization complete." -ForegroundColor Cyan
