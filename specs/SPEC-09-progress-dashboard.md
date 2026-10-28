# SPEC-09 — Progress Dashboard

Status: builds on SPEC-04, SPEC-05, SPEC-08. Owner: Venkata · 2026-10-28.

## 1. Requirement
Show each learner an honest picture of their progress — per-skill levels, review
health, streak, and badges — so effort is visible and the next step is obvious.
For a parent, it doubles as a view of each kid's progress.

Panels:
- PER-SKILL bars (L/S/R/W in their skill colors) showing current level + % to next.
- STREAK calendar (gold) — days practised; current + best streak.
- REVIEW health: # items due today, # mastered, # overdue (from SPEC-05).
- BADGES earned (SPEC-08), with the next reachable milestone shown as a target.
- "What's next" line derived from the latest diagnostic (e.g. "Listening needs work").

## 2. Field validations
- learner must exist; dashboard is strictly learner-scoped (no cross-learner leakage).
- percentages 0–100; counts >= 0.
- a skill with no data shows an explicit "not started" state (never a fake 0%-that-looks-like-fail).
- dates rendered in the learner's timezone (consistent with streak logic, SPEC-08).

## 3. Unit tests
- %-to-next computed from current level + mastered-items-at-level; bounded 0–100.
- "not started" state when a skill has zero quiz_results (distinct from 0%).
- overdue count = due_date < today; due-today separate.

## 4. Integration tests
- seed two learners with different histories → each dashboard shows only its own data.
- master a reading item → reading bar advances + a badge appears on the dashboard.
- a skipped day → streak reflects the reset on next load.

## 5. Non-functional requirements
- HONESTY: observations only — never present estimates as guarantees; "not started"
  is distinct from "failed"; no inflated numbers.
- PRIVACY: learner-scoped; a parent view is an explicit mode, not silent cross-access.
- ACCESSIBILITY: color is never the ONLY signal (bars carry labels + %); AA contrast.
- PERFORMANCE: dashboard assembled from indexed aggregate queries; < 400ms.

## 6. Depends on / enables
Depends on: 04, 05, 08. Enables: the learner/parent feedback surface; completes the set.
