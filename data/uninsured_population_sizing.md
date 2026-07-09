# Uninsured Population Sizing — Census & Federal Survey Anchors

**Purpose:** Estimate the US uninsured population relevant to Legion's scoped question: *Can ads/sponsorship fund care for **uninsured** patients without replacing Legion's reimbursed FFS book?*  
**Date:** 2026-07-09  
**Sources:** P01–P08 in `research/sources.csv`

---

## 1. National uninsured totals (2024)

| Population | Uninsured count | Rate | Source ID |
|---|---|---|---|
| All ages (civilian, noninstitutionalized) | **≈27.5 million** | **8.2%** | P01, P04 |
| Under age 65 | **≈26.7 million** | **9.8%** | P03 |
| Adults 19–64 (working age) | **≈22–23 million** | **11.3%** | P01, P03 |
| Adults 18–64 | **≈23.1 million** | **11.6%** | P05 |
| Children under 19 | **≈4–5 million** | **5.9%** | P03 |

**Methodology note:** ACS and NHIS report **point-in-time** uninsured; CPS ASEC reports **uninsured all calendar year** (2024: **8.0%**, ≈28M — P02). This analysis uses **ACS point-in-time** as the primary anchor because it matches standard market-sizing practice and KFF's under-65 analysis.

**Derivation (working-age adults 19–64):** KFF reports 26.7M uninsured under 65 at 9.8%; children under 19 at 5.9% uninsured → ≈4.4M uninsured children → **≈22.3M uninsured adults 19–64** (residual). Cross-check: NHIS 23.1M adults 18–64 uninsured (P05).

---

## 2. Legion-relevant subset: uninsured + mental health need

Legion is **adult psychiatry telehealth**. Narrow from total uninsured using **SAMHSA NSDUH 2024** (P06, P07):

| Tier | Definition | 2024 estimate | Source |
|---|---|---|---|
| **T1** | Uninsured working-age adults (19–64) | **≈22–23M** | P01, P03, P05 |
| **T2** | Uninsured adults 18+ with **any mental illness (AMI)** | **≈5.9M** | P06 |
| **T3** | Uninsured adults 18+ with **serious mental illness (SMI)** | **≈1.6M** | P06 |
| **T4** | Uninsured adults with AMI who received MH treatment (past year) | **≈1.5M** | P06, P07 |

**T2 cross-check:** 23.4% AMI prevalence among adults 18+ (P07) × ≈23M uninsured adults ≈ **5.4M** — consistent with 5.9M (NSDUH uses model-based AMI classification; categories are non-mutually-exclusive for insurance type).

**T4 calculation:** 5.9M uninsured with AMI × **24.7%** treatment rate (P06, 2024) ≈ **1.46M**.

**Caveat (P07):** NSDUH changed mental-health treatment question wording in 2024; treatment-rate comparisons to prior years are not directly comparable. KFF cites ≈37% treatment among uninsured with any mental illness in 2023 Medicaid-comparison analysis — use **25–37%** as a sensitivity band, not a single point.

---

## 3. Mapping tiers to model assumption A13

Model row **A13** (eligible free-pathway population) is **not** total US uninsured. It is Legion's **reachable uninsured AMI cohort** over 1–3 years:

| A13 scenario | Patients | % of T2 (≈5.9M uninsured AMI) | Interpretation |
|---|---|---|---|
| **Low** | 25,000 | ≈0.4% | Pilot / single-region launch |
| **Base** | 150,000 | ≈2.5% | Moderate national telepsychiatry capture |
| **High** | 750,000 | ≈12.7% | Aggressive uninsured AMI penetration |

**Today's anchor:** ≈3,000 active patients (Legion data), **0 uninsured** (Legion confirmed 2026-07-09). Uninsured pathway is **100% incremental greenfield** — no overlap with current FFS book.

**Still open:** expected uninsured volume at 6–12 months; states Legion prioritizes; whether uninsured receive sync visits vs. AI-only continuity.

---

## 4. Uninsured-only economics (why opportunity cost differs)

For **insured** patients, sponsoring a reimbursable visit forgoes **≈$153 revenue** and **≈$79 gross profit** per visit. For **uninsured** patients, the relevant bar is **delivery COGS only**:

| Care event | Variable cost (Legion data) | Base sponsorship (≈$10.50/patient/yr) | Base ads (≈$1.53/patient/yr) |
|---|---|---|---|
| AI continuity episode | **≈$8/episode** (≈$48/yr @ 6/yr) | ≈13% of ≈$78/yr break-even | Fails |
| AI-leveraged sync visit | **≈$37/visit** | Fails unless per-visit priced | Fails |
| Full sync visit | **≈$74/visit** | Fails unless per-visit priced | Fails |

At **A13 base (150K uninsured pathway patients)** with AI continuity costing ≈$48/yr:
- Care delivery ≈ **$7.2M/yr**
- Sponsorship @ $10.50 ≈ **$1.6M/yr** (≈17% of delivery cost — better than insured-replacement frame, still not full funding)
- Ads @ $1.53 ≈ **$230K/yr**

---

## 5. Source ledger (P01–P08)

| ID | Title | Publisher | Date | URL |
|---|---|---|---|---|
| **P01** | Health Insurance Coverage by State: 2023 and 2024 | U.S. Census Bureau (ACS) | 2025 | https://www2.census.gov/library/publications/2025/demo/acsbr-024.pdf |
| **P02** | Health Insurance Coverage in the United States: 2024 | U.S. Census Bureau (CPS ASEC) | 2025 | https://www2.census.gov/library/publications/2025/demo/p60-288.pdf |
| **P03** | Key Facts about the Uninsured Population | KFF (ACS analysis) | 2026-06-16 | https://www.kff.org/uninsured/key-facts-about-the-uninsured-population/ |
| **P04** | Comparing Federal Government Surveys That Count the Uninsured: 2025 | SHADAC | 2026 | https://www.shadac.org/comparing-federal-government-surveys-count-uninsured-2025 |
| **P05** | Health Insurance Coverage: NHIS Early Release 2024 | CDC/NCHS | 2025-06 | https://www.cdc.gov/nchs/data/nhis/earlyrelease/insur202506.pdf |
| **P06** | NSDUH 2024 Detailed Tables §6 (AMI/SMI by insurance) | SAMHSA | 2024 | https://www.samhsa.gov/data/report/2024-nsduh-detailed-tables |
| **P07** | NSDUH 2024 Detailed Tables §6.8B (AMI prevalence) | SAMHSA | 2024 | https://www.samhsa.gov/data/report/2024-nsduh-detailed-tables |
| **P08** | ACS Table S2701 — Health Insurance Coverage Characteristics | U.S. Census Bureau | 2024 | https://data.census.gov/table/ACSST1Y2024.S2701 |

Full excerpts and evidence-type labels: `research/sources.csv`.

---

## 6. What would change these estimates

- **Legion data:** insured/uninsured patient mix and uninsured visit volume
- **State scope:** Legion's licensed states (concentrates T2 into smaller geography)
- **Medicaid/policy shifts:** CBO projects increased uninsured after 2025 reconciliation law (P03) — T1 could grow
- **Service definition:** If "uninsured pathway" includes underinsured (high deductible, no mental health benefit), T2 expands beyond P06 "No Coverage" category
