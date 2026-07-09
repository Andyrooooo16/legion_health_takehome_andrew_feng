"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ResearchDisclaimer from "@/components/ResearchDisclaimer";
import { capture } from "@/lib/analytics";
import { readAssignment } from "@/lib/participant";
import { getCurrentRecord, saveCurrentRecord } from "@/lib/storage";
import { getVariantConfig } from "@/lib/variants";
import type { ParticipantAssignment, ParticipantRecord } from "@/lib/types";

// Page 3 — Behavioral Action. Implements the five actions from experiment_spec.md §4:
// Continue / Learn more / View privacy details / Choose sponsor-free option / Exit.
// Continue and "Choose sponsor-free option" proceed to the survey; Exit terminates
// the funnel and skips the survey entirely (per the funnel table's survey_started
// trigger: "only for participants who did not exit at Page 3").
export default function ActionPage() {
  const router = useRouter();
  const [assignment, setAssignment] = useState<ParticipantAssignment | null>(null);
  const [learnMoreOpen, setLearnMoreOpen] = useState(false);
  const [privacyOpen, setPrivacyOpen] = useState(false);

  useEffect(() => {
    const a = readAssignment();
    if (!a) {
      router.replace("/");
      return;
    }
    const record = getCurrentRecord();
    if (!record?.exposed) {
      router.replace("/concept");
      return;
    }
    // Assignment lives in localStorage, unavailable during server rendering — this is
    // the standard client-only-data-load pattern, not a value derivable during render.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setAssignment(a);
  }, [router]);

  if (!assignment) return null;

  const config = getVariantConfig(assignment.variant);
  const baseProps = {
    variant: assignment.variant,
    sponsor_category: assignment.sponsorCategory,
    participant_type: assignment.participantType,
  };

  function updateRecord(patch: Partial<ParticipantRecord>) {
    const existing = getCurrentRecord();
    if (!existing) return;
    saveCurrentRecord({ ...existing, ...patch });
  }

  function handleLearnMore() {
    capture("learn_more_clicked", baseProps);
    updateRecord({ learnMoreClicked: true });
    setLearnMoreOpen(true);
  }

  function handlePrivacy() {
    capture("privacy_details_opened", baseProps);
    updateRecord({ privacyDetailsOpened: true });
    setPrivacyOpen(true);
  }

  function handleContinue() {
    capture("continue_clicked", { ...baseProps, decision_result: "continue" });
    updateRecord({ decisionResult: "continue", optOut: false, exitedAtAction: false });
    router.push("/survey");
  }

  function handleOptOut() {
    capture("sponsor_opt_out_selected", {
      ...baseProps,
      decision_result: "opt_out",
      opt_out: true,
    });
    updateRecord({ decisionResult: "opt_out", optOut: true, exitedAtAction: false });
    router.push("/survey");
  }

  function handleExit() {
    capture("sponsor_opt_out_selected", {
      ...baseProps,
      decision_result: "exit",
      opt_out: true,
    });
    updateRecord({ decisionResult: "exit", optOut: true, exitedAtAction: true });
    router.push("/thank-you?exited=true");
  }

  return (
    <main className="page-shell">
      <span className="eyebrow">Step 3 of 4 — Your Response</span>
      <h1>What would you do next?</h1>
      <p>
        Imagine this care model was available to you today. Choose the option that best
        reflects what you would actually do.
      </p>

      <div className="card">
        <h2>{config.label}</h2>
        <p className="muted">{config.disclosureLine}</p>
      </div>

      {learnMoreOpen && (
        <div className="card">
          <h3>More about this concept</h3>
          <p>
            Sessions are delivered by licensed clinicians via secure video. Scheduling,
            intake, and clinical decisions are made independently of any sponsor.
            {config.sponsorCategory !== "none" &&
              " The sponsor's involvement is limited to funding support and, where noted, clearly separated educational content."}
          </p>
        </div>
      )}

      {privacyOpen && (
        <div className="card">
          <h3>Privacy details</h3>
          <p>
            Your health information is used only to provide your care. It is never sold
            or shared with a sponsor for advertising or marketing purposes. This research
            study does not collect diagnoses, medications, or other personal health
            information from you.
          </p>
        </div>
      )}

      <div className="button-row">
        <button className="btn btn-primary" onClick={handleContinue}>
          Continue
        </button>
        <button className="btn btn-secondary" onClick={handleLearnMore}>
          Learn more
        </button>
        <button className="btn btn-secondary" onClick={handlePrivacy}>
          View privacy details
        </button>
      </div>
      <div className="button-row">
        <button className="btn btn-secondary" onClick={handleOptOut}>
          Choose sponsor-free option
        </button>
        <button className="btn btn-danger" onClick={handleExit}>
          Exit
        </button>
      </div>

      <ResearchDisclaimer />
    </main>
  );
}
