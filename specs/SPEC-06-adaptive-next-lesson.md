# SPEC-06 — Adaptive Next-Lesson Generation (loop closes)

Status: builds on SPEC-04, SPEC-05. Owner: Venkata · 2026-10-28.

## 1. Requirement
Generate the learner's NEXT lesson FROM their latest diagnostic + due items — this
closes the adaptive loop. Inputs: per-skill action (SPEC-04), due items (SPEC-05),
current level (SPEC-02). Output: a lesson that (a) front-loads due review items,
(b) re-teaches weak items when action=reteach/drop_and_drill, (c) introduces one
new i+1 item when action=advance, (d) balances the 4 skills over time.

Source rule (same as SPEC-02): new fundamentals from the VERIFIED bank; Gemini only
composes practice/examples/explanations around verified items. Gemini NEVER invents
the authoritative new item or its diacritics.

Loop: lesson → output → shadow → quiz → branch → schedule → THIS spec → next lesson.

## 2. Field validations
- requires a prior quiz result for the skill (else: serve an intro lesson, don't guess).
- action ∈ {advance, reteach, drop_and_drill}. due items list may be empty.
- generated wrapper text tagged source="generated"; the focus item must be source="verified".
- never advance a skill's level on a single quiz — require the rolling signal (SPEC-04).

## 3. Unit tests
- action=advance + no due → lesson has 1 new verified i+1 item.
- action=drop_and_drill → lesson contains the specific missed items, no new item.
- due items present → they appear before any new item.
- next level never exceeds current+1.

## 4. Integration tests
- full loop: deliver lesson → grade quiz (reading mastered, listening weak) →
  next reading lesson advances a level; next listening lesson re-drills missed items.
- two learners diverge: same start, different quiz results → different next lessons
  (proves per-learner adaptivity).
- generated example labeled generated; focus item verified.

## 5. Non-functional requirements
- ACCURACY/SAFETY: verified focus items only; Gemini output reviewed before it can
  become a verified bank item (no silent promotion).
- COST: reuse verified items + cached generations; a model call only when composing
  genuinely new practice, not on every lesson.
- DETERMINISM: the DECISION (what to teach next) is driven by pure SPEC-04/05 logic;
  Gemini only renders the chosen plan into learner-facing text.
- TRANSPARENCY: lesson states why ("reviewing 3 due items; re-teaching numbers").

## 6. Depends on / enables
Depends on: 04, 05 (and 02 for content). Enables: the complete learning loop; 08/09 read its events.
