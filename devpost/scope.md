---
doc: scope
status: approved
---

# SolarMate AI

A small web-app proof of concept that helps a solar technician troubleshoot a system that shuts down or underperforms when a load is applied.

## The Unique Kernel
SolarMate AI is not a general chatbot: it uses practical system details and the under-load symptom to produce relevant calculations and a useful, safety-aware troubleshooting sequence. The learner will test whether the guidance makes sense using realistic solar scenarios from their installation and maintenance experience.

## Who It's For
A solar technician in the field investigating an inverter shutdown, low-voltage alarm, or battery voltage drop under load. Today, the information they need may be spread across manuals, experience, calculators, and other technical resources.

## The Core Loop
The technician enters system voltage, battery capacity and configuration, inverter rating, approximate load, and the symptom. SolarMate AI returns:
- Calculations and an explanation of what the numbers mean.
- Prioritized checks to perform first.
- Ordered troubleshooting steps.
- Safety cautions when measurements or work call for safe electrical procedures or qualified technical help.

## Inspiration & Identity
No specific visual reference or aesthetic direction established. The intended character is practical and grounded in real solar work, rather than a generic chatbot.

## Why This Matters to the Learner
The learner wants to make AI genuinely useful for real solar-work problems and combine it with their practical installation and maintenance experience. They also want to learn how to guide an AI coding agent from idea through planning, specification, testing, and improvement, and understand the finished prototype well enough to explain and demonstrate it.

## What "Working" Looks Like
The primary demo test case is a 24V system with two 12V 220Ah batteries, a 1,000W load, and an inverter that shuts down under load. The technician enters this scenario and receives sensible calculations, an explanation of the numbers, prioritized checks, an ordered troubleshooting sequence, and appropriate safety cautions. The proof is one useful workflow working from input to actionable output, not a claim that the AI can diagnose every solar fault.

## The POC Boundary
Build and demonstrate only the under-load shutdown/poor-performance troubleshooting workflow, from entering a small set of system details and symptoms to receiving calculations, interpretation, prioritized checks, and safety-aware next steps. Use realistic scenarios to test the guidance. The precise input handling and response behavior will be defined in the PRD.

## Later
No additional features are defined in this scope; it is limited to the single under-load troubleshooting proof of concept.

## Explicitly Cut
- Diagnosing every possible solar fault: it is beyond the proof of concept and would make the first experiment too broad.
- Modifying the learner's separate Python/Gradio SolarMate AI prototype: it is explicitly out of scope for this new hackathon project.
