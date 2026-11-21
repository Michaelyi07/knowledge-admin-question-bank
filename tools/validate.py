"""Validate the delivered question bank against the 4 acceptance criteria.

Every check is a real assertion on the parsed artifacts. Exits non-zero on any
failure so the verification record cannot be a placeholder.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from answer_oracle import ANSWERS as ORACLE  # human-reviewed correct-answer key

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))


def main() -> int:
    json_path = ROOT / "question_bank.json"
    csv_path = ROOT / "question_bank.csv"

    # --- C4 first: JSON must be parseable by a standard parser ---
    try:
        bank = json.loads(json_path.read_text(encoding="utf-8"))
        check("C4 JSON parses with standard json.loads", True, f"{len(bank)} objects")
    except Exception as e:
        check("C4 JSON parses with standard json.loads", False, f"{type(e).__name__}: {e}")
        print_result()
        return 1

    REQUIRED = ["question_id", "type", "stem", "options", "answer",
                "explanation", "knowledge_point", "difficulty"]

    # --- C1: 30 questions, correct type mix ---
    check("C1 total is 30", len(bank) == 30, f"total={len(bank)}")
    types = Counter(q.get("type") for q in bank)
    expected = {"single_choice": 8, "multiple_choice": 6, "true_false": 4, "scenario": 12}
    check("C1 type mix 8/6/4/12", all(types.get(k) == v for k, v in expected.items()),
          ", ".join(f"{k}={types.get(k,0)}" for k in expected))
    ids = [q.get("question_id") for q in bank]
    check("C1 question ids unique", len(set(ids)) == len(ids), f"{len(set(ids))} unique")
    check("C1 difficulty split 12/12/6",
          Counter(q.get("difficulty") for q in bank) == {"easy": 12, "medium": 12, "hard": 6},
          str(dict(Counter(q.get("difficulty") for q in bank))))

    # --- C2: >=6 review/QA scenarios, each with fictional material ---
    scenarios = [q for q in bank if q.get("type") == "scenario"]
    review_cats = {"bank_review", "extraction_review"}
    review_qa = [q for q in scenarios if q.get("scenario_category") in review_cats]
    check("C2 review+QA scenarios >= 6", len(review_qa) >= 6,
          f"count={len(review_qa)} ids={','.join(q['question_id'] for q in review_qa)}")
    check("C2 both subcategories present",
          {"bank_review", "extraction_review"} <= {q.get("scenario_category") for q in review_qa},
          str(dict(Counter(q.get("scenario_category") for q in review_qa))))
    check("C2 every scenario has non-empty fictional material",
          all(isinstance(q.get("source_material"), str) and len(q["source_material"].strip()) >= 30
              for q in scenarios),
          f"{sum(1 for q in scenarios if len(str(q.get('source_material','')).strip())>=30)}/{len(scenarios)}")
    check("C2 review/QA materials mention fictional markers",
          all(("虚构" in q["source_material"]) for q in review_qa),
          f"{sum(1 for q in review_qa if '虚构' in q['source_material'])}/{len(review_qa)}")

    # --- C3: every question has answer + explanation + knowledge_point ---
    for field in ("answer", "explanation", "knowledge_point"):
        bad = [q["question_id"] for q in bank if not str(q.get(field, "")).strip()]
        check(f"C3 every question has {field}", not bad, f"missing={bad}")
    # Real SOP anchor: a 《...（虚构 v1.0）》 citation must be present, and at
    # least two distinct wrong options must be name-checked (not a single word).
    sop_anchor = re.compile(r"《[^》]*虚构[^》]*》")
    anchored = [q["question_id"] for q in bank if sop_anchor.search(q["explanation"])]
    check("C3 every explanation cites a fictional SOP", len(anchored) == len(bank),
          f"anchored={len(anchored)}/{len(bank)}")
    # Each WRONG option must be name-checked as wrong (group mentions such as
    # "A、B、D 错" count for all three). True/false has one wrong option only.
    def refuted_wrong_options(q: dict) -> set[str]:
        text = q["explanation"]
        refuted = set()
        # grouped pattern: "A、B、D 错" / "A、C 均为..." (wrong group)
        for m in re.finditer(r"((?:[A-D][、,，]?)+)\s*(?:错|均为|均属|不正确|不构成|不能)", text):
            refuted |= set(re.findall(r"[A-D]", m.group(1)))
        # single pattern: "C 错："
        for m in re.finditer(r"(?<![A-Za-z0-9])([A-D])(?![A-Za-z0-9])\s*(?:错|不正确)", text):
            refuted.add(m.group(1))
        return refuted

    poor = []
    for q in bank:
        opts = {o["key"] for o in q["options"]}
        correct = set(k.strip() for k in q["answer"].split(","))
        wrong = opts - correct
        if wrong and not wrong <= refuted_wrong_options(q):
            poor.append(f"{q['question_id']}:{sorted(wrong - refuted_wrong_options(q))}")
    check("C3 each explanation refutes every wrong option", not poor,
          f"poor={poor}")
    check("C3 knowledge points cover required topics",
          { "入场质量标准", "可见范围判定", "敏感信息识别", "过期复核",
            "SOP修订判定", "题库审定", "萃取复核" } <= {q["knowledge_point"] for q in bank},
          str(sorted({q["knowledge_point"] for q in bank})))

    # --- answer validity (guards against bogus keys) ---
    def valid_answer(q: dict) -> bool:
        keys = [o["key"] for o in q["options"]]
        ans = q["answer"]
        if q["type"] == "multiple_choice":
            parts = [p.strip() for p in ans.split(",")]
            return len(parts) >= 2 and all(p in keys for p in parts) and len(set(parts)) == len(parts)
        return ans in keys and len(ans) == 1

    bad_ans = [q["question_id"] for q in bank if not valid_answer(q)]
    check("answer keys all reference real options", not bad_ans, f"invalid={bad_ans}")
    # ANTI-FALSE-GREEN: compare delivered answers to the independent human key.
    wrong = [q["question_id"] for q in bank
             if ORACLE.get(q["question_id"]) != q["answer"]]
    check("answers match independent human oracle", not wrong, f"wrong={wrong}")
    # Distribution guard: no position shortcut (the review found 22/30 = 'B').
    single_ans = [q["answer"] for q in bank if q["type"] == "single_choice"]
    scenario_ans = [q["answer"] for q in bank if q["type"] == "scenario"]
    check("single-choice answers not concentrated (each key <= 3)",
          max(Counter(single_ans).values()) <= 3, str(dict(Counter(single_ans))))
    check("scenario answers spread across >=3 keys",
          len(set(scenario_ans)) >= 3, str(dict(Counter(scenario_ans))))
    # Length guard: 'pick the longest option' must not be a viable shortcut.
    # Random baseline for 4 options is ~25%; tolerate up to 40%.
    strict_longest = []
    scored = []
    for q in bank:
        if q["type"] == "true_false":
            continue
        scored.append(q)
        lens = {o["key"]: len(o["text"]) for o in q["options"]}
        correct = [p.strip() for p in q["answer"].split(",")]
        clen = max(lens[k] for k in correct)
        wrong = [lens[o["key"]] for o in q["options"] if o["key"] not in correct]
        if wrong and clen > max(wrong):
            strict_longest.append(q["question_id"])
    ratio = len(strict_longest) / len(scored) if scored else 1
    check("correct option not systematically the longest (<=40%)", ratio <= 0.40,
          f"strict_longest={len(strict_longest)}/{len(scored)} ({ratio:.0%}) ids={strict_longest}")
    no_shortcut = [q["question_id"] for q in bank
                   if any("以上都" in o["text"] for o in q["options"])]
    check("no 'all of the above' shortcut options", not no_shortcut, f"found={no_shortcut}")
    uniq_text = [q["question_id"] for q in bank
                 if len({o["text"] for o in q["options"]}) != len(q["options"])]
    check("option texts distinct within each question", not uniq_text, f"dup={uniq_text}")

    # --- C4 continued: CSV round-trip equality on the 8 required fields ---
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        csv_rows = list(csv.DictReader(f))
    check("C4 CSV row count 30", len(csv_rows) == 30, f"rows={len(csv_rows)}")
    check("C4 CSV has 8 required columns",
          all(c in csv_rows[0] for c in REQUIRED), str(list(csv_rows[0].keys())))
    mismatches = []
    for j, (jrow, crow) in enumerate(zip(bank, csv_rows)):
        for k in REQUIRED:
            jv = jrow[k]
            cv = crow[k]
            if k == "options":
                cv = json.loads(cv)  # canonical JSON literal in CSV cell
            if jv != cv:
                mismatches.append(f"{jrow['question_id']}.{k}")
                break
    check("C4 CSV round-trip matches JSON on 8 fields", not mismatches,
          f"mismatch={mismatches[:5]}")

    # --- confidentiality (real scans across ALL delivered text files) ---
    # Scan delivered artifacts (exclude .py source so this scanner's own
    # detection literals do not count as content leaks).
    content_blobs = []
    for f in sorted(ROOT.rglob("*")):
        if f.is_file() and f.suffix.lower() in {".md", ".json", ".csv", ".txt"}:
            content_blobs.append(f.read_text(encoding="utf-8", errors="replace"))
    content = "\n".join(content_blobs)
    check("no client/platform name in delivered artifacts",
          not any(x in content for x in ("clawhunt.store", "daoye", "Michaelyi07")))
    check("no absolute local path in delivered artifacts",
          re.search(r"[A-Za-z]:[\\/](Users|WorkBuddyProjects|tmp)", content) is None)
    check("no token literal in delivered artifacts",
          re.search(r"(ghp_|github_pat_|sk-[A-Za-z0-9]{16})", content) is None)

    print_result()
    return 0 if all(o for _, o, _ in results) else 1


def print_result() -> None:
    ok = all(o for _, o, _ in results)
    print(f"\nRESULT total={len(results)} passed={sum(o for _,o,_ in results)} all_pass={ok}")


if __name__ == "__main__":
    sys.exit(main())
