---
id: L006
date: 2026-11-19
spec: docs/specs/archive/S006-example-recipes.md
pr: 28
merged: 2026-11-19
status: active
counts: {decisions: 0, lessons: 2, patterns: 0, surprises: 1}
supersedes: []
---

# Example recipes: a gate setup that needs one shell, a design appendix older than the rules, and a passing report that misstates its check

## Lessons

### Every spec's gate setup assumes one shell, and the harness starts a new one for each command

- **Context:** S001 to S006 each say to run the gate commands "in one Bash
  shell" in which the setup ran first, and each setup names its scratch files
  with `$(mktemp)`. Claude Code's shell tool keeps no variables or functions
  from one command to the next. Two executors worked around it and flagged
  it: PR 24 rebuilt the shell from a setup file for every command with `OUT`
  at a fixed scratch path, and PR 28 sourced a setup file before each gate
  command with `OUT`, `REPLY1`, and `REPLY2` at fixed paths. Re-running the
  setup as written gives each command a new, empty file. A gate that expects
  content in it (`tail -1 "$OUT"` printing `OK`) then fails loudly, but a
  gate that expects no hit passes silently: `namecheck` prints nothing and
  returns 0 on an empty file, as the harvest confirmed, so S006's check of
  the editor's saved reply would have checked nothing. The same run found
  that the harness hands back a subagent's reply with every line indented by
  two spaces, where the spec said to save it "exactly as returned"; the
  executor removed the indentation and flagged it, and the review accepted
  it as a note.
- **Changes:** Leg 1 writes a spec's gate setup as a file that each gate
  command sources, gives every file a later command reads a fixed path in
  place of `$(mktemp)`, and says what harness framing the executor removes
  when it saves a subagent's reply.
- **Source:** archived S006, `## Build plan — agent loop` (lines 613 to 625)
  and `### The editor run` (line 595); PR 28 body, deviations 1 and 2;
  [review](https://github.com/thecharlessamuel/chef-council/pull/28#issuecomment-7000398887),
  acknowledged deviations and cross-examination findings 2 and 3; PR 24 body,
  Deviations.

### The design appendix that ticket T012 called exact was older than the rules it had to meet

- **Context:** T012 names the design report's Appendix B as "the exact
  scrubs and rewrites" for the two cards. In three places it contradicted
  rules shipped after it: it gave the tuna melt `cooked-once` with no cook
  log, which `method/status-and-versions.md` does not allow (decision 6); it
  softened a brand claim into a statement that is still a product fact with
  no source read, and it kept a comparison of two kinds of tuna and a claim
  about what tuna and mayo are made of (decision 8); and its tuna melt Source line listed kinds of lens that are
  not seated names (decision 9). It also left four scrubs undone on the
  carrots, among them a sentence pointing to a card that is not published
  here and a Storage link to a private file (decision 10). Leg 1 found most
  of these by checking each edit against the shipped rules, cross-examination
  finding 6 found the composition claim, and the evidence value took a
  question to the cook. T014 builds the README from Appendix A of the same
  report, and its ticket names only the T002 and T003 overrides.
- **Changes:** A spec that takes text from the design report (T014's README
  from Appendix A first) checks each passage against every rule shipped
  since the report, not only the overrides its ticket names: the status and
  evidence values, the `<Name>-style lens` form, S006 decision 8's test for
  an unsourced claim, the private-predecessor phrase, and links to files
  that are not public.
- **Source:** archived S006, decisions 6, 8, 9, and 10 (lines 192 to 269)
  and `## Cross-examination` findings 3 and 6; ticket T012,
  `## Evidence and constraints`; ticket T014, `## Question` and
  `## Evidence and constraints`.

## Surprises

### A passing report with no discrepancies misstates its own check, and it ships as the public example

- **Impact:** The tuna melt's report reads `VERDICT: PASS` with `None.` under
  Discrepancies, and the verdict stands. But the review found three
  statements in it that do not match the files: it says four Failure modes
  rows had a blank Problem cell, where the approved text has three; it says
  the card states that nobody reviewed, approved, endorsed, or wrote it,
  where the card is silent on that; and it says only punctuation, italics,
  and the step-name form changed in the Method, where step 10 also gained a
  word. `reportcheck` checks the report's form, and cross-examination
  finding 14 removed the orchestrator's reading of the report so that the
  verdict is not judged twice, so only the PR review read the prose. A
  report is never edited (decision 14), so the three statements stay in the
  repository's public example of an editor check. T014 seeds its behavior
  checks from the example cards, and T015's stranger records every mismatch
  it finds for its PR to fix.
- **Changes:** The specs for T014 and T015 treat the tuna melt report's
  three statements as known and say how they are handled (a note where the
  report is pointed to, or a new report when the card next changes), and a
  spec that publishes an editor report as an example has leg 1's rehearsal
  or the review check the report's statements of fact against the card and
  the packet, apart from the verdict.
- **Source:** `qc/sandwiches/council-tuna-melt/2026-11-19.md`, lines 27, 30,
  and 33; archived S006, `## File contents` (approved text, lines 1290 and
  1305 to 1310; card, line 1450) and `## Cross-examination` finding 14;
  [review](https://github.com/thecharlessamuel/chef-council/pull/28#issuecomment-7000398887),
  cross-examination finding 1 and non-blocking notes 1 and 2.
