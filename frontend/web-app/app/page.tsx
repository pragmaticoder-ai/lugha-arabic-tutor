"use client";
import { useEffect, useState } from "react";

/**
 * Textbook layout — fetches the SEQUENCED syllabus from the backend /syllabus.
 * Falls back to a tiny inline set if the API is unreachable (dev without backend).
 * Shows the 4 positional letter forms for alphabet pages.
 */

type Page = {
  id: string; arabic: string; translit: string; sound?: string;
  forms?: { isolated: string; initial: string; medial: string; final: string };
  joins_left?: boolean; verified?: boolean; source?: string; page?: number;
};
type Chapter = { num: number; title: string; stage: string; pages: Page[] };

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const FALLBACK: Chapter[] = [
  { num: 1, title: "The Alphabet", stage: "Stage 0 · Foundation", pages: [
    { id: "alif", arabic: "ا", translit: "alif", sound: "long aa", forms: { isolated: "ا", initial: "ا", medial: "ـا", final: "ـا" }, joins_left: false },
    { id: "baa", arabic: "ب", translit: "baa", sound: "b", forms: { isolated: "ب", initial: "بـ", medial: "ـبـ", final: "ـب" }, joins_left: true },
  ]},
];

export default function Book() {
  const [chapters, setChapters] = useState<Chapter[]>(FALLBACK);
  const [offline, setOffline] = useState(false);
  const [ch, setCh] = useState(0);
  const [pg, setPg] = useState(0);

  useEffect(() => {
    fetch(`${API}/syllabus`)
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((d) => setChapters(d.chapters))
      .catch(() => setOffline(true));
  }, []);

  const chapter = chapters[ch] ?? chapters[0];
  const lesson = chapter.pages[pg] ?? chapter.pages[0];
  const atFirst = ch === 0 && pg === 0;
  const atLast = ch === chapters.length - 1 && pg === chapter.pages.length - 1;

  const [canSpeak, setCanSpeak] = useState(true);
  useEffect(() => {
    setCanSpeak(typeof window !== "undefined" && "speechSynthesis" in window);
  }, []);

  function speak(text: string) {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "ar-SA";           // Modern Standard Arabic
    u.rate = 0.75;             // slower, for learners
    const arVoice = window.speechSynthesis.getVoices().find((v) => v.lang.startsWith("ar"));
    if (arVoice) u.voice = arVoice;
    window.speechSynthesis.speak(u);
  }

  function next() {
    if (pg < chapter.pages.length - 1) setPg(pg + 1);
    else if (ch < chapters.length - 1) { setCh(ch + 1); setPg(0); }
  }
  function prev() {
    if (pg > 0) setPg(pg - 1);
    else if (ch > 0) { setCh(ch - 1); setPg(chapters[ch - 1].pages.length - 1); }
  }

  return (
    <div className="min-h-dvh bg-[#F3EFE6] text-ink">
      <header className="border-b border-[#E3DBC9] bg-[#FBF8F1]">
        <div className="mx-auto max-w-5xl px-6 py-4">
          <h1 className="font-arabic text-2xl text-lugha-700">لُغة · Lugha</h1>
          <p className="text-sm text-muted">An Arabic workbook — learn in order, page by page.</p>
          {offline && <p className="mt-1 text-xs text-gold-600">Backend offline — showing a sample page. Start the API to load the full syllabus.</p>}
        </div>
      </header>

      <div className="mx-auto grid max-w-5xl gap-6 px-6 py-8 md:grid-cols-[220px_1fr]">
        <aside className="md:border-r md:border-[#E3DBC9] md:pr-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">Contents</p>
          <ol className="space-y-1">
            {chapters.map((c, i) => (
              <li key={c.num}>
                <button onClick={() => { setCh(i); setPg(0); }}
                  className={`w-full rounded-lg px-3 py-2 text-left text-sm transition ${
                    i === ch ? "bg-lugha-50 font-semibold text-lugha-700" : "hover:bg-black/5"}`}>
                  <span className="text-muted">{c.num}.</span> {c.title}
                  <span className="block text-[11px] text-muted">{c.stage}</span>
                </button>
              </li>
            ))}
          </ol>
        </aside>

        <main>
          <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-gold-600">{chapter.stage}</div>
          <h2 className="mb-6 text-xl font-semibold">Chapter {chapter.num} — {chapter.title}</h2>

          <article className="rounded-2xl border border-[#E3DBC9] bg-[#FBF8F1] p-10 shadow-sm">
            <div className="text-center">
              <p className="font-arabic text-7xl leading-none text-ink">{lesson.arabic}</p>
              <p className="mt-4 text-lg text-lugha-700">{lesson.translit}</p>
              {lesson.sound && <p className="mx-auto mt-2 max-w-md text-muted">{lesson.sound}</p>}
            </div>

            {lesson.forms && (
              <div className="mt-8 border-t border-[#E3DBC9] pt-6">
                <p className="mb-3 text-center text-xs font-semibold uppercase tracking-wide text-muted">
                  The four forms {lesson.joins_left === false && "· does not join to the left"}
                </p>
                <div className="grid grid-cols-4 gap-2 text-center">
                  {(["isolated", "initial", "medial", "final"] as const).map((k) => (
                    <div key={k} className="rounded-xl bg-white/60 py-4">
                      <p className="font-arabic text-4xl text-ink">{lesson.forms![k]}</p>
                      <p className="mt-1 text-[11px] capitalize text-muted">{k}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="mt-8 flex flex-col items-center gap-2">
              <div className="flex items-center justify-center gap-3">
                <button onClick={() => speak(lesson.arabic)} disabled={!canSpeak}
                  className="rounded-lg border border-lugha-200 px-4 py-2 text-sm text-lugha-700 hover:bg-lugha-50 disabled:opacity-40">▶ Hear it</button>
                <button onClick={() => speak(lesson.arabic)} disabled={!canSpeak}
                  className="rounded-lg bg-gold-500 px-4 py-2 text-sm font-medium text-white hover:bg-gold-600 disabled:opacity-40">🎙 Repeat</button>
              </div>
              <p className="text-[11px] text-muted">
                {canSpeak
                  ? "Synthetic voice (your browser) — not a native recording."
                  : "Audio not available in this browser."}
              </p>
            </div>
          </article>

          {lesson.source && (
            <p className="mt-3 text-center text-[11px] text-muted">
              Source: {lesson.source}{lesson.page ? ` · p.${lesson.page}` : ""}
            </p>
          )}

          <nav className="mt-6 flex items-center justify-between">
            <button onClick={prev} disabled={atFirst}
              className="rounded-lg px-4 py-2 text-sm text-muted enabled:hover:bg-black/5 disabled:opacity-30">‹ Previous</button>
            <span className="text-xs text-muted">Chapter {chapter.num}, page {pg + 1} of {chapter.pages.length}</span>
            <button onClick={next} disabled={atLast}
              className="rounded-lg bg-lugha-600 px-4 py-2 text-sm font-medium text-white enabled:hover:bg-lugha-700 disabled:opacity-30">Next ›</button>
          </nav>
        </main>
      </div>
    </div>
  );
}
