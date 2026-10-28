"use client";
import { useState } from "react";

const TABS = ["Learn", "Library", "Progress", "Profile"] as const;
type Tab = (typeof TABS)[number];

export default function Home() {
  const [tab, setTab] = useState<Tab>("Learn");
  return (
    <main className="container">
      {tab === "Learn" && <Learn />}
      {tab === "Library" && <Library />}
      {tab === "Progress" && <Progress />}
      {tab === "Profile" && <Profile />}
      <nav className="tabbar">
        {TABS.map((t) => (
          <button key={t} className={`tab ${tab === t ? "active" : ""}`} onClick={() => setTab(t)}>{t}</button>
        ))}
      </nav>
    </main>
  );
}

function Learn() {
  return (
    <>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: 22 }}>Lugha</h1>
        <span className="streak">🔥 3-day streak</span>
      </div>
      <div className="card" style={{ marginTop: 12 }}>
        <span className="skill-pill" style={{ background: "#E8F5F1", color: "#0E7C66" }}>Reading · L1</span>
        <p className="arabic">مَرْحَبًا</p>
        <p style={{ color: "var(--slate-500)", margin: "4px 0" }}>marḥaban — hello</p>
        <button className="btn" style={{ marginTop: 8 }}>▶ Hear it</button>
        <button className="btn btn-gold" style={{ marginTop: 8 }}>🎙 Repeat (shadow)</button>
      </div>
      <div className="card" style={{ marginTop: 12 }}>
        <b>Your turn (say it):</b>
        <p style={{ color: "var(--slate-500)" }}>How do you greet someone? Reply in Arabic.</p>
      </div>
      <button className="btn" style={{ marginTop: 16 }}>Continue →</button>
      <p style={{ color: "var(--slate-500)", fontSize: 13, marginTop: 8 }}>4 items due for review</p>
    </>
  );
}

function Library() {
  return (
    <>
      <h1 style={{ fontSize: 22 }}>Library</h1>
      <p style={{ color: "var(--slate-500)" }}>Read like a book — no quiz, just immersion.</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }}>
        {["Greetings", "Numbers", "Colours", "Food"].map((c) => (
          <div key={c} className="card" style={{ textAlign: "center" }}>
            <div style={{ fontSize: 28 }}>📖</div><b>{c}</b>
          </div>
        ))}
      </div>
    </>
  );
}

function Progress() {
  const skills = [["Listening","#0284C7",40],["Speaking","#D9A441",25],["Reading","#0E7C66",60],["Writing","#7C3AED",20]] as const;
  return (
    <>
      <h1 style={{ fontSize: 22 }}>Progress</h1>
      {skills.map(([name, color, pct]) => (
        <div key={name} style={{ margin: "12px 0" }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13 }}><span>{name}</span><span>{pct}%</span></div>
          <div style={{ background: "var(--slate-200)", borderRadius: 999, height: 10 }}>
            <div style={{ width: `${pct}%`, background: color as string, height: 10, borderRadius: 999 }} />
          </div>
        </div>
      ))}
    </>
  );
}

function Profile() {
  return (
    <>
      <h1 style={{ fontSize: 22 }}>Who's learning?</h1>
      <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
        {["You", "Kid 1", "Kid 2"].map((n) => (
          <div key={n} className="card" style={{ textAlign: "center", flex: 1 }}>
            <div style={{ fontSize: 32 }}>🙂</div><b>{n}</b>
          </div>
        ))}
      </div>
    </>
  );
}
