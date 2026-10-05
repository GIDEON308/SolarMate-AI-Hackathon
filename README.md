# SolarMate AI

A small local web app for checking a solar system that shuts down or performs
poorly under load. It provides deterministic calculations and an ordered,
safety-conscious set of checks; it does not confirm a fault.

## Run locally on Windows

From this project folder, open Command Prompt or PowerShell and create the
virtual environment:

```text
py -3 -m venv .venv
```

Activate it using the command for your terminal:

```text
PowerShell:       .\.venv\Scripts\Activate.ps1
Command Prompt:   .venv\Scripts\activate.bat
```

Then install the dependency and start the app:

```text
python -m pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser. Stop the local server with
**Ctrl+C** in the terminal.

The app runs locally and does not require an AI model, API key, paid service,
database, or hosting. Internet access is needed only to install Flask the first
time; the running demo makes no external service calls.

## Run the tests

With the virtual environment active, run:

```text
python -m unittest discover -s tests
```

## Try the primary demo

Enter these system details:

- System voltage: **24V**
- Batteries: **2**, each **12V**, **220Ah**
- Connection: **Series**
- Battery type: **Tubular lead-acid**
- Inverter continuous rating: **3500W**
- Approximate load: **1000W**
- Symptom: **Inverter shuts down under load**

The calculated results should show a **24V / 220Ah** bank, **5.28kWh nominal
battery energy**, **41.7A estimated DC current before inverter losses**, and
**28.6% inverter loading**. These are calculations, not field measurements.
Use the ordered troubleshooting checks and verify with safe real measurements
and manufacturer specifications.

When valid field readings are supplied, the results also include an
**Evidence-Based Findings** section comparing bank voltage at rest and under
load, differences between individual battery readings, and the entered load
against the inverter's continuous rating. Voltage differences may suggest an
imbalance or connection issue, but do not by themselves confirm battery failure.
