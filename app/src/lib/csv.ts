"use client";

import type { DashboardData } from "./metrics";
import type { Variant } from "./types";

function fmt(n: number, digits = 3): string {
  return Number.isFinite(n) ? n.toFixed(digits) : "";
}

/** Builds an aggregate per-arm CSV of the dashboard metrics (no participant-level rows,
 * per experiment_spec.md §8 "Aggregate reporting only ... no participant-level drill-down"). */
export function buildDashboardCsv(data: DashboardData, variantFilter: Variant | "all"): string {
  const rows: string[][] = [];
  rows.push([
    "variant",
    "n_exposed",
    "continuation_rate",
    "continuation_rate_ci_low",
    "continuation_rate_ci_high",
    "opt_out_rate",
    "opt_out_rate_ci_low",
    "opt_out_rate_ci_high",
    "trust_mean",
    "trust_ci_low",
    "trust_ci_high",
    "independence_mean",
    "independence_ci_low",
    "independence_ci_high",
    "privacy_concern_mean",
    "privacy_concern_ci_low",
    "privacy_concern_ci_high",
    "booking_intent_positive_rate",
    "disclosure_comprehension_rate",
    "disclosure_comprehension_pass_80pct",
    "paid_option_preference_rate",
    "paid_option_strong_majority_flag",
  ]);

  const variants: Variant[] =
    variantFilter === "all"
      ? (["control", "variant_a", "variant_b", "variant_c"] as Variant[])
      : [variantFilter];

  variants.forEach((v) => {
    const a = data.arms[v];
    rows.push([
      v,
      String(a.n),
      fmt(a.continuationRate.point),
      fmt(a.continuationRate.lower),
      fmt(a.continuationRate.upper),
      fmt(a.optOutRate.point),
      fmt(a.optOutRate.lower),
      fmt(a.optOutRate.upper),
      fmt(a.trust.point),
      fmt(a.trust.lower),
      fmt(a.trust.upper),
      fmt(a.independence.point),
      fmt(a.independence.lower),
      fmt(a.independence.upper),
      fmt(a.privacyConcern.point),
      fmt(a.privacyConcern.lower),
      fmt(a.privacyConcern.upper),
      fmt(a.continuationIntentPositiveRate.point),
      fmt(a.comprehensionRate.point),
      String(a.comprehensionPasses),
      fmt(a.paidPreferenceRate.point),
      String(a.paidPreferenceFlag),
    ]);
  });

  rows.push([]);
  rows.push(["vs_control_metric", "variant", "diff_control_minus_variant", "ci_low", "ci_high", "margin", "label", "directional_read"]);
  data.vsControl
    .filter((r) => variantFilter === "all" || r.variant === variantFilter)
    .forEach((r) => {
      rows.push([
        r.metric,
        r.variant,
        fmt(r.diff.point),
        fmt(r.diff.lower),
        fmt(r.diff.upper),
        String(r.margin),
        r.label,
        r.directionalRead,
      ]);
    });

  return rows.map((r) => r.map(csvEscape).join(",")).join("\n");
}

function csvEscape(value: string): string {
  if (/[",\n]/.test(value)) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

export function downloadCsv(filename: string, csv: string): void {
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
