---
id: L004
date: 2026-11-19
spec: docs/specs/archive/S004-codify-and-cook-log.md
pr: 24
merged: 2026-11-19
status: active
counts: {decisions: 0, lessons: 3, patterns: 1, surprises: 0}
supersedes: []
---

# Codify and cook log: a splice the heading check missed, one value per line, rules stated once, and a mutation probe in leg 1

## Lessons

### A spec splice came back in S004, and L001's heading check could not see it

- **Context:** S004 was approved and merged with a stale passage, lines 747
  to 859, spliced into it. Line 747 is the tail of line 614, cut where that
  line's `block` command names the heading
  ``#### Fixture: `codify-message` ``; lines 748 to
  850 repeat lines 615 to 717 exactly; and lines 852 to 859 give an older,
  one-round account of leg 1's behavior-check rehearsal that contradicts the
  three-round account at lines 719 to 745. The newer account describes the
  rounds after the cross-examination, so the splice came in with an edit made
  after the spec's one cross-examination round, as S001's did (L001). The cut
  point is what a scripted replacement produces when it finds the heading's
  text without anchoring it to a whole line. L001's check (each `##` heading
  and each `### Task N` heading occurs once) passes S004, because no whole
  heading line repeats. The gates did not notice either: `block` matches whole
  lines, so it skipped line 747. The executor disclosed the splice as a spec
  text defect, and the PR cross-examination raised it again (S2). A check that
  no paragraph of 80 or more characters outside fenced blocks occurs twice
  flags the splices in S001 and S004 and nothing in S002 or S003; a check of
  repeated lines that also reads inside fences flags the repeated helper and
  test code that every spec carries.
- **Changes:** After its last edit and before approval, leg 1 also checks
  that no paragraph of 80 or more characters outside fenced blocks occurs
  twice in the spec, alongside L001's heading check.
- **Source:** archived S004, lines 614 to 859 (`### Behavior checks`) and
  `## Cross-examination` (one round, on the first draft); PR 24 body,
  Deviations ("Spec text defect, not edited");
  [review](https://github.com/thecharlessamuel/chef-council/pull/24#issuecomment-6997491258),
  acknowledged deviations, cross-examination S2, and note 7.

### Fresh writers put more than one value on a line meant for one value

- **Context:** The `log` behavior check ran six times with fresh subagents:
  three in leg 1's rehearsal, one in leg 2, and two in the review. Two runs
  failed the same way. In leg 1's second round the writer put its own advice
  after the cook's quotation on the Next controlled change line, and leg 1
  reworded the skill and the template. In the review's first run the writer
  kept the template's gloss after the date on the Reported line
  (`YYYY-MM-DD, the day the cook reported back`), and `logcheck` failed the
  log. S004's rule of one fresh retry turned that into a pass instead of a
  stop. Leg 2's single run passed, so the review was the first to see the
  gloss copied. The template's Recipe line also ends in an alternative
  (`Or: No card yet.`).
- **Changes:** A template that a fresh writer fills holds only an example
  value on each value line, with every explanation in the instruction text the
  writer deletes. The next spec that edits `templates/cook-log.md` makes its
  Reported line a bare `YYYY-MM-DD`.
- **Source:** archived S004, `### Behavior checks` (leg 1's rehearsal
  record, lines 719 to 745); `templates/cook-log.md`, the Reported line; PR 24
  body, item 8 ("Each check passed on its first run");
  [review](https://github.com/thecharlessamuel/chef-council/pull/24#issuecomment-6997491258),
  Evidence item 8 (`log`) and note 1.

### Fixing one restated rule did not fix the others

- **Context:** The spec cross-examination found the slug rule worded three
  ways (finding 8). Leg 1 fixed it by stating the rule once, in
  `method/status-and-versions.md`, with both skills referring to it, but did
  not check the other rules that the method page, the two skills, and the
  three templates share. The PR cross-examination found more of them. The
  `cook-log` skill refers to the method page for the evidence count, then
  summarizes it and leaves out an earlier log that the current version's
  changelog names (S1). The reviewer did not treat S1 as blocking only because
  the shipped bytes were the approved spec's. The `-2` rule for a second
  packet on the same day is in the template and decision 14 but not in the
  `recipe-codify` skill (S3), and D1 named the general problem. The review's
  notes 3 and 4 add two contradictions inside a single file. The `cook-log`
  skill requires an exact quotation but also says to write a double quotation
  mark inside the cook's words as a single one. The source-packet template
  says to keep the tilde lines but also, for a new card, to delete them.
- **Changes:** A spec that puts one rule in several shipped files states it
  in full in one file and only refers to it from the others, never with a
  summary beside the reference. The next spec that edits either skill, the
  templates, or `method/status-and-versions.md` settles the review's notes 2
  to 4.
- **Source:** archived S004, `## Cross-examination` finding 8;
  `.agents/skills/cook-log/SKILL.md`, `## Card follow-up`;
  [review](https://github.com/thecharlessamuel/chef-council/pull/24#issuecomment-6997491258),
  cross-examination S1, S3, and D1, and notes 2 to 4.

## Patterns

### Probe a given script with mutants in leg 1

- **When to use:** A spec gives a script and its tests byte for byte, and the
  tests are the floor and the ceiling, so leg 2 cannot add a test. S004's 29
  tests passed, and the generator matched decision 21 on every probe the
  review made. Even so, the review found ten mutants of
  `scripts/build-index.py` that the tests do not catch. Among them: `--check`
  comparing with newline translation, a title or value not stripped, a bare
  `# ` accepted as a title, and a case-insensitive sort. The PR listed three
  more untested assertions: a followed symbolic link, a `|` in a category
  name, and an `INDEX.md` that is not UTF-8. Neither leg 2 nor the review
  could act on them. The spec cross-examination added four tests
  (finding 17), but its reviewer had no shell and did not run the code.
- **Changes:** Before approval, leg 1 of such a spec runs a mutation probe
  of its own script (a handful of one-line changes, each run against the
  tests) and, for every mutant that survives, adds a test or names the gap as
  accepted. The next spec that edits `scripts/build-index.py` or its tests
  closes the gaps that the review and the PR list.
- **Source:** archived S004, `## Cross-examination` (the reviewer's tools)
  and finding 17; PR 24 body, Test gaps;
  [review](https://github.com/thecharlessamuel/chef-council/pull/24#issuecomment-6997491258),
  cross-examination S4 and note 6.
