"""Lugha API — the adaptive 'brain'. FastAPI on Cloud Run.

Endpoints are thin; real logic lives in adaptive.py (pure, tested). Gemini/TTS are
called behind this API so keys never reach the client.
"""
from __future__ import annotations

from collections import defaultdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .adaptive import decide_action
from .models import LessonRequest, QuizSubmission

app = FastAPI(title="Lugha API", version="0.1.0")

# CORS: the web app (separate Cloud Run service) calls this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: lock to the deployed web-app origin in prod
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/quiz/grade")
def grade_quiz(sub: QuizSubmission) -> dict:
    """Score per skill, return per-skill action (advance/reteach/drop_and_drill)."""
    by_skill: dict[str, list[bool]] = defaultdict(list)
    for a in sub.answers:
        by_skill[a.skill].append(a.correct)
    result = {}
    for skill, corrects in by_skill.items():
        pct = 100.0 * sum(corrects) / len(corrects)
        result[skill] = {"percent": round(pct, 1), "action": decide_action(pct)}
    return {"learner_id": sub.learner_id, "per_skill": result}


@app.post("/lesson/next")
def next_lesson(req: LessonRequest) -> dict:
    """STUB: real impl calls Gemini with learner level + due items (SPEC-06).
    Core fundamentals come from the VERIFIED lesson bank, not live generation."""
    return {
        "learner_id": req.learner_id,
        "skill": req.skill,
        "source": "verified_bank_stub",
        "item": {"arabic": "مَرْحَبًا", "translit": "marhaban", "meaning": "hello"},
        "note": "stub — wire Gemini + verified bank per SPEC-02 / SPEC-06",
    }
