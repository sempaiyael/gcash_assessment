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

## Known Pitfalls (Pre-mortem + Validated)

| Pitfall | Prevention | Status |
|---------|------------|--------|
| IMDb TSV `\N` for nulls | Replace `\N` with NaN during load | Pending |
| startYear unreliable for upcoming films | Filter to startYear <= current year | Pending |
| Few votes = unreliable ratings | Configurable threshold, default 500 (D010) | Pending |
| MovieLens uses different IDs than IMDb | Use links.csv mapping file | Pending |
| Random train/test split leaks future | Use temporal split by release year | Pending |
| Class imbalance (hits are rare) | Use stratified split, consider SMOTE or class weights | Pending |
| FT-Transformer overfits on small data | Use early stopping, dropout, regularization | Pending |
| Kaggle datasets vary wildly in quality | Verify row count, null %, key columns before committing | Validated (F002) |
| Budget/revenue data is sparse for movies | Design hit metric to work without financial data (D011) | Validated (F003) |
| GitHub HTTPS requires token, not password | Generate PAT at github.com/settings/tokens with `repo` scope | Validated (F004) |