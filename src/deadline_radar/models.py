from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Task:
    title: str
    due: date
    estimated_hours: float
    progress: float
    priority: int = 3
    repo: str = ""
    ci_status: str = "unknown"

    @property
    def remaining_hours(self) -> float:
        progress = min(100.0, max(0.0, self.progress))
        return max(0.0, self.estimated_hours * (1.0 - progress / 100.0))

    @property
    def is_done(self) -> bool:
        return self.progress >= 100.0


@dataclass(frozen=True)
class RiskAssessment:
    task: Task
    days_left: int
    score: float
    level: str
    reasons: tuple[str, ...]
