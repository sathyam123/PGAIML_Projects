Organizing your workspace

This workspace helper was created to organize files into the following structure:

GenAI/
  - RAG_Project/
  - PromptEngineering/
  - Summarization/
ML/
  - Regression/
  - Classification/
  - Ensemble/
NLP/
  - TextCleaning/
  - TFIDF/
  - ClassicalNLP/
Datasets/
Notebooks/
Archive/

How to use

1) Dry run (recommended):
   Open PowerShell in the workspace root and run:

       .\organize_projects.ps1

   The script will print planned moves without changing files.

2) Apply changes:
   If the planned moves look correct, run:

       .\organize_projects.ps1 -Execute

Notes and customization

- The script decides destination based on filename keywords and extensions.
- To change rules, edit `organize_projects.ps1` and update the `$dest` mapping.
- The script only moves files from the workspace root (non-recursive). If you want recursive behavior, ask me and I can update the script.
- The script excludes itself and `README.md` by default.

If you'd like, I can run the dry-run now or execute the moves when you confirm.