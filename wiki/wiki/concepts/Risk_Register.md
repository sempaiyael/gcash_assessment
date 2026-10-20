---
title: Risk Register
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [risks, mitigation, contingency]
---

# Risk Register

Known risks with mitigation strategies. Review at session start to anticipate problems.

## Critical Risks

### R1: Time Overrun (Likelihood: HIGH, Impact: HIGH)
- **Risk**: 3 days isn't enough for full scope
- **Mitigation**: 
  - Aggressive prioritization (required before bonus)
  - Fallback plan: cut recommender (D004)
  - Time-box each phase (don't perfect, ship)
- **Trigger**: Day 2 evening, if FT-Transformer not working
- **Action**: Cut bonus, polish required portion

### R2: FT-Transformer Doesn't Outperform Baselines (Likelihood: MEDIUM, Impact: MEDIUM)
- **Risk**: XGBoost beats FT-Transformer on this dataset
- **Mitigation**:
  - Frame as "competitive performance with interpretability advantage"
  - Show attention masks as added value
  - Small dataset may favor simpler models — acknowledge this
- **Action**: Present honest comparison, emphasize interpretability story

### R3: GPU Memory Issues (Likelihood: MEDIUM, Impact: LOW)
- **Risk**: RTX 3060 6GB VRAM insufficient for large batch sizes
- **Mitigation**:
  - Use smaller batch sizes (32-128)
  - Use gradient accumulation if needed
  - Fall back to CPU training for small datasets
- **Action**: Reduce batch size, increase gradient accumulation

## Data Risks

### R4: IMDb Data Format Surprise (Likelihood: LOW, Impact: MEDIUM)
- **Risk**: TSV files have unexpected format, encoding issues, or missing fields
- **Mitigation**:
  - Read dataset documentation first
  - Handle `\N` nulls explicitly (F001 knowledge)
  - Validate schema after loading
- **Action**: Inspect first 100 rows before processing

### R5: Data Quality Issues (Likelihood: MEDIUM, Impact: MEDIUM)
- **Risk**: Missing values, inconsistent formats, duplicate entries
- **Mitigation**:
  - Comprehensive data cleaning pipeline
  - Document cleaning decisions
  - Keep raw data immutable
- **Action**: Log all cleaning steps, report data loss statistics

### R6: MovieLens ID Mapping Failure (Likelihood: LOW, Impact: LOW)
- **Risk**: links.csv doesn't map all MovieLens IDs to IMDb
- **Mitigation**:
  - Check mapping coverage before recommender work
  - Fall back to MovieLens-only IDs if needed
- **Action**: Verify mapping coverage in Day 1

## Technical Risks

### R7: Library Compatibility on Windows (Likelihood: MEDIUM, Impact: LOW)
- **Risk**: pytorch-tabular or surprise has Windows-specific issues
- **Mitigation**:
  - Test library installation early
  - Have alternative implementations ready
  - Use conda if pip fails
- **Action**: Install and test all libraries in Day 1 morning

### R8: Long Training Times (Likelihood: LOW, Impact: MEDIUM)
- **Risk**: FT-Transformer training takes too long for iteration
- **Mitigation**:
  - Start with small subset for debugging
  - Use early stopping
  - Reduce model size if needed
- **Action**: Profile training time on first run

## Presentation Risks

### R9: Slides Not Professional Enough (Likelihood: MEDIUM, Impact: MEDIUM)
- **Risk**: Slides look like technical dumps, not executive presentations
- **Mitigation**:
  - Use consistent template from start
  - Limit text per slide, use visuals
  - Have someone review before submission
- **Action**: Create slide template in Day 1 evening

### R10: Missing Business Narrative (Likelihood: MEDIUM, Impact: HIGH)
- **Risk**: Technical results without business interpretation
- **Mitigation**:
  - Frame every finding as "what this means for the studio"
  - Include business recommendations section
  - Use [[concepts/Interview_Narrative]] talking points
- **Action**: Write business interpretation for each major finding

## Mitigation Priority

1. R1 (time) — most likely, most impactful
2. R10 (narrative) — high impact on evaluation
3. R2 (model performance) — medium risk, manageable with framing
4. R7 (Windows) — test early, low impact if caught

## Related

- [[concepts/Execution_Plan]] — timeline that R1 threatens
- [[concepts/Failures_and_Learnings]] — log actual failures here
- [[concepts/Quality_Standards]] — what we're protecting