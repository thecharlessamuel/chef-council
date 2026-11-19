---
id: L010
date: 2026-11-19
spec: docs/specs/archive/S010-name-free-agent-agnostic.md
pr: 36
merged: 2026-11-19
status: active
counts: {decisions: 0, lessons: 1, patterns: 1, surprises: 1}
supersedes: []
---

# Name-free lenses: a redaction spec that held what it removed, a placeholder that left people describable, and a cross-examination that could not show it had read

## Lessons

### The spec that said it held none of the names it removes held one in its own redaction rules

- **Context:** S010's Goal says the spec holds none of the names it removes,
  and its gates proved the tree clean with the names check. The check cannot
  see some kinds of name (decision 12), so decision 14 handled those with
  hand-written rules at the front of the redact helper (`FIRST_RULES`). Two
  of them matched by the text they removed: one spelled a publisher's cooking
  section in full, and the other kept a biographical sentence about one
  person with only the name wildcarded. A rule that matches by content
  carries the content. The names check passed both, because they were the
  very blind spots the rules were written for, and neither the spec's
  cross-examination nor the first review's raised them. The first review's
  own read of the spec found them. That cost a kickback, an executor
  session, and a second review for an edit to the spec alone, with no
  delivered file changed; the fix matched each rule by the text around the
  removed span. The evidence leaked the same way on GitHub: the PR body's
  kickback evidence used a fragment of the removed sentence as a search
  term, and the first review described the sentence in more detail. Neither
  names anyone, and both stay unless the maintainer edits them.
- **Changes:** A spec that removes text writes each hand rule, for what its
  check cannot see, to match by the surrounding text and never by the
  removed text. Before approval, leg 1 searches the spec itself, helpers
  included, with a search wider than the gate: the second review's search,
  which took every word of four letters or more from the removed terms, and
  every multi-word term with its punctuation ignored, in any letter case.
  The spec, the PR body, and the review point at a removed string by file
  and line, and never quote any part of it.
- **Source:** archived S010, the Goal's second paragraph, decisions 12 and
  14, and `#### Helper: redact` (`FIRST_RULES`, lines 812 to 820); commit
  `a1b7a56`; PR 36 body, Evidence (Kickback 1) and Deviations;
  [first review](https://github.com/thecharlessamuel/chef-council/pull/36#issuecomment-7018966150),
  finding 1 and its Cross-examination section (the paragraph after finding 8);
  [second review](https://github.com/thecharlessamuel/chef-council/pull/36#issuecomment-7019776261),
  Spec/Correctness (the wider search) and note 2.

## Patterns

### Ask the cross-examiner coverage questions, so an empty reply can be told from an unread dossier

- **When to use:** Any cross-examination on a large dossier. The profile
  requires the dossier to hold the complete bounded evidence, and S010's
  spec dossier held 74 files. In the second review of PR 36, the first
  cross-examination run returned no findings and nothing to show how much
  of the dossier it had read. The reviewer ran it again with five coverage
  questions about both ends of the dossier. Every answer was right, and that
  run returned three findings, two of them accepted as notes, among them
  the gap in the profile's new model rule.
- **Changes:** Leg 1 and the PR review put coverage questions about the
  first and the last files of the dossier into every cross-examination
  brief, and treat a reply whose answers are missing or wrong as a run that
  did not happen, not as a clean result.
- **Source:**
  [second review](https://github.com/thecharlessamuel/chef-council/pull/36#issuecomment-7019776261),
  Cross-examination ("Two runs"); archived S010, `## Cross-examination`
  (the 74-file dossier); `.agents/spec-profile.md`, `## Independent review`
  (the dossier holds the complete bounded evidence).

## Surprises

### Replacing a name with `[name removed]` left people describable beside the placeholder

- **Impact:** Decision 14's helper replaced each name, title, and link and
  kept every word around it. Archived S002 (decisions 6 and 7, and its
  per-lens tables) and archived S008 (its copy of the deleted reading list)
  therefore still hold gendered pronouns, a role at a publisher, publication
  years, and edition facts beside `[name removed]`, some of it under a
  present lens name, so the archives still pair lenses with unnamed people.
  Decision 1 accepted that a reader may guess who inspired a lens from its
  descriptor; this second channel is one it did not weigh. Both reviews
  raised it as non-blocking, because the files match their approved hashes,
  and the second asked for the maintainer's decision before the repository
  goes public. The same rule also cut seven plurals in archived S002 to
  `lens]es`.
- **Changes:** A spec that removes a person's name from text redacts the
  unit that describes the person (the sentence, the table row, or the list
  entry), or lists the context it keeps and says why. The next spec that
  touches archived S002 or S008, such as the follow-up redaction the second
  review proposes, does this there and repairs the seven `lens]es` plurals.
- **Source:** archived S010, decisions 1 and 14; archived S002 and archived
  S008;
  [first review](https://github.com/thecharlessamuel/chef-council/pull/36#issuecomment-7018966150),
  the first non-blocking note and cross-examination findings 4 and 5;
  [second review](https://github.com/thecharlessamuel/chef-council/pull/36#issuecomment-7019776261),
  notes 1 and 5.
