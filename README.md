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

## Implementation summary

The logic layer lives in `pawpal_system.py` and has four classes:

- **`Task`** (dataclass): one care activity with a description, `"HH:MM"` due time, frequency, completion flag and the name of the pet it belongs to.
- **`Pet`** (dataclass): a pet's name, species and list of tasks. `add_task()` attaches a task and stamps it with the pet's name.
- **`Owner`** (dataclass): holds the list of pets. `get_all_tasks()` returns every pet's tasks in one list.
- **`Scheduler`**: takes an `Owner` and always reads tasks through `owner.get_all_tasks()`, so it works across all pets. It sorts tasks by time, filters by pet name, and reports tasks that share a time.

Data flows `Owner -> Pet -> Task`, and the `Scheduler` sits on top, reading from the `Owner`. `main.py` is a terminal demo, and `tests/test_pawpal.py` holds the first automated tests (`python -m pytest`).

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

## 🖥️ Sample Output

Output of `python main.py`, which builds an owner with two pets and prints a combined schedule:

```
==============================================
Today's Schedule for Jordan
==============================================
Time   Pet       Task                  Status
----------------------------------------------
08:00  Mochi     Morning walk          done
08:00  Luna      Breakfast             pending
12:15  Luna      Medication            pending
18:30  Mochi     Evening walk          pending
----------------------------------------------
No conflicts.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
