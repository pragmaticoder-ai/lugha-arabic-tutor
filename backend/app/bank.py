"""Verified lesson bank loader + selection (SPEC-02).

v1 reads the JSON seed; the production path reads the `lesson_items` table.
Selection = lowest freq_rank at the learner's (skill, level) — high-frequency first.
Only verified=true items are servable as fundamentals; if none, return None
(caller emits needs_content, never a fabricated item).
"""
from __future__ import annotations

import json
from pathlib import Path

from .gemini import VerifiedItem

_SEED = Path(__file__).resolve().parents[2] / "data" / "seed" / "year1_bank.json"


def _load_raw() -> list[dict]:
    with _SEED.open(encoding="utf-8") as f:
        return json.load(f)["items"]


def select_item(skill: str, level: int, *, require_verified: bool = True) -> VerifiedItem | None:
    rows = [
        r for r in _load_raw()
        if r["skill"] == skill and r["level"] == level
        and (r.get("verified", False) or not require_verified)
    ]
    if not rows:
        return None
    rows.sort(key=lambda r: r.get("freq_rank", 10**9))
    r = rows[0]
    return VerifiedItem(
        item_id=r["item_id"], skill=r["skill"], level=r["level"],
        arabic=r["arabic"], translit=r["translit"], meaning=r["meaning"],
    )
