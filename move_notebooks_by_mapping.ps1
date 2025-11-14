# Temporary mover: move selected notebooks into project folders and write move_log.csv
$root = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$mapping = @(
    @{ File='Project_5_LLM_Notebook (1).ipynb'; Folder='GenAI\PromptEngineering' },
    @{ File='Project_5_LLM_Notebook (6).ipynb'; Folder='GenAI\PromptEngineering' },

    @{ File='Ensemble_Hands-On_Bagging-2.ipynb'; Folder='ML\Ensemble' },
    @{ File='Ensemble_Hands-On_Boosting_updated.ipynb'; Folder='ML\Ensemble' },
    @{ File='Oversampling_and_undersampling.ipynb'; Folder='ML\Ensemble' },

    @{ File='Case_Study_WineQuality_Prediction_V2-1.ipynb'; Folder='ML\Regression' },
    @{ File='w_AIML_ITP_MLS2_MovieLens_Case_Study.ipynb'; Folder='ML\Regression' },
    @{ File='SLR_W1_PracticeExercise_Question.ipynb'; Folder='ML\Regression' },
    @{ File='K fold cross validation.ipynb'; Folder='ML\Regression' },
    @{ File='Hyperparameter tuning.ipynb'; Folder='ML\Regression' },

    @{ File='Case_Study_DiabetesRisk_Prediction.ipynb'; Folder='ML\Classification' },
    @{ File='Personal_Loan_Campaign_Problem_Statement (2).ipynb'; Folder='ML\Classification' },
    @{ File='Personal_Loan_Campaign_Problem_Statement (3).ipynb'; Folder='ML\Classification' },
    @{ File='SL_MLS1_AnimeRatingPrediction.ipynb'; Folder='ML\Classification' },
    @{ File='Hands_on_K_Means_Clustering.ipynb'; Folder='ML\Classification' },
    @{ File='Hands_on_Notebook_ExploratoryDataAnalysis.ipynb'; Folder='ML\Classification' },
    @{ File='Hands_on_Notebook_Pandas-1.ipynb'; Folder='ML\Classification' }
)

$log = @()
$notebooksDir = Join-Path -Path $root -ChildPath 'Notebooks'
foreach ($m in $mapping) {
    $src = Join-Path -Path $notebooksDir -ChildPath $m.File
    $destDir = Join-Path -Path $root -ChildPath $m.Folder

    if (-not (Test-Path -Path $src)) {
        $log += [pscustomobject]@{ Source=$src; Dest=$destDir; Status='Missing'; Message='Source not found'; Time=(Get-Date) }
        continue
    }

    if (-not (Test-Path -Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }
    $target = Join-Path -Path $destDir -ChildPath $m.File
    try {
        Move-Item -Path $src -Destination $target -Force
        $log += [pscustomobject]@{ Source=$src; Dest=$target; Status='Moved'; Message=''; Time=(Get-Date) }
        Write-Host "Moved: $($m.File) -> $destDir"
    } catch {
        $msg = $_.Exception.Message
        $log += [pscustomobject]@{ Source=$src; Dest=$target; Status='Failed'; Message=$msg; Time=(Get-Date) }
        Write-Host "Failed: $($m.File) -> $destDir : $msg" -ForegroundColor Red
    }
}

$logPath = Join-Path -Path $root -ChildPath 'move_log.csv'
$log | Export-Csv -Path $logPath -NoTypeInformation -Force
Write-Host "Move complete. Log written to: $logPath" -ForegroundColor Cyan
