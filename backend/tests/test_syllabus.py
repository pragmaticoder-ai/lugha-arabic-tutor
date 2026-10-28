"""Tests for the sequenced syllabus (SPEC-02) — driven by Mastering Arabic 1."""
from app.syllabus import build_syllabus


def test_all_28_letters_across_group_chapters():
    syl = build_syllabus()
    letter_pages = [p for ch in syl["chapters"] for p in ch["pages"] if p.get("forms")]
    assert len(letter_pages) == 28


def test_book_order_group1_first():
    # Mastering Arabic 1 starts with group 1: baa, taa, thaa, nuun, yaa (NOT alif first)
    ch1 = build_syllabus()["chapters"][0]
    names = [p["translit"] for p in ch1["pages"]]
    assert names == ["baa", "taa", "thaa", "nuun", "yaa"]


def test_every_letter_has_four_forms():
    for ch in build_syllabus()["chapters"]:
        for p in ch["pages"]:
            if p.get("forms"):
                assert set(p["forms"]) == {"isolated", "initial", "medial", "final"}
                assert all(p["forms"].values())


def test_letters_before_words():
    chapters = build_syllabus()["chapters"]
    first_word_ch = next(i for i, c in enumerate(chapters) if "Words" in c["title"])
    first_letter_ch = 0
    assert first_letter_ch < first_word_ch


def test_book_source_recorded():
    assert build_syllabus()["book_source"] == "SRC-MASTERING-ARABIC-1"


def test_non_joining_letters_flagged():
    letters = {p["translit"]: p for ch in build_syllabus()["chapters"]
               for p in ch["pages"] if p.get("forms")}
    assert letters["alif"]["joins_left"] is False
    assert letters["raa"]["joins_left"] is False
    assert letters["baa"]["joins_left"] is True
