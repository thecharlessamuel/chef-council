# The vetting rule

A lens that carries a real person's or publisher's name is seated on the council only when the `kitchen/vetting/` folder holds a record for it whose verdict is `seat` or `seat narrower`. The record is what the lens is allowed to know. A lens argues only from the tendencies its record lists and only inside its recorded scope. It is a way of reading published work. It is not the person, and it does not speak for them.

## What a record holds

One file per name, `kitchen/vetting/<slug>.md`, copied from [`templates/lens-vetting-record.md`](../templates/lens-vetting-record.md):

- **The official site**, with the date it was checked. When there is none, or none could be opened, the record says `No official site`, the access notes say which, and the record needs a second independent source.
- **Two or more named published works** that are relevant to the seat: books, a column, a series, or a recipe archive, each with a link and the date checked.
- **At least one independent source**: something written by someone other than the person and the publisher of the work, such as a review, a profile of the work, an award listing, or a book by someone else, that confirms what the seat assumes. A publisher's description reprinted on another site is not independent.
- **Three to five tendencies the published work shows**, written in this repository's own words. These are all the lens may reason from.
- **The one question the lens always asks.**
- **Where the lens can mislead**: where advice argued from those tendencies goes wrong for a home cook. This is about the lens. Nothing here judges the person.
- **A verdict**: `seat`, `seat narrower` (with the scope the lens is held to), or `cut`, and the reason.
- **Access notes**: what was not read, what was behind a paywall, and what is known only from a search result.

## Rules for writing a record

1. Cite only pages that were opened and read in the session that wrote the record, each with the date. A search result is not a page that was read.
2. Describe published work, never personal life.
3. Write no quotations. Tendencies are paraphrase, in your own words, and titles are set in italics. A record never says that anyone approved, endorsed, or took part in this repository, because no one did.
4. Copy no recipe text from any publisher: no ingredient lists, methods, or headnotes.
5. Cut a name whose relevant published work cannot be verified. A famous name with no evidence in the seat's specialty is a cut, with the reason in the record. A cut record stays in `kitchen/vetting/` so the name is not proposed again without new evidence.
6. Numbers do not come from a lens. A safe temperature, a ratio, a pressure-cooker minimum, or a nutrition figure comes from a cited standard, a tested source, or the equipment manual. Food safety is a constraint on every lens, not a seat.

## Seating, changing, and removing a lens

- **To add a lens:** copy the template, read the sources, fill the record in, and reach a verdict. When the verdict seats the lens, add its entry to [`council.md`](council.md) under the heading that matches the record's `seat`, repeating the record's `lens`, `job`, `question`, and `scope` word for word.
- **To change a lens:** change its record first, then its roster entry. Open the record's links again and give every citation and the `checked` field the new date.
- **To remove a lens:** delete its roster entry, and either delete the record or set its `verdict` to `cut` and its `scope` to `none`.
- **A lens with no real name** (for example a budget lens or a weeknight lens) follows the same steps. Its record cites the published work it leans on.

Then run the check, which CI also runs:

```bash
python3 scripts/check-council.py
```

It fails when a record is missing a part, when the roster seats a lens without a seated record, when a seated record is missing from the roster, and when the two disagree.

## When a record goes stale

Links move and published work changes. A record is evidence as of its `checked` date. Before leaning on a record that is more than a year old, open its links again and update the dates, the tendencies, and the access notes.
