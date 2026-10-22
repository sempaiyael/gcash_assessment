# GCash Movie Project Knowledge Base

> Project knowledge base and decision record — review at the start of each working session together with wiki/index.md.

## Project Context

**Why this exists**: Job application exam for GCash (AI Engineering / Data Science / Machine Learning role). The hiring team sent a sample project as an assessment.

**What it simulates**: End-to-end data science flow at GCash — data engineering, analysis, modeling, and storytelling around a business problem.

**The ask**: "Give Me The Next AAA Title" — use IMDb/MovieLens data to help a movie studio decide how to make the next hit movie. Deliverables include EDA, a hit movie metric, a prediction model with a novel algorithm, and executive presentations.

**What "success" looks like**:
- Polished executive presentations (not Jupyter dumps)
- Clean, reproducible code in a Git repository
- Creative use of data + algorithms beyond standard ML
- Ability to discuss theoretical underpinnings from source papers
- Business framing that convinces hypothetical management

**Key guidance from the email**:
- "We encourage creativity and technical rigor"
- "Motivate your choice of a novel algorithm and be prepared to discuss its theoretical underpinnings"
- "Be as creative as possible and incorporate other data sets, features, and algorithms"

**Bonus (improves chances)**: Recommender system using MovieLens + second presentation for streaming service management.

**Submission**: Email slides, code, and files to the hiring team.

**See also**: [[concepts/Quality_Standards]] · [[concepts/Success_Criteria]] · [[concepts/Differentiation_Strategy]] · [[concepts/Submission_Checklist]]

## Scope

Covers:
- Tabular deep learning (FT-Transformer, TabNet, TabR, ExcelFormer)
- Movie success prediction: feature engineering, hit metrics, greenlight modeling
- Recommender systems: collaborative filtering, SVD++, evaluation
- IMDb and MovieLens datasets
- Evaluation methodology, business storytelling
- Project decisions, failures, learnings, workflow

Excludes:
- General ML tutorials, subjective film analysis

## Session Checklist

Each working session should:
1. Read this file + wiki/index.md
2. Read Decision Log [[concepts/Decision_Log]]
3. Read Failures and Learnings [[concepts/Failures_and_Learnings]]
4. Read Deferred Items [[concepts/Deferred_Items]]
5. Check log/ for most recent day's activity
6. Log any decisions, failures, or learnings from the session before ending

## Current Project State

- **Phase**: Day 2 complete — features + models done. Ready for Day 3 (slides, polish, submission).
- **Timeline**: 3 days (Day 1 = 2026-10-20, Deadline = 2026-10-22)
- **GitHub**: https://github.com/sempaiyael/gcash_assessment (private, D013)
- **Package Manager**: UV (pyproject.toml + uv.lock, D012). pandas 2.3.3 pinned <3 (D018), torch 2.14.1+cu130
- **Primary Model**: FT-Transformer (pytorch-tabular 1.2.0, GPU) — test ROC-AUC 0.863, PR-AUC 0.379 (best)
- **Baselines**: XGBoost (ROC-AUC 0.865), Logistic Regression (0.857). TabNet dropped (D019)
- **Bonus Model**: SVD++ recommender (not started — cut first if time tight)
- **Data**: IMDb TSVs + TMDb Kaggle (D007). Modeling frame: 65,799 movies (2024+ dropped, D021)
- **Features**: 76 greenlight-time features, as-of leakage-safe (D020) — src/feature_engineering.py
- **Split**: fit ≤2015 / val 2016-2018 / test 2019-2023 (D022). P90 label = 0.5612 (D016)
- **Results**: reports/tables/model_comparison.{csv,md}, reports/figures/model_*.png
- **Precision story**: P@25=0.76 (FT-T, ~10x base rate); 90% precision unreachable (measured) → two-tier slate (D025)
- **Presentation**: Studio exec deck in authoring (emailed deliverable — not committed to the repo)
- **Bonus**: MovieLens recommender DONE — SVD/SVD++/KNN on ml-25m, temporal eval (D027); SVD-full RMSE 0.804, NDCG@10 0.543
- **Wiki**: concept + entity pages, 3 day logs, results/precision/landscape documented
- **Next action**: Studio + streaming decks in authoring (owner-authored; content reviewed against the analysis); TabPFN-2.5 pinned (Deferred Items)

## Key Decisions

See [[concepts/Decision_Log]] for full log.

| ID | Decision | Date |
|----|----------|------|
| D001 | FT-Transformer as primary novel algorithm | 2026-10-19 |
| D002 | Hit metric: retrospective labeling + greenlight-time features | 2026-10-19 |
| D003 | IMDb first, TMDb API deferred | 2026-10-19 |
| D004 | Aggressive scope (attempt bonus), drop if time tight | 2026-10-19 |
| D005 | Wiki format: quick-reference cheat sheets with deep-dive links | 2026-10-19 |
| D006 | TMDb API deferred → superseded by D007 | 2026-10-19 |
| D007 | TMDb data: Kaggle alanvourch dataset over API | 2026-10-20 |
| D008 | Actor popularity: weighted formula with billing order | 2026-10-20 |
| D009 | Billing weight: 1/log(ordering+1) over 1/ordering | 2026-10-20 |
| D010 | Min vote threshold: configurable, default 500 | 2026-10-20 |
| D011 | Hit metric: two-mode (Full with ROI, Partial without) | 2026-10-20 |
| D012 | Package manager: UV over requirements.txt | 2026-10-20 |
| D013 | GitHub repo: private at sempaiyael/gcash_assessment | 2026-10-20 |
| D014 | isAdult filter: exclude adult content (stakeholder discussion point) | 2026-10-20 |
| D015 | Technical lead grilling practice: challenge plans before execution | 2026-10-20 |
| D016 | Hit metric binary label: 90th percentile threshold | 2026-10-20 |
| D017 | Temporal split: train ≤2018, test 2019-2023 | 2026-10-20 |
| D018 | Env anchored on pytorch-tabular: pandas<3, torch cu130 explicit index | 2026-10-22 |
| D019 | TabNet dropped (FT-T is the novel slot; LR+XGB are the baselines) | 2026-10-22 |
| D020 | Historical features as-of-year (shift(1)) — no future leakage | 2026-10-22 |
| D021 | Drop 2024+ rows from modeling (strict D017 window, noisy labels) | 2026-10-22 |
| D022 | Internal val: fit ≤2015 / val 2016-2018 (temporal, early stop + threshold) | 2026-10-22 |
| D023 | Imbalance: loss weighting + F1 threshold tuned on val | 2026-10-22 |
| D024 | FT-T: early stop on valid_loss; permutation importance (lib bugs F008/F011) | 2026-10-22 |
| D025 | High precision = two-tier P@K slate + recalibration; no 90% threshold chase | 2026-10-22 |
| D026 | Day 3: slides first, then 60-min TabPFN-2.5 experiment, then recommender | 2026-10-22 |

## Naming Conventions

- Concept pages: Title Case, wiki/concepts/
- Folder-split: wiki/concepts/<topic>/index.md + sub-pages
- Entity pages: Proper names, wiki/entities/
- Summary pages: kebab-case, wiki/summaries/
- Frontmatter required: title, type, created, updated, sources, tags
- Diagrams: mermaid only. Formulas: KaTeX only.

## Open Research Questions

- Optimal feature set for greenlight-time movie prediction?
- FT-Transformer vs XGBoost on movie tabular data?
- Is TabR worth the complexity?
- Best hit movie metric (ratings + votes + ROI)?
- How to handle class imbalance?

## Deferred Items

See [[concepts/Deferred_Items]] for full list.
- ~~TMDb API~~ → Resolved via Kaggle dataset (D007)
- **TabPFN-2.5 experiment — PINNED** (weights gated behind Prior Labs license at ux.priorlabs.ai; experiment script preserved locally outside version control). Revisit after the recommender is done.
- TabR deep-dive (revisit after recommender)
- Box Office Mojo scraping (not needed — model strong without it)
- NLP on plot synopses (low priority)

## Research Gaps

Sources to ingest:
- [x] FT-Transformer paper (Gorishniy et al., 2021) — documented in wiki
- [x] TabNet paper (Arik & Pfister, 2021) — documented in wiki
- [x] TabR paper (Gorishniy et al., 2024) — documented in wiki
- [x] SVD++ paper (Koren, 2008) — documented in wiki
- [x] Movie success prediction (Lash & Zhao, 2016) — documented in wiki
- [ ] IMDb dataset documentation — ingest after download

## Working Conventions

- Language: English
- Tone: Technical but accessible
- Format: Quick-reference cheat sheets; link to deeper references
- Contradictions: State both, cite each, add to Open Questions
- **Always check Deferred Items before new research**
- **Always log failures/learnings — prevents repeating mistakes**