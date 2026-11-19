# Adapter: Mem

A worked example of the [sync contract](README.md) for Mem, a notes app. It holds no ID, link, or collection name from any account, and yours do not belong in it either: an ID goes in [`sync-map.md`](sync-map.md) and nowhere else.

This repository is not affiliated with Mem. The tool names below are the ones the Mem connector offered to an agent when this page was written, read from the connector's own tool list on 2026-11-19. Connectors change. Go by the tool list your agent has, and if a tool named here is gone, find the one that does the same job before you go on.

- **Destination name:** `mem`
- **What a copy is:** one note. Mem takes a note's title from the first line of its content, so the card's title line becomes the note's title, as it is.

## The six rules in Mem

1. **Search before creating.** Look for a `mem` row for the card in the sync map. If there is none, run `search_notes` with the card's title, and look for a note whose title is exactly the card's title. The search is ranked and bounded, so it can miss a note. That is why the sync map comes first.
2. **Store the external ID.** `create_note` returns the new note's ID. Write the sync-map row with that ID and the state `unverified` before the next step.
3. **Read the live version before updating.** `get_note` with the ID returns the note as it stands and its `version`. `update_note` needs that `version`, so an update without a fresh `get_note` is not possible. Compare what `get_note` returned with the card at the version in the row. If the note says it is in the trash, stop and ask the cook.
4. **Never create a duplicate as a retry.** If `create_note` fails or times out, run `search_notes` again. If it still finds nothing, tell the cook and ask before a second `create_note`. If `update_note` is refused, run `get_note` again and start rule 3 over.
5. **Read back before claiming success.** Run `get_note` with the ID after the write and compare the note with the card. A table or a list that is laid out differently is formatting. What counts is that every ingredient, amount, step, time, and temperature is there and unchanged.
6. **Report each destination separately.** One line for the repository and one for `mem`.

`update_note` replaces the whole note. Send the whole card from its title line to its end, never a part of it.

## Collections

A collection is a named group of notes in Mem. Putting recipe notes in one is optional. If the cook wants it, ask which collection, find it with `search_collections`, and add the note with `add_note_to_collection`. Do not create a collection, or choose one, without being asked. Do not write a collection's name or ID into a card or into this page.

## A worked example

The cook says the roasted carrots are final and asks for a copy in Mem. The card is `recipes/sides/roasted-carrots.md` at `v1.1`, merged, and its latest editor report passes.

1. The sync map has no `mem` row for the card. `search_notes` for "Roasted Carrots" finds no note.
2. `create_note` is called with the card from its title line to its end. It returns an ID.
3. The row goes into the sync map at once:

   | Card | Destination | External ID | Version copied | Read back | State |
   |---|---|---|---|---|---|
   | `recipes/sides/roasted-carrots.md` | `mem` | `<the ID Mem returned>` | `v1.1` | `never` | `unverified` |

4. `get_note` with that ID returns the note. Every ingredient, amount, step, time, and temperature matches the card. The row's Read back becomes today's date and its State becomes `current`.
5. The card's `mirrors` line becomes `mirrors: mem` by the `recipe-codify` skill, and the card gets its editor check.
6. The report to the cook has two lines: the repository, with the stage the change has reached, and `mem: created and read back at v1.1`.

Three weeks later the card is at `v1.2`, and the cook asks for the copy to be brought up to date.

1. The sync map has the row, so nothing is searched and nothing is created.
2. `get_note` with the ID returns the note and its `version`. The note has a line the card never had: the cook typed "double the sumac next time" into it. The agent shows the cook that line and asks. The cook says to leave it out of the copy.
3. `update_note` is called with the ID, the `version` from step 2, and the whole card at `v1.2`.
4. `get_note` again, and the comparison matches. The row becomes `v1.2`, today's date, and `current`.
5. The report: the repository unchanged apart from the sync map, and `mem: updated and read back at v1.2`.
