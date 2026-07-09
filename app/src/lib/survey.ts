// Survey instrument, verbatim from experiment_spec.md §5, plus the flagged
// disclosure-comprehension addition. Scoring mapping matches the spec's "Scoring note"
// exactly: trust_score <- Q3, independence_score <- Q1, privacy_concern <- Q4,
// continuation_intent <- Q5. Q2, Q6, and the comprehension check are NOT sent to
// PostHog (see analytics.ts / event_schema.md) but are retained locally for the
// admin dashboard's descriptive/guardrail stats.

import type { Variant } from "./types";

export const LIKERT_LABELS = [
  "Strongly Disagree",
  "Disagree",
  "Neutral",
  "Agree",
  "Strongly Agree",
] as const;

export interface LikertItem {
  id: "q1" | "q2" | "q3" | "q4" | "q5" | "q6" | "q7" | "q8";
  text: string;
  mapsTo: string;
}

export const CORE_ITEMS: LikertItem[] = [
  {
    id: "q1",
    text: "I trust Legion to make independent clinical decisions",
    mapsTo: "independence_score",
  },
  {
    id: "q2",
    text: "I understand the sponsor's role",
    mapsTo: "self-reported comprehension (supporting signal only)",
  },
  {
    id: "q3",
    text: "I am comfortable with sponsor-supported care",
    mapsTo: "trust_score (primary component)",
  },
  {
    id: "q4",
    text: "I am concerned about my data being shared",
    mapsTo: "privacy_concern",
  },
  {
    id: "q5",
    text: "I would continue using the service",
    mapsTo: "continuation_intent",
  },
  {
    id: "q6",
    text: "I would prefer a paid sponsor-free option",
    mapsTo: "guardrail: preference for paid option (local-only)",
  },
];

/** Core-book contagion proxy items (experiment_spec.md §5, post-red-team A26). Local-only. */
export const CORE_BOOK_ITEMS: LikertItem[] = [
  {
    id: "q7",
    text: "I would recommend Legion to a friend who pays full price for visits",
    mapsTo: "core-book spillover proxy (A26)",
  },
  {
    id: "q8",
    text: "If I had insurance coverage, I would still choose Legion for my psychiatric visits",
    mapsTo: "core-book spillover proxy (A26)",
  },
];

export const ALL_SURVEY_ITEMS: LikertItem[] = [...CORE_ITEMS, ...CORE_BOOK_ITEMS];

export interface ComprehensionOption {
  id: "a" | "b" | "c" | "d";
  text: string;
  correct: boolean;
}

/**
 * Disclosure-comprehension check, per §5. For Control (no sponsor), the spec flags
 * that the sponsor-framed question doesn't apply and recommends (unconfirmed by the
 * lead) substituting a parallel question about the "affordable care, no sponsorship"
 * framing, to keep the funnel structurally comparable. That recommendation is what's
 * implemented below — flagged again in prototype_readme.md as a spec ambiguity.
 */
export function getComprehensionCheck(variant: Variant): {
  prompt: string;
  options: ComprehensionOption[];
} {
  if (variant === "control") {
    return {
      prompt:
        "Based on what you just saw, which of the following is true?",
      options: [
        {
          id: "a",
          text: "A sponsor pays for part of my care but does not see my health information",
          correct: false,
        },
        {
          id: "b",
          text: "No sponsor is involved — care is funded through standard fees/insurance, and no data is shared for sponsorship purposes",
          correct: true,
        },
        {
          id: "c",
          text: "A sponsor's staff can review my treatment plan",
          correct: false,
        },
        { id: "d", text: "I am not sure", correct: false },
      ],
    };
  }
  return {
    prompt: "Based on what you just saw, which of the following is true?",
    options: [
      {
        id: "a",
        text: "Legion shares my personal health information with the sponsor",
        correct: false,
      },
      {
        id: "b",
        text: "The sponsor pays to support access to care, but does not see my personal health information or influence my treatment",
        correct: true,
      },
      {
        id: "c",
        text: "The sponsor's staff can review my treatment plan",
        correct: false,
      },
      { id: "d", text: "I am not sure", correct: false },
    ],
  };
}

export const FREE_TEXT_MAX_LENGTH = 280;

export const FREE_TEXT_PROMPT =
  "Any concerns about this concept? (Please do not include any personal health information.)";

/** Very-soft, non-compliance-grade nudge filter — see experiment_spec.md §5 caveat. */
const SOFT_PII_KEYWORDS = [
  "diagnos",
  "medication",
  "my ssn",
  "social security",
  "date of birth",
];

export function softPiiWarning(text: string): string | null {
  const lower = text.toLowerCase();
  const hit = SOFT_PII_KEYWORDS.find((k) => lower.includes(k));
  if (hit) {
    return "This looks like it might contain personal health information. Please remove it before submitting (this is a soft reminder, not a compliance filter).";
  }
  return null;
}

/** Dichotomization rule from experiment_spec.md §4: Agree/Strongly Agree (>=4) = intent-positive. */
export function isIntentPositive(continuationIntent: number): boolean {
  return continuationIntent >= 4;
}
