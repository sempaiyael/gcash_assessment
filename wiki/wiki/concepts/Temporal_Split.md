---
title: Temporal Split
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [evaluation, data-splitting, methodology]
---

# Temporal Train/Test Split

Why random splits leak future information for time-dependent data.

## Detailed Justification (D017)

### The Problem with Random Split

Random train/test splits allow the model to "see the future" — a movie from 2023 in the training set leaks information about 2023 trends into predictions for 2022 test movies.

**Real-world scenario**:
- A studio in 2024 wants to predict which 2025 movie will be a hit.
- The model should only have access to movies from ≤2024.
- If the model has seen 2025 movies during training, it's cheating.

### Our Split: Train ≤2018, Test 2019-2023

```python
train = movies[movies['startYear'] <= 2018]
test = movies[movies['startYear'] >= 2019]
```

| Aspect | Benefit |
|--------|---------|
| **Realistic simulation** | Mimics real-world: train on past, predict future |
| **No data leakage** | Model never sees future data during training |
| **Large holdout** | 5 years of test data (2019-2023) = ~15K movies = robust evaluation |
| **Covers COVID** | 2020-2021 had unusual movie patterns (theater closures, streaming boom). Tests if model generalizes to disruptions. |
| **Recent trends** | Test set includes 2023 (most recent data), so we evaluate on current patterns. |

### Why Not Other Splits?

| Split | Problem |
|-------|---------|
| **Train ≤2020, Test 2021-2023** | Smaller holdout (3 years), less robust evaluation |
| **Train ≤2015, Test 2016-2023** | Training data becomes stale. Movie industry changes fast (streaming, superhero franchises). |
| **Random 80/20** | Data leakage. Model sees future during training. |

### The Sweet Spot
- **Training**: ~55K movies (1920-2018) = enough data
- **Test**: ~15K movies (2019-2023) = robust evaluation
- **Recent enough** to capture modern patterns

## The Solution

Split by time:
- **Train**: Movies released before year X
- **Test**: Movies released in year X and after

## Implementation

```python
train = df[df['startYear'] < 2020]
test = df[df['startYear'] >= 2020]
```

## As-of Feature Computation (D020) — the part people forget

Splitting the rows is not enough. **Historical features must also be temporal** — full-history aggregates (e.g., `actor_popularity.parquet` computed over all years) leak test-era outcomes into training features.

**Pattern (implemented in `src/feature_engineering.py`)**: aggregate per (entity, year), then cumulate with `shift(1)`:

```python
dy = base.groupby(["entity", "startYear"]).agg(**specs)   # one row per entity-year
cum = dy.groupby("entity")[col].cumsum()                   # running totals
dy[f"{prefix}_prior_{col}"] = cum.groupby(dy["entity"]).shift(1)  # PRIOR years only
```

Merge back on (entity, startYear): every movie in year Y sees the same prior-year totals — strictly earlier releases only. Same-year releases are concurrent and correctly invisible to each other.

**Spot check**: The Dark Knight (2008) sees Nolan's exactly 5 prior films (Following→Batman Begins) — not Interstellar (2014). A debut director gets `prior_films=0` + `is_debut=1`, not NaN-from-the-future.

Applies to: director track record, cast star power (D008/D009 formula on *past* credits), company track record, franchise installments, genre trend momentum.

**Audit**: `leakage_audit()` asserts banned columns (`averageRating`, `numVotes`, `revenue`, `popularity`, `hit_score` components, full-history aggregates) never appear in the feature matrix — it caught two slips during development.

## Why It Matters

- Movie success depends on trends, audience preferences, market conditions
- These change over time (genre popularity, franchise fatigue, etc.)
- Random split gives artificially high performance
- Temporal split gives realistic estimate of future performance

## Related

- [[concepts/Classification_Metrics]] — what to measure on the split
- [[concepts/Movie_Feature_Engineering]] — features that have temporal aspects