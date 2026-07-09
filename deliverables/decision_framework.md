# Decision Framework

## Core Decision

> Should Legion allocate meaningful founder, legal, engineering, clinical, product, and commercial resources during the next six months to developing a sponsor supported care model?

Answer must be: proceed, modify, or stop, falsifiable and conditional where necessary.

## Scope: What "Free Care" Means (Working Assumption)

Primary case: **sponsor-funded access for uninsured patients on a narrow, low-cost, AI-enabled care pathway where insurance reimbursement is unavailable** — not replacing Legion's existing reimbursed FFS book. (Pending CEO confirmation of scope, see Q01; Census TAM in `data/uninsured_population_sizing.md`.)

Three pathways compared throughout:

| Pathway | Relative Cost | Sponsorship Plausibility |
| | | |
| Traditional clinician visit | High | Low |
| AI supported clinician care | Medium | Conditional |
| Mostly AI driven care episode | Low | Highest |

## Five Decision Gates

1. **Economic:** Sponsor revenue per eligible patient ≥ incremental care cost + sponsor servicing + commercial cost + compliance cost + trust related churn cost + contribution margin buffer. Required revenue = incremental cost / (1 − m); at m = 25%, revenue ≈ 1.33× cost.
2. **Commercial:** Credible sponsors pay enough under acceptable conditions, identified budget owner, existing budget, WTP ≥ threshold, paid pilot willingness, procurement start, acceptance of privacy/clinical independence constraints. Interest alone is not evidence.
3. **Patient:** No material harm to trust, booking/continuation, perceived clinical independence, retention, disclosure accuracy, or experience.
4. **Regulatory/Clinical:** No patient level data to sponsors, no influence on prescribing, no prohibited referral incentives, no unacceptable privacy/advertising risk, no ambiguity about clinical independence.
5. **Strategic:** Better use of resources than insurance reimbursement, subscriptions, copays, employer funded access, payer contracts, foundation underwriting, or non advertising pharma services.

## Hypothesis Tree

* **H1, Unit economics work:** Sponsor revenue per eligible patient ≥ fully loaded incremental cost / (1 − m).
* **H2, Sponsors will pay enough:** Qualified buyer + relevant budget + price acceptance + constraint acceptance + paid pilot interest + procurement path.
* **H3, Patients accept the model:** No material decline in trust, booking intent, continuation, perceived independence; acceptable privacy concern and opt out.
* **H4, The model can scale:** Required revenue = $1B / revenue multiple; required patients = required revenue / sponsor ARPU. Plausible patient count, sponsor count, contract values, concentration, growth.
* **H5, Sponsorship is strategically preferable:** Beats employer underwriting, payer contracts, subscriptions, foundation funding on risk adjusted returns.

## North Star Metric

> **Risk adjusted contribution margin per eligible patient** = sponsor revenue − care delivery cost − sponsor servicing cost − commercial cost − incremental legal/compliance cost − estimated trust/churn cost.

## Monetization Models to Compare

A. Programmatic advertising (impressions × fill × eCPM/1000), expect insufficient.
B. Direct fixed fee sponsorship (contract value / exposed patients), most plausible initial model.
C. Performance based partnership (qualified actions × rev/action), legal review required; steering risk.
D. Employer/payer underwriting (PMPM/per episode), attractive, longer cycle.
E. Foundation/nonprofit underwriting, supplemental, less scalable.

## Initial Thesis (falsifiable)

> Traditional programmatic advertising is unlikely to fund meaningful care costs. Fixed fee, non personalized sponsorship or underwriting may be viable for a narrow AI enabled care pathway, subject to sponsor willingness to pay, patient trust, legal feasibility, and strategic fit tests.

## Kill Criteria (abridged; full list in execution brief §23)

Stop or redesign if: sponsor WTP < threshold; sponsors require PHI/patient level targeting/clinical influence; trust or continuation declines materially; economics depend on referral or prescription steering; compliance costs eliminate margin; required patient scale implausible; simpler models clearly superior; core AI care roadmap distracted.
