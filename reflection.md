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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
