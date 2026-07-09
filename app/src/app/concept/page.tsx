"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import ResearchDisclaimer from "@/components/ResearchDisclaimer";
import { capture } from "@/lib/analytics";
import { readAssignment } from "@/lib/participant";
import { getCurrentRecord, saveCurrentRecord } from "@/lib/storage";
import { getVariantConfig } from "@/lib/variants";
import type { ParticipantAssignment, ParticipantRecord } from "@/lib/types";

// Page 2 — Sponsorship Concept. Renders the participant's single assigned variant.
// Fires `concept_viewed` once the content has mounted (single-viewport page, so
// on-mount is spec-acceptable per experiment_spec.md §4).
export default function ConceptPage() {
  const router = useRouter();
  const [assignment, setAssignment] = useState<ParticipantAssignment | null>(null);
  const firedRef = useRef(false);

  useEffect(() => {
    const a = readAssignment();
    if (!a) {
      // No assignment yet (e.g., direct navigation) — send back to intro to establish one.
      router.replace("/");
      return;
    }
    // Assignment lives in localStorage, which is unavailable during server rendering —
    // this read-on-mount + setState is the standard client-only-data pattern, not a
    // derivable-during-render value.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setAssignment(a);

    if (!firedRef.current) {
      firedRef.current = true;
      capture("concept_viewed", {
        variant: a.variant,
        sponsor_category: a.sponsorCategory,
        participant_type: a.participantType,
      });

      const existing = getCurrentRecord();
      const now = new Date().toISOString();
      const record: ParticipantRecord =
        existing && existing.distinctId === a.distinctId
          ? { ...existing, exposed: true }
          : {
              distinctId: a.distinctId,
              variant: a.variant,
              sponsorCategory: a.sponsorCategory,
              participantType: a.participantType,
              createdAt: now,
              updatedAt: now,
              exposed: true,
              learnMoreClicked: false,
              privacyDetailsOpened: false,
              optOut: false,
              exitedAtAction: false,
              surveyStarted: false,
              surveySubmitted: false,
            };
      saveCurrentRecord(record);
    }
  }, [router]);

  if (!assignment) return null;

  const config = getVariantConfig(assignment.variant);

  return (
    <main className="page-shell">
      <span className="eyebrow">Step 2 of 4 — Concept</span>
      <h1>{config.headline}</h1>

      <div className={`sponsor-banner ${config.sponsorCategory}`}>
        {config.disclosureLine}
      </div>

      <div className="card">
        {config.body.map((p, i) => (
          <p key={i} style={{ marginBottom: i < config.body.length - 1 ? 10 : 0 }}>
            {p}
          </p>
        ))}
      </div>

      {config.sponsorBlurb && <p className="muted">{config.sponsorBlurb}</p>}

      {config.sponsoredEducation && (
        <div className="card" style={{ background: "#fbf8ef" }}>
          <span className="eyebrow" style={{ color: "#8a5a00" }}>
            Sponsored — Separate From Your Care
          </span>
          <h3 style={{ marginTop: 8 }}>{config.sponsoredEducation.heading}</h3>
          <p>{config.sponsoredEducation.body}</p>
        </div>
      )}

      <ResearchDisclaimer />

      <div className="button-row">
        <button className="btn btn-primary" onClick={() => router.push("/action")}>
          Continue
        </button>
      </div>
    </main>
  );
}
