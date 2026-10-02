---
doc: checklist
status: approved
---

# Build Checklist

Build mode: learn

## Slices

- [x] **1. Run the primary shutdown-under-load analysis end to end**
  Becomes usable: A local Flask page accepts the primary 24V / two 12V 220Ah tubular batteries in Series / 3,500W inverter / 1,000W load case and shows validated calculations, deterministic explanation, the approved troubleshooting order, and safety guidance.
  Why now: The practical troubleshooting kernel is the proof of concept. Bootstrapping belongs inside this first usable path so we test the local app and real output together, not hidden setup by itself.
  PRD ref: `prd.md > The Core Journey`, `Enter system details and validate inputs`, `Calculate and interpret results`, `Use measurements and troubleshoot in order`, `Safety`.
  Spec ref: `spec.md > Stack`, `Where It Runs and How Someone Tries It`, `Flask page and request handling`, `Input validation and calculations`, `Deterministic explanation and troubleshooting`, `Technician form and results page`, `Tests`, `Data Model`, `File Structure`.
  Build: Bootstrap the new project-local Flask app and test structure; add the required primary-case form fields, server-side validation, Decimal-based series-bank calculations, nominal energy, estimated DC current before inverter losses, load/rating percentage, explanatory templates, fixed ordered checks, and safety guidance. Keep it local and deterministic; do not add an AI model, database, paid service, or touch the separate Gradio project.
  Verify (mechanical): Run `python -m unittest discover -s tests`. Tests must verify the exact primary-case calculations and labels, below-rating comparison, required-field rejection, approved check ordering and safety output, and successful Flask page submission.
  Learner check: Completed in browser. The learner tested the primary case and reported that a mismatch message appeared before submission; that feedback led to the initial-load validation fix and browser retest.
  Commit: `Build primary solar shutdown analysis` (`ede560c72b921a237418df7cd1a88b5c354e80d8`)

- [x] **2. Add field measurements and safe recovery from invalid cases**
  Becomes usable: Technicians can add optional real readings and notes; invalid, unsupported, or mismatched values get clear correction messages without losing entries or displaying false success.
  Why now: Once the primary result works, optional measurements and recovery behavior can be added against a known-good baseline without risking fabricated readings or the agreed demo flow.
  PRD ref: `prd.md > Enter system details and validate inputs`, `Use measurements and troubleshoot in order`, `Recover from errors and retain entries`, `States and Boundaries`.
  Spec ref: `spec.md > Input validation and calculations`, `Deterministic explanation and troubleshooting`, `Technician form and results page`, `Data Model`, `Important Failure Modes`.
  Build: Add optional battery type, field measurements, inverter alarm/code, and notes; distinguish them from calculated values; warn and exclude invalid optional measurements. Handle all specified missing, malformed, nonpositive, unsupported configuration, and bank/system voltage mismatch cases. Preserve the submitted form on correction/retry and add a clear/reset action. Keep troubleshooting order and safety rules fixed.
  Verify (mechanical): Run `python -m unittest discover -s tests`. Test missing and malformed fields, zero/negative and fractional battery count, series/parallel voltage matching, unsupported connection and voltage, invalid optional measurement warnings, preservation after errors, and clear/reset behavior through Flask's test client.
  Learner check: Completed in browser. The learner checked optional readings, invalid-measurement warnings, preserved values, and Clear/Reset behavior.
  Commit: `Add optional field measurements and observations` (`a29d8947a07f971db5ef065b5cfac3367a912ec3`); `Add clear reset action` (`e33ad219a046c646327a9128ccb765840214f8f7`)

- [x] **3. Make the local tool field-ready and document the demo**
  Becomes usable: The complete one-page tool is readable on laptop and phone, its result categories and safety notices are easy to distinguish, and the learner can run and test it using the project instructions.
  Why now: Visual refinement and run instructions are based on working, reviewed behavior, so styling can clarify real information rather than decorate an untested shell.
  PRD ref: `prd.md > Screens and Layout`, `Look and Feel`, `Safety`, `What We're Building`.
  Spec ref: `spec.md > Look and Feel`, `Technician form and results page`, `Where It Runs and How Someone Tries It`, `File Structure`.
  Build: Apply the agreed light, practical solar-engineering styling and responsive layout; ensure calculated values, real measurements, checks, and safety are distinct; add README instructions for Windows setup, local run, tests, and the exact demo. Keep assets local and avoid adding dependencies or services.
  Verify (mechanical): Run `python -m unittest discover -s tests`; start the server using the documented command; confirm the form and primary case render through Flask's test client and inspect the rendered page/CSS for the required result labels, safety section, and responsive layout rules.
  Learner check: Completed after Slice 3. The learner tested in a laptop browser and Chrome mobile preview: the form and results remained usable, the primary figures and distinction between calculations and field readings were clear, checks and safety were readable, and Clear/Reset returned a clean form. No blocking issue was reported.
  Commit: `Improve field-ready presentation and instructions` (`978590cf9832755265e2ea712f0a4d2400a21595`)

## Hands-on Checkpoints

- [x] Early usable behavior explored — completed after Slice 1. The learner browser-tested the primary case, reported the premature mismatch message, and retested the corrected initial-load/submission behavior.
- [x] Final kick-the-tires exploration and feedback completed — after Slice 3, the learner checked laptop and Chrome mobile-preview layouts, the primary case, calculation/measurement distinction, ordered checks, safety, and Clear/Reset. During hands-on browser testing, the learner also submitted a selected 48V system with two 12V batteries in Series; the app blocked analysis, preserved values, showed the mismatch message, and allowed correction/retry. No blocking issue was found.

## Final Review

- [x] Final review complete — no blocking issues reported; learner explicitly confirmed the proof of concept is ready for the Ship stage.

## Code Tour and App Map

- [x] Learning activity complete — guided source walkthrough completed in conversation.
- [x] Optional edit and transfer reflection addressed — no code edit was made, as requested; reflection was offered, and no answer was recorded.
- [x] `devpost/app-map.html` generated from finished code, checked offline, and shown, including a project-grounded practice to reuse.

Activity and evidence: The learner completed a guided source walkthrough in conversation, requesting step-by-step explanations of the POST form, Calculations, Measurements, Troubleshooting Checks, and Safety sections. The walkthrough connected the template to `app.py` `index()`, `analysis.py` `analyze_case()`, and `guidance.py` `guidance_for_case()`, `TROUBLESHOOTING_CHECKS`, and `SAFETY_GUIDANCE`. The learner also completed the laptop and Chrome mobile-preview browser review recorded above.
Route and stops: Walkthrough: `templates/index.html` POST form and five result sections; `app.py` `index()` receives and routes the submission; `solarmate/analysis.py` `analyze_case()` validates and calculates; `solarmate/guidance.py` supplies fixed checks and safety notes; the template renders those outputs. The learner requested the relevant parts one at a time and received each explanation. The walkthrough was in conversation, not a claim of separate editor navigation.
Edit outcome: No optional code edit was made, as requested; application behavior remains unchanged.
Reflection: Transfer question offered; the learner proceeded with the App Map request and no reflection answer was recorded.
Activity mode: Guided source walkthrough in conversation, plus learner-completed live browser review on laptop and Chrome mobile preview.

## Revisions
