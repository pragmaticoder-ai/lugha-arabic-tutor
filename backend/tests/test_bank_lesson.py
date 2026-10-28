"""Tests for the verified bank + Gemini composition path (SPEC-02/06).
Gemini is DISABLED here (LUGHA_DISABLE_GEMINI=1) so tests are deterministic/offline."""
import os

os.environ["LUGHA_DISABLE_GEMINI"] = "1"

from fastapi.testclient import TestClient  # noqa: E402

from app.bank import select_item  # noqa: E402
from app.gemini import compose_lesson  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)


def test_bank_selects_highest_frequency_first():
    # require_verified=False because seed ships verified=false until human review
    item = select_item("reading", 1, require_verified=False)
    assert item is not None
    assert item.item_id == "greet_marhaba"  # lowest freq_rank (1)


def test_bank_returns_none_when_no_item():
    assert select_item("writing", 99, require_verified=False) is None


def test_compose_fallback_never_invents_focus():
    item = select_item("reading", 1, require_verified=False)
    lesson = compose_lesson(item)
    # focus Arabic is the verified item, unchanged; source is never 'verified' for example
    assert lesson.focus.arabic == item.arabic
    assert lesson.source in {"fallback", "generated"}


def test_lesson_next_needs_content_when_unverified_bank():
    # Default require_verified=True in the endpoint; seed is verified=false → needs_content
    r = client.post("/lesson/next?level=1", json={"learner_id": "you", "skill": "reading"})
    assert r.status_code == 200
    assert r.json()["status"] == "needs_content"  # honest: no fabricated fundamental


def test_lesson_next_bad_skill_422():
    r = client.post("/lesson/next", json={"learner_id": "you", "skill": "cooking"})
    assert r.status_code == 422
