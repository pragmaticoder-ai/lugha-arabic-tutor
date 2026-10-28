# SPEC-07 — Library / Read-as-a-Book

Status: builds on SPEC-02. Owner: Venkata · 2026-10-28.

## 1. Requirement
A calm, no-quiz reading space for immersion (comprehensible input without pressure).
Chapters are shown as a shelf of covers; opening one gives a paged reader (swipe
pages) of Fusha text. Tapping a word reveals meaning + audio (reuses SPEC-03 TTS).
Read-only: the Library never grades, never changes level, never schedules — it is
pure input. It MAY quietly mark words the learner tapped as "seen" (soft signal),
but does not affect quiz-driven progression.

Behavior:
- List chapters (from the verified bank, grouped by theme/level).
- Open chapter → paged reader; RTL text, large Naskh, translit toggle, meaning on tap.
- Tap word → popover: Arabic + translit + meaning + play audio.
- Reading level filter (show chapters at/below the learner's reading level + 1).

## 2. Field validations
- chapter_id: required, must exist.
- content served is source="verified" only (no live-generated text in the reader —
  immersion content must be correct; generation stays in lessons/practice).
- tap target word must map to a known lexicon entry → else no popover (no fabricated meaning).
- translit toggle: boolean; default on for child learners, off allowed for adults.

## 3. Unit tests
- chapter list filters to reading_level <= learner_level + 1.
- a word with no lexicon entry yields no popover (never a guessed meaning).
- reader is read-only: no progress/level/schedule write occurs on open or page turn.

## 4. Integration tests
- open a seeded chapter → pages render RTL; tap a known word → meaning+audio returned.
- reading a chapter does NOT change SkillLevel or create quiz_results (isolation from the loop).
- audio tap reuses the SPEC-03 cache (no duplicate synthesis).

## 5. Non-functional requirements
- ACCURACY: verified content only — a reader full of subtly-wrong diacritics teaches
  errors; especially unacceptable for children.
- CALM UX: no streaks/XP/quiz prompts inside the reader (immersion, not pressure).
- ACCESSIBILITY: large scalable Arabic, diacritics never clipped, swipe + button paging,
  audio has a visible control.
- PERFORMANCE: paging is instant (content prefetched per chapter).

## 6. Depends on / enables
Depends on: 02 (verified content), 03 (audio). Enables: richer comprehensible-input
hours that complement the lesson loop. Does NOT feed the adaptive loop (by design).
