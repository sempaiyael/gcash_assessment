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

- [ ] **TabPFN-2.5 experiment — PINNED** (2026-10-22)
  - State: experiment script complete (`gcash_scratch/tabpfn_experiment.py`); blocked on Prior Labs license acceptance (weights gated at ux.priorlabs.ai, `TABPFN_TOKEN` auth)
  - Revisit: after the bonus recommender is delivered
  - Why it matters: Feb-2026 SOTA for our data regime (≤50K rows); would add a leaderboard row + landscape credibility
- [ ] **TabR deep-dive** — ICLR 2024 paper, retrieval mechanism
  - Revisit: after the recommender, only if time remains
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