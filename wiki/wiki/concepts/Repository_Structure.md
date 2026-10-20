---
title: Repository Structure
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [code, structure, repository]
---

# Repository Structure

Planned project directory structure for the code deliverable.

## Directory Layout

```
gcash-movie-project/
├── README.md
├── requirements.txt
├── data/
│   └── .gitkeep                    # Instructions to download datasets
├── notebooks/
│   ├── 01_data_loading.ipynb       # Download + clean + merge
│   ├── 02_eda_analysis.ipynb       # 4 EDA questions
│   ├── 03_hit_metric.ipynb         # Define + justify hit metric
│   ├── 04_prediction_model.ipynb   # FT-Transformer + baselines
│   └── 05_recommender_system.ipynb # KNN + SVD++ (bonus)
├── src/
│   ├── data_loader.py              # IMDb + MovieLens loading
│   ├── feature_engineering.py      # Feature pipeline
│   ├── models/
│   │   ├── ft_transformer_model.py # FT-Transformer wrapper
│   │   ├── baselines.py            # LR, XGBoost, TabNet
│   │   └── recommender.py          # KNN, SVD++ (bonus)
│   └── evaluation.py               # Metrics + visualization
├── slides/
│   ├── AAA_Title_Presentation.pptx # Studio exec presentation
│   ├── Recommender_Presentation.pptx # Streaming exec (bonus)
│   └── images/                     # EDA charts, model results
└── reports/
    └── figures/                    # Generated figures
```

## Naming Conventions

- Notebooks: numbered prefix (01_, 02_, ...) for execution order
- Source modules: snake_case, single responsibility
- Slides: descriptive names matching deliverables
- Images: descriptive names with category prefix (eda_, model_, rec_)

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, setup instructions, key findings |
| `requirements.txt` | Python dependencies with versions |
| `data_loader.py` | Handles IMDb TSV loading, `\N` cleaning, merging |
| `feature_engineering.py` | Director/cast features, genre encoding, temporal features |
| `evaluation.py` | AUC-ROC, F1, PR curves, NDCG@K |

## Git Strategy

- Initialize with `git init`
- `.gitignore`: data/*.tsv.gz, __pycache__, .ipynb_checkpoints
- Commit after each major phase (Day 1, Day 2, Day 3)
- Clean commit messages: "Day 1: EDA and hit metric", "Day 2: FT-Transformer model"

## Related

- [[concepts/Execution_Plan]] — when to build each component
- [[concepts/Project_Requirements]] — what each file delivers