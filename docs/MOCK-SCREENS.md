# Lugha — Mock Screens (Figma-ready reference)

Owner: Venkata · 2026-10-28
HONEST NOTE: no Figma MCP is connected in this session, so I cannot emit .fig frames.
This doc is written to be dropped into Figma / Figma AI ("make frames from this spec")
or built directly in the app. Tokens/components come from ../BRAND-AND-DESIGN.md.
The working Next.js app (frontend/web-app) is the live reference implementation of these.

Frame size: 390×844 (iPhone-ish, mobile-first). Desktop = same, container max 720px centered.
Global: bottom tab bar (Learn · Library · Progress · Profile), 44px targets, dark-mode-safe.

================================================================
SCREEN 1 — LEARNER PICKER (launch)
================================================================
- Logo "Lugha" (lugha-600) + tagline "Learn Arabic, step by step".
- Grid of large avatar cards (2-col): You, Kid 1, Kid 2 + "＋ Add learner".
- Tap avatar → sets active learner → Learn. Card: white, radius 12, 72px avatar.
States: empty (only "Add learner"), 1–4 learners.

================================================================
SCREEN 2 — LEARN (home of the loop)
================================================================
Header row: "Lugha" (left) · 🔥 streak pill gold (right).
Card A (lesson): skill pill (skill color @15%) "Reading · L1";
  Arabic focus (Naskh, ~2rem, RTL) "مَرْحَبًا"; translit+meaning line (slate-500);
  [▶ Hear it] primary; [🎙 Repeat (shadow)] gold.
Card B (pushed output): "Your turn (say it)" + prompt text.
CTA: [Continue →] primary, full width. Below: "4 items due for review" (slate-500).
States: loading, needs_content ("new content coming"), due=0.

================================================================
SCREEN 3 — QUIZ (one question per screen)
================================================================
Top: progress dots (●●○○○) + skill-colored header bar.
Body: question (recognition = MCQ 2×2 cards; production = record/type).
Feedback: gentle inline ✓/✗ with the correct form; no harsh red for kids.
End-of-quiz DIAGNOSTIC card: per-skill mini-bars + one line
  ("Strong reading · Listening needs work") + [See my next lesson].

================================================================
SCREEN 4 — LIBRARY (shelf)
================================================================
Title "Library" + sub "Read like a book — no quiz, just immersion."
2-col grid of chapter covers (📖 + title): Greetings, Numbers, Colours, Food.
Filter chip row: level ≤ current+1. Calm, no streak/XP here.

================================================================
SCREEN 5 — READER (read-as-a-book)
================================================================
Paged view (swipe). Large RTL Naskh text; translit toggle (top-right, default on for kids).
Tap a word → popover: Arabic + translit + meaning + [▶ audio].
Bottom: page indicator (3/12), ‹ › buttons. NO quiz/XP. Exit = back to shelf.

================================================================
SCREEN 6 — PROGRESS
================================================================
4 per-skill bars in skill colors (Listening blue, Speaking gold, Reading green,
  Writing violet) with % to next level; "not started" state distinct from 0%.
Streak calendar (gold dots), current + best streak.
Review health: due today / mastered / overdue counts.
Badges row (earned) + next milestone target.

================================================================
SCREEN 7 — PROFILE / SWITCH
================================================================
Active learner card; list of learners to switch; [Add learner]; settings
(translit default, reduced motion, parent view toggle). Child vs adult indicated.

================================================================
GAMIFICATION OVERLAYS (not full screens)
================================================================
- Level-up: brief centered celebration (gold), reduced-motion-safe, auto-dismiss.
- Badge earned: toast + badge appears on Progress.
- Streak +1: small flame bump on Learn header.

Design rules (enforce in every frame): every surface sets bg+text together
(dark-mode safe); Arabic ≥1.4× body, diacritics never clipped; audio always has a
visible control; color never the only signal (bars carry labels); animations brief,
stoppable, respect reduced-motion.
