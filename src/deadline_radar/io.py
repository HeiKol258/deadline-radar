from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from .models import Task

FIELDNAMES = ["title", "due", "estimated_hours", "progress", "priority", "repo", "ci_status"]


def parse_date(value: str) -> date:
    value = value.strip()
    if not value:
        raise ValueError("due date is required")
    try:
        return date.fromisoformat(value)
    except ValueError:
        return datetime.fromisoformat(value).date()


def load_tasks(path: str | Path) -> list[Task]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        return [task_from_row(row) for row in rows]


def save_tasks(path: str | Path, tasks: Iterable[Task]) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for task in tasks:
            writer.writerow(
                {
                    "title": task.title,
                    "due": task.due.isoformat(),
                    "estimated_hours": f"{task.estimated_hours:g}",
                    "progress": f"{task.progress:g}",
                    "priority": task.priority,
                    "repo": task.repo,
                    "ci_status": task.ci_status,
                }
            )


def task_from_row(row: dict[str, str | None]) -> Task:
    return Task(
        title=(row.get("title") or "").strip(),
        due=parse_date(row.get("due") or ""),
        estimated_hours=float(row.get("estimated_hours") or 0),
        progress=float(row.get("progress") or 0),
        priority=int(row.get("priority") or 3),
        repo=(row.get("repo") or "").strip(),
        ci_status=(row.get("ci_status") or "unknown").strip().lower() or "unknown",
    )
