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

## SRC-MASTERING-ARABIC-1
**Mastering Arabic 1**, 4th edition (2024). Jane Wightwick & Mahmoud Gaafar.
Bloomsbury Academic. ISBN per Bloomsbury 2024 edition. MSA / Fus'ha, self-study.
File: ~/Downloads/Mastering_Arabic_1_-_Jane_Wightwick.pdf (384 pp).

Authentic teaching sequence (from the book's Contents) — letters in GROUPS, words later:
- Unit 1 (p.2):  letters ب ت ث ن ي · vowels · joining · Greetings
- Unit 2 (p.13): letters ا د ذ ر ز و · long vowels · Introducing yourself
- Unit 3 (p.25): letters ج ح خ ه م · feminine words · The family
- Unit 4 (p.37): letters س ش ص ض · plurals · Jobs
- Unit 5 (p.51): letters ف ق ك ل · the article الـ · Describing things
- Unit 6 (p.66): letters ط ظ ع غ · emphatic letters · sun letters · hamza
- Unit 10 (p.118): Arabic numbers 1–10
- Unit 11 (p.144): Colours
- Unit 12 (p.151): Eating and drinking (food)

> This is a copyrighted textbook. Cite unit/page as the SOURCE of the sequence and
> of an item's correctness; do NOT copy its text/exercises into the app. Items
> reproduce only the letters/words themselves (not copyrightable) + a page cite.

## SRC-NATIVE-REVIEW  (process, not a document)
A named native Arabic speaker who confirmed harakat/pronunciation for an item.
Record their name + date in the item. Required before any KIDS content is verified.

---

## Rule
`source` on an item = one of these ids (+ page/locator where relevant).
Letter shapes may cite SRC-UNICODE-JOINING and be verified.
SOUNDS, MEANINGS, SEQUENCE and HARAKAT need SRC-UAE-FRAMEWORK or SRC-TEXTBOOK,
and kids' items also need SRC-NATIVE-REVIEW, before verified:true.
