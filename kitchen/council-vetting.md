# The vetting rule

A lens is seated on the council only when the `kitchen/vetting/` folder holds a record for it whose verdict is `seat` or `seat narrower`. The record is what the lens is allowed to know. A lens argues only from the tendencies its record lists and only inside its recorded scope. A lens is a described cooking approach. It is not a person, it is not named for one, and it does not speak for anyone.

## What a record holds

One file per lens, `kitchen/vetting/<slug>.md`, copied from [`templates/lens-vetting-record.md`](../templates/lens-vetting-record.md):

- **The lens's name**: two or three words that describe its approach, then the word `lens`, such as `Weeknight speed lens`. It is never a person's name, a brand, or the form `<Name>-style lens`.
- **Its seat, its job, and its scope**: `core` or `specialist`, the job the lens does on the council, and what it may argue about.
- **Three to five tendencies**: what the lens holds about cooking, each one a way of working that a cook could follow or decline, written in this repository's own words. These are all the lens may reason from.
- **The one question the lens always asks.**
- **Where the lens can mislead**: where advice argued from those tendencies goes wrong for a home cook, and what to check when it does.
- **A verdict**: `seat`, `seat narrower` (with the scope the lens is held to), or `cut`, and the reason.
- **The date the record was last checked.**

## Rules for writing a record

1. Name no one. A record names no person, publication, outlet, show, book, product, or brand, and it holds no web link. Describe the approach, not where it came from.
2. Write no quotations. A record never says that anyone approved, endorsed, or took part in this repository, because no one did.
3. Copy no recipe text from any publisher: no ingredient lists, methods, or headnotes.
4. Cut a lens that has no job of its own: one whose job a seated lens already does, or one whose tendencies cannot be written without naming someone. A cut record stays in `kitchen/vetting/` so the lens is not proposed again without a new reason.
5. Numbers do not come from a lens. A safe temperature, a ratio, a pressure-cooker minimum, or a nutrition figure comes from a cited standard, a tested source, or the equipment manual. Food safety is a constraint on every lens, not a seat.

## When someone asks for a person or a brand

Asked to add a named cook, author, publisher, show, or brand to the council, seat no name. Say that the council's lenses are named for approaches and not for people, and ask what about that cooking the cook wants the council to weigh. Then offer a lens for that approach, with a descriptor for its name, and write its record by the rules above, or decline and give the reason. Write nothing about the person, quote nothing, and never say that a lens is that person or speaks for them.

## Seating, changing, and removing a lens

- **To add a lens:** copy the template, fill the record in, and reach a verdict. When the verdict seats the lens, add its entry to [`council.md`](council.md) under the heading that matches the record's `seat`, repeating the record's `lens`, `job`, `question`, and `scope` word for word.
- **To change a lens:** change its record first, then its roster entry, and give the `checked` field the new date.
- **To remove a lens:** delete its roster entry, and either delete the record or set its `verdict` to `cut` and its `scope` to `none`.

Then run the check, which CI also runs:

```bash
python3 scripts/check-council.py
```

It fails when a record is missing a part, when a record holds a web link or a lens is written `<Name>-style lens`, when the roster seats a lens without a seated record, when a seated record is missing from the roster, and when the two disagree.
