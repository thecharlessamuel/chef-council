---
id: T006
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: grilling
status: resolved
blocked_by: []
claimed_by: none
claimed_at: none
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/7
spec: none
---

## Question
May public text name the maintainer's private repositories?

## Evidence and constraints
Specs and tickets need to point executors at private source files; the history document needs to refer to the private predecessor.

## Resolution
Answered by the human in the charting session on 2026-11-18, choosing "Never name them" for: "Should public text (files, specs, issues, PRs, commits) never name your private repos ([three names])? It would say 'my private cooking repo' instead, and specs would cite private sources through a neutral alias path. The denylist would enforce this."

## Rationale
Least disclosure: the names add nothing for a reader, and the alias path is enough for an executor.

## Resulting map updates
Committed and posted text cites private material only as `private-sources/<path>` (resolved locally through the git directory, never committed) and calls the predecessor "my private cooking repo". The denylist includes the three names.
