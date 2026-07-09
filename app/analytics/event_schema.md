# Event Schema, Patient Side Sponsorship Concept Test

This is the PostHog integration contract implemented by the prototype, copied and
adapted from `deliverables/experiment_spec.md` §4 (the frozen funnel definition). It is
a **contract, not a proposal**, event names, triggers, and property sets below match
the spec exactly. Nothing here redefines or extends that contract; where the prototype
needed to hold additional data (e.g., free text, the comprehension check) that data is
explicitly marked "not sent to PostHog" and kept out of the analytics pipeline.

Implementation: `src/lib/analytics.ts` (typed `capture()` wrapper, one interface per
event so a call site cannot attach a disallowed property), `src/lib/participant.ts`
(assignment/`concept_assigned`), and the five page components under `src/app/`.

## Allowed property values

* `variant`: `control` | `variant_a` | `variant_b` | `variant_c`
* `sponsor_category`: `none` | `consumer_health` | `pharma`
* `participant_type`: `panel` | `landing_page` | `admin`
* `decision_result`: `continue` | `opt_out` | `exit`
* `trust_score`, `independence_score`, `privacy_concern`, `continuation_intent`: numeric, 1, 5
* `opt_out`: boolean

No event carries any property outside these plus standard PostHog defaults (timestamp,
distinct_id, URL). Session replay and network recording are disabled at PostHog init
(`disable_session_recording: true`, `autocapture: false`, `capture_pageview: false` in
`src/lib/analytics.ts`), no third party tracking pixels are used anywhere in the flow.

## Events

| Event | Trigger | Required properties | Optional properties | Privacy classification | Dashboard use |
| | | | | | |
| `concept_assigned` | Fires the instant the sticky client side assignment resolves a variant for this `distinct_id`, before Page 2 (Sponsorship Concept) renders. Fires once per participant per test window. Implemented on Page 1 (Intro) mount. | `variant`, `sponsor_category`, `participant_type` |, | No PHI. Anonymous distinct_id only. | Denominator for intent to treat funnel analysis (assignment logged even if participant drops off before viewing content). |
| `concept_viewed` | Fires when Page 2 (Sponsorship Concept) has fully mounted and content is on screen (on mount is spec acceptable for this single viewport page). | `variant`, `sponsor_category`, `participant_type` |, | No PHI. | Exposure count per arm (denominator for continuation rate, opt out rate). |
| `learn_more_clicked` | Participant clicks "Learn more" on Page 3 (Behavioral Action). Does not end the funnel. | `variant`, `sponsor_category`, `participant_type` |, | No PHI. | Engagement rate by arm (secondary/descriptive). |
| `privacy_details_opened` | Participant clicks "View privacy details" on Page 3. | `variant`, `sponsor_category`, `participant_type` |, | No PHI. | Engagement rate by arm (secondary/descriptive); proxy for privacy salience. |
| `continue_clicked` | Participant selects "Continue" on Page 3. | `variant`, `sponsor_category`, `participant_type`, `decision_result="continue"` |, | No PHI. | Primary behavioral proxy for **continuation rate** (H3a). |
| `sponsor_opt_out_selected` | Participant selects "Choose sponsor free option" **or** "Exit" on Page 3. Both map to `opt_out=true`; `decision_result` distinguishes which. | `variant`, `sponsor_category`, `participant_type`, `decision_result` (`"opt_out"` or `"exit"`), `opt_out=true` |, | No PHI. | Opt out rate guardrail; "exit" additionally causes the survey to be skipped entirely. |
| `survey_started` | Page 4 (Trust Survey) mount, only for participants who did not select "Exit" at Page 3. | `variant`, `participant_type` |, | No PHI. | Survey start rate; denominator check against `concept_viewed` for drop off between action and survey. |
| `survey_submitted` | Participant submits the Page 4 survey. | `variant`, `participant_type`, `trust_score`, `independence_score`, `privacy_concern`, `continuation_intent`, `opt_out` |, | No PHI. Scores are derived from Likert responses (1, 5), not free text. | Source of H3b (trust), H3c (independence), and the privacy concern guardrail; `opt_out` cross checked against Page 3 behavioral opt out. |
| `booking_intent_selected` | Fires alongside `survey_submitted` when Q5 ("I would continue using the service") is dichotomized Agree/Strongly Agree (score ≥ 4), stated intent, distinct from the Page 3 behavioral `continue_clicked`. | `variant`, `participant_type`, `continuation_intent` |, | No PHI. | Lets analysis compare **revealed** (behavioral) vs. **stated** (survey) continuation. |
| `results_viewed` | Admin loads `/admin`. | `participant_type="admin"` |, | No PHI; admin only event. | Usage tracking for the dashboard itself, not a participant metric. |
| `scenario_exported` | Admin clicks "Export CSV" on `/admin`. | `participant_type="admin"`, `variant` (selected filter, or `"all"`) |, | No PHI; admin only event. | Usage tracking; audit trail of what scope was exported and when. |

Page 5 (Thank You) intentionally fires **no named event**, per the spec's funnel table
("no event required; optionally log page view via default PostHog pageview capture, not
a named funnel event"). The prototype does not add a pageview capture either, since
`capture_pageview` is explicitly disabled at init to keep the event stream limited to
the funnel above.

## Data collected outside PostHog (explicitly NOT event properties)

Per `experiment_spec.md` §5, the following are captured for the admin dashboard's
descriptive/guardrail stats but are deliberately **not** attached to any PostHog event,
to stay within the nine property allow list above:

| Field | Source | Where it lives |
| | | |
| Q2 self reported comprehension ("I understand the sponsor's role") | Survey item | Local participant record only (`src/lib/storage.ts`) |
| Q6 preference for a paid sponsor free option | Survey item | Local participant record only |
| Disclosure comprehension check (factual, correct/incorrect) | Survey item (flagged addition, see §5) | Local participant record only |
| Optional free text concern | Survey item, capped at 280 characters | Local participant record only; used for the qualitative coding plan in spec §6, never sent to analytics |

## Explicit exclusions

No diagnoses, medications, real names, email addresses, PHI, free text health
disclosures, or session replay are captured anywhere in this prototype, per
`experiment_spec.md` §4 and §8.
