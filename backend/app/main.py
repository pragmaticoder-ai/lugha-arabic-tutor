"""Lugha API — the adaptive 'brain'. FastAPI on Cloud Run.

Endpoints are thin; real logic lives in adaptive.py (pure, tested). Gemini/TTS are
called behind this API so keys never reach the client.
"""
from __future__ import annotations

from collections import defaultdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .adaptive import decide_action
from .bank import select_item
from .gemini import compose_lesson
from .models import LessonRequest, QuizSubmission
from .syllabus import build_syllabus

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


@app.get("/syllabus")
def syllabus() -> dict:
    """SPEC-02: the sequenced textbook — letters & numerals FIRST, words last.
    Letter shapes are mechanical (verified); word chapters stay unverified."""
    return build_syllabus()


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
def next_lesson(req: LessonRequest, level: int = 1) -> dict:
    """SPEC-02/06: pick a VERIFIED item from the bank (fundamentals never invented),
    then let Gemini COMPOSE an i+1 example + pushed-output prompt around it.
    No verified item at this level → needs_content (never a fabricated item)."""
    item = select_item(req.skill, level, require_verified=True)
    if item is None:
        return {
            "learner_id": req.learner_id,
            "skill": req.skill,
            "level": level,
            "status": "needs_content",
            "note": "no VERIFIED item at this level — seed/verify the bank (SPEC-02)",
        }
    lesson = compose_lesson(item)
    return {
        "learner_id": req.learner_id,
        "skill": req.skill,
        "level": level,
        "status": "ok",
        "focus": {
            "item_id": item.item_id, "arabic": item.arabic,
            "translit": item.translit, "meaning": item.meaning,
            "source": "verified",
        },
        "example": {
            "arabic": lesson.example_arabic,
            "meaning": lesson.example_meaning,
            "source": lesson.source,  # generated | fallback — never "verified"
        },
        "output_prompt": lesson.output_prompt,
    }
