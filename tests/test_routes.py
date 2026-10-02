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

    def test_malformed_optional_under_load_voltage_warns_and_preserves_primary_analysis(self):
        values = dict(PRIMARY_CASE, battery_bank_voltage_under_load="invalid-reading")

        response = self.client.post("/", data=values)
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('name="battery_bank_voltage_under_load"', page)
        self.assertIn('type="text" inputmode="decimal"', page)
        self.assertIn('value="invalid-reading"', page)
        self.assertIn(
            "Enter a finite number greater than 0 V for battery-bank voltage under load; "
            "this reading was not used.",
            page,
        )
        self.assertIn("Nominal battery energy: 5.28 kWh", page)
        self.assertIn("41.7 A", page)
        self.assertIn("28.6% of continuous rating", page)
        self.assertNotIn("invalid-reading V", page)

    def test_blank_optional_readings_and_observations_stay_absent(self):
        response = self.client.post("/", data=PRIMARY_CASE)
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("No valid real field measurements were provided", page)
        self.assertNotIn("role=\"status\"", page)
        self.assertNotIn("Technician-provided field measurement:", page)

    def test_clear_button_submits_empty_get_and_returns_clean_form(self):
        submitted_values = dict(
            PRIMARY_CASE,
            battery_bank_voltage_under_load="Infinity",
            battery_bank_voltage_at_rest="25.4",
            individual_battery_voltages_at_rest="12.7, 12.7",
            measured_actual_load_w="920",
            inverter_alarm_code="E01",
            field_notes="Private field note",
        )
        submitted_page = self.client.post("/", data=submitted_values).get_data(as_text=True)

        self.assertIn("role=\"status\"", submitted_page)
        self.assertIn("Nominal battery energy:", submitted_page)
        self.assertIn("Private field note", submitted_page)

        response = self.client.get("/")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<button type="submit" form="clear-case-form" class="button-secondary">Clear</button>',
            page,
        )
        self.assertIn('<form id="clear-case-form" action="/" method="get" hidden></form>', page)
        self.assertNotIn("role=\"alert\"", page)
        self.assertNotIn("role=\"status\"", page)
        self.assertNotIn("Nominal battery energy:", page)
        self.assertNotIn("Private field note", page)
        self.assertIn('name="field_notes" rows="3"></textarea>', page)
        self.assertIn('name="inverter_alarm_code" type="text"\n                 value="">', page)

    def test_valid_optional_readings_are_distinct_from_calculated_results(self):
        values = dict(
            PRIMARY_CASE,
            battery_bank_voltage_at_rest="25.4",
            battery_bank_voltage_under_load="23.8",
            individual_battery_voltages_at_rest="12.7, 12.7",
            individual_battery_voltages_under_load="11.9, 11.9",
            measured_actual_load_w="920",
            inverter_alarm_code="E01",
            field_notes="Voltage dips as the pump starts.",
        )

        response = self.client.post("/", data=values)
        page = response.get_data(as_text=True)
        measurements = page.split(
            '<section class="card" aria-labelledby="measurements-title">', 1
        )[1].split("</section>", 1)[0]

        self.assertEqual(response.status_code, 200)
        self.assertIn("Battery-bank voltage at rest", page)
        self.assertIn("25.4 V", page)
        self.assertIn("Battery-bank voltage under load", page)
        self.assertIn("23.8 V", page)
        self.assertIn("Individual battery voltages at rest", page)
        self.assertRegex(
            measurements,
            r"Individual battery voltages at rest \(technician-provided field measurement\):</strong>\s*12\.7,\s*12\.7\s*V",
        )
        self.assertIn("Individual battery voltages under load", page)
        self.assertRegex(
            measurements,
            r"Individual battery voltages under load \(technician-provided field measurement\):</strong>\s*11\.9,\s*11\.9\s*V",
        )
        self.assertIn("Measured actual load (technician-provided field measurement)", page)
        self.assertIn("920 W", page)
        self.assertIn("Inverter alarm / fault code (technician observation)", page)
        self.assertIn("E01", page)
        self.assertIn("Technician field notes (technician observation)", page)
        self.assertIn("Voltage dips as the pump starts.", page)
        self.assertIn("Estimated DC current before inverter losses:", page)
        self.assertIn("41.7 A", page)
        self.assertIn("28.6% of continuous rating", page)

    def test_invalid_optional_readings_warn_preserve_raw_values_and_are_excluded(self):
        values = dict(
            PRIMARY_CASE,
            battery_bank_voltage_at_rest="not-a-voltage",
            battery_bank_voltage_under_load="invalid-reading",
            individual_battery_voltages_at_rest="12.4, invalid",
            individual_battery_voltages_under_load="Infinity, 11.9",
            measured_actual_load_w="0",
        )

        response = self.client.post("/", data=values)
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        for raw_value in (
            "not-a-voltage",
            "invalid-reading",
            "12.4, invalid",
            "Infinity, 11.9",
            "value=\"0\"",
        ):
            self.assertIn(raw_value, page)
        self.assertIn(
            "Enter a finite number greater than 0 V for battery-bank voltage at rest; "
            "this reading was not used.",
            page,
        )
        self.assertIn(
            "Enter finite numbers greater than 0, separated by commas for individual battery voltages at rest; "
            "these readings were not used.",
            page,
        )
        self.assertIn(
            "Enter a finite number greater than 0 W for measured actual load; "
            "this reading was not used.",
            page,
        )
        self.assertNotIn("Technician-provided field measurement): 12.4", page)
        self.assertNotIn("Technician-provided field measurement): 23.8", page)
        self.assertIn("Nominal battery energy: 5.28 kWh", page)
        self.assertIn("41.7 A", page)
        self.assertIn("28.6% of continuous rating", page)


if __name__ == "__main__":
    unittest.main()
