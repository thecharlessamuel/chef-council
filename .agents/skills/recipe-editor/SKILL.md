---
name: recipe-editor
description: Independently checks a new or changed recipe card one for one against the verbatim source packet the cook approved, and writes an editor report with a PASS, PASS WITH NOTES, or FAIL verdict, a discrepancy table, and the hash of the card it read. Never edits a recipe. Use after any recipe card is added or changed and before it is committed, and only in a fresh context that did not write the card.
---

# Recipe Editor

The editor exists because the agent that writes a recipe card is the wrong one to check it. You compare the card with the exact text the cook approved and write down every place where they differ. You do not improve the card, defend it, or fix it.

Paths in this file are relative to the repository root, except `references/report-format.md`, which sits beside this file.

## Before you start

1. **Check that you are independent.** You are independent only when you did not write or change the card, and the conversation in which it was written is not in your context. If you wrote the card, or you can see the writer's reasoning about it, stop. Write no report and give no verdict. Reply with one line that starts `Not independent:` and gives the reason, and tell the cook to start a fresh agent, a new session, or a new chat. The four headings under What to tell the writer do not apply to that reply. Never certify your own work.
2. **Find your two inputs.** They are the source packet, at `.sources/<slug>/<YYYY-MM-DD>.md`, and the card, at `recipes/<category>/<slug>.md`. Whoever asked for the check gives you both paths. If one is missing from what you were asked, ask for it. Do not pick a packet yourself, because a card can have several. If you were also given the writer's summary, explanation, or opinion of the card, do not use it. The packet and the card are the evidence.
3. **Check that the packet is usable.** `templates/source-packet.md` shows its form. A usable packet holds the approved text itself between the tilde lines under `## Approved text`, and the cook's own words under `## Scope instruction`. When there is no packet, or it holds a summary, a description, or the template's own text where the approved text should be, you have nothing to compare the card with. The verdict is then `FAIL`, with the one discrepancy `no verbatim source`, and you still write the report.
4. **Read the rules.** Read `method/status-and-versions.md`, which the card's version, status, and evidence are held to, and `references/report-format.md`.

## Compare the card with the packet

Go through the approved text one item at a time and find each item on the card. Then go through the card one line at a time and find where each line came from. Rewording a step is allowed, and so is arranging the recipe into the card's tables and headings. Changing what gets cooked is not.

- **Ingredients.** Every ingredient in the approved text is on the card with the same amount, unit, and prep. An amount that is divided between two uses adds up to the approved total. The card adds no ingredient and drops none. A converted unit is a difference, unless the cook asked for the conversion.
- **Method.** Every step is on the card, in the same order, with the same heat, temperature, time, size, pan or pot, cue, and doneness check. The card adds no step and drops none.
- **Equipment, yield, and time.** Each one matches the approved text.
- **Gaps.** Where the approved text leaves out something a cook needs, the card says `Not stated.` in its place, lists the gap under Notes, and has the status `draft`. A number on the card that the approved text does not hold was invented.
- **The other sections.** Why this works, Failure modes, Variations, Storage, Notes, and Next experiment hold what the approved text or the cook's instruction says, or `None recorded.` Anything else there is an addition by the writer. List each addition in the report, and treat one that could change what a cook does as a discrepancy.
- **An update or a new variant.** Compare the card with the previous version in the packet as well. Every difference between the two traces to a correction in the approved text or to the scope instruction. A difference that nobody asked for is a discrepancy, even when it reads like an improvement.
- **Version, status, and evidence.** The version is the one `method/status-and-versions.md` gives for this kind of save. The status and the kitchen evidence are no higher than that page allows. Count the cook logs the way that page says. If you can list files, read the logs in `cook-logs/<slug>/` themselves. If you cannot, read the logs the packet lists. The block at the top of the card and the lines under its title agree with each other.
- **Source and people.** The Source line credits only what the packet shows the recipe came from. The card does not say or suggest that any person reviewed, approved, endorsed, or wrote it, and it does not name a lens as an author or a source.
- **The index.** `recipes/INDEX.md` has a row for the card with the card's version, status, and evidence. If you can run commands, `python3 scripts/build-index.py --check` tells you whether the index is current.
- **The scope.** The save is the kind the cook's scope instruction asked for: a new card, a change to a saved card, or a separate version.

## Decide the verdict

Give every discrepancy one of two severities.

| Severity | What it covers |
|---|---|
| `blocking` | The card would have a cook do something the approved text does not say: a different amount, unit, ingredient, step, order, time, temperature, or doneness check. Or the card states something the packet does not support: an invented number, a status or an evidence value higher than the rules allow, a credit to a source or a person, or a difference from the previous version that nobody asked for. Or there is no verbatim source. |
| `minor` | Anything else worth fixing that changes nothing a cook would do and claims nothing untrue: wording, a label, the layout, or an index that needs regenerating. |

- One or more blocking discrepancies: the verdict is `FAIL`.
- Minor discrepancies only: the verdict is `PASS WITH NOTES`.
- No discrepancy: the verdict is `PASS`.

When you cannot tell whether a difference changes what gets cooked, it is blocking, and the report says what you could not settle. Do not pass a card because its differences are few, and do not fail one because a step was reworded.

## Write the report

Write one file, the report, at the path and in the form `references/report-format.md` gives. Write nothing else.

- Never edit the card, the packet, the index, a cook log, or any other file, even to fix something small. A fix is the writer's job, and a fixed card needs a fresh check.
- Never commit, push, or open a pull request.
- If you cannot write files, return the complete report with its path for the cook to save, and say that nothing was saved.

## What to tell the writer

Reply under these four headings, in this order:

1. `## Verdict`: the report's `VERDICT:` line and nothing else.
2. `## Report`: the path of the report you wrote. If you wrote none, `Not written:` with the reason, then the complete report.
3. `## Discrepancies`: the table from the report, or `None.`
4. `## Next step`: the one thing that happens next, and who does it. After a `FAIL`, the writer fixes the card from the packet, and a fresh editor, not you, checks it again. After a `PASS` or a `PASS WITH NOTES`, the writer commits the card, the index, and this report together. Fixing a note changes the card, and a changed card needs a fresh check before it is committed.
