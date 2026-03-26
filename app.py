import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
if "owner" not in st.session_state:
    st.session_state.owner = None
if "schedule" not in st.session_state:
    st.session_state.schedule = []
if "conflicts" not in st.session_state:
    st.session_state.conflicts = []

st.header("1. Owner info")
with st.form("owner_form"):
    owner_name = st.text_input("Your name", value="Jordan")
    available_minutes = st.number_input(
        "Time available today (minutes)", min_value=10, max_value=480, value=120
    )
    submitted_owner = st.form_submit_button("Save owner")

if submitted_owner:
    st.session_state.owner = Owner(
        name=owner_name, available_minutes=int(available_minutes)
    )
    st.session_state.schedule = []
    st.session_state.conflicts = []
    st.success(f"Owner saved: {owner_name} ({available_minutes} min available)")

st.header("2. Add a pet")
if st.session_state.owner is None:
    st.info("Save your owner info above before adding pets.")
else:
    with st.form("pet_form"):
        pet_name = st.text_input("Pet name", value="Mochi")
        species = st.selectbox("Species", ["dog", "cat", "other"])
        age = st.number_input("Age", min_value=0, max_value=30, value=2)
        submitted_pet = st.form_submit_button("Add pet")

    if submitted_pet:
        new_pet = Pet(name=pet_name, species=species, age=int(age))
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {pet_name} the {species}!")

    if st.session_state.owner.pets:
        st.write("**Your pets:**")
        for pet in st.session_state.owner.pets:
            st.write(f"- {pet.name} ({pet.species}, age {pet.age})")


st.header("3. Add a task")
if not st.session_state.owner or not st.session_state.owner.pets:
    st.info("Add at least one pet before adding tasks.")
else:
    with st.form("task_form"):
        pet_names = [p.name for p in st.session_state.owner.pets]
        selected_pet_name = st.selectbox("Which pet?", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        scheduled_time = st.text_input("Scheduled time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        description = st.text_input("Description (optional)", value="")
        submitted_task = st.form_submit_button("Add task")

    if submitted_task:
        target_pet = next(
            p for p in st.session_state.owner.pets if p.name == selected_pet_name
        )
        target_pet.add_task(
            Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                description=description,
                frequency=frequency,
                scheduled_time=scheduled_time,
            )
        )
        st.success(f"Added '{task_title}' to {selected_pet_name}'s tasks!")

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**All pending tasks:**")
        rows = [
            {
                "Pet": next(
                    p.name for p in st.session_state.owner.pets if t in p.tasks
                ),
                "Task": t.title,
                "Time": t.scheduled_time,
                "Minutes": t.duration_minutes,
                "Priority": t.priority,
                "Frequency": t.frequency,
            }
            for t in all_tasks
        ]
        st.table(rows)

st.header("4. Generate schedule")
if not st.session_state.owner or not st.session_state.owner.get_all_tasks():
    st.info("Add an owner, at least one pet, and at least one task first.")
else:
    if st.button("Generate schedule"):
        scheduler = Scheduler(st.session_state.owner)
        st.session_state.schedule = scheduler.build_schedule()
        st.session_state.conflicts = scheduler.detect_conflicts()

        st.success(
            f"Scheduled {len(st.session_state.schedule)} tasks — "
            f"{scheduler.total_time()} of {st.session_state.owner.available_minutes} min used."
        )

        #Conflict warnings
        if st.session_state.conflicts:
            for warning in st.session_state.conflicts:
                st.warning(f"Conflict: {warning}")
        else:
            st.success("No scheduling conflicts found.")

        #Sorted schedule table
        if st.session_state.schedule:
            st.write("**Today's plan (sorted by time):**")
            sorted_tasks = scheduler.sort_by_time()
            rows = [
                {
                    "Time": t.scheduled_time,
                    "Task": t.title,
                    "Minutes": t.duration_minutes,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                }
                for t in sorted_tasks
            ]
            st.table(rows)

            with st.expander("Why did the scheduler choose these tasks?"):
                st.text(scheduler.explain_plan())

        scheduled_set = set(id(t) for t in st.session_state.schedule)
        skipped = [
            t for t in st.session_state.owner.get_all_tasks()
            if id(t) not in scheduled_set
        ]
        if skipped:
            st.warning(f"{len(skipped)} task(s) skipped — time budget reached:")
            for t in skipped:
                st.write(f"- {t.title} ({t.duration_minutes} min, {t.priority})")

    if st.session_state.schedule:
        st.divider()
        st.subheader("Mark a task complete")
        task_titles = [t.title for t in st.session_state.schedule]
        selected_title = st.selectbox("Select task to complete", task_titles)

        if st.button("Mark complete"):
            for pet in st.session_state.owner.pets:
                for task in pet.tasks:
                    if task.title == selected_title and not task.completed:
                        task.mark_complete()
                        next_task = task.recur()
                        if next_task:
                            pet.add_task(next_task)
                            st.success(
                                f"'{task.title}' marked done! "
                                f"Next {task.frequency} occurrence added."
                            )
                        else:
                            st.success(f"'{task.title}' marked complete.")
                        break