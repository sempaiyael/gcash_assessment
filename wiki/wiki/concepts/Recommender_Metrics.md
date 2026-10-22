---
title: Recommender Metrics
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [evaluation, recommender, metrics]
---

# Recommender Metrics

Metrics for evaluating the recommender system (bonus).

## Rating Prediction

| Metric | Formula | Use |
|--------|---------|-----|
| **RMSE** | $\sqrt{\frac{1}{n}\sum(\hat{r} - r)^2}$ | Rating prediction accuracy |
| **MAE** | $\frac{1}{n}\sum|\hat{r} - r|$ | More robust to outliers |

## Ranking Quality

| Metric | What it Measures |
|--------|-----------------|
| **NDCG@K** | Normalized Discounted Cumulative Gain — ranking quality with position decay |
| **Precision@K** | Of top-K recommendations, how many are relevant? |
| **Recall@K** | Of all relevant items, how many in top-K? |
| **MAP** | Mean Average Precision across users |

## Our Primary Metric: NDCG@K

Justification: A streaming platform cares about ranking (show best items first), not just rating prediction. NDCG@K measures this directly.

$$NDCG@K = \frac{DCG@K}{IDCG@K}, \quad DCG@K = \sum_{i=1}^{K} \frac{2^{rel_i} - 1}{\log_2(i+1)}$$

## Qualitative Assessment

Beyond metrics: show top-N recommendations for sample users and assess relevance manually.

## Empirical Results (ml-25m, 2026-10-22)

Temporal 90/10 holdout (test = future ratings after 2018-01-04), warm-user eval on 269,110 rating rows / 4,814 users; ranking via sampled-candidate protocol (relevant = test rating ≥4.0 vs 100 distractors). See D027 for protocol.

| Model | RMSE | MAE | Precision@10 | Recall@10 | NDCG@10 | Fit |
|---|---|---|---|---|---|---|
| SVD++ (5K-user cohort) | 0.832 | 0.615 | 0.354 | 0.471 | 0.448 | 27 min |
| SVD (cohort) | 0.818 | 0.603 | 0.364 | 0.484 | 0.459 | 13 s |
| **SVD (full, 21.8M ratings)** | **0.804** | **0.593** | **0.427** | **0.568** | **0.543** | 2 min |
| KNN (item-based) | 0.825 | 0.604 | 0.407 | 0.547 | 0.520 | 16 min |

**Findings**:
- Data scale > algorithm sophistication: SVD trained on all 21.8M training ratings beats SVD++ on a 5K cohort everywhere.
- SVD++ ≈ SVD at matched scale: its implicit-feedback edge (Koren 2008) needs denser interaction data than this cohort provides, and its O(Σ_u |I_u|²·f) cost is 100x plain SVD per epoch (F013).
- Matrix factorization beats item-KNN on both metrics — expected.
- Qualitative: recommendations are coherent (cinephile user → 12 Angry Men, Rear Window, Big Lebowski).
- Cold-start reality: 65% of 2018-19 MovieLens users are brand new — production systems need popularity fallback + feature-based warm start (bridging our hit-prediction features is the natural extension).

## Related

- [[concepts/Recommender_Systems]] — what we're evaluating
- [[concepts/SVD_Plus_Plus]] — our advanced model