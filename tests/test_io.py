from datetime import date

import pytest

from deadline_radar.io import load_tasks


def test_load_tasks_reads_example():
    tasks = load_tasks("examples/tasks.csv")

    assert tasks[0].title == "Portfolio release"
    assert tasks[0].due == date(2026, 8, 10)
    assert tasks[0].remaining_hours == pytest.approx(11.7)
