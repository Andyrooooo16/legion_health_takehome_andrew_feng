"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ResearchDisclaimer from "@/components/ResearchDisclaimer";
import { ensureAssigned } from "@/lib/participant";

// Page 1 — Intro. Establishes (sticky) assignment and fires `concept_assigned`
// immediately on mount, per experiment_spec.md §4 ("Fires the instant the ... flag
// resolves a variant for this distinct_id, before Page 2 renders").
export default function IntroPage() {
  const router = useRouter();
  const [consented, setConsented] = useState(false);

  useEffect(() => {
    // Resolves/creates the sticky assignment and fires concept_assigned exactly once,
    // synchronously, as soon as this page mounts — no setState needed here, since the
    // assignment itself is persisted to localStorage (read back by later pages) rather
    // than surfaced in this component's own render.
    ensureAssigned();
  }, []);

  return (
    <main className="page-shell">
      <span className="eyebrow">Research Study — Concept Test</span>
      <h1>Help us understand patient reactions to a new care model</h1>
      <p>
        Thank you for taking part in this short research study. You will be shown one
        description of a hypothetical mental health care model, asked how you would
        respond to it, and then answer a brief survey about your reactions.
      </p>

      <div className="card">
        <h2>Before you begin, please note:</h2>
        <ul style={{ paddingLeft: 18, display: "flex", flexDirection: "column", gap: 6 }}>
          <li>This is a <strong>research concept test</strong>, not a real clinical service.</li>
          <li>You will <strong>not receive any actual medical care</strong> during this study.</li>
          <li>You do <strong>not need to share any personal health information</strong> to participate.</li>
          <li>Your responses are used <strong>for research purposes only</strong>.</li>
          <li>Participation is voluntary — you may stop at any time without penalty.</li>
          <li>This study is not a substitute for medical advice. If you are in crisis, please contact local emergency services or a crisis line.</li>
        </ul>
      </div>

      <ResearchDisclaimer />

      <label style={{ display: "flex", gap: 10, alignItems: "flex-start", fontSize: 14 }}>
        <input
          type="checkbox"
          checked={consented}
          onChange={(e) => setConsented(e.target.checked)}
          style={{ marginTop: 3 }}
        />
        <span>
          I am 18 or older, I understand this is a research study and not a clinical
          encounter, and I voluntarily consent to participate.
        </span>
      </label>

      <div className="button-row">
        <button
          className="btn btn-primary"
          disabled={!consented}
          onClick={() => router.push("/concept")}
        >
          Begin study
        </button>
      </div>
    </main>
  );
}
