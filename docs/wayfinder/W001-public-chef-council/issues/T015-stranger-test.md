---
id: T015
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: claimed
blocked_by: [T014]
claimed_by: spec-pipeline
claimed_at: 2026-11-19T07:58:50Z
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/16
spec: docs/specs/S009-stranger-test.md
---

## Question
Prove a stranger can use the repository. A fresh subagent given only the repository URL clones it into an empty temporary directory and follows the README's five-minute path end to end: the coding-agent path, with the cook's reports simulated, and the chat path as far as preparing the paste-in and the bundle. It records every point where it got stuck, had to guess, or found a mismatch, and this ticket's PR fixes those points.

Done when a second fresh stranger run on the fixed branch completes the path with no blocking trip, and a summary of both runs is in the PR.

## Evidence and constraints
- Decision T004: the repository is private until review, so the stranger clones through the maintainer's authenticated `gh`, which stands in for public access.
- The stranger is briefed with the URL and nothing else, and never reads the private sources.
- A fix that changes a card re-runs the editor and the gate; a fix that changes a skill keeps its link and index line.

## Resolution

## Rationale

## Resulting map updates
