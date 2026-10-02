---
doc: spec
status: approved
---

# SolarMate AI — Technical Spec

## How This Works, In Plain Language

SolarMate AI v1 is a small website that runs on your own computer. Flask is the lightweight Python web framework that shows the page and receives the form when you submit it. The browser sends the entered values to Python on your computer; Python checks them, performs the electrical calculations, and selects the agreed troubleshooting steps and safety notes. Flask then sends the same page back with either clear corrections or the completed analysis.

There is no AI model in v1. The explanatory text is assembled from predictable rules and templates using the calculated values and any real measurements entered. This keeps the demo free and usable without internet, an AI account, a key, or extra model software. A local language model can be reconsidered later, after checking the computer's specifications, but it is not part of this build.

The page uses HTML for its structure, CSS for the clean responsive appearance, and a small amount of JavaScript for simple browser interactions such as clearing the form. Python remains responsible for every important validation, calculation, troubleshooting decision, and safety rule. No database or cloud service is needed.

## The Core Journey Through the System

PRD ref: `prd.md > The Core Journey`.

1. The technician opens `http://127.0.0.1:5000`. Flask serves one page containing the title, safety notice, required inputs, and optional field measurements and notes.
2. They fill the form and submit it. The browser sends those values to the local Flask application; nothing is sent to a hosted AI provider.
3. Python validates required values, supported system voltage and battery connection, optional measurement formats, and whether the calculated bank voltage matches the selected system voltage.
4. If a required value is invalid or the arrangement is unsupported, Python returns the same page with field-specific messages and the entered values still filled in. No analysis is presented as successful.
5. If valid, Python calculates the bank configuration and energy, estimated DC current, and the load compared with the inverter rating. For the agreed demo, show **Nominal battery energy: 5.28kWh**; actual usable energy can be lower depending on battery condition, discharge limits, temperature, battery type, and other factors. Show **Estimated DC current before inverter losses: 41.7A** as a calculation from load ÷ system voltage, not as an actual battery-current measurement. The 1,000W load is about 28.6% of the 3,500W continuous inverter rating and is below that rating; the app must not present overload as the primary explanation.
6. Python combines the deterministic calculations with the approved ordered checks, any relevant user-provided measurements, and safety guidance. It uses fixed explanatory rules and text templates—not a language model.
7. Flask returns the page with distinct result sections. The technician can edit and resubmit the same case or clear it. No case is stored in a database or sent to a third party.

## Stack

- **Python 3.9 or newer** — runs the application and calculations. Flask's current stable documentation states support for Python 3.9+. Check the installed Python version at the start of the build.
- **Flask 3.1.x** — serves the local page and handles form submissions. Declare `Flask>=3.1,<4` in `requirements.txt`; this avoids silently jumping to a future major release. Flask's standard dependencies install with it.
- **HTML, CSS, and vanilla JavaScript** — build the single technician page without a front-end framework, build tool, or external assets.
- **Python standard library `unittest`** — test calculations, validation, troubleshooting selection, and Flask routes without adding a test dependency.

This is one small Python application and one web form. It uses the learner's Python familiarity and avoids framework, account, and deployment overhead. Flask's built-in development server is for local development and demo use only, not for production or public access.

Documentation:

- [Flask installation and Python support](https://flask.palletsprojects.com/en/stable/installation/)
- [Flask quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Python `unittest`](https://docs.python.org/3/library/unittest.html)

## Where It Runs and How Someone Tries It

**Runtime:** local Python process serving a browser page on this computer only. The app binds to `127.0.0.1`, not the public internet. It needs Python 3.9+ and Flask installed in this project's virtual environment. No API key, account, billing, database, or deployment is required. Internet access is needed to install Flask initially; after installation, the demo itself needs no internet connection.

From the project folder in Windows Command Prompt or PowerShell:

```text
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in a browser. To run the automated checks, open another terminal in the project folder, activate `.venv`, then run:

```text
python -m unittest discover -s tests
```

For the demo, enter the exact test case: 24V system; two batteries; 12V and 220Ah per battery; Series; tubular lead-acid; 3,500W inverter continuous rating; 1,000W approximate load; and “Inverter shuts down under load.” Show the 24V / 220Ah bank, **Nominal battery energy: 5.28kWh** (usable energy may be lower depending on battery condition, discharge limits, and other factors), **Estimated DC current before inverter losses: 41.7A** (a calculation, not a measured battery current), and the load at 28.6% of inverter continuous rating. Then show the approved ordered checks and safety guidance, emphasizing that the app suggests investigation rather than claiming a confirmed fault.

The required short demo video and public GitHub repository remain part of submission. Local operation is sufficient for recording; deployment is optional and has not been selected. The existing separate Python/Gradio SolarMate AI project must not be opened or modified as part of this build.

## Look and Feel

Carry forward `prd.md > Look and Feel`: practical solar engineering and simple assistance, with a light uncluttered page, deep green and solar yellow, and limited dark blue/charcoal contrast. Use readable system fonts, a clear form, and separate result sections for calculations, measurements, troubleshooting checks, and safety. Keep warnings noticeable but calm. Avoid gradients, excessive animation, decorative graphics, external font downloads, and generic AI-chat styling. CSS media queries should let the same page fit laptop and phone screens.

## Components

### Flask page and request handling

`app.py` creates the Flask app and handles the page request and form submission. On GET it renders the clean form. On POST it passes form values to the validation and analysis functions, then renders that same page with preserved inputs, errors, or results. It binds only to the local computer for the demo.

PRD ref: `prd.md > The Core Journey`, `Screens and Layout`, `Recover from errors and retain entries`.

### Input validation and calculations

`solarmate/analysis.py` contains ordinary Python functions with no network calls. It checks required numeric values and selections, accepts only 12V/24V/48V system voltage and Series/Parallel battery arrangements, validates positive values and whole-number battery count, and rejects a mismatch between selected voltage and calculated bank voltage. It calculates bank voltage/capacity, nominal Wh/kWh, estimated DC current before inverter losses, and load-to-inverter comparison as a percentage of continuous rating. Label demo values **Nominal battery energy** and **Estimated DC current before inverter losses**; the latter is a calculation, never a measured battery-current value. The demo shows 1,000W as about 28.6% of 3,500W and below rating. Use `Decimal` while parsing and calculating entered decimal values; round only for display so rounding does not hide a configuration mismatch.

Optional numeric field measurements are parsed separately. Blank values are absent, not zero. Invalid optional readings produce a warning and are excluded from interpretation; they do not silently become valid measurements.

PRD ref: `prd.md > Enter system details and validate inputs`, `Calculate and interpret results`.

### Deterministic explanation and troubleshooting

`solarmate/guidance.py` takes validated values and completed calculations and returns explanatory text, the ordered check list, and safety cautions. Its rules and templates explain nominal versus usable energy, estimated current and inverter losses, whether the input load is below or above the entered inverter rating, and how any provided measurements affect what to investigate. The seven approved troubleshooting checks remain in their agreed order. A 1,000W load against a 3,500W inverter is shown as below the continuous rating; do not describe inverter overload as the primary explanation. No branch may claim a confirmed fault or invent missing readings, codes, or test results.

This module has no generative AI in v1. It does not need Ollama, model downloads, an OpenAI key, another provider, or internet access.

PRD ref: `prd.md > Calculate and interpret results`, `Use measurements and troubleshoot in order`, `Safety`.

### Technician form and results page

`templates/index.html` presents the single-page form and conditional result sections. It includes a visible safety notice; supported voltage and connection selectors; required equipment and symptom fields; collapsible or clearly secondary optional measurements/notes; and an **Analyze System** submit action. Include an unsupported/other connection choice so a technician can receive the explicit unsupported-configuration message rather than being forced to misrepresent a Series-Parallel bank. Validation messages identify the affected fields. Keep values filled after invalid submissions, analysis errors, and successful analysis. A **Clear** action resets inputs and hides old results.

`static/css/styles.css` applies the responsive solar-engineering visual direction. `static/js/form.js` provides only small browser-side interactions such as clearing the displayed form/results; it must not replace server-side validation or calculation logic.

PRD ref: `prd.md > Screens and Layout`, `Enter system details and validate inputs`, `States and Boundaries`.

### Tests

`tests/test_analysis.py` checks battery-bank series/parallel math, the exact primary-case energy/current/load comparison, supported and unsupported configurations, invalid values, and deterministic ordered guidance. `tests/test_routes.py` uses Flask's test client to verify the form route, validation error preservation, successful result rendering, and clearing the form. The calculation and guidance tests run without an API, external service, or hardware.

PRD ref: `prd.md > Features and Behavior`, `States and Boundaries`, `What We're Building`.

## Data Model

There is no database and no long-term saved case. One form submission is represented as a Python dictionary with:

- Required user inputs: selected nominal system voltage; battery quantity, nominal volts per battery, Ah per battery, and connection; inverter continuous watts; approximate load watts; selected symptom.
- Optional user inputs: battery type; symptom notes; bank voltage at rest and under load; individual battery readings; measured actual load; inverter code/alarm.
- Derived analysis: calculated bank voltage and Ah, nominal energy, estimated DC current, load/rating comparison, explanatory text, ordered checks, safety notes, validation errors, and optional-field warnings.

The browser sends form values to the local Flask process. Validation converts and checks them; calculations and deterministic guidance are created from the validated values; Flask inserts those values and results into the returned HTML page. Entries remain visible through correction, analysis, and retry on the current page; the Clear action removes them. No case is written to disk, stored between browser sessions, or sent to a hosted service.

Calculated values, entered specifications, and optional real measurements must have distinct labels in the rendered page. A missing measurement stays missing; it is never represented as a calculated measurement.

## File Structure

```text
SolarMate-AI-Hackathon/
├── app.py                       # Flask app, local route, form orchestration
├── solarmate/
│   ├── __init__.py              # Package marker
│   ├── analysis.py              # Validation and deterministic calculations
│   └── guidance.py              # Explanation templates, ordered checks, safety rules
├── templates/
│   └── index.html               # Single form and results page
├── static/
│   ├── css/
│   │   └── styles.css           # Responsive solar-engineering presentation
│   └── js/
│       └── form.js              # Small optional UI interactions, no domain logic
├── tests/
│   ├── test_analysis.py         # Unit checks for validation, calculations, guidance
│   └── test_routes.py           # Local Flask request/response checks
├── devpost/
│   ├── learner-profile.md       # Personal learning context; keep ignored by Git
│   ├── scope.md                 # Approved project scope
│   ├── prd.md                   # Approved product requirements
│   └── spec.md                  # This technical blueprint
├── .gitignore                   # Ignore local environment and personal/secret files
├── README.md                    # Setup, local run, test, and demo instructions
└── requirements.txt             # Flask dependency only
```

Keep the project `.gitignore` rules that exclude `devpost/learner-profile.md`, `.venv/`, Python cache files, and `.env` / `.env.*` while allowing a secret-free `.env.example`. No real credentials are expected or needed in v1.

## External Services and Dependencies

There are no external runtime services. The only third-party Python package is Flask, installed from its normal package distribution using `requirements.txt`; its dependencies are installed automatically. Installation needs a network connection, but serving and demonstrating the completed app is local and does not call an external API. There are no API keys, usage limits, cloud costs, or model downloads.

Optional local generative AI is not a v1 dependency or build step. Reconsider it only as a future enhancement after checking the learner's computer specifications and deciding whether the extra software and model download are acceptable.

## Important Failure Modes

- **Invalid required input or mismatched bank/system voltage** → return the form with field-specific guidance and all entered values preserved; do not show success results.
- **Invalid optional measurement** → warn about the specific value and exclude it from interpretation; continue using otherwise valid inputs.
- **Unexpected calculation or route error** → show a clear retry message, preserve values where possible, and never present partial calculations or guidance as a successful analysis.
- **Flask not installed or local server not started** → the browser cannot load the page; README instructions explain virtual-environment setup and the local start command.

There is no hosted AI outage failure mode because v1 makes no AI request.

## What Was Simplified and Why

- Deterministic Python explanation templates instead of a hosted AI service or a local language model — guarantees a zero-cost demo, avoids sending field notes or system details off-device, avoids a billing/API-key dependency, and makes outputs straightforward to test. The tradeoff is less flexible wording.
- One Flask-rendered page instead of a separate front-end application — keeps the form, local calculations, errors, and results in one easy-to-follow path without a second development stack.
- No database or saved-case feature — a single local demo can prove the core workflow without persistence infrastructure.
- Fixed, reviewed troubleshooting and safety rules instead of generated diagnostic steps — preserves the learner-approved check order and avoids unsupported diagnosis or hazardous model output.

## Decisions and Open Issues

### Decisions

- **Learner choice:** Use Python and Flask for the new project with HTML/CSS/JavaScript for a simple technician interface. The learner has some Python experience and wants each part to remain understandable.
- **Learner choice:** Require a zero-cost local build and demo. No paid AI provider, API key, billing account, database, or paid hosting.
- **Learner choice:** Do not add a local model to v1. Revisit that only after checking the computer's hardware; deterministic explanation is the default.
- **Learner choice:** The precise demo inverter continuous rating is 3,500W. At 1,000W, the load is below that rating, so inverter overload is not the primary explanation.
- **Implementation detail derived from the PRD:** Keep validation, calculations, explanation rules, ordered troubleshooting checks, and safety guidance in ordinary testable Python. The browser only presents inputs and results.
- **Implementation detail derived from the local-only requirement:** Keep each case in the current form/request and returned page; do not add sessions, a database, or long-term storage.
- **Implementation detail derived from the small PoC:** Use Python's built-in `unittest` and Flask's test client instead of adding a separate test framework.

### Decisions and Open Issues

- **Local AI uncertainty resolved:** The learner does not yet know their computer's RAM/GPU. No local AI model will be included in v1; checking hardware is only necessary if a local model is considered later.
- **PRD open question:** Optional measurement validation wording and display can be finalized during implementation while preserving PRD behavior.
- **Environment check before build:** Confirm that a usable Python 3.9+ interpreter and the Windows `py` launcher are installed. This affects setup commands only; it does not change the agreed architecture.
- No other product, architecture, or external-service decision blocks this draft.
