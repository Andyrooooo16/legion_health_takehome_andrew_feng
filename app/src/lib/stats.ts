// Statistics helpers for the admin dashboard, per experiment_spec.md §6 (Analysis Plan).
// Implements: Wilson score interval (proportions), Newcombe interval (difference of two
// proportions), normal-approximation interval (difference of two means), and the
// Pass / Fail / Inconclusive decision mapping defined in §6's "Decision mapping" table.

const Z_95 = 1.96;

export interface Interval {
  point: number;
  lower: number;
  upper: number;
}

/** Wilson score interval for a single proportion. More robust than a normal approx at small n. */
export function wilsonInterval(successes: number, n: number, z = Z_95): Interval {
  if (n === 0) return { point: NaN, lower: NaN, upper: NaN };
  const p = successes / n;
  const denom = 1 + (z * z) / n;
  const center = p + (z * z) / (2 * n);
  const margin = z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n));
  return {
    point: p,
    lower: Math.max(0, (center - margin) / denom),
    upper: Math.min(1, (center + margin) / denom),
  };
}

/**
 * Newcombe (1998) hybrid score interval for the difference of two independent
 * proportions (p1 - p2), built from each arm's Wilson interval. Per §6, this is
 * preferred over a simple normal approximation, especially at discovery-scale n.
 */
export function newcombeDiffInterval(
  successes1: number,
  n1: number,
  successes2: number,
  n2: number,
  z = Z_95
): Interval {
  const p1 = successes1 / n1;
  const p2 = successes2 / n2;
  const w1 = wilsonInterval(successes1, n1, z);
  const w2 = wilsonInterval(successes2, n2, z);
  const diff = p1 - p2;
  const lower = diff - Math.sqrt((p1 - w1.lower) ** 2 + (w2.upper - p2) ** 2);
  const upper = diff + Math.sqrt((w1.upper - p1) ** 2 + (p2 - w2.lower) ** 2);
  return { point: diff, lower, upper };
}

export interface MeanStats {
  mean: number;
  sd: number;
  n: number;
  se: number;
}

export function meanStats(values: number[]): MeanStats {
  const n = values.length;
  if (n === 0) return { mean: NaN, sd: NaN, n: 0, se: NaN };
  const mean = values.reduce((a, b) => a + b, 0) / n;
  const variance =
    n > 1
      ? values.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1)
      : 0;
  const sd = Math.sqrt(variance);
  const se = n > 0 ? sd / Math.sqrt(n) : NaN;
  return { mean, sd, n, se };
}

/** CI on a single mean, normal approximation (adequate for Likert-ish n>=30 per arm). */
export function meanInterval(values: number[], z = Z_95): Interval {
  const { mean, se } = meanStats(values);
  return { point: mean, lower: mean - z * se, upper: mean + z * se };
}

/**
 * CI on the difference of two independent means (Welch-style normal approximation:
 * combines each group's own SE rather than assuming equal variance).
 */
export function meanDiffInterval(a: number[], b: number[], z = Z_95): Interval {
  const sa = meanStats(a);
  const sb = meanStats(b);
  const diff = sa.mean - sb.mean;
  const se = Math.sqrt(sa.se ** 2 + sb.se ** 2);
  return { point: diff, lower: diff - z * se, upper: diff + z * se };
}

/** Cohen's d for two independent samples (pooled SD), reported alongside mean diff per §6. */
export function cohensD(a: number[], b: number[]): number {
  const sa = meanStats(a);
  const sb = meanStats(b);
  const pooledSd = Math.sqrt(
    ((sa.n - 1) * sa.sd ** 2 + (sb.n - 1) * sb.sd ** 2) / (sa.n + sb.n - 2)
  );
  if (!pooledSd) return NaN;
  return (sa.mean - sb.mean) / pooledSd;
}

/** Pearson correlation coefficient — used for the Q1/Q3 (independence vs trust) reliability check. */
export function pearsonR(a: number[], b: number[]): number {
  const n = Math.min(a.length, b.length);
  if (n < 2) return NaN;
  const meanA = a.slice(0, n).reduce((x, y) => x + y, 0) / n;
  const meanB = b.slice(0, n).reduce((x, y) => x + y, 0) / n;
  let num = 0;
  let denomA = 0;
  let denomB = 0;
  for (let i = 0; i < n; i++) {
    const da = a[i] - meanA;
    const db = b[i] - meanB;
    num += da * db;
    denomA += da * da;
    denomB += db * db;
  }
  const denom = Math.sqrt(denomA * denomB);
  return denom === 0 ? NaN : num / denom;
}

export type DecisionLabel = "pass" | "fail" | "inconclusive";

/**
 * Decision mapping per experiment_spec.md §6:
 *  - Pass: upper bound of CI for (Control - Variant) is below the margin.
 *  - Fail: point + CI show decline meets/exceeds margin (lower bound >= margin).
 *  - Inconclusive: CI straddles the margin.
 * `diffCi` must be computed as (Control - Variant), i.e. positive = decline.
 */
export function decisionLabel(diffCi: Interval, margin: number): DecisionLabel {
  if (diffCi.upper < margin) return "pass";
  if (diffCi.lower >= margin) return "fail";
  return "inconclusive";
}

/**
 * Directional read, independent of statistical confirmation — per §6's guidance that
 * an inconclusive statistical result should still be described with a directional read
 * ("underpowered to conclude; directional read is [X]") rather than reported as safe.
 * Purely descriptive; thresholds here are prototype heuristics, not spec-defined.
 */
export function directionalRead(pointDiff: number, margin: number): string {
  if (pointDiff <= 0) return "no decline (variant >= control)";
  if (pointDiff < margin) return "no meaningful difference";
  if (pointDiff < margin * 2) return "directionally concerning";
  return "large / concerning decline";
}
