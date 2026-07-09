# 30 Day Validation Plan

**Objective:** resolve the open questions on the **literal ads/sponsorship prompt** and the **underwriting adjacent path** — **before Legion's patient base scales** — for low tens of thousands of dollars. This is **not** a test to reach $1B in 30 days. It is a test to decide whether to invest in a sponsorship co-funder layer and/or employer underwriting as the company grows from ~3K toward ~50K+ actives.

**What this test validates for ads/sponsorship specifically:**
- **Sponsor WTP interviews** (Packages A/B/C): could brand partnerships pay enough to co-fund free care? Kill criterion: median WTP &lt; $100/patient.
- **Patient trust survey:** will sponsor framing harm the brand as you scale?
- **No programmatic ad pilot:** base-case per-patient gap ~50x; ads contribute &lt;0.1% of revenue even at ~50K actives (see `growth_contribution_analysis.md`).

**Structure:** Legion's operating data is already in the model. Remaining steps validate sponsor WTP and patient trust.

## Step 0 — Legion data (complete)

Legion shared episode costs, visit frequency, revenue per visit, CAC, and patient counts. I integrated these into `model/assumptions.csv` and reran the model. Break-even on the AI pathway fell from ~$299 to ~$79/patient/yr. See `data/ceo_data_integration.md`.

**Outcome:** Costs came in below external benchmarks. Proceed to buyer interviews and patient survey.

## Step 1, Days 1 7 (parallel): counsel threshold read (cost: one consult)

* Put the 12 counsel questions from `regulatory_notes.md` to healthcare counsel as a threshold read (not a full review): AKS/CMP exposure of employer/foundation underwriting, CPOM constraints in target states, disclosure requirements.
* Confirm the non negotiables in writing: zero patient level data to any funder; no clinical influence; no capitated per patient risk while episode cost is unresolved.

**Outputs:** counsel flagged issue list; restricted category confirmation; pilot permissibility read.
**GATE G1:** unavoidable AKS/CPOM exposure → STOP or redesign before any buyer conversation.

## Step 2, Days 4 7: build the outreach machine (cost: ~$0, founder time)

* Finalize buyer target list: `research/expert_targets.csv` (29 named targets) + employer benefits leaders; sequencing per `sponsor_test_package.md` §7, employers, payers, foundations first; pharma education deferred pending counsel.
* Finalize interview guide (sponsor_test_package §3, incl. §3.1 probes: PEPM for a NARROW AI psychiatry benefit, realistic utilization, hybrid branded sponsorship package).
* Configure the patient concept test: prototype (`app/`) is built and QA'd; recruit research panel (75 100 per arm, 4 arms; $5 15/complete ≈ $2 6K).

**Outputs:** scheduled interviews (target 15 20); live concept test ready.

## Step 3, Days 8 21: run both sides (cost: panel fees + founder time)

* **Sponsor side:** 15 20 qualified buyer interviews. Score each on the qualification scorecard; log on the evidence ladder (L1 interest → L5 signed pilot). Van Westendorp WTP elicitation anchored to "1,000 eligible patients."
* **Patient side:** run the concept test; monitor primary metrics (continuation, trust, independence) and guardrails (privacy concern, opt out, comprehension, core book contagion proxy) against pre registered provisional thresholds.

**Outputs:** WTP distribution by buyer category; evidence ladder placement per buyer; concept test results with CIs; red flag log.
**GATE G3 (patient):** trust/continuation guardrail breach → STOP the sponsor facing framing; reassess.
**GATE G3 (sponsor):** any buyer requiring patient level data, clinical influence, or prescription linked outcomes is disqualified, not accommodated.

## Step 4, Days 22 26: update the model and seek commitment

* Re run the model with interview derived A15/A21/A05 ranges and concept test A10/A11/A26 estimates; recompute the north star metric and $1B backsolve.
* Pursue the strongest L3+ buyers toward a paid design partner LOI (term sheet skeleton in sponsor_test_package §8, counsel reviewed).

**Outputs:** updated low/base/high cases; risk adjusted contribution margin; LOI status.

## Step 5, Days 27 30: founder decision review

* Present: updated economics, evidence ladder, patient results, counsel read, kill criteria checklist.
* Decide: **proceed** (design live pilot), **modify** (narrow scope, different buyer category), or **stop** (publish rationale; revisit only on new evidence).

**Outputs:** decision memo; pilot plan or shutdown rationale; updated assumptions summary.

## Success criteria (all required to proceed)

1. Step 0 economics survive real Legion data (break even within reach of evidenced ARPU).
2. Median credible WTP above the model derived threshold; ≥1 paid design partner or signed pilot commitment; ≥2 additional qualified prospects continuing; plausible ~90 day procurement path.
3. Patient test passes: ≤5pp continuation decline, ≤0.25 trust decline, ≥80% disclosure comprehension, no material independence decline, no guardrail breach (thresholds provisional; update with Legion baselines).
4. Counsel threshold read clears the structure with zero patient level data flows.

## Kill criteria (any one stops or forces redesign)

Buyer WTP below threshold; PHI/patient level targeting or clinical influence demanded; material trust/continuation decline; economics only work via referral or prescription steering; compliance costs eliminate margin; addressable buyer base too narrow; required patient scale implausible; model works only under several aggressive assumptions simultaneously; simpler alternatives (reimbursement expansion) clearly superior; core AI care roadmap materially distracted.

## Budget summary (labeled estimates)

* Research panel: $2 6K. Counsel threshold read: $5 15K. Incentives/tools: <$2K. Founder time: the real cost, capped by early-week alignment gates.
* Total cash: **≈$10 25K** (line items sum $7 23K; the balance is contingency), fully reversible, no engineering beyond the built prototype.

*Timeline checkpoints map to the five decision gates in `decision_framework.md`; the build step (Days 4 7) carries no gate.*
