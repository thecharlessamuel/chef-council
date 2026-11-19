# How this was built

This page is the history of the system in this repository: what it was for, how it changed, and the incident behind each rule. It is written by the maintainer, in the first person. The dates come from the commit history of my private cooking repo, which is not public, and from the history of this repository.

## The problem

I develop recipes with AI agents. The real work happened in chat: picking a direction, checking the numbers, help at the stove, and my report on how the dish turned out. Chat history does not carry from one tool to the next, and saved recipe cards drifted behind my latest corrections. The agents also kept doing the same three things: calling a proposed recipe proven, saying something was saved when it was not, and grading their own write-ups.

## Three versions

1. **A council of named chefs.** The first version, in July 2026, was a set of skills inside a self-hosted assistant agent. It was useful, and it over-claimed. It told the agent to speak in the chefs' voices, it credited named chefs as the source of a recipe, and it published straight to the default branch and to a notes app.
2. **Plain files any agent can read.** In October 2026 I moved the system between assistants and found the knowledge trapped in one chat. The move forced it into files: a method, a kitchen profile, templates, and an index. It also made status honest. A saved card is not a cooked recipe, and a cooked recipe is not a house recipe.
3. **An independent editor.** In November 2026 one failure had repeated often enough: the agent that writes a recipe cannot be trusted to check it. A separate editor now compares every card, line by line, with the words I approved, and a script and a CI check refuse a change that has no passing report.

This repository is a fourth step. It is the same system, rebuilt so that someone else can use it.

## Timeline

Every date is in 2026.

| Date | What changed | What prompted it |
|---|---|---|
| July 29 | My private cooking repo was created with its first recipe card. The same day a self-hosted assistant agent got three skills: a council of named chefs, a picture of the recipe as a grid, and publishing to the repository and to a notes app. | The original idea: named chefs as lenses, and cooking treated as engineering. |
| August 1 | The first recipe was built with the council and then cooked. It is the tuna melt that ships here as an example. | The first full trip around the loop. |
| August 13 to 16 | The publishing skill gained a rule: read a note back before reporting that it was saved. | The rule's own wording refers to earlier reminders about notes that were missing. |
| August to early October | No commits. Recipe development moved into a chat app, and corrections piled up in chat and in the notes app, not in the repository. | The repository was not part of the daily loop. |
| October 9 | The chat app wrote one long handoff document, so that the system could move to other assistants. | I wanted the same council in any tool, and the knowledge was in one vendor's chat. |
| October 10 | A coding agent split the handoff into files that any agent can read and recorded the settled rules: my latest word beats a saved card, no invented endorsements, and a recipe is final only when the repository and the notes copy agree. The existing cards were imported with honest status lines, and an `AGENTS.md` was added. | A saved card gave two pounds of its main ingredient, and a correction I had made days earlier said one. |
| October 16 | The first copy to the notes app was made from the repository, not from a chat, and the format of a note was fixed. | The notes had been written in more than one format. |
| November 1 | The independent editor check was added, with a script and a CI check. Its first report was run after the fact, on a card saved earlier that day. That evening the next card was the first to be checked before it was saved, and it failed. That card was fixed, a fresh editor passed it with notes, and only then was it copied to the notes app. | I asked for it: every recipe that goes in must match what was agreed, one for one, and an agent that writes a card may not grade its own work. |
| November 18 | Work on this repository began. | I wanted to share the system without publishing my household. |
| November 19 | The lenses lost their names. Each one had carried the name of a real cook or publisher, under a decision made on November 18. That decision was superseded: each lens now carries a description of its approach, its record names no one, and a check in CI fails if a removed name comes back. | I decided that a public repository should not carry real people's names on lenses they never saw. |

## The incident behind each rule

| Rule | Incident | Where the rule lives now |
|---|---|---|
| The latest correction beats a saved card. | A saved card said two pounds. My correction, days earlier, said one. A saved file can be older than the latest truth. | [`AGENTS.md`](../AGENTS.md), and "When sources disagree" in [`method/status-and-versions.md`](../method/status-and-versions.md) |
| Status is several separate facts. | The October import. Each card needed its own honest status line, because written, cooked, and copied elsewhere turned out to be different facts. | [`method/status-and-versions.md`](../method/status-and-versions.md) |
| Lenses, not people. | The first version wrote in the chefs' voices and credited named chefs as the source of a card. Nobody named had seen it. The lenses kept real names until November 19, when the names were removed. | [`kitchen/council.md`](../kitchen/council.md) and [`kitchen/council-vetting.md`](../kitchen/council-vetting.md) |
| Safe and done are separate checks. | Beef reached a safe temperature and was still tough. | "Food safety" in the [`chef-council` skill](../.agents/skills/chef-council/SKILL.md) |
| A safety number comes from a cited standard. | A troubleshooting note in the first version gave a poultry temperature below the food-safety default, as if it were the default. | The [food-safety reference](../.agents/skills/chef-council/references/food-safety.md) |
| Owning a spice is not a reason to use it. | The roasted carrots that ship here as an example. | The "Ingredient roles" check of the pressure test, and the [carrots card](../recipes/sides/butter-roasted-carrots-with-jaggery-and-sumac.md) |
| Read the real source before adapting it. | An adaptation of a publisher's recipe, which is one of the cards left out of this repository. | "Research" in the [`chef-council` skill](../.agents/skills/chef-council/SKILL.md) |
| Never report a save that was not read back. | Notes that were reported as saved and were never created. The read-back rule of August followed. | [`AGENTS.md`](../AGENTS.md), and rule 5 of [`adapters/README.md`](../adapters/README.md) |
| The writer of a card never grades it. | The first card that was checked before it was saved failed. The first temperature check sat five minutes later than agreed, and the cook log stated equipment and thermometer details I never reported. The writer had missed both. | [`method/recipe-qc.md`](../method/recipe-qc.md) |
| The check comes before the copy. | The first editor report, run after the fact on an earlier card, found that the card had been copied to the notes app and its pull request opened before any check. | "When a copy is made" in [`adapters/README.md`](../adapters/README.md) |

## Keeping a migration

When the system moved between assistants in October, the handoff document was kept exactly as it arrived, in an archive folder with a checksum for each file, and the rule was never to cook from the archive. The working files were written from it. I recommend the same to anyone moving a body of notes into this repository: keep the input unchanged, write the cards from it, and let the editor compare the two. The archive itself is private and is not here.

## How this repository was made

I did not make my private cooking repo public. Its history holds personal details and recipes restated from publishers, and rewriting history would have destroyed the story it was meant to keep. This repository was started fresh, and this page tells the history.

- **What was carried over:** the method, the status rules, the templates, the editor check, and two recipe cards that are original work, each scrubbed and checked again by the editor here.
- **What was left out:** every other recipe card, the kitchen profile, the cook logs, the earlier editor reports, the archive, the picture generator for recipes, and an unfinished connector that would let other assistants read the cookbook.
- **What changed on the way:** the kitchen files became blank templates; the gate now ties each report to the hash of the card it checked; the notes app became an optional adapter with a written contract; and each lens was seated only after a record was written for it, on November 18, and was renamed for its approach on November 19.

The repository was built one ticket at a time by agents, each change specified, built, reviewed by a separate session, and merged by pull request. On November 19 those records were edited to remove the names: where one named a person, a publication, or a link, it now reads `[name removed]`, `[title removed]`, or `[link removed]`, and a lens's old name reads as its new name in square brackets. The plan is in [the build map](wayfinder/W001-public-chef-council/MAP.md), the specifications are in the [spec index](specs/INDEX.md), and what each change taught is in the [learning index](learnings/INDEX.md).

## What the example report gets wrong

The [editor report for the tuna melt](../qc/sandwiches/council-tuna-melt/2026-11-19.md) reads `VERDICT: PASS` with no discrepancies, and the verdict stands. A later review of the report found three remarks in it that do not match the files:

1. It says four rows of the Failure modes table had a blank Problem cell in the approved text. Three did.
2. It says the card states that nobody reviewed, approved, endorsed, or wrote it. The card names no person and makes no such statement.
3. It says only punctuation, italics, and the form of the step names changed in the Method. Step 10 also gained a word.

A report is the record of one check, and what it found is never edited, so the three remarks stay. On November 19 the Editor line of each example report lost the name of the model that ran the check, and nothing else in either report changed. The card's next change gets a fresh report. The lesson is the one the method page already states: the gate proves that a passing report exists for the card as it stands, and it cannot tell whether the check was careful.

## What is not here yet

- A generator that draws a recipe as a grid. The first one was tied to a single recipe.
- A read-only connector that lets another person's assistant read the cookbook.
- A council framework for other domains. [The council pattern](council-pattern.md) describes the shape, and that page is all that ships.
