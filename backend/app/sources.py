"""Source enforcement (SPEC-02) — no item teaches without a cited source.

Valid source ids are defined ONCE in data/SOURCES.md. An item is only servable
when it carries a `source` that is a known id. verified:true additionally requires
a non-mechanical source (not Unicode alone) for anything that teaches meaning.
"""
from __future__ import annotations

VALID_SOURCES = {
    "SRC-UAE-FRAMEWORK",
    "SRC-UNICODE-JOINING",
    "SRC-MASTERING-ARABIC-1",
    "SRC-TEXTBOOK",
    "SRC-NATIVE-REVIEW",
}

# Sources that only justify mechanical letter SHAPES, never sounds/meaning/sequence.
MECHANICAL_ONLY = {"SRC-UNICODE-JOINING"}


class UnsourcedItemError(ValueError):
    """Raised when an item has no valid source — it must not be taught."""


def require_source(item: dict) -> str:
    """Return the item's source id, or raise if missing/unknown."""
    src = item.get("source")
    if not src:
        raise UnsourcedItemError(
            f"item {item.get('item_id', '?')} has no `source` — refused "
            f"(cite one of {sorted(VALID_SOURCES)}; see data/SOURCES.md)"
        )
    if src not in VALID_SOURCES:
        raise UnsourcedItemError(
            f"item {item.get('item_id', '?')} cites unknown source {src!r} — refused"
        )
    return src


def is_servable(item: dict) -> bool:
    """True only if the item has a valid source. Missing source → never served."""
    try:
        require_source(item)
        return True
    except UnsourcedItemError:
        return False
