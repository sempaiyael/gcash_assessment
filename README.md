# Give Me The Next AAA Title

**GCash AI/ML Assessment** — Predicting hit movies using IMDb data with FT-Transformer.

## Results (temporal test holdout 2019-2023)

| Model | ROC-AUC | PR-AUC | F1 | Fit |
|---|---|---|---|---|
| XGBoost | 0.865 | 0.368 | 0.402 | 4 s |
| **FT-Transformer** (novel) | 0.863 | **0.379** | **0.406** | 72 min |
| Logistic Regression | 0.857 | 0.340 | 0.398 | 1 s |

- **Statistical tie at the top** - paired bootstrap delta-AUC (FT-T - XGB) = -0.0016, 95% CI [-0.0062, +0.0030]
- **The product is a two-tier greenlight slate** - top-25 "endorsement" at **0.76 precision (~10x the 8% base rate)**; top-250 "review" at 0.55
- **Feature engineering > model choice** - LR reaches 0.857 of the best 0.865; the leakage-safe as-of features carry the signal
- **0.86 is the honest greenlight-time level** - published 0.95+ results use post-release signals we deliberately exclude
- **Bonus recommender** (MovieLens 25M ratings) - full-data SVD RMSE **0.804**, NDCG@10 **0.543**; scale beats sophistication

Full number sheet: `wiki/wiki/concepts/Results_Summary.md` - methodology: `wiki/wiki/concepts/System_Overview.md`

## Project Structure

```
.
├── notebooks/              # Jupyter notebooks (run in order)
│   ├── 01_data_loading.ipynb    # Data loading, cleaning, merging
│   └── 02_eda_analysis.ipynb    # 4 EDA questions + hit metric
├── src/                    # Feature pipeline, models, evaluation
├── wiki/                   # Knowledge base & decision log
├── reports/figures/        # Generated charts (not in repo)
├── data/                   # Generated data (not in repo)
├── source_data/            # Downloaded datasets (not in repo)
├── pyproject.toml          # UV project config
└── uv.lock                 # Locked dependency versions
```

## Wiki

The `wiki/` directory contains the project's knowledge base and operational memory:

- **`Knowledge_Base.md`** — Session checklist and project context
- **`wiki/concepts/Decision_Log.md`** — Key decisions with rationale (D001-D028)
- **`wiki/concepts/Failures_and_Learnings.md`** — Mistakes and lessons (F001-F014)
- **`wiki/concepts/Execution_Plan.md`** — 3-day timeline with tasks and deliverables
- **`wiki/concepts/Hit_Movie_Metric.md`** — Composite success index definition
- **`wiki/concepts/FT_Transformer.md`** — Novel algorithm choice (NeurIPS 2021)
- **`wiki/log/`** — Daily activity logs

This documents the planning and decision-making process throughout the project.

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/sempaiyael/gcash_assessment.git
cd gcash_assessment

# Install dependencies (creates .venv automatically)
uv sync

# Download source data (not in repo — see Data Sources below)
# Place IMDb .tsv.gz files and TMDb .zip in source_data/

# Run notebooks
uv run jupyter notebook
```

### Data Sources

The following datasets are required but not included in the repository (too large). Download them manually and place in `source_data/`:

| Source | Files | Download |
|--------|-------|----------|
| **IMDb** | title.basics.tsv.gz, title.ratings.tsv.gz, title.principals.tsv.gz, name.basics.tsv.gz, title.crew.tsv.gz | https://datasets.imdbws.com/ |
| **TMDb** | TMDB_all_movies.csv (from alanvourch zip) | https://www.kaggle.com/datasets/alanvourch/tmdb-movies-daily-updates |

### Running the Notebooks

1. **`01_data_loading.ipynb`** — Run first. Loads, cleans, and merges all data. Saves to `data/movies_clean.parquet`.
2. **`02_eda_analysis.ipynb`** — Run after notebook 1. Answers the 4 required EDA questions with visualizations.

### Running the Pipeline

```bash
uv sync                                                # environment (Python 3.12, torch cu130)
uv run python -m src.feature_engineering extract-cast   # ~1 min (movie_cast.parquet)
uv run python -m src.feature_engineering extract-tmdb   # ~10 s (release_dates.parquet)
uv run python -m src.feature_engineering build          # ~6 s -> features.parquet (65,799 x 76)
uv run python -m src.train                              # LR 1s + XGB 4s + FT-T ~72 min
uv run python -m src.models.recommender full            # bonus: SVD++ cohort + SVD + KNN, ~55 min
```

## Key Design Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D001 | FT-Transformer as primary novel algorithm | Best avg performance among DL tabular models; NeurIPS venue |
| D007 | TMDb data from Kaggle dataset (not API) | No rate limits, has imdb_id for joining |
| D008 | Actor popularity: weighted formula | Billing order × numVotes × rating |
| D009 | Billing weight: 1/log(ordering+1) | Better handles co-leads than 1/ordering |
| D010 | Min vote threshold: configurable, default 500 | Allows experimentation during EDA |
| D011 | Hit metric: two-mode approach | Full (with ROI) and Partial (without) |

See `wiki/concepts/Decision_Log.md` for full decision history.

## License

This project is for the GCash AI/ML assessment. Not for commercial use.