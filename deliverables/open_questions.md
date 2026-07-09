# Open Questions

Format: Question | Why it matters | Current assumption | Evidence needed | Owner | Status

## Q01: What does "free care" mean for this analysis?

* **Why:** Determines which cost base sponsor revenue must cover (clinician visit — high cost vs. AI-only episode — low cost). Changes the answer.
* **Current assumption:** Narrow AI enabled pathway where reimbursement is unavailable. Sponsor content applies only to this pathway, never to existing reimbursed patients.
* **Evidence needed:** Explicit written confirmation that "free care" means the narrow AI-enabled uninsured pathway assumed in this analysis (non-blocking; analysis proceeded on the stated assumption).
* **Owner:** Analyst | **Status:** Assumption adopted. No contradictory scope answer received. Treat as confirmed unless Legion revises.

## Q02: Legion's actual visit economics and utilization

* **Why:** Required sponsor ARPU = incremental cost / (1 − target margin). Cannot compute without cost per visit/episode and visits per patient.
* **Current assumption (updated 2026-07-08):** Legion operating data integrated (`data/ceo_data_integration.md`): A01 $74/visit, A02 $37/visit, A02b ≈$8/episode, A03 5.3 visits/patient/yr (base), 13.2 high, $153/visit revenue, ≈3,000 active patients, CAC $250.
* **Still placeholder:** A03b (AI-supported cadence 12/yr), A04 (AI-driven episodes 6/yr), A06b (ad sessions 52/yr), A13 (eligible free-pathway population 25K-750K).
* **Evidence needed:** Product analytics for engagement; market sizing for A13.
* **Status:** Partially resolved. Break-evens rerun on Legion data.

## Q03: What does Lotus's "premium sponsorships" model actually sell?

* **Why:** Determines whether the closest analogue sells attention, access, education, leads, or outcomes, shapes which model Legion should test.
* **Current assumption:** RESOLVED as far as public sources allow (see `research/lotus_notes.md`): "premium sponsorships" is company PR language, not a demonstrated feature. No named sponsors, no placement mechanics public. CEO quote says monetization "may include sponsored content or subscriptions" and current focus is product/patients, not revenue. One uncorroborated single source claim of employer paid access at $50/employee/mo. Treat Lotus as an unproven experiment, not evidence the model works.
* **Evidence needed:** Ongoing monitoring; expert interviews if authorized.
* **Owner:** Analyst | **Status:** Complete (public source limit reached)

## Q04: Will sponsors pay above the required ARPU threshold?

* **Why:** H2; the commercial gate. Kills the idea if WTP is below threshold.
* **Current assumption:** Benchmarks in (see `research/comparable_notes.md`): fixed fee sponsor ARPU anchor ≈$10-20/patient/yr (GoodRx pharma solutions proxy; model uses $15 gross / $10.50 net); patient vertical eCPM $20-45; employer PEPM $36-4,200/patient/yr (Model D anchor ≈$600/yr base × 55% utilization → ≈$330 effective). No public precedent of a sponsor underwriting free psychiatric care specifically. WTP above threshold remains unproven.
* **Evidence needed:** 15-20 sponsor-side buyer interviews in 30-day plan (A15 is sensitivity #1).
* **Owner:** User for interviews | **Status:** Benchmarks complete; interviews pending

## Q05: Does sponsorship materially harm patient trust in psychiatric care?

* **Why:** H3; the patient gate. Psychiatry is a high sensitivity context.
* **Current assumption:** Some negative impact possible; magnitude unknown (A10/A11/A26 placeholders in model).
* **Evidence needed:** Randomized patient concept test; live survey at https://legion-take-home-assignment.vercel.app/ (built, not fielded at panel scale).
* **Owner:** Analyst | **Status:** Prototype deployed; fielding pending

## Q06: Which sponsor categories does Legion consider unacceptable?

* **Why:** Constrains rate card and test variants.
* **Current assumption:** No branded drug ads in initial live test; no diagnosis level targeting ever. Category matrix in `sponsor_test_package.md` §6.
* **Evidence needed:** CEO strategic context answer (non-blocking).
* **Owner:** User → CEO | **Status:** Default assumptions adopted; CEO strategic-context answer not required to proceed

## Q07: What is the realistic US addressable population for Legion's uninsured free pathway?

* **Why:** Distinguishes "all Americans" from Legion's actual eligible cohort; bounds sponsorship/ads revenue at scale.
* **Current assumption (updated 2026-07-09):** National TAM from Census ACS 2024 + SAMHSA NSDUH 2024 (P01–P08): ≈27.5M uninsured; ≈5.9M uninsured adults 18+ with AMI; ≈1.5M receiving MH treatment/yr. Model A13 (25K / 150K / 750K) = Legion **reachable capture** of uninsured AMI. **CEO confirmed 0 of ≈3,000 actives today are uninsured** — pathway is greenfield.
* **Evidence needed:** Expected uninsured volume at 6–12 months; uninsured visit type (sync vs AI-only).
* **Owner:** CEO + analyst | **Status:** **Mostly resolved** — national TAM anchored; Legion current mix confirmed zero uninsured. See `data/uninsured_population_sizing.md`.

## Q08: How often will patients engage with a sponsor-funded free AI pathway (ad inventory)?

* **Why:** Model A revenue = sessions/patient/yr × CPM. Low engagement is why ads fail even before population scale.
* **Current assumption:** A06b placeholder 12 / 52 / 450 sessions/yr (low/base/high). Not derived from US average doctor-visit statistics; specific to in-app engagement in a psychiatry product.
* **Evidence needed:** Legion product analytics or pilot data from the free AI pathway.
* **Owner:** CEO / product | **Status:** Open (placeholder); high case widened to 450 sessions/yr; base case rejection of ads unchanged
