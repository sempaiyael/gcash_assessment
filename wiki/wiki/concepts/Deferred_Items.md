---
title: Deferred Items
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [deferred, decisions, scope]
---

# Deferred Items

Items intentionally skipped. Check before starting new research.

## Data Augmentation

- [x] **TMDb API** — Budget/revenue data → Resolved via Kaggle dataset (D007). alanvourch's "Ultimate 1M Movies Dataset" provides budget/revenue without API rate limits.
- [x] **Box Office Mojo** — Opening weekend, theater counts → NOT NEEDED. Model strong without it (XGB 0.865 / FT-T 0.863 ROC-AUC).
- [ ] **The Numbers** — Production budgets, profit estimates
  - Revisit: Unlikely needed — Kaggle TMDb dataset has financial data for major releases

## Algorithm Research

- [ ] **TabR deep-dive** — ICLR 2024 paper, retrieval mechanism
  - Revisit: Day 3 evening, only if slides + recommender done
- [ ] **ExcelFormer** — Semi-permeable attention
  - Revisit: Only if extra time
- [x] **TabNet baseline** — Dropped (D019). Bundled in pytorch-tabular (TabNetConfig) if ever needed.

## Feature Engineering

- [ ] **NLP on plot synopses** — LDA topics, sentiment
  - Revisit: Only if other features underperform (they didn't)
- [ ] **Social media buzz** — Twitter, trailer views
  - Revisit: Not for this project (post-production only)

## Evaluation

- [ ] **Qualitative recommender assessment** — Sample user recommendations
  - Revisit: Day 3, if recommender built