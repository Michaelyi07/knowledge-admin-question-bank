"""Build question_bank.json (source of truth) and question_bank.csv from it.

Eight required fields appear on every row. Scenario rows additionally carry
scenario_category and source_material (fictional material attached to the stem).
Strict UTF-8 JSON, quoted keys, no trailing commas; CSV uses QUOTE_ALL so quotes
and asterisks in material survive a round trip.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from questions_data import QUESTIONS
from scenarios_data import SCENARIOS
from rebalance import rebalance

REQUIRED = [
    "question_id", "type", "stem", "options", "answer",
    "explanation", "knowledge_point", "difficulty",
]
EXTRA = ["scenario_category", "source_material"]
FIELDS = REQUIRED + EXTRA


def main() -> None:
    bank = rebalance(QUESTIONS + SCENARIOS)
    # Normalise: every row has the same field order; non-scenario extras are "".
    rows = []
    for q in bank:
        row = {k: q.get(k, "") if k in EXTRA else q[k] for k in FIELDS}
        rows.append(row)

    json_path = ROOT / "question_bank.json"
    json_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    csv_path = ROOT / "question_bank.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for row in rows:
            # options is a list -> store canonical JSON literal in the cell
            out = dict(row)
            out["options"] = json.dumps(row["options"], ensure_ascii=False)
            w.writerow(out)

    print(f"BUILT json={json_path.stat().st_size}B csv={csv_path.stat().st_size}B rows={len(rows)}")


if __name__ == "__main__":
    main()
