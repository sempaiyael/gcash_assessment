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

## Day-2 Empirical Results (test 2019-2023, thresholds tuned on val)

| Model | ROC-AUC | PR-AUC | F1 | Precision | Recall | Fit time |
|---|---|---|---|---|---|---|
| XGBoost | **0.865** | 0.368 | 0.402 | 0.366 | 0.446 | 4s |
| FT-Transformer | 0.863 | **0.379** | **0.406** | 0.355 | **0.475** | 72 min |
| Logistic Regression | 0.857 | 0.340 | 0.398 | 0.358 | 0.448 | 1s |

Story: FT-Transformer and XGBoost are **statistically tied on ROC-AUC**; FT-T wins on **PR-AUC/F1/recall** — the business metrics at an 8% base rate (PR-AUC baseline = 0.08). LR is the interpretable floor.

## Why FT-Transformer ≈ XGBoost (and why that's the correct outcome)

If asked "why didn't FT-T dominate?" — answer with evidence, not excuses:

1. **The ceiling is the features, not the model.** Only 0.008 AUC separates linear (0.857) from nonlinear (0.865). FT-T's value proposition = feature *interactions*; if interactions are weak it can only match trees, never beat them.
2. **Wrong data regime for tabular DL.** 47K rows of hand-crafted aggregates. Gorishniy et al. claim "competitive with GBDTs", not superiority; Grinsztajn et al. 2022 show trees win on medium tabular data; DL scaling wins start ~100K+ rows or learned representations.
3. **Our features are tree-native** — as-of counts/ratios/means are axis-aligned-split-friendly; trees handle skew + missing values for free.
4. **Zero tuning budget**, and FT-T is high-variance (277K params) while XGB early-stopped at 190 trees.
5. **Single seed** — 0.865 vs 0.863 is within noise. Honest claim: tie, with FT-T ahead on PR-AUC.
6. **2025-26 literature confirms it** — on the NeurIPS'25 TabPFN v2 critical-difference diagram, FT-T sits mid-pack alongside TabR/XGB; the only category that consistently beats tuned GBDTs is tabular *foundation* models (TabPFN family), which target exactly our data size.

## Expectation Anchor: 0.86 is strong at greenlight time

Any published 0.95+ AUC on movie success uses **post-release signals** (opening weekend, audience scores) — banned by design (D002). We deliberately predict with pre-production information only. **0.86 with greenlight-only features is the honest product; 0.95 would imply leakage.**

## The High-Precision Question (expected)

"Can you make it 90% precise?" → No — and we measured it (see [[concepts/Classification_Metrics]]):
- Val-threshold @90% precision transfers to test as precision 0.53-0.67 at ≤2% coverage; oracle ceiling on test = 90% only at ~1% recall
- Root causes: 8% base rate (needs 11x likelihood ratio), greenlight features cap the top end, label noise (two-mode D011), weighted-loss score inflation (predicted 81% vs actual 37% in top decile)
- **What we deliver instead**: precision@K slate — FT-T P@25 = 0.76 (~10x base rate), P@50 = 0.74; two-tier operating point (endorsement top-25 / review top-250) + recalibrated probabilities
- Business framing: the studio minimizes *false greenlights* ($50-200M each) — the endorsement tier is exactly that tool, with honest recall disclosure

## If Asked About TabPFN / Newer Models

"We benchmarked the landscape: TabPFN-2.5 (Feb 2026) is the current SOTA for our regime (≤50K rows) — an in-context tabular foundation model reporting an 87% win rate over default XGBoost up to 100K samples. TabR (ICLR'24) retrieval-augmentation is thematically ideal for movies ('find films like this one, see how they did'). We time-boxed a TabPFN implementation attempt; FT-Transformer remained our motivated choice for theory depth." Full landscape: [[concepts/Novel_Algorithm_Comparison]].

## Related

- [[concepts/FT_Transformer]] — the algorithm
- [[concepts/Novel_Algorithm_Comparison]] — full comparison
- [[concepts/Hit_Movie_Metric]] — the metric
- [[concepts/Presentation_Strategy]] — how to frame for audiences