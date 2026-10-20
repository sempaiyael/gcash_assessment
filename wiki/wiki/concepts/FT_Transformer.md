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

## Deep Theory (for Interview Discussion)

### The Problem: Why Tabular Data Is Hard for Deep Learning

Traditional deep learning (CNNs, RNNs, Transformers) excels at:
- **Images**: Grid structure, translation invariance (CNNs)
- **Text**: Sequence structure, attention (Transformers)
- **Audio**: Time series structure (RNNs)

But **tabular data** has:
- **Heterogeneous features**: Mix of numerical (budget, runtime) and categorical (genre, language)
- **No natural structure**: Features don't have spatial/temporal relationships
- **Feature interactions**: Effect of "director" depends on "genre" (Nolan + Sci-fi ≠ Nolan + Romance)
- **Small datasets**: Often <1M rows (unlike images/text)

**Traditional ML for Tabular**: XGBoost (gradient boosted trees) handles heterogeneity well. Neural networks often underperform trees on tabular data.

### The Insight: Treat Features as Tokens

FT-Transformer adapts the Transformer by treating **each feature as a "token"** — just like words in a sentence.

**Traditional Transformer (NLP)**:
```
Input: "The cat sat on the mat"
Tokens: [The] [cat] [sat] [on] [the] [mat]
Each token → embedding → Transformer encoder → output
```

**FT-Transformer (Tabular)**:
```
Input: [director=Nolan] [genre=Sci-fi] [budget=200M] [cast=Hardy]
Tokens: [director] [genre] [budget] [cast]
Each token → embedding → Transformer encoder → output
```

### Architecture (Step by Step)

**Step 1: Feature Tokenization**
Each feature is converted to a vector (token embedding).

Numerical features (e.g., budget, runtime):
$$\mathbf{x}_i = \mathbf{W}_i \cdot x_i + \mathbf{b}_i$$

Categorical features (e.g., genre, language):
$$\mathbf{x}_i = \mathbf{E}_i[\text{category}_i]$$

Key insight: Each feature gets its own token embedding (unlike NLP where all words share one embedding table).

**Step 2: Add CLS Token**
A special [CLS] token is prepended to aggregate information from all features (like BERT).

**Step 3: Transformer Encoder**
Standard Transformer encoder layers:
- Multi-head self-attention: Each token attends to all other tokens
- Feed-forward network: Non-linear transformation
- Layer normalization + residual connections

Self-attention allows features to "look at" each other and learn interactions:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Interpretation for movies:
- "director" attends to "genre" → learns "Nolan + Sci-fi = good"
- "budget" attends to "genre" → learns "High budget + Action = blockbuster"
- "cast" attends to "director" → learns "Hardy + Nolan = bankable"

**Step 4: Prediction**
The [CLS] token output → final feed-forward layer → prediction:
$$\hat{y} = \sigma(\mathbf{W}_{\text{out}} \cdot \mathbf{h}_{\text{CLS}} + \mathbf{b}_{\text{out}})$$

### Why FT-Transformer Works Better Than Trees

| Aspect | XGBoost | FT-Transformer |
|--------|---------|----------------|
| Feature interactions | Explicit (tree splits) | Learned via attention |
| Non-linearity | Ensemble of trees | Deep neural network |
| Feature heterogeneity | Handles natively | Handles via tokenization |
| Interpretability | Feature importance | Attention weights |
| Scaling with data | Plateaus | Improves with more data |
| Transfer learning | No | Yes (pre-trained embeddings) |

**Key advantage**: Attention provides **interpretability**. We can see which features drive each prediction. For a studio director: "This movie is predicted to be a hit BECAUSE of director track record + genre timing + cast popularity."

### The Paper's Key Findings (Gorishniy et al., NeurIPS 2021)

1. FT-Transformer achieves **best average performance** among DL tabular models
2. It **outperforms XGBoost** on many datasets (but not all)
3. The **attention mechanism** provides interpretable feature interactions
4. It's **robust to hyperparameters** (unlike TabNet which is sensitive)

### Presentation Talking Points

1. "We chose FT-Transformer because it treats each feature as a token, allowing the model to learn feature interactions via self-attention."
2. "The attention mechanism provides interpretability — we can see which features drive each prediction."
3. "This is principled adaptation of the Transformer (NeurIPS 2021), not just a black box."
4. "We compare against XGBoost (strong tabular baseline) to demonstrate the value of deep learning."