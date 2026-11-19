---
id: T010
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: resolved
blocked_by: [T007]
claimed_by: spec-pipeline
claimed_at: 2026-11-19T01:04:32Z
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/11
spec: docs/specs/archive/S004-codify-and-cook-log.md
---

## Question
Write the `recipe-codify` and `cook-log` skills (each with its `.claude/skills/` link and `AGENTS.md` index line) and what they write with:

- `templates/recipe-card.md`: optional YAML front matter (`id`, `version`, `status`, `evidence`, `category`) beside the human header lines, an optional `mirrors:` field instead of a notes-app field, and sections for why it works, failure modes, variations, storage, notes, next experiment, and changelog;
- `templates/cook-log.md`: every outcome either quoted from the cook or marked "not reported";
- `templates/source-packet.md`: the verbatim approved text, the scope instruction, the previous version, and paths, under the rule "paste the approved text verbatim; never summarize", saved in the git-ignored `.sources/`;
- `method/status-and-versions.md`: the four status dimensions, the version decision table, and the source-of-truth order;
- `scripts/build-index.py`, which generates `recipes/INDEX.md` from card front matter, and a `--check` mode that fails when the index is stale.

Done when following codify on a fixture produces a card, a regenerated index, and a source packet ready for the editor, and following cook-log produces a log that separates the cook's words from inference.

## Evidence and constraints
- Decisions T003 and T005.
- Design report §3 items 4–7 and 11 (codify replaces the old publish skill: never push `main`; hand off to the editor; a PR, or a direct commit when working alone), §6 (the draft frontmatter for both skills).
- Templates and rules: `private-sources/cooking/templates/` and `private-sources/cooking/context/publishing-workflow.md`, generalized; drop notes-app fields and personal fields such as named feedback.

## Resolution
Shipped as docs/specs/archive/S004-codify-and-cook-log.md through PR #24, merged 2026-11-19; harvest: L004.

## Rationale

## Resulting map updates
