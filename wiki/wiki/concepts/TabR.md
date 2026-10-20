---
title: TabR
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [tabr-paper]
tags: [deep-learning, tabular, retrieval, state-of-the-art]
---

# TabR

Tabular Deep Learning Meets Nearest Neighbors. ICLR 2024. Current SOTA for parametric tabular DL.

## Core Idea

Augments a feed-forward network with a k-NN retrieval layer. For each input, retrieves K nearest neighbors from training set in learned embedding space, extracts signal via attention, combines with encoded input.

## Architecture (Cheat Sheet)

1. **Encoder**: Maps input to learned embedding
2. **Retrieval**: Finds K nearest neighbors from training set (approximate NN search)
3. **Attention**: Weights neighbor contributions by learned scoring function
4. **Combination**: Merges retrieval signal with encoded input
5. **Prediction head**: Final output

## Key Properties

- Best avg performance among parametric tabular DL models
- Even outperforms GBDT on "GBDT-friendly" benchmarks
- Intuitive: "find similar movies and learn from their outcomes"
- Same research group as FT-Transformer (Yandex)

## Why Not Primary Model

- More complex to implement than FT-Transformer
- Retrieval infrastructure adds engineering overhead
- 3-day timeline favors simpler approach
- Good stretch goal / interview talking point

## Related

- [[concepts/FT_Transformer]] — base architecture TabR extends
- [[entities/TabR_Paper]] — source paper

## Deeper Reference

- Paper: arXiv:2307.14338
- Official code: github.com/yandex-research/tabular-dl-tabr