---
title: Classification Metrics
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [evaluation, classification, metrics]
---

# Classification Metrics

Metrics for evaluating the hit movie prediction model.

## Key Metrics

| Metric | What it Measures | When to Use |
|--------|-----------------|-------------|
| **AUC-ROC** | Discrimination ability | Primary metric, threshold-independent |
| **F1 Score** | Precision-Recall balance | When classes are imbalanced |
| **Precision** | Of predicted hits, how many are real? | When false positives are costly |
| **Recall** | Of actual hits, how many did we find? | When false negatives are costly |
| **PR-AUC** | Area under precision-recall curve | Better than AUC-ROC for imbalanced data |

## Class Imbalance Strategy

Hits are rare by definition. Options:
- Stratified train/test split
- Class weights in loss function
- SMOTE (synthetic oversampling)
- Adjust classification threshold

## Reporting

- Confusion matrix
- Precision-Recall curve
- Feature importance (from FT-Transformer attention or SHAP)

## Related

- [[concepts/Hit_Movie_Metric]] — what we're predicting
- [[concepts/Temporal_Split]] — how to split data