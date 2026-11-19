# Status and versions

A recipe card answers two questions that are easy to blur: how good is this recipe, and what is the current version of it. This page is the rule for both. The `recipe-codify` skill applies it when a card is written, and the `cook-log` skill applies it after a cook.

## Status is four separate facts

A recipe can be written down and never cooked. It can be cooked and loved and still be sitting unsaved in a conversation. So "done" is never one word. Each of these is reported separately, and none of them is inferred from another.

| Fact | Where it is recorded | Values |
|---|---|---|
| Development | The card's `status` line | `draft`, `reviewed`, `testing`, `house`, `retired` |
| Kitchen evidence | The card's `evidence` line | `untested`, `cooked-once`, `repeated`, `not-recorded` |
| Saved | Git: the working tree, a branch, a pull request, or the default branch | `written`, `committed`, `in a pull request`, `merged`. It is not written on the card |
| Mirrored | The card's `mirrors` line names each copy outside the repository | `none`, or the destinations, separated by commas |

### Development

| Value | Meaning | Who sets it |
|---|---|---|
| `draft` | Written down, with something still open: a missing quantity, a step nobody has checked, a question for the cook | The default for a new card with anything open |
| `reviewed` | Complete and checked for coherence, for example by a pressure test. It has not been proven by cooking | The writer of the card, when nothing is open, the cook approved the text, and the cook's word or a council hand-off shows the recipe was checked |
| `testing` | Being cooked to settle a named question, which the card states under Next experiment | The cook, or the writer when the cook asks to test a change |
| `house` | The cook's keeper | Only the cook, and only for a recipe with at least one logged cook |
| `retired` | No longer made. The card stays | Only the cook |

Reviewed does not mean proven, and a recipe does not have to be cooked many times before it is worth saving. A `testing` card is useful. It is just not a `house` recipe yet.

### Kitchen evidence

Kitchen evidence counts the cook logs in `cook-logs/<slug>/` for the recipe as the card now states it.

| Value | Meaning |
|---|---|
| `untested` | No logged cook of the recipe as the card now states it |
| `cooked-once` | One logged cook |
| `repeated` | Two or more logged cooks |
| `not-recorded` | The recipe has been cooked, but no log says when or how it went. For a recipe brought in from somewhere else |

- A cook counts once it has a log. When the cook reports a cook, write the log first and change the evidence line second.
- Count the logs whose Recipe line names the card's current version. A cook that departed from the card still counts, and the log says how it departed.
- A new version does not inherit the old version's evidence. After a change to what gets cooked, a log of an earlier version counts only when the changelog line for the current version names that log as the cook the change came from. A log written before the dish had a card counts the same way, when the card's first changelog line names it. If no log counts, the card is `untested`.
- Use `not-recorded` only when the cook says the recipe has been cooked and cannot give a day or a report to log.
- Nobody raises a status or an evidence value without a logged cook or the cook saying so.

### Saved and mirrored

Saved has four stages, and a report names the one the card has reached: `written` (the file is in the working tree), `committed` (on a named branch), `in a pull request`, or `merged` (into the default branch). Never name a stage the card has not reached, and never say only "saved".

A mirror is a copy outside the repository, such as a note in a notes app. A card is mirrored only when the cook asks or calls the recipe final. The `mirrors` line names the destinations and never holds an account's ID or URL. A copy counts only after it was read back and compared, and each destination is reported separately.

## Versions

A card's version is written `vX.Y`, starting at `v1.0`. The number after the point counts up one at a time and does not roll over: the version after `v1.9` is `v1.10`.

| What changed | Result |
|---|---|
| Wording, layout, or a typo, with nothing a cook would do differently | Same version. The commit records it |
| A quantity, a time, a temperature, an ingredient, a step, the yield, the source credit, or a note a cook relies on | The same card, one minor version up (`v1.0` to `v1.1`), with a changelog line saying what changed and why |
| The technique, the cut, or the appliance, or a variant the cook wants to test beside the original | A new card. The original stays as it is |
| The status or the evidence, and nothing a cook would do differently | Same version, with a changelog line that starts with the version and the date |
| Promotion to `house` | Only the cook decides, and only with a logged cook |

A new card for a second version takes the original's slug with `-v2` on the end and starts at `v2.0`. The next takes `-v3` and starts at `v3.0`, and so on with the next unused number, always added to the original's slug and never to another variant's. Its changelog names the card it came from, and its evidence starts from its own cooks.

The cook sets the scope of a save. When the cook's instruction and this table disagree, say what the table would do, then follow the cook.

## Names and places

- A card lives at `recipes/<category>/<slug>.md`.
- To make a slug from a title: write it in lowercase, write each accented letter without its accent, turn every run of characters other than the letters `a` to `z` and the digits into one hyphen, and drop a hyphen from the start or the end. "Roasted Carrots, Two Ways" becomes `roasted-carrots-two-ways`. No two cards share a slug, whatever their categories.
- The category is the folder. Its name is yours to choose, such as `mains`, `sides`, or `baked-goods`, and it is made from the name you choose the way a slug is made from a title.
- A cook log lives at `cook-logs/<slug>/<YYYY-MM-DD>.md`, named for the day of the cook.
- A source packet, the exact text the cook approved, lives at `.sources/<slug>/<YYYY-MM-DD>.md`. Git ignores that folder, so a packet is never committed.
- `recipes/INDEX.md` is generated from the cards by `python3 scripts/build-index.py`. Run it after adding or changing a card, and never edit the index by hand. `python3 scripts/build-index.py --check` fails when the index is out of date.
- The block at the top of a card repeats `version`, `status`, and `evidence` for scripts. Write each value as a plain word with no quotation marks, and keep the block and the lines under the title in step.

## When sources disagree

When two sources give different answers, name the conflict and what follows from it, then go by this order. A newer file date does not settle it.

1. The cook's latest explicit instruction.
2. The standing corrections in `kitchen/profile.md`.
3. The saved card on the default branch.
4. The cook logs. A log is evidence that a card may need to change. It does not change the card.
5. Copies outside the repository, uploaded snapshots, and what an agent remembers of an earlier conversation. These give context. None of them is a source for a missing quantity.

For example: the saved card says two pounds, and the cook's last message says one. Use one pound for this cook, say that the card still says two, and update the card.

Food-safety standards and the limits in an equipment manual are not on this list, because they are constraints on every source in it. When a card or an instruction conflicts with one, say so before anything else.
