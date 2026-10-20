---
title: Recommender Systems
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [recommender, collaborative-filtering, content-based]
---

# Recommender Systems

Overview of approaches for the bonus streaming service deliverable.

## Approaches

### Collaborative Filtering (CF)
- User-item interaction matrix
- Learns from behavior patterns (users who liked X also liked Y)
- Cold-start problem for new users/items

### Content-Based Filtering
- Uses item features (genre, director, cast)
- No cold-start problem
- Limited discovery (recommends similar items)

### Hybrid
- Combines CF + content-based
- Best of both worlds
- More complex to implement

## Our Plan

| Model | Type | Library |
|-------|------|---------|
| KNN Baseline | CF (neighborhood) | surprise |
| SVD++ | CF (matrix factorization) | surprise |

## Evaluation

- RMSE for rating prediction accuracy
- NDCG@K for ranking quality
- Qualitative: do recommendations make sense for sample users?

## Related

- [[concepts/SVD_Plus_Plus]] — our advanced model
- [[concepts/Recommender_Metrics]] — how to evaluate
- [[entities/surprise]] — implementation library