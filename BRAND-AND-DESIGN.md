# Lugha — Brand & Design System

Owner: Venkata · 2026-10-28
Personal adaptive Arabic tutor (self + kids), UAE-curriculum-aligned.
Design source of truth; all specs reference it. (No live Figma MCP in session —
this doc is written to drop straight into Figma / Figma AI to generate frames.)

## 1. NAME
**Lugha** (لُغة = "language"). Short, real Arabic word, child-sayable.
Tagline: "Learn Arabic, step by step" / "تعلّم العربية، خطوة بخطوة".
Alts: Kalima (كلمة), Harf (حرف), Daraj (steps).

## 2. PERSONALITY
Warm, patient, encouraging (works for a 6-year-old AND an adult). Calm, not noisy.
Celebrates small wins. Rooted in Arabic/UAE identity without cliché.

## 3. COLOR TOKENS
Primary teal-green: lugha-600 #0E7C66 (buttons/active), 700 #0A5F4E (pressed),
  50 #E8F5F1 (agent bubbles/tints), 100 #C9E9E0, 200 #9BD6C7
Accent sand/gold: gold-500 #D9A441 (streaks/rewards), 600 #B9872F, 100 #FBEFD6
Neutral slate: 50 #F7F9FB (bg), 100 #EEF2F6, 200 #E2E8F0 (borders),
  500 #64748B (secondary text), 800 #1E293B (headings), 900 #0F172A (nav)
Status: success #16A34A, warn #D97706, danger #DC2626, info #0284C7
Skill colors (consistent everywhere): Listening #0284C7 · Speaking #D9A441 ·
  Reading #0E7C66 · Writing #7C3AED
RULE: every surface sets bg + text together (dark-mode safe).

## 4. TYPOGRAPHY
UI: Inter (400/500/600). Arabic lessons: Noto Naskh Arabic (clear harakat);
Noto Kufi Arabic allowed for display/logo. Arabic lesson text >= 1.4x body.
Always pair Arabic + transliteration + meaning. RTL for Arabic; UI chrome LTR.

## 5. LAYOUT & SCREENS (mobile-first)
Bottom tab bar, 4 tabs: Learn · Library · Progress · Profile.
- Learner picker (launch): big avatars per learner.
- Learn: today's lesson card, gold streak, continue CTA, due count; lesson =
  Arabic(large) + translit + meaning + hear + record-shadow + output prompt.
- Quiz: one Q/screen, skill-colored header, progress dots, gentle feedback,
  end diagnostic + what's next.
- Library (read-as-a-book): shelf of chapter covers → paged reader, tap-word →
  meaning+audio, read-only immersion, no quiz pressure.
- Progress: per-skill level bars (skill colors), streak calendar, badges.

## 6. GAMIFICATION (motivation loop; esp. kids)
Streaks (gold flame) · XP/stars per lesson+quiz, bonus for mastery · badges tied
to REAL framework milestones (Alphabet, Numbers 1-10, First 100 words, 7-day streak,
Mastered Listening L1) · level-up animation on skill advance · family-only gentle
leaderboard. RULE: rewards attach to genuine learning events, never empty taps.

## 7. COMPONENTS
Buttons: primary lugha-600/white r10 w600; gold for rewards. Cards: white, border
slate-200 0.5px, r12. Agent bubble bg lugha-50. Skill tags: pill, skill color @15% bg.
Reduced-motion respected; celebratory animations brief + stoppable.

## 8. ACCESSIBILITY (NFR seed)
AA contrast; Arabic scalable, diacritics never clipped; audio always has visible
control (never audio-only); tap targets >= 44px (kids).
