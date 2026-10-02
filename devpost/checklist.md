---
doc: checklist
status: approved
---

# Build Checklist

Build mode: learn

## Slices

- [ ] **1. Run the primary shutdown-under-load analysis end to end**
  Becomes usable: A local Flask page accepts the primary 24V / two 12V 220Ah tubular batteries in Series / 3,500W inverter / 1,000W load case and shows validated calculations, deterministic explanation, the approved troubleshooting order, and safety guidance.
  Why now: The practical troubleshooting kernel is the proof of concept. Bootstrapping belongs inside this first usable path so we test the local app and real output together, not hidden setup by itself.
  PRD ref: `prd.md > The Core Journey`, `Enter system details and validate inputs`, `Calculate and interpret results`, `Use measurements and troubleshoot in order`, `Safety`.
  Spec ref: `spec.md > Stack`, `Where It Runs and How Someone Tries It`, `Flask page and request handling`, `Input validation and calculations`, `Deterministic explanation and troubleshooting`, `Technician form and results page`, `Tests`, `Data Model`, `File Structure`.
  Build: Bootstrap the new project-local Flask app and test structure; add the required primary-case form fields, server-side validation, Decimal-based series-bank calculations, nominal energy, estimated DC current before inverter losses, load/rating percentage, explanatory templates, fixed ordered checks, and safety guidance. Keep it local and deterministic; do not add an AI model, database, paid service, or touch the separate Gradio project.
  Verify (mechanical): Run `python -m unittest discover -s tests`. Tests must verify the exact primary-case calculations and labels, below-rating comparison, required-field rejection, approved check ordering and safety output, and successful Flask page submission.
  Learner check: Start the app, enter the exact demo values (including 3,500W inverter rating), and check that the results show 5.28kWh nominal energy, 41.7A estimated DC current before inverter losses, 28.6% of inverter rating, the ordered checks, and safety guidance. Tell me what is clear or what should be adjusted before we add optional readings.
  Commit: `Build primary solar shutdown analysis`

- [ ] **2. Add field measurements and safe recovery from invalid cases**
  Becomes usable: Technicians can add optional real readings and notes; invalid, unsupported, or mismatched values get clear correction messages without losing entries or displaying false success.
  Why now: Once the primary result works, optional measurements and recovery behavior can be added against a known-good baseline without risking fabricated readings or the agreed demo flow.
  PRD ref: `prd.md > Enter system details and validate inputs`, `Use measurements and troubleshoot in order`, `Recover from errors and retain entries`, `States and Boundaries`.
  Spec ref: `spec.md > Input validation and calculations`, `Deterministic explanation and troubleshooting`, `Technician form and results page`, `Data Model`, `Important Failure Modes`.
  Build: Add optional battery type, field measurements, inverter alarm/code, and notes; distinguish them from calculated values; warn and exclude invalid optional measurements. Handle all specified missing, malformed, nonpositive, unsupported configuration, and bank/system voltage mismatch cases. Preserve the submitted form on correction/retry and add a clear/reset action. Keep troubleshooting order and safety rules fixed.
  Verify (mechanical): Run `python -m unittest discover -s tests`. Test missing and malformed fields, zero/negative and fractional battery count, series/parallel voltage matching, unsupported connection and voltage, invalid optional measurement warnings, preservation after errors, and clear/reset behavior through Flask's test client.
  Learner check: Try one voltage/configuration mismatch and one optional measurement. Confirm the app preserves your inputs on the mismatch, and that an invalid optional reading is called out rather than treated as a real measurement.
  Commit: `Handle optional readings and input recovery`

- [ ] **3. Make the local tool field-ready and document the demo**
  Becomes usable: The complete one-page tool is readable on laptop and phone, its result categories and safety notices are easy to distinguish, and the learner can run and test it using the project instructions.
  Why now: Visual refinement and run instructions are based on working, reviewed behavior, so styling can clarify real information rather than decorate an untested shell.
  PRD ref: `prd.md > Screens and Layout`, `Look and Feel`, `Safety`, `What We're Building`.
  Spec ref: `spec.md > Look and Feel`, `Technician form and results page`, `Where It Runs and How Someone Tries It`, `File Structure`.
  Build: Apply the agreed light, practical solar-engineering styling and responsive layout; ensure calculated values, real measurements, checks, and safety are distinct; add README instructions for Windows setup, local run, tests, and the exact demo. Keep assets local and avoid adding dependencies or services.
  Verify (mechanical): Run `python -m unittest discover -s tests`; start the server using the documented command; confirm the form and primary case render through Flask's test client and inspect the rendered page/CSS for the required result labels, safety section, and responsive layout rules.
  Learner check: Open the app on your computer at laptop size and, if convenient, a phone-sized browser width. Submit the primary demo case and try the README instructions; tell me what is confusing, broken, or worth refining.
  Commit: `Polish responsive app and document local demo`

## Hands-on Checkpoints

- [ ] Early usable behavior explored — after Slice 1, try the complete primary demo and share feedback that can shape optional readings and presentation in later slices.
- [ ] Final kick-the-tires exploration and feedback completed — after Slice 3, explore the completed app, including the primary case and an awkward input.

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: [what actually happened; real document/test/code references; unfinished work if interrupted]
Route and stops: [actual paths and symbols; guided stops completed, or reference-only route]
Edit outcome: [tried/kept/reverted/declined/not applicable; verification if changed]
Reflection: [offered/answered/declined/already covered — personal answer belongs only in the ignored profile]
Activity mode: [live app and editor, explicit static fallback, focused alternative, prior practice, or recap]

## Revisions
