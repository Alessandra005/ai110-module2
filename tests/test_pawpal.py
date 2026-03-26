import pytest
from pawpal_system import Task, Pet, Owner, Scheduler

@pytest.fixture
def sample_task():
    return Task(title="Morning walk", duration_minutes=30, priority="high",
                frequency="daily", scheduled_time="07:00")

@pytest.fixture
def sample_pet():
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task("Walk",    30, "high",   scheduled_time="07:00", frequency="daily"))
    pet.add_task(Task("Feeding", 10, "high",   scheduled_time="08:00", frequency="daily"))
    pet.add_task(Task("Play",    20, "low",    scheduled_time="10:00", frequency="weekly"))
    return pet

@pytest.fixture
def sample_owner(sample_pet):
    owner = Owner(name="Jordan", available_minutes=90)
    owner.add_pet(sample_pet)
    return owner


def test_task_starts_incomplete(sample_task):
    """A new task should not be completed."""
    assert sample_task.completed is False

def test_mark_complete_changes_status(sample_task):
    """mark_complete() must flip completed to True."""
    sample_task.mark_complete()
    assert sample_task.completed is True

def test_completed_task_not_rescheduled(sample_owner):
    """A task marked complete before scheduling must not appear in the schedule."""
    sample_owner.pets[0].tasks[0].mark_complete()
    scheduler = Scheduler(sample_owner)
    scheduler.build_schedule()
    assert all(not t.completed for t in scheduler.schedule)


def test_daily_recur_creates_new_task(sample_task):
    """Marking a daily task complete and calling recur() should return a new Task."""
    sample_task.mark_complete()
    next_task = sample_task.recur()
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.title == sample_task.title

def test_once_task_recur_returns_none():
    """A task with frequency 'once' should return None from recur()."""
    task = Task("Bath", 15, "low", frequency="once")
    task.mark_complete()
    assert task.recur() is None

def test_weekly_recur_creates_new_task():
    """A weekly task should also produce a new instance on recur()."""
    task = Task("Grooming", 20, "medium", frequency="weekly", scheduled_time="09:00")
    task.mark_complete()
    next_task = task.recur()
    assert next_task is not None
    assert next_task.frequency == "weekly"


def test_add_task_increases_count(sample_pet):
    """Adding a task should grow the pet's task list by one."""
    before = len(sample_pet.tasks)
    sample_pet.add_task(Task("Grooming", 20, "medium"))
    assert len(sample_pet.tasks) == before + 1

def test_get_pending_excludes_completed(sample_pet):
    """Completed tasks must not appear in pending."""
    sample_pet.tasks[0].mark_complete()
    assert all(not t.completed for t in sample_pet.get_pending_tasks())

def test_tasks_sorted_high_before_low(sample_pet):
    """get_tasks_by_priority() must return high priority before low."""
    sorted_tasks = sample_pet.get_tasks_by_priority()
    assert sorted_tasks[0].priority == "high"
    assert sorted_tasks[-1].priority == "low"


def test_scheduler_respects_time_limit(sample_owner):
    """Scheduled tasks must not exceed the time limit."""
    scheduler = Scheduler(sample_owner, time_limit=40)
    scheduler.build_schedule()
    assert scheduler.total_time() <= 40

def test_scheduler_prefers_high_priority():
    """When only one task fits, the high-priority one must be chosen."""
    owner = Owner(name="Test", available_minutes=35)
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Low task",  30, "low",  scheduled_time="09:00"))
    pet.add_task(Task("High task", 30, "high", scheduled_time="08:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner, time_limit=35)
    scheduler.build_schedule()
    assert len(scheduler.schedule) == 1
    assert scheduler.schedule[0].priority == "high"

def test_sort_by_time_returns_chronological_order(sample_owner):
    """sort_by_time() must return tasks in ascending HH:MM order."""
    scheduler = Scheduler(sample_owner)
    scheduler.build_schedule()
    sorted_tasks = scheduler.sort_by_time()
    times = [t.scheduled_time for t in sorted_tasks]
    assert times == sorted(times)

def test_detect_conflicts_flags_same_time():
    """detect_conflicts() must warn when two tasks share the same scheduled_time."""
    owner = Owner(name="Test", available_minutes=120)
    pet = Pet("Buddy", "dog")
    pet.add_task(Task("Walk",    20, "high", scheduled_time="07:00"))
    pet.add_task(Task("Feeding", 10, "high", scheduled_time="07:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.build_schedule()
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) >= 1

def test_detect_conflicts_no_false_positives():
    """detect_conflicts() must return empty list when all times are unique."""
    owner = Owner(name="Test", available_minutes=120)
    pet = Pet("Luna", "cat")
    pet.add_task(Task("Feeding", 10, "high",   scheduled_time="08:00"))
    pet.add_task(Task("Play",    15, "medium", scheduled_time="09:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.build_schedule()
    assert scheduler.detect_conflicts() == []

def test_filter_by_priority_before_build_returns_empty():
    """filter_by_priority() called before build_schedule() should return empty list."""
    owner = Owner(name="Test", available_minutes=60)
    scheduler = Scheduler(owner)
    assert scheduler.filter_by_priority("high") == []