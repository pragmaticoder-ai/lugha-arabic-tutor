# SPEC-01 — Learner Profiles & Switching

Status: builds on SPEC-00. Owner: Venkata · 2026-10-28.

## 1. Requirement
Create and select learners (you + each kid). Each learner has an independent track:
own skill levels, progress, schedule, badges. Switching learner changes all state
the app reads/writes. A learner is marked is_child to drive age-appropriate tone,
encouragement emphasis, and starting level.

Behavior:
- Create learner (name, is_child). On create, seed SkillLevel=1 for all 4 skills.
- List learners; select active learner (held client-side as active_learner_id).
- Switching is instant and isolates state — no bleed between learners.
- Delete a learner removes their rows (progress, skill_level, quiz_results, badges).

## 2. Field validations
- name: required, 1–40 chars, trimmed, not whitespace-only.
- is_child: boolean, default false.
- active_learner_id (on any learner-scoped call): required, must resolve to an
  existing learner → else 404 learner_not_found.
- Create rejects a duplicate name within the same family (case-insensitive) → 409.

## 3. Unit tests
- create seeds 4 SkillLevel rows at level 1.
- name validator: "", "   ", 41 chars → rejected; "Sara" → ok.
- duplicate-name (case-insensitive) rejected.

## 4. Integration tests
- create → list returns it; select → learner-scoped read returns only that learner's rows.
- two learners: progress written under A never appears under B (isolation).
- delete learner cascades (no orphan progress/quiz/badge rows).

## 5. Non-functional requirements
- PRIVACY: children's data minimised — name + progress only; no DOB/PII required.
  Parent-controlled; all learners live in the family's own project.
- SECURITY: learner-scoped endpoints must enforce the learner id server-side
  (never trust a client-supplied id without existence check).
- UX/ACCESSIBILITY: picker uses large avatars + names, 44px targets (kids).
- PERFORMANCE: switch learner is a client state change + indexed reads only.

## 6. Depends on / enables
Depends on: SPEC-00. Enables: 02 (lessons are learner-scoped), all later specs.
