# Rename all notebooks according to naming conventions
$root = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$renameLog = @()

# Mapping: old name -> new name (based on NAMING_CONVENTIONS.md)
$renameMap = @{
    # GenAI/PromptEngineering/
    'GenAI\PromptEngineering\Project_5_LLM_Notebook (1).ipynb' = 'GenAI\PromptEngineering\GenAI_PromptEngineering_AdvancedLLMTechniques.ipynb'
    
    # GenAI/RAG_Project/
    'GenAI\RAG_Project\Project_5_LLM_Notebook (6).ipynb' = 'GenAI\RAG_Project\GenAI_RAG_DocumentQASystem.ipynb'
    
    # ML/Regression/
    'ML\Regression\Case_Study_WineQuality_Prediction_V2-1.ipynb' = 'ML\Regression\ML_Regression_WineQualityPrediction_v2.ipynb'
    'ML\Regression\w_AIML_ITP_MLS2_MovieLens_Case_Study.ipynb' = 'ML\Regression\ML_Regression_MovieRecommendations.ipynb'
    'ML\Regression\SLR_W1_PracticeExercise_Question.ipynb' = 'ML\Regression\ML_Regression_SimpleLinearRegressionFundamentals.ipynb'
    'ML\Regression\K fold cross validation.ipynb' = 'ML\Regression\ML_Regression_KFoldCrossValidation.ipynb'
    'ML\Regression\Hyperparameter tuning.ipynb' = 'ML\Regression\ML_Regression_HyperparameterTuningGridSearch.ipynb'
    
    # ML/Classification/
    'ML\Classification\Case_Study_DiabetesRisk_Prediction.ipynb' = 'ML\Classification\ML_Classification_DiabetesRiskAssessment.ipynb'
    'ML\Classification\Personal_Loan_Campaign_Problem_Statement (2).ipynb' = 'ML\Classification\ML_Classification_LoanCampaignTargeting_v1.ipynb'
    'ML\Classification\Personal_Loan_Campaign_Problem_Statement (3).ipynb' = 'ML\Classification\ML_Classification_LoanCampaignOptimization_v2.ipynb'
    'ML\Classification\SL_MLS1_AnimeRatingPrediction.ipynb' = 'ML\Classification\ML_Classification_AnimeRatingPrediction.ipynb'
    'ML\Classification\Hands_on_K_Means_Clustering.ipynb' = 'ML\Classification\ML_Classification_KMeansClustering.ipynb'
    'ML\Classification\Hands_on_Notebook_ExploratoryDataAnalysis.ipynb' = 'ML\Classification\ML_Classification_ExploratoryDataAnalysis.ipynb'
    'ML\Classification\Hands_on_Notebook_Pandas-1.ipynb' = 'ML\Classification\ML_Classification_PandasDataManipulation.ipynb'
    
    # ML/Ensemble/
    'ML\Ensemble\Ensemble_Hands-On_Bagging-2.ipynb' = 'ML\Ensemble\ML_Ensemble_BaggingAndBootstrapAggregation.ipynb'
    'ML\Ensemble\Ensemble_Hands-On_Boosting_updated.ipynb' = 'ML\Ensemble\ML_Ensemble_BoostingGradientBoosting.ipynb'
    'ML\Ensemble\Oversampling_and_undersampling.ipynb' = 'ML\Ensemble\ML_Ensemble_ClassImbalanceHandling.ipynb'
    
    # Notebooks/ (General utilities)
    'Notebooks\AIML_ML_Project_solution.ipynb' = 'Notebooks\Utils_MLProjectSolution_Comprehensive.ipynb'
    'Notebooks\Case_Study_Restaurant_Review_Analysis (5)-1.ipynb' = 'Notebooks\NLP_SentimentAnalysis_RestaurantReviews.ipynb'
    'Notebooks\flow_control.ipynb' = 'Notebooks\Tutorial_PythonFlowControl.ipynb'
    'Notebooks\IP_Project_Question_Notebook.ipynb' = 'Notebooks\Utils_ProjectQuestions_AnswersGuide.ipynb'
    'Notebooks\MLS_Apple_HBR (2).ipynb' = 'Notebooks\Utils_CaseStudy_AppleMLSAnalysis_v2.ipynb'
    'Notebooks\MLS_Apple_HBR.ipynb' = 'Notebooks\Utils_CaseStudy_AppleMLSAnalysis_v1.ipynb'
    'Notebooks\MLS_HR_AttritionV2_1.ipynb' = 'Notebooks\ML_Classification_HREmployeeAttritionPrediction.ipynb'
    'Notebooks\Project_1_Introduction_to_Neural_Networks_ReneWind_(1)_(1) (1).ipynb' = 'Notebooks\Tutorial_NeuralNetworks_Introduction_ReneWind.ipynb'
    'Notebooks\Project_3_Advance_Machine_Learning (1).ipynb' = 'Notebooks\ML_AdvancedMachineLearning_Comprehensive_v1.ipynb'
    'Notebooks\Project_3_Advance_Machine_Learning.ipynb' = 'Notebooks\ML_AdvancedMachineLearning_Comprehensive_v2.ipynb'
    'Notebooks\Python_Solution_Notebook_Cred_Pay_Case_Study.ipynb' = 'Notebooks\Utils_CaseStudy_CreditPaymentSolution.ipynb'
    'Notebooks\Python_Week_3(Data Pre Processing).ipynb' = 'Notebooks\Tutorial_DataPreprocessing_Week3.ipynb'
    'Notebooks\PythonVisualization.ipynb' = 'Notebooks\Utils_Visualization_MatplotlibSeaborn.ipynb'
    'Notebooks\Solution_Notebook_Cred_Pay_Case_Study.ipynb' = 'Notebooks\Utils_Solution_CreditPaymentCaseStudy.ipynb'
    'Notebooks\TourismPackage MLOPS and DEPLOYMENT.ipynb' = 'Notebooks\GenAI_MLOps_TourismPackageDeployment.ipynb'
    'Notebooks\TourismPackage_MLOPS_DEPLOYMENT.ipynb' = 'Notebooks\GenAI_MLOps_TourismPackageMLOps.ipynb'
}

Write-Host "Starting notebook rename operation..." -ForegroundColor Cyan
Write-Host "Processing $($renameMap.Count) notebooks" -ForegroundColor Yellow

foreach ($oldName in $renameMap.Keys) {
    $newName = $renameMap[$oldName]
    $oldPath = Join-Path -Path $root -ChildPath $oldName
    $newPath = Join-Path -Path $root -ChildPath $newName
    
    if (-not (Test-Path -Path $oldPath)) {
        $renameLog += [pscustomobject]@{ OldName=$oldName; NewName=$newName; Status='SKIPPED'; Message='File not found'; Time=(Get-Date) }
        Write-Host "SKIP: $oldName (not found)" -ForegroundColor Yellow
        continue
    }
    
    try {
        Rename-Item -Path $oldPath -NewName (Split-Path $newPath -Leaf) -Force
        $renameLog += [pscustomobject]@{ OldName=$oldName; NewName=$newName; Status='RENAMED'; Message=''; Time=(Get-Date) }
        Write-Host "RENAMED: $oldName -> $newName" -ForegroundColor Green
    } catch {
        $msg = $_.Exception.Message
        $renameLog += [pscustomobject]@{ OldName=$oldName; NewName=$newName; Status='FAILED'; Message=$msg; Time=(Get-Date) }
        Write-Host "FAILED: $oldName - $msg" -ForegroundColor Red
    }
}

# Save rename log
$logPath = Join-Path -Path $root -ChildPath 'rename_log.csv'
$renameLog | Export-Csv -Path $logPath -NoTypeInformation -Force
Write-Host "`nRename operation complete. Log saved to: $logPath" -ForegroundColor Cyan
Write-Host "Renamed: $($renameLog | Where-Object { $_.Status -eq 'RENAMED' } | Measure-Object | Select-Object -ExpandProperty Count) notebooks" -ForegroundColor Green
