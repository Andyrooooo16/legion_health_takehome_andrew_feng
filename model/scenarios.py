"""
Legion Health Sponsorship Case — Scenario Runner
==================================================

Loads model/assumptions.csv, builds coherent low/base/high scenarios
(low = pessimistic revenue + high cost; high = optimistic revenue + low
cost; base = base-case for every assumption), runs all three pathways x
all five monetization models through model.py, and writes
model/outputs.csv with a scenario x pathway x model grid.

Run: python3 scenarios.py
"""

import csv
import os
from typing import Dict

import model as m

HERE = os.path.dirname(os.path.abspath(__file__))
ASSUMPTIONS_CSV = os.path.join(HERE, "assumptions.csv")
OUTPUTS_CSV = os.path.join(HERE, "outputs.csv")
FUNNEL_LENS_CSV = os.path.join(HERE, "funnel_lens.csv")

SCENARIOS = ("low", "base", "high")
TARGET_VALUATION_USD = 1_000_000_000.0


def load_assumptions() -> Dict[str, Dict[str, str]]:
    """Load assumptions.csv into {assumption_id: row_dict}."""
    rows = {}
    with open(ASSUMPTIONS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows[row["assumption_id"]] = row
    return rows


def val(rows: Dict[str, Dict[str, str]], aid: str, scenario: str) -> float:
    """
    Fetch a numeric value for assumption id `aid` at a given scenario
    ("low"/"base"/"high"), raising clearly if the cell is a placeholder
    string rather than a resolved number (all our placeholders in
    model/assumptions.csv carry numeric external-benchmark or
    analytic-placeholder values, so this should always succeed; the
    guard exists to fail loudly rather than silently coerce a stray
    "PLACEHOLDER" string to 0).
    """
    raw = rows[aid][scenario]
    try:
        return float(raw)
    except ValueError as e:
        raise ValueError(
            f"Assumption {aid} scenario={scenario} is not numeric ({raw!r}); "
            "resolve in assumptions.csv before running scenarios."
        ) from e


def pct01(rows: Dict[str, Dict[str, str]], aid: str, scenario: str) -> float:
    """Fetch a value stored as 0-100 in assumptions.csv and return as 0-1 fraction."""
    return val(rows, aid, scenario) / 100.0


# ---------------------------------------------------------------------------
# Coherent scenario direction map.
#
# "low" scenario = pessimistic revenue (low ARPU/eCPM/etc.) + high cost
#   (high care cost, high compliance cost, high trust-churn loss, low
#   renewal, low fill rate, high platform fee, high sales cost).
# "high" scenario = optimistic revenue + low cost (mirror image).
# "base" = base case for every assumption, regardless of direction.
#
# For each assumption, direction is either:
#   "revenue-like": low scenario -> use assumption's "low" column
#   "cost-like":    low scenario -> use assumption's "high" column (i.e.
#                   pessimistic = expensive)
# ---------------------------------------------------------------------------

REVENUE_LIKE = {
    "A05",  # sponsor ARPU
    "A06",  # eCPM
    "A06b",  # ad sessions/patient/yr (more exposure = more revenue potential)
    "A06c",  # ads per session
    "A06d",  # fill rate
    "A07",  # renewal rate
    "A15",  # employer PEPM
    "A16",  # foundation grant pool
    "A19",  # qualified action rate
    "A20",  # revenue per action
    "A21",  # employer utilization adjustment
    "A22",  # baseline conversion rate (higher = better funnel, less trust cost)
    "A13",  # eligible patient population (more patients = larger scale = more optimistic for total revenue/valuation reach)
}

COST_LIKE = {
    "A01", "A02", "A02b",  # pathway costs per unit
    "A03", "A03b", "A04",  # utilization/volume (more visits = more total cost)
    "A06e",  # platform fee (higher = worse)
    "A08",  # sales+servicing cost
    "A09",  # compliance cost
    "A10", "A11",  # trust loss (higher pp decline = worse)
    "A17",  # foundation cohort size: ARPU_E = grant / cohort, so a LARGER cohort dilutes ARPU (worse for ARPU) -> cost-like (pessimistic/low ARPU scenario uses the "high" cohort-size column)
    "A18",  # grant duration (neutral/not used directionally, but classified for completeness)
    "A25",  # core-book revenue exposure per patient: higher exposure = higher contagion cost -> cost-like (worse)
    "A26",  # core-book trust-spillover rate: higher rate = higher contagion cost -> cost-like (worse)
}

# Policy-lever assumptions that are held at "base" regardless of the
# low/base/high revenue-cost scenario direction, because they are tested
# as an independent sensitivity axis per decision_framework.md (target
# contribution margin m: base 25%, tested at 20%/30% in sensitivity.py;
# revenue multiple: tested at 5/10/15/20x in the valuation backsolve,
# not varied by scenario direction). A27 (reference single-grantor grant
# size) mirrors A24's role for Model B's backsolve and is held at base
# for the same reason (normalization constant, not a pessimism/optimism
# axis) — added post model v2 review Attack 7.2.
POLICY_LEVER = {"A14", "A12", "A23", "A24", "A27"}


def scenario_column(aid: str, scenario: str) -> str:
    """
    Map a requested coherent scenario ("low"/"base"/"high") to the actual
    assumptions.csv column to read for a given assumption id, based on
    whether that assumption is revenue-like or cost-like.
    """
    if scenario == "base" or aid in POLICY_LEVER:
        return "base"
    is_revenue_like = aid in REVENUE_LIKE
    is_cost_like = aid in COST_LIKE
    if not is_revenue_like and not is_cost_like:
        raise ValueError(f"Assumption {aid} not classified as revenue-like or cost-like")
    if scenario == "low":
        return "low" if is_revenue_like else "high"
    elif scenario == "high":
        return "high" if is_revenue_like else "low"
    else:
        raise ValueError(f"Unknown scenario {scenario!r}")


def sval(rows: Dict[str, Dict[str, str]], aid: str, scenario: str) -> float:
    """Coherent-scenario-aware numeric fetch."""
    col = scenario_column(aid, scenario)
    return val(rows, aid, col)


def spct01(rows: Dict[str, Dict[str, str]], aid: str, scenario: str) -> float:
    """Coherent-scenario-aware 0-100 -> 0-1 fetch."""
    return sval(rows, aid, scenario) / 100.0


PATHWAY_COST_ASSUMPTION = {
    "traditional": ("A01", "A03"),
    "ai_supported": ("A02", "A03b"),
    "ai_driven": ("A02b", "A04"),  # A04 is interactions/mo -> convert to /yr
}


def pathway_units_per_yr(aid_units: str, pathway: str, rows, scenario: str) -> float:
    """
    All three pathway unit-frequency assumptions (A03, A03b, A04) are
    stored in assumptions.csv already as an annual rate (visits or
    episodes per patient per year), so no unit conversion is needed here.
    """
    return sval(rows, aid_units, scenario)


def build_fully_loaded_cost(rows, scenario: str, pathway: str, sponsor_revenue_usd_per_patient_per_yr: float,
                             exposed_patients: float, num_contracts: float) -> Dict[str, float]:
    cost_aid, units_aid = PATHWAY_COST_ASSUMPTION[pathway]
    cost_per_unit = sval(rows, cost_aid, scenario)
    units_per_yr = pathway_units_per_yr(units_aid, pathway, rows, scenario)

    pw_inputs = m.PathwayCostInputs(
        pathway=pathway,
        cost_per_unit_usd=cost_per_unit,
        units_per_patient_per_yr=units_per_yr,
    )
    care_cost = m.care_delivery_cost_per_patient_per_yr(pw_inputs)

    # Sponsor servicing cost: modeled as a fraction of sales+servicing cost
    # allocated per patient (simple allocation: same per-contract cost pool,
    # split across exposed patients). We treat sponsor servicing as already
    # captured inside A08 (sales + servicing cost per sponsor contract) per
    # the assumptions ledger's own label ("Sales + servicing cost per
    # sponsor contract"), so commercial_cost and sponsor_servicing_cost
    # both derive from A08 but are kept as separate line items for
    # auditability: we split A08 50/50 between "commercial" (sales) and
    # "sponsor servicing" by convention, documented here explicitly.
    sales_servicing_cost_per_contract = sval(rows, "A08", scenario)
    total_sales_servicing_cost = sales_servicing_cost_per_contract * num_contracts
    commercial_cost_per_patient = 0.5 * total_sales_servicing_cost / exposed_patients
    sponsor_servicing_cost_per_patient = 0.5 * total_sales_servicing_cost / exposed_patients

    compliance_cost_total = sval(rows, "A09", scenario)
    compliance_cost_per_patient = compliance_cost_total / exposed_patients

    trust_conv_loss_pp = sval(rows, "A10", scenario)
    trust_ret_loss_pp = sval(rows, "A11", scenario)
    baseline_conv_rate_pct = sval(rows, "A22", scenario)
    trust_cost_per_patient = m.trust_churn_cost_per_patient_per_yr(
        baseline_arpu_usd_per_patient_per_yr=sponsor_revenue_usd_per_patient_per_yr,
        trust_conversion_loss_pp=trust_conv_loss_pp,
        trust_retention_loss_pp=trust_ret_loss_pp,
        baseline_conversion_rate_pct=baseline_conv_rate_pct,
    )

    # Core-book contagion cost: a SECOND, separate trust-cost term (A25 x
    # A26), structurally new post model v2 review Attack #5 / 2.5 —
    # see model.py core_book_contagion_cost_per_patient_per_yr() docstring.
    # Always included (not gated off in the base case); base-case value is
    # deliberately small (see assumptions.csv A25/A26 notes).
    core_book_revenue_per_patient = sval(rows, "A25", scenario)
    core_book_spillover_rate_pct = sval(rows, "A26", scenario)
    core_book_contagion_cost_per_patient = m.core_book_contagion_cost_per_patient_per_yr(
        core_book_revenue_usd_per_patient_per_yr=core_book_revenue_per_patient,
        core_book_trust_spillover_rate_pct=core_book_spillover_rate_pct,
    )

    fl_inputs = m.FullyLoadedCostInputs(
        care_delivery_cost_per_patient_per_yr_usd=care_cost,
        sponsor_servicing_cost_per_patient_per_yr_usd=sponsor_servicing_cost_per_patient,
        commercial_cost_per_patient_per_yr_usd=commercial_cost_per_patient,
        compliance_cost_per_patient_per_yr_usd=compliance_cost_per_patient,
        trust_churn_cost_per_patient_per_yr_usd=trust_cost_per_patient,
        core_book_contagion_cost_per_patient_per_yr_usd=core_book_contagion_cost_per_patient,
    )
    fully_loaded = m.fully_loaded_incremental_cost_per_patient_per_yr(fl_inputs)

    return {
        "care_delivery_cost_per_patient_per_yr_usd": care_cost,
        "sponsor_servicing_cost_per_patient_per_yr_usd": sponsor_servicing_cost_per_patient,
        "commercial_cost_per_patient_per_yr_usd": commercial_cost_per_patient,
        "compliance_cost_per_patient_per_yr_usd": compliance_cost_per_patient,
        "trust_churn_cost_per_patient_per_yr_usd": trust_cost_per_patient,
        "core_book_contagion_cost_per_patient_per_yr_usd": core_book_contagion_cost_per_patient,
        "fully_loaded_cost_per_patient_per_yr_usd": fully_loaded,
    }


# Reference scale assumptions used purely to translate ARPU-style models
# into concrete revenue figures for the grid (exposed_patients, num_contracts,
# annual_contract_value). These are NOT hidden constants: num_contracts and
# annual_contract_value are A23 and A24 in assumptions.csv (policy-lever,
# held at base case per scenario_column()'s POLICY_LEVER handling — see
# A23/A24 notes for rationale). Kept as module-level fallback values only
# for direct unit-test convenience; scenario/sensitivity runs always read
# A23/A24 from the CSV via reference_num_contracts()/reference_contract_value().
DEFAULT_NUM_CONTRACTS = 3.0
DEFAULT_ANNUAL_CONTRACT_VALUE_USD = 250_000.0


def reference_num_contracts(rows: Dict[str, Dict[str, str]], scenario: str) -> float:
    """A23: reference sponsor contract count (policy-lever, always base case)."""
    return sval(rows, "A23", scenario)


def reference_contract_value_usd(rows: Dict[str, Dict[str, str]], scenario: str) -> float:
    """A24: reference annual sponsor contract value (policy-lever, always base case)."""
    return sval(rows, "A24", scenario)


def reference_grant_size_usd(rows: Dict[str, Dict[str, str]], scenario: str) -> float:
    """
    A27: reference single-grantor/foundation annual grant size
    (policy-lever, always base case) — mirrors reference_contract_value_usd()
    (A24) but for Model E's scale backsolve, added post
    model v2 review Attack 7.2.
    """
    return sval(rows, "A27", scenario)


def compute_model_revenues(rows, scenario: str, exposed_patients: float) -> Dict[str, float]:
    """Compute per-patient ARPU for all five models under a given scenario."""
    # Model A
    sessions_per_patient_per_yr = sval(rows, "A06b", scenario)
    ads_per_session = sval(rows, "A06c", scenario)
    fill_rate = spct01(rows, "A06d", scenario)
    ecpm = sval(rows, "A06", scenario)
    platform_fee = spct01(rows, "A06e", scenario)
    rev_a = m.model_a_programmatic_ad_revenue_per_patient_per_yr(
        sessions_per_patient_per_yr=sessions_per_patient_per_yr,
        ads_per_session=ads_per_session,
        fill_rate_pct=fill_rate,
        ecpm_usd_per_1000_impressions=ecpm,
        platform_fee_pct=platform_fee,
    )

    # Model B
    arpu_b_gross_anchor = sval(rows, "A05", scenario)  # external anchor ARPU, used as annual_contract_value/exposed_patients proxy check
    num_contracts = reference_num_contracts(rows, scenario)
    annual_contract_value = reference_contract_value_usd(rows, scenario)
    sales_servicing_cost_total = sval(rows, "A08", scenario) * num_contracts
    rev_b = m.model_b_fixed_fee_sponsorship_arpu(
        num_sponsors=num_contracts,
        annual_contract_value_usd=annual_contract_value,
        exposed_patients=exposed_patients,
        sales_servicing_cost_usd_per_yr=sales_servicing_cost_total,
    )
    # Blend with the literature-anchored ARPU (A05) as an external sanity
    # check/floor: report both, but the grid's "actual ARPU" for Model B
    # uses the A05 external-benchmark anchor directly since it is the
    # sourced, patient-population-independent figure requested by
    # comparable_notes.md's recommended next action. Discount by sponsor
    # renewal rate (A07) to reflect expected steady-state ARPU: a sponsor
    # contract that is not renewed mid-cycle contributes less expected
    # annualized revenue once averaged across a multi-year sponsor cohort
    # (simple expected-value treatment: renewal_rate is the probability a
    # given sponsor-year of revenue actually recurs/is realized).
    renewal_rate = spct01(rows, "A07", scenario)
    rev_b_anchor = arpu_b_gross_anchor * renewal_rate

    # Model C (flag: legal review required)
    actions_per_patient_per_yr = spct01(rows, "A19", scenario) * 12  # A19 modeled as % of sessions/mo triggering action; approximate to monthly cadence x 12
    rev_per_action = sval(rows, "A20", scenario)
    rev_c = m.model_c_performance_partnership_revenue_per_patient_per_yr(
        qualified_actions_per_patient_per_yr=actions_per_patient_per_yr,
        revenue_per_action_usd=rev_per_action,
    )

    # Model D
    pmpm = sval(rows, "A15", scenario) / 12.0  # A15 stored as USD/patient/yr; convert to PMPM
    util_adj = spct01(rows, "A21", scenario)
    rev_d = m.model_d_employer_underwriting_arpu(pmpm_usd=pmpm, utilization_adjustment_pct=util_adj)

    # Model E
    grant = sval(rows, "A16", scenario)
    cohort = sval(rows, "A17", scenario)
    duration = sval(rows, "A18", scenario)
    rev_e = m.model_e_foundation_underwriting_arpu(
        grant_usd_per_yr=grant, cohort_size_patients=cohort, duration_yrs=duration
    )

    return {
        "A_programmatic_ads": rev_a,
        "B_fixed_fee_sponsorship": rev_b,
        "B_fixed_fee_sponsorship_external_anchor": rev_b_anchor,
        "C_performance_partnership": rev_c,
        "D_employer_payer_underwriting": rev_d,
        "E_foundation_underwriting": rev_e,
    }, num_contracts, annual_contract_value


MODEL_KEYS = [
    "A_programmatic_ads",
    "B_fixed_fee_sponsorship_external_anchor",
    "C_performance_partnership",
    "D_employer_payer_underwriting",
    "E_foundation_underwriting",
]


def run_scenarios():
    rows = load_assumptions()
    output_rows = []

    for scenario in SCENARIOS:
        exposed_patients = sval(rows, "A13", scenario)
        model_revenues, num_contracts, annual_contract_value = compute_model_revenues(
            rows, scenario, exposed_patients
        )
        target_margin = spct01(rows, "A14", scenario)

        for pathway in m.PATHWAYS:
            for model_key in MODEL_KEYS:
                actual_arpu = model_revenues[model_key]
                cost_breakdown = build_fully_loaded_cost(
                    rows, scenario, pathway,
                    sponsor_revenue_usd_per_patient_per_yr=actual_arpu,
                    exposed_patients=exposed_patients,
                    num_contracts=num_contracts,
                )
                fully_loaded_cost = cost_breakdown["fully_loaded_cost_per_patient_per_yr_usd"]
                required_arpu = m.required_sponsor_revenue_per_patient_per_yr(
                    fully_loaded_cost_usd_per_patient_per_yr=fully_loaded_cost,
                    target_contribution_margin_pct=target_margin,
                )
                gap = actual_arpu - required_arpu

                north_star = m.risk_adjusted_contribution_margin_per_patient_per_yr(
                    sponsor_revenue_usd_per_patient_per_yr=actual_arpu,
                    care_delivery_cost_usd_per_patient_per_yr=cost_breakdown["care_delivery_cost_per_patient_per_yr_usd"],
                    sponsor_servicing_cost_usd_per_patient_per_yr=cost_breakdown["sponsor_servicing_cost_per_patient_per_yr_usd"],
                    commercial_cost_usd_per_patient_per_yr=cost_breakdown["commercial_cost_per_patient_per_yr_usd"],
                    compliance_cost_usd_per_patient_per_yr=cost_breakdown["compliance_cost_per_patient_per_yr_usd"],
                    trust_churn_cost_usd_per_patient_per_yr=cost_breakdown["trust_churn_cost_per_patient_per_yr_usd"],
                    core_book_contagion_cost_usd_per_patient_per_yr=cost_breakdown["core_book_contagion_cost_per_patient_per_yr_usd"],
                )

                row = {
                    "scenario": scenario,
                    "pathway": pathway,
                    "model": model_key,
                    "target_contribution_margin_pct": round(target_margin * 100, 2),
                    "care_delivery_cost_usd_per_patient_per_yr": round(cost_breakdown["care_delivery_cost_per_patient_per_yr_usd"], 2),
                    "sponsor_servicing_cost_usd_per_patient_per_yr": round(cost_breakdown["sponsor_servicing_cost_per_patient_per_yr_usd"], 2),
                    "commercial_cost_usd_per_patient_per_yr": round(cost_breakdown["commercial_cost_per_patient_per_yr_usd"], 2),
                    "compliance_cost_usd_per_patient_per_yr": round(cost_breakdown["compliance_cost_per_patient_per_yr_usd"], 2),
                    "trust_churn_cost_usd_per_patient_per_yr": round(cost_breakdown["trust_churn_cost_per_patient_per_yr_usd"], 2),
                    "core_book_contagion_cost_usd_per_patient_per_yr": round(cost_breakdown["core_book_contagion_cost_per_patient_per_yr_usd"], 2),
                    "fully_loaded_cost_usd_per_patient_per_yr": round(fully_loaded_cost, 2),
                    "required_arpu_usd_per_patient_per_yr": round(required_arpu, 2),
                    "actual_arpu_usd_per_patient_per_yr": round(actual_arpu, 2),
                    "gap_usd_per_patient_per_yr": round(gap, 2),
                    "north_star_risk_adj_contribution_margin_usd_per_patient_per_yr": round(north_star, 2),
                }

                # Valuation backsolve at 5/10/15/20x, using this model's actual ARPU
                reference_grant_size = reference_grant_size_usd(rows, scenario)
                for mult in (5, 10, 15, 20):
                    req_rev = m.required_revenue_for_valuation(1_000_000_000.0, mult)
                    if actual_arpu > 0:
                        req_patients = m.required_active_patients(req_rev, actual_arpu)
                        row[f"required_patients_at_{mult}x_for_1B"] = round(req_patients, 0)
                    else:
                        row[f"required_patients_at_{mult}x_for_1B"] = None
                    if model_key == "B_fixed_fee_sponsorship_external_anchor":
                        sponsor_info = m.required_sponsor_count_and_concentration(req_rev, annual_contract_value)
                        row[f"required_sponsors_at_{mult}x_for_1B"] = round(sponsor_info["required_sponsors"], 1)
                        row[f"sponsor_concentration_pct_at_{mult}x_for_1B"] = round(
                            sponsor_info["concentration_pct_per_sponsor"] * 100, 3
                        )
                    else:
                        row[f"required_sponsors_at_{mult}x_for_1B"] = None
                        row[f"sponsor_concentration_pct_at_{mult}x_for_1B"] = None

                    # Model E scale backsolve (added post model v2 review
                    # Attack 7.2), mirroring the Model B sponsor-count
                    # treatment above: required annual grant pool == required
                    # revenue at this multiple (Model E's ARPU is entirely
                    # grant-funded, so the dollar figures are identical);
                    # required grantors = that pool / A27 (reference
                    # single-grantor grant size, held at base case).
                    if model_key == "E_foundation_underwriting":
                        row[f"required_annual_grant_pool_at_{mult}x_for_1B"] = round(req_rev, 0)
                        grantor_info = m.required_grantor_count_and_concentration(req_rev, reference_grant_size)
                        row[f"required_grantors_at_{mult}x_for_1B"] = round(grantor_info["required_grantors"], 1)
                        row[f"grantor_concentration_pct_at_{mult}x_for_1B"] = round(
                            grantor_info["concentration_pct_per_grantor"] * 100, 3
                        )
                    else:
                        row[f"required_annual_grant_pool_at_{mult}x_for_1B"] = None
                        row[f"required_grantors_at_{mult}x_for_1B"] = None
                        row[f"grantor_concentration_pct_at_{mult}x_for_1B"] = None

                output_rows.append(row)

    fieldnames = list(output_rows[0].keys())
    with open(OUTPUTS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {len(output_rows)} rows to {OUTPUTS_CSV}")
    return output_rows


def run_funnel_lens():
    """
    "Free care as an acquisition channel" funnel lens (Legion data —
    see data/ceo_data_integration.md #8/#9). Small, standalone comparison:
    free AI-driven episode cost (A02b, low/base/high) vs. paid CAC (A28,
    single point estimate), and the break-even conversion rate at which
    the two are equal (m.free_care_acquisition_breakeven_conversion_rate()).

    Deliberately NOT wired into outputs.csv's pathway x model grid — A28
    does not feed the Gate-1 economics grid; this is a genuinely separate,
    small, second lens on the same A02b cost figure. Writes
    model/funnel_lens.csv.
    """
    rows = load_assumptions()
    cac_usd = val(rows, "A28", "base")  # A28 is a point estimate (low=base=high=250)

    out_rows = []
    for scenario in SCENARIOS:
        episode_cost = val(rows, "A02b", scenario)
        breakeven_rate = m.free_care_acquisition_breakeven_conversion_rate(
            free_episode_cost_usd=episode_cost, cac_usd=cac_usd
        )
        out_rows.append({
            "scenario": scenario,
            "free_episode_cost_usd_A02b": episode_cost,
            "cac_usd_A28": cac_usd,
            "breakeven_conversion_rate_pct": round(breakeven_rate * 100, 4),
        })

    fieldnames = list(out_rows[0].keys())
    with open(FUNNEL_LENS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows to {FUNNEL_LENS_CSV}")
    return out_rows


if __name__ == "__main__":
    run_scenarios()
    run_funnel_lens()
