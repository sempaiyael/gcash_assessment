---
title: Submission Checklist
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [submission, checklist, verification]
---

# Submission Checklist

Final verification before emailing the hiring team. Run through this completely.

## Code Repository

- [ ] README.md exists with:
  - Project overview
  - Setup instructions (pip install, data download)
  - How to run each notebook
  - Key findings summary
- [ ] requirements.txt with all dependencies
- [ ] .gitignore excludes data files, __pycache__, .ipynb_checkpoints
- [ ] No secrets, API keys, or personal data in repo
- [ ] Code runs from fresh clone (test this!)
- [ ] Notebooks run in order (01 → 02 → 03 → 04 → 05)
- [ ] No broken imports or missing modules

## Data

- [ ] Data download instructions in README
- [ ] No large data files committed to git
- [ ] Data loading handles `\N` nulls
- [ ] Data cleaning steps documented

## Analysis & Model

- [ ] All 4 EDA questions answered with visualizations
- [ ] Hit movie metric defined and justified
- [ ] FT-Transformer implemented and trained
- [ ] Baselines (LR, XGBoost, TabNet) for comparison
- [ ] Evaluation metrics computed (AUC-ROC, F1, etc.)
- [ ] Feature importance analysis included
- [ ] Source papers cited (FT-Transformer, TabNet)

## Slides

- [ ] Presentation 1 (Studio Exec) complete:
  - Executive summary
  - EDA insights with visualizations
  - Hit metric definition
  - Model development and results
  - Business recommendations
- [ ] All images embedded (no broken links)
- [ ] Consistent design/template
- [ ] No placeholder text
- [ ] Slides are self-contained (understandable without code)

## Bonus (If Completed)

- [ ] Recommender system implemented (KNN + SVD++)
- [ ] Evaluation with NDCG@K
- [ ] Qualitative assessment
- [ ] Presentation 2 (Streaming Exec) complete
- [ ] Theoretical discussion with citations

## Final Steps

- [ ] Run all notebooks from scratch (restart kernel + run all)
- [ ] Check all visualizations render correctly
- [ ] Verify Git repo is clean (no uncommitted changes)
- [ ] Prepare submission email
- [ ] Attach slides, code repo link, and any additional files
- [ ] Double-check hiring team email addresses

## Email Template

Subject: GCash Data Science Exam — [Your Name]

Body:
> Hi,
> 
> Please find attached my completed exam for the "Give Me The Next AAA Title" project.
> 
> Deliverables:
> - Presentation slides (attached)
> - Code repository (link)
> - [If bonus: Recommender system presentation (attached)]
> 
> I'm available to discuss my approach and findings at your convenience.
> 
> Best regards,
> [Your name]

## Related

- [[concepts/Quality_Standards]] — what good looks like
- [[concepts/Success_Criteria]] — pass vs exceptional
- [[concepts/Project_Requirements]] — what's required