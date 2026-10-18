import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Streamlit reruns this script on every interaction, so the Owner lives in
# session_state and is only created the first time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner: Owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        elif any(p.name.lower() == pet_name.strip().lower() for p in owner.pets):
            st.error(f"You already have a pet named {pet_name.strip()}.")
        else:
            owner.add_pet(Pet(pet_name.strip(), species))
            st.success(f"Added {pet_name.strip()}!")

if owner.pets:
    st.write("Your pets:", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        target = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task description", placeholder="Morning walk")
        due = st.time_input("Due time")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            if not description.strip():
                st.error("Please enter a task description.")
            else:
                pet = next(p for p in owner.pets if p.name == target)
                pet.add_task(Task(description.strip(), due.strftime("%H:%M"), frequency=frequency))
                st.success(f"Added '{description.strip()}' for {target}.")
else:
    st.info("Add a pet first, then you can schedule tasks for it.")

st.divider()

st.subheader("Today's Schedule")
scheduler = Scheduler(owner)
all_tasks = owner.get_all_tasks()

if all_tasks:
    pending = len(scheduler.filter_tasks(is_complete=False))
    m1, m2, m3 = st.columns(3)
    m1.metric("Pets", len(owner.pets))
    m2.metric("Pending tasks", pending)
    m3.metric("Completed", len(all_tasks) - pending)

    # Conflicts come first: they are the thing the owner needs to act on.
    warnings = scheduler.get_conflict_warnings()
    if warnings:
        st.warning(f"{len(warnings)} scheduling conflict(s) found. Move one task in each pair to a different time.")
        for warning in warnings:
            st.warning(warning, icon="⚠️")
    else:
        st.success("No scheduling conflicts. You're all set!")

    f1, f2 = st.columns(2)
    pet_choice = f1.selectbox("Show tasks for", ["All pets"] + [p.name for p in owner.pets])
    status_choice = f2.selectbox("Status", ["All", "Pending", "Completed"])
    shown = scheduler.filter_tasks(
        pet_name=None if pet_choice == "All pets" else pet_choice,
        is_complete={"All": None, "Pending": False, "Completed": True}[status_choice],
    )
    shown = scheduler.sort_by_time(shown)

    if not shown:
        st.info("No tasks match these filters.")
    for task in shown:
        cols = st.columns([2, 2, 3, 2])
        cols[0].write(f"{task.due_date} {task.due_time}")
        cols[1].write(task.pet_name)
        cols[2].write(f"{task.description} ({task.frequency})")
        if task.is_complete:
            cols[3].write("✅ done")
        else:
            # Same pet name + description + time could repeat, so key by object id.
            if cols[3].button("Mark done", key=f"done_{id(task)}"):
                next_task = scheduler.mark_task_complete(task)  # recurring tasks reschedule themselves
                if next_task is not None:
                    st.toast(f"Next '{task.description}' scheduled for {next_task.due_date}.")
                st.rerun()
else:
    st.info("No tasks yet. Add one above.")
