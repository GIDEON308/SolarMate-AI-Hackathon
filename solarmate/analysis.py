from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


FORM_FIELDS = (
    "system_voltage",
    "battery_quantity",
    "battery_voltage",
    "battery_capacity_ah",
    "connection",
    "battery_type",
    "inverter_rating_w",
    "load_w",
    "symptom",
)

SUPPORTED_SYSTEM_VOLTAGES = {"12", "24", "48"}
SUPPORTED_CONNECTIONS = {"series", "parallel"}
SUPPORTED_SYMPTOMS = {
    "inverter_shutdown_under_load": "Inverter shuts down under load",
    "low_voltage_alarm": "Low-voltage alarm",
    "battery_voltage_drop": "Battery voltage drops significantly under load",
    "unexpected_shutdown": "Inverter switches off unexpectedly",
    "other": "Other",
}

def _parse_positive_decimal(raw_value, field, label, errors):
    if not raw_value:
        errors[field] = f"{label} is required."
        return None

    try:
        value = Decimal(raw_value)
    except (InvalidOperation, ValueError):
        errors[field] = "Enter a valid number."
        return None

    if not value.is_finite():
        errors[field] = "Enter a valid number."
        return None
    if value <= 0:
        errors[field] = f"{label} must be greater than 0."
        return None
    return value


def _display_decimal(value, places):
    quantum = Decimal(1).scaleb(-places)
    rounded = value.quantize(quantum, rounding=ROUND_HALF_UP)
    return f"{rounded:.{places}f}"


def analyze_case(values):
    errors = {}

    system_voltage_text = values.get("system_voltage", "")
    if not system_voltage_text:
        errors["system_voltage"] = "System voltage is required."
    elif system_voltage_text not in SUPPORTED_SYSTEM_VOLTAGES:
        errors["system_voltage"] = "Choose a supported system voltage: 12V, 24V, or 48V."

    connection = values.get("connection", "")
    if not connection:
        errors["connection"] = "Battery connection type is required."
    elif connection not in SUPPORTED_CONNECTIONS:
        errors["connection"] = (
            "This battery configuration is not supported in v1. "
            "Use Series or Parallel."
        )

    symptom = values.get("symptom", "")
    if not symptom:
        errors["symptom"] = "Choose a symptom."
    elif symptom not in SUPPORTED_SYMPTOMS:
        errors["symptom"] = "Choose a symptom from the list."

    quantity_text = values.get("battery_quantity", "")
    quantity = None
    if not quantity_text:
        errors["battery_quantity"] = "Battery quantity is required."
    else:
        try:
            quantity_decimal = Decimal(quantity_text)
            if not quantity_decimal.is_finite():
                raise InvalidOperation
            if quantity_decimal <= 0 or quantity_decimal != quantity_decimal.to_integral_value():
                errors["battery_quantity"] = "Battery quantity must be a positive whole number."
            else:
                quantity = int(quantity_decimal)
        except (InvalidOperation, ValueError):
            errors["battery_quantity"] = "Enter a valid whole number."

    battery_voltage = _parse_positive_decimal(
        values.get("battery_voltage", ""),
        "battery_voltage",
        "Battery voltage",
        errors,
    )
    battery_capacity = _parse_positive_decimal(
        values.get("battery_capacity_ah", ""),
        "battery_capacity_ah",
        "Battery capacity",
        errors,
    )
    inverter_rating = _parse_positive_decimal(
        values.get("inverter_rating_w", ""),
        "inverter_rating_w",
        "Inverter rating",
        errors,
    )
    load = _parse_positive_decimal(values.get("load_w", ""), "load_w", "Load", errors)

    if errors:
        return errors, None

    system_voltage = Decimal(system_voltage_text)
    if connection == "series":
        bank_voltage = battery_voltage * quantity
        bank_capacity = battery_capacity
    else:
        bank_voltage = battery_voltage
        bank_capacity = battery_capacity * quantity

    if bank_voltage != system_voltage:
        message = (
            "Battery configuration does not match the selected system voltage. "
            "Check the battery voltage, quantity, connection type, and system voltage."
        )
        errors["_form"] = message
        return errors, None

    energy_wh = bank_voltage * bank_capacity
    energy_kwh = energy_wh / Decimal(1000)
    estimated_current = load / system_voltage
    inverter_loading = load / inverter_rating * Decimal(100)
    load_below_rating = load < inverter_rating

    if load_below_rating:
        inverter_interpretation = (
            "The entered load is below the inverter's continuous rating. "
            "Continuous-rating overload is not indicated by these values; "
            "startup or surge demand still needs checking."
        )
    elif load == inverter_rating:
        inverter_interpretation = (
            "The entered load equals the inverter's continuous rating. "
            "Check the actual load and any startup or surge demand."
        )
    else:
        inverter_interpretation = (
            "The entered load exceeds the inverter's continuous rating. "
            "Verify the actual load and equipment specifications."
        )

    result = {
        "system_voltage": system_voltage,
        "battery_quantity": quantity,
        "battery_voltage": battery_voltage,
        "battery_capacity_ah": battery_capacity,
        "bank_voltage": bank_voltage,
        "bank_capacity_ah": bank_capacity,
        "nominal_energy_wh": energy_wh,
        "nominal_energy_kwh": energy_kwh,
        "nominal_energy_display": _display_decimal(energy_kwh, 2),
        "estimated_dc_current_before_losses_a": estimated_current,
        "estimated_dc_current_display": _display_decimal(estimated_current, 1),
        "inverter_rating_w": inverter_rating,
        "load_w": load,
        "inverter_loading_percent": inverter_loading,
        "inverter_loading_display": _display_decimal(inverter_loading, 1),
        "load_below_rating": load_below_rating,
        "inverter_interpretation": inverter_interpretation,
        "battery_type": values.get("battery_type", ""),
        "symptom": SUPPORTED_SYMPTOMS[symptom],
    }
    return {}, result
