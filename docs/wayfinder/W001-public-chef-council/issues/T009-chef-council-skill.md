---
id: T009
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: open
blocked_by: [T008]
claimed_by: none
claimed_at: none
cross_examined: none
issue: none
spec: none
---

## Question
Write the portable `chef-council` skill (`.agents/skills/chef-council/` with its `.claude/skills/` link and its `AGENTS.md` index line):

- lens selection from `kitchen/council.md`, relevance first, and one recommendation with any remaining dissent named;
- the modes, each with a fixed response shape: develop, adapt, pressure-test, live cook, troubleshoot, research, and the hand-off to codify;
- a first-run interview that fills `kitchen/profile.md` when it is blank (who you cook for, constraints and allergies, equipment, skill and time, units);
- the pressure test with a fixed output: a findings table (check, result, fix), the reprinted corrected recipe, then the resolved recommendation and remaining dissent;
- `references/food-safety.md`, built on cited standards, with a checked-on date, a refresh-by date, and a locale note, which settles the 150–155°F versus 165°F poultry conflict from a cited source;
- `references/troubleshooting.md`.

Done when the frontmatter is spec-valid, every safety number traces to a cited source, the poultry conflict is settled in the reference, and every piece of advice is attributed to a "<Name>-style lens" or to a cited standard, never to a person.

## Evidence and constraints
- Decisions T002 and T005; T008's roster and records.
- Design report §3 items 1–3 (gaps and fixes), §5.1 ("standards, not people"; safety is a constraint, not a lens), §6 (the draft frontmatter).
- Method sources: `private-sources/cooking/context/council-method.md` and `private-sources/council-skills/culinary-counsel/` (method, modes, troubleshooting). Drop "reference the experts by name", "science wins over tradition" (it becomes "evidence beats habit; tradition explains technique"), and every household example.
- Food safety defaults to US guidance (FoodSafety.gov, USDA FSIS, FDA), °F with °C. Poultry at 165°F is the default; a lower temperature appears only as a labeled time-at-temperature hold from a cited FSIS table, never as a default. A `higher_risk_diners` entry in the kitchen profile switches to the stricter endpoints.

## Resolution

## Rationale

## Resulting map updates
