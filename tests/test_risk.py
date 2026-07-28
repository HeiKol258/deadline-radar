from datetime import date

from deadline_radar.models import Task
from deadline_radar.risk import assess_task, rank_tasks


TODAY = date(2026, 7, 28)


def test_completed_task_has_zero_risk():
    task = Task("Done", date(2026, 7, 29), estimated_hours=10, progress=100, priority=5)

    result = assess_task(task, today=TODAY)

    assert result.score == 0
    assert result.level == "done"


def test_failed_ci_increases_risk():
    base = Task("Project", date(2026, 8, 1), estimated_hours=5, progress=30, priority=4, ci_status="success")
    failed = Task("Project", date(2026, 8, 1), estimated_hours=5, progress=30, priority=4, ci_status="failed")

    assert assess_task(failed, today=TODAY).score > assess_task(base, today=TODAY).score


def test_rank_tasks_places_urgent_item_first():
    low = Task("Later", date(2026, 8, 20), estimated_hours=2, progress=80, priority=1)
    high = Task("Soon", date(2026, 7, 29), estimated_hours=8, progress=0, priority=5)

    ranked = rank_tasks([low, high], today=TODAY)

    assert ranked[0].task.title == "Soon"
    assert ranked[0].level == "high"
