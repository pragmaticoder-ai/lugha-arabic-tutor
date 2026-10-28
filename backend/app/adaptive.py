"""Core adaptive logic — pure functions, no I/O, fully unit-testable.

Implements the quiz-as-sensor branch logic (SPEC-04) and spaced-repetition
scheduling (SPEC-05). Kept free of Gemini/DB so it is deterministic to test.
"""
from __future__ import annotations

from dataclasses import dataclass

SKILLS = ("listening", "speaking", "reading", "writing")

# Mastery thresholds (SPEC-04 — tunable). Per-skill percent 0..100.
MASTER = 85
PARTIAL = 60


@dataclass
class SkillOutcome:
    skill: str
    percent: float  # 0..100


def decide_action(percent: float) -> str:
    """Branch logic: master -> advance, partial -> reteach, weak -> drop+drill."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be 0..100")
    if percent >= MASTER:
        return "advance"
    if percent >= PARTIAL:
        return "reteach"
    return "drop_and_drill"


def rolling_action(history: list[float]) -> str:
    """Use a ROLLING signal (last up-to-3) so one bad quiz doesn't over-correct."""
    if not history:
        raise ValueError("history empty")
    window = history[-3:]
    avg = sum(window) / len(window)
    return decide_action(avg)


# Spaced repetition (SPEC-05): simple expanding schedule in days.
SRS_STEPS = [1, 3, 7, 21, 60]


def next_interval_days(prev_step_index: int, correct: bool) -> tuple[int, int]:
    """Return (interval_days, new_step_index). Miss resets to the first step."""
    if correct:
        idx = min(prev_step_index + 1, len(SRS_STEPS) - 1)
    else:
        idx = 0
    return SRS_STEPS[idx], idx
