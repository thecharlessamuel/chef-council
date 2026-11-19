---
name: recipe-codify
description: Turns a recipe the cook approved into a standalone recipe card from templates/recipe-card.md, assigns the version, sets an honest status and kitchen-evidence line, regenerates the recipe index, and saves a verbatim source packet for the independent editor check. Use when someone asks to save a recipe, make a card, make a separate second version, record a change to a saved card, or calls a recipe final.
---

# Recipe Codify

Codifying writes down what the cook approved. It does not improve the recipe, fill its gaps, or decide what the cook meant. If the recipe still needs work, that is the council's job, not this skill's.

Paths in this file are relative to the repository root.

## Before you write

1. **Find the approved text.** It is the complete recipe the cook approved, or, for a change to a saved card, the cook's exact corrections. It may come from the chef-council skill's hand-off, under its `## Approved text` heading, or from the cook directly. If you cannot point to the text and to the cook approving it, ask. Never rebuild a recipe from memory or from a summary.
2. **Find the scope instruction.** The cook's own words about what to save: a new card, a change to a saved one, or a separate version to test. The cook sets the scope. If the cook has not said, ask that one question and wait.
3. **Read the rules.** Read `method/status-and-versions.md`. For a change to a saved card, find the card in `recipes/INDEX.md` and read it and its most recent log in `cook-logs/<slug>/`.
4. **Check the standing corrections** in `kitchen/profile.md`. If the approved text conflicts with one, name the conflict and ask the cook which stands before writing anything. A profile whose `filled_in` line is not exactly `filled_in: yes` is a blank template: it holds no corrections, and it is no reason to stop or to interview the cook before saving.

## Decide the kind of save

| The cook wants | Kind | What you write |
|---|---|---|
| A recipe that has no card | New card | `recipes/<category>/<slug>.md` at `v1.0` |
| A change to a saved card | Update | The same file, with the version `method/status-and-versions.md` gives for that change |
| A changed technique, cut, or appliance, or a version to test beside the original | New variant | A new file, the original's slug with `-v2` at `v2.0`, or the next unused number. Do not touch the original |
| A status or evidence change and nothing else, such as a cook recorded on a saved card, or the cook making a recipe `house` or `retired` | Update | The same file at the same version, with the new value and a changelog line that starts with the version and the date |

When the cook's instruction and the version table disagree, say what the table would do, then follow the cook. Only the cook makes a recipe `house` or `retired`, and `house` needs a logged cook.

## Write the source packet first

Copy `templates/source-packet.md` to `.sources/<slug>/<YYYY-MM-DD>.md`, using today's date, and fill it in before you write the card. Then write the card from the packet, not from your memory of the conversation.

- Paste the approved text verbatim; never summarize. Do not tidy it, reorder it, fix its spelling, or convert its units.
- Paste the scope instruction in the cook's own words.
- Put each pasted part between two lines of four tildes, or longer lines of tildes when the text itself holds a line of four or more.
- For an update or a new variant, paste the saved card whole as it stands on the default branch, `main` unless the repository uses another: `git show main:recipes/<category>/<slug>.md` prints it, and `git rev-parse main` prints the commit to name. If the card is not on the default branch yet, or you cannot run git, paste the file as it stands and say in the packet which of the two it is.
- List the paths the template asks for.
- Never commit a packet. Git ignores `.sources/` because a packet can hold private conversation text or a publisher's recipe.

## Write the card

Copy `templates/recipe-card.md` to `recipes/<category>/<slug>.md` and replace every line.

- **Slug and category.** Make the slug from the title as `method/status-and-versions.md` says under Names and places. No two cards share a slug, whatever their categories, so look at the card files in every folder under `recipes/` first, not only at the index. Use the category the cook names, made into a folder name the same way a slug is made. If the cook names none, use the folder that already holds similar cards, or ask.
- **The block at the top.** Write `id`, `version`, `status`, `evidence`, `category`, and `mirrors` as plain words with no quotation marks. `id` is the slug and `category` is the folder. The lines under the title repeat the version, status, and evidence, and the two must agree. The date is today's.
- **The recipe itself.** Equipment, Ingredients, Method, Yield, and Time carry what the approved text says and nothing else. Every ingredient keeps its amount, unit, and prep. Every step keeps its order, heat, time, cue, and doneness check. You may reword a step and arrange the recipe into the template's tables. A cue the approved text gives outside its steps, such as under a Cues heading, goes word for word into the step it describes, beside that step's own cue. A cue that describes no step goes under Notes. Use a `###` component or stage line only when the approved text has more than one component or stage, and add no step: the template's three steps show the form of a step. You may not change what gets cooked.
- **Do not invent.** Never add a quantity, a time, a temperature, an ingredient, or a step. Never convert a unit unless the cook asks for it. Where the approved text leaves out something a cook needs, write `Not stated.` in its place, list it under Notes as open, and set the status to `draft`.
- **The other sections.** Why this works, Failure modes, Variations, Storage, Notes, and Next experiment hold only what the approved text or the cook said. Under a heading with nothing to hold, write `None recorded.` Do not write new advice into a card.
- **Source.** Write `Original.` for a recipe developed here. Credit a published source by title and link only when it was actually read, as `adapted from` or `technique informed by`. A lens is never an author or a source, and no card says a person reviewed or approved it. Do not copy a publisher's ingredient list, method, or headnote into a card: when the approved text is a publisher's recipe, say so and ask the cook what of their own to save.
- **Status and evidence.** Take both from `method/status-and-versions.md`. A new card is `reviewed` when nothing is open, the cook approved the text, and the recipe was checked for coherence, which the cook's word or a chef-council hand-off with every Ready to save line at `yes` shows. Otherwise it is `draft`. Evidence counts the logs in `cook-logs/<slug>/` as that page says: read each log's Recipe line and count the ones that name the card's current version, plus an earlier one only when the changelog line for the current version names it. When the cook says they cooked the recipe and there is no log, the cook-log skill writes the log first; use `not-recorded` only when the cook cannot give a day or a report to log. Never raise either value on your own.
- **Changelog.** Add one line for this save: the version, the date, what changed, and why. For a new card, say whether it has been cooked. When `cook-logs/<slug>/` holds a log written before the card, name that log by its path in this line, which is what lets it count.

## Regenerate the index

Run `python3 scripts/build-index.py`. It rewrites `recipes/INDEX.md` from the cards and prints `index written:` with the number of cards. Never edit the index by hand. If it prints a problem with a card, fix the card and run it again. If you cannot run commands, say that the index was not regenerated and give the cook the command.

## Hand off to the editor

A card is not checked by the agent that wrote it. Hand the packet's path and the card's path, and nothing of your own reasoning, to the recipe-editor skill listed under Skills in `AGENTS.md`, run by a fresh agent that did not write the card.

- If no such skill is listed there, or you cannot start a second agent, say that the editor check has not been run and give the packet's path. Do not write a report yourself, and do not call the card checked, verified, or approved.
- On a failed check, fix the card from the packet and ask for a fresh check.
- Until a check passes, do not commit the card, open a pull request, or copy the card anywhere outside the repository. If the check cannot be run, leave that decision to the cook.

## Save

Save after a passing check. When the check could not be run and the cook then tells you to save anyway, follow the same steps, and say in the commit message and in the pull request that the editor check was not run. Never save after a failed check.

- Work on a branch, and never push `main`. Use the branch the cook names, or create one named for the card, such as `card/roasted-carrots`.
- Commit the card, the regenerated index, any new cook log, and the editor's report when there is one, together, with a subject such as `Add the roasted carrots card v1.0`.
- Open a pull request against `main`. The cook merges it.
- When the cook works alone and asks for no pull request, commit on the branch the cook names and stop there. The cook pushes.
- Copy a card to a notes app only when the cook asks or calls the recipe final. `mirrors` stays `none` until a copy has been written and read back.

## What to tell the cook

Reply under these four headings, in this order:

1. `## Files written`: each file you wrote, with its path, and each file you did not write, with the reason. Never list a file you have not written.
2. `## Status`: four lines. Development and Kitchen evidence, as the card states them. Saved: the stage the card has reached, which is `written`, `committed` with the branch, `in a pull request`, or `merged`. Mirrored: `none`, or each copy and whether it was read back.
3. `## Editor check`: who the card was handed to and the result, or `Not run:` with the reason and the packet's path.
4. `## Next step`: the one thing that happens next, and who does it.

If you cannot write files, return the complete card and the complete packet, each with its path, for the cook to save, give the index command, and say that nothing was saved.
