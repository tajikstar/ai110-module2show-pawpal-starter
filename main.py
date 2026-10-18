from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(scheduler: Scheduler) -> None:
    print("=" * 46)
    print(f"Today's Schedule for {scheduler.owner.name}")
    print("=" * 46)
    print(f"{'Time':<7}{'Pet':<10}{'Task':<22}{'Status'}")
    print("-" * 46)
    for task in scheduler.sort_by_time():
        status = "done" if task.is_complete else "pending"
        print(f"{task.due_time:<7}{task.pet_name:<10}{task.description:<22}{status}")

    conflicts = scheduler.check_conflicts()
    print("-" * 46)
    if conflicts:
        for a, b in conflicts:
            print(f"Conflict at {a.due_time}: {a.pet_name} ({a.description}) "
                  f"and {b.pet_name} ({b.description})")
    else:
        print("No conflicts.")


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task("Morning walk", "08:00", frequency="daily"))
    mochi.add_task(Task("Evening walk", "18:30", frequency="daily"))
    luna.add_task(Task("Breakfast", "08:00", frequency="daily"))
    luna.add_task(Task("Medication", "12:15", frequency="weekly"))

    mochi.tasks[0].mark_complete()

    print_schedule(Scheduler(owner))


if __name__ == "__main__":
    main()
