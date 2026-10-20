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

## Related

- [[concepts/Recommender_Systems]] — what we're evaluating
- [[concepts/SVD_Plus_Plus]] — our advanced model