# Adapters: copies outside the repository

The repository is the home of every recipe card. An adapter is a page that tells an agent how to keep a copy of a card somewhere else, such as a notes app you read from while you cook. Copies are optional, and nothing else in this repository depends on one.

This page is the sync contract, which every adapter follows. [`mem.md`](mem.md) is one worked example, and [`sync-map.md`](sync-map.md) is where an agent records what it copied.

## When a copy is made

- Only when the cook asks for one or calls the recipe final. [`method/status-and-versions.md`](../method/status-and-versions.md) holds that rule, under "Saved and mirrored".
- Only from the card file as it stands in the repository, never from a draft in a conversation.
- Only when the card's latest editor report passes for the card as it now stands: the newest report in the card's folder under `qc/` reads `VERDICT: PASS` or `VERDICT: PASS WITH NOTES`, and its `Card-SHA256:` line is the line `scripts/check-qc.sh --hash` prints for the card. A card with a failed check, an old check, or no check is not copied.
- Only cards. A cook log, a source packet, and an editor report stay in the repository.

## What is copied

The copy is the card from its title line (the line that starts with `# `) to its end, unchanged. The block of fields above the title is for scripts and is left out. The copy's title is the card's title, with nothing added to it.

A destination has a short lowercase name, such as `mem`. That name is what the card's `mirrors` line and the sync map use.

## The sync contract

An agent follows these six rules in this order, for one destination at a time. A copy is found when its title is exactly the card's title. A note that only resembles it is not the copy, and a copy in the trash is still a copy.

1. **Search before creating.** Look in the sync map for a row with this card and this destination. If there is none, search the destination for a copy by the card's title. One copy found, either way, means this is an update of that copy. A copy found only by the search gets its row in the sync map first, with `unknown` as its version, `never` as its read-back, and the state `unverified`. Several found means stop: list them for the cook and ask which one is the copy. Create a new copy only when both looks find nothing.
2. **Store the external ID in the sync map.** As soon as the destination returns the ID of a new copy, write the row in `sync-map.md`, before doing anything else. An ID that is only in a conversation is lost when the conversation ends, and the next sync then creates a second copy.
3. **Read the live version before updating.** Fetch the copy as it stands now, by its ID. If the destination gives a version with it, the update uses that version. Compare it with the card as it was at the version in the row, which git's history of the card file holds. Anything in the copy that is not in that version was put there by hand: show it to the cook and ask before replacing it. When the row's version is `unknown`, show every difference from the current card and ask. If the copy is gone or in the trash, say so and ask. Do not create another without being asked.
4. **Never create a duplicate as a retry.** When a create or an update fails, times out, or returns something you cannot read, find out first whether it landed: read by the ID if you have one, and search if you do not. Retry only what did not land. A search that finds nothing does not prove that a create failed, because a search can miss a new copy: tell the cook what happened and ask before creating again. An update is retried as an update of the same ID, and never as a new copy.
5. **Read back before claiming success.** After a create or an update, fetch the copy by its ID and compare it with the card: every ingredient with its amount, every step, every time and temperature. Formatting that the destination changed is not a difference. A missing or altered line is, and it makes the copy `failed`. A reply that says the write worked is not a read-back, and neither is an ID. Say "synced" only after this comparison.
6. **Report each destination separately.** Say what happened in the repository, in the words of `method/status-and-versions.md`, and then give one line for each destination: created, updated, unchanged, failed with the reason, or not attempted with the reason. Never fold them into one "saved". The report comes last, so that it says what the read-back found.

After a read-back that matches:

- Set the row in the sync map: the version copied, today's date, and the state `current`.
- If the card's `mirrors` line does not name the destination yet, add it by the `recipe-codify` skill. That changes the card, so the card gets its editor check like any other change. It does not change the card's version, so the copy is not stale.

## The sync map

[`sync-map.md`](sync-map.md) has one row for each copy: the card, the destination, the ID the destination gave, the version last copied, the date it was last read back, and a state.

| State | Meaning |
|---|---|
| `current` | The copy was read back and matched the card at the version in the row. |
| `stale` | The card has changed what a cook would do since the version in the row. |
| `unverified` | A copy was written and has not been read back, or the read-back could not be done. |
| `failed` | The last write did not land, or the read-back did not match. |

A row whose version is older than the card's version is stale, whatever its State cell says. The next sync corrects the cell.

The sync map is committed with your cards, so on a public fork it is public. Write only the ID in it: never a password, a token, a key, or a link that carries one. An ID is usually not a secret, but check how your app treats one: if knowing the ID is enough to open the copy, it is a secret. If you would not publish it, keep your fork private.

## What an adapter never does

- Create a copy to see whether a copy exists.
- Say a copy was made, updated, or checked when that step did not run and return a result.
- Write an account's ID, link, or folder name into a card. The card's `mirrors` line names destinations only.
- Change the title or the text of the card on the way out.
- Change the repository's default branch directly. The row in the sync map and the `mirrors` line travel on a branch and a pull request, like any change.

## Adding an adapter

Copy `mem.md` to `adapters/<destination>.md` and rewrite each section for the app: how to search, how to read, how to create, how to update, and how to read back. Put in no ID, link, or folder name from your account. If the app cannot do one of the six rules, such as reading a copy back, say so on the page. The state for that destination then never gets past `unverified`.
