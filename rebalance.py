"""Rebalance option positions so correct answers are not predictable.

Teaching-material quality: the drafted bank had 22/30 answers = 'B' and all six
multi-choice answers = 'A,B,C', which lets a learner guess by position. This
module applies a per-question permutation to OPTION POSITIONS ONLY; the question
content, option texts, answer semantics and explanations stay identical. The
explanation's option-letter references are remapped with the same permutation.

Permutation semantics: perm[old_key] = new_key (where the old option now sits).
"""
from __future__ import annotations

import re

PERM: dict[str, dict[str, str]] = {
    # single choice (original answer B -> target A/B/C/D twice each)
    "Q001": {"A": "B", "B": "A", "C": "C", "D": "D"},
    "Q002": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q003": {"A": "A", "B": "C", "C": "B", "D": "D"},
    "Q004": {"A": "A", "B": "D", "C": "C", "D": "B"},
    "Q005": {"A": "B", "B": "A", "C": "C", "D": "D"},
    "Q006": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q007": {"A": "A", "B": "C", "C": "B", "D": "D"},
    "Q008": {"A": "A", "B": "D", "C": "C", "D": "B"},
    # multiple choice (original A,B,C -> varied target sets)
    "Q009": {"A": "A", "B": "B", "C": "D", "D": "C"},
    "Q010": {"A": "A", "B": "C", "C": "D", "D": "B"},
    "Q011": {"A": "D", "B": "B", "C": "C", "D": "A"},
    "Q012": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q013": {"A": "A", "B": "B", "C": "D", "D": "C"},
    "Q014": {"A": "D", "B": "B", "C": "C", "D": "A"},
    # true/false (unchanged)
    "Q015": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q016": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q017": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q018": {"A": "A", "B": "B", "C": "C", "D": "D"},
    # scenarios (11xB -> 3 each of A/B/C/D)
    "Q019": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q020": {"A": "A", "B": "C", "C": "B", "D": "D"},
    "Q021": {"A": "B", "B": "A", "C": "C", "D": "D"},
    "Q022": {"A": "A", "B": "D", "C": "C", "D": "B"},
    "Q023": {"A": "A", "B": "C", "C": "B", "D": "D"},
    "Q024": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q025": {"A": "A", "B": "C", "C": "B", "D": "D"},
    "Q026": {"A": "A", "B": "B", "C": "C", "D": "D"},
    "Q027": {"A": "A", "B": "D", "C": "C", "D": "B"},
    "Q028": {"A": "B", "B": "A", "C": "C", "D": "D"},
    "Q029": {"A": "A", "B": "D", "C": "C", "D": "B"},
    "Q030": {"A": "A", "B": "B", "C": "C", "D": "D"},
}
_LETTER = re.compile(r"(?<![A-Za-z0-9])([A-D])(?![A-Za-z0-9])")


def rebalance(questions: list[dict]) -> list[dict]:
    """Return a new list with permuted option positions and remapped references."""
    out = []
    for q in questions:
        perm = PERM.get(q["question_id"], {})
        if not perm:
            out.append(q)
            continue
        by_key = {o["key"]: o for o in q["options"]}
        # Only permute keys that actually exist in this question (true/false has A/B only).
        active = {old: perm[old] for old in by_key if old in perm}
        inv = {new: old for old, new in active.items()}
        new_options = [dict(by_key[inv[new_key]], key=new_key)
                       for new_key in ("A", "B", "C", "D") if new_key in inv]
        # answer may be a single key or a comma list (multi-choice)
        parts = [p.strip() for p in q["answer"].split(",")]
        new_answer = ",".join(sorted({perm.get(p, p) for p in parts}))
        new_expl = _LETTER.sub(lambda m: perm.get(m.group(1), m.group(1)), q["explanation"])
        new_q = dict(q)
        new_q["options"] = new_options
        new_q["answer"] = new_answer
        new_q["explanation"] = new_expl
        out.append(new_q)
    return out
