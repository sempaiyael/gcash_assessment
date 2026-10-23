---
title: Results Summary
type: concept
created: 2026-10-22
updated: 2026-10-22
sources: []
tags: [results, metrics, summary]
---

# Results Summary

Every headline number in one place. Test sets were held out **temporally** — the models never saw the future. Full detail: [[concepts/Classification_Metrics]], [[concepts/Recommender_Metrics]], [[concepts/Interview_Narrative]].

## Dataset

| Stat | Value |
|---|---|
| Films after quality filters (≥500 votes, adult excluded) | 71,056 |
| Modeling frame (1897–2023; 2024+ dropped — labels incomplete) | 65,799 |
| Greenlight-time features | 76 (all leakage-audited) |
| Train/val/test (temporal) | 46,946 / 7,218 / 11,635 |
| Hit base rate (label = top 10% of hit score, P90 = 0.5612) | 8.0% on test |
| MovieLens (bonus) | 25,000,095 ratings · 162,541 users · 59,047 movies |

## Hit Prediction — test 2019–2023

| Model | ROC-AUC | PR-AUC | F1 | Precision | Recall | Fit |
|---|---|---|---|---|---|---|
| XGBoost | **0.865** | 0.368 | 0.402 | 0.366 | 0.446 | 4 s |
| FT-Transformer | 0.863 | **0.379** | **0.406** | 0.355 | **0.475** | 72 min |
| Logistic Regression | 0.857 | 0.340 | 0.398 | 0.358 | 0.448 | 1 s |

*(thresholds tuned on validation; PR-AUC baseline = 0.08; paired bootstrap, 2,000 resamples: ΔAUC (FT-T − XGB) = −0.0016, 95% CI [−0.0062, +0.0030] — a statistical tie)*

## Greenlight Slate — precision@K (D025)

| Slate | FT-Transformer | XGBoost | LR | vs base rate |
|---|---|---|---|---|
| Top 25 ("endorsement") | **0.76** | 0.64 | 0.52 | ~10x |
| Top 50 | **0.74** | 0.64 | 0.56 | |
| Top 100 | **0.67** | 0.60 | 0.49 | |
| Top 250 ("review") | **0.55** | 0.54 | 0.51 | |

**90% precision is not reachable at usable coverage** (measured: oracle-on-test reaches it only at ~1% recall; val-tuned thresholds transfer to test at 0.53–0.67 precision at ≤2% coverage). Root causes: 8% base rate, greenlight-only signals (D002), two-mode label noise (D011), weighted-loss score inflation (top decile: predicted 81% vs actual 37%).

## Case-Study Slate (test picks by FT-Transformer)

- Right: *Oppenheimer* 0.99, *Once Upon a Time in... Hollywood* 0.99, *Avengers: Endgame* 0.98, *Spider-Man: Across the Spider-Verse* 0.96, *Everything Everywhere All at Once* 0.91, *Top Gun: Maverick* 0.87 — 17 of the top 20 are hits (XGBoost: 13 of 20)
- Honest discussion: *Killers of the Flower Moon* 0.98 predicted / label 0 — acclaimed, but the ROI/quality composite says not top-decile

## What Drives Hits (permutation importance)

Top features across models: **keyword richness** (disclosed metadata caveat), **has_budget**, **runtime**, **director prior hit rate**, **log_budget**, **cast prior hit rate**, **certification**. Consistent with Lash & Zhao (2016): director track record is the #1 signal.

## Recommender (MovieLens, temporal holdout after 2018-01-04)

| Model | RMSE | MAE | Precision@10 | NDCG@10 | Fit |
|---|---|---|---|---|---|
| **SVD (full, 21.8M ratings)** | **0.804** | **0.593** | **0.427** | **0.543** | 2 min |
| KNN (item-based) | 0.825 | 0.604 | 0.407 | 0.520 | 16 min |
| SVD++ (5K-user cohort) | 0.832 | 0.615 | 0.354 | 0.448 | 27 min |
| SVD (cohort) | 0.818 | 0.603 | 0.364 | 0.459 | 13 s |

*(269,110 rating rows · 4,814 users · sampled-candidate ranking protocol, D027. Scope note: 0.804 is the cohort RMSE; on all warm users SVD-full is 0.809 over 345,684 rows. Always state the population next to the number.)*

## Key Findings (the five to remember)

1. **Feature engineering > model choice**: LR hits 0.857 of the best 0.865 — the as-of feature set carries the signal.
2. **FT-Transformer ≈ XGBoost is the theoretically expected outcome** (Gorishniy 2021 claims "competitive with GBDTs"; Grinsztajn 2022 shows trees win at this data scale). FT-T leads on PR-AUC/F1 — the metrics that matter at 8% base rates.
3. **0.86 AUC is strong for greenlight time** — published 0.95+ results use post-release signals we deliberately banned (D002). Higher would imply leakage.
4. **The product is a two-tier slate**, not a classifier: ~76% precision at the top-25 endorsement tier (~10x base rate), honestly disclosed recall.
5. **Scale beats sophistication in recommendation too**: full-data SVD beats a fancier SVD++ on a cohort; MF beats KNN.

## Related

- [[concepts/System_Overview]] — how it all works
- [[concepts/Interview_Narrative]] — how to tell the story
- [[concepts/Classification_Metrics]] · [[concepts/Recommender_Metrics]] — metric deep-dives
