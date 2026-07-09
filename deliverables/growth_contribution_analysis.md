# Growth & Contribution Analysis — Reframing the $1B Question

**Purpose:** The assignment asks whether ads/sponsorship can fund free care and support a **$1B valuation** — not whether Legion hits $1B in six months. This document reframes the analysis using Legion's operating data: **as Legion grows over time, does each monetization mechanic become a meaningful contributor to an eventual ~$100M revenue company (~$1B at 10x)?**

**Legion inputs used (2026-07-08):**

| Input | Value |
|---|---|
| Active patients | ~3,000 (visit in past 3 months) |
| Active utilization | ~1.08–1.13 completed visits / active patient / month (~13/yr) |
| Historical avg utilization | ~5.3 completed visits / patient (lifecycle average) |
| Net revenue per visit | ~$153 |
| Provider COGS per sync visit | ~$74 today → ~$37 at 2x AI leverage |
| Visit-level gross margin | ~52–53% today → ~76% on leveraged path |
| AI renewal token cost | ~$1 per renewal/review |
| CAC | ~$250 |
| Mature cohort LTV/CAC | ~8.1x booked (~$2,025 LTV) / ~4.2x GM (~$1,050 GM LTV) |

Full integration: `data/ceo_data_integration.md`.  
Uninsured TAM: `data/uninsured_population_sizing.md` (sources P01–P08).

---

## 2a. Uninsured population anchor (Census + NSDUH 2024)

**Scope:** Ads/sponsorship tested for **uninsured patients only** — not replacing Legion's reimbursed FFS book.

| Tier | Estimate | Source |
|---|---|---|
| All uninsured (US) | ~27.5M (8.2%) | P01, P04 |
| Uninsured working-age 19–64 | ~22–23M (11.3%) | P01, P03, P05 |
| Uninsured adults with any mental illness (AMI) | ~5.9M | P06 |
| Uninsured AMI receiving MH treatment/yr | ~1.5M | P06, P07 |
| Model A13 base (Legion reachable capture) | **150K** (~2.5% of AMI uninsured) | Analyst |

**Uninsured economics differ from insured:** no **$153/visit** opportunity cost — sponsor revenue is compared to **COGS only** (~$8 AI episode to ~$74 sync visit). See `data/uninsured_population_sizing.md` §4.

---

## 1. What "$1B" actually means here

```
Eventual valuation target     ≈ $1B
Typical digital-health multiple ≈ 10x revenue (tested at 5x–20x in model)
Implied eventual revenue need  ≈ $100M / year (at 10x)
Time horizon                   Years, not six months
```

The six-month recommendation is **whether to invest in building** ads/sponsorship infrastructure **now**, before the patient base scales — not whether sponsorship alone carries Legion to $1B this year.

---

## 2. Legion's core engine today (the baseline everything else sits on)

**Active-cohort revenue run-rate (CEO math):**

```
3,000 actives × ~1.1 visits/mo × 12 × $153/visit ≈ $6.0M / year gross booked revenue
```

**Per active patient per year:** ~13 visits × $153 ≈ **$1,989/yr** (mature/active run-rate)

**Per historical-average patient:** 5.3 × $153 ≈ **$811/yr** (used for trust-contagion exposure in model)

**Gross margin today:** ~52–53% on $74 COGS → path to **~76%** at $37 COGS with AI leverage.

**This is the growth engine that actually reaches $100M:** at constant utilization and pricing, roughly **~50,000 active patients** gets core booked revenue to ~$100M/yr (50K × $1,989). That is ~17x today's 3,000 actives — aggressive but structurally different from the 65M patients ads would need on their own.

---

## 3. Unit economics of the free AI pathway (what sponsors would fund)

| Cost component | CEO-based value |
|---|---|
| AI episode fully loaded (A02b) | ~$8/episode (base) |
| Episodes per patient/yr (A04 placeholder) | 6 base |
| Annual care cost per free-pathway patient | ~$48–$79 fully loaded (pathway-dependent) |
| Break-even funder revenue (25% margin) | ~$79–$167/patient/yr depending on mechanic |

**Free care as acquisition (independent of sponsorship):**

```
Free AI episode cost  ≈ $8
Paid CAC              ≈ $250
Break-even if         ≈ 3.2% of free users convert to paid reimbursed care
```

As Legion grows, a free AI tier can **feed the core $6M engine** even if no sponsor pays — this is a growth lever the original "can ads fund care?" frame underweights.

---

## 4. Revenue per patient by mechanic (unchanged from model — scales linearly with patients)

| Mechanic | $/patient/yr (base) | Scales with patient growth? |
|---|---|---|
| A. Programmatic ads | ~$1.53 | Yes — linear, but tiny per head |
| B. Brand sponsorship | ~$10.50 net ($15 gross) | Yes — linear |
| B. (if WTP trigger fires) | ~$100+ | Yes — testable in interviews |
| D. Employer underwriting | ~$330 effective | Yes — per covered life |
| Core FFS (reimbursed) | ~$1,989/active/yr | Yes — this is the main engine |

**Key insight:** All mechanics scale linearly with patients. The question is **what % of company revenue** each becomes at realistic scale — not whether static 3,000-patient math works today.

---

## 5. Contribution at growth milestones

Assumptions for this table:
- Core revenue scales with active patients at **$1,989/patient/yr** (13 visits × $153).
- Free AI pathway patients = **30% of actives** at scale (analytic placeholder; CEO to confirm). At 3K today, illustration uses **500** on free pathway (pilot-scale).
- Sponsorship ARPU = **$10.50/yr** base; **$100/yr** = co-funder threshold from interviews.
- Ads ARPU = **$1.53/yr** base.

| Total actives | Core FFS revenue | Free-pathway patients (illustrative) | Sponsor rev @ $10.50 | Sponsor rev @ $100 | Ads @ $1.53 | Sponsor as % of core |
|---|---|---|---|---|---|---|
| **3,000** (today) | **~$6.0M** | 500 | $5.3K | $50K | $765 | **0.09%** |
| **10,000** | **~$20M** | 2,000 | $21K | $200K | $3.1K | **0.1%** |
| **30,000** | **~$60M** | 8,000 | $84K | $800K | $12K | **0.14%** |
| **50,000** (~$100M core) | **~$99M** | 15,000 | $158K | $1.5M | $23K | **0.16%** |

**Employer underwriting at scale (different mechanic — B2B lives covered):**

| Covered lives (underwritten) | Revenue @ $330/patient/yr | As % of $100M company |
|---|---|---|
| 10,000 | $3.3M | 3.3% |
| 50,000 | $16.5M | 16.5% |
| 303,000 (model $1B backsolve on underwriting alone) | $100M | 100% (underwriting-only story) |

---

## 6. Revised answers to the three assignment questions

### Q1: Viable strategy for eventual $1B?

**Ads (Model A):** No as a **primary contributor**. At base engagement, even at 50K actives on the free pathway, ads produce ~$23K against ~$99M core — **0.02%**. To make ads alone = $100M revenue requires **~65M patients** at $1.53 ARPU regardless of growth rate. Growth does not fix a 40–50x per-patient gap without a simultaneous engagement/CPM revolution (model tests this at 450 sessions/yr — see below).

**Sponsorship (Model B):** No as **primary funder of free care** or **primary path to $1B**. At 50K company actives, base sponsorship contributes **~0.16%** of revenue. Even at **$100/patient** co-funder WTP on 15K free-pathway patients, **~1.5%** of a $100M company.

**Brand partnerships:** Same economics as Model B unless WTP proves otherwise (buyer interviews).

**Employer underwriting (Model D):** The only alternative mechanic that can contribute **double-digit %** of a $100M revenue base at achievable covered-life counts (50K–300K). Honestly labeled as an **adjacent** B2B mechanic, not sponsorship.

**Eventual $1B path (revised):** Core FFS growth (~17x actives from today with margin expansion) **plus** optional employer underwriting **plus** free AI as CAC — **not** ads/sponsorship as the engine.

### Q2: Biggest risks (unchanged in substance)

Economic, regulatory, trust, strategic distraction — see deck slide 6. New emphasis: **misallocating six months of build toward a stream that caps at ~1–2% of revenue at scale** even if sponsor WTP exceeds expectations.

### Q3: Cheap test — reframed

The test is **not** "reach $1B in 30 days." It is:

1. **Before the patient base scales**, resolve: Will sponsors pay enough to **co-fund** free care (not fully fund)? Will patients accept it?
2. **Falsify** the sponsorship co-funder trigger ($100/patient WTP) and trust guardrails.
3. **In parallel**, test employer PEPM for a material contributor path.

**What the test does for ads/sponsorship specifically:**
- Sponsorship: buyer WTP interviews + patient trust survey (**yes**).
- Ads: no live ad pilot recommended — gap is ~50x at base; even at 50K actives, contribution is immaterial. Optimistic model edge (450 sessions/yr, high CPM, CEO costs) yields **+$36/patient/yr** on AI pathway only — flagged, not adopted; would still need ~2.3M free-pathway patients for $100M ads-only revenue at $43.74 ARPU.

---

## 7. Optimistic ads scenario (why we don't rule it out without nuance)

Red-team widened engagement to **450 sessions/patient/yr** (~daily use). With CEO costs, **all-best-case stacked**:

| Metric | Value |
|---|---|
| Model A ARPU (high scenario, AI pathway) | ~$43.74/patient/yr |
| Break-even | ~$10.78/patient/yr |
| North-star margin | **+$35.65/patient/yr** |

This does **not** change the primary recommendation. It requires simultaneous best-case engagement, CPM, fill, and cost — a product transformation, not a monetization tweak. At that ARPU, $100M ads revenue needs **~2.3M** free-pathway patients, not 65M — still large, but acknowledges growth + engagement could theoretically matter **if** Legion becomes a daily-use ambient AI product. That hypothesis is **untested** and **not** assumed in the six-month recommendation.

---

## 8. Revised six-month recommendation

| Decision | Rationale |
|---|---|
| **NO-GO:** Build ad platform as path to eventual $1B | Contribution caps at ~0.02% of revenue at 50K-actives scale; 65M-patient backsolve is not a growth trajectory Legion is on |
| **NO-GO:** Build sponsorship as **primary funder** of free care | ~7x gap to break-even at base WTP; cannot carry $100M revenue story |
| **MAYBE (test first):** Lightweight sponsorship on free AI pathway | Could contribute 1–2% of revenue at scale if WTP > $100; co-funds ~$8 episodes; scales with patient growth — **if** trust and WTP tests pass |
| **CONDITIONAL GO:** Employer fee-for-benefit underwriting | Only mechanic that can contribute double-digit % at achievable scale |
| **YES (already happening):** Free AI as CAC offset | $8 episode vs $250 CAC; feeds core $6M → $100M engine regardless of sponsors |

---

## 9. What would change this revised conclusion

- **Sponsor interviews:** median WTP > $100/patient on 1K+ cohort → sponsorship moves from "maybe" to "pilot co-funder layer."
- **Patient test:** trust guardrails pass → safe to scale sponsorship with patient growth.
- **Product data:** sustained 200+ sessions/patient/yr with health-vertical CPMs → reopen ads as secondary stream (not six-month build).
- **Employer interviews:** PEPM clears threshold → underwriting becomes parallel material contributor.

---

## 10. Link to model artifacts

- Unit economics grid: `model/outputs.csv`, Excel tabs `02–03`
- Static $1B backsolve (mechanic-only story): Excel tab `04_Path_to_1B`
- This document: **company-level contribution** over growth milestones using Legion data
- Uninsured TAM: `data/uninsured_population_sizing.md` · Research notes: `research/uninsured_population_notes.md`
- Assumptions: `assumptions_summary.md` · Decision tree: `decision_framework.md`
