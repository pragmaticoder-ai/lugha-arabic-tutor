"""Tests for source enforcement (SPEC-02): no source → not taught."""
import pytest
from app.sources import is_servable, require_source, UnsourcedItemError


def test_item_without_source_is_refused():
    assert is_servable({"item_id": "x"}) is False
    with pytest.raises(UnsourcedItemError):
        require_source({"item_id": "x"})


def test_item_with_unknown_source_is_refused():
    assert is_servable({"item_id": "x", "source": "made-up"}) is False
    with pytest.raises(UnsourcedItemError):
        require_source({"item_id": "x", "source": "made-up"})


def test_item_with_valid_source_is_servable():
    assert is_servable({"item_id": "x", "source": "SRC-UAE-FRAMEWORK"}) is True
    assert require_source({"item_id": "x", "source": "SRC-UNICODE-JOINING"}) == "SRC-UNICODE-JOINING"


def test_syllabus_only_contains_sourced_pages():
    from app.syllabus import build_syllabus
    for ch in build_syllabus()["chapters"]:
        for p in ch["pages"]:
            assert p["source"], f"{p['id']} served without a source"


def test_syllabus_sequence_from_data_file():
    # order comes from chapters.json, alphabet still first
    from app.syllabus import build_syllabus
    titles = [c["title"] for c in build_syllabus()["chapters"]]
    assert titles[0] == "The Alphabet"
