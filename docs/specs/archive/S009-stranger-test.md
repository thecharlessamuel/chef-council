---
date: 2026-11-19
id: S009
wayfinder: docs/wayfinder/W001-public-chef-council/issues/T015-stranger-test.md
target_release: none
status: shipped
base_branch: main
base_sha: d28bb614dd66138805544e2f810ad3129ba54897
work_branch: workstream/t015-stranger-test
pr_base: main
prior_specs:
  - docs/specs/archive/S001-scaffold.md
  - docs/specs/archive/S002-council-roster-and-vetting.md
  - docs/specs/archive/S003-chef-council-skill.md
  - docs/specs/archive/S004-codify-and-cook-log.md
  - docs/specs/archive/S005-editor-gate.md
  - docs/specs/archive/S006-example-recipes.md
  - docs/specs/archive/S007-chat-path-and-adapters.md
  - docs/specs/archive/S008-docs-and-behavior-checks.md
references:
  - docs/wayfinder/W001-public-chef-council/MAP.md
  - docs/wayfinder/W001-public-chef-council/issues/T004-private-until-review.md
  - docs/learnings/L003-chef-council-skill.md
  - docs/learnings/L004-codify-and-cook-log.md
  - docs/learnings/L006-example-recipes.md
  - docs/learnings/L007-chat-path-and-adapters.md
  - docs/learnings/L008-docs-and-behavior-checks.md
  - .agents/spec-profile.md
cross_examined: meta/muse-wonder-full-1.0 (architect), 16 findings, 14 accepted
approved_by: autonomous
approved_at: 2026-11-19T08:36Z
pr: 34
kickbacks: 0
merged: 2026-11-19
harvested: 2026-11-19 (4 learnings)
---

# Stranger test: two fresh runs of the README's five-minute path, and the fixes for what the first one tripped on

## Goal and definition of done

Ship ticket T015: prove that a stranger can use the repository. A fresh
agent that knows only the repository's address clones it, follows the
README's five-minute path (the coding-agent steps with the cook's lines
scripted, and the chat steps as far as a person can go without a chat app),
and records every trip. The pull request fixes the trips, and a second
fresh run on the fixed branch completes with no blocking trip.

Leg 1 made the first run itself, on `main` at `base_sha`, so that the fixes
could be decided in this spec and not by the executor (decision 1, L003).
That run completed with eleven trips, none blocking. Eleven exact edits to
five files answer them and what two rehearsals of the second run found, and
a sixth file, `chat/bundle.md`, is regenerated.
The executor applies the edits with the script this spec gives, pushes, and
makes the second run with the brief this spec gives. It does not write a
fix of its own.

Done means all of the following, each observed on the work branch's head
commit after Task 2, from the repository root, with the setup file of `##
Build plan — agent loop` sourced:

1. **The files.** `git diff --name-only "$BASE_SHA"...HEAD -- .
   ':!docs/specs/' ':!docs/wayfinder/' | LC_ALL=C sort` prints exactly
   these six lines:

   ```text
   .agents/skills/chef-council/SKILL.md
   .agents/skills/recipe-codify/SKILL.md
   README.md
   chat/bundle.md
   method/recipe-qc.md
   method/status-and-versions.md
   ```

2. **The bytes.** This prints six lines, each a path followed by `: OK`:

   ```bash
   sha256sum -c - <<'SUMS'
   bcc049965d53fb3d45dbb9411a44d6f214099b2a61f7241ed4d8d8f27b47c6f0  .agents/skills/chef-council/SKILL.md
   a9a3291b49a3a42fa449c3059a6d1b0489bb89ceffbfe19f57e933300c2cd2a2  .agents/skills/recipe-codify/SKILL.md
   f82bc00505e11899eeabe716be7f090d44f63213ccaabd9acd9eeec530f77181  README.md
   e51c5621c4fdac454e242416c7b09aadb938d1bd4d8b5f17f4f3885d327c9558  chat/bundle.md
   b13bbd5ae0752e9dae23560dc8aff7aee3979ff3c734a425244f435c70647e9a  method/recipe-qc.md
   aa55fe9987bdae2fb75af3014020dd6fa3c017f28b5486445e1fa8ec0284550f  method/status-and-versions.md
   SUMS
   ```

3. **Links, anchors, and paths.** `linkcheck README.md $MD; echo $?` prints
   `0` and nothing else. `anchorcheck README.md $MD; echo $?` prints
   `anchors checked: 16` then `0`. `pathcheck README.md; echo $?` prints
   `paths checked: 37` then `0` (decision 9).
4. **Nothing private.** `"$SWEEP" --text README.md $MD chat/bundle.md` ends
   with a line beginning `privacy sweep: clean` and exits 0, and so does
   the full sweep, `"$SWEEP"`, after `git fetch origin`.
5. **The repository's checks still pass.** `python3 scripts/check-skills.py`
   prints `skills checked: 4`; `python3 scripts/check-council.py` prints
   `council checked: 14 seated, 14 records`; `python3 -m unittest discover
   -s tests -v > "$OUT" 2>&1; echo $?` prints `0` and `tail -1 "$OUT"`
   prints `OK`; `python3 scripts/lint-cards.py` prints `cards checked: 2`;
   `scripts/check-qc.sh; echo $?` prints `qc checked: 0` then `0`;
   `scripts/build-chat-bundle.sh --check; echo $?` prints `chat bundle
   checked: 33 files` then `0`; `scripts/secret-scan.sh; echo $?` ends with
   `no leaks found` then `0`; `python3 "$WAYFINDER/scripts/lint.py"
   docs/wayfinder/*/MAP.md; echo $?` prints `0` and nothing else, run with
   `WAYFINDER=<the directory the harness printed when the wayfinder skill
   loaded>` written before `python3` on the same command line, because the
   setup file cannot know that directory; and `git diff --check
   "$BASE_SHA"...HEAD -- .; echo $?` prints `0` and nothing else. `wc -c <
   AGENTS.md` prints `8156` and `wc -m < chat/project-instructions.md`
   prints `6779`: neither copy of the agent rules is touched (decision 8).
6. **The pages render.** After the push, this prints five lines, each a
   path followed by ` 1 0` (one top heading, and no link left as raw
   Markdown). `{owner}` and `{repo}` are typed as they stand; `gh` fills
   them in from the repository:

   ```bash
   for p in README.md $MD; do gh api "repos/{owner}/{repo}/contents/$p?ref=$BRANCH" -H 'Accept: application/vnd.github.html' > "$OUT" && echo "$p $(grep -o '<h1' "$OUT" | wc -l) $(grep -c '\](' "$OUT")"; done
   ```

   Leg 1 ran the same loop with `ref=main` and got ` 1 0` for all five
   files; no edit adds a heading or a link form the pages do not already
   use.
7. **The second stranger run.** Made as `### The second stranger run` says,
   after the push, on a commit that is both `git rev-parse HEAD` and `git
   rev-parse "origin/$BRANCH"`. `runcheck "$RUN2" "$(git rev-parse HEAD)";
   echo $?` prints `clone directory: <D>`, then `stranger run ok: <N>
   trips` for some number `<N>`, then `0`. With `D` the path on that first
   line, `git -C "$D" rev-parse "origin/$BRANCH"` prints the same commit, and
   `(cd "$D" && scripts/check-qc.sh --working-tree; echo $?)` prints `qc
   checked: 1` then `0`: the stranger's one new card has a current passing
   report (decision 5).
8. **The summary of both runs is in the pull request.** With the pull
   request's body saved by `gh pr view <PR> --json body -q .body > "$OUT"`:
   `grep -c '^## Stranger runs$' "$OUT"` prints `1`, `grep -c '^\*\*Run [12]\*\* was made by' "$OUT"`
   prints `2`, `grep -c 'now says to use `--working-tree`' "$OUT"` prints
   `1`, and `grep -c "^\*\*Run 2\*\* was made by the executor on this
   branch at .$(git rev-parse HEAD)." "$OUT"` prints `1`, with that command
   written on one line (decision 6). `gh pr view <PR> --json headRefOid -q .headRefOid`
   prints the commit of item 7: a commit added after the second run means
   the run is made again (decision 7).
9. **The pull request's checks.** `gh pr checks <PR>` reports every check
   passed (profile).

## Decisions

1. **Leg 1's rehearsal is the first run.** The ticket asks for a first run,
   fixes, and a second run on the fixed branch. L003 says a spec gated on a
   fresh reader runs that reader in leg 1. Leg 1 therefore made the first
   run on 2026-11-19, with a fresh subagent given the brief of `### The
   stranger brief` with `main` as its branch, cloning from GitHub through
   the maintainer's authenticated `gh` (decision T004). `main` was at
   `base_sha`, the tree a first run in leg 2 would have cloned. Its trips
   are `### The first run`, and the fixes are decided here. Leg 2 makes
   only the second run. The pull request says who made each run (decision
   6).
2. **What the stranger is told.** The ticket says the stranger is briefed
   with the URL and nothing else. The brief gives the address, the task the
   ticket describes, ground rules that keep the run safe (work only in the
   clone, write nothing to GitHub, fix nothing), the reply's form, and the
   cook's seven lines. The cook's lines are a script because the ticket
   says the cook's reports are simulated, and a fixed script makes two runs
   comparable. Lines C1, C4, C5, and C6 are the README's own quoted
   prompts. Lines C2, C3, and C7 are made up for this test and describe no
   real kitchen. The script was fixed before the first run and is
   the same for every run, so it does not say the README's new prompt,
   "Pressure-test it." (edit 9): the runs show only that the agent offers
   the test. C3 and C7 are said as often as they are needed, and the brief
   says so. The brief says nothing about the repository's contents and
   never names a private source.
3. **A blocking trip** is a trip of kind `blocked`: the stranger could not
   do a README step with what the clone gives it. A trip of kind
   `no-second-agent` also stops the second run from counting, because
   README step 5 ends in a separate agent's check, and a run without one
   did not follow the path to its end. Trips of kind `guessed` and
   `mismatch` do not block. `runcheck` applies this.
4. **Which trips are fixed.** Of the first run's eleven trips, nine are
   fixed and two are not. R10 came from the test harness, which starts a
   subagent outside the clone; a person who opens the clone in their agent
   does not meet it. R6 is a report that fits two skills, and either order
   ends with the same log. Leg 1 then rehearsed the second run twice
   (`### The rehearsals of the second run`). Both completed with seven
   trips and none blocking. Two trips of the first rehearsal are fixed by
   edits 10 and 11, and a third was a mismatch that a sentence of leg 1's
   own had caused, which is gone. The second rehearsal ran on the final
   files and nothing from it is fixed: each trip is left with its reason.
   The ticket's "done" is a second run with no blocking trip, and a fresh
   agent finds a new guess on most runs, so this spec does not chase the
   list to zero.
5. **The second run that fails.** `runcheck` prints one line per problem.
   Read them in this order. First, a line that starts `Verdict is`, or
   ends `is blocked` or `is no-second-agent`: the run has a blocking trip.
   Do not retry and do not write a fix. Report ``Question: the second
   stranger run of `S009` has a blocking trip (<the line, and the trip's
   row when there is one>); revise the spec?`` and stop. Otherwise, any
   other line (`headings are`, `text before the first heading`, `Clone
   does not name commit`, `Clone has no one Clone directory line`, `Trips
   is neither`, `trip row <n> is malformed`, `<id> has the kind`): the
   reply is malformed and says nothing about the repository. Make the run
   once more with a new fresh subagent. If that reply is malformed too,
   report ``Question: two stranger replies failed `runcheck` on form (<its
   lines>); is the checker or the brief wrong?`` and stop (L007). When
   `runcheck` passes and the clone observation of item 7 does not, report
   ``Question: the second stranger run passed `runcheck` but its clone
   prints <the output> for the editor gate; accept it or revise the
   spec?`` and stop.
6. **Where the record of the runs lives.** In the pull request's body,
   under `## Stranger runs`, placed after the profile's Evidence section,
   as `### The pull request's stranger section` gives it. The replies
   themselves are not committed: each names a temporary directory on the
   machine that ran it, and this spec's `### The first run` already holds
   the first run's trips. The second run's trip rows go into the body as
   the stranger wrote them, after the profile's `--text` sweep; every occurrence
   of the temporary directory, which is `D` without its last part
   `/chef-council`, is replaced by `<tmp>` first.
   Trips of the second run are recorded and not fixed in this pull request.
7. **The second run is made on the pull request's head.** It needs the
   pushed branch, because the stranger clones from GitHub. `### After
   Task 2` gives the order: push, make the run, then open the pull request
   with the summary in its body. The run changes no file in this repository. A commit added later,
   for example after a kickback, changes the head, and the run is made
   again on the new head and the summary replaced.
8. **`AGENTS.md` and `chat/project-instructions.md` are not changed.**
   `AGENTS.md` is 8,156 bytes against a limit of 8,192, and a rule changed
   in one copy must change in the other (L007). No trip needed a rule
   changed. Every edit is to a skill, a method page, or the README, and
   each says how an existing rule applies at a point where a stranger had
   to guess.
9. **Restatements (L008).** The edits change the `chef-council` skill's
   interview and three of its modes. Leg 1 searched `README.md`, `docs/`,
   `evals/behavior-checks.md`, `chat/project-instructions.md`,
   `chat/README.md`, and `kitchen/README.md` for sentences that restate the
   changed lines. Only the README's steps 2 and 3 do, and edits 8 and 9
   change them. `evals/behavior-checks.md` is not edited, so the three
   items L008 leaves for the next spec that edits it stay open, and
   `tests/` is not touched, so the item L007 leaves for the next spec that
   touches it stays open. `pathcheck` is run on the README only: on the
   skill and method pages it reports, on `main`, paths that are relative to
   a skill's folder or are not files (`references/food-safety.md`,
   `origin/main`), which is old debt this spec does not take on.
10. **The edits, and the trip each answers.** The exact text is in the
    `apply` helper, numbered here in its order. R1 to R11 are the first
    run's trips; the rehearsals' trips are named as such.
    1. `chef-council` skill, First-run interview: after writing a kitchen
       file, rebuild the chat bundle; an agent that wrote files does not
       commit them and tells the cook which are written and not committed
       (R1, R2).
    2. `chef-council` skill, Modes: an offer of the pressure test is an
       allowed closing note (R5).
    3. `chef-council` skill, Develop: a saved card for a different dish is
       not the cook's recipe, and a number borrowed from it is named and
       listed as not tested for this dish; a number with no allowed source
       is written as missing and the recipe is still given; the pressure
       test is its own reply, offered in the closing note, and only the
       text the cook then approves is the approved text (R3, R4, R5).
    4. `chef-council` skill, Troubleshoot: what to do when the reference
       has no entry for the symptom, with or without a card, and what to
       write when no cause can be named (R7).
    5. `chef-council` skill, Hand off to codify: when the cook asked for
       the save, the same reply continues with the `recipe-codify` skill
       (R8).
    6. `method/status-and-versions.md`, Kitchen evidence: the Recipe line
       of a log written before the card is not changed afterward (R9).
    7. `method/recipe-qc.md`, The gate: before a commit the default gate
       prints `qc checked: 0` and has checked nothing; use
       `--working-tree` (R11).
    8. `README.md`, step 2: the agent rebuilds `chat/bundle.md` and leaves
       all three files for the cook to commit (R1, R2).
    9. `README.md`, step 3: how to ask for the pressure test (R5).
    10. `recipe-codify` skill, The recipe itself: a cue given outside the
        steps goes word for word into the step it describes, or under
        Notes when it describes none (second rehearsal, R6).
    11. `recipe-codify` skill, Changelog: a log written before the card is
        named by its path in the changelog line (second rehearsal, R5).

    No edit adds a rule that `AGENTS.md` does not already hold. A saved
    card is one of the sources the skill already lets advice be attributed
    to ("the cook's own card"), so edit 3 adds no source: it says how a
    number from a card for another dish is labeled. Its sentence on
    missing numbers applies the skill's own "Numbers do not come from a
    lens" to the Develop shape. A log whose folder was named before the
    card chose a different slug is not covered: neither run met it, and
    moving a log is outside this ticket. `chat/bundle.md` is regenerated by
    `scripts/build-chat-bundle.sh` and never edited by hand.
11. **The stranger's model.** The executor starts the stranger as a
    `general-purpose` subagent through the harness's agent tool and sets no
    model, so it runs on the executor's own. Leg 1's runs ran on the
    architect tier. One run of each is a sample, not a proof.

## Prerequisites

- Leg 2 starts from this spec's approval commit on
  `workstream/t015-stranger-test`, which already holds the claim commit for
  T015. Staging, the per-task commit with its `Spec-Task: S009/<N>`
  trailer, the push, the pull request, and the base-drift check are the
  `2-spec-execute` skill's standing procedure and the profile's ship tail.
  Each task's commit holds exactly that task's Touches.
- The executor's machine has Git 2.32 or later, Bash 4.4 or later, Python
  3, GNU coreutils (`sha256sum`), and an authenticated `gh`. It is Linux
  x86_64, where `scripts/secret-scan.sh` fetches its pinned gitleaks, or
  `GITLEAKS_BIN` names an installed gitleaks of the pinned version
  (profile). `git config user.email` ends in `@users.noreply.github.com`
  (profile). `git rev-parse --verify origin/main` succeeds after `git fetch
  origin`.
- Before Task 1, `git status --porcelain --untracked-files=all` prints
  nothing, and `git diff --name-only "$BASE_SHA" HEAD -- README.md .agents
  method chat` prints nothing: the six files are as they were at
  `base_sha`.
- `test -x "$(git rev-parse --git-common-dir)/info/privacy-sweep"`
  succeeds, and the executor knows the directory the harness prints when
  the wayfinder skill loads. If either is missing, report ``Question: <the
  privacy sweep | the Wayfinder lint> that the profile requires is not on
  this machine; provide it?`` and stop.
- The harness's agent tool can start a `general-purpose` subagent. If it
  cannot, report ``Question: this session cannot start the fresh subagent
  the second stranger run needs; run it another way?`` and stop.

### Gate helpers

Four blocks, none of them a repository file. Each is the text inside the
fenced block that follows its heading: every line between the opening line
of four backticks and the next line that is exactly four backticks.

- `setup` sets the fixed paths the gates use and loads the rest. `S009` is
  a folder outside the repository, and `OUT`, `RUN2`, and `BODY` are files
  in it at fixed paths, because the harness starts a new shell for each
  command (L006). `MD` is the four Markdown paths other than the README, in
  one variable that gate commands use unquoted. It writes the `apply` block
  to `$S009/apply.py` and the brief to `$S009/brief.txt`, and it loads
  `linkcheck`, `anchorcheck`, and `pathcheck` from the archived S008,
  unchanged (L008).
- `apply` is a Python script that makes the eleven edits of decision 10.
  `python3 "$S009/apply.py" <path>...` edits only the paths named. Each
  edit replaces one exact piece of text that must occur exactly once in its
  file; when it does not, the script changes nothing and exits with a line
  that starts `apply:`. It prints `edited: <path>` for each file it wrote.
- `runcheck <reply file> <commit>` is decision 3. It removes two leading
  spaces from every line when every line that is not blank has them,
  because the harness indents a subagent's reply (L006). It requires the
  brief's seven headings in order with nothing before the first, the commit
  and exactly one `Clone directory:` line with an absolute path in the
  Clone section, a Verdict section whose one line is `STRANGER RUN:
  COMPLETE`, and a Trips section that is `None.` or a table whose rows are
  numbered `R1`, `R2`, and so on, each with one of the four kinds and none
  with `blocked` or `no-second-agent`. It prints one line per problem and
  returns 1, or prints `clone directory: <path>` and `stranger run ok: <N> trips` and
  returns 0.

#### Helper: `setup`

````bash
S009="${TMPDIR:-/tmp}/s009"
OUT="$S009/out.txt"
RUN2="$S009/run2.txt"
BODY="$S009/pr-body.md"
ROOT="$(git rev-parse --show-toplevel)"
SPEC="$ROOT/docs/specs/S009-stranger-test.md"
ARCH="$ROOT/docs/specs/archive/S008-docs-and-behavior-checks.md"
BASE_SHA=d28bb614dd66138805544e2f810ad3129ba54897
BRANCH=workstream/t015-stranger-test
SWEEP="$(git rev-parse --git-common-dir)/info/privacy-sweep"
MD=".agents/skills/chef-council/SKILL.md .agents/skills/recipe-codify/SKILL.md method/recipe-qc.md method/status-and-versions.md"
block() {
  python3 - "$1" "$2" <<'PY'
import re, sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index(sys.argv[2])
opening = next(i for i in range(start + 1, len(lines)) if re.fullmatch(r"`{4,}[a-z]*", lines[i]))
fence = re.match(r"`+", lines[opening]).group(0)
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == fence)
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
}
block "$SPEC" '#### Helper: `apply`' > "$S009/apply.py"
block "$SPEC" '#### The stranger brief' > "$S009/brief.txt"
eval "$(block "$SPEC" '#### Helper: `runcheck`')"
eval "$(block "$ARCH" '#### Helper: `linkcheck`')"
eval "$(block "$ARCH" '#### Helper: `anchorcheck`')"
eval "$(block "$ARCH" '#### Helper: `pathcheck`')"
````

#### Helper: `apply`

````python
import sys
EDITS = [
    (
        ".agents/skills/chef-council/SKILL.md",
        "- Leave `kitchen/pantry.md` alone. Offer to fill it in later.\n",
        "- Leave `kitchen/pantry.md` alone. Offer to fill it in later.\n"
        "- After writing a kitchen file, run `scripts/build-chat-bundle.sh`. It rebuilds `chat/bundle.md`, which includes the kitchen files, and until it is rebuilt `scripts/build-chat-bundle.sh --check` and the test suite fail. If you cannot run commands, give the cook the command. When you wrote files, do not commit them: tell the cook which files are written and not committed. The cook says when to commit them, together, on a branch and never on `main`.\n",
    ),
    (
        ".agents/skills/chef-council/SKILL.md",
        "an offer to run the interview that was skipped, or a request for the cook's report.",
        "an offer to run the interview that was skipped, an offer to pressure-test a recipe before it is cooked, or a request for the cook's report.",
    ),
    (
        ".agents/skills/chef-council/SKILL.md",
        "A recipe developed here is a draft that has not been cooked. Say so.\n",
        "A recipe developed here is a draft that has not been cooked. Say so. A saved card for a different dish, an example card included, is not the cook's recipe for this one: say that it exists, and when you borrow a number from it, name that card as the number's source and list the number under Sources and open questions as not tested for this dish. Where a quantity, a time, or a temperature has none of the sources that [How the council answers](#how-the-council-answers) allows, write in its place that it is missing, and list it under Sources and open questions. A recipe with a missing number is still an answer.\n"
        "\n"
        "The pressure test is its own reply, not part of this shape. Offer it in the closing note. When the cook asks for it, put its Corrected recipe to the cook, and only the text the cook then approves is the approved text.\n",
    ),
    (
        ".agents/skills/chef-council/SKILL.md",
        "Read `references/troubleshooting.md` for the symptom. Then answer in this shape:\n",
        "Read `references/troubleshooting.md` for the symptom. When it has no entry for the symptom, say so, and work from the cook's report and, when the dish has a card, its Failure modes. Name a cause only when the report points to one; otherwise say under `## What probably happened` that the cause cannot be told from the report, and ask for the one fact that would settle it. Then answer in this shape:\n",
    ),
    (
        ".agents/skills/chef-council/SKILL.md",
        "A recipe with a `no` can still be saved as a draft when the cook asks. Say which lines are open.\n",
        "A recipe with a `no` can still be saved as a draft when the cook asks. Say which lines are open.\n"
        "\n"
        "When the cook has asked for the save and you can follow the recipe-codify skill yourself, the hand-off does not end the reply. After these four headings, continue in the same reply with that skill and its own four headings. The last sentence of item 4 means that a card is written only through that skill.\n",
    ),
    (
        "method/status-and-versions.md",
        "A log written before the dish had a card counts the same way, when the card's first changelog line names it.",
        "A log written before the dish had a card counts the same way, when the card's first changelog line names it. That log's Recipe line is not changed afterward: it still reads `No card yet.`",
    ),
    (
        "method/recipe-qc.md",
        "or one line for each card that lacks a report. To compare with another branch,",
        "or one line for each card that lacks a report. Before a commit, the card you just wrote is not in your last commit, so that command prints `qc checked: 0` and has checked nothing. Run `scripts/check-qc.sh --working-tree` then, which reads the files as they are now. To compare with another branch,",
    ),
    (
        "README.md",
        "and writes your answers into `kitchen/profile.md` and `kitchen/equipment.md`.\n",
        "and writes your answers into `kitchen/profile.md` and `kitchen/equipment.md`. It then rebuilds `chat/bundle.md`, which includes those files, and leaves all three for you to commit.\n",
    ),
    (
        "README.md",
        "3. Choose a direction, cook, and tell it how it went: \"Made it. Too sweet, and the thin pieces burned.\"\n",
        "3. Choose a direction. To have the recipe checked before you cook, say: \"Pressure-test it.\" Then cook, and tell it how it went: \"Made it. Too sweet, and the thin pieces burned.\"\n",
    ),
    (
        ".agents/skills/recipe-codify/SKILL.md",
        "You may reword a step and arrange the recipe into the template's tables.",
        "You may reword a step and arrange the recipe into the template's tables. A cue the approved text gives outside its steps, such as under a Cues heading, goes word for word into the step it describes, beside that step's own cue. A cue that describes no step goes under Notes.",
    ),
    (
        ".agents/skills/recipe-codify/SKILL.md",
        "For a new card, say whether it has been cooked.\n",
        "For a new card, say whether it has been cooked. When `cook-logs/<slug>/` holds a log written before the card, name that log by its path in this line, which is what lets it count.\n",
    ),
]
only = sys.argv[1:]
texts = {}
for path, old, new in EDITS:
    if only and path not in only:
        continue
    if path not in texts:
        texts[path] = open(path, encoding="utf-8", newline="").read()
        for p, o, n in EDITS:
            if p == path and n in texts[path]:
                sys.exit("apply: %s is already edited; nothing was changed" % path)
    if texts[path].count(old) != 1:
        sys.exit("apply: %s: expected one match, found %d, for %r; nothing was changed" % (path, texts[path].count(old), old[:60]))
    texts[path] = texts[path].replace(old, new)
for path in sorted(texts):
    open(path, "w", encoding="utf-8", newline="").write(texts[path])
    print("edited: %s" % path)
````

#### Helper: `runcheck`

````bash
runcheck() {
  python3 - "$@" <<'PY'
import re, sys
path, sha = sys.argv[1], sys.argv[2]
lines = open(path, encoding="utf-8").read().split("\n")
while lines and not lines[-1].strip():
    lines.pop()
if lines and all(line.startswith("  ") or not line.strip() for line in lines):
    lines = [line[2:] for line in lines]
HEADS = ["## Clone", "## Coding-agent path", "## Chat path", "## Checks run", "## Files", "## Trips", "## Verdict"]
KINDS = ["blocked", "guessed", "mismatch", "no-second-agent"]
bad = []
found = [line for line in lines if line.startswith("## ")]
if found != HEADS:
    bad.append("headings are %r" % found)
    print("\n".join(bad))
    sys.exit(1)
if lines[0] != HEADS[0]:
    bad.append("text before the first heading")
at = [lines.index(h) for h in HEADS] + [len(lines)]
sec = {h: [l for l in lines[at[i] + 1:at[i + 1]] if l.strip()] for i, h in enumerate(HEADS)}
if not any(sha in l for l in sec["## Clone"]):
    bad.append("Clone does not name commit %s" % sha)
where = [m.group(1) for m in (re.match(r"[-*\s]*Clone directory: `?(/[^`\s]+)`?\s*$", l) for l in sec["## Clone"]) if m]
if len(where) != 1:
    bad.append("Clone has no one Clone directory line")
if sec["## Verdict"] != ["STRANGER RUN: COMPLETE"]:
    bad.append("Verdict is %r" % sec["## Verdict"])
trips = 0
if sec["## Trips"] != ["None."]:
    rows = [l for l in sec["## Trips"] if l.startswith("|")]
    if len(rows) != len(sec["## Trips"]) or len(rows) < 3:
        bad.append("Trips is neither None. nor a table")
    for n, row in enumerate(rows[2:], 1):
        cells = [c.strip().strip("`") for c in row.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0] != "R%d" % n:
            bad.append("trip row %d is malformed" % n)
            continue
        trips += 1
        if cells[2] not in KINDS:
            bad.append("%s has the kind %r" % (cells[0], cells[2]))
        elif cells[2] in ("blocked", "no-second-agent"):
            bad.append("%s is %s" % (cells[0], cells[2]))
if bad:
    print("\n".join(bad))
    sys.exit(1)
print("clone directory: %s" % where[0])
print("stranger run ok: %d trips" % trips)
PY
}
````

#### The stranger brief

````text
You are a stranger to a repository. You know its address and nothing else about it:

    https://github.com/thecharlessamuel/chef-council

Your job is to find out whether a newcomer can use it by following its README, and to record every place the newcomer would trip.

Ground rules:

- Make a new, empty directory and clone into it with this one command, which prints the clone's path: `DIR="$(mktemp -d)" && gh repo clone thecharlessamuel/chef-council "$DIR/chef-council" -- --branch workstream/t015-stranger-test && echo "$DIR/chef-council"`. Work only inside that clone. Do not read any other directory on this machine, and ignore any project instruction, memory, or skill your harness loaded from anywhere other than the clone: a stranger has only the clone.
- Never push, never open a pull request or an issue, and never write anything to GitHub. A local commit on a new local branch is allowed when the repository's own instructions call for a commit.
- Do not fix the repository. When something is wrong, record it and carry on by the most reasonable reading; when you cannot carry on, stop that step and say so.

What to do:

1. Read the README. Find its section "Try it in five minutes".
2. Follow the "With a coding agent" steps 1 to 5 in order, as the coding agent that has just been opened in the clone: read what the repository tells an agent to read, and do what it tells an agent to do, exactly as written. You also play the cook, and the cook says only the lines below, whenever the agent needs the cook to speak. C1, C2, C4, C5, and C6 are each said once, in that order. C3 and C7 are said as often as they are needed:
   - C1 (README step 2): "Summon the council. I have two pounds of carrots, butter, and forty minutes."
   - C2 (the answers to whatever first-run questions the repository has the agent ask): "I cook for two adults. No allergies and no dietary constraints, and nobody I cook for is at higher risk from foodborne illness. I have a home oven, a sheet pan, a skillet, and an instant-read thermometer. I am a comfortable home cook with forty minutes on a weeknight. US units."
   - C3 (when asked to choose a direction or approve a recipe): "Go with your recommendation. I approve that recipe as written."
   - C4 (README step 3): "Made it. Too sweet, and the thin pieces burned."
   - C5 (README step 4): "Log this cook."
   - C6 (README step 5): "Save the recipe as a card."
   - C7 (to any other question from the agent): "I have nothing to add. Mark it as not reported."
   Where the repository calls for a separate agent in a fresh context, start one if your harness lets you, briefed only as the repository says to brief it. If you cannot start one, say so, do what the repository says to do in that case, and record it as a trip of kind `no-second-agent`.
   Run every check the repository tells an agent or a contributor to run before a commit or a pull request, and record each command with its exit status and last line of output.
3. Follow the "With a chat app" steps as far as a person can without a chat app: find the text to paste in and the knowledge file to upload, confirm each exists and is what the instructions say it is, run any command the instructions give for building or checking them, and find the editor prompt the third step points to. Do not open a chat app.

Record a trip every time you: could not do a step with what the clone gives you (kind `blocked`); had to guess between two readings or fill a gap the files leave open (kind `guessed`); found two files, or a file and the repository's actual behavior, that disagree (kind `mismatch`); or could not start a separate agent (kind `no-second-agent`). A smooth step is not a trip. Do not pad the list, and do not leave a real trip out.

Reply with exactly these sections and nothing before or after them:

## Clone
A line `Clone directory: ` followed by the absolute path of the clone, then the branch, then the output of `git rev-parse HEAD` as it was straight after the clone.

## Coding-agent path
One short paragraph per README step (1 to 5): what you read, what you did, what the result was.

## Chat path
One short paragraph per README step (1 to 3).

## Checks run
One line per command: the command, its exit status, its last line of output.

## Files
The output of `git status --porcelain --ignored` in the clone, and of `git log --oneline -3`.

## Trips
A table with the columns `ID | Path step | Kind | Where (file and line or heading) | What happened | What I did`. IDs are R1, R2, and so on. Write `None.` when there are none.

## Verdict
One line, exactly `STRANGER RUN: COMPLETE` when both paths were followed to the end with no trip of kind `blocked`, or `STRANGER RUN: BLOCKED at <path and step>` otherwise.
````

## Build plan — agent loop

Run every command from the repository root. The harness starts a new shell
for each command, so every command this spec gives (a task's Work, a gate,
and the steps of `### After Task 2`) begins by sourcing the setup file
(L006). Write the setup file once, before Task 1, with this command, which
reads the `setup` block out of this spec:

```bash
mkdir -p "${TMPDIR:-/tmp}/s009" && python3 - docs/specs/S009-stranger-test.md > "${TMPDIR:-/tmp}/s009/setup.sh" <<'PY'
import re, sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index("#### Helper: `setup`")
opening = next(i for i in range(start + 1, len(lines)) if re.fullmatch(r"`{4,}[a-z]*", lines[i]))
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "````")
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
```

Every such command is then run as `. "${TMPDIR:-/tmp}/s009/setup.sh" &&
<the command>`. After sourcing, `type -t block runcheck linkcheck
anchorcheck pathcheck` prints `function` five times, and `sha256sum
"${TMPDIR:-/tmp}/s009/setup.sh" "${TMPDIR:-/tmp}/s009/apply.py"
"${TMPDIR:-/tmp}/s009/brief.txt"` prints three lines that begin, in order,
`dd37b5afd9c0aaa60f001004382d090a0f6feb404989537941257f16770830fa`,
`18cceaebc4df8d3e508c781c11452bb2824c5071a72b7783881e345cebfdaf81`, and
`902e7f3b3464c42c0d318682c937a5563522a8a7ace0c41aab45a37ea88ca552`. A gate
passes only when every command in it prints what is stated. Where a gate
ends in `; echo $?`, the printed status is part of the expected output. The
gate's commands run in the order listed.

Baseline, measured by leg 1 on 2026-11-19 in a scratch clone at `base_sha`:
`python3 -m unittest discover -s tests -v` exits 0 and ends `OK` with 269
tests; `python3 scripts/check-skills.py` prints `skills checked: 4`;
`python3 scripts/check-council.py` prints `council checked: 14 seated, 14
records`; `python3 scripts/lint-cards.py` prints `cards checked: 2`;
`scripts/check-qc.sh` prints `qc checked: 0`; `scripts/build-chat-bundle.sh
--check` prints `chat bundle checked: 33 files`; `linkcheck README.md $MD`
prints nothing; `anchorcheck README.md $MD` prints `anchors checked: 15`;
`pathcheck README.md` prints `paths checked: 36`; `wc -c < AGENTS.md`
prints `8156`. The SHA-256 lines, the anchor count of 16, and the path
count of 37 are red on the base by design, because they name the edited
files; none measures old debt. Leg 1 then built both tasks in a second
scratch clone from this spec's text, sourcing the setup file as above, and
ran every gate line below on it except the lines that need this run's own
commits, `origin`, the pull request, the secret scan, or the full privacy
sweep.

Helper probe, run by leg 1 on 2026-11-19. `runcheck` printed `stranger run
ok: 7 trips` on the second rehearsal's reply, with and without the
harness's two-space indentation. On altered copies of that reply it
printed a problem and returned 1 for each of: a trip's kind changed to
`blocked`; a trip's kind changed to `no-second-agent`; the verdict changed
to `STRANGER RUN: BLOCKED at coding 5`; the `## Files` heading removed; the
`Clone directory:` line removed; and a commit the Clone section does not
name. `apply`, run a second time on each edited file, exits with a line
that starts `apply:` and changes nothing.

### The first run

Made by leg 1 on 2026-11-19 on `main` at `base_sha`. Verdict: `STRANGER RUN:
COMPLETE`. The stranger filled in the kitchen files from the cook's script,
developed a butter-roasted carrots recipe, wrote a cook log, a source
packet, and a card at v1.0 (`draft`, `cooked-once`), had a fresh agent
write an editor report (`PASS WITH NOTES`), committed locally, and found
both chat files and the editor prompt. Its trips, shortened:

| Trip | Kind | Path step | What happened |
|---|---|---|---|
| R1 | mismatch | Coding 2 | The interview writes two kitchen files, which makes `chat/bundle.md` stale. Nothing on the path says to rebuild it, so the bundle check and the test suite fail. |
| R2 | guessed | Coding 2 | Nothing says which branch the interview's edits belong on, or whether and when they are committed. |
| R3 | guessed | Coding 2 | The only carrots card is a shipped example for a different dish. Nothing says whether it is the cook's baseline. |
| R4 | guessed | Coding 2 | Develop asks for every quantity and forbids inventing one, and a fresh kitchen has no source for this dish. |
| R5 | guessed | Coding 2 to 3 | The loop puts a pressure test before the cook. The README path and the Develop shape have no place for it. |
| R6 | guessed | Coding 3 | The cook's report fits both Troubleshoot mode and the cook-log skill. The README has the log written only at step 4. |
| R7 | guessed | Coding 3 | The troubleshooting reference has no entry for the README's own example report, and nothing says what to do then. |
| R8 | guessed | Coding 5 | "Save the recipe as a card." fits both the hand-off mode and the recipe-codify skill. Nothing says whether the hand-off ends the turn. |
| R9 | guessed | Coding 5 | The log was written before the card, so its Recipe line reads `No card yet.` Nothing says whether to update it. |
| R10 | guessed | Coding 5 | The harness started the stranger outside the clone, so the `recipe-editor` agent on offer came from another directory. |
| R11 | mismatch | Coding 5 | Before a commit, `scripts/check-qc.sh` prints `qc checked: 0` and exits 0, which looks like a pass and checks no card. |

### The rehearsals of the second run

Both were made by leg 1 on 2026-11-19, each with a fresh subagent, and each
with one difference from the brief: the clone line named a local scratch
repository holding `base_sha` plus the edits, because leg 1 does not push.

**The first rehearsal** ran on an earlier draft of the edits and of the
brief. Verdict: `STRANGER RUN: COMPLETE`, seven trips, none blocking. None
of the first run's R1, R2, R5, R8, R9, or R11 came back. Its first editor
returned `FAIL`, because three cues from the Develop reply were not on the
card, and a second editor returned `PASS` after the stranger moved them
into their steps. Three of its trips changed this spec:

| Trip | Kind | What happened | Disposition |
|---|---|---|---|
| R3 | mismatch | A sentence leg 1 had added to README step 3 said the agent says what probably happened, and for the example report it cannot. | The sentence was removed (edit 9 as it now stands). |
| R5 | guessed | Nothing tells the writer of a card whether to name an earlier log in the changelog. | Fixed by edit 11. |
| R6 | guessed | Develop has a Cues section and the card template has no place for one. | Fixed by edit 10. |

Its other four trips came back in the second rehearsal and are in the
table below. The cross-examination then changed the wording of nine of the
eleven edits and three lines of the brief.

**The second rehearsal** ran on the files exactly as the `apply` helper in
this spec leaves them, with the brief exactly as this spec gives it apart
from the clone line. Verdict: `STRANGER RUN: COMPLETE`, seven trips, none
blocking. The stranger rebuilt the bundle and left the three files
uncommitted, named the example card as a different dish and labeled the
numbers it borrowed, offered the pressure test, said that the reference
has no entry and that the cause of the sweetness could not be told, left
the log's Recipe line as it was, named the log by its path in the
changelog, and ran the gate with `--working-tree` before its commit. Its
one editor returned `PASS`. `runcheck` printed the clone directory and
`stranger run ok: 7 trips`, and in that clone `scripts/check-qc.sh
--working-tree` printed `qc checked: 1` and exited 0. Its trips, none of
them fixed here:

| Trip | Kind | What happened | Why it is left |
|---|---|---|---|
| R1 | guessed | The Directions round has no place for a recommended direction, and the cook's line said to go with the recommendation. | The cook's script is this test's, not the repository's; a real cook names a direction. |
| R2 | guessed | The README's example prompt is close to the shipped carrots card, and the stranger had to decide that it is a different dish. | Edit 3 is the rule it used, and it reached the reading the rule intends. |
| R3 | guessed | The pantry is blank, so whether salt is on hand was open, and no source gave a total time. | The stranger listed both as open, which is what the skill asks. |
| R4 | guessed | The cook's report fits both Troubleshoot mode and the cook-log skill. | The first run's R6: either order ends with the same log. |
| R5 | guessed | The cook gave no date for the cook. | The cook-log skill covers it, and the report came the same day. |
| R6 | guessed | The README's five steps have no moment where the cook approves a text unless the pressure test is run. | The recipe-codify skill makes the agent ask, and it did. A README step for it is a change to the path, for the maintainer's review. |
| R7 | mismatch | The README says there is nothing to install, and `scripts/secret-scan.sh` downloads a pinned gitleaks on first use. | The script and the profile say so, the five-minute path does not run it, and `AGENTS.md` has no room for the note (decision 8). |

One run is a sample. The second run in leg 2 is the first made from GitHub
on these files.

### The second stranger run

After Task 2's commit is pushed, and with `git rev-parse HEAD` equal to
`git rev-parse "origin/$BRANCH"` after `git fetch origin`:

1. Start one `general-purpose` subagent through the harness's agent tool,
   with no model set. Its prompt is the contents of `$S009/brief.txt`, the
   whole file and nothing else. Do not tell it about this spec, the first
   run, or the fixes, and send it no second message.
2. Save its reply to `$RUN2` as returned, leaving out any frame the harness
   puts around it. The two spaces the harness adds at the start of each
   line may stay; `runcheck` removes them.
3. Run the gates of definition-of-done item 7. On a failure, follow
   decision 5. A second attempt's reply replaces the first in `$RUN2`.
4. Leave the stranger's clone directory in place until the pull request is
   reviewed. It is outside the repository.

### After Task 2

No file in the repository changes after Task 2's commit, so these steps
are not a task and make no commit. In this order:

1. Run the profile's sweeps and push the branch, as the profile's ship
   tail says.
2. Observe definition-of-done item 6.
3. Make the second run, as the section above says, and pass item 7.
4. Write the pull request's body to `$BODY`: the profile's four sections,
   with the section below after Evidence. `"$SWEEP" --text "$BODY"` ends
   with a line beginning `privacy sweep: clean` and exits 0.
5. Open the pull request with `--body-file "$BODY"`.
6. Observe items 8 and 9, and run the full sweep of item 4 once more, now
   that the pull request's text is part of what it reads.

### The pull request's stranger section

The pull request's body holds this section after the profile's Evidence
section. Write it to `$BODY` with the rest of the body. Replace `<SHA>`
with the commit of item 7, `<N>` with the number `runcheck` printed, and
the last line with the Trips section of the second reply: its table, or
`None.`, after the replacement decision 6 gives.

````markdown
## Stranger runs

Two fresh agents, each given only the repository's address and the same brief, followed the README's five-minute path: the coding-agent steps with a scripted cook, and the chat steps as far as a person can go without a chat app.

**Run 1** was made by the author of the spec on 2026-11-19, on `main` at `d28bb614dd66138805544e2f810ad3129ba54897`, before any fix. It ended `STRANGER RUN: COMPLETE` with eleven trips, none blocking. This pull request fixes nine of them and leaves two:

| Trip | Kind | What tripped the stranger | What this pull request does |
|---|---|---|---|
| R1 | mismatch | The first-run interview left `chat/bundle.md` stale, and two checks failed | The skill and the README now say to rebuild it |
| R2 | guessed | Where the interview's edits go, and when they are committed | The skill now says: not committed, and the cook says when |
| R3 | guessed | Whether an example card for another dish is the cook's baseline | The skill now says it is not, and how a number borrowed from it is labeled |
| R4 | guessed | Where a first recipe's numbers come from | The skill now says a number with no source is written as missing |
| R5 | guessed | Where the pressure test fits on the path | The skill and the README now offer it before the cook |
| R6 | guessed | Whether the cook's report is troubleshot or logged at once | Nothing: both skills fit the report, and either order ends with the same log |
| R7 | guessed | The troubleshooting reference has no entry for the example report | The skill now says what to do when no entry fits |
| R8 | guessed | Whether the hand-off ends the turn | The skill now says the same reply goes on to the save |
| R9 | guessed | Whether a log written before the card is updated | The status rules now say its Recipe line is not |
| R10 | guessed | The test harness started the stranger outside the clone | Nothing: a person who opens the clone in an agent does not meet this |
| R11 | mismatch | Before a commit the editor gate printed `qc checked: 0` | The method page now says to use `--working-tree` |

The spec's author also rehearsed the second run twice on a local copy of the fixes. Each rehearsal found seven trips, none blocking; two from the first are fixed here, and the rest are left, with the reasons in the spec.

**Run 2** was made by the executor on this branch at `<SHA>`, after the fixes. It ended `STRANGER RUN: COMPLETE` with <N> trips, none blocking. They are recorded here and not fixed in this pull request:

<the Trips section of the second reply>
````

### Task 1 — Fix the skills and the method pages, and rebuild the chat bundle
- **Work:** Run `python3 "$S009/apply.py" $MD`, which prints four `edited:`
  lines. Then run `scripts/build-chat-bundle.sh`, which prints `chat bundle
  written: 33 files`. Then run `git add $MD chat/bundle.md`.
- **Touches:** `.agents/skills/chef-council/SKILL.md`,
  `.agents/skills/recipe-codify/SKILL.md`, `method/recipe-qc.md`,
  `method/status-and-versions.md`, `chat/bundle.md`
- **Gate:** This prints five lines, each a path followed by `: OK`:

  ```bash
  sha256sum -c - <<'SUMS'
  bcc049965d53fb3d45dbb9411a44d6f214099b2a61f7241ed4d8d8f27b47c6f0  .agents/skills/chef-council/SKILL.md
  a9a3291b49a3a42fa449c3059a6d1b0489bb89ceffbfe19f57e933300c2cd2a2  .agents/skills/recipe-codify/SKILL.md
  e51c5621c4fdac454e242416c7b09aadb938d1bd4d8b5f17f4f3885d327c9558  chat/bundle.md
  b13bbd5ae0752e9dae23560dc8aff7aee3979ff3c734a425244f435c70647e9a  method/recipe-qc.md
  aa55fe9987bdae2fb75af3014020dd6fa3c017f28b5486445e1fa8ec0284550f  method/status-and-versions.md
  SUMS
  ```

  `scripts/build-chat-bundle.sh --check; echo $?` prints `chat bundle
  checked: 33 files` then `0`. `linkcheck $MD; echo $?` prints `0` and
  nothing else. `anchorcheck $MD; echo $?` prints `anchors checked: 14`
  then `0`. `python3 scripts/check-skills.py` prints `skills checked: 4`.
  `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
  `0`, and `tail -1 "$OUT"` prints `OK`. `"$SWEEP" --text $MD
  chat/bundle.md` ends with a line beginning `privacy sweep: clean` and
  exits 0. `git diff --cached --check; echo $?` prints `0` and nothing
  else, and `git diff --cached --name-only | LC_ALL=C sort` prints exactly
  the five paths of Touches.
- **Nature:** mechanical

### Task 2 — Fix the README's five-minute steps
- **Work:** Run `python3 "$S009/apply.py" README.md`, which prints
  `edited: README.md`. Then run `git add README.md`.
- **Touches:** `README.md`
- **Gate:** `sha256sum README.md` prints a line that begins
  `f82bc00505e11899eeabe716be7f090d44f63213ccaabd9acd9eeec530f77181`.
  Definition-of-done item 3 holds as written. `"$SWEEP" --text README.md`
  ends with a line beginning `privacy sweep: clean` and exits 0. `git diff
  --cached --check; echo $?` prints `0` and nothing else, and `git diff
  --cached --name-only` prints exactly `README.md`. After the task's
  commit, definition-of-done items 1, 2, 4, and 5 hold as written. Items 6
  and 7 are observed after the push, and items 8 and 9 after the pull
  request is opened.
- **Nature:** mechanical

## Repo profile

No additions and no overrides. This spec follows `.agents/spec-profile.md`
as it stands: its deterministic checks are definition-of-done items 4, 5,
and 9, its Markdown observation method is item 6, and its agent-behavior
observation method, a fresh subagent briefed only with what the spec
names, is item 7. Every task is mechanical, so there is no tests task. No
card changes, so no editor run and no new report is owed in this
repository; the stranger's card lives only in its own clone.

## Cross-examination

One round, on the first complete draft, run by leg 1 on 2026-11-19 through
the route the profile's `## Independent review` section selects for an
Anthropic session at the architect tier: provider `meta`, model
`muse-wonder-full-1.0`, reasoning effort high, Muse Code 1.4.15
(1.4.15-R8339.1), read-only and sandboxed, with no shell, write, or web
tool. The dossier held the draft spec, `AGENTS.md`, the profile, ticket
T015 and the map, the six files of the touch set as they stand at
`base_sha`, the `cook-log` and `recipe-editor` skills, the cook-log and
recipe-card templates, `chat/README.md`, `chat/project-instructions.md`,
the troubleshooting reference, `scripts/check-qc.sh`,
`scripts/build-chat-bundle.sh`, and learnings L003, L006, L007, and L008.
It held no private-source file, and the privacy sweep's `--text` printed
`privacy sweep: clean` on it. The reviewer could not run the helpers. It
returned sixteen findings. Fourteen are accepted, and two are accepted in
part with the rest rejected:

1. **ACCEPT.** The cook's script never says "Pressure-test it." Decision 2
   now says the script is the same for every run and that the runs show
   only that the test is offered.
2. **ACCEPT.** The brief now says which of the cook's lines are said once
   and that C3 and C7 are said as often as needed.
3. **ACCEPT.** The brief's clone step is now one command that sets the
   directory, clones, and prints the clone's path.
4. **ACCEPT.** Decision 5 now sorts every line `runcheck` can print into
   a blocking trip or a malformed reply, and gives the order to read them.
5. **ACCEPT.** The brief now asks for a `Clone directory:` line, `runcheck`
   requires exactly one and prints it, and item 7 takes `D` from that
   line.
6. **ACCEPT.** The build plan now says every command this spec gives, a
   task's Work included, begins by sourcing the setup file.
7. **ACCEPT.** The sentence on a saved card for a different dish moved
   from Before you answer, step 4, into Develop (edit 3), and a borrowed
   number is now named and listed as not tested for this dish. Decision 10
   says why a saved card is not a new source.
8. **ACCEPT.** Edits 1 and 8 now say the bundle includes the kitchen
   files, and edit 1's sentence on committing applies when the agent wrote
   files.
9. **ACCEPT.** Edit 3 now says the Corrected recipe is put to the cook,
   and only what the cook then approves is the approved text.
10. **ACCEPT.** Edit 4 now reads "when the dish has a card", and says what
    goes under `## What probably happened` when no cause can be named.
11. **ACCEPT.** Edit 5 now keeps the save in the same reply and says what
    the last sentence of item 4 means.
12. **ACCEPT.** The sentence added to README step 3 did not settle which
    skill answers the report. It was removed, and the first run's R6 is
    now recorded as left, with the reason (decision 4).
13. **ACCEPT in part.** Edit 6 now speaks only of the log's Recipe line,
    and edit 11 says to name the log by its path. **REJECT** for the rest:
    a step to search for a log whose folder has a different slug from the
    card. Neither run met that case, and settling it means moving a log,
    which is outside this ticket (decision 10).
14. **ACCEPT in part.** Edit 10 now says a cue goes into the step it
    describes, beside that step's own cue, and under Notes when it
    describes no step. **REJECT** for the rest: a rule for replacing a
    step's cue and for setting `draft`, which would change what a card
    states beyond what the trip needs.
15. **ACCEPT.** Item 6 is now one loop over the five paths, and it says
    that `{owner}` and `{repo}` are typed as they stand. Leg 1 ran the
    loop on `main` for all five files.
16. **ACCEPT.** `### After Task 2` now gives the order of the push, the
    render check, the second run, the sweep of the pull request's body,
    the pull request, and the last gates. It is a procedure and not a
    task, because nothing in the repository changes and no commit is made.
    Decision 6 now says exactly which string is replaced.

After these edits leg 1 regenerated the hashes, rebuilt both tasks from
this spec's text in a fresh scratch clone, ran the helper probe again with
the two new cases, made the second rehearsal on the final files, and ran
the privacy sweep's `--text` on this spec, the edited files, and the brief.
The edits were not sent to a second round.
