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

## The Problem

Random train/test splits allow the model to "see the future" — a movie from 2023 in the training set leaks information about 2023 trends into predictions for 2022 test movies.

## The Solution

Split by time:
- **Train**: Movies released before year X
- **Test**: Movies released in year X and after

## Implementation

```python
train = df[df['startYear'] < 2020]
test = df[df['startYear'] >= 2020]
```

## Why It Matters

- Movie success depends on trends, audience preferences, market conditions
- These change over time (genre popularity, franchise fatigue, etc.)
- Random split gives artificially high performance
- Temporal split gives realistic estimate of future performance

## Related

- [[concepts/Classification_Metrics]] — what to measure on the split
- [[concepts/Movie_Feature_Engineering]] — features that have temporal aspects