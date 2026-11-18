---
id: L002
date: 2026-11-18
spec: docs/specs/archive/S002-council-roster-and-vetting.md
pr: 20
merged: 2026-11-18
status: active
counts: {decisions: 0, lessons: 1, patterns: 1, surprises: 1}
supersedes: []
---

# Council roster and vetting: open source rules, text gates before the reader, and names in verifier output

## Lessons

### The authorship test for independence left three kinds of page to each reader, and the readers differed

- **Context:** S002 defined an independent source by who wrote the content
  (decision 9) and let the person's own page, else the publisher's, stand for
  a published work (`### Writing a record`, step 2). Three kinds of page fell
  between those rules. Interviews mostly in the subject's own words were cited
  as independent and failed verification in Tasks 5 and 7; in Task 6 one
  fresh verifier accepted a reader's newsletter as independent and the next
  rejected it; and the review found that verifiers judged interview-derived
  pages slightly differently. Low-reach outlets (a reader's newsletter, a
  student newspaper, a reader-review site, a librarian's blog) passed because
  the test counts authorship, not reach, and one seated record's only
  independent sources are two posts of the same newsletter. Where a
  publisher's page would not load, bookseller and aggregator pages stood in
  for a published work in three records; the review accepted that and asked a
  later spec to say which reading of step 2 it means.
- **Changes:** The next spec that writes or changes how a lens is vetted (a
  record refresh, a new name, or a skill that vets a name on request) states
  whether an interview counts as independent and by what test, whether reach
  matters, whether two posts from one outlet count as one source, and whether
  a bookseller or aggregator page may stand for a published work.
- **Source:** PR 20 body, run history (Tasks 5, 6, and 7) and flagged
  deviations 3 and 7;
  [review](https://github.com/thecharlessamuel/chef-council/pull/20#issuecomment-6993345295),
  notes 2 and 6, acknowledged deviations 3 and 7, and cross-examination S3 to
  S5.

## Patterns

### Run every mechanical text gate before the fresh reader starts

- **When to use:** A task whose evidence includes a fresh-context reader (the
  citation verifier here; an editor check or a behavior check has the same
  shape) and also mechanical text gates whose failure forces a text edit: the
  privacy sweep's `--text`, a banned-word net, a shape check. S002's record
  task ran the verifier in its Work and the mechanical gates after it. In
  Task 5 the privacy sweep's `--text` hit an Access-notes line after the
  verifier had passed, the reworded records passed the gate on the old report
  (flagged deviation 1), and the review had to start a fresh verifier to
  close the gap. In Task 9 a `lenscheck` banned-word failure sent the reworded
  pair to a fresh verifier.
- **Changes:** A spec with such a task orders it as draft, then every
  mechanical text gate, then the fresh reader, and says that any edit after
  the reader starts needs a new reader.
- **Source:** S002 `### The record task` (Work and Gate); PR 20 body, run
  history (Tasks 5 and 9) and flagged deviation 1;
  [review](https://github.com/thecharlessamuel/chef-council/pull/20#issuecomment-6993345295),
  acknowledged deviations 1 and 2 and cross-examination S1.

## Surprises

### The verifier's independence line put private writers' names into pull-request text

- **Impact:** S002's verifier line form is `independent <url> <who wrote or
  published the content>`, and definition-of-done item 5 put every report
  verbatim in the PR 20 body. The reports therefore name individual writers
  of small publications, among them a student newspaper's reviewer, in GitHub
  text that becomes public with the repository; the records themselves
  mostly name outlets. The review left the PR 20 body to the maintainer
  before publication. The profile's public-by-default list covers the
  maintainer's household and private sources, not third parties named as
  source authors, so no automated gate flagged it.
- **Changes:** A spec that puts an independent reader's output into GitHub
  text asks it to name the outlet and what on the page shows independence,
  not the individual writer.
- **Source:** S002 `### Citation verification`, step 2, and
  definition-of-done item 5; PR 20 body, Evidence (the seven verifier
  reports);
  [review](https://github.com/thecharlessamuel/chef-council/pull/20#issuecomment-6993345295),
  note 7.
