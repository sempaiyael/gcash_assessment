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

## Leakage-Safe Implementation (Day 2, implemented)

**Final inventory**: 76 greenlight-time features in `data/features.parquet`, built by `src/feature_engineering.py`:

| Block | Features | Leakage note |
|---|---|---|
| As-of director | prior_films, prior_avg_hit, prior_avg_votes, years_since_debut/last, is_debut | prior years only (D020) |
| As-of cast (top-3 billing) | cast_pop_sum/mean/max (D008/D009 weights), cast_prior_films/avg_hit, actor-director prior collabs | past credits only |
| As-of company | company_prior_hit_max/mean, company_known (≥20-occurrence tokens) | comma-in-name hazard documented |
| As-of franchise | prior_releases, prior_avg_hit, is_sequel (title markers + shared-title groups) | heuristic — misses "The Dark Knight"-style franchise entries |
| Genre momentum | mean prior-year genre hit-rate | lag-1 by design |
| Static | log_budget + has_budget, runtime (+missing), genre multi-hot + count, is_usa, n_countries, certification, n_writers, keyword_count + top-15 kw flags, month sin/cos, is_summer/is_holiday, language | budget = greenlight estimate (caveat below) |
| Timing/language | from TMDb release_date + original_language (re-extracted, 692K rows) | 99.2% coverage |

**Banned as features** (they define or feed the label): `averageRating`, `numVotes`, `revenue`, `popularity` (TMDb post-release), `hit_score` and all its components, full-history `actor_popularity`/`director_stats` parquets. Enforced by `leakage_audit()`.

**Caveats to disclose**:
- **`keyword_count`** is FT-T's top permutation feature. TMDb keyword tagging richness correlates with a film's eventual attention — a metadata-recognition bias, not pure greenlight signal. Available at greenlight (marketing teams tag titles) but should be flagged in slides; removable without hurting XGB.
- **Budget** is *reported* budget (post-hoc), used as a greenlight *estimate* proxy — standard practice, slight optimism for big productions.
- **Franchise heuristic** is title-based; misses franchise entries with distinct titles (Dark Knight ≠ Batman). Keyword/IP features would fix this.

## Related

- [[concepts/Hit_Movie_Metric]] — what we're predicting
- [[concepts/IMDb_Datasets]] — data source
- [[concepts/Data_Sources]] — external APIs
- [[entities/Movie_Success_Paper]] — research basis