import unittest
from unittest.mock import patch

import app as solar_app
from app import app


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


class FlaskRouteTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_home_page_displays_form_and_safety_notice(self):
        with patch.object(solar_app, "analyze_case") as analyze:
            response = self.client.get("/")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("SolarMate AI", page)
        self.assertIn("System Details", page)
        self.assertIn("Safety first", page)
        self.assertNotIn("role=\"alert\"", page)
        self.assertNotIn("Battery configuration does not match", page)
        self.assertNotIn("aria-invalid=\"true\"", page)
        analyze.assert_not_called()

    def test_primary_case_renders_calculations_checks_and_safety(self):
        response = self.client.post("/", data=PRIMARY_CASE)
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Nominal battery energy: 5.28 kWh", page)
        self.assertIn("Estimated DC current before inverter losses:", page)
        self.assertIn("41.7 A", page)
        self.assertIn("28.6% of continuous rating", page)
        self.assertIn("The entered load is below the inverter&#39;s continuous rating", page)
        self.assertIn("Troubleshooting Checks", page)
        self.assertIn("Avoid short circuits", page)

    def test_invalid_submission_preserves_entered_values(self):
        values = dict(PRIMARY_CASE, battery_capacity_ah="")

        response = self.client.post("/", data=values)
        page = response.get_data(as_text=True)

        self.assertIn("Battery capacity is required.", page)
        self.assertIn('name="load_w"', page)
        self.assertIn('value="1000"', page)
        self.assertNotIn("Nominal battery energy:", page)

    def test_bank_voltage_mismatch_is_shown_once_and_preserves_values(self):
        values = dict(PRIMARY_CASE, system_voltage="48")
        message = (
            "Battery configuration does not match the selected system voltage. "
            "Check the battery voltage, quantity, connection type, and system voltage."
        )

        response = self.client.post("/", data=values)
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(page.count(message), 1)
        self.assertIn('value="48"', page)
        self.assertIn('value="2"', page)
        self.assertIn('value="12"', page)
        self.assertIn('value="220"', page)
        self.assertNotIn("Nominal battery energy:", page)

    def test_duplicate_form_and_field_mismatch_errors_render_once(self):
        values = dict(PRIMARY_CASE, system_voltage="48")
        message = (
            "Battery configuration does not match the selected system voltage. "
            "Check the battery voltage, quantity, connection type, and system voltage."
        )
        duplicate_errors = {
            "_form": message,
            "system_voltage": message,
            "battery_quantity": message,
            "battery_voltage": message,
            "connection": message,
        }

        with patch.object(solar_app, "analyze_case", return_value=(duplicate_errors, None)):
            response = self.client.post("/", data=values)
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(page.count(message), 1)
        self.assertIn('value="48"', page)
        self.assertIn('value="2"', page)
        self.assertNotIn("Nominal battery energy:", page)


if __name__ == "__main__":
    unittest.main()
