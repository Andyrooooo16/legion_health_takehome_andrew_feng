"""
Legion Health Sponsorship Case — One-Way Sensitivity + Break-Even Solver
==========================================================================

Runs one-way (tornado-style) sensitivity on the north-star metric
(risk-adjusted contribution margin per patient per year) by flexing one
assumption at a time between its low and high value while holding all
others at base case. Also solves for break-even sponsor ARPU per pathway
(the ARPU at which north-star margin = 0, i.e., fully loaded cost is
exactly covered with zero contribution margin) and break-even ARPU at
the target contribution margin (m = 25% base).

Writes model/sensitivity_outputs.csv.

Run: python3 sensitivity.py
"""

import csv
import os
from typing import Dict, List

import model as m
import scenarios as sc

HERE = os.path.dirname(os.path.abspath(__file__))
SENSITIVITY_CSV = os.path.join(HERE, "sensitivity_outputs.csv")

# Assumptions to include in the one-way tornado, per the task spec:
# sponsor ARPU, care cost, patient volume, engagement, renewal, sales cost,
# compliance cost, trust churn.
TORNADO_ASSUMPTIONS = [
    ("A05", "Sponsor ARPU (Model B anchor)"),
    ("A15", "Sponsor ARPU - employer PEPM rate (Model D anchor)"),
    ("A01", "Care cost - traditional visit"),
    ("A02", "Care cost - AI-supported visit"),
    ("A02b", "Care cost - AI-driven episode"),
    ("A13", "Eligible patient volume"),
    ("A06b", "Engagement - ad sessions/patient/yr"),
    ("A21", "Engagement - employer utilization adjustment"),
    ("A07", "Sponsor renewal rate"),
    ("A08", "Sales/servicing cost per contract"),
    ("A09", "Compliance/legal cost"),
    ("A10", "Trust churn - booking conversion loss"),
    ("A11", "Trust churn - retention loss"),
    ("A25", "Core-book revenue exposure per patient (contagion term, v2)"),
    ("A26", "Core-book trust-spillover rate (contagion term, v2)"),
]


def run_base_case_for_pathway_model(rows, pathway: str, model_key: str, scenario_override: Dict[str, str] = None):
    """
    Compute north-star margin and actual/required ARPU for one pathway x
    model combination, at base case for all assumptions except any
    explicitly overridden in scenario_override ({assumption_id: "low"|"base"|"high"}).
    """
    scenario_override = scenario_override or {}

    def get(aid, default_scenario="base"):
        s = scenario_override.get(aid, default_scenario)
        return sc.val(rows, aid, s)

    def get_pct01(aid, default_scenario="base"):
        return get(aid, default_scenario) / 100.0

    exposed_patients = get("A13")

    # --- Model revenues (base-case logic mirrored from scenarios.py, with overrides) ---
    sessions_per_patient_per_yr = get("A06b")
    ads_per_session = get("A06c")
    fill_rate = get_pct01("A06d")
    ecpm = get("A06")
    platform_fee = get_pct01("A06e")
    rev_a = m.model_a_programmatic_ad_revenue_per_patient_per_yr(
        sessions_per_patient_per_yr=sessions_per_patient_per_yr,
        ads_per_session=ads_per_session,
        fill_rate_pct=fill_rate,
        ecpm_usd_per_1000_impressions=ecpm,
        platform_fee_pct=platform_fee,
    )

    renewal_rate = get_pct01("A07")
    arpu_b_anchor = get("A05") * renewal_rate  # discount external-anchor ARPU by sponsor renewal probability, mirroring scenarios.py
    num_contracts = get("A23")
    annual_contract_value = get("A24")

    actions_per_patient_per_yr = get_pct01("A19") * 12
    rev_per_action = get("A20")
    rev_c = m.model_c_performance_partnership_revenue_per_patient_per_yr(
        qualified_actions_per_patient_per_yr=actions_per_patient_per_yr,
        revenue_per_action_usd=rev_per_action,
    )

    pmpm = get("A15") / 12.0
    util_adj = get_pct01("A21")
    rev_d = m.model_d_employer_underwriting_arpu(pmpm_usd=pmpm, utilization_adjustment_pct=util_adj)

    grant = get("A16")
    cohort = get("A17")
    duration = get("A18")
    rev_e = m.model_e_foundation_underwriting_arpu(grant_usd_per_yr=grant, cohort_size_patients=cohort, duration_yrs=duration)

    model_revenues = {
        "A_programmatic_ads": rev_a,
        "B_fixed_fee_sponsorship_external_anchor": arpu_b_anchor,
        "C_performance_partnership": rev_c,
        "D_employer_payer_underwriting": rev_d,
        "E_foundation_underwriting": rev_e,
    }
    actual_arpu = model_revenues[model_key]

    # --- Fully loaded cost ---
    cost_aid, units_aid = sc.PATHWAY_COST_ASSUMPTION[pathway]
    cost_per_unit = get(cost_aid)
    units_per_yr = get(units_aid)
    pw_inputs = m.PathwayCostInputs(pathway=pathway, cost_per_unit_usd=cost_per_unit, units_per_patient_per_yr=units_per_yr)
    care_cost = m.care_delivery_cost_per_patient_per_yr(pw_inputs)

    sales_servicing_cost_per_contract = get("A08")
    total_sales_servicing_cost = sales_servicing_cost_per_contract * num_contracts
    commercial_cost_per_patient = 0.5 * total_sales_servicing_cost / exposed_patients
    sponsor_servicing_cost_per_patient = 0.5 * total_sales_servicing_cost / exposed_patients

    compliance_cost_total = get("A09")
    compliance_cost_per_patient = compliance_cost_total / exposed_patients

    trust_conv_loss_pp = get("A10")
    trust_ret_loss_pp = get("A11")
    baseline_conv_rate_pct = get("A22")
    trust_cost_per_patient = m.trust_churn_cost_per_patient_per_yr(
        baseline_arpu_usd_per_patient_per_yr=actual_arpu,
        trust_conversion_loss_pp=trust_conv_loss_pp,
        trust_retention_loss_pp=trust_ret_loss_pp,
        baseline_conversion_rate_pct=baseline_conv_rate_pct,
    )

    # Core-book contagion cost (A25 x A26) — structurally new term, see
    # model.py core_book_contagion_cost_per_patient_per_yr() and
    # assumptions.csv A25/A26 (added post model v2 review Attack
    # #5 / 2.5). Always included, not gated off.
    core_book_revenue_per_patient = get("A25")
    core_book_spillover_rate_pct = get("A26")
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
    fully_loaded_cost = m.fully_loaded_incremental_cost_per_patient_per_yr(fl_inputs)

    target_margin = get_pct01("A14")
    required_arpu = m.required_sponsor_revenue_per_patient_per_yr(fully_loaded_cost, target_margin)

    north_star = m.risk_adjusted_contribution_margin_per_patient_per_yr(
        sponsor_revenue_usd_per_patient_per_yr=actual_arpu,
        care_delivery_cost_usd_per_patient_per_yr=care_cost,
        sponsor_servicing_cost_usd_per_patient_per_yr=sponsor_servicing_cost_per_patient,
        commercial_cost_usd_per_patient_per_yr=commercial_cost_per_patient,
        compliance_cost_usd_per_patient_per_yr=compliance_cost_per_patient,
        trust_churn_cost_usd_per_patient_per_yr=trust_cost_per_patient,
        core_book_contagion_cost_usd_per_patient_per_yr=core_book_contagion_cost_per_patient,
    )

    return {
        "actual_arpu": actual_arpu,
        "fully_loaded_cost": fully_loaded_cost,
        "required_arpu": required_arpu,
        "north_star": north_star,
    }


def one_way_tornado(rows, pathway: str, model_key: str) -> List[Dict]:
    """
    For each assumption in TORNADO_ASSUMPTIONS, flex it to low and to high
    (holding everything else at base) and record the resulting north-star
    metric, to identify dominant assumptions (largest swing = most
    dominant) and directionality.
    """
    base_result = run_base_case_for_pathway_model(rows, pathway, model_key)
    base_north_star = base_result["north_star"]

    results = []
    for aid, label in TORNADO_ASSUMPTIONS:
        low_result = run_base_case_for_pathway_model(rows, pathway, model_key, scenario_override={aid: "low"})
        high_result = run_base_case_for_pathway_model(rows, pathway, model_key, scenario_override={aid: "high"})
        swing = abs(high_result["north_star"] - low_result["north_star"])
        results.append({
            "pathway": pathway,
            "model": model_key,
            "assumption_id": aid,
            "assumption_label": label,
            "base_north_star_usd_per_patient_per_yr": round(base_north_star, 2),
            "north_star_at_assumption_low_usd_per_patient_per_yr": round(low_result["north_star"], 2),
            "north_star_at_assumption_high_usd_per_patient_per_yr": round(high_result["north_star"], 2),
            "swing_usd_per_patient_per_yr": round(swing, 2),
        })
    results.sort(key=lambda r: r["swing_usd_per_patient_per_yr"], reverse=True)
    for rank, r in enumerate(results, start=1):
        r["tornado_rank"] = rank
    return results


def break_even_sponsor_arpu(rows, pathway: str, target_margin_pct: float) -> Dict[str, float]:
    """
    Solve for break-even sponsor ARPU per pathway at base-case cost
    assumptions, for a given target contribution margin (0 = pure
    break-even/no-margin-buffer; 0.25 = base target margin per
    decision_framework.md Gate 1).

    Formula: break_even_arpu = fully_loaded_cost / (1 - target_margin_pct)
    (identical to required_sponsor_revenue_per_patient_per_yr(), exposed
    here as an explicit named solver per the task's sensitivity spec.)
    """
    cost_aid, units_aid = sc.PATHWAY_COST_ASSUMPTION[pathway]
    cost_per_unit = sc.val(rows, cost_aid, "base")
    units_per_yr = sc.val(rows, units_aid, "base")
    pw_inputs = m.PathwayCostInputs(pathway=pathway, cost_per_unit_usd=cost_per_unit, units_per_patient_per_yr=units_per_yr)
    care_cost = m.care_delivery_cost_per_patient_per_yr(pw_inputs)

    exposed_patients = sc.val(rows, "A13", "base")
    num_contracts = sc.val(rows, "A23", "base")
    sales_servicing_cost_total = sc.val(rows, "A08", "base") * num_contracts
    commercial_cost_per_patient = 0.5 * sales_servicing_cost_total / exposed_patients
    sponsor_servicing_cost_per_patient = 0.5 * sales_servicing_cost_total / exposed_patients
    compliance_cost_per_patient = sc.val(rows, "A09", "base") / exposed_patients

    # Trust churn cost depends on ARPU itself (baseline_arpu term); for the
    # break-even solve we approximate using the Model B external-anchor
    # ARPU (A05 base) as the revenue-at-risk base, documented explicitly
    # since a fully closed-form solve would require iterating (trust cost
    # is a small fraction of ARPU so this approximation is stable).
    arpu_proxy_for_trust_calc = sc.val(rows, "A05", "base")
    trust_cost_per_patient = m.trust_churn_cost_per_patient_per_yr(
        baseline_arpu_usd_per_patient_per_yr=arpu_proxy_for_trust_calc,
        trust_conversion_loss_pp=sc.val(rows, "A10", "base"),
        trust_retention_loss_pp=sc.val(rows, "A11", "base"),
        baseline_conversion_rate_pct=sc.val(rows, "A22", "base"),
    )

    # Core-book contagion cost (A25 x A26, base case) — see model.py
    # core_book_contagion_cost_per_patient_per_yr() and assumptions.csv
    # A25/A26 (added post model v2 review Attack #5 / 2.5).
    core_book_contagion_cost_per_patient = m.core_book_contagion_cost_per_patient_per_yr(
        core_book_revenue_usd_per_patient_per_yr=sc.val(rows, "A25", "base"),
        core_book_trust_spillover_rate_pct=sc.val(rows, "A26", "base"),
    )

    fl_inputs = m.FullyLoadedCostInputs(
        care_delivery_cost_per_patient_per_yr_usd=care_cost,
        sponsor_servicing_cost_per_patient_per_yr_usd=sponsor_servicing_cost_per_patient,
        commercial_cost_per_patient_per_yr_usd=commercial_cost_per_patient,
        compliance_cost_per_patient_per_yr_usd=compliance_cost_per_patient,
        trust_churn_cost_per_patient_per_yr_usd=trust_cost_per_patient,
        core_book_contagion_cost_per_patient_per_yr_usd=core_book_contagion_cost_per_patient,
    )
    fully_loaded_cost = m.fully_loaded_incremental_cost_per_patient_per_yr(fl_inputs)
    break_even_arpu_zero_margin = m.required_sponsor_revenue_per_patient_per_yr(fully_loaded_cost, 0.0)
    break_even_arpu_target_margin = m.required_sponsor_revenue_per_patient_per_yr(fully_loaded_cost, target_margin_pct)

    return {
        "pathway": pathway,
        "fully_loaded_cost_usd_per_patient_per_yr": round(fully_loaded_cost, 2),
        "break_even_arpu_zero_margin_usd_per_patient_per_yr": round(break_even_arpu_zero_margin, 2),
        f"break_even_arpu_at_{int(target_margin_pct*100)}pct_margin_usd_per_patient_per_yr": round(break_even_arpu_target_margin, 2),
        "external_anchor_arpu_low_usd_per_patient_per_yr": sc.val(rows, "A05", "low"),
        "external_anchor_arpu_base_usd_per_patient_per_yr": sc.val(rows, "A05", "base"),
        "external_anchor_arpu_high_usd_per_patient_per_yr": sc.val(rows, "A05", "high"),
        "gap_to_external_anchor_base_usd_per_patient_per_yr": round(sc.val(rows, "A05", "base") - break_even_arpu_target_margin, 2),
    }


def contribution_margin_scenarios(rows) -> List[Dict]:
    """Test target contribution margin at 20% / 25% / 30% per pathway (Gate 1 requirement)."""
    results = []
    for pathway in m.PATHWAYS:
        for margin_pct in (0.20, 0.25, 0.30):
            be = break_even_sponsor_arpu(rows, pathway, margin_pct)
            results.append({
                "pathway": pathway,
                "target_contribution_margin_pct": margin_pct * 100,
                "fully_loaded_cost_usd_per_patient_per_yr": be["fully_loaded_cost_usd_per_patient_per_yr"],
                "break_even_arpu_at_target_margin_usd_per_patient_per_yr": be[f"break_even_arpu_at_{int(margin_pct*100)}pct_margin_usd_per_patient_per_yr"],
            })
    return results


def run_sensitivity():
    rows = sc.load_assumptions()

    all_tornado_rows = []
    for pathway in m.PATHWAYS:
        for model_key in sc.MODEL_KEYS:
            all_tornado_rows.extend(one_way_tornado(rows, pathway, model_key))

    break_even_rows = []
    for pathway in m.PATHWAYS:
        be = break_even_sponsor_arpu(rows, pathway, 0.25)
        break_even_rows.append(be)

    margin_test_rows = contribution_margin_scenarios(rows)

    # Write three sections into one CSV file, each clearly labeled, since
    # the task allows "append/write results to a separate
    # sensitivity_outputs.csv".
    with open(SENSITIVITY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["SECTION 1: ONE-WAY TORNADO SENSITIVITY (north-star metric, USD/patient/yr)"])
        fieldnames = list(all_tornado_rows[0].keys())
        writer.writerow(fieldnames)
        for r in all_tornado_rows:
            writer.writerow([r[k] for k in fieldnames])

        writer.writerow([])
        writer.writerow(["SECTION 2: BREAK-EVEN SPONSOR ARPU PER PATHWAY (base-case cost, m=25%)"])
        fieldnames2 = list(break_even_rows[0].keys())
        writer.writerow(fieldnames2)
        for r in break_even_rows:
            writer.writerow([r[k] for k in fieldnames2])

        writer.writerow([])
        writer.writerow(["SECTION 3: CONTRIBUTION MARGIN SENSITIVITY (m = 20% / 25% / 30%)"])
        fieldnames3 = list(margin_test_rows[0].keys())
        writer.writerow(fieldnames3)
        for r in margin_test_rows:
            writer.writerow([r[k] for k in fieldnames3])

    print(f"Wrote sensitivity results to {SENSITIVITY_CSV}")
    print(f"  Tornado rows: {len(all_tornado_rows)}")
    print(f"  Break-even rows: {len(break_even_rows)}")
    print(f"  Margin test rows: {len(margin_test_rows)}")

    # Print top dominant assumptions overall (aggregated by max swing across
    # pathway/model combos) for quick console visibility.
    from collections import defaultdict
    max_swing_by_aid = defaultdict(float)
    label_by_aid = {}
    for r in all_tornado_rows:
        aid = r["assumption_id"]
        max_swing_by_aid[aid] = max(max_swing_by_aid[aid], r["swing_usd_per_patient_per_yr"])
        label_by_aid[aid] = r["assumption_label"]
    ranked = sorted(max_swing_by_aid.items(), key=lambda kv: kv[1], reverse=True)
    print("\nDominant assumptions (max swing across all pathway/model combos):")
    for aid, swing in ranked:
        print(f"  {aid} ({label_by_aid[aid]}): max swing ${swing:,.2f}/patient/yr")

    return all_tornado_rows, break_even_rows, margin_test_rows


if __name__ == "__main__":
    run_sensitivity()
