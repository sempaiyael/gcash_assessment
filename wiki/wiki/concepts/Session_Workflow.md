---
title: Session Workflow
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [workflow, sessions, project-management]
---

# Session Workflow

How to run effective sessions for this project.

## Startup Checklist

1. Read CLAUDE.md + wiki/index.md
2. Read Decision Log, Failures, Deferred Items
3. Check log/ for recent activity
4. Assess current phase

## Subagent Usage

| Task | Subagent |
|------|----------|
| Research questions | explore |
| Codebase exploration | explore |
| Literature review | explore |
| Code implementation | main agent |
| Data pipeline | main agent |
| Slide creation | main agent |

## Decision Framework

1. Research alternatives (explore subagent)
2. List pros/cons
3. Consider 3-day timeline
4. Consider interview impact
5. Document in Decision Log
6. Note deferred items

## Time Blocks

- Morning: High-focus (modeling, complex analysis)
- Afternoon: Data work, feature engineering
- Evening: Polish, documentation, planning

## Session Ending Protocol

Before ending a session:
1. Log any decisions made → Decision Log
2. Log any failures/learnings → Failures and Learnings
3. Update Deferred Items if new items deferred
4. Update log/YYYYMMDD.md with session activity
5. Update CLAUDE.md "Current Project State" if phase changed