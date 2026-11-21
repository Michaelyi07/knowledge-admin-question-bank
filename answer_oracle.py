"""Independently human-reviewed answer key (the anti-false-green oracle).

This file is a SEPARATE, human-verified record of the correct answer to each
question after the option-position rebalance. tools/validate.py compares the
delivered bank against this oracle: changing any answer in the bank (even to
another syntactically valid key) makes validation FAIL. This closes the
"answer wrong but all checks green" false-green gap found in independent review.

Answers were verified by reading each stem + source material against the
fictional SOP rules in the explanations. Rebalance only permuted option
positions; semantics are unchanged from questions_data.py / scenarios_data.py.
"""
from __future__ import annotations

# question_id -> correct answer after rebalance (multi-choice keys sorted).
ANSWERS: dict[str, str] = {
    # single choice (8) — original all B, permuted A/B/C/D
    "Q001": "A", "Q002": "B", "Q003": "C", "Q004": "D",
    "Q005": "A", "Q006": "B", "Q007": "C", "Q008": "D",
    # multiple choice (6)
    "Q009": "A,B,D", "Q010": "A,C,D", "Q011": "B,C,D",
    "Q012": "A,B,C", "Q013": "A,B,D", "Q014": "B,C,D",
    # true / false (4)
    "Q015": "B", "Q016": "B", "Q017": "A", "Q018": "B",
    # scenarios (12) — 3 each of A/B/C/D
    "Q019": "B", "Q020": "C", "Q021": "A", "Q022": "D",
    "Q023": "C", "Q024": "A", "Q025": "C", "Q026": "B",
    "Q027": "D", "Q028": "A", "Q029": "D", "Q030": "B",
}
