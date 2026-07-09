// Shared types for the patient-side sponsorship concept test.
// These types mirror experiment_spec.md §4 (PostHog integration contract) and §5 (survey instrument).
// Do not add fields beyond what the spec allows for analytics properties — see analytics.ts.

export type Variant = "control" | "variant_a" | "variant_b" | "variant_c";

export type SponsorCategory = "none" | "consumer_health" | "pharma";

export type ParticipantType = "panel" | "landing_page" | "admin";

export type DecisionResult = "continue" | "opt_out" | "exit";

/** A fully-resolved participant assignment, established once per distinct_id and persisted (sticky). */
export interface ParticipantAssignment {
  distinctId: string;
  variant: Variant;
  sponsorCategory: SponsorCategory;
  participantType: ParticipantType;
}

/**
 * Full local record of one participant's journey through the flow.
 * This is the prototype's own local "database" (localStorage) — separate from the
 * restricted PostHog property list in analytics.ts. It intentionally holds a few
 * fields (Q2 self-report, Q6 paid-option preference, comprehension check, free text)
 * that experiment_spec.md §5 says should NOT be added as new PostHog properties,
 * but still need to be captured somewhere for the admin dashboard's descriptive stats.
 */
export interface ParticipantRecord {
  distinctId: string;
  variant: Variant;
  sponsorCategory: SponsorCategory;
  participantType: ParticipantType;
  createdAt: string;
  updatedAt: string;

  exposed: boolean; // concept_viewed fired
  learnMoreClicked: boolean;
  privacyDetailsOpened: boolean;

  decisionResult?: DecisionResult;
  optOut: boolean;
  exitedAtAction: boolean; // true only for the "Exit" terminal action (skips survey)

  surveyStarted: boolean;
  surveySubmitted: boolean;

  // Scored / mapped survey properties (also sent to PostHog on survey_submitted per spec §4)
  trustScore?: number; // Q3
  independenceScore?: number; // Q1
  privacyConcern?: number; // Q4
  continuationIntent?: number; // Q5

  // Local-only fields (NOT sent to PostHog — see event_schema.md "privacy classification")
  selfReportedComprehension?: number; // Q2 (supporting signal only)
  paidOptionPreference?: number; // Q6
  coreBookRecommendScore?: number; // Q7 (A26 proxy)
  coreBookInsuredChoiceScore?: number; // Q8 (A26 proxy)
  comprehensionCorrect?: boolean; // factual comprehension check
  freeText?: string; // optional, capped, no-PHI-by-instruction

  isSynthetic?: boolean;
}

/** Allowed PostHog property keys, per experiment_spec.md §4. Nothing else may be attached to an event. */
export interface AllowedProperties {
  variant?: Variant;
  sponsor_category?: SponsorCategory;
  participant_type?: ParticipantType;
  decision_result?: DecisionResult;
  trust_score?: number;
  independence_score?: number;
  privacy_concern?: number;
  continuation_intent?: number;
  opt_out?: boolean;
}
