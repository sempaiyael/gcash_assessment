---
title: TabNet
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [tabnet-paper]
tags: [deep-learning, tabular, attention, interpretability]
---

# TabNet

Attentive Interpretable Tabular Learning. Google Cloud AI, AAAI 2021.

## Core Idea

Sequential attention for instance-wise feature selection at each decision step. Uses sparsemax activation for sparse masks.

## Architecture (Cheat Sheet)

1. **Feature Transformer**: GLU (Gated Linear Unit) blocks process input features
2. **Attentive Transformer**: Produces sparse feature selection masks via sparsemax
3. **Sequential Steps**: At each step, mask selects which features to attend to
4. **Sparsity Regularization**: Encourages using few features per step

## Key Properties

- **Interpretable**: Feature masks show which features drive each decision
- Self-supervised pre-training option (masked feature prediction)
- Handles mixed feature types without preprocessing
- **Weakness**: Consistently underperforms XGBoost/CatBoost in independent benchmarks

## Interpretability Advantage

TabNet provides feature importance masks at each decision step — can tell stakeholders "this prediction is driven by director track record + genre + budget."

## Related

- [[concepts/FT_Transformer]] — alternative that often outperforms
- [[entities/TabNet_Paper]] — source paper
- [[entities/pytorch_tabnet]] — implementation library

## Deeper Reference

- Paper: arXiv:1908.07442
- Library: pip install pytorch-tabnet