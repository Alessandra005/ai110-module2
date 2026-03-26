from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    owner = Owner(name="Jordan", available_minutes=90)

    mochi = Pet(name="Mochi", species="dog", age=3)
    mochi.add_task(Task("Morning walk",     30, "high",   "30-min neighbourhood loop"))
    mochi.add_task(Task("Breakfast",        10, "high",   "1 cup kibble + water"))
    mochi.add_task(Task("Training session", 20, "medium", "Sit, stay, recall practice"))
    mochi.add_task(Task("Evening walk",     25, "high",   "Park run before sunset"))

    luna = Pet(name="Luna", species="cat", age=5)
    luna.add_task(Task("Feeding",          10, "high",   "Wet food, morning"))
    luna.add_task(Task("Litter box",       10, "medium", "Scoop and replace as needed"))
    luna.add_task(Task("Enrichment play",  15, "low",    "Wand toy or puzzle feeder"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    #Scheduler 
    scheduler = Scheduler(owner)
    scheduler.build_schedule()

    #Output
    sep = "-" * 50
    print(f"\nPawPal+ — Today's Schedule for {owner.name}")
    print(sep)
    print(f"{'#':<4} {'Task':<24} {'Min':>4}  {'Priority':<8}")
    print(sep)
    for i, task in enumerate(scheduler.schedule, 1):
        print(f"{i:<4} {task.title:<24} {task.duration_minutes:>4}  {task.priority:<8}")
    print(sep)
    print(f"     {'TOTAL':<24} {scheduler.total_time():>4}  (of {owner.available_minutes} min available)")

    skipped = [t for t in owner.get_all_tasks() if t not in scheduler.schedule]
    if skipped:
        print("\nSkipped (time limit reached):")
        for t in skipped:
            print(f"  - {t.title} ({t.duration_minutes} min, {t.priority})")

    print(f"\n{scheduler.explain_plan()}\n")


if __name__ == "__main__":
    main()