# Content Sources — Lugha

Every teachable item MUST cite one of these. No source → `verified:false` →
the app refuses to teach it (enforced in code, see SPEC-02 / sources.py).
This file is the ONLY place a source id is defined. Do not invent content.

---

## SRC-UAE-FRAMEWORK
**UAE Framework for Learning Arabic as an Additional Language** (MoE).
Read via the Education Perfect curriculum-alignment map (public PDF):
https://www.educationperfect.com/media/content/Arabic/1614247153.1611281f/1614247153073-3584839929757840.pdf

Authentic Year-1 (one year of study) performance indicators, quoted:
- "The student can sometimes recognize the letter sounds which he learned in the context of familiar words."
- "The student can understand single words that have been learned and memorized."
- "The student can understand common greetings."
- "The student can recognize some colour names."
- "The student can count from one to ten."
- "The student knows some types of food."

Four skills: Listening, Speaking, Reading, Writing (framework structure).

> HONEST NOTE: this is the framework as quoted by a third-party alignment map,
> NOT the MoE original. Get the MoE PDF to confirm exact level descriptors
> before treating any level boundary as authoritative.

## SRC-UNICODE-JOINING
Arabic letter positional FORMS (isolated/initial/medial/final) and which letters
do not join left. Mechanical from the Unicode bidi/joining algorithm — not opinion.
Use ONLY for letter shapes, never for sounds, meaning, or sequence.

## SRC-TEXTBOOK  (placeholder — you fill this)
A named, published beginner Fus'ha textbook you own, e.g.:
  "Alif Baa: Introduction to Arabic Letters and Sounds, 3rd ed., Georgetown UP"
Record: title, edition, page/unit for each item. REPLACE this line with the
real book before citing it.

## SRC-NATIVE-REVIEW  (process, not a document)
A named native Arabic speaker who confirmed harakat/pronunciation for an item.
Record their name + date in the item. Required before any KIDS content is verified.

---

## Rule
`source` on an item = one of these ids (+ page/locator where relevant).
Letter shapes may cite SRC-UNICODE-JOINING and be verified.
SOUNDS, MEANINGS, SEQUENCE and HARAKAT need SRC-UAE-FRAMEWORK or SRC-TEXTBOOK,
and kids' items also need SRC-NATIVE-REVIEW, before verified:true.
