import pytest
from pawpal_system import Task, Pet, Owner, Scheduler

@pytest.fixture
def sample_task():
    return Task(title="Morning walk", duration_minutes=30, priority="high")


@pytest.fixture
def sample_pet():
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(Task("Walk",    30, "high"))
    pet.add_task(Task("Feeding", 10, "high"))
    pet.add_task(Task("Play",    20, "low"))
    return pet


@pytest.fixture
def sample_owner(sample_pet):
    owner = Owner(name="Jordan", available_minutes=90)
    owner.add_pet(sample_pet)
    return owner


#Task tests
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


#Pet tests
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


#Scheduler tests
def test_scheduler_respects_time_limit(sample_owner):
    """Scheduled tasks must not exceed the time limit."""
    scheduler = Scheduler(sample_owner, time_limit=40)
    scheduler.build_schedule()
    assert scheduler.total_time() <= 40


def test_scheduler_prefers_high_priority():
    """When only one task fits, the high-priority one must be chosen."""
    owner = Owner(name="Test", available_minutes=35)
    pet = Pet("Rex", "dog")
    pet.add_task(Task("Low task",  30, "low"))
    pet.add_task(Task("High task", 30, "high"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner, time_limit=35)
    scheduler.build_schedule()
    assert len(scheduler.schedule) == 1
    assert scheduler.schedule[0].priority == "high"


def test_filter_by_priority_before_build_returns_empty():
    """filter_by_priority() called before build_schedule() should return empty list."""
    owner = Owner(name="Test", available_minutes=60)
    scheduler = Scheduler(owner)
    result = scheduler.filter_by_priority("high")
    assert result == []