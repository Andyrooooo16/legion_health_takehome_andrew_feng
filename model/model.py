"""
Legion Health Sponsorship Case — Core Quantitative Model
==========================================================

Pure functions implementing the economics described in
deliverables/decision_framework.md. No hidden constants: every numeric
input is a function argument, sourced from model/assumptions.csv via
scenarios.py / sensitivity.py. This module contains NO Legion-specific
data — all defaults live in assumptions.csv and are loaded by callers.

Units discipline (see model_readme.md for the full units glossary):
  - All "per year" (annual) quantities are suffixed `_per_yr` or `_annual`.
  - All "per visit"/"per episode" quantities are suffixed `_per_visit` /
    `_per_episode`.
  - All monetary quantities are USD unless otherwise noted.
  - Percentages used as multipliers are expressed as fractions in (0, 1)
    inside functions; where assumptions.csv stores them as 0-100 or pp,
    the scenario/sensitivity loaders convert before calling into here.

Three care pathways (per decision_framework.md):
  1. "traditional"      — traditional clinician visit
  2. "ai_supported"      — AI-supported clinician care
  3. "ai_driven"         — mostly-AI-driven care episode

Glossary of margin terms:
  - Gross margin: (revenue - direct care delivery COGS) / revenue.
    NOT used as the decision metric here; kept separate from contribution
    margin, which nets out sponsor-servicing/commercial/compliance/trust
    costs. Legion's existing ~53% visit gross margin figure refers to
    this narrower COGS-only margin, not the fully loaded contribution
    margin computed below.
  - Contribution margin (m): (sponsor revenue - fully loaded incremental
    cost) / sponsor revenue. This is the target margin in the decision
    framework's Gate 1 (m = 25% base; 20%/30% tested).
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

PATHWAYS = ("traditional", "ai_supported", "ai_driven")
MODELS = ("A", "B", "C", "D", "E")


# ---------------------------------------------------------------------------
# 1. Pathway cost model
# ---------------------------------------------------------------------------

@dataclass
class PathwayCostInputs:
    """Per-pathway cost and volume inputs, all explicit (no hidden constants).

    cost_per_unit: USD per visit (traditional/ai_supported) or per episode
        (ai_driven).
    units_per_patient_per_yr: visits/patient/yr (traditional/ai_supported)
        or episodes/patient/yr (ai_driven) — all three already expressed
        as an annual rate in assumptions.csv (A03, A03b, A04).
    """
    pathway: str
    cost_per_unit_usd: float
    units_per_patient_per_yr: float

    def __post_init__(self):
        if self.pathway not in PATHWAYS:
            raise ValueError(f"Unknown pathway {self.pathway!r}; must be one of {PATHWAYS}")
        if self.cost_per_unit_usd < 0:
            raise ValueError("cost_per_unit_usd cannot be negative")
        if self.units_per_patient_per_yr < 0:
            raise ValueError("units_per_patient_per_yr cannot be negative")


def care_delivery_cost_per_patient_per_yr(inputs: PathwayCostInputs) -> float:
    """
    Care-delivery (COGS-only) cost per patient per year for one pathway.

    Formula:
        care_cost_per_patient_per_yr = cost_per_unit_usd * units_per_patient_per_yr

    This is the direct clinical/technical delivery cost only — it excludes
    sponsor servicing, commercial (sales), compliance/legal, and trust/churn
    costs, which are added in fully_loaded_incremental_cost_per_patient_per_yr().
    """
    return inputs.cost_per_unit_usd * inputs.units_per_patient_per_yr


# ---------------------------------------------------------------------------
# 2. Fully loaded incremental cost
# ---------------------------------------------------------------------------

@dataclass
class FullyLoadedCostInputs:
    """
    All non-care-delivery cost components, explicit and separable.

    care_delivery_cost_per_patient_per_yr_usd: from care_delivery_cost_per_patient_per_yr()
    sponsor_servicing_cost_per_patient_per_yr_usd: incremental ops cost to
        service a sponsor relationship, allocated per patient (e.g., sponsor
        reporting, account management amortized across exposed patients).
    commercial_cost_per_patient_per_yr_usd: sales cost per patient, i.e.
        (sales_cost_per_contract_usd * num_contracts) / exposed_patients,
        computed upstream and passed in per patient.
    compliance_cost_per_patient_per_yr_usd: incremental legal/compliance
        cost allocated per patient (annual compliance budget / patient base).
    trust_churn_cost_per_patient_per_yr_usd: modeled as % revenue loss or
        $/patient — see trust_churn_cost_per_patient_per_yr(). Scoped to
        SPONSOR-TIER ARPU only (the revenue this term nets against).
    core_book_contagion_cost_per_patient_per_yr_usd: a SECOND, separate
        trust-cost term — see core_book_contagion_cost_per_patient_per_yr().
        Added post model v2 review Attack #5 / 2.5: trust damage from
        sponsorship plausibly bleeds beyond the sponsored tier into
        Legion's existing core fee-for-service patient book, which the
        original trust_churn_cost_per_patient_per_yr_usd term (scoped only
        to sponsor-tier ARPU) cannot see by construction. This term is
        structurally new and entirely placeholder (A25/A26 in
        assumptions.csv, both status=placeholder_unresolved) — it is
        included in every run (not switched off in the base case) with a
        deliberately small base-case value so it remains visibly
        provisional rather than a considered central estimate.
    """
    care_delivery_cost_per_patient_per_yr_usd: float
    sponsor_servicing_cost_per_patient_per_yr_usd: float
    commercial_cost_per_patient_per_yr_usd: float
    compliance_cost_per_patient_per_yr_usd: float
    trust_churn_cost_per_patient_per_yr_usd: float
    core_book_contagion_cost_per_patient_per_yr_usd: float


def trust_churn_cost_per_patient_per_yr(
    baseline_arpu_usd_per_patient_per_yr: float,
    trust_conversion_loss_pp: float,
    trust_retention_loss_pp: float,
    baseline_conversion_rate_pct: float,
) -> float:
    """
    Trust-related churn cost, modeled as expected revenue loss per patient
    per year attributable to sponsorship-driven declines in booking
    conversion and retention.

    Formula (illustrative, explicit — not hidden):
        combined_loss_fraction = (trust_conversion_loss_pp + trust_retention_loss_pp) / 100
        trust_churn_cost_per_patient_per_yr = baseline_arpu_usd_per_patient_per_yr * combined_loss_fraction

    Where baseline_arpu_usd_per_patient_per_yr represents the revenue at
    stake per patient (sponsor ARPU here, since that is the revenue this
    model is trying to protect). trust_conversion_loss_pp and
    trust_retention_loss_pp are percentage-point declines (A10, A11).
    baseline_conversion_rate_pct (A22) is accepted for transparency/
    auditability (shows the base being declined from) but the cost
    calculation itself uses the pp decline directly, which is the
    conservative/explicit approach requested (keep trust cost explicit,
    not buried in a compounded funnel model).
    """
    if not (0 <= baseline_conversion_rate_pct <= 100):
        raise ValueError("baseline_conversion_rate_pct must be within [0, 100]")
    combined_loss_fraction = (trust_conversion_loss_pp + trust_retention_loss_pp) / 100.0
    return baseline_arpu_usd_per_patient_per_yr * combined_loss_fraction


def core_book_contagion_cost_per_patient_per_yr(
    core_book_revenue_usd_per_patient_per_yr: float,
    core_book_trust_spillover_rate_pct: float,
) -> float:
    """
    Core-book contagion cost — a SECOND, separate trust-cost term added
    post v2 model revision (model v2 review
    Attack #5 / 2.5: "The trust-churn cost formula only charges trust
    damage against the new sponsor revenue, never against Legion's
    existing core patient book"). trust_churn_cost_per_patient_per_yr()
    above nets trust damage only against sponsor-tier ARPU; this function
    nets a (much smaller, placeholder) spillover rate against Legion's
    EXISTING fee-for-service revenue per patient, which is a materially
    larger revenue base and therefore a materially larger absolute-dollar
    risk even at a low spillover rate.

    Both inputs are entirely unresolved, analyst placeholders pending
    real data:
      - core_book_revenue_usd_per_patient_per_yr: A25 in assumptions.csv
        ("Core-book revenue exposure per patient"), status
        placeholder_unresolved, source = Legion data.
      - core_book_trust_spillover_rate_pct: A26 in assumptions.csv
        ("Core-book trust-spillover rate"), status placeholder_unresolved,
        validation method = patient concept test.

    This term is structurally new: it is included in every scenario and
    sensitivity run (not switched off / defaulted to zero in the base
    case), but its base-case value is deliberately set small so it reads
    as visibly provisional rather than a considered central estimate —
    see assumptions.csv A25/A26 notes.

    Formula:
        core_book_contagion_cost_per_patient_per_yr =
            core_book_revenue_usd_per_patient_per_yr
            * (core_book_trust_spillover_rate_pct / 100)
    """
    if core_book_revenue_usd_per_patient_per_yr < 0:
        raise ValueError("core_book_revenue_usd_per_patient_per_yr cannot be negative")
    if not (0 <= core_book_trust_spillover_rate_pct <= 100):
        raise ValueError("core_book_trust_spillover_rate_pct must be within [0, 100]")
    return core_book_revenue_usd_per_patient_per_yr * (core_book_trust_spillover_rate_pct / 100.0)


def fully_loaded_incremental_cost_per_patient_per_yr(inputs: FullyLoadedCostInputs) -> float:
    """
    Fully loaded incremental cost per patient per year.

    Formula:
        fully_loaded_cost = care_delivery_cost
                           + sponsor_servicing_cost
                           + commercial_cost
                           + compliance_cost
                           + trust_churn_cost
                           + core_book_contagion_cost
        (all terms per patient per year, USD; core_book_contagion_cost is
        a structurally new, entirely placeholder term added post
        v2 model revision — see core_book_contagion_cost_per_patient_per_yr()
        and assumptions.csv A25/A26)
    """
    return (
        inputs.care_delivery_cost_per_patient_per_yr_usd
        + inputs.sponsor_servicing_cost_per_patient_per_yr_usd
        + inputs.commercial_cost_per_patient_per_yr_usd
        + inputs.compliance_cost_per_patient_per_yr_usd
        + inputs.trust_churn_cost_per_patient_per_yr_usd
        + inputs.core_book_contagion_cost_per_patient_per_yr_usd
    )


# ---------------------------------------------------------------------------
# 3. Required sponsor revenue (Gate 1 economic test)
# ---------------------------------------------------------------------------

def required_sponsor_revenue_per_patient_per_yr(
    fully_loaded_cost_usd_per_patient_per_yr: float,
    target_contribution_margin_pct: float,
) -> float:
    """
    Required sponsor revenue per patient per year to hit a target
    contribution margin m.

    Formula (decision_framework.md Gate 1):
        required_revenue = fully_loaded_cost / (1 - m)

    target_contribution_margin_pct expressed as a fraction in (0, 1)
    (e.g., 0.25 for 25%). Raises if m >= 1 (undefined/negative-cost masking).
    """
    if not (0 <= target_contribution_margin_pct < 1):
        raise ValueError("target_contribution_margin_pct must be in [0, 1)")
    return fully_loaded_cost_usd_per_patient_per_yr / (1 - target_contribution_margin_pct)


def contribution_margin_pct(
    sponsor_revenue_usd_per_patient_per_yr: float,
    fully_loaded_cost_usd_per_patient_per_yr: float,
) -> float:
    """
    Realized contribution margin given actual sponsor revenue and fully
    loaded cost.

    Formula:
        m = (revenue - fully_loaded_cost) / revenue

    Returns a fraction (can be negative if cost > revenue — negative
    economics are NOT masked/clipped).  Raises ZeroDivisionError if
    revenue is exactly 0 (caller should guard/report as undefined, not
    silently coerce to 0).
    """
    if sponsor_revenue_usd_per_patient_per_yr == 0:
        raise ZeroDivisionError("sponsor_revenue_usd_per_patient_per_yr is 0; margin undefined")
    return (
        sponsor_revenue_usd_per_patient_per_yr - fully_loaded_cost_usd_per_patient_per_yr
    ) / sponsor_revenue_usd_per_patient_per_yr


def gross_margin_pct(
    revenue_usd_per_patient_per_yr: float,
    care_delivery_cost_usd_per_patient_per_yr: float,
) -> float:
    """
    Gross margin = (revenue - care delivery COGS only) / revenue.

    Distinct from contribution_margin_pct(), which nets out sponsor
    servicing, commercial, compliance, and trust-churn costs in addition
    to care delivery COGS. Legion's reported ~53% visit gross margin
    (context given by the CEO, not modeled here as Legion data) refers to
    this narrower measure.
    """
    if revenue_usd_per_patient_per_yr == 0:
        raise ZeroDivisionError("revenue_usd_per_patient_per_yr is 0; margin undefined")
    return (
        revenue_usd_per_patient_per_yr - care_delivery_cost_usd_per_patient_per_yr
    ) / revenue_usd_per_patient_per_yr


# ---------------------------------------------------------------------------
# 4. Monetization models A-E
# ---------------------------------------------------------------------------

def model_a_programmatic_ad_revenue_per_patient_per_yr(
    sessions_per_patient_per_yr: float,
    ads_per_session: float,
    fill_rate_pct: float,
    ecpm_usd_per_1000_impressions: float,
    platform_fee_pct: float,
) -> float:
    """
    Model A — Programmatic advertising.

    Formula:
        impressions_per_patient_per_yr = sessions_per_patient_per_yr * ads_per_session * fill_rate_pct
        gross_ad_revenue_per_patient_per_yr = impressions_per_patient_per_yr * ecpm / 1000
        net_ad_revenue_per_patient_per_yr = gross_ad_revenue_per_patient_per_yr * (1 - platform_fee_pct)

    fill_rate_pct and platform_fee_pct expressed as fractions in (0, 1).
    """
    if not (0 <= fill_rate_pct <= 1):
        raise ValueError("fill_rate_pct must be within [0, 1]")
    if not (0 <= platform_fee_pct <= 1):
        raise ValueError("platform_fee_pct must be within [0, 1]")
    impressions_per_patient_per_yr = sessions_per_patient_per_yr * ads_per_session * fill_rate_pct
    gross_ad_revenue = impressions_per_patient_per_yr * ecpm_usd_per_1000_impressions / 1000.0
    return gross_ad_revenue * (1 - platform_fee_pct)


def model_b_fixed_fee_sponsorship_arpu(
    num_sponsors: float,
    annual_contract_value_usd: float,
    exposed_patients: float,
    sales_servicing_cost_usd_per_yr: float,
) -> float:
    """
    Model B — Fixed-fee sponsorship, net of sales + servicing.

    Formula:
        gross_arpu = (num_sponsors * annual_contract_value_usd) / exposed_patients
        net_arpu   = gross_arpu - (sales_servicing_cost_usd_per_yr / exposed_patients)

    Returns net ARPU (USD/patient/yr). Raises if exposed_patients <= 0.
    """
    if exposed_patients <= 0:
        raise ValueError("exposed_patients must be positive")
    gross_arpu = (num_sponsors * annual_contract_value_usd) / exposed_patients
    net_arpu = gross_arpu - (sales_servicing_cost_usd_per_yr / exposed_patients)
    return net_arpu


def model_c_performance_partnership_revenue_per_patient_per_yr(
    qualified_actions_per_patient_per_yr: float,
    revenue_per_action_usd: float,
) -> float:
    """
    Model C — Performance-based partnership.

    FLAG: decision_framework.md requires legal review before real-world use
    (steering-risk / prohibited referral incentives, Gate 4). Modeled here
    for economic comparison ONLY; not a recommendation to deploy.

    Formula:
        revenue_per_patient_per_yr = qualified_actions_per_patient_per_yr * revenue_per_action_usd
    """
    return qualified_actions_per_patient_per_yr * revenue_per_action_usd


def model_d_employer_underwriting_arpu(
    pmpm_usd: float,
    utilization_adjustment_pct: float,
) -> float:
    """
    Model D — Employer/payer underwriting.

    Formula:
        annual_pmpm = pmpm_usd * 12
        arpu = annual_pmpm * utilization_adjustment_pct

    utilization_adjustment_pct expressed as a fraction in (0, 1),
    representing the share of covered lives who actively engage /
    the utilization-adjusted realization of the nominal PMPM rate.
    """
    if not (0 <= utilization_adjustment_pct <= 1):
        raise ValueError("utilization_adjustment_pct must be within [0, 1]")
    return pmpm_usd * 12 * utilization_adjustment_pct


def model_e_foundation_underwriting_arpu(
    grant_usd_per_yr: float,
    cohort_size_patients: float,
    duration_yrs: float,
) -> float:
    """
    Model E — Foundation/nonprofit underwriting.

    Formula:
        arpu = grant_usd_per_yr / cohort_size_patients

    duration_yrs is accepted and returned for transparency (grants are
    typically multi-year commitments; ARPU itself is an annual rate and
    does not divide by duration, since grant_usd_per_yr is already
    an annual figure). Raises if cohort_size_patients <= 0.
    """
    if cohort_size_patients <= 0:
        raise ValueError("cohort_size_patients must be positive")
    if duration_yrs <= 0:
        raise ValueError("duration_yrs must be positive")
    return grant_usd_per_yr / cohort_size_patients


# ---------------------------------------------------------------------------
# 5. North-star metric
# ---------------------------------------------------------------------------

def risk_adjusted_contribution_margin_per_patient_per_yr(
    sponsor_revenue_usd_per_patient_per_yr: float,
    care_delivery_cost_usd_per_patient_per_yr: float,
    sponsor_servicing_cost_usd_per_patient_per_yr: float,
    commercial_cost_usd_per_patient_per_yr: float,
    compliance_cost_usd_per_patient_per_yr: float,
    trust_churn_cost_usd_per_patient_per_yr: float,
    core_book_contagion_cost_usd_per_patient_per_yr: float,
) -> float:
    """
    North-star metric: Risk-adjusted contribution margin per eligible
    patient (decision_framework.md).

    Formula:
        north_star = sponsor_revenue
                    - care_delivery_cost
                    - sponsor_servicing_cost
                    - commercial_cost
                    - compliance_cost
                    - trust_churn_cost
                    - core_book_contagion_cost
        (all terms per patient per year, USD; "risk-adjusted" because the
        trust_churn_cost and core_book_contagion_cost terms already
        discount revenue for trust/behavioral risk, and cost ranges should
        be run at low/base/high scenarios rather than a single point
        estimate. core_book_contagion_cost is a structurally new term
        added post v2 model revision — see
        core_book_contagion_cost_per_patient_per_yr() and assumptions.csv
        A25/A26 — netting a placeholder trust-spillover rate against
        Legion's EXISTING core fee-for-service revenue per patient, as
        distinct from trust_churn_cost which nets only against sponsor-
        tier ARPU.)

    This is a $/patient/yr figure (NOT a percentage); it can be negative,
    which is not masked or floored at zero.
    """
    return (
        sponsor_revenue_usd_per_patient_per_yr
        - care_delivery_cost_usd_per_patient_per_yr
        - sponsor_servicing_cost_usd_per_patient_per_yr
        - commercial_cost_usd_per_patient_per_yr
        - compliance_cost_usd_per_patient_per_yr
        - trust_churn_cost_usd_per_patient_per_yr
        - core_book_contagion_cost_usd_per_patient_per_yr
    )


# ---------------------------------------------------------------------------
# 6. Valuation backsolve (H4)
# ---------------------------------------------------------------------------

def required_revenue_for_valuation(
    target_valuation_usd: float,
    revenue_multiple_x: float,
) -> float:
    """
    Required annual revenue to justify a target valuation at a given
    revenue multiple.

    Formula:
        required_revenue_usd = target_valuation_usd / revenue_multiple_x
    """
    if revenue_multiple_x <= 0:
        raise ValueError("revenue_multiple_x must be positive")
    return target_valuation_usd / revenue_multiple_x


def required_active_patients(
    required_revenue_usd_per_yr: float,
    arpu_usd_per_patient_per_yr: float,
) -> float:
    """
    Required active/eligible patients to hit a required revenue figure at
    a given ARPU.

    Formula:
        required_patients = required_revenue_usd_per_yr / arpu_usd_per_patient_per_yr
    """
    if arpu_usd_per_patient_per_yr <= 0:
        raise ValueError("arpu_usd_per_patient_per_yr must be positive")
    return required_revenue_usd_per_yr / arpu_usd_per_patient_per_yr


def required_sponsor_count_and_concentration(
    required_revenue_usd_per_yr: float,
    annual_contract_value_usd: float,
) -> Dict[str, float]:
    """
    Model B-specific: required sponsor count and implied concentration
    (revenue per sponsor as % of total required revenue, assuming equal
    contract sizes).

    Formula:
        required_sponsors = required_revenue_usd_per_yr / annual_contract_value_usd
        concentration_pct_per_sponsor = 1 / required_sponsors   (equal-weight assumption)

    Returns dict with keys: required_sponsors, concentration_pct_per_sponsor.
    """
    if annual_contract_value_usd <= 0:
        raise ValueError("annual_contract_value_usd must be positive")
    required_sponsors = required_revenue_usd_per_yr / annual_contract_value_usd
    concentration_pct_per_sponsor = 1.0 / required_sponsors if required_sponsors > 0 else float("inf")
    return {
        "required_sponsors": required_sponsors,
        "concentration_pct_per_sponsor": concentration_pct_per_sponsor,
    }


def free_care_acquisition_breakeven_conversion_rate(
    free_episode_cost_usd: float,
    cac_usd: float,
) -> float:
    """
    "Free care as an acquisition channel" funnel lens (Legion data —
    see data/ceo_data_integration.md #8/#9 and assumptions.csv A02b/A28).

    A free mostly-AI-driven episode costs ~$2-25/episode (A02b) to deliver,
    vs. Legion's stated paid customer-acquisition cost (CAC) of ~$250
    (A28). If a fraction of free-episode users go on to become an
    acquired, reimbursed patient (i.e., "convert"), the free episode is an
    alternative acquisition mechanic, not just a cost center. This
    function solves for the BREAK-EVEN conversion rate: the conversion
    rate at which the free episode's cost, amortized over converted
    patients, exactly equals CAC.

    Formula:
        cost_per_converted_patient = free_episode_cost_usd / conversion_rate
        break-even when cost_per_converted_patient == cac_usd, i.e.:
        breakeven_conversion_rate = free_episode_cost_usd / cac_usd

    A realized conversion rate ABOVE this break-even rate means free AI
    care is a CHEAPER acquisition channel than paid CAC; below it, paid
    CAC remains cheaper per acquired patient. This does not change
    whether free care can be fully FUNDED by ads/sponsorship (see Models
    A-E elsewhere in this module) — it is an independent, second lens on
    the same free-episode cost figure.

    Returns a fraction in (0, ...) — NOT clamped to [0, 1]; a result above
    1.0 would indicate the free episode alone already costs more than CAC
    even at a 100% conversion rate (not expected at current A02b/A28
    magnitudes, but not masked if it occurred).
    """
    if cac_usd <= 0:
        raise ValueError("cac_usd must be positive")
    if free_episode_cost_usd < 0:
        raise ValueError("free_episode_cost_usd cannot be negative")
    return free_episode_cost_usd / cac_usd


def required_grantor_count_and_concentration(
    required_revenue_usd_per_yr: float,
    reference_grant_size_usd: float,
) -> Dict[str, float]:
    """
    Model E-specific: required number of foundation/grantor funders and
    implied concentration, mirroring required_sponsor_count_and_concentration()
    for Model B. Added post v2 model revision
    (model v2 review Attack 7.2: "Apply the same
    backsolve rigor to Model E (required grantors/grant pool size at $1B
    target) that was applied to Model B (required sponsors), so the 'E
    doesn't scale' claim is demonstrated, not asserted.").

    Formula:
        required_grantors = required_revenue_usd_per_yr / reference_grant_size_usd
        concentration_pct_per_grantor = 1 / required_grantors   (equal-weight assumption)

    reference_grant_size_usd is the illustrative single-grantor/foundation
    annual grant size (A27 in assumptions.csv — a placeholder,
    policy-lever denominator held at base case across scenarios, analogous
    to A24's role for Model B), NOT a market-sized estimate of how many
    qualified grantors actually exist.

    Returns dict with keys: required_grantors, concentration_pct_per_grantor.
    """
    if reference_grant_size_usd <= 0:
        raise ValueError("reference_grant_size_usd must be positive")
    required_grantors = required_revenue_usd_per_yr / reference_grant_size_usd
    concentration_pct_per_grantor = 1.0 / required_grantors if required_grantors > 0 else float("inf")
    return {
        "required_grantors": required_grantors,
        "concentration_pct_per_grantor": concentration_pct_per_grantor,
    }
