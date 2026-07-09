# Patient Side Concept Test, Experiment Specification

**Status:** Draft specification for prototype implementation (Next.js + PostHog).
**Answers:** H3, does sponsor supported care materially harm patient trust or continuation behavior?
**Does not answer:** Whether Legion should proceed with sponsorship (H1, H2, H4, H5, and the five decision gates are out of scope here).
**Source of truth for parameters:** `decision_framework.md` and execution brief §20, §22, §26, §27. This document elaborates those parameters; it does not redefine metrics, thresholds, or variants.

## 1. Hypotheses

H3 (execution brief): *Patients accept the model, no material decline in trust, booking intent, continuation, or perceived independence; acceptable privacy concern and opt out.*

H3 is not a single testable hypothesis, it is a bundle of three primary non inferiority hypotheses (one per primary metric) plus a set of guardrail checks that are evaluated against absolute thresholds rather than tested against Control. Framing each primary metric as **non inferiority** (rather than a two sided difference test) matches the actual business question: we are trying to rule out *harm*, not detect a benefit.

### H3a, Continuation rate

* **H0 (material decline exists):** Control continuation rate − Variant continuation rate ≥ 5 percentage points.
* **H1 (no material decline):** Control continuation rate − Variant continuation rate < 5 percentage points.
* Non inferiority margin: 5pp (provisional, per brief §22).

### H3b, Trust in Legion

* **H0 (material decline exists):** Control mean trust score − Variant mean trust score ≥ 0.25 (5 point scale).
* **H1 (no material decline):** Control mean trust score − Variant mean trust score < 0.25.
* Non inferiority margin: 0.25 points (provisional, per brief §22).

### H3c, Perceived clinical independence

* **H0 (material decline exists):** Control mean independence score − Variant mean independence score ≥ margin.
* **H1 (no material decline):** difference < margin.
* The brief does not quantify "material decline" for this metric. **Recommendation (flagged, not adopted):** apply the same 0.25 point provisional margin used for trust, since both are measured on the same 5 point scale and independence is arguably the more sensitive construct. This is a gap in the lead approved thresholds, not a redefinition, see Recommendations section.

### Guardrail checks (not hypothesis tests; threshold/flag checks)

Evaluated as pass/fail against absolute or comparative thresholds, not as null/alternative pairs:

| Guardrail | Rule |
| | |
| Disclosure comprehension | ≥80% of respondents answer the comprehension check correctly |
| Privacy concern | Descriptive; flagged if materially elevated vs. Control (no numeric threshold set, see Recommendations) |
| Opt out rate | Descriptive; flagged if materially elevated vs. Control |
| Willingness to provide accurate information | Descriptive; flagged if materially reduced vs. Control |
| Preference for paid sponsor free option | Flagged if a strong majority (recommend: >50% as a starting operational definition, unconfirmed) prefer paying |
| Sponsor category acceptability | Descriptive by variant, especially C (visible pharma/healthcare sponsor) |
| Core book trust spillover (A26 proxy) | Flagged if mean "would you recommend Legion to a friend paying full price?" or "would you continue using Legion for insured visits if this sponsor model existed?" drops ≥5pp vs. Control (provisional non-inferiority proxy for model A26; v2) |
| Negative qualitative feedback | Flagged if a severe concern theme recurs (see §6 qualitative coding plan) |

## 2. Design

### Structure

Four arm, between subjects, single exposure concept test:

* **Control**, affordable care, no sponsorship
* **Variant A**, free care, "supported by Sponsor X"
* **Variant B**, Variant A + clearly separated sponsored education content
* **Variant C**, visible healthcare/pharma sponsor (concept test only; not for the first live pilot)

Each participant sees exactly one arm (no within subject exposure to multiple variants, this avoids contamination and demand effects from comparing conditions).

### Randomization mechanism

* Use a **PostHog multivariate feature flag** (e.g., `patient sponsorship concept test`) with four payload values (`control`, `variant_a`, `variant_b`, `variant_c`).
* Assignment is **client side**, keyed to the PostHog `distinct_id` (anonymous device/browser ID persisted via cookie/localStorage), so assignment is **sticky**: a returning participant within the same test window always sees the same arm.
* Equal allocation (25%/25%/25%/25%) unless a recruitment channel requires stratified quotas (see §3).
* The `concept_assigned` event is fired immediately on flag evaluation, before the concept page renders, so assignment is logged even if the participant drops off before viewing content (needed for intent to treat style funnel analysis).
* Feature flag payload also carries `sponsor_category` (e.g., `none`, `consumer_health`, `pharma`) so downstream events can log sponsor category without a second lookup.

### Blinding limits

* This is **not a blinded design** in the classic sense: the manipulation *is* the visible content the participant sees, so participants cannot be blinded to their own condition by construction. Each participant is naive to the existence of other conditions (single exposure, no side by side comparison), which limits demand characteristic bias relative to a within subject design.
* Analysts are **not blinded** to variant assignment, since variant is required for every metric computation. This is mitigated by (a) pre registering the thresholds and non inferiority margins in this document before data collection, and (b) computing all primary metrics through an automated PostHog/analysis pipeline rather than manual tallying, to reduce analyst discretion.
* Qualitative coders (see §6) should be blinded to variant where feasible to reduce confirmation bias in severity coding.

### Allocation caveat

Variant C is explicitly a concept test only arm. Its results inform sponsor category acceptability and worst case trust/independence exposure, but a "pass" on C does not imply readiness for a live pilot with a visible pharma sponsor, that would require a separate legal/regulatory review (execution brief §24.3).

## 3. Participants

### Definition

A study participant is an adult who is shown one concept variant and completes (or exits) the behavioral action and survey flow. Participants are **not** current Legion patients and receive **no actual care**, the intro page (§27 Page 1) must state this explicitly.

### Recruitment channels

1. **Research panel**, a commercial panel vendor (e.g., a standard online panel provider) recruiting general population adults, filtered to the screening criteria below. Panel vendor manages participant PII and incentive payment; Legion/the prototype never receives panel side identity data.
2. **Landing page traffic**, organic or lightly promoted traffic to a standalone research landing page (clearly separate from Legion's live patient facing product), disclosed as a research study, not a booking flow.

### Screening criteria (must pass all)

* Age 18+
* Not a current Legion patient
* Has used telehealth before, OR is a prospective patient open to using telehealth for mental health care (per audience definition: "telehealth experienced adults" and "prospective patients" are both acceptable, in line with brief §22)
* Able to read and respond in the study's language
* Provides informed consent to a research study (not a clinical encounter)
* Passes a basic attention check embedded in the screener

### Exclusions

* Current or recent (defined by Legion clinical/legal, e.g., within 12 months) Legion psychiatric patients, excluded unless Legion's legal and clinical teams have explicitly approved their inclusion (per brief §22, this is a hard constraint, not a suggestion)
* Individuals in apparent acute mental health crisis (screen for and route to standard crisis resources rather than the study; exclude their data)
* Panel/vendor employees or known survey fraud profiles
* Duplicate participants (same PostHog `distinct_id` or panel ID re entering the flow)
* Participants who fail the in survey attention/comprehension check may be flagged and analyzed separately rather than silently dropped (dropping without disclosure risks biasing comprehension estimates upward)

### Allocation targets

Equal allocation across the four arms; if recruiting from both panel and landing page traffic, stratify allocation within each channel (i.e., randomize independently within "panel" and within "landing page" `participant_type`) so channel mix is balanced across arms and channel effects can be checked as a covariate.

## 4. Funnel Definition, PostHog Integration Contract

This section is the contract the prototype's event tracking layer must implement exactly. Event and property names are taken verbatim from execution brief §26; no new events or properties are introduced beyond what is explicitly needed to fill an execution gap (flagged where that occurs).

### Funnel stages and events

| Stage | Page (per §27) | Event | Trigger definition |
| | | | |
| 0. Assignment | Pre render | `concept_assigned` | Fires the instant the PostHog feature flag resolves a variant for this `distinct_id`, before Page 2 renders. Fires once per participant per test window. |
| 1. Exposure | Page 2, Sponsorship Concept | `concept_viewed` | Fires when the concept page has fully mounted and the concept content is in viewport (on mount is acceptable for a single viewport page; use an intersection observer if content requires scrolling). |
| 2a. Engagement (optional) | Page 3, Behavioral Action | `learn_more_clicked` | Fires when the participant clicks "Learn more." Does not end the funnel, participant proceeds to a final action afterward. |
| 2b. Engagement (optional) | Page 3 | `privacy_details_opened` | Fires when the participant clicks "View privacy details." |
| 2c. Terminal action | Page 3 | `continue_clicked` | Fires when the participant selects "Continue." This is the primary behavioral proxy for **continuation rate**. |
| 2d. Terminal action | Page 3 | `sponsor_opt_out_selected` | Fires when the participant selects "Choose sponsor free option" **or** "Exit." Both map to `opt_out=true`; use `decision_result` to distinguish which. |
| 3. Survey start | Page 4, Trust Survey | `survey_started` | Fires on Page 4 mount, only for participants who did not exit at Page 3. |
| 4. Survey complete | Page 4 | `survey_submitted` | Fires on submit. Carries the computed score properties (§4 property schema below). This is where `trust_score`, `independence_score`, `privacy_concern`, `continuation_intent`, and final `opt_out` state are logged. |
| 5. Booking intent | Page 4 (survey item 5) or a dedicated CTA | `booking_intent_selected` | Fires when the participant indicates stated intent to continue/book (Likert item 5, "I would continue using the service," dichotomized at "Agree"/"Strongly Agree" = intent positive), distinct from the *behavioral* `continue_clicked` action at Page 3. Having both a behavioral and a stated intent event lets analysis compare revealed vs. stated continuation. |
| 6. Close | Page 5, Thank You | *(no event required; optionally log page view via default PostHog pageview capture, not a named funnel event)* |, |
| 7. Reporting | Admin Dashboard | `results_viewed` | Fires when an authenticated admin loads the results dashboard. |
| 8. Export | Admin Dashboard | `scenario_exported` | Fires when an admin exports results (CSV/JSON). |

### Property schema (per event)

Properties are restricted to the list in brief §26.2: `variant`, `sponsor_category`, `participant_type`, `decision_result`, `trust_score`, `independence_score`, `privacy_concern`, `continuation_intent`, `opt_out`. No event should carry any property outside this list plus standard PostHog defaults (timestamp, distinct_id, URL).

| Event | Properties attached |
| | |
| `concept_assigned` | `variant`, `sponsor_category`, `participant_type` |
| `concept_viewed` | `variant`, `sponsor_category`, `participant_type` |
| `learn_more_clicked` | `variant`, `sponsor_category`, `participant_type` |
| `privacy_details_opened` | `variant`, `sponsor_category`, `participant_type` |
| `continue_clicked` | `variant`, `sponsor_category`, `participant_type`, `decision_result="continue"` |
| `sponsor_opt_out_selected` | `variant`, `sponsor_category`, `participant_type`, `decision_result="opt_out"` or `"exit"`, `opt_out=true` |
| `survey_started` | `variant`, `participant_type` |
| `survey_submitted` | `variant`, `participant_type`, `trust_score`, `independence_score`, `privacy_concern`, `continuation_intent`, `opt_out` |
| `booking_intent_selected` | `variant`, `participant_type`, `continuation_intent` |
| `results_viewed` | `participant_type="admin"` |
| `scenario_exported` | `participant_type="admin"`, `variant` (filter applied, or `"all"`) |

Allowed values (for prototype validation/typing):

* `variant`: `control` \| `variant_a` \| `variant_b` \| `variant_c`
* `sponsor_category`: `none` \| `consumer_health` \| `pharma` (or the specific synthetic sponsor category used per variant)
* `participant_type`: `panel` \| `landing_page` \| `admin`
* `decision_result`: `continue` \| `opt_out` \| `exit`
* `trust_score`, `independence_score`, `privacy_concern`, `continuation_intent`: numeric, 1, 5 (derived from survey items, see §5)
* `opt_out`: boolean

### Explicit exclusions (per §26.2 and §24.1)

Do not capture: diagnoses, medications, names, email addresses (unless the panel vendor requires it for payment, handled outside PostHog), any PHI, free text health disclosures, or session replay of any kind. Session replay and network recording must be disabled in the PostHog project config for this test (`24.1`, `26.3`).

## 5. Survey Instrument

Page 4 ("Trust Survey") presents the six items from brief §27 on a 5 point Likert scale (1 = Strongly Disagree, 5 = Strongly Agree), followed by one comprehension check item not in the original six (flagged addition, needed to satisfy the ≥80% disclosure comprehension guardrail, which cannot be measured by a self report Likert item alone).

### Core items (verbatim from brief §27, response scale added)

| # | Item | 5 point scale | Primary mapping |
| | | | |
| Q1 | "I trust Legion to make independent clinical decisions" | Strongly Disagree → Strongly Agree | `independence_score` |
| Q2 | "I understand the sponsor's role" | Strongly Disagree → Strongly Agree | Self reported comprehension (supporting signal only, see comprehension check below) |
| Q3 | "I am comfortable with sponsor supported care" | Strongly Disagree → Strongly Agree | `trust_score` (primary component) |
| Q4 | "I am concerned about my data being shared" | Strongly Disagree → Strongly Agree | `privacy_concern` |
| Q5 | "I would continue using the service" | Strongly Disagree → Strongly Agree | `continuation_intent` (stated intent; feeds `booking_intent_selected`) |
| Q6 | "I would prefer a paid sponsor free option" | Strongly Disagree → Strongly Agree | Guardrail: preference for paid option |

### Core book contagion proxy items (maps to model A26)

These items proxy whether sponsor framing damages trust in Legion's **core** paid/insured product, not just the sponsored tier. Scored descriptively against Control using the ≥5pp non inferiority framing in §1 guardrails; not added to the frozen PostHog property list (analysis layer only, same pattern as comprehension check).

| # | Item | 5 point scale | Primary mapping |
| | | | |
| Q7 | "I would recommend Legion to a friend who pays full price for visits" | Strongly Disagree → Strongly Agree | Core book spillover proxy (A26) |
| Q8 | "If I had insurance coverage, I would still choose Legion for my psychiatric visits" | Strongly Disagree → Strongly Agree | Core book spillover proxy (A26) |

**Scoring note:** `trust_score` is computed from Q3 (comfort with sponsor supported care) as the primary trust item; Q1 is scored separately into `independence_score` since it specifically probes independence of clinical decision making, not general comfort. Both are correlated constructs by design (a participant who doubts independence will likely also show lower trust), and that correlation should be reported, not treated as redundant. This scoring choice is a specification decision made to fit the six fixed items into the two required score properties; it should be validated with a reliability check (e.g., correlation between Q1 and Q3 in pilot data) before the inference scale run.

### Disclosure comprehension check (flagged addition, not in original six items)

Self reported understanding (Q2) is not adequate evidence for the ≥80% comprehension threshold, because agreement with "I understand the sponsor's role" measures confidence, not accuracy. Add one factual, multiple choice item immediately after Q2:

> "Based on what you just saw, which of the following is true?"
> a) Legion shares my personal health information with the sponsor *(incorrect, distractor)*
> b) The sponsor pays to support access to care, but does not see my personal health information or influence my treatment *(correct)*
> c) The sponsor's staff can review my treatment plan *(incorrect, distractor)*
> d) I am not sure *(incorrect but distinguishes confusion from wrong but confident)*

* Scored as correct/incorrect (binary), aggregated per variant as the disclosure comprehension percentage.
* For Control (no sponsor), this item is not applicable, either skip it for Control or replace with a parallel comprehension check about the "affordable care, no sponsorship" framing, to keep the funnel structurally comparable. Recommend the latter for cleaner cross arm comparability; flagged as a specification decision for the prototype team to confirm with the lead.
* This item's response is stored as part of `survey_submitted`'s payload for scoring but is **not** one of the nine listed PostHog properties; recommend deriving a boolean or percentage server side/in the analysis layer rather than adding a new PostHog property, to stay within the approved property list. Flagged as a genuine gap between the fixed property list and the stated ≥80% comprehension requirement, see Recommendations.

### Optional bounded free text (guardrail: negative feedback / severe concern detection)

One optional, short free text box at the end of Page 4: *"Any concerns about this concept? (Please do not include any personal health information.)"* Capped length (e.g., 280 characters), with an on screen reminder not to enter health information, and a client side simple keyword/PII filter as a soft guard (not a compliance control, real health information filtering requires more than keyword matching, so this is a UX nudge, not a safeguard to rely on for compliance). This text is used only for the qualitative coding plan in §6 and is not sent to PostHog as an event property (kept out of analytics to avoid inadvertent PHI capture in the analytics pipeline); store it in the prototype's own database with the same no PHI expectations enforced by copy and input constraints.

## 6. Analysis Plan

### Per metric comparison vs. Control

| Metric | Type | Test | Effect size | CI |
| | | | | |
| Continuation rate (H3a) | Binary (`continue_clicked` / total exposed) | Two proportion z test / chi square, framed as **non inferiority** against the 5pp margin | Absolute risk difference (pp), relative risk | 95% CI on the difference (Newcombe/Wilson method for difference of proportions, more robust at small n than a simple normal approximation) |
| Trust score (H3b) | Ordinal treated as continuous, 1, 5 | Welch's t test as primary (robust to unequal variance); Mann Whitney U as a robustness check given Likert scale ordinality | Mean difference, Cohen's d | 95% CI on mean difference |
| Independence score (H3c) | Ordinal treated as continuous, 1, 5 | Same as trust score | Mean difference, Cohen's d | 95% CI on mean difference |

Guardrails (privacy concern, opt out rate, willingness to provide accurate information, preference for paid option, sponsor category acceptability) are reported descriptively by variant with 95% CIs, and flagged against the rules in §1, rather than formally hypothesis tested, they are risk indicators, not go/no go statistical tests in their own right, per the brief's framing of them as guardrails rather than primary hypotheses.

### Multiple comparison caution

Three treatment arms (A, B, C) each compared to Control across three primary metrics = up to 9 primary pairwise tests. Apply a Holm Bonferroni (or Benjamini Hochberg FDR) correction **within the family of 9 primary non inferiority tests** before treating any single result as confirmatory. Given the discovery scale sample size (§7), most individual comparisons will already be underpowered before any correction is applied, the correction matters more for the inference scale (≈400/arm) replication than for the initial discovery run, but should be pre specified now so it isn't skipped later. Guardrail comparisons are not included in this correction family since they are treated as descriptive flags, not confirmatory tests.

### Qualitative coding plan (open feedback)

1. Two independent coders review all optional free text responses (see §5), blinded to variant where the prototype's data structure allows it.
2. Use an inductive then structured codebook: first pass generates open codes, second pass groups into themes (e.g., "distrust of sponsor motives," "confusion about data sharing," "objection to any advertising in a mental health context," "general negative valence, no specific complaint").
3. Each response is also tagged with a severity tier: none / mild / moderate / severe. "Severe" is reserved for responses indicating the participant would not use or recommend the service, or expresses acute distrust specifically tied to sponsorship (not general survey fatigue).
4. Compute inter rater agreement (Cohen's kappa); target ≥0.7 before treating codes as reliable. If below, reconcile disagreements via discussion and re code.
5. Operational rule for "recurring severe concern" (guardrail): flagged if the same severe theme appears in **3 or more independent responses within a single variant**, or in **≥10% of that variant's free text responses**, whichever threshold is reached first. This numeric operationalization is a specification recommendation, not a lead approved number, flagged for confirmation.

### Decision mapping (per hypothesis)

For each of H3a, H3b, H3c, per treatment arm vs. Control:

| Result | Definition | Decision implication |
| | | |
| **Pass (non inferiority demonstrated)** | Upper bound of the 95% CI for (Control − Variant) is below the provisional margin (5pp for continuation, 0.25 for trust/independence) | No evidence of material harm on this metric for this arm at this sample size |
| **Fail (material decline confirmed)** | Point estimate and CI show the decline meets or exceeds the margin, i.e., non inferiority is rejected | Triggers kill criterion #4 ("trust or continuation declines materially") for that arm; recommend redesign or drop of that variant, not necessarily the whole program |
| **Inconclusive** | CI straddles the margin, cannot rule out material decline, but cannot confirm it either | The expected outcome for most metrics at 75, 100/arm (see §7); should not be reported as "safe" or "harmful," only as "underpowered to conclude; directional read is [X]" |

A guardrail flag (comprehension <80%, strong majority preferring paid option, recurring severe concern, materially elevated privacy concern or opt out vs. Control) can independently support a "redesign" recommendation even where all three primary hypotheses pass, consistent with the Patient Gate in `decision_framework.md` ("no material harm to trust, booking/continuation, perceived clinical independence, retention, disclosure accuracy, or experience").

## 7. Sample Size

### Discovery vs. inference framing

Two distinct sample size regimes are specified in the brief, and they answer different questions:

* **Discovery (75, 100/arm):** sized to catch large, obvious problems and get directional reads quickly and cheaply. Not sized to formally confirm the provisional non inferiority margins.
* **Inference (≈400/arm):** sized to detect a 10 percentage point difference with conventional power, and is closer to what would be needed to make a statistically defensible non inferiority claim at the stated margins.

### Power calculation method

For a two proportion comparison (continuation rate), using the standard formula for sample size per arm:

```
n = (z_(α/2) + z_β)² × [p1(1−p1) + p2(1−p2)] / (p1 − p2)²
```

**Worked example (continuation rate):** assume baseline (Control) continuation rate p1 = 0.60, and we want to detect a 10pp decline (p2 = 0.50), at α = 0.05 two sided (z = 1.96) and 80% power (z_β = 0.84):

```
n = (1.96 + 0.84)² × [0.60×0.40 + 0.50×0.50] / (0.10)²
n = 7.84 × 0.49 / 0.01
n ≈ 384 per arm
```

This matches the brief's "≈400 participants per arm" guidance for a 10pp MDE and confirms the stated figure is internally consistent with a standard two proportion power calculation at conventional α/power settings.

**Worked example (trust score, continuous):** using `n = 2(z_(α/2)+z_β)²σ²/δ²`, assuming σ ≈ 1.0 (typical SD for a 5 point Likert item) and wanting to detect the 0.25 point margin:

```
n = 2 × 7.84 × 1.0² / 0.25²
n = 15.68 / 0.0625
n ≈ 251 per arm
```

So detecting the *trust* margin at conventional power requires fewer participants (≈251/arm) than detecting the *continuation* margin (≈384/arm) under these assumptions, continuation rate is the binding constraint on required sample size if both are to be formally tested at 80% power.

### What a 75, 100/arm test can and cannot conclude

Using n = 87 (midpoint of 75, 100) per arm:

* **Continuation rate:** standard error of the difference in proportions (assuming p ≈ 0.5 for a conservative estimate) ≈ √(2×0.5×0.5/87) ≈ 0.076. A 95% CI half width ≈ 1.96 × 0.076 ≈ **0.149 (≈15pp)**, wider than the 5pp non inferiority margin itself. **This means the discovery scale test cannot statistically confirm non inferiority at the 5pp margin.** It can reliably flag differences roughly in the 15, 20pp range or larger; anything smaller will likely land in the "inconclusive" bucket by design, not due to a flaw in execution.
* **Trust/independence score:** SE of the mean difference (σ ≈ 1.0) ≈ √(2×1²/87) ≈ 0.152; 95% CI half width ≈ 1.96 × 0.152 ≈ **0.298**, again wider than the 0.25 margin. Same conclusion: the discovery scale test is built to catch gross problems, not to certify the provisional margins statistically.
* **Practical implication:** at 75, 100/arm, treat results as **directional and diagnostic** (e.g., "Variant C shows a large, obviously concerning drop in trust and should not proceed to any live pilot" is a legitimate discovery scale conclusion; "Variant A passed non inferiority on trust" is not, unless the CI happens to be tight enough by chance, this should be checked per metric after the data is in, not assumed).
* If Variants A/B look promising directionally at discovery scale, the inference scale replication (≈400/arm) is the appropriate next step before treating H3 as formally resolved.

## 8. Privacy and Ethics

* **No PHI is collected at any point.** No diagnoses, medications, real names (beyond what a panel vendor separately manages for payment), or real health disclosures. Free text is optional, length capped, and explicitly instructed not to contain health information (§5).
* **Synthetic sponsors only.** "Sponsor X" and any Variant C healthcare/pharma sponsor must use fictitious names, not real companies, to avoid implied endorsement and to limit legal exposure (per brief §24.3 regulatory risk).
* **Research disclaimers.** Page 1 (Intro) must state: this is a concept test, no medical care is being delivered, no PHI is required, responses are for research purposes only. Page 5 (Thank You) must state: no data was shared with a sponsor, this was a research concept, and the participant's real care (if any) is unaffected.
* **Informed consent.** Standard research consent language: voluntary participation, right to withdraw at any point without penalty, contact point for questions, and confirmation that this is not a clinical interaction.
* **Data minimization.** No email collection by the prototype unless strictly required for panel incentive payment, and that should be handled by the panel vendor, not stored in Legion's/the prototype's own systems.
* **Session replay and network recording disabled** in the PostHog project configuration for this test, per §24.1 and §26.3. No third party tracking pixels in the flow.
* **Aggregate reporting only** on the admin dashboard, no participant level drill down that could re identify an individual from a small cell.

## 9. Limitations

* **Hypothetical bias.** This is a stated preference/vignette study: participants respond to a description of a hypothetical care model, not a live, consequential decision involving their own real diagnosis, medication, or clinician relationship. Stated continuation intent and stated trust may not predict real behavioral response when actual health stakes and actual money are involved (a well documented gap in contingent valuation and intention behavior research). Findings should be treated as an upper bound on comfort with the concept, not a forecast of real world uptake.
* **Panel/landing page participants vs. real patients.** Research panel participants are incentivized by payment and are often more survey experienced than the general population; landing page traffic may skew toward people already comfortable with digital health or the specific channel used to recruit them. Neither group is a validated proxy for Legion's actual prospective patient population.
* **Generalization to a real psychiatric population.** The audience is explicitly *not* current psychiatric patients (per brief §22, absent legal/clinical approval). People actively seeking or receiving psychiatric care may have systematically different trust and privacy sensitivity than a general research panel, plausibly more sensitive, given the stigma and vulnerability considerations specific to mental health. Results from this test should be treated as a screening signal, not a substitute for in population validation before any live pilot with real patients.
* **Non inferiority framing is a modeling choice, not a guarantee of interpretability at small n.** As shown in §7, most comparisons at discovery scale will be genuinely inconclusive by construction; this is a known and accepted limitation of a low cost screening design, not a defect to be explained away.
* **Fast-follows if discovery is directionally positive.** Conjoint / forced-choice research and message testing are named next steps after a positive discovery screen; they are out of scope for this low-cost concept test and should not be read as missing from the primary design.

## 10. Timeline and Cost Estimate

*(All figures are estimates for planning purposes, not commitments, actual figures depend on panel vendor pricing, incidence rate for screening criteria, and fielding speed.)*

### Discovery scale test (75, 100/arm × 4 arms = 300, 400 completes)

* **Fielding:** typically 3, 5 business days once the prototype and feature flags are live, assuming a standard panel vendor and no unusual screening incidence issues.
* **Cost:** at a typical $5, 15/complete panel rate: low end 4 × 75 × $5 = **$1,500**; high end 4 × 100 × $15 = **$6,000**. A reasonable planning midpoint is roughly **$3,000, $4,000** for 4 × 87 completes at ≈$10/complete.
* **Analysis turnaround:** 2, 3 business days for quantitative analysis plus qualitative coding (coding is the likely bottleneck if free text volume is high).

### Inference scale replication (≈400/arm × 4 arms = 1,600 completes), if discovery results warrant it

* **Fielding:** likely 1, 2 weeks depending on screening incidence and panel capacity at this volume.
* **Cost:** at $5, 15/complete: **$8,000, $24,000** for 1,600 completes.
* This step should only be run for variants that look directionally viable after discovery (i.e., not necessarily all four arms).

### Sequencing note

The PostHog event contract in §4 should be implemented and QA'd before recruitment begins, it is the integration contract the prototype must satisfy, and changing event/property names mid field would break funnel continuity between the discovery and inference runs.

## Recommendations (flagged concerns, not changes to lead approved parameters)

These are gaps or ambiguities in the lead approved spec, surfaced for lead review, not resolved unilaterally in this document:

1. **H3c (independence) has no numeric margin.** Brief §22 says "no material decline" without quantifying it. This spec proposes reusing the 0.25 point trust margin as a placeholder; needs lead confirmation.
2. **Guardrails other than comprehension have no numeric thresholds** (privacy concern, opt out rate, "strong majority" for paid option preference, "recurring" severe concern). This spec proposes working operational definitions (e.g., >50% for "strong majority," ≥3 responses or ≥10% for "recurring") purely so the test is executable; these are not lead approved numbers and should be confirmed or replaced with Legion baseline data as instructed in brief §22.
3. **Disclosure comprehension cannot be measured by the six fixed survey items alone.** A factual comprehension check item is required in addition to the self report Likert item (Q2); this adds one data point that doesn't map cleanly onto the nine approved PostHog properties. Recommend scoring it in the analysis layer rather than as a new PostHog event property, to avoid expanding the approved property list.
4. **Trust vs. independence scoring uses only one item each (Q3, Q1 respectively)** from a 6 item instrument, which limits reliability. A longer validated instrument would improve measurement precision but was not specified by the lead; flagged as a possible future refinement, not implemented here.
5. **At 75, 100/arm, none of the three primary hypotheses can be statistically confirmed against their provisional margins** (see §7). This is not a flaw in this design, but it means the discovery test should be explicitly described to stakeholders as a "large problem screen," not a validated harm test, to avoid overclaiming when results come back "no significant difference."
