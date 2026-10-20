---
title: Hit Movie Metric
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [metric, business, movie-prediction]
---

# Hit Movie Metric

Composite index capturing "AAA title" potential. Must justify in context of studio investment decisions.

## Approach: Option (c)

- **Retrospective metric** for labeling (defines what IS a hit)
- **Greenlight-time features** for prediction (what we can know before production)

## Components (Draft)

| Component | Rationale | Data Source |
|-----------|-----------|-------------|
| Weighted Rating | Balance avg rating vs vote count | IMDb ratings + numVotes |
| Audience Reach | Proxy for cultural impact | numVotes (normalized) |
| ROI | Profitability relative to budget | Revenue / Budget (if available) |
| Critical Acclaim | Award nominations/wins | Augmented data (optional) |

## Weighted Rating Formula

IMDB's Bayesian average:
$$WR = \frac{v}{v+m} \cdot R + \frac{m}{v+m} \cdot C$$

Where:
- $R$ = average rating
- $v$ = number of votes
- $m$ = minimum votes required (e.g., 25th percentile)
- $C$ = mean rating across all movies

## Business Framing

For studio director: "Which movies should we invest in?"
- High weighted rating = quality
- High numVotes = broad audience appeal
- High ROI = financial success

## Two-Mode Implementation (D011)

Budget/revenue data is sparse (~1.2% of TMDb dataset). Hit metric operates in two modes:

| Mode | Data Available | Formula | Coverage |
|------|---------------|---------|----------|
| **Full** | Budget + Revenue | `WR×0.4 + Reach×0.3 + ROI×0.3` | ~14,669 movies |
| **Partial** | Ratings + Votes only | `WR×0.6 + Reach×0.4` | ~481,442 movies |

**Component Definitions**:
- WR = IMDB Bayesian weighted rating (normalized 0-1)
- Reach = log(numVotes) normalized (0-1)
- ROI = (revenue - budget) / budget, capped and normalized (0-1)

**Validation**: Check that known hits (Avengers, Dark Knight, Barbie) rank in top decile.

**Stakeholder note**: ROI is retrospective — it defines what IS a hit, not what we predict. The model uses greenlight-time features (D002) for prediction. Missing ROI at prediction time is acceptable.

## Binary Label Threshold (D016)

For the prediction model, we need a binary hit/not-hit label. The threshold is the **90th percentile** (top 10%) of hit scores.

### Formula
$$\text{hit\_label} = \begin{cases} 1 & \text{if hit\_score} \geq P_{90} \\ 0 & \text{otherwise} \end{cases}$$

Where $P_{90}$ is the 90th percentile of hit scores in the **training set** (computed on training data only to avoid data leakage).

### Why 90th Percentile (Not Fixed Threshold or 80th)?

| Approach | Problem |
|----------|---------|
| **Fixed threshold (e.g., 0.7)** | Arbitrary. Distribution varies by era. Why 0.7 and not 0.65? |
| **Top 20% (80th pctl)** | Too generous. ~20% of movies being "hits" is unrealistic. Studios are selective. |
| **Top 10% (90th pctl)** | Industry-realistic. ~10% of movies are genuine hits. Statistically robust. Easy to explain. |

### Business Justification
- **Industry realism**: ~10% of movies are genuine hits (high ROI + high audience reach). Aligns with real-world greenlight decisions.
- **Class balance**: ~7,100 hits out of ~71K movies. Enough positive examples for training while keeping realistic class imbalance.
- **Statistical convention**: 90th percentile is standard in anomaly detection and rare event prediction.
- **Clarity**: "We predict the top 10% of movies" is easy to explain to stakeholders.

## Status

Finalized Day 1 (2026-10-20). Weights are placeholders — validate during EDA against known hits. Binary threshold = 90th percentile (D016).

## Related

- [[concepts/Movie_Feature_Engineering]] — what features predict hits
- [[concepts/Classification_Metrics]] — how to evaluate the model