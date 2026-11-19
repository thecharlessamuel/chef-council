---
id: W001
status: built
created: 2026-11-18
classified: 2026-11-18
spec: none
issue: https://github.com/thecharlessamuel/chef-council/issues/1
---

## Destination
`thecharlessamuel/chef-council` is a fork-ready repository, private until the maintainer's review, that any agent (Claude Code, Codex, Cursor, Gemini CLI, Pi, Muse, and chat apps with no file access) can use to develop, cook, log, and independently check recipes with a council of vetted named-chef lenses. CI (QC gate, card lint, gitleaks) is green on `main`, a stranger can follow the README end to end, and a final privacy sweep is clean.

## Notes
- Design: `private-sources/design/design-report.md`, a private source (see `.agents/spec-profile.md`, `## Pipeline constraints`): history §1, the loop §2, skills and robustness gaps §3, the sanitization ledger §4, harness support and the proposed tree §6, a README draft in Appendix A, and the example recipes in Appendix B. Decision T002 overrides its persona recommendation (§5, option C), and T003 overrides its license line.
- Standing constraints for every ticket live in `.agents/spec-profile.md` `## Pipeline constraints`: public by default, private sources, third-party recipe text, real people, and the privacy sweep.
- Each skill ticket adds its own line to the skill index in `AGENTS.md` and its own `.claude/skills/<name>` link.
- Relevant skills: `wayfinder`, `spec-pipeline`, and the four numbered spec legs.

## Decisions so far
- [Repository and launch scope](issues/T001-repository-and-launch-scope.md) — `thecharlessamuel/chef-council`, this repository only.
- [Named chefs with guardrails](issues/T002-named-chefs-with-guardrails.md) — the council keeps the real chef names, each seated only with a vetting record.
- [License](issues/T003-license.md) — MIT for everything.
- [Private until review](issues/T004-private-until-review.md) — built private; the maintainer makes it public after review.
- [Privacy rules](issues/T005-privacy-rules.md) — everything that enters the repository is public-bound; a private denylist is swept before every merge.
- [Private repository names](issues/T006-private-repository-names.md) — public text never names the maintainer's private repositories.
- [Scaffold](issues/T007-scaffold.md) — shipped as S001 (PR #18)
- [Council roster and vetting](issues/T008-council-roster-and-vetting.md) — shipped as S002 (PR #20)
- [Chef council skill](issues/T009-chef-council-skill.md) — shipped as S003 (PR #22)
- [Codify and cook log](issues/T010-codify-and-cook-log.md) — shipped as S004 (PR #24)
- [Editor gate](issues/T011-editor-gate.md) — shipped as S005 (PR #26)
- [Example recipes](issues/T012-example-recipes.md) — shipped as S006 (PR #28)
- [Chat path and adapters](issues/T013-chat-path-and-adapters.md) — shipped as S007 (PR #30)
- [Docs and behavior checks](issues/T014-docs-and-behavior-checks.md) — shipped as S008 (PR #32)
- [Stranger test](issues/T015-stranger-test.md) — shipped as S009 (PR #34)

## Not yet specified
- [deferred] How Antigravity CLI and Muse Code load instructions is unverified (design §6); `AGENTS.md` covers them by convention, and no ticket tests them.
- [deferred] Whether Cursor lists each skill twice through the `.claude/skills` links is unverified (design §6); harmless if it does.

## Out of scope
- Making the repository public and linking it from the maintainer's website: the maintainer's separate steps after review (T004).
- Any change to the private sources, the website, or another repository (T001).
- The recipe-block image generator and the read-only cookbook connector (design §3, items 12 and 15): later candidates, not v1.
- Every private card other than the two examples, including the family recipes (design §4).
- A domain-neutral council framework or generic council skill (design §5.1): only the pattern document ships.

## Frontier
- [Scaffold](issues/T007-scaffold.md)

## Handoff
Destination as above. Resolved decisions: [T001](issues/T001-repository-and-launch-scope.md), [T002](issues/T002-named-chefs-with-guardrails.md), [T003](issues/T003-license.md), [T004](issues/T004-private-until-review.md), [T005](issues/T005-privacy-rules.md), [T006](issues/T006-private-repository-names.md). Deferred fog: instruction loading in Antigravity CLI and Muse Code, and duplicate skill listing in Cursor, both safe to leave. Out of scope: publication and the website, other repositories, the image generator and connector, the other private cards, and a generic council framework.

> Map `docs/wayfinder/W001-public-chef-council/MAP.md` is ready to build. Kick off `spec-pipeline docs/wayfinder/W001-public-chef-council/MAP.md --grant
> autonomous` to work it ticket by ticket, or `1-spec-write docs/wayfinder/W001-public-chef-council/MAP.md` for one ticket.
