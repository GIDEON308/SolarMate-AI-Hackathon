import unittest
from decimal import Decimal

from solarmate.analysis import analyze_case
from solarmate.guidance import guidance_for_case


PRIMARY_CASE = {
    "system_voltage": "24",
    "battery_quantity": "2",
    "battery_voltage": "12",
    "battery_capacity_ah": "220",
    "connection": "series",
    "battery_type": "Tubular lead-acid",
    "inverter_rating_w": "3500",
    "load_w": "1000",
    "symptom": "inverter_shutdown_under_load",
}


class AnalyzeCaseTests(unittest.TestCase):
    def test_primary_demo_calculations_and_labels(self):
        errors, result = analyze_case(PRIMARY_CASE)

        self.assertEqual(errors, {})
        self.assertEqual(result["bank_voltage"], Decimal("24"))
        self.assertEqual(result["bank_capacity_ah"], Decimal("220"))
        self.assertEqual(result["nominal_energy_wh"], Decimal("5280"))
        self.assertEqual(result["nominal_energy_kwh"], Decimal("5.28"))
        self.assertEqual(result["nominal_energy_display"], "5.28")
        self.assertEqual(
            result["estimated_dc_current_display"],
            "41.7",
        )
        self.assertEqual(result["inverter_loading_display"], "28.6")
        self.assertTrue(result["load_below_rating"])
        self.assertIn("not indicated", result["inverter_interpretation"])
        guidance = guidance_for_case(result)
        self.assertIn("not a measured battery current", guidance["current_explanation"])
        self.assertIn("Usable energy can be lower", guidance["energy_explanation"])

    def test_series_parallel_bank_formulas(self):
        series_values = dict(PRIMARY_CASE)
        parallel_values = dict(PRIMARY_CASE, system_voltage="12", connection="parallel")

        series_errors, series_result = analyze_case(series_values)
        parallel_errors, parallel_result = analyze_case(parallel_values)

        self.assertEqual(series_errors, {})
        self.assertEqual(series_result["bank_voltage"], Decimal("24"))
        self.assertEqual(series_result["bank_capacity_ah"], Decimal("220"))
        self.assertEqual(parallel_errors, {})
        self.assertEqual(parallel_result["bank_voltage"], Decimal("12"))
        self.assertEqual(parallel_result["bank_capacity_ah"], Decimal("440"))

    def test_evidence_findings_compare_valid_readings_cautiously(self):
        values = dict(
            PRIMARY_CASE,
            battery_bank_voltage_at_rest="25.4",
            battery_bank_voltage_under_load="21.8",
            individual_battery_voltages_at_rest="12.4, 13.0",
            individual_battery_voltages_under_load="10.4, 11.4",
        )

        errors, result = analyze_case(values)

        self.assertEqual(errors, {})
        self.assertEqual(
            result["evidence_findings"],
            (
                "Battery-bank voltage dropped by 3.6 V, from 25.4 V at rest to "
                "21.8 V under load.",
                "Individual battery voltages at rest span 0.6 V, from 12.4 V to "
                "13.0 V. This may indicate battery imbalance or a connection "
                "issue; voltage readings alone do not confirm battery failure.",
                "Individual battery voltages under load span 1.0 V, from 10.4 V "
                "to 11.4 V. This may indicate battery imbalance or a connection "
                "issue; voltage readings alone do not confirm battery failure.",
                "The entered load (1000 W) is below the inverter's continuous "
                "rating (3500 W).",
            ),
        )

    def test_evidence_findings_report_load_at_or_above_inverter_rating(self):
        matching_values = dict(PRIMARY_CASE, load_w="3500")
        exceeding_values = dict(PRIMARY_CASE, load_w="4000")

        _, matching_result = analyze_case(matching_values)
        _, exceeding_result = analyze_case(exceeding_values)

        self.assertIn(
            "The entered load (3500 W) matches the inverter's continuous "
            "rating (3500 W).",
            matching_result["evidence_findings"],
        )
        self.assertIn(
            "The entered load (4000 W) exceeds the inverter's continuous "
            "rating (3500 W).",
            exceeding_result["evidence_findings"],
        )

    def test_required_input_error_blocks_analysis(self):
        values = dict(PRIMARY_CASE, battery_capacity_ah="")

        errors, result = analyze_case(values)

        self.assertEqual(errors["battery_capacity_ah"], "Battery capacity is required.")
        self.assertIsNone(result)

    def test_selected_voltage_must_match_calculated_bank(self):
        values = dict(PRIMARY_CASE, system_voltage="48")

        errors, result = analyze_case(values)

        self.assertIn("_form", errors)
        self.assertIn("does not match", errors["_form"])
        self.assertIsNone(result)

    def test_troubleshooting_sequence_and_safety_are_present(self):
        errors, result = analyze_case(PRIMARY_CASE)

        self.assertEqual(errors, {})
        guidance = guidance_for_case(result)
        expected_order = (
            "Confirm the connected load.",
            "Measure and record the battery-bank voltage with no load.",
            "Measure and record the battery-bank voltage while the load is running.",
            "For a series bank, measure each battery separately",
            "Using safe procedures, inspect terminals",
            "Record any inverter fault code",
            "After correcting an identified issue, retest under load",
        )
        self.assertEqual(len(guidance["checks"]), len(expected_order))
        for check, expected_start in zip(guidance["checks"], expected_order):
            self.assertTrue(check.startswith(expected_start))
        self.assertTrue(any("PPE" in note for note in guidance["safety"]))
        self.assertTrue(any("qualified technical assistance" in note for note in guidance["safety"]))


if __name__ == "__main__":
    unittest.main()
