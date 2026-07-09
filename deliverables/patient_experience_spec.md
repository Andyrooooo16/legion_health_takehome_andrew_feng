# Patient Experience and Sponsorship Guardrails

**One page. Founder-facing product picture of where sponsorship can and cannot live.** Companion sources: `sponsor_test_package.md` §§1, 6 · deck.html slide 6 · `experiment_spec.md`.

## Where sponsorship lives

Only inside the free AI-enabled care pathway. Existing reimbursed patients never see sponsor content. Three placements only:

1. **Pathway entry screen:** a PBS-style credit: "Access supported by [Sponsor]."
2. **Optional sponsored-education module:** a clearly bounded, labeled resources section (Package C), never inside the clinical chat or care plan.
3. **One-line footer on care summaries:** name/logo attribution only.

Nothing else. No banners in the session, no interstitial ads, no product CTAs adjacent to clinical output.

## Where it never appears

Inside clinical conversation, assessments, prescription or medication flows, crisis/safety flows, or any clinician-facing surface. Sponsor content is never adjacent in time or visual proximity to a recommendation or diagnosis.

## Frequency and control

Occasional, not persistent: at most one sponsor placement per session. Patients can dismiss any sponsored module; a full opt-out is honored; a sponsor-free paid alternative is offered. Opt-out and disclosure comprehension are test guardrails in `experiment_spec.md`.

## Visual separation

Sponsor content sits on a visually distinct surface with an explicit "Sponsored" label, different from clinical typography, and never adjacent to a recommendation or diagnosis. The design intent matches Package B/C in the test package: association and education, not clinical adjacency.

## Category rules

Summarized from `sponsor_test_package.md` §6 (do not contradict):

| Status | Categories |
| | |
| **Acceptable** | Non-endemic corporates (CSR/ESG style); health-adjacent consumer brands with no prescription product; foundations; employers funding their own employees (Model D, tracked separately) |
| **Conditional (counsel first)** | Pharma disease-awareness / education budgets (Package C only); payers acting as sponsors rather than contracted payers |
| **Excluded** | Branded drug ads; anything requiring diagnosis-level or patient-level targeting; any data return that enables patient or provider identification |

## Governance

Hard constraints (non-negotiable, same spirit as deck slide 6):

1. Funders receive zero patient-level data, ever.
2. No funder influence on clinical decisions.
3. No prescription- or referral-linked economics.
4. No capitated per-patient risk while costs are unaudited.
5. No third-party ad-tech in care flows; session replay off.

Add: a clinical-content firewall (sponsor never sees, shapes, or adjoins clinical content), and disclosure comprehension is a test guardrail (at least 80%).

## Design principle

The sponsorship is on the door, never in the room.
