# Methodology

How this analysis was produced, what it can support, and what was not done.

## Approach

1. Frame the decision (five gates, five funding models, kill criteria)
2. Research comparable models, regulation, and market sizing
3. Build a unit economics model
4. Stress-test assumptions and update when Legion shared operating data
5. Design a validation plan for the open questions

Legion provided cost, visit, revenue, and CAC figures mid-assignment; I integrated them into the model the same day (`data/ceo_data_integration.md`).

**Reader map:** `assumptions_summary.md` · `decision_framework.md` · `open_questions.md` · `data/uninsured_population_sizing.md`

## Research

Four tracks: Lotus Health AI, comparable business models, regulatory constraints, uninsured population sizing. **134 sources** logged in `research/sources.csv` with publisher, date, URL, and evidence type. Preference order: official company materials → government/regulatory → primary product artifacts → industry publications → third-party estimates.

Lotus private metrics (conversion, sponsor revenue, contracts) were treated as unknowable. A dedicated search documented employer/payer failures (Pear, Mindstrong, Babylon) to avoid survivorship bias on the underwriting comparison.

## Model

Python implementation mirrored by an Excel workbook (`legion_sponsorship_model.xlsx`). Unit tests cover formula correctness and scenario ordering. Every input has low/base/high values with source notes in `assumptions.csv`.

Legion's figures ($74/visit, $37 AI-supported, ~$8 AI episode, 5.3 visits/patient, $153/visit, CAC $250) are the cost basis. External benchmarks fill gaps where Legion data was not available (employer PEPM, sponsor ARPU, ad CPMs).

## Proposed validation (not yet fielded)

- **Buyer side:** 15–20 interviews, Van Westendorp pricing, qualification scorecard
- **Patient side:** Randomized 4-arm concept test with guardrails (≤5pp continuation decline, ≤0.25 trust decline, ≥80% disclosure comprehension)
- **Prototype:** Next.js survey deployed at the live URL; no PHI, session replay off

## Limitations

- No buyer interviews conducted (top model sensitivity is employer PEPM)
- Patient survey built but not fielded at scale
- Legion cost inputs are from the company, not independently audited
- No legal conclusions — regulatory research produces questions for counsel, not answers
- Comparability caveats: Lyra/Spring PEPM prices broad benefits; physician CPMs don't transfer to patients

## Privacy

No PHI in any artifact. Aggregate-only reporting for funders. Synthetic data in the prototype.
