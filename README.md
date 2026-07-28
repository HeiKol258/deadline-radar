# Deadline Radar

[![CI](https://github.com/HeiKol258/deadline-radar/actions/workflows/ci.yml/badge.svg)](https://github.com/HeiKol258/deadline-radar/actions/workflows/ci.yml)

Deadline Radar is a small command line tool for students who want one quick view of
which tasks deserve attention first. It reads a CSV file of tasks, deadlines,
estimated work hours, progress, priority, and optional GitHub Actions status, then
turns them into a risk-ranked list or a chart.

It is useful when a task is not simply "due soon": a half-finished high-priority
task with failing CI should feel more urgent than a small task due on the same day.

## Install

```bash
git clone https://github.com/HeiKol258/deadline-radar.git
cd deadline-radar
python -m pip install .
```

## Quick Start

Run the example summary:

```bash
deadline-radar summary examples/tasks.csv --today 2026-07-28
```

Example output:

```text
score  level   days  task
----------------------------------------------------
 54.2  medium    13  Portfolio release
 52.8  medium     4  CI practice repo
 46.4  medium    10  Reading summary
```

Create a vector PDF chart:

```bash
deadline-radar chart examples/tasks.csv --output examples/risk_chart.pdf
```

Refresh GitHub Actions status for rows that have a `repo` value:

```bash
deadline-radar refresh-ci examples/tasks.csv --output examples/tasks.generated.csv
```

For private repositories, set a GitHub token before running `refresh-ci`:

```bash
export GITHUB_TOKEN=...
```

Never commit `.env` files or tokens.

## CSV Format

The input file should contain these columns:

```csv
title,due,estimated_hours,progress,priority,repo,ci_status
Portfolio release,2026-08-10,18,35,5,HeiKol258/deadline-radar,unknown
```

- `due`: ISO date, such as `2026-08-10`
- `estimated_hours`: estimated total work hours
- `progress`: completion percentage from 0 to 100
- `priority`: 1 to 5
- `repo`: optional GitHub repository, such as `owner/name`
- `ci_status`: optional status, such as `success`, `failed`, `running`, or `unknown`

## Development

Set up a development environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest -q
```

The GitHub Actions workflow in `.github/workflows/ci.yml` runs the same tests on
every push and pull request.
