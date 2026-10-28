"""Unit + integration tests for the adaptive core and API (SPEC-04/05/06)."""
from fastapi.testclient import TestClient

from app.adaptive import decide_action, rolling_action, next_interval_days
from app.main import app

client = TestClient(app)


# ---- UNIT: branch logic (SPEC-04) ----
def test_decide_action_thresholds():
    assert decide_action(90) == "advance"
    assert decide_action(85) == "advance"
    assert decide_action(70) == "reteach"
    assert decide_action(60) == "reteach"
    assert decide_action(40) == "drop_and_drill"


def test_decide_action_rejects_out_of_range():
    import pytest
    for bad in (-1, 101):
        with pytest.raises(ValueError):
            decide_action(bad)


def test_rolling_signal_smooths_one_bad_quiz():
    # two strong, one bad -> still not dropped to weak
    assert rolling_action([90, 88, 40]) in {"advance", "reteach"}


# ---- UNIT: spaced repetition (SPEC-05) ----
def test_srs_advances_then_resets_on_miss():
    interval, idx = next_interval_days(0, correct=True)
    assert (interval, idx) == (3, 1)
    interval, idx = next_interval_days(idx, correct=False)
    assert (interval, idx) == (1, 0)


# ---- INTEGRATION: grade endpoint ties answers -> per-skill action ----
def test_grade_quiz_integration():
    r = client.post("/quiz/grade", json={
        "learner_id": "you",
        "answers": [
            {"item_id": "i1", "skill": "reading", "is_recognition": True, "correct": True},
            {"item_id": "i2", "skill": "reading", "is_recognition": True, "correct": True},
            {"item_id": "i3", "skill": "listening", "is_recognition": False, "correct": False},
        ],
    })
    assert r.status_code == 200
    body = r.json()
    assert body["per_skill"]["reading"]["action"] == "advance"
    assert body["per_skill"]["listening"]["action"] == "drop_and_drill"


def test_field_validation_rejects_bad_skill():
    r = client.post("/quiz/grade", json={
        "learner_id": "you",
        "answers": [{"item_id": "i1", "skill": "cooking", "is_recognition": True, "correct": True}],
    })
    assert r.status_code == 422  # pydantic validation


def test_health():
    assert client.get("/health").json() == {"status": "ok"}
