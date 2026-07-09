"use client";

import { useEffect, useState } from "react";
import ResearchDisclaimer from "@/components/ResearchDisclaimer";

// Page 5 — Thank You. No PostHog event is required here per experiment_spec.md §4
// ("no event required; optionally log page view via default PostHog pageview capture").
// We intentionally do not fire a custom event to stay within the frozen §4 event list.
export default function ThankYouPage() {
  const [exited, setExited] = useState(false);

  useEffect(() => {
    // window.location is unavailable during server rendering — reading it on mount and
    // setting state is the standard client-only-data pattern here (kept out of
    // useSearchParams/Suspense to keep this a plain static page).
    const params = new URLSearchParams(window.location.search);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setExited(params.get("exited") === "true");
  }, []);

  return (
    <main className="page-shell">
      <span className="eyebrow">Thank You</span>
      <h1>{exited ? "Thanks for your time" : "Thank you for participating"}</h1>

      {exited ? (
        <p>
          You chose to exit before completing the survey. That&apos;s completely fine —
          thank you for considering this concept.
        </p>
      ) : (
        <p>
          Thank you for sharing your reactions. Your responses will help inform whether
          and how this care model concept could be refined.
        </p>
      )}

      <div className="card">
        <h2>A reminder about this study</h2>
        <ul style={{ paddingLeft: 18, display: "flex", flexDirection: "column", gap: 6 }}>
          <li>No data from this study was shared with any sponsor.</li>
          <li>This was a research concept only — no real care was provided or affected.</li>
          <li>If you are a real Legion patient, your actual care is completely unaffected by this study.</li>
          <li>No personal health information was collected.</li>
        </ul>
      </div>

      <ResearchDisclaimer />

      <p className="muted">You may now close this window.</p>
    </main>
  );
}
