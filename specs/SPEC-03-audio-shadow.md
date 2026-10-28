# SPEC-03 — Audio: TTS + Shadowing

Status: builds on SPEC-02. Owner: Venkata · 2026-10-28.

## 1. Requirement
Let the learner HEAR correct Fusha for any lesson item (Cloud Text-to-Speech) and
practise SHADOWING: play the model audio, record themselves, compare. Shadowing
sessions are short and comprehension-gated (per the 44-study review).

Behavior:
- "Hear it": synthesize Arabic → audio; cache by item (don't re-synthesize).
- "Shadow": play model → record learner (Speech-to-Text transcribes) → show the
  learner their transcript next to the target for SELF-comparison.
- v1 does NOT score pronunciation accuracy (hard problem) — self-assess only.
- Shadowing guidance: cap a session at 10–15 min; only offer shadow on items the
  learner already comprehends (seen in a lesson / >=80% familiar).

## 2. Field validations
- item_id: required, must exist. text to synthesize: non-empty Arabic.
- language/voice: ar-XA Fusha voice; reject non-Arabic voice for Arabic text.
- recorded audio: duration 0.3–30s; reject empty/too-long.
- STT result may be empty (silence) → handled as "didn't catch that", not an error.

## 3. Unit tests
- TTS request builder picks an ar-XA voice for Arabic input.
- audio cache key = (item_id, voice); second request is a cache hit (no new synth).
- recording-duration validator rejects 0s and 31s, accepts 2s.

## 4. Integration tests
- "hear it" on a seeded item returns playable audio; repeat = cached.
- shadow flow: model plays → mock STT transcript returned → UI shows target vs transcript.
- v1 asserts NO numeric pronunciation score is returned (only comparison view).

## 5. Non-functional requirements
- COST: cache TTS audio (per item/voice) in storage; synth once.
- PRIVACY: learner audio (esp. children) processed for transcription only; not
  stored by default; if stored for review, parent opt-in + deletable.
- ACCESSIBILITY: audio always paired with a visible control + the text; never audio-only.
- PERFORMANCE: cached audio served immediately; cold synth < 1.5s.
- HONESTY: UI never implies an accuracy score in v1; "listen and compare" framing.

## 6. Depends on / enables
Depends on: 02. Enables: 04 (listening/speaking quiz items use audio).
