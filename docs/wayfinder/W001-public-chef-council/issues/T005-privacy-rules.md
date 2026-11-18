---
id: T005
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: grilling
status: resolved
blocked_by: []
claimed_by: none
claimed_at: none
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/6
spec: none
---

## Question
What must stay out of everything that enters the repository, and how is that checked?

## Evidence and constraints
The design report's sanitization ledger (§4) lists the private material by file. The maintainer's rules below apply to files, history, commit messages, branch names, specs, map tickets, issues, PR bodies, and review comments.

## Resolution
Answered by the human in the charting session on 2026-11-18:

> Everything that enters the repo will become public: files, history, commit messages, branch names, specs, map tickets, issues, PR bodies and review comments. So:
> - Leave out household names, health details, location, Mem IDs, private URLs or hosts, VM paths, [references to the self-hosted assistant] and session links.
> - Copy no third-party recipe text ([a publisher], NYT Cooking, ATK recipes).
> - Build a privacy denylist from the private sources at [a path outside the repository], and never commit it. Run it against the working tree, the full history and all issue and PR text before every merge.
> - Set the repo-local git email to my GitHub noreply address before the first commit.
> - Run a secret scan (gitleaks) in CI from the start.

The bracketed words replace text the rule itself excludes.

## Rationale
Once the repository is public, anything in its history or GitHub text is effectively permanent, so the check runs before every merge rather than once at the end.

## Resulting map updates
`.agents/spec-profile.md` carries these rules as pipeline constraints and names the maintainer-local privacy sweep, which reads the denylist and prints only rule IDs and locations. T007 adds gitleaks to CI. The repository-local git identity is the maintainer's GitHub noreply address.
