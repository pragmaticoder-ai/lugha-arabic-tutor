# SPEC-00 — Foundation & Data Model

Status: base spec (everything builds on this). Owner: Venkata · 2026-10-28.

## 1. Requirement
Define the core entities and the verified-lesson-bank storage that all later specs
use. No feature behavior yet — this is the shared vocabulary and persistence.

Entities (see data/schema/schema.sql):
- Learner (id, name, is_child)
- LessonItem (id, skill, level, arabic, translit, meaning, verified, freq_rank)
- Progress (learner_id, item_id, srs_step, due_date, last_correct)
- SkillLevel (learner_id, skill, level)
- QuizResult (learner_id, skill, percent, taken_at)
- Badge (learner_id, badge_key, earned_at)

Skills are the UAE framework's four: listening, speaking, reading, writing.
Fundamentals are served from VERIFIED items (verified=true), not live generation.

## 2. Field validations
- Learner.id: non-empty, <=64 chars. Learner.name: 1–40 chars.
- LessonItem.skill: one of the 4 skills (DB CHECK + app enum). level: int >=1.
- LessonItem.arabic/translit/meaning: non-empty. verified: boolean.
- QuizResult.percent: 0–100 (DB CHECK + app validator).
- Progress.srs_step: int >=0. due_date: valid date.
- All skill fields constrained to the 4-skill set everywhere (DB + Pydantic).

## 3. Unit tests
- enum/skill validator rejects a non-skill (e.g. "cooking") — see backend tests.
- percent out of 0–100 rejected.
- name length bounds enforced.

## 4. Integration tests
- schema.sql applies cleanly to a fresh Postgres (CI: spin up, run, assert tables).
- insert learner + item + progress row; FK constraints hold; CHECKs reject bad skill/percent.

## 5. Non-functional requirements
- SECURITY: no secrets in repo; DB password via Secret Manager / env only. API keys server-side.
- PRIVACY: learners are family members (incl. children) — store only name + progress;
  no unnecessary PII; data stays in the user's own GCP project.
- PERFORMANCE: reads for "next lesson" + "due items" must be single-digit-ms indexed queries.
- PORTABILITY: schema standard Postgres (Cloud SQL now; swappable).
- ACCESSIBILITY (seeded here, enforced per UI spec): AA contrast, scalable Arabic,
  diacritics never clipped, audio never the only channel, tap targets >=44px.
- COST: smallest DB tier for family scale; no model calls at this layer.

## 6. Depends on / enables
Depends on: none. Enables: all subsequent specs (01–09).
