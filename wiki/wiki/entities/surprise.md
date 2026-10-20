---
title: surprise
type: entity
entity_type: tool
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [library, recommender, collaborative-filtering]
---

# surprise

Python library for building and analyzing recommender systems.

## Installation

```bash
pip install scikit-surprise
```

## Supported Algorithms

- KNN (KNNBasic, KNNBaseline, KNNWithMeans, KNNWithZScore)
- SVD, SVD++
- NMF (Non-negative Matrix Factorization)
- SlopeOne, CoClustering

## Usage

```python
from surprise import SVDpp, Dataset, Reader
from surprise.model_selection import cross_validate

data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
model = SVDpp()
results = cross_validate(model, measures=['RMSE', 'MAE'], cv=5)
```

## Related

- [[concepts/Recommender_Systems]]
- [[concepts/SVD_Plus_Plus]]