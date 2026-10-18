# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML has four classes:

- **Task** (dataclass): one care activity, with a description, due time, completion flag and frequency. It knows how to mark itself complete and change its time.
- **Pet** (dataclass): a pet's name and species plus its list of tasks. It adds tasks and reports which ones are still pending.
- **Owner** (dataclass): the owner's name and list of pets. It adds pets and gathers every task across all pets.
- **Scheduler**: holds an Owner and does the "thinking": sorting tasks by time, filtering by pet name, and detecting conflicts. I kept this logic out of the data classes so they stay simple.

Relationships: an Owner has many Pets, a Pet has many Tasks, and the Scheduler manages one Owner.

**b. Design changes**

I asked my AI assistant to review the skeleton for missing relationships and bottlenecks. It raised these points:

- **Tasks didn't know their pet.** `Owner.get_all_tasks()` flattens tasks, so `Scheduler.filter_by_pet()` and conflict reports couldn't tell which pet a task belonged to. *Change:* I added a `pet_name` field to `Task`, which `Pet.add_task()` will fill in.
- **Time format.** `due_time` is a string, so sorting only works if it's always "HH:MM". I documented that format in `sort_by_time`. I'm keeping strings for now and may switch to `datetime.time` later.
- **Conflict checking could be O(n^2).** I noted in the docstring that `check_conflicts` should group tasks by `due_time` instead of comparing every pair.

I did not act on two points right away: tasks have no duration, so only exact same-time clashes count as conflicts, and `frequency` was just a string.

Later changes while building the smarter scheduler (the final UML is `diagrams/uml_final.mmd`):

- **Recurrence needed a date.** Adding `due_date` to `Task` let `mark_complete()` return the next occurrence using `timedelta`. `Scheduler.mark_task_complete()` then adds it to the owning pet. Sorting and conflict detection now use `(due_date, due_time)`, so the same time on different days is not a conflict.
- **Filtering and warnings.** `filter_tasks(pet_name, is_complete)` replaced one-off filters, and `get_conflict_warnings()` turns conflict pairs into readable messages for the UI.
- **Safer completion.** Writing edge-case tests showed that completing a task that belongs to no pet crashed with `StopIteration`, and completing a task twice created duplicate next occurrences. I fixed both in `mark_task_complete()`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers a task's date and time, its completion status, which pet it belongs to, and how often it repeats. Time matters most, because a pet owner's day is organized around when things happen, so sorting and conflict detection are built on it. I left out priority and duration to keep the first version small.

**b. Tradeoffs**

The conflict check only compares exact date and time matches, not overlapping durations. A 30-minute walk at 08:00 and a feeding at 08:15 would not be flagged. This is reasonable for now because tasks have no duration field, and exact matching is one pass over the tasks (grouping them in a dictionary), easy to read and easy to test. It still catches the most obvious double-booking, and it returns warnings instead of raising errors, so the app keeps running. Overlap detection would need a `duration_minutes` field and an interval comparison.

I also reviewed `check_conflicts()` for readability. I kept the explicit loop that builds a dictionary of slots and then pairs up the tasks in each slot, because it is easier to follow than a single dense comprehension. I only simplified the final pairing step with `itertools.combinations`.

---

## 3. AI Collaboration

**a. How you used AI**

I used an AI coding assistant to turn my UML into dataclass skeletons, review the skeleton for gaps, implement the four classes, write the `main.py` demo and draft the first tests. The most helpful prompts were specific ones, such as asking whether the skeleton had missing relationships or bottlenecks, and requiring that the Scheduler read from the Owner instead of a single pet.

**b. Judgment and verification**

- **Accepted:** adding a `pet_name` field to `Task` after the review pointed out that a flattened task list loses track of which pet owns each task. I also accepted grouping tasks by time in `check_conflicts` instead of comparing every pair.
- **Held back / modified:** the review also suggested task durations and recurrence logic. I added recurrence later, but still left out durations, since overlap detection would grow the design beyond what the app needs. For recurrence I also kept the date logic inside `Task` (it returns the next task) and put the "add it to the pet" step in `Scheduler`, so `Task` doesn't need to know about its pet's list.
- **Changed:** `check_conflicts` ignores completed tasks, a choice the AI made on its own. I kept it, but I checked that it behaves the way I want.
- **AI strategy, most effective features:** editing several files in one pass (logic, `main.py`, `app.py`, tests and docs together) kept them consistent, and running the code and tests right after each change caught problems quickly. Asking targeted review questions, such as "what relationships or bottlenecks are missing?", worked better than asking for "improvements".
- **Separate chat sessions:** I worked in one continuous session instead of a new chat per phase, so I can't claim the organizational benefit. What kept the work organized was following the phases in order and committing at the end of each one.
- **Verification:** I ran `main.py` with two pets and compared the printed schedule to what I expected (sorted order, per-pet filtering, one conflict found, then none after marking a task done). I also added pytest tests for `mark_complete()` and `Pet.add_task()` and confirmed they pass.

---

## 4. Testing and Verification

**a. What you tested**

I wrote 17 tests covering sorting (across pets, date before time, ties), filtering, recurrence (daily, weekly, month and year rollover, "once" tasks), conflict detection (same pet, different pets, three-way, different dates, completed tasks), and edge cases (no pets, no tasks, completing an unowned or already-completed task). These matter because the scheduler's value is in being correct about order, repeats and clashes, and those are easy to break silently when the code changes.

**b. Confidence**

About 4 out of 5. All tests pass and the Streamlit app worked when I tried it by hand. The gaps are that the UI has no automated tests, tasks have no duration so overlapping (not identical) times are missed, and `due_time` is not validated. Next I would test malformed times, very large numbers of tasks, and duplicate pet names entered with different capitalization.

---

## 5. Reflection

**a. What went well**

I'm most satisfied that the `Scheduler` always works through `Owner.get_all_tasks()`, so every feature works across all pets with no special cases, and that the same methods power both the CLI demo and the Streamlit app.

**b. What you would improve**

I would add task duration and priority, so conflicts can be overlapping time windows and a daily plan can choose tasks when time runs out. I would also validate times with `datetime.time` instead of `"HH:MM"` strings, and add automated UI tests.

**c. Key takeaway**

AI can write working code quickly, but it doesn't decide what the system should be. Design choices such as where recurrence logic lives, what counts as a conflict, and what to leave out stayed with me, and tests were how I checked the AI's code instead of trusting it. Being the "lead architect" meant setting the structure first (the UML), then reviewing each change against it.
