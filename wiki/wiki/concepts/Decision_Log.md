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

## D018: Environment Anchored on pytorch-tabular — pandas Pinned <3
- **Date**: 2026-10-22
- **Decision**: Adjust the environment to fit pytorch-tabular, not the reverse. `pandas>=2.2,<3` (installed 2.3.3), numpy stays 2.5.4. Torch from the pytorch.org cu130 index (`torch==2.14.1+cu130`, explicit index + `[tool.uv.sources]`).
- **Alternatives**: Drop pytorch-tabular for rtdl/custom FT-Transformer; downgrade numpy too
- **Rationale**: pytorch-tabular 1.2.0 hard-pins `pandas<3.0.0` (verified on PyPI). It is the fastest, most reliable FT-Transformer path (Lightning trainer, categorical embeddings, maintained Jan 2026). Only pandas needed to move — numpy 2.5.4 satisfies `numpy<=3.0.0`. Day-1 parquet artifacts unaffected (pyarrow-written).
- **Verification**: GPU smoke test (200 synthetic rows, 2 epochs, fit + predict) passed BEFORE any extraction work — install success ≠ runtime compatibility.
- **Status**: Accepted

## D019: TabNet Dropped from Committed Plan
- **Date**: 2026-10-22
- **Decision**: Baselines = Logistic Regression + XGBoost + FT-Transformer. Drop TabNet.
- **Rationale**: The novel-algorithm slot is FT-Transformer (D001); LR is the linear floor, XGBoost the tabular-GBDT benchmark. TabNet is a second DL tabular model that typically loses to XGBoost — costs VRAM/debug time with zero narrative gain. pytorch-tabular bundles TabNet (TabNetConfig) if ever needed.
- **Status**: Accepted

## D020: As-of-Year Rolling Historical Features (Leakage-Safe)
- **Date**: 2026-10-22
- **Decision**: Director/cast/company/franchise/genre-momentum features computed as-of: per (entity, year) aggregates cumulated with `shift(1)` — a movie sees only outcomes of strictly earlier releases. Replaces the leaky full-history `actor_popularity`/`director_stats` parquets.
- **Alternatives**: Frozen-at-2018 stats; full-history aggregates (rejected — future leakage)
- **Rationale**: Realistic greenlight information (historical track record only), defensible in interview; same-year releases are concurrent and invisible to each other. Spot-checked: The Dark Knight (2008) correctly sees Nolan's 5 prior films.
- **Status**: Accepted

## D021: Test Window — Drop 2024+ Rows
- **Date**: 2026-10-22
- **Decision**: Modeling frame = startYear ≤ 2023. The 5,257 rows from 2024-2026 are dropped (strict D017 window).
- **Rationale**: 2024+ labels are noisy (incomplete box office/revenue runs) and D017 explicitly defines test as 2019-2023. Mention in slides as a future deployment set.
- **Status**: Accepted

## D022: Temporal Internal Validation — fit ≤2015 / val 2016-2018
- **Date**: 2026-10-22
- **Decision**: Within train ≤2018: fit = ≤2015 (46,946 rows), val = 2016-2018 (7,218 rows). Val serves early stopping + F1-threshold tuning. Label threshold P90 computed on fit+val (all ≤2018) per D016.
- **Rationale**: A random val would leak future patterns into model selection; temporal val matches deployment. Test untouched (11,635 rows, 2019-2023).
- **Status**: Accepted

## D023: Class Imbalance Handling + Threshold Tuning
- **Date**: 2026-10-22
- **Decision**: LR `class_weight='balanced'`; XGBoost `scale_pos_weight = neg/pos = 8.76`; FT-Transformer weighted CrossEntropy (`w_pos = 8.76`) passed via `fit(loss=...)` kwarg. Report metrics at 0.5 AND at an F1-optimal threshold tuned on val (~0.69-0.72).
- **Rationale**: ~8-10% positive rate (D016). Imbalance handled at loss level; operating point chosen on val, never on test. PR-AUC is the primary ranking metric (baseline 8%).
- **Status**: Accepted

## D024: FT-Transformer Training Config — valid_loss Monitoring, Permutation Importance
- **Date**: 2026-10-22
- **Decision**: Early stopping/checkpoints on `valid_loss` (not `valid_auroc`); feature importance via batched permutation AUC (not attention weights).
- **Rationale**: torchmetrics `auroc` dispatch crashes for binary targets in this pytorch-tabular 1.2 stack (F008); pytorch-tabular's attention importance returns 152 values for 76 features (F011). Weighted loss + own evaluation module (AUC/F1/PR) cover model selection honestly; permutation importance is model-agnostic and comparable across all three models.
- **Status**: Accepted

## D025: High-Precision Framing — Two-Tier Slate, Not a 90% Threshold
- **Date**: 2026-10-22
- **Decision**: Deliver the high-precision story as a **precision@K slate** with a two-tier operating point (endorsement top-25 ≈ 75-80% precision; review top-250 ≈ 55%), plus isotonic/Platt recalibration on val. Do NOT chase a fixed 90% precision threshold.
- **Alternatives**: Tune threshold to 90% precision; retrain optimizing precision (focal loss)
- **Rationale**: Measured — val-thresholds at 90% precision transfer to test as 0.53-0.67 precision at ≤2% coverage; even oracle-on-test reaches 90% only at ~1% recall. Root causes: 8% base rate, greenlight-feature ceiling (D002), two-mode label noise (D011), weighted-loss score inflation (top decile: predicted 81% vs actual 37%). Business-wise the studio minimizes false greenlights ($50-200M) — the endorsement tier delivers that with honest recall disclosure. P@25=0.76 ≈ 10x base rate.
- **Status**: Accepted

## D026: Slides First, Then Time-Boxed TabPFN-2.5 Experiment
- **Date**: 2026-10-22
- **Decision**: Day-3 sequence: (1) executive slides, (2) 60-min TabPFN-2.5 experiment (skip without ceremony if slides slip), (3) recommender only if both done. FT-Transformer remains the motivated novel algorithm regardless of TabPFN outcome.
- **Rationale**: Deadline 2026-10-23 with buffer (user is a day ahead of the original 3-day plan); slides are the graded deliverable. TabPFN-2.5 (arXiv 2511.08667, Feb 2026) is the one model category that consistently beats tuned GBDTs on our data regime (≤50K rows) and is inference-only (no training loop) — high story value per minute. TabR/RealMLP/TabM stay as cited future work.
- **Status**: Superseded in sequence by D028 (TabPFN pinned → recommender prioritized); experiment itself remains planned.

## D027: Recommender Protocol — Temporal Split, Warm-User Eval, SVD++ Cohort
- **Date**: 2026-10-22
- **Decision**: MovieLens ml-25m (25M ratings): temporal 90/10 split by timestamp; item support filter ≥200 train ratings (D010 philosophy, keeps 96.7% of ratings); evaluate on warm users only (user + item in train) with coverage reported; ranking via sampled-candidate protocol (relevant = test rating ≥4.0 vs 100 distractors). SVD++ trained on a 5K warm-user cohort (all histories intact); plain SVD scales to the full 21.8M training ratings.
- **Rationale**: Temporal split keeps the no-leakage narrative (D017/D022). SVD++ in surprise costs O(Σ_u |I_u|²·f) — quadratic in user history — making full-data training hours/epoch (F013); a rating-sample gauge understates this because it shortens histories. Cohort-with-full-histories is the honest compromise; SVD-full covers scale.
- **Status**: Accepted

## D028: TabPFN-2.5 Pinned — Recommender Prioritized
- **Date**: 2026-10-22
- **Decision**: Pin the TabPFN-2.5 experiment (blocked on Prior Labs license acceptance for model weights) and deliver the bonus recommender instead. Experiment script preserved locally outside version control.
- **Rationale**: User preference; recommender is an exam bonus deliverable with clear value, while TabPFN requires an external account action and is a "nice-to-have" leaderboard row.
- **Status**: Accepted — revisit per Deferred_Items