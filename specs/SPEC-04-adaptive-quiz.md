# SPEC-04 — Adaptive Quiz Engine

Status: builds on SPEC-02, SPEC-03. Owner: Venkata · 2026-10-28.
Implemented core: backend/app/adaptive.py (decide_action, rolling_action), main.py /quiz/grade.

## 1. Requirement
After a chapter/lesson set, run a DIAGNOSTIC quiz — the sensor that drives
adaptation. Each question is tagged by SKILL (L/S/R/W), ITEM, and TYPE
(recognition vs production). Grade per skill; emit a per-skill ACTION:
- MASTERED (>=85%) → advance level (i+1 up)
- PARTIAL (60–85%) → re-teach weak items, mix into next lesson
- WEAK (<60%) → drop difficulty, re-teach weak items; schedule sooner (SPEC-05)
Use a ROLLING signal (last up-to-3 quizzes per skill) before changing a level, so
one bad quiz doesn't over-correct.

## 2. Field validations
- answers: 1–50 items; each has item_id (<=64), skill (one of 4), is_recognition
  (bool), correct (bool). → else 422.
- computed percent per skill bounded 0–100.
- learner_id required + must exist.
- production (spoken) items: graded by self-assessment/typed check, NOT auto-scored
  for pronunciation (ties to SPEC-03 v1).

## 3. Unit tests (present + passing)
- decide_action: 90→advance, 85→advance, 70→reteach, 60→reteach, 40→drop_and_drill.
- decide_action rejects <0 / >100.
- rolling_action([90,88,40]) not "drop_and_drill" (smoothing).

## 4. Integration tests (present + passing)
- /quiz/grade: reading all-correct → action "advance"; listening all-wrong → "drop_and_drill".
- bad skill ("cooking") → 422.
- result feeds SPEC-05 (misses scheduled sooner) and SPEC-06 (next lesson reads scores).

## 5. Non-functional requirements
- DETERMINISM: grading/branch logic is pure + unit-tested (no model in the decision path).
- FAIRNESS: thresholds (85/60) tunable + documented; rolling window prevents yo-yo.
- TRANSPARENCY: quiz returns a per-skill diagnostic ("strong reading, weak listening"),
  not just a single score.
- ENCOURAGEMENT (kids): surface wins alongside corrections (handoff to SPEC-08).
- PERFORMANCE: grading O(n answers), < 50ms.

## 6. Depends on / enables
Depends on: 02, 03. Enables: 05 (scheduling from results), 06 (next lesson from results),
08 (badges/XP on mastery), 09 (progress charts).
