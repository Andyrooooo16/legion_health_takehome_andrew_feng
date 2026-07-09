"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { capture } from "@/lib/analytics";
import { getCapturedRecords } from "@/lib/storage";
import {
  COMPREHENSION_GUARDRAIL,
  CORE_BOOK_SPILLOVER_MARGIN_PP,
  computeDashboardData,
  CONTINUATION_MARGIN_PP,
  INDEPENDENCE_MARGIN_PLACEHOLDER,
  OPT_OUT_FLAG_DELTA_PP,
  PAID_PREFERENCE_STRONG_MAJORITY,
  PRIVACY_CONCERN_FLAG_DELTA,
  TRUST_MARGIN,
  type DashboardData,
} from "@/lib/metrics";
import { buildDashboardCsv, downloadCsv } from "@/lib/csv";
import type { ParticipantRecord, Variant } from "@/lib/types";
import syntheticDataRaw from "@/data/synthetic-participants.json";

const syntheticData = syntheticDataRaw as unknown as ParticipantRecord[];

const VARIANT_LABELS: Record<Variant, string> = {
  control: "Control",
  variant_a: "Variant A (free + sponsor)",
  variant_b: "Variant B (+ separated education)",
  variant_c: "Variant C (visible pharma sponsor)",
};

function pct(n: number): string {
  return Number.isFinite(n) ? `${(n * 100).toFixed(1)}%` : "—";
}

function ciPct(lower: number, upper: number): string {
  return Number.isFinite(lower) && Number.isFinite(upper)
    ? `[${(lower * 100).toFixed(1)}%, ${(upper * 100).toFixed(1)}%]`
    : "—";
}

function num(n: number, digits = 2): string {
  return Number.isFinite(n) ? n.toFixed(digits) : "—";
}

function ciNum(lower: number, upper: number, digits = 2): string {
  return Number.isFinite(lower) && Number.isFinite(upper)
    ? `[${lower.toFixed(digits)}, ${upper.toFixed(digits)}]`
    : "—";
}

function Badge({ label }: { label: "pass" | "fail" | "inconclusive" }) {
  const cls =
    label === "pass" ? "badge-pass" : label === "fail" ? "badge-fail" : "badge-inconclusive";
  return <span className={`badge ${cls}`}>{label}</span>;
}

export default function AdminDashboard() {
  const [realRecords, setRealRecords] = useState<ParticipantRecord[]>([]);
  const [includeSynthetic, setIncludeSynthetic] = useState(true);
  const [exportVariant, setExportVariant] = useState<Variant | "all">("all");
  const firedResultsViewed = useRef(false);

  useEffect(() => {
    // Captured records live in localStorage, unavailable during server rendering —
    // this is the standard client-only-data-load pattern, not a render-derivable value.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setRealRecords(getCapturedRecords());
    if (!firedResultsViewed.current) {
      firedResultsViewed.current = true;
      capture("results_viewed", { participant_type: "admin" });
    }
  }, []);

  const records: ParticipantRecord[] = useMemo(() => {
    return includeSynthetic ? [...syntheticData, ...realRecords] : realRecords;
  }, [includeSynthetic, realRecords]);

  const data: DashboardData = useMemo(() => computeDashboardData(records), [records]);

  const variants: Variant[] = ["control", "variant_a", "variant_b", "variant_c"];

  function handleExport() {
    capture("scenario_exported", { participant_type: "admin", variant: exportVariant });
    const csv = buildDashboardCsv(data, exportVariant);
    downloadCsv(`legion-concept-test-results-${exportVariant}.csv`, csv);
  }

  return (
    <main className="admin-shell">
      <div className="synthetic-banner">
        SYNTHETIC DATA — this dashboard is seeded with fabricated demo data (~90/arm) to
        illustrate the metrics pipeline. It does not represent real patients, real panel
        respondents, or real Legion outcomes.
      </div>

      <div>
        <span className="eyebrow">Admin — Results Dashboard</span>
        <h1>Patient-Side Sponsorship Concept Test</h1>
        <p className="muted">
          {realRecords.length} real (locally captured) record(s) in this browser ·{" "}
          {syntheticData.length} synthetic records available · aggregate reporting only,
          no participant-level drill-down, per experiment_spec.md §8.
        </p>
      </div>

      <div className="card" style={{ display: "flex", flexWrap: "wrap", gap: 16, alignItems: "center" }}>
        <label style={{ display: "flex", gap: 8, alignItems: "center", fontSize: 14 }}>
          <input
            type="checkbox"
            checked={includeSynthetic}
            onChange={(e) => setIncludeSynthetic(e.target.checked)}
          />
          Include synthetic data
        </label>
        <div style={{ display: "flex", gap: 8, alignItems: "center", fontSize: 14 }}>
          Export scope:
          <select
            value={exportVariant}
            onChange={(e) => setExportVariant(e.target.value as Variant | "all")}
            style={{ padding: "6px 8px", borderRadius: 6, border: "1px solid var(--border)" }}
          >
            <option value="all">All variants</option>
            {variants.map((v) => (
              <option key={v} value={v}>
                {VARIANT_LABELS[v]}
              </option>
            ))}
          </select>
          <button className="btn btn-secondary" onClick={handleExport}>
            Export CSV
          </button>
        </div>
      </div>

      <section className="card">
        <h2>Exposure by variant</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Variant</th>
                <th>N exposed</th>
                <th>Continued</th>
                <th>Opted out</th>
                <th>Learn more rate</th>
                <th>Privacy details rate</th>
              </tr>
            </thead>
            <tbody>
              {variants.map((v) => {
                const a = data.arms[v];
                return (
                  <tr key={v}>
                    <td>{VARIANT_LABELS[v]}</td>
                    <td>{a.n}</td>
                    <td>{a.continued}</td>
                    <td>{a.optOut}</td>
                    <td>{pct(a.learnMoreRate)}</td>
                    <td>{pct(a.privacyDetailsRate)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid-2">
        {variants.map((v) => {
          const a = data.arms[v];
          return (
            <div className="card" key={v}>
              <h3>{VARIANT_LABELS[v]}</h3>
              <p className="muted">n = {a.n}</p>
              <div style={{ marginTop: 8 }}>
                <div className="stat-value">{pct(a.continuationRate.point)}</div>
                <div className="stat-ci">
                  continuation rate · 95% CI {ciPct(a.continuationRate.lower, a.continuationRate.upper)}
                </div>
              </div>
              <div style={{ marginTop: 10 }}>
                <div className="stat-value">{num(a.trust.point)} / 5</div>
                <div className="stat-ci">
                  trust score (Q3) · 95% CI {ciNum(a.trust.lower, a.trust.upper)}
                </div>
              </div>
              <div style={{ marginTop: 10 }}>
                <div className="stat-value">{num(a.independence.point)} / 5</div>
                <div className="stat-ci">
                  independence score (Q1) · 95% CI {ciNum(a.independence.lower, a.independence.upper)}
                </div>
              </div>
            </div>
          );
        })}
      </section>

      <section className="card">
        <h2>Primary hypotheses vs. Control (H3a/b/c)</h2>
        <p className="muted">
          Non-inferiority margins per experiment_spec.md §1: continuation 5pp, trust 0.25
          pts. Independence has no lead-approved margin — the spec&apos;s own
          placeholder ({INDEPENDENCE_MARGIN_PLACEHOLDER} pts) is used here and flagged.
          Diff shown is (Control − Variant); positive = decline.
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Variant</th>
                <th>Diff (Control − Variant)</th>
                <th>95% CI</th>
                <th>Margin</th>
                <th>Result</th>
                <th>Directional read</th>
              </tr>
            </thead>
            <tbody>
              {data.vsControl.map((r, i) => (
                <tr key={i}>
                  <td style={{ textTransform: "capitalize" }}>{r.metric}</td>
                  <td>{VARIANT_LABELS[r.variant]}</td>
                  <td>
                    {r.metric === "continuation" ? pct(r.diff.point) : num(r.diff.point)}
                  </td>
                  <td>
                    {r.metric === "continuation"
                      ? ciPct(r.diff.lower, r.diff.upper)
                      : ciNum(r.diff.lower, r.diff.upper)}
                  </td>
                  <td>{r.metric === "continuation" ? pct(r.margin) : num(r.margin)}</td>
                  <td>
                    <Badge label={r.label} />
                  </td>
                  <td>{r.directionalRead}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="muted" style={{ marginTop: 10 }}>
          Per §7, a 75–100/arm discovery test is generally underpowered to statistically
          confirm these margins — expect most results to read &quot;inconclusive&quot;
          even when a real effect exists. Treat non-&quot;pass&quot; results as
          directional, not confirmatory, and see §7 before treating any &quot;pass&quot;
          as a validated non-inferiority claim.
        </p>
      </section>

      <section className="grid-2">
        <div className="card">
          <h2>Privacy concern (descriptive guardrail)</h2>
          <p className="muted">
            No lead-approved numeric threshold (spec Recommendations #2). Prototype flags
            a variant if its mean privacy concern exceeds Control&apos;s by more than{" "}
            {PRIVACY_CONCERN_FLAG_DELTA} points — an unconfirmed operational definition.
          </p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Variant</th>
                  <th>Mean (1-5)</th>
                  <th>95% CI</th>
                  <th>Δ vs Control</th>
                  <th>Flag</th>
                </tr>
              </thead>
              <tbody>
                {variants.map((v) => {
                  const a = data.arms[v];
                  const flag = data.privacyFlags.find((f) => f.variant === v);
                  return (
                    <tr key={v}>
                      <td>{VARIANT_LABELS[v]}</td>
                      <td>{num(a.privacyConcern.point)}</td>
                      <td>{ciNum(a.privacyConcern.lower, a.privacyConcern.upper)}</td>
                      <td>{flag ? num(flag.delta) : "—"}</td>
                      <td>{flag?.flagged ? "⚠ flagged" : "—"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <h2>Opt-out rate (guardrail)</h2>
          <p className="muted">
            No lead-approved numeric threshold. Prototype flags a variant if its opt-out
            rate exceeds Control&apos;s by more than {pct(OPT_OUT_FLAG_DELTA_PP)} — an
            unconfirmed operational definition.
          </p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Variant</th>
                  <th>Rate</th>
                  <th>95% CI</th>
                  <th>Δ vs Control (pp)</th>
                  <th>Flag</th>
                </tr>
              </thead>
              <tbody>
                {variants.map((v) => {
                  const a = data.arms[v];
                  const flag = data.optOutFlags.find((f) => f.variant === v);
                  return (
                    <tr key={v}>
                      <td>{VARIANT_LABELS[v]}</td>
                      <td>{pct(a.optOutRate.point)}</td>
                      <td>{ciPct(a.optOutRate.lower, a.optOutRate.upper)}</td>
                      <td>{flag ? pct(flag.deltaPp) : "—"}</td>
                      <td>{flag?.flagged ? "⚠ flagged" : "—"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="grid-2">
        <div className="card">
          <h2>Disclosure comprehension (hard guardrail: ≥{pct(COMPREHENSION_GUARDRAIL)})</h2>
          <p className="muted">
            Factual comprehension check, scored correct/incorrect — the only guardrail with
            a lead-approved numeric threshold (spec §1).
          </p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Variant</th>
                  <th>Correct rate</th>
                  <th>95% CI</th>
                  <th>Pass ≥80%?</th>
                </tr>
              </thead>
              <tbody>
                {variants.map((v) => {
                  const a = data.arms[v];
                  return (
                    <tr key={v}>
                      <td>{VARIANT_LABELS[v]}</td>
                      <td>{pct(a.comprehensionRate.point)}</td>
                      <td>{ciPct(a.comprehensionRate.lower, a.comprehensionRate.upper)}</td>
                      <td>{a.comprehensionPasses ? "✓ pass" : "✗ fail"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <h2>Preference for paid sponsor-free option</h2>
          <p className="muted">
            Guardrail: flagged if a strong majority (spec&apos;s own unconfirmed starting
            point: &gt;{pct(PAID_PREFERENCE_STRONG_MAJORITY)}) prefer paying (Q6
            Agree/Strongly Agree).
          </p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Variant</th>
                  <th>Agree/Strongly Agree rate</th>
                  <th>95% CI</th>
                  <th>Flag</th>
                </tr>
              </thead>
              <tbody>
                {variants.map((v) => {
                  const a = data.arms[v];
                  return (
                    <tr key={v}>
                      <td>{VARIANT_LABELS[v]}</td>
                      <td>{pct(a.paidPreferenceRate.point)}</td>
                      <td>{ciPct(a.paidPreferenceRate.lower, a.paidPreferenceRate.upper)}</td>
                      <td>{a.paidPreferenceFlag ? "⚠ flagged" : "—"}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Core-book trust spillover (A26 proxy guardrail)</h2>
        <p className="muted">
          Per experiment_spec.md §1 (post-red-team): flags if Q7 or Q8 Agree/Strongly
          Agree rate drops ≥{pct(CORE_BOOK_SPILLOVER_MARGIN_PP)} vs. Control. Q7/Q8 are
          local-only (not sent to PostHog).
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Variant</th>
                <th>Metric</th>
                <th>Control rate</th>
                <th>Variant rate</th>
                <th>Drop (pp)</th>
                <th>Flag</th>
              </tr>
            </thead>
            <tbody>
              {data.coreBookSpilloverFlags.map((f, i) => (
                <tr key={i}>
                  <td>{VARIANT_LABELS[f.variant]}</td>
                  <td>{f.metric === "recommend" ? "Q7 recommend" : "Q8 insured choice"}</td>
                  <td>{pct(f.controlRate)}</td>
                  <td>{pct(f.variantRate)}</td>
                  <td>{pct(f.dropPp)}</td>
                  <td>{f.flagged ? "⚠ flagged" : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h2>Booking / continuation intent (stated) vs. behavioral continuation</h2>
        <p className="muted">
          Compares the behavioral action (Page 3 &quot;Continue&quot;) against stated
          intent (Survey Q5, dichotomized Agree/Strongly Agree), per §4&apos;s note that
          both are logged to compare revealed vs. stated continuation.
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Variant</th>
                <th>Behavioral continuation rate</th>
                <th>Stated intent-positive rate</th>
              </tr>
            </thead>
            <tbody>
              {variants.map((v) => {
                const a = data.arms[v];
                return (
                  <tr key={v}>
                    <td>{VARIANT_LABELS[v]}</td>
                    <td>{pct(a.continuationRate.point)}</td>
                    <td>{pct(a.continuationIntentPositiveRate.point)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <h2>Reliability check: Q1 (independence) vs. Q3 (trust)</h2>
        <p className="muted">
          Per §5&apos;s scoring note, trust_score and independence_score are each scored
          from a single item; correlating them is a lightweight reliability sanity check,
          not a redefinition of either metric.
        </p>
        <div className="stat-value">r = {num(data.reliability.qCorrelationR, 2)}</div>
        <div className="stat-ci">n = {data.reliability.n}</div>
      </section>

      <p className="muted">
        Margins shown: continuation {pct(CONTINUATION_MARGIN_PP)}, trust {TRUST_MARGIN} pts
        (provisional, per brief §22 as elaborated in experiment_spec.md §1).
      </p>
    </main>
  );
}
