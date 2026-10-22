---
title: System Overview
type: concept
created: 2026-10-22
updated: 2026-10-22
sources: []
tags: [architecture, pipeline, reproducibility, code]
---

# System Overview

How the whole system works end to end — the reading guide for understanding the codebase deeply.

## Two Deliverables, One Pipeline Philosophy

| | Hit Prediction (studio) | Recommender (streaming, bonus) |
|---|---|---|
| Question | Which films should we greenlight? | What should we show this user next? |
| Data | IMDb bulk + TMDb (65,799 films) | MovieLens ml-25m (25M ratings) |
| Model | FT-Transformer vs XGBoost vs LR | SVD++ / SVD / item-KNN |
| Guardrail | As-of features + temporal split | Temporal split + warm-user eval |
| Output | Two-tier greenlight slate | Top-10 recommendation lists |

Both share one discipline: **the model may only learn from the past** (D020, D027).

## Hit-Prediction Pipeline (data flow)

```
source_data/                       (raw, not in repo)
  title.*.tsv.gz  +  TMDb Kaggle zip
        │  notebooks/01_data_loading.ipynb   (clean \N nulls, filters D010/D014, merge)
        ▼
data/                              (generated, not in repo)
  movies_with_hit_score.parquet    (71K films + two-mode hit_score, D011)
  actor_popularity.parquet, director_stats.parquet, valid_tconst_set.parquet
        │  src/feature_engineering.py
        │    extract-cast  → movie_cast.parquet     (672K credits)
        │    extract-tmdb  → release_dates.parquet  (692K releases)
        │    build         → features.parquet       (65,799 × 76 features)
        ▼
  features.parquet                 (greenlight features + hit_label + split)
        │  src/train.py             (LR, XGBoost, FT-Transformer)
        ▼
reports/
  tables/model_comparison.{csv,md} (headline metrics)
  figures/model_*.png              (ROC, PR, metrics, confusion, importance, slate)
data/test_predictions.parquet      (per-film scores for case studies)
```

### Module map (`src/`)

| Module | Responsibility |
|---|---|
| `feature_engineering.py` | Extractions (chunked, timing-gauged) + as-of rolling features + static features + label/split + `leakage_audit()` |
| `models/baselines.py` | Logistic Regression + XGBoost pipelines (one-hot, class weighting) |
| `models/ft_transformer_model.py` | FT-Transformer wrapper (pytorch-tabular): weighted CE loss, early stopping, input sanitizing |
| `train.py` | Orchestrator: trains all models, evaluates, writes tables/figures, supports `--sample-frac` timing gauges |
| `evaluation.py` | ROC-AUC / PR-AUC / F1, threshold tuning, precision@K slate analysis, all comparison charts |
| `ftt_perm_importance.py` | Batched permutation importance for the transformer (attention path is buggy — F011) |
| `models/recommender.py` | MovieLens: temporal split, SVD++/SVD/KNN, rating + ranking evaluation |

### Key commands (reproducibility)

```bash
uv sync                                          # environment (Python 3.12, torch cu130)
uv run python -m src.feature_engineering extract-cast   # ~1 min (full scan)
uv run python -m src.feature_engineering extract-tmdb   # ~10 s
uv run python -m src.feature_engineering build          # ~6 s  -> features.parquet
uv run python -m src.train                              # LR 1s + XGB 4s + FT-T ~72 min
uv run python -m src.ftt_perm_importance                # importance figure
uv run python -m src.models.recommender full            # ~55 min (SVD++ cohort + SVD + KNN)
```

### The as-of rule (the core engineering idea)

Historical track-record features (director, cast, company, franchise, genre momentum) are computed **per (entity, year) with `cumsum().shift(1)`** — a film sees only strictly earlier releases. Spot check: *The Dark Knight* (2008) sees Nolan's exactly 5 prior films, never *Interstellar*. `leakage_audit()` asserts banned columns (ratings, votes, revenue, popularity, hit-score components) never reach the feature matrix. Details: [[concepts/Temporal_Split]].

### Label and split

- Label: `hit_label = hit_score >= P90(training population)` (D016), two-mode hit score underneath (D011)
- Split: fit ≤2015 (46,946) / val 2016–2018 (7,218) / test 2019–2023 (11,635); 2024+ dropped (D021)

## Recommender Pipeline

```
source_data/ml-25m/ratings.csv     (25M ratings, 162K users, 59K movies)
        │  src/models/recommender.py
        │    temporal 90/10 split (cutoff 2018-01-04)
        │    item support filter >=200 train ratings (7,424 items, 96.7% of rows)
        ▼
  SVD++ (5K warm-user cohort) · SVD (full 21.8M) · item-KNN
        ▼
reports/tables/recommender_comparison_full.{csv,md}, recommender_examples_full.csv
```

Protocol details and metrics: [[concepts/Recommender_Metrics]], decisions [[concepts/Decision_Log]] (D027).

## Artifact Dictionary

| Artifact | Contents | In repo? |
|---|---|---|
| `data/*.parquet` | Clean data, features, predictions | No (regenerable) |
| `reports/tables/*` | Metric tables (model + recommender comparisons) | Yes |
| `reports/figures/*` | All charts | No (regenerable) |
| `wiki/` | Decisions, failures, results, this overview | Yes |
| `slides/` | Presentation working files | No (emailed deliverables) |

## Interpretability

- XGBoost: gain importance (`xgb_gain_importance`)
- LR: standardized |coefficients|
- FT-Transformer: batched permutation AUC importance (model-agnostic, comparable across models)
- Business meaning: talent track record + spend + timing dominate; genre alone is secondary

## Related

- [[concepts/Results_Summary]] — all headline numbers
- [[concepts/Decision_Log]] · [[concepts/Failures_and_Learnings]] — the why and the scars
- [[concepts/Repository_Structure]] — directory layout
