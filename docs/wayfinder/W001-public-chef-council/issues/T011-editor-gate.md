---
id: T011
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: resolved
blocked_by: [T010]
claimed_by: spec-pipeline
claimed_at: 2026-11-19T02:24:41Z
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/12
spec: docs/specs/archive/S005-editor-gate.md
---

## Question
Make the independent editor check the gate that works with any agent, enforced in CI:

- the portable `recipe-editor` skill with `references/report-format.md` (its `.claude/skills/` link and `AGENTS.md` index line): a fresh agent compares the card line by line with the verbatim source packet and writes a report with a verdict (PASS, PASS WITH NOTES, or FAIL), a discrepancy table with severity, and a `Card-SHA256:` line; it never edits recipes, and with no second agent available it says so and never self-certifies;
- a thin `.claude/agents/recipe-editor.md` wrapper that runs the skill in a fresh context;
- `scripts/check-qc.sh`: a changed card passes only when a changed report for it holds a passing verdict and a `Card-SHA256` equal to the committed card's hash; it fails closed when `CI=true` or the base ref is missing, and reports are keyed so slugs cannot collide;
- `scripts/lint-cards.py`: header and front-matter fields, status values, unique slugs, links, and `scripts/build-index.py --check`;
- an optional `scripts/install-git-hooks.sh` (pre-commit) and an optional Claude Stop hook in `.claude/settings.json`, both calling the same script;
- `method/recipe-qc.md` for humans and chat users, with the new-chat editor prompt;
- CI jobs running the gate and the linter on every pull request and every push to `main`, actions pinned by SHA.

Done when the tests show the gate failing a card change with no report, with a stale-hash report, and with a FAIL report, and passing one with a current passing report; and CI is green on this PR, which changes no card.

## Evidence and constraints
- Decisions T005 and T002 (an editor report never claims a real person reviewed anything).
- Design report §3 items 8–9 (gaps and the hardening list), §6 (the portable table and the draft frontmatter).
- Sources to generalize: `private-sources/cooking/context/recipe-qc.md`, `private-sources/cooking/.claude/agents/recipe-editor.md`, `private-sources/cooking/.claude/hooks/recipe-qc-gate.sh`, and `private-sources/cooking/.github/workflows/recipe-qc-gate.yml`; drop the notes-app checks and the maintainer's name.

## Resolution
Shipped as docs/specs/archive/S005-editor-gate.md through PR #26, merged 2026-11-19; harvest: L005.

## Rationale

## Resulting map updates
