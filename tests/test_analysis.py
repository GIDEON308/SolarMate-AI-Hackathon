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
