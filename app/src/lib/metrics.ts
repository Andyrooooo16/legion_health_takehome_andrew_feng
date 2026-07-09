// Aggregation layer for the admin dashboard: turns a flat array of ParticipantRecord
// into the per-arm metrics required by experiment_spec.md §1 (guardrails) and §6
// (analysis plan), including non-inferiority decision labels vs. Control.

import type { ParticipantRecord, Variant } from "./types";
import {
  cohensD,
  decisionLabel,
  directionalRead,
  meanDiffInterval,
  meanInterval,
  newcombeDiffInterval,
  pearsonR,
  wilsonInterval,
  type Interval,
} from "./stats";
import { VARIANT_ORDER } from "./variants";

// Provisional non-inferiority margins, per experiment_spec.md §1.
export const CONTINUATION_MARGIN_PP = 0.05; // 5 percentage points
export const TRUST_MARGIN = 0.25; // 5-point scale
// H3c has NO lead-approved numeric margin (spec §1/§Recommendations #1). Reusing the
// trust margin as a flagged placeholder, exactly as the spec's own recommendation does.
export const INDEPENDENCE_MARGIN_PLACEHOLDER = 0.25;

// Prototype-only operational thresholds for guardrails the spec leaves unquantified
// (§1 and Recommendations #2). NOT lead-approved — flagged in prototype_readme.md.
export const COMPREHENSION_GUARDRAIL = 0.8; // spec-defined (only guardrail with a hard number)
export const PAID_PREFERENCE_STRONG_MAJORITY = 0.5; // spec's own proposed starting point
export const PRIVACY_CONCERN_FLAG_DELTA = 0.5; // prototype-only heuristic
export const OPT_OUT_FLAG_DELTA_PP = 0.1; // prototype-only heuristic (10pp)

export const CORE_BOOK_SPILLOVER_MARGIN_PP = 0.05; // experiment_spec.md §1 A26 proxy

export interface ArmMetrics {
  variant: Variant;
  n: number;
  exposed: number;
  continued: number;
  continuationRate: Interval;
  optOut: number;
  optOutRate: Interval;
  trust: Interval & { sd: number };
  independence: Interval & { sd: number };
  privacyConcern: Interval & { sd: number };
  continuationIntentPositiveRate: Interval;
  comprehensionCorrectCount: number;
  comprehensionN: number;
  comprehensionRate: Interval;
  comprehensionPasses: boolean;
  paidPreferenceAgreeCount: number;
  paidPreferenceN: number;
  paidPreferenceRate: Interval;
  paidPreferenceFlag: boolean;
  coreBookRecommendPositiveRate: Interval;
  coreBookInsuredChoicePositiveRate: Interval;
  learnMoreRate: number;
  privacyDetailsRate: number;
}

export interface VsControlResult {
  variant: Variant;
  metric: "continuation" | "trust" | "independence";
  diff: Interval; // Control - Variant
  margin: number;
  label: ReturnType<typeof decisionLabel>;
  directionalRead: string;
  cohensD?: number;
}

export interface DashboardData {
  arms: Record<Variant, ArmMetrics>;
  vsControl: VsControlResult[];
  reliability: { qCorrelationR: number; n: number };
  privacyFlags: { variant: Variant; flagged: boolean; delta: number }[];
  optOutFlags: { variant: Variant; flagged: boolean; deltaPp: number }[];
  coreBookSpilloverFlags: {
    variant: Variant;
    metric: "recommend" | "insured_choice";
    controlRate: number;
    variantRate: number;
    dropPp: number;
    flagged: boolean;
  }[];
}

function computeArmMetrics(variant: Variant, records: ParticipantRecord[]): ArmMetrics {
  const exposed = records.filter((r) => r.exposed);
  const n = exposed.length;
  const continued = exposed.filter((r) => r.decisionResult === "continue").length;
  const optOut = exposed.filter((r) => r.optOut).length;

  const surveyed = exposed.filter((r) => r.surveySubmitted);
  const trustVals = surveyed.map((r) => r.trustScore).filter((v): v is number => v != null);
  const indepVals = surveyed
    .map((r) => r.independenceScore)
    .filter((v): v is number => v != null);
  const privacyVals = surveyed
    .map((r) => r.privacyConcern)
    .filter((v): v is number => v != null);
  const intentVals = surveyed
    .map((r) => r.continuationIntent)
    .filter((v): v is number => v != null);
  const intentPositive = intentVals.filter((v) => v >= 4).length;

  const comprehensionVals = surveyed.filter((r) => r.comprehensionCorrect != null);
  const comprehensionCorrectCount = comprehensionVals.filter(
    (r) => r.comprehensionCorrect
  ).length;

  const paidVals = surveyed
    .map((r) => r.paidOptionPreference)
    .filter((v): v is number => v != null);
  const paidAgreeCount = paidVals.filter((v) => v >= 4).length;

  const recommendVals = surveyed
    .map((r) => r.coreBookRecommendScore)
    .filter((v): v is number => v != null);
  const insuredVals = surveyed
    .map((r) => r.coreBookInsuredChoiceScore)
    .filter((v): v is number => v != null);
  const recommendPositive = recommendVals.filter((v) => v >= 4).length;
  const insuredPositive = insuredVals.filter((v) => v >= 4).length;

  const trustI = meanInterval(trustVals);
  const indepI = meanInterval(indepVals);
  const privacyI = meanInterval(privacyVals);

  return {
    variant,
    n,
    exposed: n,
    continued,
    continuationRate: wilsonInterval(continued, n),
    optOut,
    optOutRate: wilsonInterval(optOut, n),
    trust: { ...trustI, sd: stdDev(trustVals) },
    independence: { ...indepI, sd: stdDev(indepVals) },
    privacyConcern: { ...privacyI, sd: stdDev(privacyVals) },
    continuationIntentPositiveRate: wilsonInterval(intentPositive, intentVals.length || 1),
    comprehensionCorrectCount,
    comprehensionN: comprehensionVals.length,
    comprehensionRate: wilsonInterval(comprehensionCorrectCount, comprehensionVals.length || 1),
    comprehensionPasses:
      comprehensionVals.length > 0 &&
      comprehensionCorrectCount / comprehensionVals.length >= COMPREHENSION_GUARDRAIL,
    paidPreferenceAgreeCount: paidAgreeCount,
    paidPreferenceN: paidVals.length,
    paidPreferenceRate: wilsonInterval(paidAgreeCount, paidVals.length || 1),
    paidPreferenceFlag:
      paidVals.length > 0 &&
      paidAgreeCount / paidVals.length > PAID_PREFERENCE_STRONG_MAJORITY,
    coreBookRecommendPositiveRate: wilsonInterval(
      recommendPositive,
      recommendVals.length || 1
    ),
    coreBookInsuredChoicePositiveRate: wilsonInterval(
      insuredPositive,
      insuredVals.length || 1
    ),
    learnMoreRate: n ? exposed.filter((r) => r.learnMoreClicked).length / n : 0,
    privacyDetailsRate: n ? exposed.filter((r) => r.privacyDetailsOpened).length / n : 0,
  };
}

function stdDev(values: number[]): number {
  const n = values.length;
  if (n < 2) return 0;
  const mean = values.reduce((a, b) => a + b, 0) / n;
  return Math.sqrt(values.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1));
}

export function computeDashboardData(records: ParticipantRecord[]): DashboardData {
  const byVariant = (v: Variant) => records.filter((r) => r.variant === v);

  const arms = Object.fromEntries(
    VARIANT_ORDER.map((v) => [v, computeArmMetrics(v, byVariant(v))])
  ) as Record<Variant, ArmMetrics>;

  const controlExposed = byVariant("control").filter((r) => r.exposed);
  const controlSurveyed = controlExposed.filter((r) => r.surveySubmitted);
  const controlContinued = controlExposed.filter((r) => r.decisionResult === "continue").length;
  const controlTrust = controlSurveyed
    .map((r) => r.trustScore)
    .filter((v): v is number => v != null);
  const controlIndep = controlSurveyed
    .map((r) => r.independenceScore)
    .filter((v): v is number => v != null);

  const vsControl: VsControlResult[] = [];
  (["variant_a", "variant_b", "variant_c"] as Variant[]).forEach((variant) => {
    const vExposed = byVariant(variant).filter((r) => r.exposed);
    const vSurveyed = vExposed.filter((r) => r.surveySubmitted);
    const vContinued = vExposed.filter((r) => r.decisionResult === "continue").length;
    const vTrust = vSurveyed.map((r) => r.trustScore).filter((v): v is number => v != null);
    const vIndep = vSurveyed
      .map((r) => r.independenceScore)
      .filter((v): v is number => v != null);

    // Continuation: diff = Control - Variant (positive = decline)
    const contDiff = newcombeDiffInterval(
      controlContinued,
      controlExposed.length,
      vContinued,
      vExposed.length
    );
    vsControl.push({
      variant,
      metric: "continuation",
      diff: contDiff,
      margin: CONTINUATION_MARGIN_PP,
      label: decisionLabel(contDiff, CONTINUATION_MARGIN_PP),
      directionalRead: directionalRead(contDiff.point, CONTINUATION_MARGIN_PP),
    });

    // Trust: diff = Control - Variant
    const trustDiff = meanDiffInterval(controlTrust, vTrust);
    vsControl.push({
      variant,
      metric: "trust",
      diff: trustDiff,
      margin: TRUST_MARGIN,
      label: decisionLabel(trustDiff, TRUST_MARGIN),
      directionalRead: directionalRead(trustDiff.point, TRUST_MARGIN),
      cohensD: cohensD(controlTrust, vTrust),
    });

    // Independence: diff = Control - Variant (placeholder margin, flagged)
    const indepDiff = meanDiffInterval(controlIndep, vIndep);
    vsControl.push({
      variant,
      metric: "independence",
      diff: indepDiff,
      margin: INDEPENDENCE_MARGIN_PLACEHOLDER,
      label: decisionLabel(indepDiff, INDEPENDENCE_MARGIN_PLACEHOLDER),
      directionalRead: directionalRead(indepDiff.point, INDEPENDENCE_MARGIN_PLACEHOLDER),
      cohensD: cohensD(controlIndep, vIndep),
    });
  });

  // Reliability check per §5 scoring note: correlation between Q1 (independence_score)
  // and Q3 (trust_score) across all surveyed participants.
  const allSurveyed = records.filter((r) => r.surveySubmitted);
  const q1 = allSurveyed.map((r) => r.independenceScore).filter((v): v is number => v != null);
  const q3 = allSurveyed.map((r) => r.trustScore).filter((v): v is number => v != null);
  const reliability = { qCorrelationR: pearsonR(q1, q3), n: Math.min(q1.length, q3.length) };

  const controlPrivacy = meanStatsSimple(
    controlSurveyed.map((r) => r.privacyConcern).filter((v): v is number => v != null)
  );
  const controlOptOutRate = controlExposed.length
    ? controlExposed.filter((r) => r.optOut).length / controlExposed.length
    : 0;

  const privacyFlags = (["variant_a", "variant_b", "variant_c"] as Variant[]).map((variant) => {
    const delta = arms[variant].privacyConcern.point - controlPrivacy;
    return { variant, flagged: delta > PRIVACY_CONCERN_FLAG_DELTA, delta };
  });

  const optOutFlags = (["variant_a", "variant_b", "variant_c"] as Variant[]).map((variant) => {
    const deltaPp = arms[variant].optOutRate.point - controlOptOutRate;
    return { variant, flagged: deltaPp > OPT_OUT_FLAG_DELTA_PP, deltaPp };
  });

  const controlRecommendRate = arms.control.coreBookRecommendPositiveRate.point;
  const controlInsuredRate = arms.control.coreBookInsuredChoicePositiveRate.point;
  const coreBookSpilloverFlags: DashboardData["coreBookSpilloverFlags"] = [];
  (["variant_a", "variant_b", "variant_c"] as Variant[]).forEach((variant) => {
    const recommendRate = arms[variant].coreBookRecommendPositiveRate.point;
    const insuredRate = arms[variant].coreBookInsuredChoicePositiveRate.point;
    const recommendDrop = controlRecommendRate - recommendRate;
    const insuredDrop = controlInsuredRate - insuredRate;
    coreBookSpilloverFlags.push({
      variant,
      metric: "recommend",
      controlRate: controlRecommendRate,
      variantRate: recommendRate,
      dropPp: recommendDrop,
      flagged: recommendDrop >= CORE_BOOK_SPILLOVER_MARGIN_PP,
    });
    coreBookSpilloverFlags.push({
      variant,
      metric: "insured_choice",
      controlRate: controlInsuredRate,
      variantRate: insuredRate,
      dropPp: insuredDrop,
      flagged: insuredDrop >= CORE_BOOK_SPILLOVER_MARGIN_PP,
    });
  });

  return { arms, vsControl, reliability, privacyFlags, optOutFlags, coreBookSpilloverFlags };
}

function meanStatsSimple(values: number[]): number {
  if (!values.length) return NaN;
  return values.reduce((a, b) => a + b, 0) / values.length;
}
