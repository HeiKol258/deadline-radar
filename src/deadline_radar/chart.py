from __future__ import annotations

from datetime import date
from pathlib import Path

from .models import Task
from .risk import rank_tasks


def plot_risk_chart(tasks: list[Task], output: str | Path, today: date | None = None) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ranked = rank_tasks(tasks, today=today)
    visible = ranked[:10]
    names = [item.task.title for item in visible][::-1]
    scores = [item.score for item in visible][::-1]
    colors = [_color(item.level) for item in visible][::-1]

    fig, ax = plt.subplots(figsize=(8, max(3.5, 0.45 * len(visible))))
    ax.barh(names, scores, color=colors)
    ax.set_xlim(0, 100)
    ax.set_xlabel("risk score")
    ax.set_title("Deadline Radar")
    ax.grid(axis="x", alpha=0.25)
    for index, score in enumerate(scores):
        ax.text(min(score + 1.5, 96), index, f"{score:.1f}", va="center", fontsize=9)
    fig.tight_layout()

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def _color(level: str) -> str:
    return {
        "done": "#7a7a7a",
        "low": "#2a9d8f",
        "medium": "#e9c46a",
        "high": "#e76f51",
    }.get(level, "#8d99ae")
