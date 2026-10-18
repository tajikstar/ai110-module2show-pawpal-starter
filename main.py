from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, tasks: list) -> None:
    print(f"\n{title}")
    print("-" * 58)
    print(f"{'Date':<12}{'Time':<7}{'Pet':<9}{'Task':<20}{'Repeats':<8}{'Status'}")
    for t in tasks:
        status = "done" if t.is_complete else "pending"
        print(f"{t.due_date!s:<12}{t.due_time:<7}{t.pet_name:<9}{t.description:<20}"
              f"{t.frequency:<8}{status}")


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added deliberately out of order.
    mochi.add_task(Task("Evening walk", "18:30", frequency="daily"))
    luna.add_task(Task("Medication", "12:15", frequency="weekly"))
    mochi.add_task(Task("Morning walk", "08:00", frequency="daily"))
    luna.add_task(Task("Breakfast", "08:00"))  # same time as Mochi's walk
    luna.add_task(Task("Grooming", "08:00"))   # same time, same pet

    scheduler = Scheduler(owner)

    print_tasks("All tasks as added (unsorted)", owner.get_all_tasks())
    print_tasks("Sorted by time", scheduler.sort_by_time())
    print_tasks("Filter: Luna only", scheduler.filter_tasks(pet_name="Luna"))

    print("\nConflict warnings")
    print("-" * 58)
    for warning in scheduler.get_conflict_warnings() or ["No conflicts."]:
        print(warning)

    print("\nCompleting Mochi's daily morning walk and Luna's weekly medication...")
    for task in (mochi.tasks[1], luna.tasks[0]):
        new = scheduler.mark_task_complete(task)
        print(f"  {task.description}: next occurrence on {new.due_date}")

    print_tasks("Filter: pending only", scheduler.sort_by_time(scheduler.filter_tasks(is_complete=False)))
    print_tasks("Filter: completed only", scheduler.filter_tasks(is_complete=True))


if __name__ == "__main__":
    main()
