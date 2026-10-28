"""Request/response models with field validations (mirrors each spec's validations)."""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

VALID_SKILLS = {"listening", "speaking", "reading", "writing"}


class Learner(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=40)
    is_child: bool = False


class LessonRequest(BaseModel):
    learner_id: str = Field(min_length=1, max_length=64)
    skill: str

    @field_validator("skill")
    @classmethod
    def _skill(cls, v: str) -> str:
        if v not in VALID_SKILLS:
            raise ValueError(f"skill must be one of {sorted(VALID_SKILLS)}")
        return v


class QuizAnswer(BaseModel):
    item_id: str = Field(min_length=1, max_length=64)
    skill: str
    is_recognition: bool  # recognition vs production (SPEC-04)
    correct: bool

    @field_validator("skill")
    @classmethod
    def _skill(cls, v: str) -> str:
        if v not in VALID_SKILLS:
            raise ValueError(f"skill must be one of {sorted(VALID_SKILLS)}")
        return v


class QuizSubmission(BaseModel):
    learner_id: str = Field(min_length=1, max_length=64)
    answers: list[QuizAnswer] = Field(min_length=1, max_length=50)
