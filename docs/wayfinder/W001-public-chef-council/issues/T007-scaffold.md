---
id: T007
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: open
blocked_by: []
claimed_by: none
claimed_at: none
cross_examined: none
issue: none
spec: none
---

## Question
Build the skeleton any agent finds its way into:

- `AGENTS.md` as the canonical entry, under 8 KB: read order, the rules that are easy to get wrong (latest correction beats a saved card; status is several facts; never report a save, sync, or check that did not happen), the loop, and a skill index with paths that each later skill ticket extends;
- one-line `CLAUDE.md` (`@AGENTS.md`) and `GEMINI.md` (`@./AGENTS.md`);
- `LICENSE`: MIT for the whole repository;
- `kitchen/` fill-in templates: `README.md` (fill-in order), `profile.md` (who you cook for, priorities, constraints, a `higher_risk_diners` field, units, standing corrections), `equipment.md` (verified versus assumed, manual limits), and `pantry.md` (a dated snapshot);
- the `.agents/skills/` home and its convention of one `.claude/skills/<name>` link per skill, with a check that every skill has its link;
- `.gitignore`, including the `.sources/` folder for source packets;
- CI that runs gitleaks over the full history on every pull request and every push to `main`, with every action pinned by commit SHA.

Done when a fresh clone shows these files, the CI run on the PR is green, and the spec's observation shows gitleaks failing on a planted test secret in a scratch fixture that is never committed or pushed.

## Evidence and constraints
- Decisions T001, T003, T005.
- Design report (`private-sources/design/design-report.md`): §6 (what each harness reads, the decision, the proposed tree), §3 items 9 and 13, §4 rows for `AGENTS.md` and `CLAUDE.md`. The private `AGENTS.md` (`private-sources/cooking/AGENTS.md`) is generalized: keep its structure, drop the maintainer's name, the notes-app rules, and the personal standing corrections.
- The one-line `README.md` GitHub created stays until T014 replaces it.

## Resolution

## Rationale

## Resulting map updates
