# Source packet: Recipe title

- **Card:** recipes/category-folder/recipe-slug.md
- **Kind of save:** new card, update, or new variant
- **Date:** YYYY-MM-DD
- **Where the approved text came from:** For example, this conversation on YYYY-MM-DD, or a file the cook pasted.

Copy this file to `.sources/<slug>/<YYYY-MM-DD>.md` and replace every line. The `.sources/` folder is ignored by git, because a packet can hold private conversation text or a publisher's recipe: never commit one. A second packet for the same card on the same day ends in `-2`.

The one rule: paste the approved text verbatim; never summarize. The editor compares the card with this packet one for one, so a packet that was tidied, shortened, or retyped from memory makes the check worthless. Put each pasted part between two lines of four tildes, as below. If the text itself holds a line of four or more tildes, use longer lines of tildes around it. Keep the title, the four lines above, the four headings, and the tilde lines. Delete these two paragraphs and the sentence of instruction under each heading when the packet is filled in.

## Approved text

Everything the cook approved, exactly as approved: the whole recipe for a new card or a new variant, or the exact corrections for an update.

~~~~
Paste here.
~~~~

## Scope instruction

The cook's own words about what to save and how, such as whether this is a new card, a change to a saved one, or a separate version to test.

~~~~
Paste here.
~~~~

## Previous version

For an update or a new variant, the saved card as it stands on the default branch, pasted whole, with a line above the tildes naming the commit it was read from. For a new card, write `None: this is a new card.` and delete the tildes.

~~~~
Paste here.
~~~~

## Paths

- Card: recipes/category-folder/recipe-slug.md
- Previous card: the path and commit of the previous version, or none
- Cook logs: each cook log this save relies on, or none
- Index: recipes/INDEX.md
- This packet: .sources/recipe-slug/YYYY-MM-DD.md
