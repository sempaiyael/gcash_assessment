---
title: Decision Log
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [decisions, project-management]
---

# Decision Log

Chronological record of key project decisions. Reference IDs (D001, D002...) for use in code comments.

## D001: Primary Novel Algorithm — FT-Transformer
- **Date**: 2026-10-19
- **Decision**: Use FT-Transformer (NeurIPS 2021) as primary novel algorithm
- **Alternatives**: TabNet, NODE, TabR, ExcelFormer, SAINT, GrowNet, DeepGBM
- **Rationale**: Best avg performance among DL tabular models; NeurIPS venue = interview credibility; clean architecture easy to explain; PyTorch-native; good library support
- **Tradeoffs**: Not SOTA (TabR is better), but easier to implement in 3-day timeline
- **Status**: Accepted

## D002: Hit Metric — Option (c)
- **Date**: 2026-10-19
- **Decision**: Retrospective metric for labeling, greenlight-time features for prediction
- **Alternatives**: (a) pure retrospective, (b) pure predictive
- **Rationale**: Clean labels from retrospective data; actionable model from greenlight features
- **Status**: Accepted

## D003: Data Priority — IMDb First
- **Date**: 2026-10-19
- **Decision**: Start with IMDb datasets only; defer TMDb API
- **Rationale**: Faster start; avoid API rate limits; can augment later
- **Status**: Accepted (revisit Day 1 afternoon)

## D004: Scope — Aggressive with Bonus
- **Date**: 2026-10-19
- **Decision**: Attempt full scope including bonus recommender
- **Fallback**: Cut recommender if Day 2 runs long
- **Status**: Accepted

## D005: Wiki Format — Quick-Reference Cheat Sheets
- **Date**: 2026-10-19
- **Decision**: Use quick-reference cheat sheet style with links to deeper references
- **Rationale**: Token-efficient; dense info over verbose explanations; links allow drilling down when needed
- **Status**: Accepted

## D006: TMDb API Deferred
- **Date**: 2026-10-19
- **Decision**: Start with IMDb only; register TMDb API later if budget data needed
- **Rationale**: Faster start; avoid API rate limits; can augment after EDA validates approach
- **Status**: Superseded by D007

## D007: TMDb Data Source — Kaggle Dataset over API
- **Date**: 2026-10-20
- **Decision**: Use alanvourch's "Ultimate 1M Movies Dataset (TMDB + IMDb)" from Kaggle instead of TMDb API
- **Alternatives**: TMDb API (requires key, rate limits), Kaggle TMDb 2023 dataset (rejected — 3,966 rows, no imdb_id, 40% missing revenue)
- **Rationale**: No API key needed, no rate limits, already has imdb_id for joining, includes budget/revenue/cast/director, updated daily
- **Tradeoffs**: 665MB file size; only 1.2% have both budget+revenue (but covers major releases); data freshness depends on Kaggle update schedule
- **Verification**: Ran quality check — 1,261,171 rows, 30 columns, 55% have imdb_id, 38% have IMDb votes, 14,669 movies have both budget+revenue
- **Status**: Accepted

## D008: Actor Popularity Metric — Weighted Formula
- **Date**: 2026-10-20
- **Decision**: Actor popularity = `SUM( (1/log(ordering+1)) × numVotes × averageRating )` for each movie they appear in
- **Alternatives**: (a) Simple count of appearances, (b) SUM(numVotes), (c) SUM(numVotes × rating), (d) 1/ordering weighting
- **Rationale**: Multi-layered weighting handles edge cases: extras in many flops don't outrank leads in blockbusters. Billing order matters — co-leads get more credit than extras.
- **Components**:
  - `1/log(ordering+1)` — billing prominence (diminishing returns, see D009)
  - `numVotes` — audience reach proxy
  - `averageRating` — quality filter
- **Filter**: category in ["actor", "actress"] only (exclude self, archive_footage, etc.)
- **Status**: Accepted

## D009: Billing Weight Function — Logarithmic over Inverse
- **Date**: 2026-10-20
- **Decision**: Use `1/log(ordering+1)` instead of `1/ordering` for actor billing weight
- **Alternatives**: `1/ordering` (simple inverse)
- **Rationale**:
  - `1/ordering`: ordering 2 gets 50% of lead's weight — too harsh on co-leads
  - `1/log(ordering+1)`: ordering 2 gets 79% — more realistic for ensemble casts
  - Supporting actors (ordering 3-5) still contribute meaningfully
  - Extras (ordering 50+) get negligible weight either way
- **Presentation talking point**: "We weight actors by billing prominence using a logarithmic scale — top-billed actors get the most credit, but key supporting cast still contribute meaningfully."
- **Status**: Accepted

## D010: Min Vote Threshold — Configurable, Default 500
- **Date**: 2026-10-20
- **Decision**: Make min vote threshold a configurable parameter; start with 500 (not 1000)
- **Alternatives**: Fixed 1000 (wiki pre-mortem suggestion), fixed 100, adaptive
- **Rationale**: 500 includes more 2023 films while still filtering unreliable ratings. Configurable allows experimentation during EDA. Lower threshold = more data but noisier; higher = cleaner but smaller.
- **Status**: Accepted

## D011: Hit Metric — Two-Mode Approach
- **Date**: 2026-10-20
- **Decision**: Hit metric operates in two modes based on data availability
- **Full mode** (budget+revenue available): `weighted_rating × 0.4 + audience_reach × 0.3 + ROI × 0.3`
- **Partial mode** (no financial data): `weighted_rating × 0.6 + audience_reach × 0.4`
- **Rationale**: Only 1.2% of TMDb data has both budget and revenue. Two-mode approach avoids losing 98% of dataset. Movies without ROI use partial formula. Weights are placeholders — finalize during EDA.
- **Stakeholder note**: ROI is retrospective — it defines what IS a hit, not what we predict. Missing ROI at prediction time is acceptable.
- **Status**: Accepted (weights TBD during EDA)

## D012: Package Manager — UV over requirements.txt
- **Date**: 2026-10-20
- **Decision**: Use UV (Astral) as package manager instead of pip + requirements.txt
- **Alternatives**: pip + requirements.txt, poetry, conda
- **Rationale**: UV is faster (Rust-based), creates lockfile for reproducibility, manages Python versions, auto-creates .venv, single tool for env + deps
- **Tradeoffs**: Newer tool, less community examples. But uv.lock + pyproject.toml is the modern standard.
- **Setup**: `uv init --python 3.12 --no-package` then `uv add pandas numpy matplotlib seaborn pyarrow jupyter`
- **Files created**: pyproject.toml, uv.lock, .python-version, .venv/
- **Status**: Accepted

## D013: GitHub Repository — Private
- **Date**: 2026-10-20
- **Decision**: Create private GitHub repo at `https://github.com/sempaiyael/gcash_assessment`
- **Alternatives**: Public repo, GitLab, no remote
- **Rationale**: Private = control over who sees it. Share link directly with hiring managers. GitHub is industry standard.
- **Auth**: HTTPS + Personal Access Token (classic), scopes: `repo`
- **Status**: Accepted

## D014: isAdult Filter — Exclude Adult Content
- **Date**: 2026-10-20
- **Decision**: Filter `isAdult` to valid values (0 or 1), then exclude adult content (isAdult == 1)
- **Alternatives**: Drop column entirely, keep all content
- **Rationale**: Adult content (3.3% of dataset) not relevant for mainstream movie studio recommendation. Also fixes corrupt data (year values mixed into isAdult column).
- **Stakeholder discussion point**: "We excluded adult content as it's not relevant for mainstream movie studio recommendations. This could be discussed with stakeholders as a data cleaning decision."
- **Status**: Accepted

## D015: Technical Lead Grilling Practice
- **Date**: 2026-10-20
- **Decision**: Actively grill implementation plans before execution — challenge assumptions, identify conflicts with requirements, and propose better alternatives
- **Rationale**: Prevents wasted effort on approaches that would break downstream requirements. Example: caught 2023-only filter that would have made Q3, Q4, and Day 2 impossible.
- **Status**: Accepted — will apply to all future planning

## D016: Hit Metric Binary Label — 90th Percentile Threshold
- **Date**: 2026-10-20
- **Decision**: Binary hit/not-hit label uses 90th percentile (top 10%) of hit scores as threshold
- **Alternatives**: Fixed threshold (e.g., 0.7), top 20% (80th percentile)
- **Rationale**:
  - Industry realism: ~10% of movies are genuine hits (high ROI + high audience reach)
  - Class balance: ~7,100 hits out of ~71K movies = enough positive examples while keeping realistic imbalance
  - Statistical convention: 90th percentile is standard in anomaly detection and rare event prediction
  - Clarity: "We predict the top 10% of movies" is easy to explain to stakeholders
- **Implementation**: Threshold computed on training set only (avoid data leakage)
- **Status**: Accepted

## D017: Temporal Split — Train ≤2018, Test 2019-2023
- **Date**: 2026-10-20
- **Decision**: Train on movies ≤2018, test on movies 2019-2023 (5-year holdout)
- **Alternatives**: Train ≤2020 (3-year holdout), random 80/20 split
- **Rationale**:
  - Realistic simulation: Mimics real-world scenario (train on past, predict future)
  - No data leakage: Model never sees future data during training
  - Large holdout: 5 years of test data (~15K movies) = robust evaluation
  - Covers COVID: 2020-2021 had unusual patterns (theater closures, streaming boom). Tests generalization to disruptions.
  - Recent trends: Test set includes 2023 (most recent data), so we evaluate on current patterns.
- **Status**: Accepted