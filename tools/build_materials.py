"""Extract fictional source materials for scenario questions into materials/.

Single source of truth is question_bank.json; this file is a human-readable view.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    bank = json.loads((ROOT / "question_bank.json").read_text(encoding="utf-8"))
    scenarios = [q for q in bank if q["type"] == "scenario"]
    lines = [
        "# Fictional Source Materials — Scenario Questions",
        "",
        "All entries, AI-generated questions, meeting minutes and FAQ drafts below",
        "are **fictional**. No real person, enterprise, or client information appears.",
        "Each block is attached to one scenario question in `question_bank.json/csv`.",
        "",
    ]
    for q in scenarios:
        lines += [
            f"## {q['question_id']} — {q['scenario_category']}",
            "",
            f"**knowledge_point:** {q['knowledge_point']}  ",
            f"**difficulty:** {q['difficulty']}",
            "",
            q["source_material"],
            "",
            "---",
            "",
        ]
    out = ROOT / "materials" / "scenario_materials.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"MATERIALS_WRITTEN {out.stat().st_size}B scenarios={len(scenarios)}")


if __name__ == "__main__":
    main()
