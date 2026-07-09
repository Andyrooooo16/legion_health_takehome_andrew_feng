"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import ResearchDisclaimer from "@/components/ResearchDisclaimer";
import { capture } from "@/lib/analytics";
import { readAssignment } from "@/lib/participant";
import { getCurrentRecord, saveCurrentRecord } from "@/lib/storage";
import {
  ALL_SURVEY_ITEMS,
  CORE_BOOK_ITEMS,
  CORE_ITEMS,
  FREE_TEXT_MAX_LENGTH,
  FREE_TEXT_PROMPT,
  LIKERT_LABELS,
  getComprehensionCheck,
  isIntentPositive,
  softPiiWarning,
} from "@/lib/survey";
import type { ParticipantAssignment } from "@/lib/types";

type LikertAnswers = Record<string, number | undefined>;

// Page 4 — Trust Survey. Fires `survey_started` on mount (only reached when the
// participant did not Exit at Page 3), presents the six core Likert items plus the
// flagged disclosure-comprehension check, and on submit fires `survey_submitted`
// (carrying trust_score/independence_score/privacy_concern/continuation_intent/opt_out)
// and `booking_intent_selected` (dichotomized at Agree/Strongly Agree), per
// experiment_spec.md §4 and §5.
export default function SurveyPage() {
  const router = useRouter();
  const [assignment, setAssignment] = useState<ParticipantAssignment | null>(null);
  const [answers, setAnswers] = useState<LikertAnswers>({});
  const [comprehensionChoice, setComprehensionChoice] = useState<string | null>(null);
  const [freeText, setFreeText] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const startedRef = useRef(false);

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
    if (record.decisionResult == null) {
      router.replace("/action");
      return;
    }
    if (record?.exitedAtAction) {
      // Exited at Page 3 — survey_started must not fire for this participant.
      router.replace("/thank-you?exited=true");
      return;
    }
    // Assignment lives in localStorage, unavailable during server rendering — this is
    // the standard client-only-data-load pattern, not a value derivable during render.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setAssignment(a);

    if (!startedRef.current) {
      startedRef.current = true;
      capture("survey_started", {
        variant: a.variant,
        participant_type: a.participantType,
      });
      if (record) {
        saveCurrentRecord({ ...record, surveyStarted: true });
      }
    }
  }, [router]);

  const comprehension = useMemo(
    () => (assignment ? getComprehensionCheck(assignment.variant) : null),
    [assignment]
  );

  if (!assignment || !comprehension) return null;

  const allAnswered = ALL_SURVEY_ITEMS.every((item) => answers[item.id] != null);
  const canSubmit = allAnswered && comprehensionChoice != null && !submitting;
  const piiWarning = softPiiWarning(freeText);

  function setAnswer(id: string, value: number) {
    setAnswers((prev) => ({ ...prev, [id]: value }));
  }

  function handleSubmit() {
    if (!canSubmit || !assignment) return;
    setSubmitting(true);

    const trustScore = answers["q3"]!;
    const independenceScore = answers["q1"]!;
    const privacyConcern = answers["q4"]!;
    const continuationIntent = answers["q5"]!;
    const paidOptionPreference = answers["q6"]!;
    const selfReportedComprehension = answers["q2"]!;
    const coreBookRecommendScore = answers["q7"]!;
    const coreBookInsuredChoiceScore = answers["q8"]!;
    const comprehensionCorrect =
      comprehension?.options.find((o) => o.id === comprehensionChoice)?.correct ?? false;

    const record = getCurrentRecord();
    const optOut = record?.decisionResult !== "continue";

    capture("survey_submitted", {
      variant: assignment.variant,
      participant_type: assignment.participantType,
      trust_score: trustScore,
      independence_score: independenceScore,
      privacy_concern: privacyConcern,
      continuation_intent: continuationIntent,
      opt_out: optOut,
    });

    if (isIntentPositive(continuationIntent)) {
      capture("booking_intent_selected", {
        variant: assignment.variant,
        participant_type: assignment.participantType,
        continuation_intent: continuationIntent,
      });
    }

    if (record) {
      saveCurrentRecord({
        ...record,
        surveySubmitted: true,
        trustScore,
        independenceScore,
        privacyConcern,
        continuationIntent,
        paidOptionPreference,
        selfReportedComprehension,
        coreBookRecommendScore,
        coreBookInsuredChoiceScore,
        comprehensionCorrect,
        freeText: freeText.slice(0, FREE_TEXT_MAX_LENGTH),
      });
    }

    router.push("/thank-you");
  }

  return (
    <main className="page-shell">
      <span className="eyebrow">Step 4 of 4 — Trust Survey</span>
      <h1>A few quick questions</h1>
      <p>Please respond based on the concept you just saw.</p>

      <div className="card">
        {CORE_ITEMS.map((item) => (
          <div className="likert-item" key={item.id}>
            <p style={{ fontWeight: 600 }}>{item.text}</p>
            <div className="likert-options">
              {LIKERT_LABELS.map((label, idx) => {
                const value = idx + 1;
                return (
                  <label className="likert-option" key={value}>
                    <input
                      type="radio"
                      name={item.id}
                      value={value}
                      checked={answers[item.id] === value}
                      onChange={() => setAnswer(item.id, value)}
                    />
                    {label}
                  </label>
                );
              })}
            </div>
          </div>
        ))}

        <p className="muted" style={{ marginTop: 16, marginBottom: 8 }}>
          The next two questions ask about Legion&apos;s core paid/insured service, not
          just the sponsored concept you saw.
        </p>
        {CORE_BOOK_ITEMS.map((item) => (
          <div className="likert-item" key={item.id}>
            <p style={{ fontWeight: 600 }}>{item.text}</p>
            <div className="likert-options">
              {LIKERT_LABELS.map((label, idx) => {
                const value = idx + 1;
                return (
                  <label className="likert-option" key={value}>
                    <input
                      type="radio"
                      name={item.id}
                      value={value}
                      checked={answers[item.id] === value}
                      onChange={() => setAnswer(item.id, value)}
                    />
                    {label}
                  </label>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3>{comprehension.prompt}</h3>
        <div>
          {comprehension.options.map((opt) => (
            <label className="comprehension-option" key={opt.id}>
              <input
                type="radio"
                name="comprehension"
                value={opt.id}
                checked={comprehensionChoice === opt.id}
                onChange={() => setComprehensionChoice(opt.id)}
              />
              <span>{opt.text}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="card">
        <h3>{FREE_TEXT_PROMPT}</h3>
        <div className="field">
          <textarea
            rows={3}
            maxLength={FREE_TEXT_MAX_LENGTH}
            value={freeText}
            onChange={(e) => setFreeText(e.target.value)}
            placeholder="Optional — do not include personal health information"
          />
          <span className="muted">
            {freeText.length}/{FREE_TEXT_MAX_LENGTH} characters. This response is stored
            for qualitative research only and is never sent to our analytics pipeline.
          </span>
          {piiWarning && (
            <span className="muted" style={{ color: "var(--danger)" }}>
              {piiWarning}
            </span>
          )}
        </div>
      </div>

      <ResearchDisclaimer />

      <div className="button-row">
        <button className="btn btn-primary" disabled={!canSubmit} onClick={handleSubmit}>
          Submit survey
        </button>
      </div>
    </main>
  );
}
