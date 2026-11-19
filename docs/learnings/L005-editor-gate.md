---
id: L005
date: 2026-11-19
spec: docs/specs/archive/S005-editor-gate.md
pr: 26
merged: 2026-11-19
status: active
counts: {decisions: 0, lessons: 0, patterns: 0, surprises: 2}
supersedes: []
---

# Editor gate: a locale hole in the fail-closed gate, and a card hash that line endings change

## Surprises

### In a UTF-8 locale the gate skips a card whose name holds an invalid byte, and exits 0

- **Impact:** `scripts/check-qc.sh` picks out cards with a bash regular
  expression (line 188, `[[ "$path" =~ ^recipes/([^/]+)/([^/]+)\.md$ ]]`). In
  a UTF-8 locale, `[^/]` does not match a byte that is not valid UTF-8, so a
  card whose name holds one is never counted: the gate prints
  `qc checked: 0` and exits 0. With `LC_ALL=C` the same repository exits 1.
  The review reproduced this, and so did the harvest, in a scratch
  repository. It breaks decision 8's rule that the script exits 0 only when
  every changed card passed, in the `editor gate` CI job, a bare run, and the
  Stop hook. CI still fails such a card, but only because the name rule in
  `scripts/lint-cards.py` rejects it in the `tests` job. The script already
  sets `LC_ALL=C` for its `sort` (line 134), but not for the match. Leg 1's
  83-mutant probe, the tests (whose accented name is valid UTF-8), and the
  spec's 17-finding cross-examination all missed it. The review found it by
  feeding the script a name, not by changing the code.
- **Changes:** A spec that gives a shell script which picks out files by
  matching their paths sets `LC_ALL=C` before the match and tests a path
  holding a byte that is not valid UTF-8, and the next spec that edits
  `scripts/check-qc.sh` does both there.
- **Source:**
  [review](https://github.com/thecharlessamuel/chef-council/pull/26#issuecomment-6999092694),
  Spec/Correctness note 1; archived S005, decision 8 and the mutation-probe
  paragraph of `## Build plan — agent loop`; `scripts/check-qc.sh`, lines 134
  and 188; `tests/test_check_qc.py`,
  `test_card_with_a_space_and_an_accent_in_its_name_is_checked`.

### A card hash taken from the working file can differ from the one CI takes

- **Impact:** CI's gate hashes the committed bytes (decision 7). But
  `scripts/check-qc.sh --hash` hashes the file as it stands, and so does
  `--working-tree`, which the Stop hook runs. The report format tells the
  editor to run `--hash` (line 57), and `method/recipe-qc.md` tells a chat
  user to run it (line 40). With `core.autocrlf=true`, a card that has CRLF
  line endings in the working tree is committed with LF. A report written
  exactly as the report format says then carries a hash that CI rejects. The
  harvest reproduced this in a scratch repository. The Stop hook's mode
  printed `qc checked: 1` and exited 0, and the default mode on the commit
  printed the stale-hash line and exited 1. The gate fails closed, but the
  local check and CI disagree, and nothing tells the cook why. Decision 7
  records the difference. The method page, the report format, and the tests
  do not, and the repository has no `.gitattributes`.
- **Changes:** Before a spec tells a cook or an editor to hash a card
  (T013's chat path and T014's README among them), or edits the gate, the
  report format, or `method/recipe-qc.md`, it settles which bytes are hashed
  on a checkout that converts line endings (for example by a `.gitattributes`
  rule for `recipes/`, or by `--hash` hashing the bytes git would commit) and
  tests that case.
- **Source:**
  [review](https://github.com/thecharlessamuel/chef-council/pull/26#issuecomment-6999092694),
  Spec/Correctness note 2; archived S005, decision 7;
  `.agents/skills/recipe-editor/references/report-format.md`, line 57;
  `method/recipe-qc.md`, line 40.
