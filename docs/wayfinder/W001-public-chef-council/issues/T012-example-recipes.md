---
id: T012
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: open
blocked_by: [T009, T011]
claimed_by: none
claimed_at: none
cross_examined: none
issue: none
spec: none
---

## Question
Ship two example cards, each run through the real editor with its QC report committed:

- Butter-Roasted Carrots with Jaggery and Sumac;
- Council Tuna Melt, with its unsourced claims removed and no real person credited as author;

both as v1.1 with the public-release edits in their changelogs, plus the generated `recipes/INDEX.md`. Done when both cards pass `scripts/check-qc.sh` and the linter in CI, each report was written by a fresh editor subagent from a verbatim source packet, and neither card credits a real person or makes an unsourced claim.

## Evidence and constraints
- Decisions T002 and T005.
- Design report Appendix B gives the exact scrubs and rewrites for both cards; their ingredient lines, quantities, temperatures, and method stay as the appendix says.
- Private cards: `private-sources/cooking/recipes/sides/butter-roasted-carrots.md` and `private-sources/cooking/recipes/meats/council-tuna-melt.md` (original council work, no publisher's recipe adapted). The private QC reports are not carried over.
- Status: the carrots are reviewed and not yet cooked as written; the tuna melt is cooked once (the dill-pickle variant, 2026-08-01).
- Lens references read "<Name>-style lens", and no lens is credited as author.
- Each source packet is the scrubbed approved text. The spec decides whether the packets are committed as examples or kept in `.sources/`.

## Resolution

## Rationale

## Resulting map updates
