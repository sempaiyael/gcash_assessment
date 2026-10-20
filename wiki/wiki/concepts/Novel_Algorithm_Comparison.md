---
title: Novel Algorithm Comparison
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [ft-transformer-paper, tabnet-paper, tabr-paper]
tags: [deep-learning, tabular, comparison, algorithms]
---

# Novel Algorithm Comparison

Full comparison of 11 algorithms researched. Decision: FT-Transformer (D001).

## Comparison Table

| Algorithm | Venue | Year | vs GBDT | Interpretability | PyTorch Library | GPU Fit | Interview Impact |
|-----------|-------|------|---------|------------------|-----------------|---------|-----------------|
| **TabNet** | AAAI | 2021 | Mixed (often loses) | High (masks) | Excellent (pip) | Great | Medium |
| **NODE** | ICLR | 2020 | Mixed | Low | Good | Moderate (memory) | Medium |
| **TabTransformer** | arXiv | 2020 | Mixed | Medium | Excellent | Great | Low (superseded) |
| **FT-Transformer** | NeurIPS | 2021 | Competitive | Low-Medium | Excellent | Great | **High** |
| **SAINT** | arXiv | 2021 | Competitive | Medium | Good | Good | Medium |
| **GrowNet** | arXiv | 2020 | Modest gains | Low | Adequate | Great | Low |
| **DeepGBM** | KDD | 2019 | Mixed | Low | Adequate | Good | Low |
| **TabR** | ICLR | 2024 | **Often wins** | Low | Good | Good | **Very High** |
| **ExcelFormer** | KDD | 2024 | **Often wins** | Medium | Good | Good | **Very High** |
| **TabPFN v2** | Nature | 2025 | **Wins (small data)** | Medium | Excellent (pip) | Great | **Very High** |
| **XTab** | ICML | 2023 | Competitive | Low | Good | Good | High |

## Decision: FT-Transformer (D001)

**Why FT-Transformer:**
- Best avg performance among DL tabular models in rigorous benchmarks (NeurIPS 2021)
- NeurIPS venue = high interview credibility
- Clean architecture: "it's just a Transformer for tabular features" — easy to explain
- Handles mixed feature types (categorical + numerical) natively
- PyTorch-native with excellent library support (pytorch-tabular)
- Runs comfortably on RTX 3060

**Why not TabNet:**
- Independent benchmarks (Shwartz-Ziv & Armon 2022, Grinsztajn et al. 2022) show TabNet consistently underperforms XGBoost/CatBoost
- Interviewers may view it as "2019-era" thinking

**Why not TabR:**
- More complex (retrieval infrastructure adds engineering overhead)
- 3-day timeline favors simpler approach
- Good stretch goal / interview talking point

**Why not ExcelFormer/TabPFN:**
- Less established, fewer citations
- TabPFN designed for small datasets (<10K samples)
- Good to mention as "future directions"

## Interview Narrative

> "I implemented FT-Transformer (NeurIPS 2021) which showed that a principled adaptation of the Transformer — treating each tabular feature as a token — achieves the best average performance among deep learning models for tabular data. I then explored retrieval-augmented predictions inspired by TabR (ICLR 2024), which augments the network with nearest-neighbor reasoning. For movie prediction, this means the model explicitly reasons about similar historical films."

## Key Papers to Cite

1. Gorishniy et al. 2021 — "Revisiting Deep Learning Models for Tabular Data" (FT-Transformer)
2. Arik & Pfister 2021 — "TabNet: Attentive Interpretable Tabular Learning"
3. Gorishniy et al. 2024 — "TabR: Tabular Deep Learning Meets Nearest Neighbors"
4. Shwartz-Ziv & Armon 2022 — "Tabular Data: Deep Learning is Not All You Need"
5. Grinsztajn et al. 2022 — "Why Do Tree-Based Models Still Outperform Deep Learning on Tabular Data?"

## Related

- [[concepts/FT_Transformer]] — chosen algorithm
- [[concepts/TabR]] — stretch goal
- [[concepts/TabNet]] — comparison baseline
- [[entities/FT_Transformer_Paper]] — source paper