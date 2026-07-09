# Assumptions & Scope Summary

**One page. Read this to see every load-bearing assumption before you challenge a number.** Full ledger: `model/legion_sponsorship_model.xlsx` tab `01_Assumptions` (low/base/high, source, confidence, status on every row). Decision tree: `decision_framework.md`. Growth reframe: `growth_contribution_analysis.md`. Uninsured TAM: `data/uninsured_population_sizing.md` (P01–P08).

## What this analysis is scoped to

| Assumption | What we assumed | Status | What would change it |
|---|---|---|---|
| **Geography** | United States; employer-benefits and FTC/OIG precedents are US-specific | Stated | Non-US expansion would need its own regulatory and pricing research |
| **Clinical focus** | AI psychiatry (Legion's actual business), not general primary care or "all Americans who see a doctor" | Stated | A different care type changes visit cadence, trust sensitivity, and CPM benchmarks |
| **"Free care" definition** | Sponsor-funded access for **uninsured patients** to a narrow, mostly-AI pathway where insurance will not pay — **not** replacing Legion's existing reimbursed FFS book | Working assumption | Legion confirms broader scope (e.g. all free clinician visits) would raise cost base and worsen ads/sponsorship |
| **Pathways compared** | Three care modes run in parallel: traditional clinician-led, AI-supported clinician, mostly AI-driven episode | Framework locked | Legion data pins A01/A02/A02b; A03b and A04 (AI cadences) remain placeholders |
| **Existing patients** | Sponsor/funder content applies **only** to the free AI pathway; reimbursed patients never see sponsor placements | Design constraint | N/A |

**Not modeled:** total US population × average doctor visits. **Modeled instead:** per-patient visit/episode frequency and an **uninsured AMI cohort** sized from Census/SAMHSA (P01–P08): ~5.9M nationally; A13 low/base/high = Legion reachable capture (25K / 150K / 750K). Detail: `data/uninsured_population_sizing.md`.

## Data from Legion

| Input | Base value used | Source |
|---|---|---|
| Traditional visit COGS (A01) | $74/visit | Legion |
| AI-supported visit COGS (A02) | $37/visit | Legion |
| AI episode cost (A02b) | ~$8/episode fully loaded | Legion (+ escalation estimate) |
| Visits per patient/yr (A03) | 5.3 base; 13.2 high | Legion |
| Net revenue per visit | $153 | Legion |
| Active patients | ~3,000 (0 uninsured) | Legion |
| CAC (A28) | $250 | Legion |
| Core-book revenue exposure (A25) | $811/yr | Derived: 5.3 × $153 |

| Input | Base value used | Still needed |
|---|---|---|
| Employer PEPM (A15) | $600/yr | Buyer interviews |
| Utilization (A21) | 55% | Buyer interviews |
| Ad sessions/patient/yr (A06b) | 52 | Product data |
| AI-supported visits/yr (A03b) | 12 | Legion / product data |
| AI-driven episodes/yr (A04) | 6 | Legion / product data |
| Eligible population (A13) | 150,000 | Census TAM + capture assumptions |
| Trust impact (A10, A11, A26) | Placeholder | Patient survey |
| Sponsorship ARPU (A05) | $15 gross → $10.50 net | Comparables + sponsor interviews |

Detail: `data/ceo_data_integration.md`.

## Revenue anchors (where headline ARPUs come from)

| Model | Mechanic | Base ARPU/patient/yr | Anchor |
|---|---|---|---|
| A | Programmatic ads | ~$1.53 | A06b sessions × A06 CPM ($20-45) × fill/take-rate |
| B | Fixed-fee sponsorship | ~$10.50 net ($15 gross) | GoodRx pharma-solutions proxy (`comparable_notes.md`) |
| C | Performance deals | Fails | Legal/steering risk; not recommended |
| D | Employer/payer underwriting | ~$330 | A15 PEPM × A21 utilization (Lyra/Spring range) |
| E | Foundation grants | ~$750 | Grant pool ÷ cohort (supplemental only) |

**Margin target:** 25% contribution margin on fully loaded cost (A14). **Formula:** required funder revenue = fully loaded cost ÷ (1 − 0.25).

## The $1B question — reframed (eventual, not six months)

```
Eventual target     ≈ $1B valuation  →  ~$100M/yr revenue at 10x (years, not this quarter)
Core engine today   ≈ 3,000 actives × ~13 visits/yr × $153 ≈ $6M/yr FFS
Core to ~$100M      ≈ ~50,000 actives at current utilization (~17x today's base)
```

**Static mechanic-only backsolve** (if one stream carried the whole company): ads ~65M patients; sponsorship ~9.5M + ~400 sponsors; underwriting ~303K covered lives. See Excel tab `04_Path_to_1B`.

**Company-level contribution as Legion grows** (the more honest frame):

| Total actives | Core FFS | Sponsor @ $10.50 (15K free-path at 50K co.) | Sponsor @ $100 WTP | Ads @ $1.53 |
|---|---|---|---|---|
| 3K (today) | ~$6M | ~$5K | ~$50K | ~$1K |
| 50K (~$100M co.) | ~$99M | ~$158K (0.16%) | ~$1.5M (1.5%) | ~$23K (&lt;0.1%) |

Detail and assumptions: `growth_contribution_analysis.md`.

**Conclusion:** Growth does not rescue ads (per-patient gap ~50x). Sponsorship can grow linearly but caps at ~1–2% of a $100M company unless WTP far exceeds the GoodRx anchor. **Core FFS + AI margin expansion + optional underwriting** is the eventual $1B path.

## Decision tree (how to follow the logic)

1. **Frame** (`decision_framework.md`): five gates (economic, commercial, patient, regulatory, strategic) and hypotheses H1-H5.
2. **Research** (`research/`, **134 sources** incl. P01–P08 population track): Lotus, comparables, regulation, uninsured sizing; every claim labeled.
3. **Model** (`model/`): compare five funding mechanics A-E per pathway; solve break-even; backsolve $1B.
4. **Falsify:** stress-test assumptions; revisions reflected in model and `assumptions_summary.md`.
5. **Test** (`30_day_plan.md`): Legion data integrated; counsel, buyer interviews, and patient survey pending.
6. **Decide** (days 27–30): proceed / modify / stop against the kill criteria in `decision_framework.md`.

**Key judgment calls:** scope (uninsured AI pathway) → model falsifies sponsorship as primary funder → employer underwriting is the stronger adjacent model → Legion operating data integrated → $1B reframed as eventual contribution → uninsured TAM from Census/NSDUH.

## Uninsured population tiers (Census + NSDUH 2024, sources P01–P08)

| Tier | Population | Estimate | Source |
|---|---|---|---|
| T0 | All uninsured (US) | ~27.5M (8.2%) | P01, P04 |
| T1 | Uninsured working-age 19–64 | ~22–23M (11.3%) | P01, P03, P05 |
| T2 | Uninsured adults with AMI | ~5.9M | P06 |
| T3 | Uninsured AMI receiving MH care/yr | ~1.5M | P06, P07 |
| T4 | Legion reachable (A13 base) | 150K (~2.5% of T2) | Analyst; `data/uninsured_population_sizing.md` |

## What would flip the recommendation

**Toward full stop:** buyer WTP clusters at EAP floor (~$36/patient/yr); patient trust test fails guardrails; counsel finds unavoidable AKS/CPOM exposure; audited costs come in at/above old external benchmarks.

**Toward sponsorship as co-funder:** sponsor WTP > ~$100/patient/yr in interviews AND episode cost stays < ~$75 (cost half already met at ~$8).

**Toward hard GO on underwriting:** commercial + patient gates pass; median qualified buyer WTP above model threshold; ≥1 paid design partner.

Kill criteria: deck slide 6, `executive_summary.md`, `experiment_spec.md`.

## What this document does not establish

No buyer interviews conducted. Patient test built and deployed but not fielded at scale. No legal conclusions. Legion cost inputs are from the company directly, not independently audited. See `methodology.md` for limitations.
