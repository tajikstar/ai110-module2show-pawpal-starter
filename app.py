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
tasks = scheduler.sort_by_time()

if tasks:
    filter_choice = st.selectbox("Show tasks for", ["All pets"] + [p.name for p in owner.pets])
    if filter_choice != "All pets":
        shown = scheduler.sort_by_time(scheduler.filter_by_pet(filter_choice))
    else:
        shown = tasks

    for i, task in enumerate(shown):
        cols = st.columns([2, 2, 3, 2])
        cols[0].write(f"{task.due_date} {task.due_time}")
        cols[1].write(task.pet_name)
        cols[2].write(f"{task.description} ({task.frequency})")
        if task.is_complete:
            cols[3].write("✅ done")
        else:
            # Same pet name + description + time could repeat, so key by object id.
            if cols[3].button("Mark done", key=f"done_{id(task)}"):
                scheduler.mark_task_complete(task)  # also schedules the next one if it recurs
                st.rerun()

    for warning in scheduler.get_conflict_warnings():
        st.warning(warning)
else:
    st.info("No tasks yet. Add one above.")
