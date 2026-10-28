"use client";
import { useState } from "react";

/**
 * Textbook-style layout: a calm, page-like workbook — NOT an app dashboard.
 * Left: contents (chapters/stages, in sequence). Right: the open "page".
 * Sequence follows docs/SYLLABUS.md: Letters → Harakat → Numerals → Decoding → Words.
 */

type Lesson = { id: string; arabic: string; translit: string; note: string };
type Chapter = { num: number; title: string; stage: string; lessons: Lesson[] };

const BOOK: Chapter[] = [
  { num: 1, title: "The Alphabet", stage: "Stage 0 · Foundation", lessons: [
    { id: "alif", arabic: "ا", translit: "alif", note: "Sound: long 'aa'. Does not join to the left." },
    { id: "baa", arabic: "ب", translit: "baa", note: "Sound: 'b'. Forms: بـ ـبـ ـب" },
    { id: "taa", arabic: "ت", translit: "taa", note: "Sound: 't'. Two dots above." },
    { id: "thaa", arabic: "ث", translit: "thaa", note: "Sound: 'th'. Three dots above." },
  ]},
  { num: 2, title: "Short Vowels (Harakat)", stage: "Stage 0 · Foundation", lessons: [
    { id: "fatha", arabic: "بَ", translit: "ba", note: "Fatha: short 'a' above the letter." },
    { id: "kasra", arabic: "بِ", translit: "bi", note: "Kasra: short 'i' below the letter." },
    { id: "damma", arabic: "بُ", translit: "bu", note: "Damma: short 'u' above the letter." },
  ]},
  { num: 3, title: "Numerals ٠–٩", stage: "Stage 0 · Foundation", lessons: [
    { id: "n0", arabic: "٠", translit: "sifr", note: "Numeral 0." },
    { id: "n1", arabic: "١", translit: "wahid", note: "Numeral 1." },
    { id: "n2", arabic: "٢", translit: "ithnan", note: "Numeral 2." },
  ]},
  { num: 4, title: "Decoding Syllables", stage: "Stage 1 · Reading", lessons: [
    { id: "ba_series", arabic: "بَ بِ بُ", translit: "ba · bi · bu", note: "Blend a consonant with each short vowel." },
    { id: "al", arabic: "الـ", translit: "al-", note: "The article 'the'. Sun vs moon letters." },
  ]},
  { num: 5, title: "First Words", stage: "Stage 2 · Vocabulary", lessons: [
    { id: "marhaba", arabic: "مَرْحَبًا", translit: "marhaban", note: "hello — now you can decode it." },
    { id: "shukran", arabic: "شُكْرًا", translit: "shukran", note: "thank you" },
  ]},
];

export default function Book() {
  const [ch, setCh] = useState(0);
  const [pg, setPg] = useState(0);
  const chapter = BOOK[ch];
  const lesson = chapter.lessons[pg];
  const atFirst = ch === 0 && pg === 0;
  const atLast = ch === BOOK.length - 1 && pg === chapter.lessons.length - 1;

  function next() {
    if (pg < chapter.lessons.length - 1) setPg(pg + 1);
    else if (ch < BOOK.length - 1) { setCh(ch + 1); setPg(0); }
  }
  function prev() {
    if (pg > 0) setPg(pg - 1);
    else if (ch > 0) { setCh(ch - 1); setPg(BOOK[ch - 1].lessons.length - 1); }
  }

  return (
    <div className="min-h-dvh bg-[#F3EFE6] text-ink">
      {/* Book masthead */}
      <header className="border-b border-[#E3DBC9] bg-[#FBF8F1]">
        <div className="mx-auto max-w-5xl px-6 py-4">
          <h1 className="font-arabic text-2xl text-lugha-700">لُغة · Lugha</h1>
          <p className="text-sm text-muted">An Arabic workbook — learn in order, page by page.</p>
        </div>
      </header>

      <div className="mx-auto grid max-w-5xl gap-6 px-6 py-8 md:grid-cols-[220px_1fr]">
        {/* Table of contents */}
        <aside className="md:border-r md:border-[#E3DBC9] md:pr-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">Contents</p>
          <ol className="space-y-1">
            {BOOK.map((c, i) => (
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

        {/* The open page */}
        <main>
          <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-gold-600">{chapter.stage}</div>
          <h2 className="mb-6 text-xl font-semibold">Chapter {chapter.num} — {chapter.title}</h2>

          <article className="rounded-2xl border border-[#E3DBC9] bg-[#FBF8F1] p-10 shadow-sm">
            <div className="text-center">
              <p className="font-arabic text-7xl leading-none text-ink">{lesson.arabic}</p>
              <p className="mt-4 text-lg text-lugha-700">{lesson.translit}</p>
              <p className="mx-auto mt-3 max-w-md text-muted">{lesson.note}</p>
            </div>
            <div className="mt-8 flex items-center justify-center gap-3">
              <button className="rounded-lg border border-lugha-200 px-4 py-2 text-sm text-lugha-700 hover:bg-lugha-50">▶ Hear it</button>
              <button className="rounded-lg bg-gold-500 px-4 py-2 text-sm font-medium text-white hover:bg-gold-600">🎙 Repeat</button>
            </div>
          </article>

          {/* Page turn */}
          <nav className="mt-6 flex items-center justify-between">
            <button onClick={prev} disabled={atFirst}
              className="rounded-lg px-4 py-2 text-sm text-muted enabled:hover:bg-black/5 disabled:opacity-30">‹ Previous page</button>
            <span className="text-xs text-muted">Chapter {chapter.num}, page {pg + 1} of {chapter.lessons.length}</span>
            <button onClick={next} disabled={atLast}
              className="rounded-lg bg-lugha-600 px-4 py-2 text-sm font-medium text-white enabled:hover:bg-lugha-700 disabled:opacity-30">Next page ›</button>
          </nav>
        </main>
      </div>
    </div>
  );
}
