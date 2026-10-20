# Index — GCash Movie Project

> Research companion and operational memory for the "Give Me The Next AAA Title" project.

## 🔖 Navigation
- [[#Concepts]] · [[#Entities]] · [[#Summaries]] · [[#Open Questions]]

## Concepts

### Project Management
- [[concepts/Decision_Log]] — Key decisions with rationale and tradeoffs
- [[concepts/Failures_and_Learnings]] — Mistakes, issues, lessons learned
- [[concepts/Deferred_Items]] — Skipped items with revisit dates
- [[concepts/Session_Workflow]] — How to run effective sessions
- [[concepts/Project_Requirements]] — Structured checklist from email
- [[concepts/Execution_Plan]] — 3-day plan with tasks and deliverables
- [[concepts/User_Context]] — Skills, constraints, hardware
- [[concepts/Risk_Register]] — Known risks with mitigation strategies
- [[concepts/Quality_Standards]] — What "exceptional" looks like
- [[concepts/Success_Criteria]] — Pass vs exceptional evaluation
- [[concepts/Submission_Checklist]] — Final verification before submission
- [[concepts/Differentiation_Strategy]] — What makes this stand out

### Machine Learning
- [[concepts/FT_Transformer]] — Feature tokenization + Transformer for tabular data
- [[concepts/TabNet]] — Sequential attention, sparse feature selection
- [[concepts/TabR]] — Retrieval-augmented tabular predictions
- [[concepts/Novel_Algorithm_Comparison]] — Full comparison of 11 algorithms
- [[concepts/Hit_Movie_Metric]] — Composite success index
- [[concepts/Movie_Feature_Engineering]] — Director, cast, genre, budget features + research

### Recommender Systems
- [[concepts/Recommender_Systems]] — CF, content-based, hybrid overview
- [[concepts/SVD_Plus_Plus]] — Matrix factorization with implicit feedback

### Evaluation
- [[concepts/Classification_Metrics]] — AUC-ROC, F1, precision-recall
- [[concepts/Recommender_Metrics]] — RMSE, NDCG@K, Precision@K
- [[concepts/Temporal_Split]] — Why random splits leak, how to fix

### Data
- [[concepts/IMDb_Datasets]] — Schema, fields, quirks of IMDb TSV files
- [[concepts/MovieLens_Dataset]] — Ratings, links, mapping to IMDb
- [[concepts/Data_Sources]] — External APIs and augmentation sources

### Strategy
- [[concepts/Interview_Narrative]] — Talking points for technical choices
- [[concepts/Presentation_Strategy]] — Dual-audience framing
- [[concepts/Repository_Structure]] — Code directory layout

## Entities

### Papers
- [[entities/FT_Transformer_Paper]] — Gorishniy et al., NeurIPS 2021
- [[entities/TabNet_Paper]] — Arik & Pfister, AAAI 2021
- [[entities/TabR_Paper]] — Gorishniy et al., ICLR 2024
- [[entities/SVD_Paper]] — Koren, KDD 2008
- [[entities/Movie_Success_Paper]] — Lash & Zhao, 2016

### Tools
- [[entities/pytorch_tabular]] — FT-Transformer library
- [[entities/pytorch_tabnet]] — TabNet library
- [[entities/surprise]] — Recommender systems library
- [[entities/IMDb_Datasets]] — Official IMDb bulk data
- [[entities/MovieLens_Dataset]] — GroupLens research data

## Summaries (chronological)

*(none yet)*

## Open Questions

- Optimal feature set for greenlight-time prediction?
- FT-Transformer vs XGBoost on this dataset?
- Is TabR worth the complexity?
- Best hit movie metric?
- Class imbalance handling strategy?