# Notebook Naming Conventions Guide

This document establishes consistent, meaningful naming conventions for all Jupyter notebooks across the AIML repository to improve discoverability, organization, and professional presentation.

---

## 📋 Naming Convention Format

### Basic Structure
```
[Category]_[ProjectType]_[Description]_[Version].ipynb
```

### Components

| Component | Purpose | Examples |
|-----------|---------|----------|
| **Category** | Domain/folder shorthand | `ML`, `NLP`, `GenAI`, `Utils` |
| **ProjectType** | Type of ML/AI task | `Regression`, `Classification`, `Clustering`, `RAG`, `Prompt`, `TextClean` |
| **Description** | Clear, specific project name | `WineQualityPrediction`, `DiabetesRiskAssessment`, `TextCleaning` |
| **Version** | Optional version/iteration | `v1`, `v2`, `Final`, `Updated` (omit if not needed) |

---

## 🏷️ Category Prefixes

| Prefix | Folder | Use Case |
|--------|--------|----------|
| `ML_` | ML/** | Machine Learning projects |
| `NLP_` | NLP/** | Natural Language Processing |
| `GenAI_` | GenAI/** | Generative AI, LLMs, RAG |
| `Utils_` | Notebooks/ | Utility scripts, tutorials, helpers |
| `EDA_` | Notebooks/ | Exploratory Data Analysis |
| `Tutorial_` | Notebooks/ | Educational/learning notebooks |

---

## 🎯 Project Type Suffixes

### Machine Learning
| Type | Usage | Examples |
|------|-------|----------|
| `Regression` | Linear/non-linear regression tasks | `ML_Regression_WineQualityPrediction.ipynb` |
| `Classification` | Binary/multi-class classification | `ML_Classification_DiabetesRiskAssessment.ipynb` |
| `Clustering` | Unsupervised clustering tasks | `ML_Clustering_CustomerSegmentation.ipynb` |
| `Ensemble` | Bagging, boosting, stacking | `ML_Ensemble_BaggingAndBoosting.ipynb` |
| `HyperparameterTuning` | Model optimization | `ML_HyperparameterTuning_GridSearch.ipynb` |
| `CrossValidation` | CV techniques and evaluation | `ML_CrossValidation_KFoldAnalysis.ipynb` |

### NLP
| Type | Usage | Examples |
|------|-------|----------|
| `TextCleaning` | Preprocessing and normalization | `NLP_TextCleaning_StandardPipeline.ipynb` |
| `TFIDF` | TF-IDF vectorization | `NLP_TFIDF_FeatureExtraction.ipynb` |
| `SentimentAnalysis` | Sentiment classification | `NLP_SentimentAnalysis_Reviews.ipynb` |
| `NamedEntityRecognition` | NER tasks | `NLP_NER_EntityExtraction.ipynb` |
| `ClassicalNLP` | Traditional NLP methods | `NLP_ClassicalNLP_POSTagging.ipynb` |

### GenAI/LLM
| Type | Usage | Examples |
|------|-------|----------|
| `RAG` | Retrieval-Augmented Generation | `GenAI_RAG_DocumentQA.ipynb` |
| `PromptEngineering` | Prompt optimization | `GenAI_PromptEngineering_ChainOfThought.ipynb` |
| `Summarization` | Text summarization | `GenAI_Summarization_AbstractiveExtractive.ipynb` |
| `LLMIntegration` | LLM API integration | `GenAI_LLMIntegration_OpenAI.ipynb` |

### Utilities
| Type | Usage | Examples |
|------|-------|----------|
| `DataPreprocessing` | Data cleaning and transformation | `Utils_DataPreprocessing_MissingValues.ipynb` |
| `Visualization` | Plotting and visualization | `Utils_Visualization_Matplotlib_Seaborn.ipynb` |
| `FeatureEngineering` | Feature creation and selection | `Utils_FeatureEngineering_PolynomialFeatures.ipynb` |
| `Tutorial` | Learning/educational content | `Tutorial_PandasBasics.ipynb` |

---

## ✅ Naming Examples

### Good (Meaningful) Names
```
ML_Classification_DiabetesRiskPrediction.ipynb
ML_Regression_WineQualityPrediction_v2.ipynb
ML_Ensemble_RandomForestVsGradientBoosting.ipynb
GenAI_RAG_DocumentQASystem.ipynb
GenAI_PromptEngineering_AdvancedTechniques.ipynb
NLP_TextCleaning_StandardPipeline.ipynb
NLP_SentimentAnalysis_MovieReviews.ipynb
Utils_DataPreprocessing_MissingValueHandling.ipynb
Utils_Visualization_CorrelationMatrix.ipynb
```

### Bad (Unclear) Names
```
❌ Project_5_LLM_Notebook (1).ipynb
❌ Case_Study_DiabetesRisk_Prediction.ipynb (missing category prefix)
❌ Hands_on_K_Means_Clustering.ipynb (too casual)
❌ w_AIML_ITP_MLS2_MovieLens_Case_Study.ipynb (cryptic abbreviations)
❌ TourismPackage MLOPS and DEPLOYMENT.ipynb (spaces, mixed format)
```

---

## 📝 Best Practices

1. **Use PascalCase** for multi-word descriptions (no spaces or special chars except underscores)
2. **Keep it concise** but descriptive (aim for 3-5 meaningful words)
3. **Avoid version suffixes** unless tracking iterations (v1, v2, Final)
4. **Use underscores** to separate components, never spaces
5. **No numbers alone** — always pair with descriptive text
6. **Be specific** — "DiabetesRiskPrediction" is better than "PredictionModel"
7. **Consistent casing** — use PascalCase consistently across all notebooks

---

## 🔄 Naming Convention by Folder

### GenAI/PromptEngineering/
```
GenAI_PromptEngineering_[SpecificTechnique].ipynb
Examples:
  - GenAI_PromptEngineering_ChainOfThought.ipynb
  - GenAI_PromptEngineering_FewShotLearning.ipynb
  - GenAI_PromptEngineering_RolePlayingPrompts.ipynb
```

### GenAI/RAG_Project/
```
GenAI_RAG_[ApplicationName].ipynb
Examples:
  - GenAI_RAG_DocumentQASystem.ipynb
  - GenAI_RAG_KnowledgeRetrieval.ipynb
```

### ML/Regression/
```
ML_Regression_[ProblemStatement].ipynb
Examples:
  - ML_Regression_WineQualityPrediction_v2.ipynb
  - ML_Regression_MovieRecommendations.ipynb
  - ML_Regression_HyperparameterTuning.ipynb
  - ML_Regression_CrossValidationAnalysis.ipynb
```

### ML/Classification/
```
ML_Classification_[ProblemStatement].ipynb
Examples:
  - ML_Classification_DiabetesRiskAssessment.ipynb
  - ML_Classification_LoanApprovalPrediction.ipynb
  - ML_Classification_AnimeRatingPrediction.ipynb
  - ML_Classification_ExploratoryDataAnalysis.ipynb
  - ML_Classification_PandasDataManipulation.ipynb
```

### ML/Ensemble/
```
ML_Ensemble_[Technique].ipynb
Examples:
  - ML_Ensemble_BaggingAndBoosting.ipynb
  - ML_Ensemble_RandomForestVsGradientBoosting.ipynb
  - ML_Ensemble_ClassImbalanceHandling.ipynb
```

### NLP/TextCleaning/
```
NLP_TextCleaning_[Approach].ipynb
Examples:
  - NLP_TextCleaning_StandardPipeline.ipynb
  - NLP_TextCleaning_TokenizationAndLemmatization.ipynb
```

### NLP/TFIDF/
```
NLP_TFIDF_[Application].ipynb
Examples:
  - NLP_TFIDF_FeatureExtraction.ipynb
  - NLP_TFIDF_DocumentSimilarity.ipynb
```

### NLP/ClassicalNLP/
```
NLP_ClassicalNLP_[Task].ipynb
Examples:
  - NLP_ClassicalNLP_POSTagging.ipynb
  - NLP_ClassicalNLP_SentimentAnalysis.ipynb
```

### Notebooks/ (General utilities & tutorials)
```
[Category]_[Type]_[Description].ipynb
Examples:
  - Utils_DataPreprocessing_MissingValues.ipynb
  - Utils_Visualization_CorrelationMatrix.ipynb
  - Utils_FeatureEngineering_PolynomialFeatures.ipynb
  - Tutorial_PandasBasics.ipynb
  - Tutorial_NumPyFundamentals.ipynb
  - EDA_RestaurantReviewAnalysis.ipynb
  - EDA_HousingMarketAnalysis.ipynb
```

---

## 🔄 Migration Guide: Current → New Names

| Current Name | Recommended New Name | Reason |
|--------------|---------------------|--------|
| `Project_5_LLM_Notebook (1).ipynb` | `GenAI_PromptEngineering_LLMTechniques.ipynb` | Clear category + purpose |
| `Project_5_LLM_Notebook (6).ipynb` | `GenAI_RAG_DocumentQASystem.ipynb` | Identifies as RAG project |
| `Case_Study_WineQuality_Prediction_V2-1.ipynb` | `ML_Regression_WineQualityPrediction_v2.ipynb` | Standardized format |
| `Case_Study_DiabetesRisk_Prediction.ipynb` | `ML_Classification_DiabetesRiskAssessment.ipynb` | Clear problem statement |
| `Ensemble_Hands-On_Bagging-2.ipynb` | `ML_Ensemble_BaggingAndBoosting.ipynb` | Professional naming |
| `Hands_on_K_Means_Clustering.ipynb` | `ML_Classification_KMeansClustering.ipynb` | Standardized format |
| `Case_Study_Restaurant_Review_Analysis (5)-1.ipynb` | `NLP_SentimentAnalysis_RestaurantReviews.ipynb` | Domain + task clarity |
| `flow_control.ipynb` | `Tutorial_PythonFlowControl.ipynb` | Identifies as tutorial |
| `PythonVisualization.ipynb` | `Utils_Visualization_MatplotlibSeaborn.ipynb` | Specifies tools used |
| `Python_Week_3(Data Pre Processing).ipynb` | `Utils_DataPreprocessing_StandardPipeline.ipynb` | Clear purpose |

---

## 💡 Benefits of This Convention

✅ **Discoverability** — Easy to search and find notebooks by category/type  
✅ **Professional** — Clear, organized names for employer/portfolio  
✅ **Scalability** — Supports future growth without confusion  
✅ **Consistency** — Uniform format across all projects  
✅ **SEO-Friendly** — Better for GitHub search and discovery  
✅ **Self-Documenting** — Name tells you what the notebook does  

---

**Document Version:** 1.0  
**Last Updated:** November 14, 2025  
**Status:** Ready for Implementation
