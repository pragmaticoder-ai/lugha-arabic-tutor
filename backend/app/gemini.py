"""Gemini (Vertex AI) integration — SPEC-02/06.

HARD RULE: Gemini never invents a fundamental item or its diacritics. It only
COMPOSES practice text (an i+1 example sentence + a pushed-output prompt) AROUND a
verified bank item passed in. The focus item always comes from the verified bank.

Keys/credentials are server-side (ADC / Cloud Run service account). This module is
import-safe without credentials: if Vertex is unavailable it falls back to a
deterministic local composer so the app and tests still run (source flagged).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass


@dataclass
class VerifiedItem:
    item_id: str
    skill: str
    level: int
    arabic: str
    translit: str
    meaning: str


@dataclass
class ComposedLesson:
    focus: VerifiedItem
    example_arabic: str
    example_meaning: str
    output_prompt: str
    source: str  # "generated" (Gemini) or "fallback" (local, offline)


_PROMPT = """You are an Arabic (Modern Standard Arabic / Fusha) tutor.
You are given ONE verified vocabulary item. Do NOT change its Arabic spelling or
diacritics. Produce STRICT JSON with keys:
  example_arabic  : one short i+1 sentence (<=8 words) USING the item, correct harakat
  example_meaning : English meaning of that sentence
  output_prompt   : a question (English) that makes the learner PRODUCE Arabic using the item
Item: {item}
Return ONLY the JSON object."""


def _fallback(item: VerifiedItem) -> ComposedLesson:
    return ComposedLesson(
        focus=item,
        example_arabic=item.arabic,
        example_meaning=item.meaning,
        output_prompt=f"Use '{item.translit}' ({item.meaning}) in a short Arabic phrase.",
        source="fallback",
    )


def compose_lesson(item: VerifiedItem) -> ComposedLesson:
    """Compose practice around a VERIFIED item. Falls back offline/without creds."""
    if os.getenv("LUGHA_DISABLE_GEMINI") == "1":
        return _fallback(item)
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel

        vertexai.init(
            project=os.environ["GOOGLE_CLOUD_PROJECT"],
            location=os.getenv("VERTEX_AI_LOCATION", "us-central1"),
        )
        model = GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
        payload = {
            "item_id": item.item_id, "arabic": item.arabic,
            "translit": item.translit, "meaning": item.meaning,
        }
        resp = model.generate_content(_PROMPT.format(item=json.dumps(payload, ensure_ascii=False)))
        data = json.loads(_extract_json(resp.text))
        return ComposedLesson(
            focus=item,
            example_arabic=str(data["example_arabic"]),
            example_meaning=str(data["example_meaning"]),
            output_prompt=str(data["output_prompt"]),
            source="generated",
        )
    except Exception:
        # Any failure (no creds, bad JSON, network) → safe deterministic fallback.
        return _fallback(item)


def _extract_json(text: str) -> str:
    """Pull the first {...} block from a model reply."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON object in model reply")
    return text[start : end + 1]
