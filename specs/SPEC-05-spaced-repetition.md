# SPEC-05 — Spaced-Repetition Scheduler

Status: builds on SPEC-00, SPEC-04. Owner: Venkata · 2026-10-28.
Implemented core: backend/app/adaptive.py (next_interval_days, SRS_STEPS).

## 1. Requirement
Schedule each learned item for review timed to memory decay, so review beats
cramming. Quiz/lesson outcomes feed the schedule: a correct review expands the
interval; a miss resets it. "Due" items are surfaced first in the next lesson.

Model (v1, simple expanding steps, days): [1, 3, 7, 21, 60].
- correct → advance one step (cap at last).
- miss → reset to step 0 (interval 1 day).
- due_date = today + interval.

## 2. Field validations
- srs_step: int 0..len(steps)-1. correct: bool. due_date: valid date >= today on write.
- item must exist in the learner's progress (or be inserted at step 0 on first learn).
- a review cannot set a due_date in the past.

## 3. Unit tests (present + passing)
- next_interval_days(0, correct=True) → (3, 1).
- then (idx=1, correct=False) → (1, 0)  [reset on miss].
- correct at last step stays at last step (no index overflow).

## 4. Integration tests
- learn item → progress row at step 0, due today.
- answer correct in quiz → due_date pushed to +3d, step 1.
- miss → due_date back to +1d, step 0.
- "due items" query returns only rows with due_date <= today for that learner.

## 5. Non-functional requirements
- CORRECTNESS: scheduling is pure + deterministic (unit-tested), no model in the path.
- PERFORMANCE: "due items" is an indexed query on (learner_id, due_date).
- DATA INTEGRITY: one progress row per (learner_id, item_id) — upsert, never duplicate.
- TUNABILITY: steps are a documented constant; can later swap for FSRS without API change.

## 6. Depends on / enables
Depends on: 00, 04. Enables: 06 (next lesson pulls due items first), 09 (streak/retention stats).
