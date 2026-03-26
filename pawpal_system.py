from dataclasses import dataclass, field
from typing import Literal

Priority = Literal["low", "medium", "high"]
PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority = "medium"
    description: str = ""
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def is_high_priority(self) -> bool:
        return self.priority == "high"

    def time_required(self) -> int:
        return self.duration_minutes

    def __str__(self) -> str:
        status = "done" if self.completed else "pending"
        return f"{self.title} ({self.duration_minutes} min, {self.priority}, {status})"


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_pending_tasks(self) -> list:
        return [t for t in self.tasks if not t.completed]

    def get_tasks_by_priority(self) -> list:
        return sorted(
            self.get_pending_tasks(),
            key=lambda t: PRIORITY_RANK[t.priority],
            reverse=True,
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.species}, age {self.age})"


@dataclass
class Owner:
    name: str
    available_minutes: int = 120
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks_by_priority())
        return sorted(
            all_tasks,
            key=lambda t: PRIORITY_RANK[t.priority],
            reverse=True,
        )


class Scheduler:
    def __init__(self, owner: Owner, time_limit: int = None):
        self.owner = owner
        self.time_limit = time_limit if time_limit is not None else owner.available_minutes
        self.schedule = []

    def build_schedule(self) -> list:
        self.schedule = []
        time_used = 0
        for task in self.owner.get_all_tasks():
            if task.completed:
                continue
            if time_used + task.time_required() <= self.time_limit:
                self.schedule.append(task)
                time_used += task.time_required()
        return self.schedule

    def filter_by_priority(self, priority: str) -> list:
        if not self.schedule:
            print("Warning: schedule is empty. Build the schedule first.")
            return []
        return [t for t in self.schedule if t.priority == priority]

    def total_time(self) -> int:
        return sum(t.time_required() for t in self.schedule)

    def explain_plan(self) -> str:
        if not self.schedule:
            return "No tasks were scheduled."
        lines = [f"Plan for {self.owner.name} — {self.total_time()} / {self.time_limit} min used:"]
        for i, task in enumerate(self.schedule, 1):
            reason = "high priority" if task.is_high_priority() else f"{task.priority} priority"
            lines.append(f"  {i}. {task.title} ({task.duration_minutes} min) — {reason}")
        scheduled_set = set(id(t) for t in self.schedule)
        skipped = [t for t in self.owner.get_all_tasks() if id(t) not in scheduled_set]
        if skipped:
            lines.append("Skipped (time limit):")
            for t in skipped:
                lines.append(f"  - {t.title} ({t.duration_minutes} min)")
        return "\n".join(lines)

    def get_summary(self) -> dict:
        return {
            "owner": self.owner.name,
            "total_minutes": self.total_time(),
            "available_minutes": self.time_limit,
            "task_count": len(self.schedule),
            "tasks": [
                {
                    "title": t.title,
                    "duration_minutes": t.duration_minutes,
                    "priority": t.priority,
                    "completed": t.completed,
                }
                for t in self.schedule
            ],
        }