---
id: T014
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: claimed
blocked_by: [T012, T013]
claimed_by: spec-pipeline
claimed_at: 2026-11-19T06:44:50Z
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/15
spec: docs/specs/S008-docs-and-behavior-checks.md
---

## Question
Write the human-facing docs:

- `README.md` from design Appendix A, rewritten for the named lenses and MIT: a plain statement that no chef is affiliated with or has endorsed this repository, the five-minute paths for coding agents and chat apps, the pieces table, and the rules;
- `docs/how-this-was-built.md`: the dated evolution and the incident behind each rule, from design §1, with no household or infrastructure detail;
- `docs/council-pattern.md`: the reusable council pattern, the cooking and home-design mapping, and how to start a council in another domain;
- `docs/reading-list.md`: the named chefs' published work that shaped the lenses, linked;
- `evals/behavior-checks.md`: generalized scenarios, each with a prompt, the expected behavior, and red flags, seeded by the example cards, with a run-by-hand section, including "Did Kenji approve this?" (no) and "Add <famous name> to the council" (vet first).

Done when every relative link resolves, every path the README names exists, and each behavior check names the file it runs against.

## Evidence and constraints
- Decisions T002 (the disclaimer and the Kenji check), T003 (MIT, replacing the appendix's license line), T005, and T006.
- Design report §1, §2, §5.1, and Appendix A.
- Behavior checks: `private-sources/cooking/context/behavior-checks.md` and `private-sources/home-design/context/behavior-checks.md`, generalized; drop every personal recipe and name.
- The history calls the predecessors "my private cooking repo" and "a self-hosted assistant agent".

## Resolution

## Rationale

## Resulting map updates
