---
title: Project Requirements
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [project-brief]
tags: [requirements, deliverables, scope]
---

# Project Requirements

Structured checklist from the original email. Verify completion against this list.

## Goal Clarification

**The exact wording**: "Build a model to predict the next AAA title using the given data plus other data you may think would be predictive."

**Interpretation**: This is NOT about generating a movie title (text generation). It's about **predicting whether a proposed movie will be a hit (AAA title) before it's made**.

**The business scenario**:
1. Studio has a movie proposal: "Sci-fi action film directed by Christopher Nolan, starring Tom Hardy, $200M budget."
2. Director asks: "Will this be a hit? Should we invest?"
3. Model takes greenlight-time features → outputs prediction: "Yes, likely a hit" or "No, risky."

**What we're predicting**:
- Target: Binary hit/not-hit (based on hit metric, 90th percentile threshold — D016)
- Input: Greenlight-time features (what we know BEFORE production)
- Output: Probability of being a hit (0 to 1)

**What we're NOT doing**:
- Generating movie titles (that's NLP/text generation)
- Predicting exact box office revenue (that's regression)
- Recommending what movie to make (that's the recommender system, bonus)

## Required Deliverables

### EDA (4 Questions)
- [ ] Q1: Highest rated movie 2023 + balance ratings vs votes
- [ ] Q2: Most popular actor 2023
- [ ] Q3: User-movie preference trends over years
- [ ] Q4: Define hit movie metric + business justification

### Prediction Model
- [ ] Build model to predict next AAA title
- [ ] Use novel algorithm beyond LR/XGBoost
- [ ] Cite source paper(s) for novel algorithm
- [ ] Be prepared to discuss theoretical underpinnings

### Presentation (Studio Exec)
- [ ] Executive slides for movie studio management
- [ ] Include EDA insights with visualizations
- [ ] Include hit metric definition and justification
- [ ] Include model development and results
- [ ] Include business recommendations

### Code
- [ ] Git repository with clean code
- [ ] README with instructions
- [ ] requirements.txt

## Bonus Deliverables

### Recommender System
- [ ] KNN benchmark model
- [ ] SVD++ advanced model
- [ ] Theoretical discussion with citations
- [ ] Evaluation metric (NDCG@K) + justification
- [ ] Model comparison (benchmark vs advanced)
- [ ] Qualitative assessment

### Second Presentation (Streaming Exec)
- [ ] Slides for movie streaming service management
- [ ] Model development process and results
- [ ] Convince to adopt recommender system

## Submission

- Email slides, code, and files to hiring team

## Related

- [[raw/notes/project-brief]] — original email
- [[concepts/Execution_Plan]] — day-by-day plan
- [[concepts/Hit_Movie_Metric]] — Q4 answer
- [[concepts/FT_Transformer]] — novel algorithm choice
- [[concepts/Recommender_Systems]] — bonus recommender