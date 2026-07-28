from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .chart import plot_risk_chart
from .github import fetch_latest_actions_status
from .io import load_tasks, save_tasks
from .models import Task
from .risk import rank_tasks


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "summary":
        return _summary(args)
    if args.command == "chart":
        return _chart(args)
    if args.command == "refresh-ci":
        return _refresh_ci(args)
    parser.print_help()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="deadline-radar", description="Rank deadline risk from a task CSV.")
    subparsers = parser.add_subparsers(dest="command")

    summary = subparsers.add_parser("summary", help="print a risk-ranked task summary")
    summary.add_argument("csv_path")
    summary.add_argument("--today", help="override today's date, e.g. 2026-07-28")
    summary.add_argument("--json", action="store_true", help="print machine-readable JSON")

    chart = subparsers.add_parser("chart", help="create a PDF/PNG risk chart")
    chart.add_argument("csv_path")
    chart.add_argument("--output", "-o", default="risk_chart.pdf")
    chart.add_argument("--today", help="override today's date, e.g. 2026-07-28")

    refresh = subparsers.add_parser("refresh-ci", help="refresh GitHub Actions status for rows with a repo")
    refresh.add_argument("csv_path")
    refresh.add_argument("--output", "-o", help="output CSV path; defaults to overwriting input")

    return parser


def _summary(args: argparse.Namespace) -> int:
    ranked = rank_tasks(load_tasks(args.csv_path), today=_parse_today(args.today))
    if args.json:
        print(json.dumps([_as_dict(item) for item in ranked], ensure_ascii=False, indent=2))
        return 0

    print(f"{'score':>5}  {'level':<6}  {'days':>4}  task")
    print("-" * 52)
    for item in ranked:
        print(f"{item.score:5.1f}  {item.level:<6}  {item.days_left:4d}  {item.task.title}")
    return 0


def _chart(args: argparse.Namespace) -> int:
    output = plot_risk_chart(load_tasks(args.csv_path), args.output, today=_parse_today(args.today))
    print(f"saved {output}")
    return 0


def _refresh_ci(args: argparse.Namespace) -> int:
    tasks = []
    for task in load_tasks(args.csv_path):
        if task.repo:
            task = Task(
                title=task.title,
                due=task.due,
                estimated_hours=task.estimated_hours,
                progress=task.progress,
                priority=task.priority,
                repo=task.repo,
                ci_status=fetch_latest_actions_status(task.repo),
            )
        tasks.append(task)
    output = Path(args.output or args.csv_path)
    save_tasks(output, tasks)
    print(f"wrote {output}")
    return 0


def _parse_today(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def _as_dict(item) -> dict[str, object]:
    return {
        "title": item.task.title,
        "score": item.score,
        "level": item.level,
        "days_left": item.days_left,
        "ci_status": item.task.ci_status,
        "reasons": list(item.reasons),
    }


if __name__ == "__main__":
    raise SystemExit(main())
