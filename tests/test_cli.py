from deadline_radar.cli import main


def test_summary_command_prints_ranked_tasks(capsys):
    code = main(["summary", "examples/tasks.csv", "--today", "2026-07-28"])

    output = capsys.readouterr().out
    assert code == 0
    assert "Portfolio release" in output
    assert "score" in output
