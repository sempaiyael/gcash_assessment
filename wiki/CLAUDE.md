# GCash Movie Project Knowledge Base

> Schema document — read at the start of every session together with wiki/index.md.
> Dual purpose: (1) research companion, (2) operational memory for session continuity.

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

## Session Startup Protocol

Every new session MUST:
1. Read this file + wiki/index.md
2. Read Decision Log [[concepts/Decision_Log]]
3. Read Failures and Learnings [[concepts/Failures_and_Learnings]]
4. Read Deferred Items [[concepts/Deferred_Items]]
5. Check log/ for most recent day's activity
6. **Log any decisions, failures, or learnings from the session before ending**

## Team Roles (Subagent Mapping)

| Role | Subagent Type | When to Use |
|------|--------------|-------------|
| Technical Manager | explore | Scope, risk, timeline |
| Lead Engineer | explore | Architecture, code structure, tradeoffs |
| Data Scientist | explore | Feature engineering, model selection, evaluation |
| Research Analyst | explore | Paper reading, algorithm comparison, literature |
| Code Implementer | main agent | Code, data pipeline, slides |

## Current Project State

- **Phase**: Day 1 execution — data loading and EDA
- **Timeline**: 3 days (Day 1 = 2026-10-20)
- **Primary Model**: FT-Transformer (NeurIPS 2021)
- **Baselines**: Logistic Regression, XGBoost, TabNet
- **Bonus Model**: SVD++ recommender
- **Data**: IMDb (5 TSV files downloaded), TMDb via Kaggle (alanvourch dataset, D007)
- **Data quality**: Verified — 1.26M TMDb rows, budget/revenue sparse but sufficient for major releases
- **Presentation**: Executive slides for movie studio management
- **Wiki**: 27 concept pages, 5 entity pages, 2 day logs
- **Next action**: Create notebooks for data loading and EDA

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
- TabR deep-dive (revisit Day 2 evening)
- Box Office Mojo scraping (revisit Day 2 if model weak)
- NLP on plot synopses (low priority)

## Research Gaps

Sources to ingest:
- [x] FT-Transformer paper (Gorishniy et al., 2021) — documented in wiki
- [x] TabNet paper (Arik & Pfister, 2021) — documented in wiki
- [x] TabR paper (Gorishniy et al., 2024) — documented in wiki
- [x] SVD++ paper (Koren, 2008) — documented in wiki
- [x] Movie success prediction (Lash & Zhao, 2016) — documented in wiki
- [ ] IMDb dataset documentation — ingest after download

## Notes for LLM

- Language: English
- Tone: Technical but accessible
- Style: Quick-reference cheat sheets; link to deeper references
- Token budget: Be efficient. Dense info over verbose explanations.
- Contradictions: State both, cite each, add to Open Questions
- **Always check Deferred Items before new research**
- **Always log failures/learnings — prevents repeating mistakes**