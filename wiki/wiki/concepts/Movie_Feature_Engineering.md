---
title: Movie Feature Engineering
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [movie-success-paper]
tags: [features, engineering, movie-prediction]
---

# Movie Feature Engineering

Features for predicting movie success. Prioritized by research evidence.

## Feature Priority

| Feature | Source | Predictive Power | Available at Greenlight |
|---------|--------|-----------------|------------------------|
| Director avg historical gross | IMDb filmography | HIGH | Yes |
| Cast star power (total/avg gross) | IMDb filmography | MEDIUM-HIGH | Yes |
| Franchise/sequel status | TMDb/Wikidata | HIGH | Yes |
| Production budget | TMDb/The Numbers | HIGH | Estimated |
| Genre + genre trend momentum | Box Office Mojo | MEDIUM | Yes |
| Production company track record | TMDb/IMDb | MEDIUM | Yes |
| MPAA rating | Early announcements | MEDIUM | Target only |
| Release season | Production schedule | MEDIUM | Target |
| Plot synopsis NLP | TMDb | MEDIUM-HIGH | Yes |
| Cast novelty / genre expertise | IMDb network | MEDIUM | Yes |

## Key Insight (Lash & Zhao 2016)

- Director's avg historical gross = #1 predictor (information gain)
- Budget predicts revenue well but ROI poorly
- Star power correlates with revenue but NOT profitability

## Budget Data Research

Budget is the strongest predictor in multiple studies:

| Study | Finding |
|-------|---------|
| Udandarao & Gupta (2024) | Budget had highest SelectKBest score (~6,569), far exceeding all other features |
| Cheang et al. (2021) | Budget top-ranked feature in neural network model (88.8% accuracy) |
| Berkeley (Hu) | log(Budget) coefficient 0.675 in log-linear regression |
| Lash & Zhao (2016) | Revenue and profitability nearly uncorrelated (r=0.077) |

**Key nuance**: Budget predicts *revenue* well but *profitability* (ROI) poorly. A $200M film that grosses $200M is a failure. A $5M film that grosses $50M is a hit.

## Feature Availability Timing

| Stage | Features Available | Predictive Power |
|-------|-------------------|-----------------|
| **Greenlight** (script exists, talent attached) | Director history, cast power, franchise/IP, genre, production company, target rating, target season | HIGH |
| **Post-production** (film complete) | Final runtime, final MPAA rating, full cast list | MEDIUM |
| **Post-release** (in theaters) | Opening weekend, theater count, audience scores, critical reviews, marketing buzz | VERY HIGH |

**Our model uses greenlight-time features only** (D002) — makes predictions actionable for investment decisions.

## Full Feature List

| Feature | Source | Power | Greenlight? |
|---------|--------|-------|-------------|
| Director avg historical gross | IMDb filmography | HIGH | Yes |
| Cast star power (total/avg gross) | IMDb filmography | MEDIUM-HIGH | Yes |
| Franchise/sequel status + prior performance | TMDb/Wikidata | HIGH | Yes |
| Production budget (estimated) | TMDb/The Numbers | HIGH | Estimated |
| Genre + genre trend momentum | Box Office Mojo | MEDIUM | Yes |
| Production company track record | TMDb/IMDb | MEDIUM | Yes |
| MPAA rating (target) | Early announcements | MEDIUM | Target only |
| Release season | Production schedule | MEDIUM | Target |
| Plot synopsis NLP | TMDb | MEDIUM-HIGH | Yes |
| Cast novelty / genre expertise | IMDb network | MEDIUM | Yes |
| Adaptation source (book, comic, true story) | TMDb | LOW-MEDIUM | Yes |
| Actor-director collaboration history | IMDb network | MEDIUM | Yes |

## Actor Popularity Formula (D008, D009)

For each actor in a movie:
```
score = (1 / log(ordering + 1)) × numVotes × averageRating
```

**Actor Popularity** = SUM(score) across all their films in the dataset

**Components**:
- `1/log(ordering+1)`: billing prominence (diminishing returns — see D009 for comparison with 1/ordering)
- `numVotes`: audience reach proxy
- `averageRating`: quality filter

**Filter**: `category` in ["actor", "actress"] only (exclude self, archive_footage, etc.)

**Why this works**: A lead in a blockbuster (ordering=1, 1M votes, 8.0 rating) scores 8M. An extra in 50 flops (ordering=50, 100 votes, 5.0 rating each) scores ~500 total. Correctly ranks star power.

## Data Sources for Features

See [[concepts/Data_Sources]] for full API/source details.

## Implementation Notes

- Compute director/cast features from IMDb filmography (title.principals + title.ratings)
- Genre trends: rolling avg of genre profitability by year
- Franchise: binary flag + prior installment performance
- Budget: from Kaggle TMDb dataset (D007) — 14,669 movies with both budget+revenue

## Related

- [[concepts/Hit_Movie_Metric]] — what we're predicting
- [[concepts/IMDb_Datasets]] — data source
- [[concepts/Data_Sources]] — external APIs
- [[entities/Movie_Success_Paper]] — research basis