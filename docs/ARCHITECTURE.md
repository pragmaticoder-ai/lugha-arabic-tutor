# Lugha — Architecture

Monorepo, Google-native, deployable as two independent Cloud Run services.

```
 Mobile/Web browser (responsive, RTL-aware)
        │
        ▼
 lugha-web  (Next.js standalone → Cloud Run)   ──calls──►  lugha-api (FastAPI → Cloud Run)
                                                               │
                        ┌──────────────────────────────────────┼───────────────────┐
                        ▼                    ▼                   ▼                   ▼
                 Gemini (Vertex AI)   Cloud Text-to-Speech   Cloud Speech-to-Text   Cloud SQL (Postgres)
                 lessons/grading      Fusha audio            shadow/compare (v2)    learners/progress/
                                                                                    schedule/verified bank
```

## Separation (why two services)
- **lugha-web**: UI only; no secrets. Talks to lugha-api over HTTPS.
- **lugha-api**: the adaptive "brain" + all credentialed calls (Gemini/TTS/STT/DB).
- They scale independently and can be redeployed independently (steering requirement).

## Core loop (SPEC-02→06)
serve i+1 lesson → pushed output → TTS shadow → diagnostic quiz → per-skill branch
(advance/reteach/drop+drill) → update spaced-repetition schedule → next lesson adapts.

## Key rules
- Core fundamentals come from the VERIFIED lesson bank; live Gemini only for practice/variation.
- Keys never reach the client. Don't call the model per keystroke.
- Adaptation uses a rolling signal (last 2–3 quizzes/skill), not one result.

## Learning science embedded (validated — see spec)
comprehensible input (i+1) · pushed output · spaced repetition · shadowing · high-freq-vocab-first.
