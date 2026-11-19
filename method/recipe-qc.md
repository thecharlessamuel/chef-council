# The editor check

Every recipe card that is added or changed gets an independent check before it is committed. A separate agent, one that did not write the card, compares the card with the exact text the cook approved and writes a report. This page explains why, how to run the check with any agent or in a chat app, and what the automatic gate does with the report.

## Why

An agent that has just written a recipe card is a poor judge of it. It remembers what it meant to write, so it reads the card and sees that. Quantities drift, a time moves by five minutes, or a helpful detail appears that nobody reported. The agent will then tell you, sincerely, that the card matches what you agreed.

A second agent has no such memory. It is given only the approved text and the card, and its one job is to find where they differ. So the rule is simple: the writer of a card never grades it.

## How the check works

1. The writer saves a **source packet** before it writes the card. This is the text the cook approved, pasted exactly, with the cook's instruction about what to save. [`templates/source-packet.md`](../templates/source-packet.md) is its form. Packets live in `.sources/`, which git ignores, because a packet can hold a private conversation or a publisher's recipe.
2. A fresh agent, the **editor**, gets the packet and the card and nothing else. It follows the [`recipe-editor` skill](../.agents/skills/recipe-editor/SKILL.md), which says what it compares and what counts as a discrepancy.
3. The editor writes a **report** under `qc/`. The [report format](../.agents/skills/recipe-editor/references/report-format.md) gives the path and the layout. The report holds a verdict, a table of discrepancies, and the hash of the card file the editor read.
4. The verdict decides what happens next.

| Verdict | Meaning | What happens next |
|---|---|---|
| `PASS` | The card matches the approved text. | Commit the card, the index, and the report together. |
| `PASS WITH NOTES` | Only small things differ, and none changes what gets cooked. | The same. If you fix a note, the card has changed, so it needs a fresh check. |
| `FAIL` | Something differs that changes what gets cooked, or the card claims something the approved text does not support. | Fix the card from the packet, then have a fresh editor check it again. The failed report stays as the record. |

The editor never edits a recipe. It reports, and the writer fixes.

## Running the editor

| Where you work | How to get a fresh editor |
|---|---|
| Claude Code | Use the `recipe-editor` subagent in `.claude/agents/`. It starts in a fresh context and follows the skill. |
| Another agent that can start subagents | Start a fresh subagent, and give it the skill's path, the packet's path, and the card's path. |
| An agent with no subagents | Start a new session in the repository, and ask it to follow the `recipe-editor` skill on the packet and the card. |
| A chat app | Open a new chat and paste the prompt below. |
| None of these | Say that the check has not been run. Never write the report in the conversation that wrote the card. |

When no check can be run, the cook decides whether to save anyway. The gate below then fails for that change, which is accurate, and merging over a failed check is the cook's call.

### The editor prompt for a new chat

A chat has no access to your files, so you paste in what the editor needs. First, in a terminal, run `scripts/check-qc.sh --hash recipes/<category>/<slug>.md`, which prints the card's `Card-SHA256:` line. Then open a new chat, not the one that wrote the card. Paste the prompt below, and after it paste these six things in this order: the contents of `.agents/skills/recipe-editor/SKILL.md`, the contents of `.agents/skills/recipe-editor/references/report-format.md`, the contents of `method/status-and-versions.md`, the source packet, the card, and the `Card-SHA256:` line.

```text
You are an independent recipe editor. You did not write the recipe card below, and you have not seen the conversation in which it was written. After this message I am pasting six things, in this order: your instructions (a file named SKILL.md), the report format (a file named report-format.md), the status and version rules (a file named status-and-versions.md), the source packet, the recipe card, and the card's Card-SHA256 line. Follow the instructions exactly. You cannot read or write files here, so use only what I paste, skip any check that needs a command and say that you skipped it, and return the complete report with the path where I should save it. Do not rewrite or fix the card.
```

The editor's reply has four headings, and the report sits under the second. Save only the report, from its `# Editor report:` line to the end of its Checks run list, at the path the editor gives. Leave out the rest of the reply, which repeats the verdict line, and do not change the card. If you change the card after computing the hash, start again from the hash.

## The gate

A script, `scripts/check-qc.sh`, makes the rule hard to skip. CI runs it on every pull request and on every push to `main`.

For each card that was added or changed, the gate looks for an editor report that was added or changed along with it, under `qc/<category>/<slug>/`. The card passes when one such report has both of these:

- a `VERDICT:` line that reads `PASS` or `PASS WITH NOTES`;
- a `Card-SHA256:` line equal to the SHA-256 of the card file.

The hash is what keeps a report honest about time. If the card is edited after the check, even by one character, its hash changes, the old report stops counting, and the card needs a fresh check. A report for one card never counts for another, because each card has its own folder under `qc/`, named for its category and its slug.

The gate cannot tell whether a check was careful, or whether a fresh agent really ran it. It proves that a report exists, that it passes, and that it describes the card as it now stands. The rule at the top of this page still depends on you and your agents following it.

To run the gate yourself, from the repository root:

```bash
scripts/check-qc.sh
```

It compares your last commit with `origin/main` and prints `qc checked:` with the number of changed cards, or one line for each card that lacks a report. To compare with another branch, name it with `--base`, or set `QC_BASE`. The gate never passes when it cannot find the base to compare with. The comments at the top of the script list its other options and its exit statuses.

A second script, `python3 scripts/lint-cards.py`, checks the form of every card: the block at the top, the lines under the title, the status and evidence values, the file and folder names, one slug per card, links that lead somewhere, and an index that is up to date. CI runs it beside the gate.

## Optional local checks

CI is the gate. These two only tell you sooner.

- **A git pre-commit hook, for any agent or none.** Run `scripts/install-git-hooks.sh` once. Each commit then runs the gate on what is staged, and the linter, and stops when either fails. It never replaces a pre-commit hook that it did not write. Running it again rewrites its own hook, so keep changes of yours out of that file. To remove it, delete the file the script names.
- **A Claude Code Stop hook.** `.claude/settings.json` runs the gate on your working files when a Claude Code session is about to finish. If a card lacks its report, Claude is told so and keeps working. To turn it off, remove the `Stop` entry from that file.

Both compare with `origin/main`. In a repository with no such branch, set `QC_BASE` to the branch you work from, such as `main`.

## On a fork

GitHub turns workflows off on a new fork. Open the Actions tab of your fork and enable them, so the gate and the linter run on your pull requests.
