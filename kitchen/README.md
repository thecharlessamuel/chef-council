# Your kitchen

These three files are the only ones you need to edit to make this repository yours. They tell every agent who it is cooking for and what it has to work with, so its advice fits your kitchen instead of an imagined one. Filling them in takes about ten minutes, and you can ask your agent to interview you and write them for you.

## Fill them in, in this order

1. [`profile.md`](profile.md): who you cook for, what matters most, constraints such as allergies, whether anyone at the table is a higher-risk diner, your units, and your standing corrections.
2. [`equipment.md`](equipment.md): what you cook with, and the limits your manuals state.
3. [`pantry.md`](pantry.md): a dated snapshot of what you usually have.

Each file starts with a short block of fields between `---` lines. When you have filled a file in, set `filled_in: yes` and put today's date, as `YYYY-MM-DD`, in the date field. Until then agents treat the file as blank and ask you instead of assuming.

## How to fill them in

- Write only what is true today. Leave a line blank, or write "unknown", instead of guessing.
- Replace the example rows and the text in italics. Delete rows you do not need.
- Keep a preference tied to the dish it came from. "No raisins in the rice pilaf" is not a general dislike of raisins.
- Change these files whenever your kitchen changes, and update the date.

## The council

[`council.md`](council.md) is the roster of lenses your agent consults, and the `vetting/` folder holds the record behind each one. They work as they are. To add a lens, narrow one, or remove one, follow [`council-vetting.md`](council-vetting.md).

## Before you publish a fork

If your fork is public, these files are public too, along with their history. You do not have to name anyone or give a medical detail: "two adults and a small child" and `higher_risk_diners: yes` tell an agent all it needs.
