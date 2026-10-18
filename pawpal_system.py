from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Tuple


@dataclass
class Task:
    description: str
    due_time: str  # "HH:MM", 24-hour, so string order matches time order
    is_complete: bool = False
    frequency: str = "once"
    pet_name: str = ""  # set by Pet so a task knows which pet it belongs to

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True

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

    def sort_by_time(self) -> List[Task]:
        """Return all tasks across all pets sorted by due time."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.due_time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks belonging to the named pet (case-insensitive)."""
        wanted = pet_name.lower()
        return [t for t in self.owner.get_all_tasks() if t.pet_name.lower() == wanted]

    def check_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pairs of incomplete tasks scheduled at the same time, across all pets."""
        by_time = defaultdict(list)
        for task in self.owner.get_all_tasks():
            if not task.is_complete:
                by_time[task.due_time].append(task)
        return [
            pair
            for tasks in by_time.values()
            for pair in combinations(tasks, 2)
        ]
