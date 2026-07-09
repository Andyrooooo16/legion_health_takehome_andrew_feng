# Legion Sponsorship Case — Quantitative Model

Transparent unit-economics model for three care pathways and five monetization models (A–E), aligned with `deliverables/decision_framework.md`. Legion provided operating data mid-assignment (`data/ceo_data_integration.md`); those figures are the cost basis. External benchmarks fill gaps where Legion data was not available.

## Files

| File | Purpose |
|---|---|
| `assumptions.csv` | Every input with low/base/high, source, confidence, status |
| `model.py` | Pathway cost, fully loaded cost, Models A–E, north star, valuation backsolve |
| `scenarios.py` | Low/base/high scenarios → `outputs.csv`, `funnel_lens.csv` |
| `sensitivity.py` | Tornado sensitivity → `sensitivity_outputs.csv` |
| `tests/test_model.py` | Formula and ordering checks (71 tests) |
| `build_excel.py` | Generates `legion_sponsorship_model.xlsx` |
| `legion_sponsorship_model.xlsx` | Editable Excel companion (6 tabs, live formulas) |

## How to run

```bash
cd model/
python3 scenarios.py      # outputs.csv + funnel_lens.csv
python3 sensitivity.py    # sensitivity_outputs.csv
python3 -m pytest tests/test_model.py -v
python3 build_excel.py    # regenerate workbook
```

Edit `assumptions.csv` and rerun the scripts above to refresh all outputs.

## Formula summary

- **Care delivery cost** = cost per unit × units per patient/yr (per pathway)
- **Fully loaded cost** = care delivery + servicing + commercial + compliance + trust churn + core-book contagion
- **Required sponsor revenue** = fully loaded cost / (1 − target margin); base margin 25%
- **North star** = sponsor revenue − all costs above (negative values are not masked)
- **Valuation backsolve** = $1B target ÷ revenue multiple → required revenue → required patients
- **Free-care acquisition break-even** = AI episode cost (A02b) / CAC (A28)

## Data sources

**From Legion:** A01 ($74/visit), A02 ($37/visit), A02b (≈$8/episode fully loaded), A03 (5.3 visits/yr base / 13.2 high), A25 ($811–$2,025 revenue exposure), A28 (CAC $250), A29/A30 (LTV:CAC ratios). See `data/ceo_data_integration.md`.

**Still estimated:** A03b/A04 (AI pathway cadence), A10/A11/A26 (trust impact), A15/A21 (employer PEPM), A05–A07 (sponsor-side), A13 range (reachable uninsured population).

## Headline findings (base case, Legion costs)

| Pathway | Fully loaded cost | Break-even ARPU @ 25% margin | Gap vs $15 sponsor anchor |
|---|---|---|---|
| Traditional | $403/patient/yr | $538 | −$523 |
| AI-supported | $455 | $607 | −$592 |
| Mostly AI-driven | $59 | $79 | −$64 |

Legion's costs are 58–74% below the external telehealth benchmarks used initially. Break-evens fell accordingly, but the qualitative conclusion holds: **only employer underwriting (Model D) and foundation grants (Model E) clear break-even at base case** on the AI-driven pathway. Ads (A) and fixed-fee sponsorship (B) remain far short.

**Model D (employer PEPM):** $330 ARPU vs ≈$79 break-even on AI-driven pathway → +$243 north star.

**Model B (sponsorship):** $15 anchor covers ≈19% of AI-driven break-even — worth testing as co-funder, not primary funder.

**Free care as acquisition:** ≈$8 episode cost vs $250 CAC → break-even at ≈3.2% free-to-paid conversion.

## Known tension

Legion provided traditional-pathway visit frequency (A03) but not AI-pathway frequencies (A03b, A04). With A03b still at 12 visits/yr (placeholder), the AI-supported pathway's *annual* cost ($455) exceeds traditional ($403) even though per-visit costs are correctly ordered ($74 > $37 > $8). Resolving A03b/A04 is the highest-priority remaining data ask.

## Sensitivity (top drivers)

1. A15 — Employer PEPM ($2,084 swing)
2. A21 — Employer utilization ($273)
3. A02 — AI-supported visit cost ($156; partly inflated by stale A03b)
4. A02b — AI episode cost ($138)
5. A11 — Trust retention loss ($105)

## Version history

- **v1:** External benchmark placeholders
- **v2 (2026-07-07):** Core-book contagion term (A26), widened ad engagement ceiling, Model E grantor backsolve
- **v3 (2026-07-08):** Legion operating data integrated; funnel-lens added; Excel formula bugs fixed
