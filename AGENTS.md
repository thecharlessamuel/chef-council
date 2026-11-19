# Agent entry point: Chef Council

This repository is a system for cooking with AI agents: a council of cooking lenses that develops and pressure-tests recipes, plain-text recipe cards and cook logs, and an independent editor check on every recipe change. Read this file first, then the files it points to. It applies to every agent, whichever harness runs it.

The person you are working with is called the cook here. If you cannot read or write files in this repository (a chat app, for example), say so once, and when asked to save something return the complete file and its path for the cook to save.

## Read in this order

1. [`kitchen/README.md`](kitchen/README.md), then [`kitchen/profile.md`](kitchen/profile.md), [`kitchen/equipment.md`](kitchen/equipment.md), and [`kitchen/pantry.md`](kitchen/pantry.md): who is being cooked for, their constraints and standing corrections, the equipment, and a dated pantry snapshot. A file whose front matter says `filled_in: no` is still a blank template: ask the cook, and never treat a placeholder as a fact.
2. [`kitchen/council.md`](kitchen/council.md): the lenses on the council, what each one is for, its scope, and where it can mislead. Each lens has a vetting record in `kitchen/vetting/`, and [`kitchen/council-vetting.md`](kitchen/council-vetting.md) is the rule for seating one.
3. The skill for the job, from [Skills](#skills) below. Read its `SKILL.md` in full before acting on it.
4. The saved recipe card, and its most recent cook log, before changing that recipe or cooking from it.

## Rules that are easy to get wrong

- **The latest correction beats a saved card.** When the cook's most recent explicit instruction disagrees with a saved card, name the conflict, follow the correction, and update the card. The standing corrections in `kitchen/profile.md` beat a card in the same way.
- **Status is several separate facts:** how far the recipe has been developed, whether it has been cooked and how that went, whether the card is saved in the repository, and whether any copy outside the repository is up to date. Writing a card does not make it cooked, and cooking it once does not make it a house recipe. Never raise any of these without a logged cook or the cook saying so.
- **Never report a save, sync, or check that did not happen.** Say "saved" only after the file is written, "synced" only after reading the other copy back, and "checked" only when the check ran and you read its result. When a step failed or was skipped, say which one and why.
- **Do not invent** quantities, times, temperatures, cook outcomes, allergies, equipment limits, or sources. When a number is missing, say so on the card.
- **Keep the old version when testing a new one.** A small edit is a version bump on the same card. A changed technique or a variant is its own card, and the original stays.
- **The council is a set of lenses, not people.** Attribute advice to a lens, written `<Name>-style lens`. No real chef has reviewed, approved, endorsed, or contributed to anything here, so never say or imply one did, and never invent a quote. A lens argues only from the tendencies in its vetting record and only inside its scope. Asked to add a name to the council, vet it first under `kitchen/council-vetting.md`, then seat it or decline with the reason.
- **Food safety is a constraint, not a lens's opinion.** A safety number comes from a cited standard. When `higher_risk_diners` in `kitchen/profile.md` is `yes`, use the stricter endpoints; when it is `unknown`, ask before giving one.
- **Every recipe change gets an independent editor check.** A separate agent, in a fresh context that did not write the card, compares the card one for one with the exact text the cook approved. A failed check blocks the change. With no second agent available, say so; never certify your own work.
- **Copy no third-party recipe text:** no ingredient lists, methods, or headnotes from any publisher. Credit a source by title and link only when it was actually read.

## The loop

1. **Idea.** The cook says what they want to make or what they have on hand.
2. **Baseline.** Recover the current card and its last cook log, if they exist.
3. **Council.** Pick the lenses that matter, then give one recommendation, or two or three directions when the choice changes the dish. The cook chooses the direction.
4. **Pressure test.** Before anyone cooks, check the recipe: each ingredient's role, stacked salt, sugar and acid, cut and thickness, crowding, liquid, scaling, and whether the ingredient list matches the method. Reprint the corrected recipe in full.
5. **Live cook.** Guide one step at a time: do this now, the cue to look for, what comes next. The cook cooks and may substitute.
6. **Report back.** The cook says what they actually did and how it turned out. That report is the evidence.
7. **Codify.** Write or update the card and the cook log from what was approved and reported, with an honest status. The cook sets the scope of the save.
8. **Editor check.** A fresh agent checks the card against the approved text. On a fail, fix the card and run a fresh check.
9. **Pull request.** Open one; the cook merges it.
10. **Mirror, on request only.** Copy a card to a notes app only when the cook asks or calls the recipe final, then read the copy back.
11. **Promote.** Only the cook calls a recipe a house recipe.

What stays with the cook: choosing a direction, the scope of a save, what was cooked and how it tasted, promoting a recipe, and the merge.

## Skills

Skills live in `.agents/skills/<name>/`, and Claude Code finds them through the links in `.claude/skills/`. If your harness did not load a skill on its own, open the path given here and follow it. [`.agents/skills/README.md`](.agents/skills/README.md) explains how a skill is added.

- `chef-council`: [`.agents/skills/chef-council/SKILL.md`](.agents/skills/chef-council/SKILL.md). Use it to develop, adapt, pressure-test, cook live from, troubleshoot, or research a recipe with the council, to hand a finished recipe off to be saved, and to run the first-run kitchen interview when `kitchen/profile.md` is blank.

## Making changes

- Work on a branch and open a pull request against `main`, so the checks run before the merge.
- Write commit subjects in the imperative mood, such as `Add the roasted carrots card v1.0`.
- Before opening a pull request, run the checks CI runs:
  - `python3 scripts/check-skills.py`: every skill has its link and its line above.
  - `python3 scripts/check-council.py`: the council roster matches the vetting records.
  - `python3 -m unittest discover -s tests -v`: the tests for the scripts.
  - `scripts/secret-scan.sh`: gitleaks over the full history.
- Never commit a secret, a credential, or a token. Source packets, the exact text a cook approved, stay in the git-ignored `.sources/` folder.
- Everything committed to a public fork is public, including `kitchen/` and the history. Keep out anything the cook would not publish.
