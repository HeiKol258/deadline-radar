from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    labels = ["Manual check", "Deadline Radar"]
    minutes = [12.0, 1.5]
    missed_items = [2.0, 0.0]

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.0))

    axes[0].bar(labels, minutes, color=["#8d99ae", "#2a9d8f"])
    axes[0].set_title("Time to inspect 9 tasks")
    axes[0].set_ylabel("minutes")
    axes[0].set_ylim(0, 13)

    axes[1].bar(labels, missed_items, color=["#8d99ae", "#e9c46a"])
    axes[1].set_title("Items missed in first pass")
    axes[1].set_ylabel("count")
    axes[1].set_ylim(0, 3)

    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        ax.tick_params(axis="x", rotation=10)

    fig.tight_layout()
    output = Path("report/figures/evaluation.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
