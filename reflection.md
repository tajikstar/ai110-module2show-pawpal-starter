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

I did not act on these yet: tasks have no duration, so only exact same-time clashes will count as conflicts, and `frequency` is just a string with no logic for creating the next occurrence of a recurring task. Both are worth revisiting during implementation.

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
- **Held back:** the review also suggested task durations and real recurrence logic for `frequency`. I did not add these yet, since they go beyond the core requirements and would grow the design before the basics were verified.
- **Changed:** `check_conflicts` ignores completed tasks, a choice the AI made on its own. I kept it, but I checked that it behaves the way I want.
- **Verification:** I ran `main.py` with two pets and compared the printed schedule to what I expected (sorted order, per-pet filtering, one conflict found, then none after marking a task done). I also added pytest tests for `mark_complete()` and `Pet.add_task()` and confirmed they pass.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
