"""Syllabus loader (SPEC-02) — builds the SEQUENCED textbook structure.

A language starts with letters + numerals, not words. This assembles chapters
in the correct order from the seed files:
  Ch 1 Alphabet (28 letters, 4 forms) -> Ch 2 Harakat -> Ch 3 Numerals
  -> Ch 4 Decoding -> Ch 5 First words.
Letter SHAPES are mechanical (Unicode joining) so verified=true; harakat on
words still need human review, so word chapters stay verified=false.
"""
from __future__ import annotations

import json
from pathlib import Path

_SEED = Path(__file__).resolve().parents[2] / "data" / "seed"


def _load(name: str) -> dict:
    with (_SEED / name).open(encoding="utf-8") as f:
        return json.load(f)


def build_syllabus() -> dict:
    alphabet = _load("alphabet.json")["letters"]
    foundation = _load("stage0_foundation.json")["items"]

    # Chapter 1 — the alphabet, one page per letter, forms + sound.
    ch1_pages = [
        {
            "id": f"ltr_{l['order']}",
            "arabic": l["isolated"],
            "translit": l["name"],
            "sound": l["sound"],
            "forms": {
                "isolated": l["isolated"], "initial": l["initial"],
                "medial": l["medial"], "final": l["final"],
            },
            "joins_left": l["joins_left"],
            "verified": True,  # shapes are mechanical
        }
        for l in alphabet
    ]

    # Chapters 2+ from the staged foundation seed, grouped by stage.
    def pages_for(stage_prefix: str) -> list[dict]:
        return [
            {
                "id": it["item_id"], "arabic": it["arabic"],
                "translit": it["translit"], "sound": it["meaning"],
                "verified": it.get("verified", False),
            }
            for it in foundation
            if it.get("stage", "").startswith(stage_prefix)
            and not it["item_id"].startswith("_")
        ]

    return {
        "chapters": [
            {"num": 1, "title": "The Alphabet", "stage": "Stage 0 · Foundation", "pages": ch1_pages},
            {"num": 2, "title": "Short Vowels (Harakat)", "stage": "Stage 0 · Foundation", "pages": pages_for("0-harakat")},
            {"num": 3, "title": "Numerals", "stage": "Stage 0 · Foundation", "pages": pages_for("0-numerals")},
            {"num": 4, "title": "Decoding Syllables", "stage": "Stage 1 · Reading", "pages": pages_for("1-decoding")},
        ]
    }
