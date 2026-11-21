# Real verification record — #3186 knowledge administrator question bank

Commands below were actually executed with the captured interpreter. Outputs are verbatim; local home/repo paths anonymized. No database or external service is required by this ticket (Dependencies: None).

## Environment (captured)

```
captured_at_utc: 2026-11-21T14:00:59.906704+00:00
platform: Windows-10-10.0.19045-SP0
python_executable: <python 3.13.14>  # path withheld
csv_module: stdlib csv (QUOTE_ALL)
json_module: stdlib json (json.loads strict parse)
```

## Commands run (verbatim output)

```
$ python tools/build_bank.py
BUILT json=37736B csv=28530B rows=30
```

```
$ python tools/build_materials.py
MATERIALS_WRITTEN 4563B scenarios=12
```

```
$ python tools/validate.py
PASS C4 JSON parses with standard json.loads | 30 objects
PASS C1 total is 30 | total=30
PASS C1 type mix 8/6/4/12 | single_choice=8, multiple_choice=6, true_false=4, scenario=12
PASS C1 question ids unique | 30 unique
PASS C1 difficulty split 12/12/6 | {'easy': 12, 'medium': 12, 'hard': 6}
PASS C2 review+QA scenarios >= 6 | count=6 ids=Q025,Q026,Q027,Q028,Q029,Q030
PASS C2 both subcategories present | {'bank_review': 3, 'extraction_review': 3}
PASS C2 every scenario has non-empty fictional material | 12/12
PASS C2 review/QA materials mention fictional markers | 6/6
PASS C3 every question has answer | missing=[]
PASS C3 every question has explanation | missing=[]
PASS C3 every question has knowledge_point | missing=[]
PASS C3 every explanation cites a fictional SOP | anchored=30/30
PASS C3 each explanation refutes every wrong option | poor=[]
PASS C3 knowledge points cover required topics | ['SOP修订判定', '入场质量标准', '可见范围判定', '敏感信息识别', '萃取复核', '过期复核', '题库审定']
PASS answer keys all reference real options | invalid=[]
PASS answers match independent human oracle | wrong=[]
PASS single-choice answers not concentrated (each key <= 3) | {'A': 2, 'B': 2, 'C': 2, 'D': 2}
PASS scenario answers spread across >=3 keys | {'B': 3, 'C': 3, 'A': 3, 'D': 3}
PASS correct option not systematically the longest (<=40%) | strict_longest=7/26 (27%) ids=['Q020', 'Q021', 'Q025', 'Q026', 'Q028', 'Q029', 'Q030']
PASS no 'all of the above' shortcut options | found=[]
PASS option texts distinct within each question | dup=[]
PASS C4 CSV row count 30 | rows=30
PASS C4 CSV has 8 required columns | ['question_id', 'type', 'stem', 'options', 'answer', 'explanation', 'knowledge_point', 'difficulty', 'scenario_category', 'source_material']
PASS C4 CSV round-trip matches JSON on 8 fields | mismatch=[]
PASS no client/platform name in delivered artifacts
PASS no absolute local path in delivered artifacts
PASS no token literal in delivered artifacts

RESULT total=28 passed=28 all_pass=True
```

## Acceptance criteria result

| AC | Result |
|---|---|
| C1 — 30 questions, type mix 8/6/4/12 | PASS |
| C2 — >=6 bank-review/extraction-QA scenarios with fictional material | PASS |
| C3 — every question has answer + explanation + knowledge_point | PASS |
| C4 — JSON parseable by standard parser (plus CSV round-trip) | PASS |
