from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Callable, Protocol


class ResponseLike(Protocol):
    def read(self) -> bytes: ...

    def __enter__(self) -> "ResponseLike": ...

    def __exit__(self, exc_type, exc, tb) -> None: ...


OpenUrl = Callable[[urllib.request.Request], ResponseLike]


def normalize_repo(value: str) -> str:
    value = value.strip()
    if value.startswith("https://github.com/"):
        value = value.removeprefix("https://github.com/").strip("/")
    parts = value.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError(f"invalid GitHub repository: {value!r}")
    return f"{parts[0]}/{parts[1]}"


def fetch_latest_actions_status(
    repo: str,
    token: str | None = None,
    opener: OpenUrl | None = None,
) -> str:
    repo = normalize_repo(repo)
    opener = opener or urllib.request.urlopen
    token = token if token is not None else os.environ.get("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=1"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)

    try:
        with opener(request) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        return "unknown"

    runs = payload.get("workflow_runs", [])
    if not runs:
        return "no_runs"

    latest = runs[0]
    conclusion = latest.get("conclusion")
    status = latest.get("status")
    if conclusion:
        return str(conclusion).lower()
    if status:
        return str(status).lower()
    return "unknown"
