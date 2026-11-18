---
id: T008
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: resolved
blocked_by: [T007]
claimed_by: spec-pipeline
claimed_at: 2026-11-18T19:03:32Z
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/9
spec: docs/specs/archive/S002-council-roster-and-vetting.md
---

## Question
Seat the named council under decision T002:

- the vetting rule, adapted from the home-design council (`private-sources/home-design/context/council-vetting.md`): a named lens is seated only with a record holding the official site with the date checked, two or more named published works relevant to the seat, at least one independent source or book, three to five tendencies the published work shows (in this repository's words), the one question the lens always asks, where the lens can mislead, a verdict (seat, seat narrower, or cut), and access notes;
- `templates/lens-vetting-record.md`, adapted from `private-sources/home-design/templates/vetting-record.md`;
- one record for each of the fourteen names: J. Kenji López-Alt, America's Test Kitchen / Dan Souza, Heston Blumenthal, Stella Parks, Claire Saffitz, Sohla El-Waylly, Rick Martinez, Madhur Jaffrey, Fuchsia Dunlop, Samin Nosrat, Jacques Pépin, Yotam Ottolenghi, Maangchi, and Marcella Hazan;
- `kitchen/council.md`, the roster: the six core lenses and the eight on-demand specialists that the records seat, each named "<Name>-style lens" with its job, typical question, scope, and where it can mislead.

Done when every name has a record whose citations were read in the session with the date checked, the roster seats exactly the names whose records say seat or seat narrower, and no file quotes, or claims approval, review, endorsement, or contribution from, a real person.

## Evidence and constraints
- Decision T002 and the real-people constraint in `.agents/spec-profile.md`.
- Design report §5 (the lens jobs and typical questions) and §5.1 (the vetting rule, "standards, not people", named disagreement with stated dissent).
- `private-sources/council-skills/culinary-counsel/references/chefs.md` supplies names, roles, and domains only. Its "Weaknesses" lines are not carried over in any form.
- A name the evidence cannot support is cut under the rule, with the reason in its record. Marcella Hazan died in 2013; her record rests on her books and independent sources, and its access notes say there is no official site.
- A record describes published work, never personal life.

## Resolution
Shipped as docs/specs/archive/S002-council-roster-and-vetting.md through PR #20, merged 2026-11-18; harvest: L002.

## Rationale

## Resulting map updates
