---
id: L008
date: 2026-11-19
spec: docs/specs/archive/S008-docs-and-behavior-checks.md
pr: 32
merged: 2026-11-19
status: active
counts: {decisions: 1, lessons: 1, patterns: 0, surprises: 0}
supersedes: []
---

# Docs and behavior checks: pages that restate other files with no check to keep them in step, and expected behavior no rule file states

## Decisions

### The new pages restate facts held in other files, and no check keeps them in step

- **Rationale:** S008 built no repository check for its five pages
  (decisions 1 and 11). Its link, anchor, path, check-format, and
  reading-list helpers ran only as spec gates, and no job in
  `.github/workflows/ci.yml` reads `README.md`, `docs/`, or `evals/`.
  Decision 20 says the pages state facts as they were at `base_sha`, and
  that a later spec that changes one of those facts changes the sentence.
  It names three: two example cards, six core lenses and eight specialists,
  and fourteen pressure-test checks. The review found more (Design/Simplicity,
  note 10). B12 and B13 pin the carrots card's 1½ tsp of jaggery and its
  v1.1 to v1.2 bump. B15 pins `untested`, and B17 pins `not-recorded`. The
  README restates the five interview questions, the seven modes, both cards'
  status values, and the editor reports' dated paths. The reading list
  copies 56 links from the fourteen vetting records. The README's rule
  summary restates `AGENTS.md` and says that `AGENTS.md` wins. That summary
  is a deliberate exception to L004, made because the ticket asked for the
  rules in the README (decision 7). Two restatements drifted within S008
  itself. Cross-examination finding 9 made the history page exact about the
  first editor check, but the README still says "the first card through the
  check failed", the wording decision 5 set (note 8). And the README sentence
  that finding 10 added says the behavior checks link the examples, when they
  only name the cards as paths (note 7).
- **Changes:** A spec that changes an example card or its report, a vetting
  record or the roster, the pressure-test checks, the `chef-council` skill's
  modes or interview, or a rule in `AGENTS.md` (T015's fixes among them)
  searches `README.md`, `docs/`, and `evals/behavior-checks.md` for the old
  value and changes every restatement in the same pull request. It reuses
  S008's `linkcheck`, `pathcheck`, `evalcheck`, and `readingcheck` as gates.
- **Source:** archived S008, decisions 1, 5, 7, 11, and 20 (lines 141 to
  149, 203 to 204, 219 to 226, 254 to 272, and 329 to 333) and
  `## Cross-examination` findings 9 and 10 (lines 852 to 856);
  [review](https://github.com/thecharlessamuel/chef-council/pull/32#issuecomment-7003048980),
  Design/Simplicity and notes 7, 8, and 10; `.github/workflows/ci.yml`.

## Lessons

### Seven of the eighteen behavior checks expected something the rule files do not say, and the form check could not see it

- **Context:** Decision 12 says each check's Expected line states what the
  shipped skills and method pages require, and that the file named under
  Runs against decides. `evalcheck` proves only the four-line form and that
  the named files exist. Leg 1 rehearsed seven checks. That run found that
  B12's draft Expected line went against `AGENTS.md`, because it expected
  the card to be left unchanged. The spec cross-examination had the rule
  files in its dossier and changed four more checks that disagreed with a
  rule file or missed one of its branches: B03, B06, B13, and B16 (findings
  3 to 6 and 11). The review then found two more. B07 expects "at most one
  or two additions", and B11 accepts a labeled estimate, but no rule file
  states either. Neither check was rehearsed, and each names only a card
  under Runs against (notes 3 and 4). The same review found that run step 2
  relies on `git status`, which does not show a source packet that B12 or
  B13 writes into the git-ignored `.sources/` folder (note 5). The five
  pages were the approved spec's bytes, so the review could only record
  these as notes.
- **Changes:** A spec that writes or changes a behavior check maps every
  Expected and Red flags clause to the line of a Runs against file that
  requires it, and drops or sources each clause with no such line, before
  the cross-examination. The next spec that edits `evals/behavior-checks.md`
  settles B07, B11, and run step 2 (review notes 3 to 5).
- **Source:** archived S008, decisions 12 and 16 (lines 273 to 291 and 304
  to 309), the behavior-check rehearsal (lines 701 to 741), and
  `## Cross-examination` findings 3 to 6 and 11 (lines 837 to 847 and 857
  to 858);
  [review](https://github.com/thecharlessamuel/chef-council/pull/32#issuecomment-7003048980),
  notes 3 to 5; `.gitignore`.
