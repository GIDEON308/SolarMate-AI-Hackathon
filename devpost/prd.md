---
doc: prd
status: approved
---

# SolarMate AI — Product Requirements

A practical solar troubleshooting web app that helps a field technician investigate inverter shutdown or poor performance under load.
Source: `scope.md > Who It's For`, `The Unique Kernel`.

## The Core Journey

1. The technician opens SolarMate AI and sees a focused troubleshooting form, a short explanation of its purpose, and a visible safety notice.
2. They enter the required system, battery, inverter, load, and symptom details. They may also enter battery type, field measurements, an inverter alarm/code, and symptom notes.
3. The app validates required values and checks that the calculated battery-bank voltage agrees with the selected supported system voltage. If something is invalid or unsupported, it explains what needs attention and preserves the entered values.
4. Once valid, the technician selects **Analyze System** (or **Troubleshoot**) and sees calculated values clearly distinguished from real field measurements, an interpretation, prioritized checks, ordered troubleshooting steps, and safety cautions.
5. The technician follows the guidance using actual equipment measurements and manufacturer information. The app does not claim a confirmed diagnosis without evidence.

Source: `scope.md > The Core Loop`, `What "Working" Looks Like`, `The POC Boundary`.

## Screens and Layout

One simple, responsive troubleshooting surface; no dashboard or multi-feature navigation.

- A clear **SolarMate AI** title and short description: “Troubleshoot solar system shutdowns and poor performance under load.”
- A concise safety notice reminding users to follow safe electrical procedures and verify AI guidance with actual measurements and equipment specifications.
- A **System Details** form with required system, battery, inverter, load, and symptom inputs, followed by optional field measurements and notes.
- After successful analysis, clearly separated sections/cards for **Calculations**, **Measurements**, **Troubleshooting Checks**, and **Safety**. Results should be readable on a laptop and reasonably usable on a phone.
- Keep the technician on the same troubleshooting surface when correcting errors or retrying analysis; preserve their entered information.

Source: `scope.md > The Core Loop`, `The POC Boundary`.

## Look and Feel

Practical solar engineering and simple AI assistance—not a generic chatbot or futuristic dashboard. Use a clean, modern, professional layout with a mostly light, uncluttered background; solar-inspired deep green and solar yellow; and a small amount of dark blue or charcoal for contrast. Use clear sections/cards and simple, helpful icons where appropriate. Make warnings distinct but not alarming. Avoid excessive animation, gradients, and decorative graphics. Prioritize clarity and usability over visual effects.

## Features and Behavior

### Enter system details and validate inputs

The technician supplies these required values:

- **System voltage:** select 12V, 24V, or 48V.
- **Battery quantity:** positive whole number.
- **Battery nominal voltage per battery:** positive number.
- **Battery capacity per battery:** positive Ah value.
- **Battery connection:** Series or Parallel only.
- **Inverter continuous rating:** positive watts.
- **Approximate load:** positive watts.
- **Primary symptom:** select one of:
  - Inverter shuts down under load
  - Low-voltage alarm
  - Battery voltage drops significantly under load
  - Inverter switches off unexpectedly
  - Other

Optional fields:

- Battery type: tubular lead-acid, AGM, gel, lithium, or other.
- Symptom description / field notes.
- Battery-bank voltage at rest and under load.
- Individual battery voltage measurements, at rest and, where safely possible, under load.
- Measured actual load.
- Inverter fault code or alarm message.

Validation behavior:

- Do not analyze until all required fields are present and valid. Keep the user on the form, highlight invalid fields, and explain how to correct them.
- Show a clear field-specific message for missing values (for example, “Battery capacity is required.”) and non-numeric values (“Enter a valid number.”).
- Reject zero or negative battery capacity, inverter rating, or load with a specific greater-than-zero message. Battery quantity must be a positive whole number; battery voltage must be positive.
- System voltage must be selected from 12V, 24V, or 48V, and battery connection and symptom must be selected.
- Calculate the battery-bank voltage before analysis: Series uses individual battery voltage × quantity; Parallel uses the individual battery voltage. The calculated bank voltage must match the selected system voltage. If not, block analysis, identify the relevant values, preserve entries, and explain: “Battery configuration does not match the selected system voltage. Check the battery voltage, quantity, connection type, and system voltage.” Do not automatically change a selection or guess which value is correct.
- Only Series and Parallel are supported. Do not calculate Series-Parallel or another unsupported arrangement; clearly identify it as unsupported and ask the technician to use a supported configuration.
- Blank optional fields do not block analysis. If an optional numeric measurement is invalid, show a warning and exclude that value from the analysis until corrected. Optional text may remain blank.

**Acceptance criteria**

- The primary demo values (24V system, quantity 2, 12V and 220Ah per battery, Series, 1,000W load, and the under-load shutdown symptom) pass validation.
- Two 12V batteries in Series calculate to a 24V bank; two 12V batteries in Parallel calculate to a 12V bank. The Ah capacity follows the selected connection rule described under **Calculate and interpret results**.
- A mismatched bank voltage blocks analysis, preserves values, and identifies the voltage/configuration mismatch.
- Missing, malformed, zero/negative, and unsupported inputs show an actionable message and do not produce partial results as if analysis succeeded.

Source: `scope.md > The Core Loop`, `What "Working" Looks Like`, `The POC Boundary`.

### Calculate and interpret results

After required inputs pass validation, show practical nominal calculations:

- **Battery-bank voltage and capacity:** Series increases voltage by battery quantity and keeps the per-battery Ah capacity; Parallel keeps voltage the same and multiplies Ah capacity by battery quantity. These calculations assume identical batteries.
- **Nominal battery energy:** bank voltage × bank Ah, displayed in Wh and kWh. For the demo: 24V × 220Ah = 5,280Wh (5.28kWh).
- **Estimated DC current:** approximate load ÷ system voltage, before inverter losses. For the demo: 1,000W ÷ 24V ≈ 41.7A. Explain that actual battery current can be higher because the inverter is not 100% efficient.
- **Load compared with inverter rating:** compare approximate load with the inverter's continuous rating so the technician can see whether it is near or above that rating. Mention possible startup/surge demand as a check; do not infer a surge value.

Explain that nominal energy is not actual usable energy; usable energy depends on battery type, condition, discharge limits, temperature, and operating conditions. Explain that calculated values are estimates based on entered specifications, not field measurements or confirmation of equipment condition.

Interpret high current demand and possible voltage drop as reasons to investigate a weak, discharged, undersized, or high-resistance battery system, poor connections, or excessive current demand—not as a definitive diagnosis. Where real measurements are absent, say that actual measurements are needed to confirm the cause. Never create missing measurements, fault codes, or diagnostic results.

**Acceptance criteria**

- For the primary demo, results show 24V, 220Ah, 5,280Wh / 5.28kWh nominal energy, approximately 41.7A before inverter losses, and a comparison of the 1,000W load against the 3,500W continuous inverter rating.
- The primary demo works end-to-end using a 24V system with two 12V 220Ah tubular batteries in series, a 3,500W continuous inverter rating, a 1,000W load, and an inverter shutdown-under-load symptom. The app correctly calculates the battery-bank configuration and nominal energy, estimates DC current before inverter losses, shows that the load is below the inverter's continuous rating without presenting overload as the primary explanation, and produces the approved ordered troubleshooting checks with safety guidance.
- Every calculated value is labeled as calculated/estimated; user-entered specifications and real field measurements are visually distinguishable.
- Results explain assumptions and limitations, and describe possible causes as checks to investigate rather than confirmed faults.

Source: `scope.md > The Unique Kernel`, `The Core Loop`, `What "Working" Looks Like`.

### Use measurements and troubleshoot in order

Optional real measurements and inverter fault/alarm information may refine the interpretation and troubleshooting sequence. Label these as technician-provided field information, not calculated values. Never fill in absent measurements or codes. Identify when measurements are missing and direct the technician to obtain appropriate real readings safely.

For the primary 24V / two 12V 220Ah tubular batteries in Series / 3,500W continuous inverter / 1,000W load / inverter-shutdown case, present these checks in order:

1. Confirm the actual load; measure AC load where possible, check it against inverter continuous rating, and consider startup/surge demand.
2. Measure and record battery-bank voltage with no load.
3. Measure and record battery-bank voltage while the load is running; compare it with the no-load reading. Explain that a significant drop can have several possible causes, not a single confirmed diagnosis.
4. Measure each 12V battery separately at rest and, where safely possible, under load; look for differences between the batteries.
5. Safely inspect terminals, cables, lugs, fuses/breakers, and connections for looseness, corrosion, overheating, or inadequate cable sizing.
6. Record the inverter fault code, low-voltage alarm, or shutdown message if available; check relevant low-voltage cutoff and operating settings against manufacturer specifications.
7. After correcting an identified issue, retest under load and record the new battery voltage and inverter behavior for comparison.

**Acceptance criteria**

- The primary case presents the checks in the specified order, distinguishes calculated values from field measurements, and does not claim a fault is confirmed without relevant evidence.
- If optional measurements or an inverter code are absent, the app says so and does not invent them. If supplied, the app may use them to tailor interpretation and checks.

Source: `scope.md > The Core Loop`, `What "Working" Looks Like`, `The POC Boundary`.

### Safety

Keep safety cautions visible throughout the troubleshooting experience. Remind technicians to use appropriate PPE and safe electrical procedures, avoid short circuits, and follow battery and inverter manufacturer instructions. Do not give unsafe step-by-step directions for risky measurements or interventions; recommend qualified technical assistance when risk is significant. Guidance is advisory and must be verified against actual measurements and equipment specifications.

**Acceptance criteria**

- Safety advice is visible before and during troubleshooting, including with the primary demo case.
- Risky work is directed to safe procedures and qualified help rather than unsafe procedural instructions.

Source: `scope.md > The Core Loop`, `What "Working" Looks Like`.

### Recover from errors and retain entries

If analysis cannot complete, show a clear, non-technical message such as “Analysis could not be completed. Please check your inputs and try again.” Identify the specific issue where possible. Keep all entered values available so the technician can correct the problem and retry without re-entering the form. Do not present incomplete calculations or troubleshooting advice as successful results. An unsupported configuration should be identified specifically. Entered information remains available until the technician chooses to clear or reset it.

**Acceptance criteria**

- A failed analysis leaves the current entries intact and provides a retry path.
- An error does not display incomplete results as valid guidance; specific known input/configuration problems are identified.

Source: `scope.md > The Core Loop`, `The POC Boundary`.

## States and Boundaries

- **First use / ready:** show the purpose, safety notice, required form, and optional measurements/notes; no dashboard or extra features.
- **Validation error:** remain on the form, highlight relevant fields, explain corrections, and preserve all entries.
- **Successful analysis:** show the calculations and interpretation, real measurements (if provided), ordered checks, and safety cautions in distinct sections.
- **Analysis failure:** preserve entries, explain the failure where possible, and permit retry; do not show partial results as success.
- **Unsupported voltage/configuration:** block analysis, explain what is unsupported or mismatched, and preserve entries.
- **Information and diagnosis boundary:** calculations are nominal estimates from entered specifications; real measurements are user-provided. The app suggests checks and possible causes but does not confirm a diagnosis.
- **Persistence:** entered information remains available on the current troubleshooting surface until the technician chooses to clear or reset it. No account, cross-session history, or saved-case behavior is defined for this POC.

## Product Decisions

- Keep the first release to one under-load shutdown/poor-performance workflow for solar technicians, rather than a general diagnostic assistant.
- Accept only 12V, 24V, and 48V nominal system voltages and Series or Parallel battery configurations, keeping the first version predictable.
- Require the core system and equipment specifications; keep battery type, field measurements, inverter code, and symptom notes optional so analysis can proceed without fabricated data.
- Validate battery-bank voltage against the selected system voltage; block mismatches rather than guessing or silently changing technician inputs.
- Present calculations, field measurements, prioritized checks, ordered troubleshooting steps, and safety cautions as distinct kinds of information.
- Use the 24V / two 12V 220Ah Series batteries / 1,000W under-load shutdown scenario as the primary demo and test case.
- Keep the interface simple, professional, solar-inspired, responsive, and focused on field usability.

## What We're Building

- One focused, responsive troubleshooting surface for inverter shutdown or poor performance under load.
- Required input validation, supported voltage/configuration checks, nominal battery-bank calculations, estimated DC current, and load-to-inverter comparison.
- Optional real measurement, battery-type, alarm/code, and symptom-note inputs that may refine the interpretation.
- Clearly differentiated calculated values, user-entered specifications, and real field measurements.
- An ordered, safety-conscious troubleshooting sequence, recoverable errors, and the primary demo case.

## Deferred From the POC

- Series-Parallel battery calculations: explicitly unsupported in v1 because they add complexity beyond the proof of concept.
- Other system voltages and unsupported battery arrangements: outside the deliberately bounded supported set.
- Broader solar fault diagnosis or a general solar technician/learner assistant: outside the single under-load troubleshooting workflow.
- Accounts, saved cases, and cross-session case history: not needed to demonstrate the workflow.

## Possible Later Enhancements

Additional supported battery arrangements or system voltages and troubleshooting workflows for other solar faults could be considered later, after validating this focused workflow. They are not v1 requirements.

## Non-Goals

- Confirming a fault or replacing technician judgment: the app provides estimates and possible checks; technicians verify with real measurements and equipment documentation.
- Inventing missing readings, fault codes, or test outcomes: absent data must remain explicitly absent.
- Giving unsafe instructions for hazardous electrical work: significant-risk interventions require safe procedures and qualified assistance.
- Modifying the learner's separate existing Python/Gradio SolarMate AI project: that project is explicitly out of scope.
- Adding IoT sensors, offline LLM functionality, quotation generation, or unrelated future features: these are not part of the approved hackathon scope.

## Open Questions

- None blocking PRD review. The exact presentation and validation wording for optional measurement fields can be finalized in the specification/build while preserving the behavior defined here.
