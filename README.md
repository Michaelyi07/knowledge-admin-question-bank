# Knowledge Administrator Question Bank (S4-TRAIN-031)

30 practice questions for knowledge administrators: visibility-scope rulings,
entry quality, sensitive-data detection, expiry review, SOP minor/major change,
question-bank review, and extraction QA.

**All content is fictional.** Entries, enterprises (星辰科技（虚构）, 云栖制造（虚构）),
people (王某某), amounts, meeting minutes, AI-generated questions and FAQ drafts
are invented. No real personal/enterprise information, no client name, no secrets.

## Deliverables

| File | Contents |
|---|---|
| `question_bank.json` | 30 questions, strict UTF-8, 8 required fields + 2 scenario-only fields |
| `question_bank.csv` | Same 30 rows, 8 required columns + 2 scenario columns, QUOTE_ALL |
| `materials/scenario_materials.md` | Fictional source material for all 12 scenario questions |
| `questions_data.py`, `scenarios_data.py` | Single source of truth (18 + 12 questions) |
| `tools/build_bank.py`, `tools/build_materials.py` | Regenerate JSON/CSV and materials |
| `rebalance.py` | Permutes option positions only (answer distribution) so answers cannot be guessed by position |
| `answer_oracle.py` | Independent human-reviewed answer key — the anti-false-green oracle |
| `tools/validate.py` | 28 real assertions over the 4 acceptance criteria + answer oracle + length guard |
| `tools/capture_evidence.py` | Captures real command output + versions to `evidence/` |
| `evidence/verification.md`, `evidence/validate_output.txt` | Real verification record |

Required fields (every question): `question_id`, `type`, `stem`, `options`,
`answer`, `explanation`, `knowledge_point`, `difficulty`.
Scenario rows additionally carry `scenario_category` and `source_material`
(the attached fictional material). `options` is a JSON array of
`{"key","text"}` objects; in CSV it is stored as a canonical JSON literal
so a round trip is lossless.

## Question mix & coverage

- **30 total**: 8 single-choice, 6 multiple-choice, 4 true/false, 12 scenario.
- **Difficulty**: 12 easy / 12 medium / 6 hard.
- **Answer distribution** (after `rebalance.py`, option positions permuted only):
  single-choice A/B/C/D = 2 each; scenario A/B/C/D = 3 each; multi-choice uses
  four distinct answer sets. Wrong options are length-balanced with the correct
  one (only 27% of items have the strictly longest correct option, ~random).
  No "always B" or "pick the longest" shortcut.
- **Knowledge points**: 入场质量标准, 可见范围判定, 敏感信息识别, 过期复核,
  SOP修订判定, 题库审定, 萃取复核.
- **Review + QA scenarios**: 6 (Q025–Q030) — 3 question-bank review,
  3 extraction re-verification — each with attached fictional source material.
- Examined rules include: three-way visibility (all members / designated role /
  named person) with over-broad settings as traps; sensitive info (financing
  plans, personal contacts, undisclosed partnerships); source-present /
  answer-unique / no-leak bank review; extraction QA spotting factual errors and
  leaks, AI output queued for review (never sent externally), AI never computes
  monetary amounts.

## Run & verify

```bash
# Regenerate artifacts from the data source (Python 3.11+, stdlib only):
python tools/build_bank.py
python tools/build_materials.py

# Validate all 4 acceptance criteria (exit 0 = all pass):
python tools/validate.py

# Refresh the verification record with real outputs:
python tools/capture_evidence.py
```

No third-party packages, no external services, no environment secrets required.

## Acceptance criteria → verification

| AC | Checked by |
|---|---|
| C1 — 30 questions, exact type mix 8/6/4/12 | `validate.py`: total, type Counter, unique ids, difficulty split |
| C2 — >=6 review/QA scenarios, each with fictional material | `validate.py`: category filter, material length, fictional markers |
| C3 — answer + explanation + knowledge point on every question | `validate.py`: non-empty fields, wrong-option reasoning, topic coverage |
| C4 — JSON parseable by standard parser | `validate.py`: `json.loads`, CSV round-trip equality on 8 fields |

`validate.py` additionally guards answer-key syntactic validity (keys reference
real options, no "all of the above" shortcut, distinct option texts), compares
every answer to the independent human-reviewed `answer_oracle.py` (so a changed
answer fails validation), requires each explanation to cite a fictional SOP and
refute every wrong option, and scans all delivered artifacts for confidentiality.
28/28 checks pass on the delivered artifacts. Tamper tests confirmed that
flipping an answer or blanking all explanations makes validation fail; the
length guard fails if the "longest correct option" pattern is systematically
re-introduced (>40% of scored items).

## Scope & boundaries

In scope: the 30-question bank in CSV + JSON, fictional materials, verification
log. Out of scope: courseware, video, third-party API costs, real records,
client naming. Dependencies: none. Revisions: 1 round included.
