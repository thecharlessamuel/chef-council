---
name: cook-log
description: Records what actually happened when a recipe was cooked, using only what the cook reported and marking everything else as not reported, keeps the writer's inferences apart from the cook's words, and proposes one next controlled change. Use when someone reports back after cooking, such as saying they made it tonight, that it came out dry, or that everyone liked it.
---

# Cook Log

A cook log is the evidence a recipe's status rests on, so it holds what the cook said happened and nothing else. What the recipe recommended is not evidence, and neither is what probably happened.

Paths in this file are relative to the repository root.

## Before you write

1. **Find the card.** Look the recipe up in `recipes/INDEX.md` and read the card, so you know its slug and the version that was cooked. A dish with no card can still be logged: make the slug from the dish's name as `method/status-and-versions.md` says under Names and places, and write `No card yet.` on the Recipe line.
2. **Find the date of the cook.** Use the date the cook gives. Work out a date such as last night from today's date when you know it. If you cannot tell the date, ask, because the file is named for it. The Reported line holds the day the cook told you, which is today unless the cook says otherwise.
3. **Gather the report.** The report is everything the cook has said about this cook in the conversation. Nothing else goes into the log as fact.

## Write the log

Copy `templates/cook-log.md` to `cook-logs/<slug>/<YYYY-MM-DD>.md`, named for the day of the cook, and replace every line. A second cook of the same recipe on the same day ends in `-2`. Keep the template's title, its three top lines, its four headings, and its ten labels, in their order, and delete its sentences of instruction, so that each heading holds only what you wrote.

Under `## What the cook reported`:

- Each line holds the cook's own words inside straight double quotation marks, or `Not reported.` and nothing else. No paraphrase, no summary, and no words of yours beside a quotation.
- A quotation is an exact, unbroken piece of what the cook wrote, with the cook's spelling and units. Quote as much as the line needs, and put two pieces on one line as two quotations. Write a double quotation mark inside the cook's words as a single one.
- Never fill a line from the recipe card. If the card says twelve minutes and the cook did not mention the time, the line is `Not reported.`
- Write the log from what you have. Do not hold it back to ask for more: the reply lists what was not reported, and the cook can add to it.
- A log is committed with the repository, and a public fork publishes it. When the cook's words name a person or give a health detail, quote the part that leaves it out, or ask the cook before writing it down.

Under `## Inference`, write what you concluded and the cook did not say, such as a likely cause. Start each line with `Inference:` and say what it rests on. Write `None.` when you have nothing to add. An inference never moves up into the report.

Under `## Next controlled change`, give one change on one line, so that its effect can be seen at the next cook. When the idea is the cook's, the line is the cook's words in quotation marks and nothing else. When it is yours, the line starts with `Proposed:`. Write `None proposed.` when the cook wants the recipe left alone or nothing suggests a change. Advice on how to run the change belongs in your reply, not in the log.

## Card follow-up

This skill never changes a recipe card. Under `## Card follow-up`, write what the card needs:

- **Evidence.** The kitchen-evidence value the card holds now and the one it should hold, such as `untested` to `cooked-once`, counted as `method/status-and-versions.md` says: this log and each earlier log in `cook-logs/<slug>/` whose Recipe line names the same version. For a dish with no card, write `No card yet.`
- **Changes the cook asked for.** Each one in the cook's words, in quotation marks, or `None requested.`

The card is changed through the recipe-codify skill listed under Skills in `AGENTS.md`, which takes the change through the editor check. Only the cook makes a recipe `house`. Never raise a status because a cook went well.

## Save

Write the file and stop. Do not commit it in the same turn: a log travels with the card's change when there is one, and otherwise the cook says when to commit it, on a branch and never on `main`.

## What to tell the cook

Reply under these four headings, in this order:

1. `## Logged`: the path of the log, and that it is written and not committed. If you cannot write files, return the complete log with its path for the cook to save, and say that nothing was saved.
2. `## Not reported`: the labels that hold `Not reported.`, so the cook can fill in any that matter.
3. `## Next controlled change`: the one change, as the log has it.
4. `## Card follow-up`: what the card needs, and that the recipe-codify skill makes the change.
