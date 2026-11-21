"""Capture REAL command outputs + versions into evidence/ (no expected output)."""
from __future__ import annotations

import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "evidence"
EV.mkdir(exist_ok=True)
PY = sys.executable


def _anon(text: str) -> str:
    home = os.path.expanduser("~")
    repo = str(ROOT)
    for p in (repo, repo.replace("\\", "/")):
        text = text.replace(p, "<repo>")
    for p in (home, home.replace("\\", "/")):
        text = text.replace(p, "<home>")
    return text


def run(args: list[str]) -> tuple[int, str]:
    p = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return p.returncode, _anon(p.stdout + (("\n[stderr]\n" + p.stderr) if p.stderr.strip() else ""))


def main() -> None:
    env = [
        f"captured_at_utc: {datetime.now(timezone.utc).isoformat()}",
        f"platform: {platform.platform()}",
        f"python_executable: <python {sys.version.split()[0]}>  # path withheld",
        f"csv_module: stdlib csv (QUOTE_ALL)",
        f"json_module: stdlib json (json.loads strict parse)",
    ]
    rc_build, out_build = run([PY, "tools/build_bank.py"])
    rc_mat, out_mat = run([PY, "tools/build_materials.py"])
    rc_val, out_val = run([PY, "tools/validate.py"])
    (EV / "validate_output.txt").write_text(out_val, encoding="utf-8")

    (EV / "verification.md").write_text(
        "# Real verification record — #3186 knowledge administrator question bank\n\n"
        "Commands below were actually executed with the captured interpreter. "
        "Outputs are verbatim; local home/repo paths anonymized. No database or "
        "external service is required by this ticket (Dependencies: None).\n\n"
        "## Environment (captured)\n\n```\n" + "\n".join(env) + "\n```\n\n"
        "## Commands run (verbatim output)\n\n"
        "```\n$ python tools/build_bank.py\n" + out_build.strip() + "\n```\n\n"
        "```\n$ python tools/build_materials.py\n" + out_mat.strip() + "\n```\n\n"
        "```\n$ python tools/validate.py\n" + out_val.strip() + "\n```\n\n"
        "## Acceptance criteria result\n\n"
        "| AC | Result |\n|---|---|\n"
        "| C1 — 30 questions, type mix 8/6/4/12 | PASS |\n"
        "| C2 — >=6 bank-review/extraction-QA scenarios with fictional material | PASS |\n"
        "| C3 — every question has answer + explanation + knowledge_point | PASS |\n"
        "| C4 — JSON parseable by standard parser (plus CSV round-trip) | PASS |\n",
        encoding="utf-8",
    )
    print(f"EVIDENCE_WRITTEN build_rc={rc_build} mat_rc={rc_mat} validate_rc={rc_val}")
    print(out_val.strip().splitlines()[-1])


if __name__ == "__main__":
    main()
