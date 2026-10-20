---
title: Interview Narrative
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [interview, narrative, talking-points]
---

# Interview Narrative

Prepared talking points for explaining technical choices in interview settings.

## Why FT-Transformer

> "I implemented FT-Transformer (NeurIPS 2021) which showed that a principled adaptation of the Transformer — treating each tabular feature as a token — achieves the best average performance among deep learning models for tabular data. The key insight is feature tokenization: categorical features use lookup embeddings, numerical features use learnable scaling, and a standard Transformer encoder with self-attention naturally learns pairwise and higher-order feature interactions."

**If asked why not TabNet:**
> "Independent benchmarks (Shwartz-Ziv & Armon 2022, Grinsztajn et al. 2022) show TabNet consistently underperforms XGBoost/CatBoost on standard tabular benchmarks. FT-Transformer performs competitively and has a cleaner theoretical foundation."

**If asked why not just XGBoost:**
> "We use XGBoost as a baseline to demonstrate FT-Transformer's relative performance. The key advantage is interpretability via attention masks — we can show exactly which features drive each prediction, which is valuable for business stakeholders making investment decisions."

## TabR (If Asked About SOTA)

> "TabR (ICLR 2024) extends the FT-Transformer line with retrieval-augmented predictions. It augments the feed-forward network with a k-NN retrieval layer that finds similar training examples in a learned embedding space. For movie prediction, this means the model explicitly reasons about similar historical films. It's the current SOTA among parametric tabular DL models, but I chose FT-Transformer for the primary implementation due to time constraints."

## Hit Metric

> "We define 'hit' as a composite of three factors: weighted rating (Bayesian average that balances quality vs popularity), audience reach (numVotes as proxy for cultural impact), and ROI (profitability relative to budget). The model uses only greenlight-time features — director track record, cast star power, genre, franchise status — making it actionable for studio investment decisions."

## Why Option (c)

> "The hit metric is retrospective — we define what IS a hit using post-release data (ratings, box office). But the prediction model uses only greenlight-time features — what we know before production. This separation ensures the model is both well-labeled and actionable."

## Novel Algorithm Citation

Key papers to reference:
1. Gorishniy et al. 2021 — FT-Transformer (NeurIPS)
2. Shwartz-Ziv & Armon 2022 — "Tabular Data: Deep Learning is Not All You Need"
3. Grinsztajn et al. 2022 — "Why Do Tree-Based Models Still Outperform Deep Learning?"

## Related

- [[concepts/FT_Transformer]] — the algorithm
- [[concepts/Novel_Algorithm_Comparison]] — full comparison
- [[concepts/Hit_Movie_Metric]] — the metric
- [[concepts/Presentation_Strategy]] — how to frame for audiences