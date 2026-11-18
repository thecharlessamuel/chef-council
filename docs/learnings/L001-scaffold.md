---
id: L001
date: 2026-11-18
spec: docs/specs/archive/S001-scaffold.md
pr: 18
merged: 2026-11-18
status: active
counts: {decisions: 0, lessons: 2, patterns: 0, surprises: 1}
supersedes: []
---

# Scaffold: front-matter booleans, a spliced spec, and task names as commit subjects

## Lessons

### An approved spec can carry a stale copy of its own earlier draft, and its gates will not notice

- **Context:** S001 was approved and merged with the pre-cross-examination
  Goal, Decisions, Prerequisites, Build plan, and Link check still in it,
  from the line beginning ``## File contents`, and`` to the real
  `## File contents` heading. The two build plans disagree (one test file, a
  red of `FAILED (failures=15)`, and the secret scan in Task 5, against two
  test files, `FAILED (failures=24, errors=2)`, and the scan in Task 2). Leg 1
  re-ran every task gate after its edits and the approval followed a clean
  cross-examination, yet neither caught it, because the gates check the files
  and not the spec's own text: the `#### File:` blocks occur once, and both
  plans pin the same hashes. The executor found it and followed the first
  plan, the one the spec's `## Cross-examination` record describes; that
  first plan is the operative one when S001 is read as a prior spec.
- **Changes:** Before a spec is approved, leg 1 confirms that each `##`
  heading and each `### Task N` heading outside fenced blocks occurs exactly
  once, because re-running the gates from the spec's text cannot detect a
  duplicated plan.
- **Source:** PR 18 body, deviation 1;
  [first review](https://github.com/thecharlessamuel/chef-council/pull/18#issuecomment-6988054294)
  (acknowledged deviation 1 and cross-examination SC-1);
  [second review](https://github.com/thecharlessamuel/chef-council/pull/18#issuecomment-6988363155)
  (acknowledged deviation 1).

### Task names become commit subjects

- **Context:** `2-spec-execute` commits each task with its task name as the
  subject, so S001's noun-phrase task names became five task commit subjects
  (`Tests for the two scripts`, `Kitchen templates`, and three more) that
  break the profile's imperative-mood rule. The first review traced this to
  the spec, not the execution, and the maintainer merged them as they were.
- **Changes:** A spec names every task in the imperative mood, as a usable
  commit subject: `Add the tests for the two scripts`, not `Tests for the two
  scripts`.
- **Source:** [first review](https://github.com/thecharlessamuel/chef-council/pull/18#issuecomment-6988054294),
  non-blocking finding 1; commits `d9d7c18`, `3a1aebd`, `7055bbe`, `27f20d5`,
  `6b0d0c1`.

## Surprises

### YAML reads the kitchen templates' `no` as a boolean

- **Impact:** The kitchen templates mark a blank file with `filled_in: no`,
  and `kitchen/profile.md` answers `higher_risk_diners` with `yes` or `no`
  (`unknown` until answered). GitHub's front-matter table shows
  `filled_in: no` as `false` in all three templates, so definition-of-done
  item 5, which expected `no`, failed on bytes the spec pinned and the
  executor could not change; the maintainer accepted the render mid-run. Any
  YAML 1.1 reader does the same: a cook's `yes` becomes `true`, and
  `higher_risk_diners` becomes a mix of booleans and the string `unknown`.
  The raw text, which an agent reading the file sees, still says `no`.
- **Changes:** The first spec whose skill or script reads `filled_in` or
  `higher_risk_diners` (the first-run interview in T009 at the latest)
  settles first how they are written and read: quoted strings, `true` and
  `false`, or plain-text line matching. No spec again predicts how GitHub
  renders an unquoted YAML value it has not observed.
- **Source:** PR 18 body, deviation 4;
  [first review](https://github.com/thecharlessamuel/chef-council/pull/18#issuecomment-6988054294)
  (acknowledged deviation 4);
  [second review](https://github.com/thecharlessamuel/chef-council/pull/18#issuecomment-6988363155)
  (acknowledged deviation 4 and cross-examination SC-1).
