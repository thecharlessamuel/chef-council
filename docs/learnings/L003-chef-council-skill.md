---
id: L003
date: 2026-11-19
spec: docs/specs/archive/S003-chef-council-skill.md
pr: 22
merged: 2026-11-19
status: active
counts: {decisions: 0, lessons: 0, patterns: 1, surprises: 1}
supersedes: []
---

# Chef-council skill: rehearse the fresh verifier in leg 1, and say how a unit conversion is cited

## Patterns

### Rehearse every fresh-reader gate in leg 1, on the exact bytes the spec gives

- **When to use:** A spec gives text byte for byte, forbids editing it after
  a failed independent check (S003 decision 21), and gates it on a fresh
  reader that the cross-examination cannot stand in for. S003's leg 1
  rehearsed its behavior checks with fresh subagents on the given files, and
  all five passed on their first run in leg 2, as did the four the review ran
  again. It rehearsed `safetycheck` only against placeholder reports and never
  ran a real citation verifier, and the cross-examiner could not open web
  pages (round 2 and the PR review's cross-examination say so). The first
  real verifier therefore ran in leg 2: it failed one unsourced prose
  sentence, which cost a stop, a spec revision, and a second approval. The
  second failed row R6, which shipped under a waived gate.
- **Changes:** Leg 1 of such a spec runs the reader itself on the final draft
  before approval (a fresh subagent briefed exactly as the gate briefs it) and
  records the result beside the behavior-check rehearsal, so a failure is a
  draft edit, not a leg-2 stop.
- **Source:** archived S003, `### Behavior checks` (last paragraph), the
  baseline paragraph of `## Build plan — agent loop`, `## Cross-examination`
  round 2, and `## Revision record`; commits `ded8c7c`, `56a3143`, and
  `c4a4a96`; PR 22 body, Deviations 1;
  [review](https://github.com/thecharlessamuel/chef-council/pull/22#issuecomment-6996259955),
  Evidence (behavior) and Cross-examination.

## Surprises

### Two fresh verifiers judged the same unit conversion opposite ways

- **Impact:** Row R6 of `references/food-safety.md` gives 165°F (74°C) for
  heated cheese made from unpasteurized milk. Its cited page gives only 165°F
  on that line, though it pairs 165°F with 74°C for other foods. R6 was the
  same text in both approved drafts. The first verifier supported all 32
  pairs, R6 included. The second failed R6, so definition-of-done item 3
  shipped red (35 of 36 pairs supported) after the maintainer accepted it as
  a deviation. Two rules collide here: the ticket asks for °F with °C, and
  verification step 3 supports a number only when the source gives it. The
  spec never said which one governs a conversion the source does not print.
  One verifier run is a sample, not a verdict, on a rule the spec leaves open.
- **Changes:** A spec that writes sourced numbers in two units states, in the
  row format and in the verifier's steps, how a conversion the source does
  not print is written and judged: marked as a conversion and exempt from the
  number match, or left out. The next spec that touches
  `references/food-safety.md` settles row R6 that way before its verifier
  runs.
- **Source:** archived S003, `## Revision record` (the first verifier's
  result) and row R6 of the food-safety reference under `## File contents`;
  commit `5839096`;
  PR 22 body, Deviations 1 and Merge Danger;
  [review](https://github.com/thecharlessamuel/chef-council/pull/22#issuecomment-6996259955),
  acknowledged deviation 1 and cross-examination finding 1.
