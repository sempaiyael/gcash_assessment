---
title: FT-Transformer
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [ft-transformer-paper]
tags: [deep-learning, tabular, transformer, architecture]
---

# FT-Transformer

Feature Tokenizer Transformer — a principled Transformer adaptation for tabular data. NeurIPS 2021.

## Core Idea

Treat each input feature as a "token" → feed all feature tokens through a standard Transformer encoder → use CLS token for prediction.

## Architecture (Cheat Sheet)

1. **Feature Tokenizer**: Maps each feature to a d-dimensional vector
   - Categorical: lookup embedding
   - Numerical: $x_i \cdot \mathbf{w}_i + \mathbf{b}_i$ (element-wise multiply + bias)
2. **[CLS] token**: Learnable token appended to sequence
3. **Transformer Encoder**: Standard multi-head self-attention + FFN blocks
4. **Prediction head**: MLP on CLS token output

## Key Properties

- Handles mixed feature types natively
- Self-attention learns pairwise + higher-order feature interactions
- Best avg performance among DL tabular models (per original benchmarks)
- Does NOT universally beat GBDT — "no universally superior solution"

## When to Use

- Tabular data with mixed categorical + numerical features
- When interpretability via attention weights is desired
- When you have GPU available (CPU training is slow)

## Related

- [[concepts/TabR]] — extends FT-Transformer with retrieval
- [[concepts/TabNet]] — alternative attention-based approach
- [[entities/FT_Transformer_Paper]] — source paper
- [[entities/pytorch_tabular]] — implementation library

## Deeper Reference

- Paper: arXiv:2106.11959
- Official code: github.com/yandex-research/tabular-dl-revisiting-models