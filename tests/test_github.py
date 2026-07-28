import json

from deadline_radar.github import fetch_latest_actions_status, normalize_repo


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_normalize_repo_accepts_url():
    assert normalize_repo("https://github.com/owner/repo") == "owner/repo"


def test_fetch_latest_actions_status_uses_latest_conclusion():
    def opener(request):
        assert request.full_url.endswith("/repos/owner/repo/actions/runs?per_page=1")
        return FakeResponse({"workflow_runs": [{"conclusion": "success"}]})

    assert fetch_latest_actions_status("owner/repo", opener=opener) == "success"


def test_fetch_latest_actions_status_handles_no_runs():
    def opener(request):
        return FakeResponse({"workflow_runs": []})

    assert fetch_latest_actions_status("owner/repo", opener=opener) == "no_runs"
