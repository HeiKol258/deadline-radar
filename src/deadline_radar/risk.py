from __future__ import annotations

from datetime import date

from .models import RiskAssessment, Task

CI_PENALTY = {
    "success": 0.0,
    "completed": 0.0,
    "passed": 0.0,
    "skipped": 4.0,
    "missing": 8.0,
    "no_runs": 8.0,
    "unknown": 6.0,
    "running": 10.0,
    "failed": 18.0,
    "failure": 18.0,
    "cancelled": 14.0,
    "timed_out": 18.0,
}


def assess_task(task: Task, today: date | None = None) -> RiskAssessment:
    today = today or date.today()
    days_left = (task.due - today).days

    if task.is_done:
        return RiskAssessment(task, days_left, 0.0, "done", ("already complete",))

    deadline_pressure = _deadline_pressure(days_left)
    work_pressure = min(25.0, task.remaining_hours / 8.0 * 25.0)
    priority_pressure = min(20.0, max(0.0, (task.priority - 1) / 4.0 * 20.0))
    ci_penalty = CI_PENALTY.get(task.ci_status, CI_PENALTY["unknown"])

    score = min(100.0, deadline_pressure + work_pressure + priority_pressure + ci_penalty)
    score = round(score, 1)
    return RiskAssessment(task, days_left, score, _level(score), _reasons(task, days_left, ci_penalty))


def rank_tasks(tasks: list[Task], today: date | None = None) -> list[RiskAssessment]:
    assessed = [assess_task(task, today=today) for task in tasks]
    return sorted(assessed, key=lambda item: (item.score, -item.days_left), reverse=True)


def _deadline_pressure(days_left: int) -> float:
    if days_left < 0:
        return 55.0
    if days_left <= 14:
        return (14 - days_left) / 14.0 * 45.0
    return 0.0


def _level(score: float) -> str:
    if score <= 0:
        return "done"
    if score < 35:
        return "low"
    if score < 65:
        return "medium"
    return "high"


def _reasons(task: Task, days_left: int, ci_penalty: float) -> tuple[str, ...]:
    reasons: list[str] = []
    if days_left < 0:
        reasons.append("overdue")
    elif days_left <= 3:
        reasons.append("deadline soon")
    if task.remaining_hours >= 6:
        reasons.append("many hours left")
    if task.priority >= 4:
        reasons.append("high priority")
    if ci_penalty >= 10:
        reasons.append("CI needs attention")
    elif ci_penalty > 0:
        reasons.append("CI not confirmed")
    return tuple(reasons or ["on track"])
