---
title: User Context
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [context, skills, constraints]
---

# User Context

Background, skills, and constraints for the project owner. Use this to calibrate advice depth and implementation choices.

## Skills

| Area | Level | Notes |
|------|-------|-------|
| Python data stack (pandas, sklearn) | Comfortable | Can work independently |
| PyTorch | Experience | Can implement models, read docs |
| Deep learning | Moderate | Has used PyTorch, understands architectures |
| Recommendation systems | None | Zero experience, needs guidance |
| Presentation / storytelling | Experienced | Used to presenting to stakeholders |
| Reading academic papers | Comfortable | 2 years R&D experience |
| Recreating papers from scratch | Limited | Can read and explain, but not reproduce from scratch |

## Hardware

- **GPU**: NVIDIA RTX 3060 (mobile/laptop)
- **VRAM**: 6GB (sufficient for FT-Transformer, may need batch size tuning)
- **Platform**: Windows 11

## Timeline

- **Total**: 3 days
- **Day 1**: 2026-10-19 (today)
- **Deadline**: 2026-10-21

## Constraints

- **Token budget**: Be efficient with LLM usage. Dense info over verbose explanations.
- **Time**: Aggressive scope, need to prioritize high-impact work
- **Recommender**: No experience — rely on surprise library documentation and wiki

## Preferences

- Quick-reference cheat sheets with links to deeper references
- Polished executive slides (not Jupyter-style dumps)
- Aggressive scope: attempt bonus, cut if time tight
- ID format for decisions (D001, D002...) for easy reference

## Calibration Guidelines

When advising:
- Don't over-explain Python basics
- Do explain DL architecture details (user can follow)
- Do provide implementation snippets (saves time)
- Don't assume recommender knowledge (explain concepts)
- Do reference papers by name (user can read them)
- Do flag when something is risky or time-consuming

## Related

- [[concepts/Execution_Plan]] — timeline calibrated to these skills
- [[concepts/Decision_Log]] — decisions made with these constraints in mind