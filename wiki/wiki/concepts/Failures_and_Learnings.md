---
title: Failures and Learnings
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [failures, learnings, project-management]
---

# Failures and Learnings

Real-time record of mistakes and lessons. Prevents repeating errors across sessions.

## Format

- **What**: Brief description
- **Root cause**: Why
- **Impact**: Time/data/code cost
- **Lesson**: What to do differently

## Entries

### F001: scaffold.py Unicode Error on Windows
- **What**: scaffold.py failed with UnicodeEncodeError when printing ✓ character
- **Root cause**: Script uses Unicode ✓, Windows terminal defaults to cp1252 (no Unicode support)
- **Impact**: ~2 minutes to debug
- **Fix**: Set `$env:PYTHONIOENCODING='utf-8'` before running Python scripts on Windows
- **Prevention**: Use ASCII-safe output in scripts or set encoding explicitly

### F002: Kaggle TMDb 2023 Dataset — Poor Quality
- **What**: Downloaded `kaggle_TMBD_2023.zip` (3,966 rows). Missing imdb_id, 40.5% missing revenue, 23.6% missing budget. No ratings/votes data.
- **Root cause**: Small curated dataset, not comprehensive. Chosen before quality verification.
- **Impact**: ~5 minutes to verify and reject. No data loss.
- **Lesson**: Always verify dataset quality (row count, null %, key columns) before committing to a data source. Sample first, download full later.
- **Resolution**: Switched to alanvourch's "Ultimate 1M Movies Dataset" (D007)

### F003: TMDb Budget/Revenue Data Is Sparse
- **What**: Even in the 1.26M-row alanvourch dataset, only 6.8% have budget > 0, 2.3% have revenue > 0, 1.2% have both.
- **Root cause**: Most movies don't report financials. Industry-normal for non-major releases.
- **Impact**: ROI calculable for ~14,669 movies (mostly major releases). Hit metric needs two-mode approach (D011).
- **Lesson**: Don't filter dataset to only budget-available movies — would lose 98% of data. Use partial formula for movies without financials.
- **Mitigation**: Two-mode hit metric (D011). Major releases (our target) have better coverage.

### F004: GitHub HTTPS Auth Failure — Token Required
- **What**: `git push` failed with "Invalid username or token. Password authentication is not supported for Git operations."
- **Root cause**: GitHub deprecated password auth for git operations in 2021. Must use Personal Access Token (PAT) or SSH.
- **Impact**: ~5 minutes to resolve. Generated PAT at github.com/settings/tokens with `repo` scope.
- **Lesson**: For GitHub HTTPS, always use Personal Access Token as password. Or use `gh auth login` for browser-based auth.
- **Fix**: Generate PAT at https://github.com/settings/tokens (classic), scopes: `repo`. Use token as password when git prompts.

### F005: runtimeMinutes Stored as String
- **What**: `runtimeMinutes` column in `movies_clean.parquet` was stored as `str` instead of `int`. Caused errors when computing averages.
- **Root cause**: IMDb TSV stores runtime as string (e.g., "95", "120"). Pandas didn't auto-convert due to `\N` null values.
- **Impact**: ~2 minutes to fix. User manually cast to int in notebook 02.
- **Fix**: `movies['runtimeMinutes'] = movies['runtimeMinutes'].fillna(0).astype(int)`
- **Prevention**: Add dtype conversion to `load_imdb_tsv()` helper for all numeric columns.

### F006: torch Resolved to CPU-Only Wheel on Windows
- **What**: `uv add pytorch-tabular` pulled `torch==2.14.1+cpu` — CUDA unavailable, RTX 3060 idle.
- **Root cause**: PyPI serves CPU builds for Windows; CUDA builds live on download.pytorch.org indexes. Also: adding the cu130 index naively broke resolution ("numpy found on pytorch index but not at requested version") — uv's dependency-confusion guard stops at the first index that has a package.
- **Impact**: ~15 min to diagnose and fix.
- **Fix**: `[[tool.uv.index]] pytorch-cu130` with `explicit = true` + `[tool.uv.sources] torch = {index = "pytorch-cu130"}` → `torch==2.14.1+cu130` (1.9GB). Everything else resolves from PyPI.
- **Lesson**: After any torch install, immediately check `torch.cuda.is_available()`. Use explicit-index + uv.sources for pytorch, never a bare `--index`.

### F007: pytorch-tabular Custom Loss Only via fit() kwarg
- **What**: Passing a custom `WeightedCrossEntropy` instance in `FTTransformerConfig(loss=...)` crashed: "module 'torch.nn' has no attribute 'WeightedCrossEntropy()'".
- **Root cause**: OmegaConf coerces the config field to str; `_setup_loss` does `getattr(nn, self.hparams.loss)()`. The supported path is `TabularModel.fit(..., loss=<nn.Module>)` → `custom_loss`.
- **Impact**: ~5 min. Caught by the 20% timing-gauge run, not the full run.
- **Lesson**: pytorch-tabular config fields are strings; custom objects (loss, metrics) go through `prepare_model`/`fit` kwargs. Gauge runs catch API mismatches cheaply.

### F008: torchmetrics `auroc` Crashes on Binary Targets
- **What**: `metrics=["auroc"]` raised `ValueError: Expected preds to have one more dimension than target` during validation.
- **Root cause**: pytorch-tabular's `calculate_metrics` passes per-class 1-D columns; torchmetrics' `auroc` dispatcher landed on multiclass mode. Version-mismatch between pytorch-tabular 1.2 and torchmetrics 1.8.
- **Impact**: ~10 min. Worked around, not fixed (library bug).
- **Fix**: `metrics=["accuracy"]` + early stopping on `valid_loss` (mode min). Real AUC/F1/PR computed by our own `src/evaluation.py`.
- **Lesson**: Never rely on library metric plumbing for the headline numbers — compute evaluation metrics yourself.

### F009: NaN Loss from Unhandled Input NaNs
- **What**: FT-Transformer `train_loss: nan` from epoch 0; all predictions NaN; early stopping aborted after 1 epoch.
- **Root cause**: Features contain NaN by design (e.g., `director_prior_avg_hit` 41% NaN = debut directors). Nullable Float64 (`release_month`) + residual NaNs leaked through the datamodule scaler (`normalize_continuous_features`) into the forward pass.
- **Impact**: ~15 min to diagnose (the 20% gauge reproduced it — again cheaper than a full run).
- **Fix**: Explicit `_prep()` in `ft_transformer_model.py`: cast all numeric to plain float64, fill NaN with fit-split medians, normalize categoricals to str. Applied identically at predict time via stashed medians.
- **Lesson**: Never assume a library's `handle_missing_values` covers pandas nullable dtypes. Sanitize inputs yourself; treat the model as dtype-strict.

### F010: sklearn permutation_importance vs pytorch-tabular — Two Failures
- **What**: (1) `'_FttProba' object has no attribute '__sklearn_tags__'` (sklearn 1.9 requires BaseEstimator); (2) after fixing, 77 `predict()` calls rebuilt the dataloader each time → 15-min timeout.
- **Root cause**: sklearn 1.x estimator-tag API; pytorch-tabular `predict()` has heavy per-call overhead.
- **Impact**: ~20 min.
- **Fix**: Batched permutation: stack 76 permuted copies of the 2,000-row sample into ONE 154K-row predict call, then compute per-block AUC drop. 314s for the predict, done in one shot.
- **Lesson**: When wrapping deep models for sklearn tools, prefer hand-rolled loops with batched inference. Per-call predict overhead dominates anything that calls predict O(n_features) times.

### F011: FT-T Attention Importance Shape Mismatch
- **What**: `feature_importance()` returned 152 values for 76 features ("Length of values (152) does not match length of index (76)").
- **Root cause**: pytorch-tabular 1.2.0 attention-importance aggregation bug (attn weights summed over heads/layers leave 2× features).
- **Impact**: ~5 min. Worked around via F010's batched permutation importance.
- **Lesson**: Interpretability paths in libraries are the least-tested code — always have a model-agnostic fallback (permutation importance).

### F012: Timing Gauge Under-Extrapolated 20x on FT-Transformer
- **What**: 20% gauge predicted ~196s full fit; actual full fit = 4,322s (72 min). Total run 72.9 min vs 45-min OK threshold.
- **Root cause**: Per-batch time grew 10x between the gauge epoch (19 batches @ 6.4 it/s) and the full epoch (92 batches @ 0.93 it/s) — dataloader/collation contention at larger epoch sizes, not row-count scaling.
- **Impact**: No result impact (model completed and beat LR), but timeline risk.
- **Lesson**: Extrapolate by **batches/epoch × epoch count**, and include at least one FULL-size epoch in the gauge (e.g., 1 epoch on 100%) before committing. For refits: batch_size 1024 + `num_workers` or `max_epochs=25` caps cost.

### F013: SVD++ Gauge Mis-Extrapolation — Quadratic-in-History Cost
- **What**: SVD++ gauge (5% rating sample) extrapolated to ~28 min full run; reality = hours (60-min timeout killed a run with no result).
- **Root cause**: surprise's SVD++ updates implicit y-factors for every item in a user's history **on every rating** — cost is O(Σ_u |I_u|²·f). A random rating-sample shrinks per-user histories 20x, making per-rating cost ~20x cheaper in the gauge than in production. Second instance of F012's lesson: cost is not linear in row count.
- **Impact**: ~60 min lost to one killed run. Fixed by restructuring: SVD++ on a 5K warm-user cohort with histories intact + plain SVD (O(|R|·f)) on full data.
- **Lesson**: Before gauging an algorithm, write down its complexity class and what the sample changes. **Sample users-with-full-histories, not rows**, whenever per-row cost depends on group size. Also: run Python with line buffering (`sys.stdout.reconfigure(line_buffering=True)`) so timeouts keep the logs.

### F014: Cohort Sampling Design Determines Ranking-Metric Size
- **What**: First full recommender run reported ranking metrics over 230 users; expected ~5,000.
- **Root cause**: Cohort sampled uniformly from train users — but only 6,492 of 150K train users are "warm" (appear in the future test window), so the cohort ∩ evaluable ≈ 230.
- **Impact**: Results usable but under-powered; re-run with warm-user cohort (4,814 eval users) cost ~55 min.
- **Lesson**: When evaluation requires users in both splits, sample the cohort from the intersection — uniform sampling of the wrong population silently shrinks your eval set. Always print n_eval alongside metrics.

## Known Pitfalls (Pre-mortem + Validated)

| Pitfall | Prevention | Status |
|---------|------------|--------|
| IMDb TSV `\N` for nulls | Replace `\N` with NaN during load | Validated (Day 1) |
| startYear unreliable for upcoming films | Filter to startYear <= current year | Validated (D021: dropped 2024+) |
| Few votes = unreliable ratings | Configurable threshold, default 500 (D010) | Validated (Day 1) |
| MovieLens uses different IDs than IMDb | Use links.csv mapping file | Pending (recommender) |
| Random train/test split leaks future | Use temporal split by release year | Validated (D017/D022) |
| Class imbalance (hits are rare) | Loss weighting + val-tuned threshold (D023) | Validated |
| FT-Transformer overfits on small data | Early stopping on valid_loss, dropout, weighted loss | Validated (D024) |
| Kaggle datasets vary wildly in quality | Verify row count, null %, key columns before committing | Validated (F002) |
| Budget/revenue data is sparse for movies | Design hit metric to work without financial data (D011) | Validated (F003) |
| GitHub HTTPS requires token, not password | Generate PAT at github.com/settings/tokens with `repo` scope | Validated (F004) |
| torch resolves CPU-only on Windows | Explicit pytorch index + `torch.cuda.is_available()` check | Validated (F006) |
| Library custom-loss/metric plumbing is brittle | Pass via fit() kwargs; compute metrics in own code | Validated (F007/F008) |
| NaN inputs NaN the loss through scalers | Explicit float64 + median impute before fit | Validated (F009) |
| Timing gauges under-extrapolate | Extrapolate by batches; gauge one full-size epoch | Validated (F012) |