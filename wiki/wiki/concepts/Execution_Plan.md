---
title: Execution Plan
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [planning, timeline, execution]
---

# Execution Plan

3-day plan to deliver the GCash movie project. Day 1 = 2026-10-19.

## Day 1: Data + EDA + Hit Metric

**Morning (3-4 hrs)**
- Download IMDb datasets (title.basics, title.ratings, title.principals, name.basics, title.crew)
- Download MovieLens dataset (ml-25M)
- Data cleaning: filter to movies, handle `\N` nulls, merge datasets
- Create unified analysis dataframe

**Afternoon (3-4 hrs)**
- EDA Q1: Highest rated 2023 + Bayesian weighted rating
- EDA Q2: Most popular actor 2023 (define popularity metric)
- EDA Q3: Preference trends over decades (genre shifts, runtime, franchise)
- EDA Q4: Define hit movie metric (weighted rating + audience reach + ROI)
- Decision point: TMDb API for budget data?

**Evening (1-2 hrs)**
- Generate visualizations (save PNGs for slides)
- Start slide skeleton

**Day 1 Deliverable**: Clean data, 4 EDA analyses, hit metric defined, visualizations

## Day 2: Prediction Model + FT-Transformer

**Morning (3-4 hrs)**
- Feature engineering pipeline
  - Director historical performance
  - Cast aggregate popularity
  - Genre encoding + trend momentum
  - Franchise/sequel status
  - Budget (if TMDb API available)
  - Runtime, language, release timing
- Define target using hit metric (binary: hit/not-hit)
- Temporal train/test split

**Afternoon (4-5 hrs)**
- Implement FT-Transformer (pytorch-tabular or official repo)
- Baselines: Logistic Regression, XGBoost, TabNet
- Evaluation: AUC-ROC, F1, precision-recall curves
- Feature importance / attention analysis

**Evening (1-2 hrs)**
- Model comparison tables and charts
- Update slides with modeling section

**Day 2 Deliverable**: Trained FT-Transformer, baseline comparisons, feature importance

## Day 3: Bonus Recommender + Polish

**Morning (3-4 hrs)**
- KNN collaborative filtering baseline (surprise library)
- SVD++ model (surprise library)
- Evaluate: RMSE + NDCG@K
- Qualitative assessment

**Afternoon (3-4 hrs)**
- Finalize both presentations
- Code cleanup, README, repo structure

**Evening (1-2 hrs)**
- Final review, package for submission

**Day 3 Deliverable**: Complete presentations, clean repo, all code

## Fallback Plan

If Day 2 runs long:
1. Cut recommender system entirely
2. Focus on polished required portion
3. Add "Future Work" slide mentioning recommender as extension

## Related

- [[concepts/Project_Requirements]] — what we're delivering
- [[concepts/User_Context]] — constraints and skills
- [[concepts/Repository_Structure]] — code organization