---
title: SVD++
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [svd-paper]
tags: [recommender, matrix-factorization, collaborative-filtering]
---

# SVD++

Enhanced SVD with implicit feedback for collaborative filtering. Koren, KDD 2008.

## Core Idea

Extends standard matrix factorization by incorporating implicit feedback (viewing history, browsing behavior) in addition to explicit ratings.

## Formulation (Cheat Sheet)

$$\hat{r}_{ui} = \mu + b_u + b_i + q_i^T \left( p_u + |N(u)|^{-1/2} \sum_{j \in N(u)} y_j \right)$$

Where:
- $\mu$ = global mean rating
- $b_u, b_i$ = user/item biases
- $p_u$ = user latent factor
- $q_i$ = item latent factor
- $y_j$ = implicit feedback factor
- $N(u)$ = set of items user interacted with implicitly

## Key Properties

- Captures both explicit ratings and implicit behavior
- Better than basic SVD for sparse datasets
- Well-supported in surprise library
- Published at KDD 2008 (highly cited)

## Our Implementation

```python
from surprise import SVDpp
model = SVDpp(n_factors=100, n_epochs=20, lr_all=0.007, reg_all=0.02)
```

## Related

- [[concepts/Recommender_Systems]] — overview of approaches
- [[concepts/Recommender_Metrics]] — evaluation
- [[entities/SVD_Paper]] — source paper