from pawpal_system import Pet, Task


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
