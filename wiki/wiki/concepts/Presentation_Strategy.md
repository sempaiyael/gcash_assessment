---
title: Presentation Strategy
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [presentation, strategy, audience]
---

# Presentation Strategy

Two presentations for two different audiences. Each needs distinct framing.

## Presentation 1: Movie Studio Executives (Required)

**Audience**: Studio director + data scientists
**Goal**: Convince them to invest in next AAA title
**Tone**: Investment-focused, risk/reward framing

### Structure
1. **Executive Summary** — Key findings and recommendation
2. **EDA Insights** — 4 questions answered with visualizations
3. **Hit Movie Metric** — Definition, justification, business framing
4. **Prediction Model** — FT-Transformer, feature importance, accuracy
5. **Business Recommendations** — What to invest in, what to avoid

### Key Messages
- "Here's what drives movie success" (feature importance)
- "Here's how to predict it before production" (greenlight features)
- "Here's the ROI story" (hit metric = investment score)

### Visualizations
- Genre trends over decades
- Top actors/directors by hit rate
- Feature importance charts
- Model performance curves

## Presentation 2: Streaming Service Executives (Bonus)

**Audience**: Streaming execs + data scientists
**Goal**: Convince them to adopt recommender system
**Tone**: User experience, engagement, retention

### Structure
1. **Executive Summary** — Why a recommender system matters
2. **Model Development** — KNN baseline → SVD++ upgrade
3. **Evaluation Results** — RMSE, NDCG@K comparison
4. **Qualitative Assessment** — Sample recommendations
5. **Business Impact** — Engagement, retention, revenue

### Key Messages
- "Users who get better recommendations watch more" (engagement)
- "Our model outperforms the baseline on ranking quality" (NDCG@K)
- "These recommendations make sense" (qualitative examples)

### Visualizations
- Rating distribution
- Model comparison charts
- Sample recommendation lists
- NDCG@K comparison

## Common Elements

Both presentations should include:
- Clean, professional slides (not Jupyter dumps)
- Clear data visualizations
- Model comparison tables
- Business recommendations
- "Future work" section (what we'd do with more time)

## Narrative Arc

Both presentations follow the same story structure:

1. **Problem** — "We need to decide how to make the next AAA title" / "We need to keep users engaged"
2. **Analysis** — "Here's what the data tells us" (EDA insights)
3. **Insight** — "Here's the pattern we found" (hit metric, feature importance)
4. **Solution** — "Here's the model we built" (FT-Transformer / SVD++)
5. **Recommendation** — "Here's what you should do" (business actions)

This arc turns a technical report into a compelling argument. Every slide should advance the story.

## Slide Tools

Options:
- PowerPoint (standard, professional)
- Google Slides (collaborative)
- Marp (Markdown → slides, good for code-heavy content)

## Related

- [[concepts/Interview_Narrative]] — talking points
- [[concepts/Project_Requirements]] — what's required
- [[concepts/Recommender_Systems]] — bonus content