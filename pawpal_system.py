from collections import defaultdict
from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from itertools import combinations
from typing import List, Optional, Tuple

# How far ahead a recurring task's next occurrence is scheduled.
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    description: str
    due_time: str  # "HH:MM", 24-hour, so string order matches time order
    is_complete: bool = False
    frequency: str = "once"  # "once", "daily" or "weekly"
    pet_name: str = ""  # set by Pet so a task knows which pet it belongs to
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete and return its next occurrence if it recurs, else None."""
        self.is_complete = True
        days = RECURRENCE_DAYS.get(self.frequency)
        if days is None:
            return None
        return replace(self, is_complete=False, due_date=self.due_date + timedelta(days=days))

    def update_time(self, new_time: str) -> None:
        """Change the task's due time."""
        self.due_time = new_time


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Stamp any tasks passed to the constructor with this pet's name."""
        for task in self.tasks:
            task.pet_name = self.name

    def add_task(self, task: Task) -> None:
        """Add a task to this pet and stamp it with this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return tasks that are not yet complete."""
        return [t for t in self.tasks if not t.is_complete]


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler that reads tasks from the given owner."""
        self.owner = owner

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks (default: all pets') ordered by date, then "HH:MM" time."""
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: (t.due_date, t.due_time))

    def filter_tasks(
        self, pet_name: Optional[str] = None, is_complete: Optional[bool] = None
    ) -> List[Task]:
        """Return tasks matching the given pet name (case-insensitive) and/or completion status.

        A filter left as None is ignored, so no arguments returns every task.
        """
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name.lower() == pet_name.lower()]
        if is_complete is not None:
            tasks = [t for t in tasks if t.is_complete == is_complete]
        return tasks

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to the named pet (case-insensitive)."""
        return self.filter_tasks(pet_name=pet_name)

    def check_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pairs of incomplete tasks sharing the same date and time, across all pets."""
        by_slot = defaultdict(list)
        for task in self.owner.get_all_tasks():
            if not task.is_complete:
                by_slot[(task.due_date, task.due_time)].append(task)
        return [pair for tasks in by_slot.values() for pair in combinations(tasks, 2)]

    def get_conflict_warnings(self) -> List[str]:
        """Return a human-readable warning for each conflict; an empty list means none."""
        warnings = []
        for a, b in self.check_conflicts():
            who = "for" if a.pet_name == b.pet_name else "between"
            names = a.pet_name if a.pet_name == b.pet_name else f"{a.pet_name} and {b.pet_name}"
            warnings.append(
                f"Conflict on {a.due_date} at {a.due_time} {who} {names}: "
                f"'{a.description}' and '{b.description}'"
            )
        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task and, if it recurs, add its next occurrence to the same pet.

        Returns the new task, or None if the task does not recur.
        """
        next_task = task.mark_complete()
        if next_task is not None:
            pet = next(p for p in self.owner.pets if task in p.tasks)
            pet.add_task(next_task)
        return next_task
