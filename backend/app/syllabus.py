"""Syllabus loader (SPEC-02) — sequence comes from DATA, not hardcoded.

The chapter order lives in data/seed/chapters.json (cites SRC-UAE-FRAMEWORK).
Each chapter's pages are pulled from its named seed file. Every item MUST carry
a valid `source`; an unsourced item is DROPPED, never taught (see sources.py).
"""
from __future__ import annotations

import json
from pathlib import Path

from .sources import is_servable

_SEED = Path(__file__).resolve().parents[2] / "data" / "seed"


def _load(name: str) -> dict:
    with (_SEED / name).open(encoding="utf-8") as f:
        return json.load(f)


def _alphabet_pages() -> list[dict]:
    pages = []
    for l in _load("alphabet.json")["letters"]:
        if not is_servable(l):  # must cite a source
            continue
        pages.append({
            "id": f"ltr_{l['order']}", "arabic": l["isolated"],
            "translit": l["name"], "sound": l["sound"],
            "forms": {"isolated": l["isolated"], "initial": l["initial"],
                      "medial": l["medial"], "final": l["final"]},
            "joins_left": l["joins_left"], "verified": True,
            "source": l["source"],
        })
    return pages


def _seed_pages(seed_file: str, stage_filter: str | None) -> list[dict]:
    pages = []
    for it in _load(seed_file)["items"]:
        if it["item_id"].startswith("_"):
            continue
        if stage_filter and not it.get("stage", "").startswith(stage_filter):
            continue
        if not is_servable(it):  # refuse unsourced
            continue
        pages.append({
            "id": it["item_id"], "arabic": it["arabic"],
            "translit": it["translit"], "sound": it["meaning"],
            "verified": it.get("verified", False), "source": it["source"],
        })
    return pages


def build_syllabus() -> dict:
    """Read chapters.json, fill each chapter's pages from its seed, drop unsourced."""
    spec = _load("chapters.json")
    chapters = []
    for ch in spec["chapters"]:
        if ch["from_seed"] == "alphabet.json":
            pages = _alphabet_pages()
        else:
            pages = _seed_pages(ch["from_seed"], ch.get("stage_filter"))
        chapters.append({
            "num": ch["num"], "title": ch["title"], "stage": ch["stage"],
            "source": ch["source"], "pages": pages,
        })
    return {"framework_source": spec["framework_source"], "chapters": chapters}
