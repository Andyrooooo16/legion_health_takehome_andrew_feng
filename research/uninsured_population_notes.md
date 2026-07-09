# Uninsured Population Research Notes

**Track:** Population sizing (fourth research track, added 2026-07-09)  
**Purpose:** Anchor model assumption **A13** and the uninsured-only scope for ads/sponsorship analysis.  
**Detail doc:** `data/uninsured_population_sizing.md`  
**Sources:** P01–P08 in `sources.csv`

---

## Headline numbers (2024 federal data)

1. **≈27.5M** Americans uninsured at a point in time (**8.2%**) — ACS (P01, P04)
2. **≈26.7M** under age 65 uninsured (**9.8%**) — KFF ACS analysis (P03)
3. **≈22–23M** working-age adults 19–64 uninsured (**11.3%**) — ACS/KFF (P01, P03); NHIS 18–64: 23.1M (P05)
4. **≈5.9M** uninsured adults 18+ with any mental illness — NSDUH 2024 Table 6.3A (P06)
5. **≈1.5M** uninsured adults with AMI who received mental health treatment in past year — NSDUH 2024 (P06, P07)

---

## Implications for Legion case

| Finding | Implication |
|---|---|
| Uninsured TAM is **millions**, not thousands | Sponsorship/ads scale with patients, but per-patient ARPU stays tiny |
| Psychiatry-relevant slice ≈ **6M** (uninsured + AMI) | A13 base 150K = ≈2.5% capture — reasonable 1–3 yr target, not conservative for TAM |
| Uninsured have **no $153 opportunity cost** | Compare sponsor revenue to **$8–$74 COGS**, not reimbursement |
| Treatment rate among uninsured AMI **≈25%** | Near-term serviceable demand ≈ **1.5M**, not full 5.9M |
| CEO never returned insured/uninsured mix | Cannot calibrate Legion's current uninsured volume; Q07 remains partially open |

---

## Survey comparability warnings

- **ACS vs CPS vs NHIS** use different uninsured definitions (point-in-time vs full-year; question wording). Do not blend counts without labeling (P04).
- **NSDUH 2024** mental-health treatment estimates are **not comparable to 2023** due to questionnaire changes (P07).
- **AMI/SMI** in NSDUH are **model-predicted**, not clinical diagnoses (P06).

---

## Model linkage

- **A13** updated in `model/assumptions.csv` with P01–P08 derivation note
- **Q07** in `open_questions.md` — partially resolved on national TAM; Legion-specific mix still open
- See `data/uninsured_population_sizing.md`
