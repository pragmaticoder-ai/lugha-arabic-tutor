"""Tests for the sequenced syllabus (SPEC-02)."""
from app.syllabus import build_syllabus


def test_chapter_one_has_all_28_letters_in_order():
    syl = build_syllabus()
    ch1 = syl["chapters"][0]
    assert ch1["num"] == 1 and ch1["title"] == "The Alphabet"
    assert len(ch1["pages"]) == 28
    # alif first, yaa last
    assert ch1["pages"][0]["translit"] == "alif"
    assert ch1["pages"][27]["translit"] == "yaa"


def test_every_letter_has_four_forms():
    ch1 = build_syllabus()["chapters"][0]
    for p in ch1["pages"]:
        assert set(p["forms"]) == {"isolated", "initial", "medial", "final"}
        assert all(p["forms"].values())


def test_non_joining_letters_flagged():
    ch1 = build_syllabus()["chapters"][0]
    by_name = {p["translit"]: p for p in ch1["pages"]}
    # alif, daal, raa, waaw do not join to the left
    assert by_name["alif"]["joins_left"] is False
    assert by_name["raa"]["joins_left"] is False
    assert by_name["baa"]["joins_left"] is True


def test_sequence_letters_before_words():
    chapters = build_syllabus()["chapters"]
    titles = [c["title"] for c in chapters]
    assert titles.index("The Alphabet") < titles.index("Decoding Syllables")


def test_letters_verified_shapes_are_mechanical():
    ch1 = build_syllabus()["chapters"][0]
    assert all(p["verified"] for p in ch1["pages"])
