import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

with st.sidebar:
    st.title("🐾 PawPal+")
    st.caption("Pet care planning assistant")
    st.divider()

    if "owner" not in st.session_state:
        st.session_state.owner = None
    if "schedule" not in st.session_state:
        st.session_state.schedule = []
    if "conflicts" not in st.session_state:
        st.session_state.conflicts = []

    st.subheader("Owner info")
    with st.form("owner_form"):
        owner_name = st.text_input("Your name", value="Jordan")
        available_minutes = st.number_input(
            "Time available (min)", min_value=10, max_value=480, value=120
        )
        if st.form_submit_button("Save owner", use_container_width=True):
            st.session_state.owner = Owner(
                name=owner_name, available_minutes=int(available_minutes)
            )
            st.session_state.schedule = []
            st.session_state.conflicts = []
            st.success(f"Saved {owner_name}!")

    st.divider()

    st.subheader("Add a pet")
    if st.session_state.owner is None:
        st.info("Save owner info first.")
    else:
        with st.form("pet_form"):
            pet_name = st.text_input("Pet name", value="Mochi")
            species = st.selectbox("Species", ["dog", "cat", "other"])
            age = st.number_input("Age", min_value=0, max_value=30, value=2)
            if st.form_submit_button("Add pet", use_container_width=True):
                st.session_state.owner.add_pet(Pet(pet_name, species, int(age)))
                st.success(f"Added {pet_name}!")

        if st.session_state.owner.pets:
            st.write("**Your pets:**")
            for p in st.session_state.owner.pets:
                st.write(f"- {p.name} ({p.species}, age {p.age})")


PRIORITY_EMOJI = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
SPECIES_EMOJI  = {"dog": "🐶", "cat": "🐱", "other": "🐾"}
FREQ_EMOJI     = {"daily": "📅 Daily", "weekly": "🗓️ Weekly", "once": "1️⃣ Once"}

def priority_emoji(p): return PRIORITY_EMOJI.get(p, p)
def species_emoji(s):  return SPECIES_EMOJI.get(s, "🐾")
def freq_emoji(f):     return FREQ_EMOJI.get(f, f)


st.title("🐾 PawPal+")

if st.session_state.owner is None:
    st.info("Set up your owner profile in the sidebar to get started.")
    st.stop()

owner = st.session_state.owner


tab_tasks, tab_schedule = st.tabs(["📋 Manage Tasks", "📅 Today's Schedule"])
with tab_tasks:
    if not owner.pets:
        st.info("Add at least one pet in the sidebar first.")
    else:
        st.subheader("Add a task")
        with st.form("task_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
                task_title = st.text_input("Task title", value="Morning walk")
            with col2:
                duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
                scheduled_time = st.text_input("Scheduled time (HH:MM)", value="08:00")
            with col3:
                priority = st.selectbox("Priority", ["high", "medium", "low"])
                frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
            description = st.text_input("Description (optional)", value="")

            if st.form_submit_button("Add task", use_container_width=True):
                target = next(p for p in owner.pets if p.name == selected_pet_name)
                target.add_task(Task(
                    title=task_title,
                    duration_minutes=int(duration),
                    priority=priority,
                    description=description,
                    frequency=frequency,
                    scheduled_time=scheduled_time,
                ))
                st.success(f"Added '{task_title}' to {selected_pet_name}'s tasks!")

        
        all_tasks = owner.get_all_tasks()
        if all_tasks:
            st.subheader("All pending tasks")
            rows = []
            for t in all_tasks:
                pet = next((p for p in owner.pets if t in p.tasks), None)
                rows.append({
                    "Pet": f"{species_emoji(pet.species)} {pet.name}" if pet else "—",
                    "Task": t.title,
                    "Time": t.scheduled_time,
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": priority_emoji(t.priority),
                    "Frequency": freq_emoji(t.frequency),
                })
            st.table(rows)
        else:
            st.info("No pending tasks yet.")


with tab_schedule:
    st.subheader(f"Daily plan for {owner.name}")

    if not owner.get_all_tasks():
        st.info("Add tasks in the Manage Tasks tab first.")
    else:
        if st.button("Generate schedule", type="primary", use_container_width=True):
            scheduler = Scheduler(owner)
            st.session_state.schedule = scheduler.build_schedule()
            st.session_state.conflicts = scheduler.detect_conflicts()

        if st.session_state.schedule:
            scheduler = Scheduler(owner)
            scheduler.schedule = st.session_state.schedule

            used = scheduler.total_time()
            available = owner.available_minutes
            pct = min(used / available, 1.0)
            st.markdown(f"**Time used:** {used} / {available} min")
            st.progress(pct)

            if st.session_state.conflicts:
                for w in st.session_state.conflicts:
                    st.warning(f"⚠️ {w}")
            else:
                st.success("✅ No scheduling conflicts found.")

            st.subheader("Today's plan (sorted by priority, then time)")
            sorted_tasks = sorted(
                st.session_state.schedule,
                key=lambda t: (-{"high": 3, "medium": 2, "low": 1}[t.priority], t.scheduled_time)
            )
            rows = []
            for t in sorted_tasks:
                rows.append({
                    "Time": t.scheduled_time,
                    "Task": t.title,
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": priority_emoji(t.priority),
                    "Frequency": freq_emoji(t.frequency),
                })
            st.table(rows)

            with st.expander("💡 Why did the scheduler choose these tasks?"):
                st.text(scheduler.explain_plan())

            scheduled_ids = set(id(t) for t in st.session_state.schedule)
            skipped = [t for t in owner.get_all_tasks() if id(t) not in scheduled_ids]
            if skipped:
                st.warning(f"⏭️ {len(skipped)} task(s) skipped — time budget reached:")
                for t in skipped:
                    st.write(f"- {priority_emoji(t.priority)} {t.title} ({t.duration_minutes} min)")

            st.divider()
            st.subheader("Mark a task complete")
            task_titles = [t.title for t in st.session_state.schedule]
            selected_title = st.selectbox("Select task", task_titles)
            if st.button("Mark complete ✓", use_container_width=True):
                for pet in owner.pets:
                    for task in pet.tasks:
                        if task.title == selected_title and not task.completed:
                            task.mark_complete()
                            next_task = task.recur()
                            if next_task:
                                pet.add_task(next_task)
                                st.success(
                                    f"✅ '{task.title}' done! "
                                    f"Next {freq_emoji(task.frequency)} occurrence added."
                                )
                            else:
                                st.success(f"✅ '{task.title}' marked complete.")
                            break