from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    owner = Owner(name="Jordan", available_minutes=90)

    mochi = Pet(name="Mochi", species="dog", age=3)
    mochi.add_task(Task("Morning walk",     30, "high",   "Park loop",      frequency="daily",  scheduled_time="07:00"))
    mochi.add_task(Task("Breakfast",        10, "high",   "Kibble + water", frequency="daily",  scheduled_time="07:30"))
    mochi.add_task(Task("Training session", 20, "medium", "Recall practice",frequency="weekly", scheduled_time="09:00"))
    mochi.add_task(Task("Evening walk",     25, "high",   "Sunset park run",frequency="daily",  scheduled_time="07:00"))  # conflict!

    luna = Pet(name="Luna", species="cat", age=5)
    luna.add_task(Task("Feeding",         10, "high",   "Wet food",    frequency="daily",  scheduled_time="08:00"))
    luna.add_task(Task("Litter box",      10, "medium", "Scoop",       frequency="daily",  scheduled_time="08:30"))
    luna.add_task(Task("Enrichment play", 15, "low",    "Wand toy",    frequency="weekly", scheduled_time="10:00"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    scheduler.build_schedule()

    sep = "-" * 52

    print(f"\nPawPal+ — Today's Schedule for {owner.name} (sorted by time)")
    print(sep)
    print(f"{'Time':<8} {'Task':<24} {'Min':>4}  {'Priority':<8}")
    print(sep)
    for task in scheduler.sort_by_time():
        print(f"{task.scheduled_time:<8} {task.title:<24} {task.duration_minutes:>4}  {task.priority:<8}")
    print(sep)
    print(f"{'':8} {'TOTAL':<24} {scheduler.total_time():>4}  min\n")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("Conflicts detected:")
        for w in conflicts:
            print(f"  ! {w}")
    else:
        print("No conflicts detected.")

    print(f"\nMochi's tasks only:")
    for t in scheduler.filter_tasks(pet_name="Mochi"):
        print(f"  - {t.title} ({t.priority})")

    print(f"\nRecurring task demo:")
    walk = mochi.tasks[0]
    walk.mark_complete()
    next_task = walk.recur()
    if next_task:
        print(f"  '{walk.title}' completed. Next occurrence: {next_task.description}")

    print(f"\n{scheduler.explain_plan()}\n")


if __name__ == "__main__":
    main()