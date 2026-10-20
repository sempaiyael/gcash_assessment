---
title: Quality Standards
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: [project-brief]
tags: [quality, standards, deliverables]
---

# Quality Standards

What "exceptional" looks like to the hiring team. Use this as a quality bar for every deliverable.

## From the Email

The email explicitly states:
- "We encourage **creativity and technical rigor**"
- "Be as **creative** as possible and incorporate other data sets, features, and algorithms"
- "**Motivate** your choice of a novel algorithm and be prepared to discuss its **theoretical underpinnings**"
- "**Convince** the hypothetical management team"

## Quality Bar

### Code
| Standard | Minimum | Exceptional |
|----------|---------|-------------|
| Runs without errors | ✓ | ✓ from fresh clone |
| README with setup instructions | ✓ | ✓ with architecture diagram |
| requirements.txt | ✓ | ✓ with pinned versions |
| Modular structure | ✓ | ✓ with src/ package |
| Comments | Basic | Meaningful docstrings, decision rationale |
| Error handling | None | Handles missing data, edge cases |

### Analysis (EDA)
| Standard | Minimum | Exceptional |
|----------|---------|-------------|
| Answers 4 questions | ✓ | ✓ with additional insights |
| Visualizations | Basic plots | Labeled, styled, presentation-ready |
| Statistical rigor | Means/medians | Confidence intervals, significance tests |
| Business framing | Technical | "What this means for the studio" |

### Model
| Standard | Minimum | Exceptional |
|----------|---------|-------------|
| Novel algorithm implemented | ✓ | ✓ with ablation study |
| Baselines for comparison | ✓ | ✓ with analysis of why model wins |
| Evaluation metrics | AUC-ROC | Multiple metrics + PR curve + calibration |
| Feature importance | ✓ | ✓ with business interpretation |
| Reproducible results | ✓ | ✓ with seed control + documentation |

### Presentation
| Standard | Minimum | Exceptional |
|----------|---------|-------------|
| Covers all required sections | ✓ | ✓ with executive summary |
| Visualizations included | ✓ | ✓ consistent style, labeled axes |
| Business recommendations | ✓ | ✓ with actionable next steps |
| Professional design | Basic slides | Polished, consistent, stakeholder-ready |
| Narrative | Checklist | Compelling story arc |

## Key Differentiators (What Impresses)

1. **Interpretability**: "This movie is predicted to be a hit BECAUSE of director track record + genre timing" — not just accuracy numbers
2. **Business framing**: Every technical decision justified in business terms
3. **Self-awareness**: Acknowledging limitations, discussing what you'd do with more time
4. **Reproducibility**: Someone else can clone your repo and run everything
5. **Polish**: Slides look like they'd present to actual executives

## Anti-Patterns (What Hurts)

- Jupyter notebook dumps as slides
- No business interpretation of results
- Missing README or broken setup instructions
- Code that only works on your machine
- Accuracy numbers without context ("85% accuracy" means nothing without baseline)
- No discussion of limitations or future work

## Related

- [[concepts/Success_Criteria]] — pass vs exceptional
- [[concepts/Submission_Checklist]] — final verification
- [[concepts/Presentation_Strategy]] — how to present