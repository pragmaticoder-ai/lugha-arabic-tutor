# Lugha — Arabic Syllabus & Sequence

Owner: Venkata · 2026-10-28
Fixes the gap: a language starts with LETTERS and NUMERALS, not vocabulary.
Fusha (MSA). Aligned to UAE "Arabic as an Additional Language" early stages.
Each stage gates the next: you cannot read a WORD before letters + harakat.

================================================================
STAGE 0 — PRE-READING FOUNDATION  (must come first)
================================================================
0.1 The Arabic alphabet — 28 letters, in order:
    ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي
    - Teach NAME + SOUND of each letter. Reading is RIGHT-TO-LEFT.
0.2 Letter FORMS (critical, Arabic-specific): each letter changes shape by position
    — isolated / initial / medial / final. e.g. ب → بـ ـبـ ـب.
    - Teach which letters DON'T join to the left (ا د ذ ر ز و).
0.3 Short vowels / HARAKAT: fatha ( َ ), kasra ( ِ ), damma ( ُ ), sukun ( ْ ),
    shadda ( ّ ), tanwin ( ً ٍ ٌ ). These make letters readable as sounds.
0.4 Eastern Arabic NUMERALS 0–10: ٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ ١٠  (shape + value).
    (Distinct from the number WORDS — numerals are symbols, taught here.)

STAGE 0 EXIT: learner can name every letter, pick its 4 forms, read a letter +
harakat as a sound, and read numerals 0–10.

================================================================
STAGE 1 — DECODING  (letters → syllables → first reading)
================================================================
1.1 CV syllables: consonant + short vowel (بَ بِ بُ), blend letters into sound.
1.2 Two/three-letter syllable chains → read a simple pointed (voweled) word aloud.
1.3 Sun vs moon letters + the article الـ (al-) — why ال sometimes assimilates.
STAGE 1 EXIT: learner can SOUND OUT any fully-voweled short word, even unknown.

================================================================
STAGE 2 — FIRST WORDS  (NOW vocabulary is safe)
================================================================
Only here do the seeded items belong:
2.1 Greetings (marhaban, salam, shukran, naam, la)
2.2 Number WORDS 1–10 (wahid…ashara) — paired with the numerals from 0.4
2.3 Colours · 2.4 Food/basics
Each new word is fully voweled so Stage-1 decoding applies.

================================================================
STAGE 3 — PHRASES & GRAMMAR SEED
================================================================
Simple sentences (noun + adjective, "this is…"), pronouns, the article in context.
Pushed output: produce a 2–3 word phrase.

================================================================
SEQUENCE RULE (enforced by SPEC-02/06 level gating)
================================================================
level 1 = Stage 0 (letters, forms, harakat, numerals)
level 2 = Stage 1 (decoding/syllables)
level 3 = Stage 2 (first words — where old seed lives)
level 4 = Stage 3 (phrases)
The adaptive engine must NOT serve a Stage-2 word before Stage-0/1 mastery.
High-frequency-first applies WITHIN a stage, never across (no words before letters).

================================================================
HONEST NOTES
================================================================
- The earlier year1_bank.json seeded Stage-2 words at level 1 — WRONG order.
  Fix: those become level 3 (Stage 2); seed letters/harakat/numerals at level 1 (Stage 0),
  decoding at level 2 (Stage 1). (Reorder in a follow-up to the bank + seed.)
- All content still needs human harakat verification before verified=true (esp. for kids).
- Letter audio (28 names+sounds) via Cloud TTS; letter-form shapes may need images/font
  rendering, not just text — a build consideration for Stage 0.
