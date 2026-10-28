# SPEC-02 — Curriculum & Lesson Delivery

Status: builds on SPEC-00, SPEC-01. Owner: Venkata · 2026-10-28.

## 1. Requirement
Serve the active learner a lesson at their current level for a chosen skill,
following the UAE "Arabic as an Additional Language" framework (Fusha, 4 skills,
leveled). A lesson presents: one focus item (Arabic + transliteration + meaning),
a comprehensible-input (i+1) example sentence using it, and a pushed-output prompt
that makes the learner PRODUCE Arabic.

Source rule (critical):
- FUNDAMENTALS come from the VERIFIED lesson bank (verified=true). Live Gemini
  generation is allowed ONLY for practice/variation/examples, never as the sole
  source of a core first-teach item.
- Ordering favours HIGH-FREQUENCY items first (freq_rank).
- Level selection = learner's SkillLevel for that skill (i = current; serve i+1).

## 2. Field validations
- skill: one of the 4 skills → else 422.
- learner must exist (SPEC-01) → else 404.
- Returned item: arabic/translit/meaning all non-empty; arabic carries harakat.
- If no verified item exists at the level → return explicit empty state
  (needs_content), never a fabricated/unverified item for a fundamental.
- Gemini-generated practice text flagged source="generated" (never source="verified").

## 3. Unit tests
- level selector returns next-unmastered item by (skill, level, freq_rank).
- a generated example is tagged source="generated"; a bank item source="verified".
- empty bank at level → needs_content (no fabricated item).

## 4. Integration tests
- seed bank with 3 verified reading items L1 → lesson returns the lowest freq_rank first.
- learner at reading L2 is not served an L1 item as "new".
- generated example sentence passes through but is labeled generated.

## 5. Non-functional requirements
- ACCURACY: fundamentals verified by a human (diacritics/grammar) before verified=true.
- SECURITY: Gemini called server-side only; prompt + output logged for review.
- PERFORMANCE: lesson fetch < 300ms for bank items; generated content cached to the
  bank after review rather than re-generated each call (cost + consistency).
- COST: no model call when a suitable verified item exists.
- ACCESSIBILITY: Arabic >=1.4x body; always show translit + meaning.

## 6. Depends on / enables
Depends on: 00, 01. Enables: 03 (audio of the item), 04 (quiz on delivered items),
07 (library reuses verified content).
