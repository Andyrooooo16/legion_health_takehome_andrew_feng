"""
Unit tests for model.py (core formulas), plus ordering/consistency checks
against model/assumptions.csv and model/outputs.csv.

Run: python3 -m pytest model/tests/test_model.py -v
  or: python3 model/tests/test_model.py  (falls back to unittest runner)
"""

import csv
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import model as m

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.dirname(HERE)
ASSUMPTIONS_CSV = os.path.join(MODEL_DIR, "assumptions.csv")
OUTPUTS_CSV = os.path.join(MODEL_DIR, "outputs.csv")


class TestPathwayCost(unittest.TestCase):
    def test_hand_computed_traditional(self):
        """8 visits/yr * $150/visit = $1,200/yr."""
        inputs = m.PathwayCostInputs(pathway="traditional", cost_per_unit_usd=150, units_per_patient_per_yr=8)
        self.assertAlmostEqual(m.care_delivery_cost_per_patient_per_yr(inputs), 1200.0)

    def test_hand_computed_ai_driven(self):
        """6 episodes/yr * $35/episode = $210/yr."""
        inputs = m.PathwayCostInputs(pathway="ai_driven", cost_per_unit_usd=35, units_per_patient_per_yr=6)
        self.assertAlmostEqual(m.care_delivery_cost_per_patient_per_yr(inputs), 210.0)

    def test_rejects_unknown_pathway(self):
        with self.assertRaises(ValueError):
            m.PathwayCostInputs(pathway="robot_army", cost_per_unit_usd=10, units_per_patient_per_yr=1)

    def test_rejects_negative_cost(self):
        with self.assertRaises(ValueError):
            m.PathwayCostInputs(pathway="traditional", cost_per_unit_usd=-1, units_per_patient_per_yr=1)

    def test_rejects_negative_units(self):
        with self.assertRaises(ValueError):
            m.PathwayCostInputs(pathway="traditional", cost_per_unit_usd=1, units_per_patient_per_yr=-1)

    def test_pathway_unit_cost_ordering_traditional_gt_ai_supported_gt_ai_driven(self):
        """
        Per decision_framework.md's explicit qualitative table: traditional
        (High) > AI-supported (Medium) > mostly-AI-driven (Low) relative
        COST-PER-UNIT (A01 > A02 > A02b). This is the ordering the CEO's
        Legion data (data/ceo_data_integration.md) anchors and
        preserves at base case: $74 > $37 > $8.
        """
        rows = _load_assumptions_rows()
        self.assertGreater(float(rows["A01"]["base"]), float(rows["A02"]["base"]))
        self.assertGreater(float(rows["A02"]["base"]), float(rows["A02b"]["base"]))

    def test_pathway_ANNUAL_cost_ordering_no_longer_holds_post_legion_data_KNOWN_TENSION(self):
        """
        Known tension after Legion data integration: annual pathway cost
        ordering can invert when A03b/A04 remain placeholders. Legion
        updated A01/A02/A02b and A03 but not AI-pathway frequencies.
        At base case: traditional ($74 x 5.3 = $392) < ai_supported
        ($37 x 12 = $444) even though unit costs are correctly ordered.
        Documented explicitly — not silently patched.
        """
        rows = _load_assumptions_rows()
        trad_cost = float(rows["A01"]["base"]) * float(rows["A03"]["base"])
        ai_sup_cost = float(rows["A02"]["base"]) * float(rows["A03b"]["base"])
        ai_driven_cost = float(rows["A02b"]["base"]) * float(rows["A04"]["base"])
        # Documented as a known, flagged tension -- NOT asserted as "correct":
        self.assertGreater(ai_sup_cost, trad_cost, msg=(
            "If this assertion ever fails, A03b has been revised (intentionally "
            "or not) -- re-check model_readme.md v3's tension note, it may be stale."
        ))
        self.assertGreater(trad_cost, ai_driven_cost)
        self.assertGreater(ai_sup_cost, ai_driven_cost)


class TestFullyLoadedCost(unittest.TestCase):
    def test_hand_computed_sum(self):
        """1000+50+25+10+5+15 = 1105 (adds core_book_contagion_cost, v2)."""
        inputs = m.FullyLoadedCostInputs(
            care_delivery_cost_per_patient_per_yr_usd=1000,
            sponsor_servicing_cost_per_patient_per_yr_usd=50,
            commercial_cost_per_patient_per_yr_usd=25,
            compliance_cost_per_patient_per_yr_usd=10,
            trust_churn_cost_per_patient_per_yr_usd=5,
            core_book_contagion_cost_per_patient_per_yr_usd=15,
        )
        self.assertAlmostEqual(m.fully_loaded_incremental_cost_per_patient_per_yr(inputs), 1105.0)

    def test_trust_churn_cost_formula(self):
        """
        baseline_arpu=100, conv_loss_pp=4, ret_loss_pp=5 ->
        combined_loss_fraction = 9/100 = 0.09 -> cost = 100*0.09 = 9.0
        """
        cost = m.trust_churn_cost_per_patient_per_yr(
            baseline_arpu_usd_per_patient_per_yr=100,
            trust_conversion_loss_pp=4,
            trust_retention_loss_pp=5,
            baseline_conversion_rate_pct=70,
        )
        self.assertAlmostEqual(cost, 9.0)

    def test_trust_churn_rejects_bad_baseline_conversion(self):
        with self.assertRaises(ValueError):
            m.trust_churn_cost_per_patient_per_yr(100, 4, 5, baseline_conversion_rate_pct=150)


class TestCoreBookContagionCost(unittest.TestCase):
    """
    Tests for the SECOND, separate trust-cost term added post
    model v2 review Attack #5 / 2.5: core-book contagion cost, which
    nets a placeholder spillover rate against Legion's EXISTING core FFS
    revenue per patient (A25/A26), distinct from trust_churn_cost_per_patient_per_yr()
    which nets only against sponsor-tier ARPU.
    """

    def test_hand_computed(self):
        """core_book_revenue=1500, spillover_rate_pct=0.5 -> 1500*0.005 = 7.5."""
        cost = m.core_book_contagion_cost_per_patient_per_yr(
            core_book_revenue_usd_per_patient_per_yr=1500,
            core_book_trust_spillover_rate_pct=0.5,
        )
        self.assertAlmostEqual(cost, 7.5)

    def test_rejects_negative_core_book_revenue(self):
        with self.assertRaises(ValueError):
            m.core_book_contagion_cost_per_patient_per_yr(-1, 0.5)

    def test_rejects_bad_spillover_rate(self):
        with self.assertRaises(ValueError):
            m.core_book_contagion_cost_per_patient_per_yr(1500, 150)

    def test_zero_spillover_rate_yields_zero_cost(self):
        """Sanity: 0% spillover -> $0 contagion cost, not masked/forced positive."""
        cost = m.core_book_contagion_cost_per_patient_per_yr(1500, 0)
        self.assertAlmostEqual(cost, 0.0)

    def test_core_book_contagion_cost_is_separate_from_trust_churn_cost(self):
        """
        Same core-book revenue figure plugged into the two different-scope
        formulas should NOT generally produce the same cost, demonstrating
        the two trust-related terms are genuinely distinct (sponsor-tier
        ARPU scope vs. core-book revenue scope).
        """
        sponsor_scope_cost = m.trust_churn_cost_per_patient_per_yr(
            baseline_arpu_usd_per_patient_per_yr=15,  # sponsor-tier ARPU (A05 base)
            trust_conversion_loss_pp=4,
            trust_retention_loss_pp=5,
            baseline_conversion_rate_pct=70,
        )
        core_book_scope_cost = m.core_book_contagion_cost_per_patient_per_yr(
            core_book_revenue_usd_per_patient_per_yr=1500,  # core-book revenue (A25 base)
            core_book_trust_spillover_rate_pct=0.5,
        )
        self.assertNotAlmostEqual(sponsor_scope_cost, core_book_scope_cost)


class TestRequiredRevenueAndMargins(unittest.TestCase):
    def test_required_revenue_hand_computed(self):
        """cost=750, m=0.25 -> required = 750 / 0.75 = 1000."""
        self.assertAlmostEqual(m.required_sponsor_revenue_per_patient_per_yr(750, 0.25), 1000.0)

    def test_required_revenue_matches_gate1_133x_approximation(self):
        """decision_framework.md: at m=25%, revenue ~= 1.33x cost."""
        cost = 1000.0
        required = m.required_sponsor_revenue_per_patient_per_yr(cost, 0.25)
        self.assertAlmostEqual(required / cost, 1.3333333, places=4)

    def test_required_revenue_rejects_margin_of_one(self):
        with self.assertRaises(ValueError):
            m.required_sponsor_revenue_per_patient_per_yr(100, 1.0)

    def test_required_revenue_rejects_negative_margin(self):
        with self.assertRaises(ValueError):
            m.required_sponsor_revenue_per_patient_per_yr(100, -0.1)

    def test_contribution_margin_hand_computed(self):
        """revenue=1000, cost=750 -> m = 250/1000 = 0.25."""
        self.assertAlmostEqual(m.contribution_margin_pct(1000, 750), 0.25)

    def test_contribution_margin_can_be_negative_not_masked(self):
        """revenue=100, cost=1000 -> m = -9.0 (900% negative margin), not clipped to 0."""
        margin = m.contribution_margin_pct(100, 1000)
        self.assertAlmostEqual(margin, -9.0)
        self.assertLess(margin, 0)

    def test_contribution_margin_zero_revenue_raises(self):
        with self.assertRaises(ZeroDivisionError):
            m.contribution_margin_pct(0, 100)

    def test_gross_margin_hand_computed(self):
        """revenue=1000, care_cost=470 (53% gross margin case) -> (1000-470)/1000=0.53."""
        self.assertAlmostEqual(m.gross_margin_pct(1000, 470), 0.53)

    def test_gross_margin_distinct_from_contribution_margin(self):
        """
        Same revenue/care-cost pair should yield a HIGHER gross margin than
        contribution margin once additional fully-loaded costs are added,
        demonstrating the two are genuinely distinct metrics.
        """
        revenue = 1000.0
        care_cost = 470.0
        gross = m.gross_margin_pct(revenue, care_cost)
        fully_loaded_cost = care_cost + 100 + 50 + 30 + 20  # add servicing/commercial/compliance/trust
        contribution = m.contribution_margin_pct(revenue, fully_loaded_cost)
        self.assertGreater(gross, contribution)


class TestMonetizationModels(unittest.TestCase):
    def test_model_a_hand_computed(self):
        """
        sessions=52/yr, ads/session=2, fill=0.7, ecpm=30, platform_fee=0.3
        impressions = 52*2*0.7 = 72.8
        gross = 72.8*30/1000 = 2.184
        net = 2.184*0.7 = 1.5288
        """
        rev = m.model_a_programmatic_ad_revenue_per_patient_per_yr(
            sessions_per_patient_per_yr=52, ads_per_session=2, fill_rate_pct=0.7,
            ecpm_usd_per_1000_impressions=30, platform_fee_pct=0.3,
        )
        self.assertAlmostEqual(rev, 1.5288, places=4)

    def test_model_a_rejects_bad_fill_rate(self):
        with self.assertRaises(ValueError):
            m.model_a_programmatic_ad_revenue_per_patient_per_yr(52, 2, 1.5, 30, 0.3)

    def test_model_b_hand_computed(self):
        """
        3 sponsors * $250,000 / 150,000 patients = $5.00 gross ARPU
        sales_servicing = $450,000 / 150,000 = $3.00
        net = 5.00 - 3.00 = $2.00
        """
        arpu = m.model_b_fixed_fee_sponsorship_arpu(
            num_sponsors=3, annual_contract_value_usd=250_000, exposed_patients=150_000,
            sales_servicing_cost_usd_per_yr=450_000,
        )
        self.assertAlmostEqual(arpu, 2.0)

    def test_model_b_rejects_zero_patients(self):
        with self.assertRaises(ValueError):
            m.model_b_fixed_fee_sponsorship_arpu(3, 250_000, 0, 450_000)

    def test_model_c_hand_computed(self):
        """8 actions/yr * $10/action = $80/yr."""
        rev = m.model_c_performance_partnership_revenue_per_patient_per_yr(8, 10)
        self.assertAlmostEqual(rev, 80.0)

    def test_model_d_hand_computed(self):
        """pmpm=50, util_adj=0.55 -> 50*12*0.55 = 330."""
        arpu = m.model_d_employer_underwriting_arpu(pmpm_usd=50, utilization_adjustment_pct=0.55)
        self.assertAlmostEqual(arpu, 330.0)

    def test_model_d_rejects_bad_utilization(self):
        with self.assertRaises(ValueError):
            m.model_d_employer_underwriting_arpu(50, 1.2)

    def test_model_e_hand_computed(self):
        """grant=750,000 / cohort=1000 = $750/patient/yr."""
        arpu = m.model_e_foundation_underwriting_arpu(grant_usd_per_yr=750_000, cohort_size_patients=1000, duration_yrs=2)
        self.assertAlmostEqual(arpu, 750.0)

    def test_model_e_rejects_zero_cohort(self):
        with self.assertRaises(ValueError):
            m.model_e_foundation_underwriting_arpu(750_000, 0, 2)

    def test_model_e_rejects_zero_duration(self):
        with self.assertRaises(ValueError):
            m.model_e_foundation_underwriting_arpu(750_000, 1000, 0)


class TestNorthStar(unittest.TestCase):
    def test_north_star_hand_computed(self):
        """750 - 500 - 50 - 25 - 10 - 5 - 8 = 152 (adds core_book_contagion_cost, v2)."""
        val = m.risk_adjusted_contribution_margin_per_patient_per_yr(
            sponsor_revenue_usd_per_patient_per_yr=750,
            care_delivery_cost_usd_per_patient_per_yr=500,
            sponsor_servicing_cost_usd_per_patient_per_yr=50,
            commercial_cost_usd_per_patient_per_yr=25,
            compliance_cost_usd_per_patient_per_yr=10,
            trust_churn_cost_usd_per_patient_per_yr=5,
            core_book_contagion_cost_usd_per_patient_per_yr=8,
        )
        self.assertAlmostEqual(val, 152.0)

    def test_north_star_can_be_negative_not_masked(self):
        """15 - 1200 - 1 - 1 - 1 - 1 - 1 should be a large negative number, not zero."""
        val = m.risk_adjusted_contribution_margin_per_patient_per_yr(
            sponsor_revenue_usd_per_patient_per_yr=15,
            care_delivery_cost_usd_per_patient_per_yr=1200,
            sponsor_servicing_cost_usd_per_patient_per_yr=1,
            commercial_cost_usd_per_patient_per_yr=1,
            compliance_cost_usd_per_patient_per_yr=1,
            trust_churn_cost_usd_per_patient_per_yr=1,
            core_book_contagion_cost_usd_per_patient_per_yr=1,
        )
        self.assertLess(val, 0)
        self.assertAlmostEqual(val, 15 - 1200 - 1 - 1 - 1 - 1 - 1)


class TestValuationBacksolve(unittest.TestCase):
    def test_required_revenue_hand_computed(self):
        """$1B / 10x = $100M."""
        self.assertAlmostEqual(m.required_revenue_for_valuation(1_000_000_000, 10), 100_000_000)

    def test_required_revenue_rejects_zero_multiple(self):
        with self.assertRaises(ValueError):
            m.required_revenue_for_valuation(1_000_000_000, 0)

    def test_required_patients_hand_computed(self):
        """$100M / $15 ARPU = 6,666,666.67 patients."""
        patients = m.required_active_patients(100_000_000, 15)
        self.assertAlmostEqual(patients, 100_000_000 / 15)

    def test_required_patients_rejects_zero_arpu(self):
        with self.assertRaises(ValueError):
            m.required_active_patients(100_000_000, 0)

    def test_required_patients_higher_multiple_means_fewer_patients_needed(self):
        """Higher revenue multiple -> lower required revenue -> fewer required patients, at fixed ARPU."""
        arpu = 15.0
        patients_at_5x = m.required_active_patients(m.required_revenue_for_valuation(1e9, 5), arpu)
        patients_at_20x = m.required_active_patients(m.required_revenue_for_valuation(1e9, 20), arpu)
        self.assertGreater(patients_at_5x, patients_at_20x)

    def test_sponsor_count_and_concentration_hand_computed(self):
        """required_revenue=$100M, contract=$250,000 -> 400 sponsors, 0.25% concentration each."""
        result = m.required_sponsor_count_and_concentration(100_000_000, 250_000)
        self.assertAlmostEqual(result["required_sponsors"], 400.0)
        self.assertAlmostEqual(result["concentration_pct_per_sponsor"], 1.0 / 400.0)

    def test_sponsor_count_rejects_zero_contract_value(self):
        with self.assertRaises(ValueError):
            m.required_sponsor_count_and_concentration(100_000_000, 0)

    def test_grantor_count_and_concentration_hand_computed(self):
        """
        Model E scale backsolve (added post model v2 review Attack
        7.2, mirroring required_sponsor_count_and_concentration for Model
        B): required_revenue=$100M, reference grant size=$750,000 ->
        133.33 grantors, 0.75% concentration each.
        """
        result = m.required_grantor_count_and_concentration(100_000_000, 750_000)
        self.assertAlmostEqual(result["required_grantors"], 100_000_000 / 750_000)
        self.assertAlmostEqual(result["concentration_pct_per_grantor"], 750_000 / 100_000_000)

    def test_grantor_count_rejects_zero_reference_grant_size(self):
        with self.assertRaises(ValueError):
            m.required_grantor_count_and_concentration(100_000_000, 0)

    def test_grantor_count_higher_multiple_means_fewer_grantors_needed(self):
        """Higher revenue multiple -> lower required revenue -> fewer required grantors, at fixed reference grant size."""
        ref_grant_size = 750_000.0
        grantors_at_5x = m.required_grantor_count_and_concentration(
            m.required_revenue_for_valuation(1e9, 5), ref_grant_size
        )["required_grantors"]
        grantors_at_20x = m.required_grantor_count_and_concentration(
            m.required_revenue_for_valuation(1e9, 20), ref_grant_size
        )["required_grantors"]
        self.assertGreater(grantors_at_5x, grantors_at_20x)


class TestFreeCareAcquisitionFunnelLens(unittest.TestCase):
    """
    Tests for the "free care as acquisition channel" funnel lens
    channel" funnel lens: m.free_care_acquisition_breakeven_conversion_rate()
    compares A02b (free AI-driven episode cost) against A28 (CAC, $250).
    """

    def test_hand_computed_base_case(self):
        """A02b base=$8, A28=$250 -> breakeven = 8/250 = 0.032 (3.2%)."""
        rate = m.free_care_acquisition_breakeven_conversion_rate(
            free_episode_cost_usd=8, cac_usd=250
        )
        self.assertAlmostEqual(rate, 0.032)

    def test_hand_computed_low_and_high_case(self):
        """A02b low=$2 -> 2/250=0.008 (0.8%); A02b high=$25 -> 25/250=0.10 (10%)."""
        self.assertAlmostEqual(
            m.free_care_acquisition_breakeven_conversion_rate(2, 250), 0.008
        )
        self.assertAlmostEqual(
            m.free_care_acquisition_breakeven_conversion_rate(25, 250), 0.10
        )

    def test_rejects_zero_or_negative_cac(self):
        with self.assertRaises(ValueError):
            m.free_care_acquisition_breakeven_conversion_rate(8, 0)
        with self.assertRaises(ValueError):
            m.free_care_acquisition_breakeven_conversion_rate(8, -250)

    def test_rejects_negative_episode_cost(self):
        with self.assertRaises(ValueError):
            m.free_care_acquisition_breakeven_conversion_rate(-1, 250)

    def test_lower_episode_cost_means_lower_breakeven_conversion_rate_needed(self):
        """Cheaper free episode -> lower conversion rate needed to beat CAC."""
        low_rate = m.free_care_acquisition_breakeven_conversion_rate(2, 250)
        high_rate = m.free_care_acquisition_breakeven_conversion_rate(25, 250)
        self.assertLess(low_rate, high_rate)


class TestNewCeoDataAssumptionsPresent(unittest.TestCase):
    """
    Sanity checks that Legion-data assumptions (A28/A29/A30) were
    added correctly and that A02b's derived low/base/high match the
    task-specified values.
    """

    @classmethod
    def setUpClass(cls):
        cls.rows = _load_assumptions_rows()

    def test_a28_a29_a30_present(self):
        for aid in ("A28", "A29", "A30"):
            self.assertIn(aid, self.rows, msg=f"{aid} missing from assumptions.csv")

    def test_a28_cac_is_250_point_estimate(self):
        row = self.rows["A28"]
        self.assertAlmostEqual(float(row["low"]), 250.0)
        self.assertAlmostEqual(float(row["base"]), 250.0)
        self.assertAlmostEqual(float(row["high"]), 250.0)

    def test_a29_a30_point_estimates(self):
        self.assertAlmostEqual(float(self.rows["A29"]["base"]), 8.1)
        self.assertAlmostEqual(float(self.rows["A30"]["base"]), 4.2)

    def test_a02b_derived_values_match_spec(self):
        row = self.rows["A02b"]
        self.assertAlmostEqual(float(row["low"]), 2.0)
        self.assertAlmostEqual(float(row["base"]), 8.0)
        self.assertAlmostEqual(float(row["high"]), 25.0)
        self.assertEqual(row["status"].strip(), "legion_derived")

    def test_a01_a02_a03_a25_legion_data_status(self):
        for aid in ("A01", "A02", "A03", "A25"):
            self.assertEqual(
                self.rows[aid]["status"].strip(), "legion_data",
                msg=f"{aid} expected status legion_data",
            )

    def test_a03_low_base_high_ordering_and_values(self):
        row = self.rows["A03"]
        self.assertAlmostEqual(float(row["low"]), 4.0)
        self.assertAlmostEqual(float(row["base"]), 5.3)
        self.assertAlmostEqual(float(row["high"]), 13.2)

    def test_a25_low_equals_base_high_is_mature_cohort_figure(self):
        row = self.rows["A25"]
        self.assertAlmostEqual(float(row["low"]), 811.0)
        self.assertAlmostEqual(float(row["base"]), 811.0)
        self.assertAlmostEqual(float(row["high"]), 2025.0)


class TestFunnelLensCsvGenerated(unittest.TestCase):
    """Sanity-check the generated model/funnel_lens.csv (requires scenarios.py's run_funnel_lens() to have run)."""

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join(MODEL_DIR, "funnel_lens.csv")
        if not os.path.exists(cls.path):
            raise unittest.SkipTest("funnel_lens.csv not found; run scenarios.run_funnel_lens() first")
        with open(cls.path, newline="", encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))

    def test_covers_all_scenarios(self):
        scenarios = {r["scenario"] for r in self.rows}
        self.assertEqual(scenarios, {"low", "base", "high"})

    def test_base_breakeven_rate_matches_expected(self):
        base_row = next(r for r in self.rows if r["scenario"] == "base")
        self.assertAlmostEqual(float(base_row["breakeven_conversion_rate_pct"]), 3.2, places=2)

    def test_cac_constant_across_scenarios(self):
        cacs = {float(r["cac_usd_A28"]) for r in self.rows}
        self.assertEqual(cacs, {250.0})


def _load_assumptions_rows():
    rows = {}
    with open(ASSUMPTIONS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows[row["assumption_id"]] = row
    return rows


class TestAssumptionsCsvIntegrity(unittest.TestCase):
    """
    Validate model/assumptions.csv itself: low <= base <= high ordering for
    every numeric assumption (both revenue-like and cost-like — ordering
    is a property of the raw low/base/high columns as stored, independent
    of scenario-direction interpretation applied downstream), and every
    row must carry a placeholder/sourced status label (never silently
    presented as Legion data).
    """

    @classmethod
    def setUpClass(cls):
        cls.rows = _load_assumptions_rows()

    def test_all_ids_present_and_numeric_ordering(self):
        skipped_non_numeric = []
        for aid, row in self.rows.items():
            try:
                low = float(row["low"])
                base = float(row["base"])
                high = float(row["high"])
            except ValueError:
                skipped_non_numeric.append(aid)
                continue
            self.assertLessEqual(low, base, msg=f"{aid}: low > base ({low} > {base})")
            self.assertLessEqual(base, high, msg=f"{aid}: base > high ({base} > {high})")
        # Every assumption in this ledger should be numeric (no unresolved
        # PLACEHOLDER strings shipped in the model-ready file); the
        # research/assumptions.csv ledger (upstream, not this file) is
        # where raw PLACEHOLDER strings still live pending Legion data.
        self.assertEqual(skipped_non_numeric, [], f"Non-numeric low/base/high found in model/assumptions.csv: {skipped_non_numeric}")

    def test_every_row_has_a_status_label(self):
        valid_statuses = {
            "placeholder_external", "placeholder_unresolved", "estimated_external",
            "awaiting_data", "awaiting_research", "set_provisional",
            "legion_data", "legion_derived",
        }
        for aid, row in self.rows.items():
            status = row["status"].strip()
            self.assertIn(status, valid_statuses, msg=f"{aid}: unexpected status {status!r}")

    def test_no_row_silently_claims_to_be_legion_sourced(self):
        """
        Guard against accidentally labeling a placeholder as if it were
        real Legion data: no status should claim direct Legion sourcing
        without going through the awaiting_data pipeline.
        """
        forbidden_terms = ("legion internal", "legion actuals", "legion confirmed")
        for aid, row in self.rows.items():
            source_lower = row["source"].lower()
            for term in forbidden_terms:
                self.assertNotIn(term, source_lower, msg=f"{aid}: source text suggests un-vetted Legion-internal claim")


class TestOutputsCsvGenerated(unittest.TestCase):
    """Sanity-check the generated outputs.csv grid (requires scenarios.py to have run)."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(OUTPUTS_CSV):
            raise unittest.SkipTest("outputs.csv not found; run scenarios.py first")
        with open(OUTPUTS_CSV, newline="", encoding="utf-8") as f:
            cls.rows = list(csv.DictReader(f))

    def test_outputs_not_empty(self):
        self.assertGreater(len(self.rows), 0)

    def test_outputs_cover_all_scenarios_pathways_models(self):
        scenarios = {r["scenario"] for r in self.rows}
        pathways = {r["pathway"] for r in self.rows}
        models = {r["model"] for r in self.rows}
        self.assertEqual(scenarios, {"low", "base", "high"})
        self.assertEqual(pathways, set(m.PATHWAYS))
        self.assertEqual(len(models), 5)

    def test_low_scenario_cost_gte_high_scenario_cost_same_pathway_model(self):
        """
        Coherent scenario check: for a fixed pathway/model, the "low"
        (pessimistic revenue + high cost) scenario's fully_loaded_cost
        should be >= the "high" scenario's fully_loaded_cost.
        """
        by_key = {}
        for r in self.rows:
            key = (r["pathway"], r["model"])
            by_key.setdefault(key, {})[r["scenario"]] = float(r["fully_loaded_cost_usd_per_patient_per_yr"])
        for key, scen_costs in by_key.items():
            self.assertGreaterEqual(
                scen_costs["low"], scen_costs["high"],
                msg=f"{key}: low-scenario cost should be >= high-scenario cost (coherent pessimistic/optimistic framing)",
            )

    def test_negative_north_star_present_not_masked(self):
        """
        Given how far current external ARPU anchors are from fully loaded
        psychiatric care costs, at least some pathway/model/scenario combos
        must show negative north-star margin — and this test fails if the
        grid has silently floored/clipped negative values to zero.
        """
        north_stars = [float(r["north_star_risk_adj_contribution_margin_usd_per_patient_per_yr"]) for r in self.rows]
        self.assertTrue(any(v < 0 for v in north_stars), "Expected at least one negative north-star value; negative economics may be masked")

    def test_core_book_contagion_cost_column_present_and_not_zero_at_base(self):
        """
        v2 (post model v2 review Attack #5 / 2.5): the core-book
        contagion cost term must be present in every row (not switched off
        in the base case) and must be strictly positive at base case,
        since A25/A26 base values are both nonzero placeholders.
        """
        self.assertIn("core_book_contagion_cost_usd_per_patient_per_yr", self.rows[0].keys())
        base_rows = [r for r in self.rows if r["scenario"] == "base"]
        self.assertTrue(base_rows, "Expected at least one base-scenario row")
        for r in base_rows:
            self.assertGreater(
                float(r["core_book_contagion_cost_usd_per_patient_per_yr"]), 0.0,
                msg="core_book_contagion_cost should be > 0 at base case (visibly provisional, not zero/off)",
            )

    def test_core_book_contagion_cost_included_in_fully_loaded_cost(self):
        """
        fully_loaded_cost should equal the sum of its five prior components
        plus core_book_contagion_cost (i.e., the new term is actually wired
        into the total, not just reported alongside it unused).
        """
        for r in self.rows:
            component_sum = (
                float(r["care_delivery_cost_usd_per_patient_per_yr"])
                + float(r["sponsor_servicing_cost_usd_per_patient_per_yr"])
                + float(r["commercial_cost_usd_per_patient_per_yr"])
                + float(r["compliance_cost_usd_per_patient_per_yr"])
                + float(r["trust_churn_cost_usd_per_patient_per_yr"])
                + float(r["core_book_contagion_cost_usd_per_patient_per_yr"])
            )
            self.assertAlmostEqual(component_sum, float(r["fully_loaded_cost_usd_per_patient_per_yr"]), places=1)

    def test_model_e_grantor_backsolve_columns_present(self):
        """
        v2 (post model v2 review Attack 7.2): Model E rows must carry
        required_annual_grant_pool / required_grantors / grantor_concentration_pct
        at each of the 5/10/15/20x multiples, mirroring Model B's
        required_sponsors treatment; non-Model-E rows should leave them
        blank (None/empty), matching the existing required_sponsors pattern.
        """
        e_rows = [r for r in self.rows if r["model"] == "E_foundation_underwriting"]
        b_rows = [r for r in self.rows if r["model"] == "B_fixed_fee_sponsorship_external_anchor"]
        self.assertTrue(e_rows, "Expected Model E rows in outputs.csv")
        for mult in (5, 10, 15, 20):
            pool_col = f"required_annual_grant_pool_at_{mult}x_for_1B"
            grantors_col = f"required_grantors_at_{mult}x_for_1B"
            conc_col = f"grantor_concentration_pct_at_{mult}x_for_1B"
            self.assertIn(pool_col, e_rows[0].keys())
            for r in e_rows:
                self.assertNotEqual(r[pool_col], "", msg=f"{pool_col} should be populated for Model E rows")
                self.assertNotEqual(r[grantors_col], "", msg=f"{grantors_col} should be populated for Model E rows")
                self.assertGreater(float(r[grantors_col]), 0)
                self.assertGreater(float(r[conc_col]), 0)
            for r in b_rows:
                self.assertEqual(r[grantors_col], "", msg=f"{grantors_col} should be blank for non-Model-E rows")


if __name__ == "__main__":
    unittest.main(verbosity=2)
