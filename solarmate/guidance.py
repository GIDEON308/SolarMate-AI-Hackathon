"""Fixed explanations, troubleshooting order, and safety guidance for v1."""

TROUBLESHOOTING_CHECKS = (
    "Confirm the connected load. Measure the actual AC load where possible, "
    "compare it with the inverter's continuous rating, and consider startup "
    "or surge demand.",
    "Measure and record the battery-bank voltage with no load.",
    "Measure and record the battery-bank voltage while the load is running. "
    "Compare it with the no-load reading; a significant drop can have several "
    "possible causes and does not confirm one by itself.",
    "For a series bank, measure each battery separately at rest and, where "
    "safely possible, under load. Compare the readings for differences.",
    "Using safe procedures, inspect terminals, cables, lugs, fuses or breakers, "
    "and connections for looseness, corrosion, overheating, or inadequate cable sizing.",
    "Record any inverter fault code, low-voltage alarm, or shutdown message. "
    "Check relevant cutoff and operating settings against the manufacturer's specifications.",
    "After correcting an identified issue, retest under load and record the "
    "new battery voltage and inverter behavior for comparison.",
)

SAFETY_GUIDANCE = (
    "Use appropriate PPE and safe electrical procedures. Avoid short circuits "
    "and follow the battery and inverter manufacturer's instructions.",
    "Do not perform measurements or interventions that exceed your training or "
    "safe working conditions; seek qualified technical assistance when risk is significant.",
    "These calculations and checks are advisory. Verify guidance with real "
    "measurements and the equipment specifications; this result does not confirm a fault.",
)


def guidance_for_case(result):
    """Explain calculated results and attach fixed checks without diagnosing a fault."""
    energy_explanation = (
        "Nominal battery energy is calculated from the entered bank voltage "
        "and capacity. Usable energy can be lower depending on battery type, "
        "condition, discharge limits, temperature, and operating conditions."
    )
    current_explanation = (
        "This is an estimate calculated as load divided by system voltage, "
        "not a measured battery current. Actual battery current can be higher "
        "because the inverter is not 100% efficient."
    )
    measurements_status = (
        "No real field measurements were provided. Measure actual values "
        "safely before drawing conclusions."
    )

    return {
        "energy_explanation": energy_explanation,
        "current_explanation": current_explanation,
        "measurements_status": measurements_status,
        "checks": TROUBLESHOOTING_CHECKS,
        "safety": SAFETY_GUIDANCE,
    }
