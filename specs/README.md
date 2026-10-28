# Lugha — Specs (layered; each builds on the previous)

Every spec contains: Requirement · Field validations · Unit tests · Integration
tests · Non-functional requirements (NFRs). Build in order; each depends on the prior.

| # | Spec | Builds on | Core |
|---|------|-----------|------|
| 00 | Foundation & data model | — | entities, verified lesson bank schema |
| 01 | Learner profiles & switching | 00 | create/select learner (you + kids) |
| 02 | Curriculum & lesson delivery | 00,01 | serve i+1 lesson (Arabic+translit+meaning), UAE-framework-leveled |
| 03 | Audio: TTS + shadow | 02 | speak Fusha; record-and-compare |
| 04 | Adaptive quiz engine | 02,03 | diagnostic quiz (skill/item/type), scoring, branch logic |
| 05 | Spaced-repetition scheduler | 00,04 | due-item scheduling; quiz feeds it |
| 06 | Adaptive next-lesson generation | 04,05 | next lesson from quiz result — loop closes |
| 07 | Library / read-as-a-book | 02 | paged reader, tap-word→meaning+audio, no-quiz immersion |
| 08 | Gamification | 04,05,06 | streaks, XP, badges tied to real milestones |
| 09 | Progress dashboard | 04,05,08 | per-skill bars, streak calendar, badges |

Status: SPEC-00 written as the template. 01–09 follow the same shape.
Design/brand: ../BRAND-AND-DESIGN.md
