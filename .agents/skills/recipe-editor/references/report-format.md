# The editor report

One report records one check of one card. The editor writes it, and nobody else changes it afterwards.

## Where it goes

The report for the card `recipes/<category>/<slug>.md` goes at `qc/<category>/<slug>/<YYYY-MM-DD>.md`, named for the day of the check. A second report for the same card on the same day ends in `-2`, and the next in `-3`. Never edit or delete an earlier report. A `FAIL` that was later fixed stays where it is, as the record of what the check caught.

## The form

A report looks like this. Keep the title, the two lines inside the fence, the six labels, and the three headings, and replace everything else.

````markdown
# Editor report: Recipe title v1.0

```text
VERDICT: PASS WITH NOTES
Card-SHA256: 0000000000000000000000000000000000000000000000000000000000000000
```

- **Card:** `recipes/category-folder/recipe-slug.md`
- **Date:** YYYY-MM-DD
- **Kind of save:** new card
- **Source:** this conversation on YYYY-MM-DD
- **Packet:** `.sources/recipe-slug/YYYY-MM-DD.md`
- **Editor:** a fresh agent session that did not write the card

## Discrepancies

| Where | Approved text says | Card says | Severity |
|---|---|---|---|
| Method, step 2 | until crisp-tender | until tender | minor |

## Additions

- Notes: a line on substitutions that the approved text does not hold. It sits outside the recipe.

## Checks run

- Ingredients: checked.
- Method: checked.
- Equipment, yield, and time: checked.
- Gaps: checked.
- The other sections: checked.
- Update or new variant: not applicable, this is a new card.
- Version, status, and evidence: checked.
- Source and people: checked.
- The index: not checked, because no command could be run.
- The scope: checked.
````

## The two lines the gate reads

`scripts/check-qc.sh` reads two lines of a report and nothing else. [`method/recipe-qc.md`](../../../../method/recipe-qc.md) says what it does with them.

- **`VERDICT:`** is followed by one space and exactly one of `PASS`, `PASS WITH NOTES`, or `FAIL`. The skill's `## Decide the verdict` section says which.
- **`Card-SHA256:`** is followed by one space and the SHA-256 of the card file, as 64 lowercase hexadecimal digits. After you have read the card, run `scripts/check-qc.sh --hash recipes/<category>/<slug>.md` and copy the line it prints. If you cannot run commands, use the `Card-SHA256:` line you were given with the card. If you were given none, write `Card-SHA256: not computed` and say in your reply that the cook must run that command and put its line in place of yours, without changing the card.

Each of the two starts a line of its own, with nothing in front of it, and appears once in the report. Never start another line of the report with `VERDICT:` or `Card-SHA256:`.

The hash ties the report to the card as you read it. If the card changes afterwards by even one character, the hash no longer matches, and the report stops counting. That is intended: a changed card needs a fresh check.

## The rest of the report

- **Title.** The card's title and version.
- **Card, Date, Kind of save, Source, Packet.** The card's path, the day of the check, and three lines from the top of the packet: the kind of save, where the approved text came from, and the packet's own path. For Source, say where the text came from, never what it said. When there is no packet, or the packet does not say, write `not stated` for Kind of save and for Source, and for Packet write the path you were given, or `none`.
- **Editor.** What ran the check, such as a fresh agent session. It is never a person's name and never a lens.
- **Discrepancies.** One row for each. Where: the section and the item. Then what the approved text says and what the card says, in as few words as show the difference, and the severity, `blocking` or `minor`. Write `None.` in place of the table when there is none. For a missing or summarized packet, the one row reads `no verbatim source` under Where.
- **Additions.** Each thing on the card that the approved text does not hold, and whether it sits outside the Equipment, Ingredients, and Method. Write `None.` when there is none.
- **Checks run.** One line for each check in the skill's `## Compare the card with the packet` section, in that order, saying `checked`, `not applicable` with the reason, or `not checked` with the reason. With no verbatim source, every check that needs the approved text reads `not checked, because there is no verbatim source`.

## What stays out of a report

A report is committed with the card, and a public fork publishes it. The packet is not committed, because it can hold a private conversation or a publisher's recipe.

- Do not copy the approved text into the report. Quote only the few words a discrepancy turns on.
- Name no person: not the cook, not anyone the cook's words mention, and not a chef. Leave out any health detail.
- Never say or suggest that a person or a lens reviewed, checked, or approved the card. An agent ran this check.
