# Legion operating data

Numbers provided by Legion during the assignment. I used these as the base case in the model (`model/assumptions.csv`, tab `01_Assumptions` in the Excel workbook).

## Inputs received

| # | What Legion shared | Model assumption | Value used (base) |
|---|---|---|---|
| 1 | Active patients (visit in past 3 months) | A13 context | ~3,000 (0 uninsured) |
| 2 | Visits per active patient per month (continuously engaged) | A03 high | ~13/yr |
| 3 | Historical average visits per patient | A03 base | 5.3/yr |
| 4 | Net revenue per completed visit | A25 | $153 |
| 5 | Provider COGS per synchronous visit | A01 | $74 |
| 6 | AI leverage (2x) → COGS per AI-supported visit | A02 | $37 |
| 7 | Token cost per AI renewal/review | A02b (base) | ~$1 compute; ~$8 fully loaded with escalation |
| 8 | Customer acquisition cost | A28 | $250 |
| 9 | LTV/CAC (mature cohorts) | A29, A30 | 8.1x booked / 4.2x gross margin |

## What changed in the analysis

Once I plugged these in, break-even costs dropped sharply versus the external benchmarks I had been using:

| Pathway | Old break-even (benchmark costs) | New break-even (Legion costs) |
|---|---|---|
| Mostly AI-driven | ~$299/patient/yr | ~$79 |
| AI-supported | ~$1,459 | ~$607 |
| Traditional | ~$1,619 | ~$538 |

**Sponsorship:** Still insufficient as a primary funder at the ~$10.50/patient/yr industry anchor (~13% of break-even on the AI pathway), but the gap narrowed enough that sponsorship is worth testing as a co-funder.

**Employer underwriting (Model D):** Strengthened materially — $330 ARPU vs. ~$79–$116 break-even on the AI pathway.

**Free care as acquisition:** A free AI episode costs ~$8 to deliver vs. ~$250 CAC. At ~3.2% free-to-paid conversion, the economics break even — a separate reason to run the pilot, independent of sponsor revenue.

## Open items

Legion did not provide AI-pathway visit frequencies (A03b, A04) — those remain estimates. Trust/spillover assumptions (A10, A11, A26) still need the patient survey. Employer PEPM and utilization (A15, A21) need buyer interviews.
