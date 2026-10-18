from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task("Morning walk", "08:00")
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Breakfast", "08:00"))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Evening walk", "18:30"))
    assert len(pet.tasks) == 2


def _scheduler():
    owner = Owner("Jordan")
    mochi, luna = Pet("Mochi", "dog"), Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner, mochi, luna, Scheduler(owner)


def test_sort_by_time_orders_tasks_across_pets():
    _, mochi, luna, scheduler = _scheduler()
    mochi.add_task(Task("Evening walk", "18:30"))
    luna.add_task(Task("Breakfast", "08:00"))
    mochi.add_task(Task("Lunch", "12:15"))

    times = [t.due_time for t in scheduler.sort_by_time()]

    assert times == ["08:00", "12:15", "18:30"]


def test_filter_tasks_by_pet_and_status():
    _, mochi, luna, scheduler = _scheduler()
    walk, feed = Task("Walk", "08:00"), Task("Feed", "09:00")
    mochi.add_task(walk)
    luna.add_task(feed)
    walk.mark_complete()

    assert scheduler.filter_tasks(pet_name="luna") == [feed]
    assert scheduler.filter_tasks(is_complete=True) == [walk]
    assert scheduler.filter_tasks(pet_name="Mochi", is_complete=False) == []


def test_completing_daily_task_creates_next_day_occurrence():
    _, mochi, _, scheduler = _scheduler()
    walk = Task("Walk", "08:00", frequency="daily", due_date=date(2026, 1, 31))
    mochi.add_task(walk)

    new = scheduler.mark_task_complete(walk)

    assert walk.is_complete
    assert new.due_date == date(2026, 2, 1)
    assert not new.is_complete and new.pet_name == "Mochi"
    assert new in mochi.tasks


def test_completing_weekly_task_adds_seven_days_and_once_task_does_not_recur():
    _, mochi, _, scheduler = _scheduler()
    med = Task("Meds", "12:00", frequency="weekly", due_date=date(2026, 3, 1))
    once = Task("Vet", "10:00")
    mochi.add_task(med)
    mochi.add_task(once)

    assert scheduler.mark_task_complete(med).due_date == date(2026, 3, 8)
    assert scheduler.mark_task_complete(once) is None
    assert len(mochi.tasks) == 3


def test_conflict_detection_warns_for_same_slot_only():
    _, mochi, luna, scheduler = _scheduler()
    mochi.add_task(Task("Walk", "08:00"))
    luna.add_task(Task("Breakfast", "08:00"))
    luna.add_task(Task("Play", "09:00"))

    warnings = scheduler.get_conflict_warnings()

    assert len(warnings) == 1
    assert "08:00" in warnings[0] and "Mochi" in warnings[0] and "Luna" in warnings[0]


def test_conflict_ignores_other_dates_and_completed_tasks():
    _, mochi, luna, scheduler = _scheduler()
    mochi.add_task(Task("Walk", "08:00", due_date=date(2026, 1, 1)))
    luna.add_task(Task("Feed", "08:00", due_date=date(2026, 1, 2)))
    done = Task("Play", "08:00", due_date=date(2026, 1, 1))
    luna.add_task(done)
    done.mark_complete()

    assert scheduler.get_conflict_warnings() == []
