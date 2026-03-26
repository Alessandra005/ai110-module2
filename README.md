# PawPal+ (Module 2 Project)
You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario
A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:
- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

- Enter basic owner and pet info
- Add tasks with duration, priority, scheduled time, and frequency
- Generate a daily schedule based on time budget and priority
- Display the plan sorted by priority then time, with plain-language reasoning
- Conflict detection warns when two tasks share the same time slot
- Recurring tasks (daily/weekly) auto-generate the next occurrence on completion
- Color-coded priority indicators (🔴 High, 🟡 Medium, 🟢 Low)

## Smarter Scheduling
PawPal+ now includes the following algorithmic features:
- **Sort by time**: Tasks are ordered chronologically by their scheduled time (HH:MM).
- **Filter tasks**: Filter by pet name or completion status.
- **Recurring tasks**: Daily and weekly tasks automatically generate a new instance when marked complete.
- **Conflict detection**: The scheduler warns when two tasks share the same time slot.

## Testing PawPal+
Run the full test suite with:
```bash
python -m pytest -v
```
Tests cover task completion, recurrence logic, priority sorting, time limit enforcement, conflict detection, and chronological ordering.

Confidence level: ☆☆☆☆

## 📸 Demo

<a href="/pawpal_screenshot.png" target="_blank">
  <img src="/pawpal_screenshot.png" title="PawPal App" width="" alt="PawPal App" class="center-block" />
</a>

<a href="/improved_pawpal_screenshot.png" target="_blank">
  <img src="/improved_pawpal_screenshot.png" title="PawPal App (improved UI)" width="" alt="PawPal App improved" class="center-block" />
</a>