# Sync map

One row for each copy of a card outside the repository. [`README.md`](README.md) is the contract for writing a row, and it lists the four states. This file ships empty: add a row only after a destination has returned an ID.

- **Card:** the card's path, such as `recipes/sides/roasted-carrots.md`.
- **Destination:** the adapter's short name, such as `mem`.
- **External ID:** the ID the destination gave for the copy. Only the ID: never a link, a password, a token, or a key.
- **Version copied:** the card's version when the copy was last written, such as `v1.1`, or `unknown` for a copy that was found and not yet written by a sync.
- **Read back:** the date the copy was last fetched and compared with the card, as `YYYY-MM-DD`, or `never`.
- **State:** `current`, `stale`, `unverified`, or `failed`.

| Card | Destination | External ID | Version copied | Read back | State |
|---|---|---|---|---|---|
