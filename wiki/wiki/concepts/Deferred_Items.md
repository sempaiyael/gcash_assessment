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
- [ ] **Box Office Mojo** — Opening weekend, theater counts
  - Revisit: Day 2, if model performance weak
- [ ] **The Numbers** — Production budgets, profit estimates
  - Revisit: Unlikely needed — Kaggle TMDb dataset has financial data for major releases

## Algorithm Research

- [ ] **TabR deep-dive** — ICLR 2024 paper, retrieval mechanism
  - Revisit: Day 2 evening, if FT-Transformer done early
- [ ] **ExcelFormer** — Semi-permeable attention
  - Revisit: Only if extra time

## Feature Engineering

- [ ] **NLP on plot synopses** — LDA topics, sentiment
  - Revisit: Only if other features underperform
- [ ] **Social media buzz** — Twitter, trailer views
  - Revisit: Not for this project (post-production only)

## Evaluation

- [ ] **Qualitative recommender assessment** — Sample user recommendations
  - Revisit: Day 3, if recommender built