# Risk Analysis — Sponsored Free Care for Uninsured Patients

**Purpose:** A deeper read on what could go wrong if Legion pursues ads, sponsorship, or underwriting for a new uninsured-only pipeline. Deck slides 6–7 summarize the decision tree and contagion math; this document is the full map.

**Scope reminder:** ~3,000 actives today are insured. This analysis is about a **greenfield uninsured pipeline** — but several risks spill over into the core business anyway.

---

## How to read this

| Severity | Meaning |
|---|---|
| **Existential** | Could damage Legion's core business, trigger enforcement, or make the initiative net-negative regardless of sponsor revenue |
| **Structural** | Could invalidate the economics even if execution is good |
| **Execution** | Could waste founder time and capital without changing the strategic answer |
| **Reputational** | Could erode trust or brand even if legally compliant |

Each risk includes: **mechanism** (how it happens), **early signal** (what to watch in the 30-day test), and **guardrail** (what stops or contains it).

---

## 1. Economic risks

### 1.1 Employer underwriting rests on two unvalidated inputs (Structural — #1 and #2 model sensitivities)

**Mechanism:** Model D's positive case ($330/patient/yr, ~+$243 margin) is `PEPM willingness to pay × utilization rate`. Both are external placeholders — not Legion pilot data. If employers offer Lyra-style platform pricing but only for a narrow AI psychiatry slice (not full EAP), or if utilization is 30% instead of 55%, revenue falls below break-even with no change in care cost.

**Early signal:** Buyer interviews cluster below $50/employee/month *for this product shape*, or procurement contacts say utilization historically runs 20–35% for single-condition digital benefits.

**Guardrail:** Pre-registered WTP floor (~$36/patient/yr). Kill if Model D ARPU falls below break-even even at "reasonable" PEPM. Probe utilization explicitly in interviews (see `sponsor_test_package.md` §3.1).

### 1.2 Pathway mix drift — AI-only vs. clinician-heavy (Structural)

**Mechanism:** Economics assume a mostly-AI uninsured pathway (~$8/episode, break-even ~$79–167/yr). Uninsured patients with active mental illness may need more synchronous psychiatric visits than modeled. Clinician-heavy pathways need **$538+/patient/yr** — only employer/foundation-scale funders clear that bar; ads and sponsorship cannot.

**Early signal:** Clinical advisors flag that uninsured AMI population skews higher acuity; intake data from early cohort shows >50% escalating to sync within 90 days.

**Guardrail:** Cap the free pathway to AI-appropriate acuity at launch; measure escalation rate before scaling acquisition. Do not promise "full psychiatry" on sponsorship economics built for AI continuity.

### 1.3 Trust churn is modeled on sponsor-tier revenue only (Structural)

**Mechanism:** The model's trust cost formula charges trust damage against sponsor/employer ARPU. The larger downside is **contagion to Legion's existing insured book** (~$6M/yr core FFS): if sponsor branding makes paying patients question clinical independence, the loss dwarf sponsor revenue. Model v3 added a core-book contagion placeholder (A25/A26) but inputs are unresolved.

**Quantified scenario (Legion data, deck slide 7):**

| Scenario | Calculation | Core FFS loss | Brand sponsor rev @ 15K uninsured ($10.50/yr) | Net |
|---|---|---|---|---|
| 2% churn · avg patient | 2% × 3,000 × $811 | **~$49K/yr** | ~$158K/yr | +$109K |
| 2% churn · mature cohort | 2% × 3,000 × $2,025 | **~$122K/yr** | ~$158K/yr | +$36K (thin) |
| 5% churn · mature cohort | 5% × 3,000 × $2,025 | **~$304K/yr** | ~$158K/yr | **−$146K** |

**Rule:** Sponsor revenue on the uninsured pipeline must exceed core-book spillover loss.

**Early signal:** Patient concept test shows trust decline among *insured* respondents when shown sponsor-funded framing; NPS dip among current actives after any public sponsor announcement.

**Guardrail:** Pre-registered A26 spillover limit in `experiment_spec.md`. Separate measurement for core-book exposure, not just uninsured cohort. Any trust breach → stop or redesign.

### 1.4 Free care as CAC may not convert (Execution)

**Mechanism:** The upside case (~$8/episode vs $250 CAC) requires ~3.2% free-to-paid conversion to break even on acquisition economics. Uninsured free users may convert to paid insurance coverage at different rates than general DTC — or may never convert if they remain uninsured.

**Early signal:** Conversion tracking on any pilot cohort shows <1% insured conversion at 90 days.

**Guardrail:** Treat free-care-as-CAC as a *separate* hypothesis from sponsorship funding; don't justify sponsor build on conversion hope alone.

### 1.5 Scale requirements are unrealistic for niche positioning (Structural)

**Mechanism:** Even Model D's favorable backsolve implies ~303K underwritten patients for a $1B revenue story at 10× multiple — ~100× today's actives. Employer contracts at that scale require an enterprise sales machine, capital, and product breadth (Lyra/Spring Health raised $1B+ over years) that a narrow AI psychiatry episode product may not command.

**Early signal:** Buyers say they'd pilot 500–2,000 lives, not 50K+; sales cycle estimates exceed 12 months.

**Guardrail:** Treat backsolves as **consistency checks**, not growth plans. Success in 30 days = directional WTP + trust, not $1B path proof.

---

## 2. Regulatory and legal risks

### 2.1 FTC / health-data advertising pattern (Existential for ad models)

**Mechanism:** BetterHelp ($7.8M) and GoodRx ($1.5M) were penalized for sharing health-adjacent data with ad platforms — not hacks, ordinary pixel integrations. Mental health intake + ad tech is the closest factual analog to Legion. Remedies included **structural bans** on sharing health data for advertising.

**Early signal:** Any vendor or sponsor asks for attribution pixels, conversion APIs, or audience matching on authenticated care pages.

**Guardrail:** Hard line — no ad-tech in care flows; session replay off. Funders get zero patient-level data. Already in `patient_experience_spec.md`.

### 2.2 AKS / Beneficiary Inducement on "free care" (Existential if federal billing exists)

**Mechanism:** Sponsor-funded free care is "remuneration" under AKS and Beneficiary Inducement CMP if it induces use of services billable to Medicare/Medicaid. Legion's core business is insurance reimbursement — free uninsured care could be viewed as inducing downstream reimbursed services if patients convert, share providers, or if wrap-around services touch federal programs. OIG favorable opinions uniformly require **no identifiable patient data back to sponsor** and no steering.

**Early signal:** Counsel flags that free-care + current billing footprint creates inducement exposure; sponsor requests prescription or referral metrics.

**Guardrail:** Threshold counsel read before outreach scales. No pay-per-prescription or referral-linked economics. Document financial-need eligibility if offering free care.

### 2.3 FDA promotion blur on "sponsored education" (Structural for pharma sponsors)

**Mechanism:** Disease-awareness content funded by pharma sits adjacent to product promotion rules. FDA's own research shows consumers conflate disease ads with branded ads when similar or proximate. In psychiatry, off-label perception risk is acute.

**Early signal:** Sponsor proposes co-branded content, speaker programs, or "education" that names products or treatment classes.

**Guardrail:** Firewall between unbranded education and clinical care; no sponsor talking points in clinical workflows. Legal review of any Package B/C content (`sponsor_test_package.md`).

### 2.4 Corporate practice of medicine (Existential in strict states)

**Mechanism:** If sponsorship gives funders influence over which patients receive care, which clinicians deliver it, or treatment protocols, CPOM risk compounds in ~16 strict states. Distinct from AKS — can exist even when economics work.

**Early signal:** Sponsor contract includes clinical KPIs, formulary preferences, or staffing input.

**Guardrail:** No funder influence on clinical decisions — hard line. State-by-state counsel for operating footprint.

### 2.5 HIPAA marketing rule on sponsored communications (Structural)

**Mechanism:** Any arrangement where Legion discloses PHI to a sponsor for remuneration to communicate about the sponsor's product is HIPAA "marketing" with **no exception** — requires individual written authorization. "Free care" alone isn't marketing; sponsor-branded patient communications likely are.

**Early signal:** Sponsor asks for segmented outreach to patients based on diagnosis or medication status.

**Guardrail:** No PHI to sponsors; sponsor visibility limited to aggregate reporting only.

### 2.6 Legal review latency vs. build pressure (Execution)

**Mechanism:** Full AKS/CPOM opinion can take months to a year. Teams often "build while legal reviews" and accumulate rework. Regulatory_notes flags this explicitly.

**Early signal:** Engineering or GTM starts before threshold counsel read returns.

**Guardrail:** Gate 1 (counsel read) before paid pilot or public sponsor branding.

---

## 3. Patient trust and clinical risks

### 3.1 Psychiatry is the highest-sensitivity context (Reputational → Existential)

**Mechanism:** Patients seeking psychiatric care have elevated vulnerability and skepticism of commercial influence. Sponsor presence — especially pharma — can reduce perceived clinician independence more than in primary care or wellness.

**Early signal:** Concept test arms with pharma funding show >0.25 trust drop or >5pp continuation decline.

**Guardrail:** Pre-registered limits in live survey. Prefer employer/community funders over pharma in early tests if trust data is borderline.

### 3.2 Selection bias in who adopts free sponsored care (Structural)

**Mechanism:** Free sponsored care may attract patients who are cost-desperate, higher crisis acuity, or skeptical of quality — different from Legion's insured cohort. Clinical outcomes and cost per episode may exceed model.

**Early signal:** Early cohort escalation-to-crisis rates exceed insured baseline; cost per episode trends above $8–37 range.

**Guardrail:** Tight clinical eligibility criteria; crisis protocols independent of sponsor funding.

### 3.3 Survey ≠ real behavior (Execution)

**Mechanism:** Stated trust in a survey may not predict dropout when a real sponsor logo appears in the app during a medication discussion.

**Early signal:** Qualitative interviews reveal comprehension gaps despite ≥80% survey comprehension.

**Guardrail:** Small real-world pilot (hundreds, not thousands) before scale; monitor live continuation and complaints.

---

## 4. Commercial and market risks

### 4.1 Sponsorship WTP may be categorically below need (Structural — core thesis)

**Mechanism:** The $15 GoodRx anchor (net $10.50) reflects pharma point-of-sale mechanics, not brand sponsorship of care access. No public comparable proves sponsors pay $100+/patient/yr for patient-facing psychiatric access without data in return.

**Early signal:** Van Westendorp median <$50/patient/yr; sponsors condition payment on engagement or conversion metrics.

**Guardrail:** Re-entry trigger requires median >$100/patient/yr. Otherwise sponsorship stays co-funder-only or off the table.

### 4.2 Employer sales cycle mismatch (Execution)

**Mechanism:** Framework labels Model D "longer cycle." A 30-day test can produce interest and directional WTP, not procurement-grade evidence (Gate 2). Pearl/Mindstrong/Babylon failed on payer-side economics despite "interest."

**Early signal:** Buyers enthusiastic in discovery but cite 6–18 month procurement; no budget line until next renewal.

**Guardrail:** Label 30-day output as L1–L3 evidence only. Paid pilot is the Gate 2 bar, not verbal interest.

### 4.3 Survivorship bias in comparables (Structural)

**Mechanism:** Research catalogued ad-model failures thoroughly; employer/payer failures (Pear Chapter 11, Mindstrong shutdown, Babylon Chapter 7) are real but easy to underweight when Lyra/Spring are visible survivors.

**Early signal:** Due diligence on failed employer models surfaces same failure mode Legion is proposing (capitation, unmeasured utilization).

**Guardrail:** Fee-for-benefit PEPM only — no capitated per-patient risk while costs unmeasured. Already in recommendation.

### 4.4 Sponsor concentration and renewal (Execution)

**Mechanism:** Model B backsolve at scale implies hundreds of sponsors ($250K/yr each) or few mega-sponsors. Concentration creates renewal cliff and negotiating leverage against Legion.

**Early signal:** Pipeline shows 2–3 sponsors would fund >80% of revenue; contracts are 12-month with performance outs.

**Guardrail:** Diversification threshold in any pilot contract design; avoid single-sponsor dependency.

---

## 5. Strategic and organizational risks

### 5.1 Opportunity cost vs. core FFS (Structural — Gate 5)

**Mechanism:** Legion's proven engine is reimbursed visits (~$6M, ~76% GM on leveraged AI). Founder days on sponsor buyer interviews are not delegable at validation stage. Same time on payer expansion or reimbursement categories moves **known-margin** revenue.

**Early signal:** Reimbursement opportunities delayed; core growth metrics flat during sponsor pursuit.

**Guardrail:** Legion operating data integrated (economics viable). Cap founder time; sequence reimbursement priorities first if conflicts arise.

### 5.2 Building the pipeline before evidence (Execution)

**Mechanism:** Classic sunk-cost trap: acquire uninsured patients, build sponsor ops, then discover WTP or trust failure. CEO confirmed zero uninsured actives today — ordering is controllable.

**Early signal:** Patient acquisition spend approved before buyer interview results.

**Guardrail:** <$25K test **before** scale acquisition. This is the headline recommendation.

### 5.3 Category confusion — sponsorship vs. underwriting (Reputational)

**Mechanism:** The assignment asks about ads/sponsorship; the surviving economics are employer underwriting (Gate 5 alternative). Internally and externally, teams may blur "sponsored free care" with "employer benefit" — setting wrong buyer expectations and compliance posture.

**Early signal:** Sales materials use "sponsor" for employer PEPM contracts; pharma outreach runs parallel to employer outreach with same deck.

**Guardrail:** Separate packages A/B/C in interviews; document underwriting pivot honestly in interview notes.

### 5.4 Thesis protection / asymmetric falsifiability (Process)

**Mechanism:** Red-team flagged that falsification triggers lean toward keeping "proceed" alive (e.g., cost trigger fired, WTP trigger not tested; Model D promoted with less scale scrutiny than rejected Model B). Pattern: falsify → reframe → still proceed.

**Early signal:** Kill criteria debated away when first evidence is soft positive.

**Guardrail:** Pre-registered symmetric triggers in `experiment_spec.md` and `30_day_plan.md`. Kill-now rationale in `executive_summary.md`.

---

## 6. Risk interaction map

**Risk-weighted decision tree (deck slide 6):**

```
Uninsured sponsor path?
  → Economics [existential] — Legion costs plausible?
  → G1 Legal [existential] — counsel OK?
  → G2 WTP [structural] — buyers above floor?
  → G3 Trust [existential] — survey passes?
  → Contagion check [existential] — sponsor rev > core spillover? (slide 7)
  → Pathway check [structural] — mostly-AI or employer-scale funder?
  → Micro-pilot [execution] — 500–2K → scale or stop
```

Any **existential** NO → stop. 30-day test resolves G2–G3 only, not employer procurement (6–18 months).

Some risks compound:

```
Unvalidated employer WTP ──┐
                           ├──► Build uninsured pipeline ──► Higher acuity mix ──► Costs exceed sponsor revenue ──► Kill
Low sponsor WTP ───────────┘                                      │
                                                                  ▼
Trust damage in concept test ──────────────────────────────► Core book contagion ──► Existential harm to core FFS
                                                                  │
Pharma sponsor + education content ──────────────────────────────┴──► FDA/AKS/trust triple exposure
```

**Highest-order combo risk:** Legion launches a pharma-sponsored free uninsured tier, attracts higher-acuity patients, escalates them to sync care, underprices employer PEPM, and spooks existing insured patients — burning founder time while damaging the core brand. This is not far-fetched; it's the default failure mode if gates 2–4 are skipped.

---

## 7. What the 30-day test actually de-risks (and what it doesn't)

| Risk | Partially addressed by test? | How |
|---|---|---|
| Sponsor WTP | **Yes** | Buyer interviews + Van Westendorp |
| Patient trust (uninsured framing) | **Yes** | Live survey + concept arms |
| Core book contagion | **Partially** | A26 proxy in survey; not a substitute for insured-patient measurement |
| Employer utilization | **Partially** | Interview probes (§3.1); not longitudinal |
| Regulatory exposure | **No** | Needs counsel read, not interviews |
| Pathway acuity / cost mix | **No** | Needs clinical pilot data |
| Opportunity cost | **No** | Founder judgment call |
| Enterprise sales cycle | **No** | 30 days ≠ procurement |

---

## 8. Recommended sequencing (risk-adjusted)

1. **Counsel threshold read** (Gate 1) — cheap relative to brand exposure; scopes AKS/CPOM/FDA.
2. **Legion cost validation** — done; re-run if pathway mix shifts.
3. **Buyer interviews** — only after Step 0; prioritize employer PEPM + utilization, not just headline price.
4. **Patient trust survey** — parallel OK; include insured-respondent arm if possible for contagion signal.
5. **Paid pilot** — only if 1–4 pass; smallest cohort, shortest contract, no capitation.
6. **Scale acquisition** — last, not first.

---

## 9. Kill criteria (consolidated)

Stop or redesign if **any one** fires:

- Employer/sponsor WTP below floor (~$36/patient/yr; sponsorship co-funder needs >$100)
- Patient trust drop >0.25 or continuation drop >5pp (or core-book contagion above A26 limit)
- Counsel finds unavoidable AKS/CPOM exposure or required data sharing with funders
- Utilization evidence pushes Model D below break-even
- Sponsor demands clinical influence, patient-level data, or prescription-linked economics
- Real episode cost + pathway mix pushes break-even above plausible funder ARPU
- Implausible scale / concentration (renewal cliff, single-sponsor dependency)

Full list: `decision_framework.md` §Kill Criteria, `experiment_spec.md`, `30_day_plan.md`.

---

*Sources: `regulatory_notes.md`, `executive_summary.md`, `model/sensitivity_outputs.csv`, `comparable_notes.md`.*
