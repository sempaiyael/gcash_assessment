---
title: Movie Success Paper
type: entity
entity_type: paper
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [paper, movie-prediction, features]
---

# Movie Success Paper

**Title**: Early Predictions of Movie Success
**Authors**: Lash, M. T., Zhao, K.
**Affiliation**: University of Iowa
**Year**: 2016

## Key Findings

- Director's avg historical gross = #1 predictor (information gain ranking)
- Star power correlates with revenue but NOT profitability
- Budget predicts revenue but not ROI (r = 0.077 between revenue and profitability)
- 111 features tested; "When" features (release timing) contributed to AUC 0.822
- Sequels excluded from study (behave differently)

## Relevance to Our Project

- Informs feature engineering priorities
- Validates budget as important feature (supports TMDb API decision)
- Warns that revenue ≠ profitability — critical for hit metric design

## Related

- [[concepts/Movie_Feature_Engineering]]
- [[concepts/Hit_Movie_Metric]]