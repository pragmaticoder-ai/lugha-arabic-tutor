# SPEC-08 — Gamification

Status: builds on SPEC-04, SPEC-05, SPEC-06. Owner: Venkata · 2026-10-28.

## 1. Requirement
A motivation layer that rewards GENUINE learning events, not empty taps. Surfaces:
- STREAKS: consecutive days with >=1 completed lesson (makes "daily > cramming" visible).
- XP/STARS: per completed lesson + quiz; bonus on mastery (SPEC-04 action=advance).
- BADGES: tied to REAL milestones — framework indicators (Alphabet complete,
  Numbers 1–10, First 100 words), streak milestones (7-day), skill mastery
  (Mastered Listening L1).
- LEVEL-UP: celebratory (brief, reduced-motion-safe) when a skill advances (i+1 up).
- FAMILY LEADERBOARD: gentle, family-only, encouraging (never harsh ranking).

Hard rule: a reward fires ONLY on a verified learning event (mastery, completion,
streak day, framework milestone). No reward for opening the app, tapping, or guessing.

## 2. Field validations
- badge_key: known enum; awarding an unknown key → rejected.
- a badge is awarded at most once per (learner_id, badge_key) — idempotent.
- streak increments at most once per calendar day per learner (timezone = learner's).
- XP delta >= 0; mastery bonus only when SPEC-04 action == "advance".

## 3. Unit tests
- streak: two completions same day → +1 day only; a skipped day resets to 1.
- badge idempotency: awarding the same badge twice stores one row.
- mastery bonus applies only on action=="advance", not on reteach/drop_and_drill.
- milestone badge "numbers_1_10" fires only when all those items are mastered.

## 4. Integration tests
- complete lesson → XP up, streak updated; quiz mastery → bonus XP + level-up event.
- earning "7-day streak" badge writes exactly one badge row; re-trigger is a no-op.
- kid learner: a correction is paired with a surfaced win (encouragement requirement).

## 5. Non-functional requirements
- INTEGRITY: rewards attach to real learning events only (no slot-machine dark patterns).
- CHILD WELLBEING: encouragement-first for is_child; no punishing/harsh framing; the
  family leaderboard is opt-in and gentle.
- ACCESSIBILITY: animations brief, stoppable, respect prefers-reduced-motion.
- DETERMINISM: award rules are pure functions over learning events (unit-tested).

## 6. Depends on / enables
Depends on: 04 (mastery events), 05 (streak/review events), 06 (loop events).
Enables: 09 (dashboard shows badges/streaks/XP).
