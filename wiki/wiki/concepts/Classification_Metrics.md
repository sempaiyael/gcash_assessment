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

## High-Precision Operating Point (Day-2 Findings, 2026-10-22)

Asked: "can we tune to 90% precision?" — measured answer: **not at usable coverage** (analysis on test predictions).

| Model | Thr @ 90% val-prec | Test coverage | Test precision | Test recall |
|---|---|---|---|---|
| LR | never reaches 0.90 | 220 (1.9%) | 0.53 | 0.12 |
| XGBoost | 0.978 (val P=1.0 over 2-3 rows) | 9 (0.1%) | 0.67 | 0.006 |
| FT-Transformer | 0.988 | 1 | 1.00 | 0.001 |

Even with **oracle hindsight on test**, ≥90% precision needs recall ≤1% (10-25 picks out of 935 hits); ≥80% needs ≤2%.

### Why 90% is unreachable

1. **Base rate 8%** — 90% precision needs a likelihood ratio ≈ 11x at the very top of the ranking
2. **Greenlight-time features cap the top end** — quality/marketing/cultural-moment signals that separate hits are unobserved pre-production (by design, D002)
3. **Label noise ceiling** — hit label mixes full/partial modes (D011); precision-vs-label ≠ precision-vs-truth
4. **Score inflation** — weighted training loss inflates probabilities (XGB top decile: predicted 81% vs actual 37% hit rate; Brier XGB 0.116 / LR 0.134 / FTT 0.140). Any threshold claim requires isotonic/Platt recalibration on val first.

### The practical framing: precision@K slate

| Top-K | FT-Transformer | XGBoost | LR | Base rate |
|---|---|---|---|---|
| P@25 | **0.76** | 0.64 | 0.52 | 0.08 |
| P@50 | **0.74** | 0.64 | 0.56 | |
| P@100 | **0.67** | 0.60 | 0.49 | |
| P@250 | **0.55** | 0.54 | 0.51 | |

**Two-tier operating point (D025)**:
- **Endorsement tier** (top ~25): ~75-80% precision (with ensemble) = ~10x base rate — "strong yes, invest"
- **Review tier** (top ~250): ~55% precision — "worth human review"

**Risks of chasing a fixed 90% threshold**: recall collapse (miss nearly every hit — missed blockbusters are invisible in precision), tiny-n confidence intervals (±30pt on 9 predictions), threshold overfitting to val noise ("P=1.000" over 2-3 rows), calibration drift under COVID-era distribution shift.

**Reporting standard**: precision@K + recall-coverage curve + calibrated probabilities. Never report threshold-precision without n and a confidence interval. To genuinely reach 90%: better top-end features (marketing spend, franchise IP, director×genre fit) or post-production signals — the latter breaks the greenlight-time promise.

## Related

- [[concepts/Hit_Movie_Metric]] — what we're predicting
- [[concepts/Temporal_Split]] — how to split data