# Chef Council

I cook at home most nights, and I've got a slew of fantastic cookbooks I use for idea generation. On top of that, (naturally) I work with AI agents to develop composite recipes and improve them over time.

This repository is the core of the system I use for that. A council of cooking lenses argues a recipe into shape. Plain-text recipe cards and cook logs record what actually happened in the kitchen. An independent editor checks every saved recipe against what I approved before it is allowed in. It works with any agent that can read files, and, by copy and paste, with a chat app that cannot.

**No chef is affiliated with this repository, and none has endorsed it.** Each lens is a described cooking approach, named for the approach and never for a person or a brand. No lens is a real person or speaks for one, nothing a lens argues is a quotation of anyone, and no cook, author, or publisher has reviewed, approved, endorsed, or contributed to anything in this repository. [`kitchen/council.md`](kitchen/council.md) is the roster.

## Why this exists

Cooking with an AI agent works well in the moment and badly over time. The good decisions live in a chat thread that the next tool cannot see. Saved recipes drift behind the latest correction. And agents tend to do three things:

- call a proposed recipe tested,
- say something was saved when it was not,
- check their own work and find it fine.

I wanted the opposite: one place where recipes and the reasons behind them are written down, where "written", "cooked", and "something we make every week" are different facts, and where no recipe changes without a second agent comparing it, line by line, with what I approved.

## Try it in five minutes

You need Git, Bash, and Python 3. There is nothing to install and nothing to build.

**With a coding agent** (any agent that reads `AGENTS.md`):

1. Fork or clone this repository and open it in your agent.
2. Say what you have: "Summon the council. I have two pounds of carrots, butter, and forty minutes." The first time, the agent asks five short questions before it answers (who you cook for, constraints and allergies, equipment, skill and time, and units) and writes your answers into `kitchen/profile.md` and `kitchen/equipment.md`. It then rebuilds `chat/bundle.md`, which includes those files, and leaves all three for you to commit.
3. Choose a direction. To have the recipe checked before you cook, say: "Pressure-test it." Then cook, and tell it how it went: "Made it. Too sweet, and the thin pieces burned."
4. Say: "Log this cook." It writes a cook log in your own words, marks what you did not say as not reported, and proposes one change for next time.
5. Say: "Save the recipe as a card." It writes the card with an honest status, and a separate agent checks the card against what you approved before anything is committed.

**With a chat app** (one that takes pasted instructions and an uploaded file):

1. Follow [`chat/README.md`](chat/README.md): paste `chat/project-instructions.md` into the app's instructions and upload `chat/bundle.md` as its knowledge file.
2. Use the same prompts. The chat cannot write to the repository, so it returns each finished file for you to save and says that nothing was saved.
3. For the editor check, open a new chat and follow [The editor prompt for a new chat](method/recipe-qc.md#the-editor-prompt-for-a-new-chat).

## What is inside

| Piece | What it does |
|---|---|
| [`AGENTS.md`](AGENTS.md) | The entry point every agent reads: the reading order, the rules, the loop, and where the skills are. |
| [`chef-council` skill](.agents/skills/chef-council/SKILL.md) | Weighs the lenses that fit the question and gives one recommendation, with any remaining dissent named. Its modes are develop, adapt, pressure-test, live cook, troubleshoot, research, and hand off to codify. It also holds the food-safety reference. |
| [`recipe-codify` skill](.agents/skills/recipe-codify/SKILL.md) | Turns a recipe you approved into a card with a version and an honest status, and keeps the exact text you approved for the editor. |
| [`cook-log` skill](.agents/skills/cook-log/SKILL.md) | Records what actually happened, in your words, and marks everything you did not say as not reported. |
| [`recipe-editor` skill](.agents/skills/recipe-editor/SKILL.md) | A separate agent compares the card with what you approved and writes a report with a verdict. It never edits a recipe. |
| `scripts/check-qc.sh` and CI | Block any recipe change that has no passing editor report for the card as it now stands. [`method/recipe-qc.md`](method/recipe-qc.md) explains the check. |
| [`kitchen/`](kitchen/README.md) | Who you cook for, your equipment, your pantry, and the council roster with its vetting records. The folder you make yours. |
| [`recipes/`](recipes/INDEX.md) and `qc/` | The recipe cards with their generated index, and the editor reports. Two example cards ship here. |
| [`method/`](method/status-and-versions.md) | The status and version rules, and how the editor check works, written for people. |
| [`chat/`](chat/README.md) | The paste-in instructions and the generated knowledge file for a chat app with no file access. |
| [`adapters/`](adapters/README.md) | Optional: how an agent keeps a copy of a card in a notes app without making duplicates. |
| [`evals/behavior-checks.md`](evals/behavior-checks.md) | Scenarios you run by hand to see whether your setup behaves well. |
| `docs/` | [How this was built](docs/how-this-was-built.md) and [the council pattern](docs/council-pattern.md). |

## The council

The council is a set of lenses, not people. Six core lenses are consulted by default, each for its own job: heat and ingredient function, reliability, the finishing touch, baking formulas, baking workflow, and pantry cooking. Eight specialists join only when a dish is in their scope, such as a regional cuisine or the balance of a dish. Each lens is named for its approach, such as the Savory science lens, argues only from the tendencies in its record, and stays inside its recorded scope.

The roster is yours to edit. To add, narrow, or remove a lens, follow [`kitchen/council-vetting.md`](kitchen/council-vetting.md): the record comes first, and a lens is named for an approach, never for a person or a brand.

Food safety is not a lens. It is a constraint on all of them, and a number such as a safe temperature comes from a cited standard, never from a lens.

The same pattern works outside the kitchen, and I use it for home design too. [`docs/council-pattern.md`](docs/council-pattern.md) describes the reusable parts.

## Rules the agents follow

This is a summary for people. [`AGENTS.md`](AGENTS.md) holds the rules the agents follow, and where the two differ, that file is right.

- **Your latest correction beats a saved card.** The agent names the conflict, follows the correction, and updates the card.
- **Status is several separate facts:** how far a recipe has been developed, whether it has been cooked, whether the card is saved, and whether any copy outside the repository is up to date. Writing a card does not make it cooked, and cooking it once does not make it a house recipe. Only you promote a recipe.
- **The old version stays when a new one is tested.** A small edit is a version bump on the same card. A changed technique, cut, or appliance is its own card.
- **Lenses, not people.** Advice is attributed to a lens. No agent says that a chef said, approved, or would do anything, and none invents a quotation.
- **Food safety is a constraint.** Safety numbers come from the dated food-safety reference, and the stricter ones apply when you cook for someone at higher risk.
- **Every recipe change gets an independent editor check.** The agent that wrote a card never grades it. A failed check blocks the change.
- **Nothing is invented:** no quantity, time, temperature, cook outcome, allergy, or source. A missing number is marked as missing.
- **No third-party recipe text is copied,** and a source is credited only when it was actually read.
- **No save, sync, or check is reported unless it happened.**

## Make it yours

1. Fill in the three files that [`kitchen/README.md`](kitchen/README.md) lists, or let your agent interview you. Say whether you ever cook for someone at higher risk from foodborne illness; the safety numbers tighten when you do.
2. Edit the roster if you want different lenses, for example one for the cuisine you cook most. The vetting rule above says how.
3. Keep the two example recipes, or delete their cards under `recipes/` and their reports under `qc/`, then run `python3 scripts/build-index.py`. The links to the examples in this README, in the history page, and in the behavior checks then lead nowhere, so remove them or point them at your own cards.
4. After any change to `kitchen/`, a skill, `method/`, or `templates/`, run `scripts/build-chat-bundle.sh`. CI fails when `chat/bundle.md` is out of date, even if you never use a chat app.
5. In your fork's Actions tab, enable workflows, so the checks run on your pull requests. Optionally run `scripts/install-git-hooks.sh` once to run the editor gate and the card linter before each commit.
6. If you read recipes in a notes app, [`adapters/README.md`](adapters/README.md) says how an agent mirrors a card there.

Everything you commit to a public fork is public, including `kitchen/` and its history. You never have to name anyone or give a medical detail.

The food-safety numbers follow United States federal guidance. They are dated, with a refresh-by date, in [the food-safety reference](.agents/skills/chef-council/references/food-safety.md), which also says what to do in another country.

## Example recipes

- [Butter-Roasted Carrots with Jaggery and Sumac](recipes/sides/butter-roasted-carrots-with-jaggery-and-sumac.md): a restrained roast where the sugar goes on after the oven. Its status is reviewed and its kitchen evidence is untested: it has not been cooked as written, and the card says so. [Its editor report](qc/sides/butter-roasted-carrots-with-jaggery-and-sumac/2026-11-19.md).
- [Council Tuna Melt](recipes/sandwiches/council-tuna-melt.md): reviewed, with kitchen evidence not recorded. One variation was cooked once, before this repository existed, and no cook log of it was written, so the card does not count it as a logged cook. [Its editor report](qc/sandwiches/council-tuna-melt/2026-11-19.md) passes, and three of its remarks are inaccurate; [what the example report gets wrong](docs/how-this-was-built.md#what-the-example-report-gets-wrong) lists them.

## Check your setup

[`evals/behavior-checks.md`](evals/behavior-checks.md) holds scenarios such as "the card says one thing; didn't we change that?" and "did a famous chef approve this?" (the answer is no). Each one gives a prompt, the behavior to expect, and the red flags. Run a few after you set up, and again after you change the rules or the roster.

## How this was built

It started in July 2026 as a council of named chefs inside one agent, publishing straight to a notes app. In October 2026 it became plain files any agent can read, when I moved it between tools and found the knowledge stuck in one chat. In November 2026 it gained the independent editor, and the first card through the check failed: the card put the first temperature check five minutes later than I had agreed, and the cook log described equipment I never mentioned. The editor caught both before anything was published. This repository was then built fresh from my private cooking repo, with the personal details left out. Until November 19, 2026, the lenses carried the names of real cooks and publishers. That decision was superseded on that day, and each lens now carries a description of its approach. The full timeline, and the incident behind each rule, is in [`docs/how-this-was-built.md`](docs/how-this-was-built.md).

## License

MIT. See [`LICENSE`](LICENSE).
