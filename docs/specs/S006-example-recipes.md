---
date: 2026-11-19
id: S006
wayfinder: docs/wayfinder/W001-public-chef-council/issues/T012-example-recipes.md
target_release: none
status: draft
base_branch: main
base_sha: e4fcbf0f1e81554d38eb455889dc48bf94645409
work_branch: workstream/t012-example-recipes
pr_base: main
prior_specs:
  - docs/specs/archive/S001-scaffold.md
  - docs/specs/archive/S002-council-roster-and-vetting.md
  - docs/specs/archive/S003-chef-council-skill.md
  - docs/specs/archive/S004-codify-and-cook-log.md
  - docs/specs/archive/S005-editor-gate.md
references:
  - docs/wayfinder/W001-public-chef-council/MAP.md
  - docs/wayfinder/W001-public-chef-council/issues/T002-named-chefs-with-guardrails.md
  - docs/wayfinder/W001-public-chef-council/issues/T005-privacy-rules.md
  - docs/wayfinder/W001-public-chef-council/issues/T006-private-repository-names.md
  - docs/learnings/L001-scaffold.md
  - docs/learnings/L002-council-roster-and-vetting.md
  - docs/learnings/L003-chef-council-skill.md
  - docs/learnings/L004-codify-and-cook-log.md
  - docs/learnings/L005-editor-gate.md
  - .agents/spec-profile.md
cross_examined: pending
approved_by: pending
approved_at: pending
pr: none
kickbacks: 0
merged: none
harvested: none
---

# Example recipes: two cards at v1.1, each with a real editor report, and the generated index

## Goal and definition of done

Ship ticket T012: the repository's two example recipe cards, Butter-Roasted
Carrots with Jaggery and Sumac and Council Tuna Melt, each at v1.1 with its
public-release edits in its changelog, each checked by a fresh editor
subagent against a verbatim source packet with the editor's report
committed, and `recipes/INDEX.md` regenerated from them.

Both cards and both source packets are given byte for byte under `## File
contents`. Leg 1 wrote them from the maintainer's two private cards by the
edits decisions 8 to 12 list, built them in a scratch clone at `base_sha`,
and rehearsed the editor on those bytes (`## Build plan — agent loop`). The
executor writes the four files from this spec, regenerates the index, and
starts one fresh editor for each card; it does not reword a card or a
packet. The two reports are the editor's own text and are not given here.

Done means all of the following, each observed on the work branch's head
commit after Task 2, from the repository root, in a shell prepared as `##
Build plan — agent loop` says:

1. **The files.** `git ls-files recipes qc cook-logs .sources | sed -E
   's#[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$#<date>.md#'` prints exactly these five
   lines:

   ```text
   qc/sandwiches/council-tuna-melt/<date>.md
   qc/sides/butter-roasted-carrots/<date>.md
   recipes/INDEX.md
   recipes/sandwiches/council-tuna-melt.md
   recipes/sides/butter-roasted-carrots.md
   ```

   No source packet and no cook log is committed (decisions 3 and 7).
2. **The bytes.** This prints three lines, each a path followed by `: OK`:

   ```bash
   sha256sum -c - <<'SUMS'
   54e66767555d226cb68acaf4ab5a11f9bff5b422687e9c48a458f04266ceef9d  recipes/sandwiches/council-tuna-melt.md
   5b2e933ff179eacfa7272507d4d353d0cbdedac2b178bd851c2bd2f945c7b16b  recipes/sides/butter-roasted-carrots.md
   b3b99dbbf85bbee404019f96c76864a83d9029d1099dead90e7891f29ad65130  recipes/INDEX.md
   SUMS
   ```

   `git diff --name-only "$BASE_SHA"...HEAD -- . ':!docs/'` prints exactly
   the five paths of item 1, with the two dates as they are.
3. **The reports.** `reportcheck recipes/sides/butter-roasted-carrots.md;
   echo $?` prints `report ok: VERDICT: PASS
   qc/sides/butter-roasted-carrots/<YYYY-MM-DD>.md`, or the same line with
   `VERDICT: PASS WITH NOTES`, then `0`, and `reportcheck
   recipes/sandwiches/council-tuna-melt.md; echo $?` prints the same for
   `qc/sandwiches/council-tuna-melt/<YYYY-MM-DD>.md`. Each report was written
   by the fresh editor subagent of its task and by nothing else: the pull
   request's Evidence section gives, for each card, the editor's reply as
   saved, and says that the orchestrator wrote no line of either report.
4. **No person, no lens, no unsourced claim.** `namecheck
   recipes/sides/butter-roasted-carrots.md
   recipes/sandwiches/council-tuna-melt.md qc/sides/butter-roasted-carrots/*.md
   qc/sandwiches/council-tuna-melt/*.md; echo $?` prints `0` and nothing
   else. `grep -ci 'lens' recipes/sides/butter-roasted-carrots.md
   recipes/sandwiches/council-tuna-melt.md` prints the two paths, each
   followed by `:0`. `grep -ciE 'proved|150|sugar-free|no sugar|vinegar|hellmann|kewpie|leaner|flakier'
   recipes/sandwiches/council-tuna-melt.md` prints `0` (decision 8).
5. **The repository's checks.** `python3 scripts/check-skills.py; echo $?`
   prints `skills checked: 4` then `0`. `python3 scripts/check-council.py;
   echo $?` prints `council checked: 14 seated, 14 records` then `0`.
   `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
   `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"` prints
   `225`. `python3 scripts/build-index.py --check; echo $?` prints `index
   current: 2` then `0`. `python3 scripts/lint-cards.py; echo $?` prints
   `cards checked: 2` then `0`. After `git fetch origin`,
   `scripts/check-qc.sh; echo $?` prints `qc checked: 2` then `0`.
   `scripts/secret-scan.sh; echo $?` ends with `0`. `python3
   "$WAYFINDER/scripts/lint.py" docs/wayfinder/*/MAP.md; echo $?` prints `0`
   and nothing else. The three diff checks and the full privacy sweep pass
   as the profile's ship tail requires.
6. **CI.** `gh pr checks <PR> --watch` returns once every check has
   finished; then `gh pr checks <PR>` reports every check passed, and lists
   three checks: `gitleaks (full history)`, `tests`, and `editor gate`. With
   `HEAD_SHA=$(gh pr view <PR> --json headRefOid --jq .headRefOid)` and
   `RUN=$(gh run list --commit "$HEAD_SHA" --workflow CI --event pull_request
   --json databaseId --jq '.[0].databaseId')`, `RUN` is not empty, `gh run
   view "$RUN" --log > "$OUT"` succeeds, and each of these two prints `0`:
   `grep -qF 'qc checked: 2' "$OUT"; echo $?` and `grep -qF 'cards checked:
   2' "$OUT"; echo $?`. That is the ticket's "both cards pass
   `scripts/check-qc.sh` and the linter in CI".
7. **The rendered pages.** For each of the two cards, the two reports, and
   `recipes/INDEX.md`, on the pushed branch, `gh api
   "repos/{owner}/{repo}/contents/<path>?ref=workstream/t012-example-recipes"
   -H 'Accept: application/vnd.github.html' > "$OUT"` succeeds. `grep -c
   '<table' "$OUT"` prints at least `4` for each card and at least `1` for
   the index. The orchestrator reads each of the five rendered pages and
   answers yes to both: every ingredient row and every failure-mode row of a
   card sits in a table, with no row shown as a line of text with `|` marks;
   and each of the index's two links is to a card of item 1. How GitHub
   shows a card's front matter is not predicted here (L001) and is not part
   of this item.

## Decisions

1. **Scope.** This spec adds five files: the two cards, the regenerated
   index, and the two editor reports. It changes no skill, script, test,
   template, method page, `AGENTS.md`, `README.md`, or workflow. `README.md`
   and its links to the examples are T014's.
2. **Who approved the text.** The cook, for these two cards, is the
   maintainer. The approved text of each card is the block under `##
   Approved text` of its packet in `## File contents`. Leg 1 wrote it from
   the maintainer's private v1.0 card by the edits of the design report's
   Appendix B (`private-sources/design/design-report.md`), which ticket T012
   names as the exact scrubs and rewrites, plus the further edits decisions
   8 to 11 list with their reasons. The approval of this spec is the
   approval of that text. Nobody opens anything under `private-sources/` to
   execute or review this spec: the bytes here are complete.
3. **Packets stay in `.sources/` and are not committed.** The ticket leaves
   this to the spec. `AGENTS.md`, `templates/source-packet.md`,
   `method/recipe-qc.md`, and the `recipe-codify` skill all say that a packet
   is never committed, and an example that broke the rule it demonstrates
   would teach the wrong thing. The two packets are published all the same,
   because this spec holds their bytes and is committed: anyone can write
   them back to `.sources/` with `extract` and rerun the editor. Each report's
   Packet line names the ignored path, which is what a stranger's own reports
   will show.
4. Each example card is saved as a new card in this repository. Its v1.0 exists only in my private cooking repo and is not published, so the packet holds no previous version. The card starts here at v1.1, not v1.0, because the approved text is v1.0 with the public-release edits, and its changelog keeps a line for each of the two versions.
5. The carrots keep the status `reviewed`, which the ticket gives them. The cut size is not an open gap: the v1.0 card held `reviewed` beside the same sentence about the cut dimension, and the instruction a cook follows is complete without a dimension, which is to cut the carrots into similar-size roasting pieces, roast for the stated range, and pull them when browned and tender. What the cut was at a given cook is for the next experiment to record.
6. The tuna melt's kitchen evidence is `not-recorded`. It was cooked once, on 2026-08-01, and no cook log of that cook was written: my private cooking repo records the result only as one line of the card's changelog. No cook log is written for it now, because a log holds the cook's own words and those were not kept.
7. **Why decisions 4 to 6 are written as they are, and what they depart
   from.** Each of the three is one unbroken paragraph because the packets
   quote it word for word under `## Scope instruction`, beside the ticket's
   own words; do not rewrap them. Decision 4 follows the ticket ("both as
   v1.1"), where `method/status-and-versions.md` would give a new card
   `v1.0`; that page says to follow the cook when the two disagree. Decision
   5 exists because leg 1's first rehearsal editor failed the carrots card
   on this point and said it was the cook's call; the ticket had already
   made that call. Decision 6 departs from Appendix B, which wrote the
   evidence as `cooked-once`: that appendix predates
   `method/status-and-versions.md`, under which `cooked-once` means one
   logged cook and `not-recorded` means a recipe "brought in from somewhere
   else" that "has been cooked, but no log says when or how it went". A
   cook log written now could hold only `Not reported.` lines, because the
   `cook-log` skill allows nothing but the cook's own words. The card's
   changelog and Notes still say that it was cooked once, when, and in which
   variation, which is the ticket's "cooked once (the dill-pickle variant,
   2026-08-01)". To raise the value later, the maintainer reports that cook
   in their own words, the `cook-log` skill writes the log, and
   `recipe-codify` updates the card through a fresh editor check. No leg of
   this spec does that.
8. **What an unsourced claim is, and what was removed.** For the ticket's
   "makes no unsourced claim", an unsourced claim is a statement that a
   named publisher, person, or test showed something; a statement of fact
   about a named product or brand; or a physical constant or a composition
   (a melting temperature, what a food contains), given with no source that
   was read. A card's own reasoning about its method, such as "crowded
   carrots steam instead of browning", is the recipe's rationale and is not
   such a claim. The tuna melt loses these, the first four by Appendix B and
   the last two by this definition:
   - "(ATK Method)" in a heading, and "(Kenji's trick)" in step 6;
   - "ATK proved this reduces sogginess dramatically", which becomes "so
     pre-toasting the inside faces limits sogginess";
   - "Swiss is a medium-moisture cheese that melts at ~150°F", which
     becomes "on high heat, the bread burns before the cheese melts";
   - the two variation credits, which become "The version that was cooked."
     and "A brighter variation (untested).";
   - the whole claim about what Duke's contains. Appendix B softened it to
     "Duke's has no added sugar", which is still a product fact with no
     source read, so the card says only "This recipe was developed with
     Duke's. With a sweeter mayo, add ½ tsp more lemon juice." The two
     other brands the v1.0 card named there are gone with it;
   - "Yellowtail is slightly leaner and flakier" and "albacore holds more
     water", leaving the instruction to drain albacore more.
   The ingredient lines keep their product names (Duke's mayonnaise,
   Diamond Crystal as the preferred kosher salt): naming what the cook used
   is not a claim about it.
9. **No person, no publisher, and no lens on either card.** Neither card
   names a chef, a publisher, the maintainer, or a lens, anywhere. The
   Source lines read `Original. Developed with the council on 2026-09-12 and
   pressure-tested; not yet cooked as written.` and `Original. Developed
   with the council; no published recipe was adapted.` Appendix B's tuna
   melt Source line listed four kinds of lens in brackets; they are left
   out, because the ticket requires every lens reference to read
   `<Name>-style lens`, those four are not seated names, and naming the
   seated ones would credit them. The changelogs call the predecessor "my
   private cooking repo" (decision T006).
10. **The carrots edits.** Appendix B's: the Source line; the notes-app
    field removed; "the household verdict" becomes "the cook's verdict";
    the note for other kitchens on the cumin, in Appendix B's words; v1.1
    with its changelog line. And four the scrub needs: the sentence that
    pointed to a card which is not published here is removed; the Storage
    line's link, which led to a private file, now leads to rows K3 and K6
    of `.agents/skills/chef-council/references/food-safety.md`, which give
    the same two numbers; the kitchen evidence is `untested`, the value
    `method/status-and-versions.md` gives a recipe with no logged cook,
    where v1.0 said "not recorded" in a private sense and the ticket says
    "not yet cooked as written"; and the Yield line reads `2 lb carrots;
    servings not recorded`, which states the batch first. The ingredient
    lines, quantities, temperature, times, and the five steps are v1.0's.
11. **The other tuna melt edits.** The category is `sandwiches` (Appendix
    B's first choice). The status is `reviewed`, which Appendix B adds. The
    two variations nobody is recorded as cooking besides the caper one are
    marked `Untested.`, as `templates/recipe-card.md` asks, and one Notes
    line says that only the dill-pickle variation has been cooked and the
    base version has not, which Appendix B states. The Storage lines are the
    cook's own keeping notes and are unchanged; the card gives no cooking
    endpoint, so no food-safety row is cited. The ingredient lines,
    quantities, heats, times, and the ten steps are v1.0's.
12. **Card form.** Each card follows `templates/recipe-card.md`: the block
    at the top, the seven lines under the title, the template's headings in
    its order, and a `## Next experiment` section. What differs from the
    packet's layout is arrangement only: a dash in a Prep cell is written
    `None`; a blank Problem cell in the tuna melt's failure table repeats
    the problem of the row above; the bracketed notes after the packet's
    Status and Kitchen evidence values are left off those two lines, which
    the linter requires to equal the block's values, and what they say is
    on the Source line, in the Notes, and in the changelog; italics are
    dropped; and step names end in a full stop. `mirrors` is `none`.
13. **Dates.** Both cards and both packets carry 2026-11-19, the day leg 1
    fixed their text, whatever day leg 2 runs. A report is named for the
    day its editor ran, which is why no gate names that date.
14. **One fresh editor for each card, and no second try.** Each card is
    checked once, by a fresh subagent at the orchestrator tier that is
    given the brief of `### The editor run` and nothing else. A passing
    verdict, `PASS` or `PASS WITH NOTES`, is the gate. Notes are copied into
    the pull request's Evidence section and the card is not edited for
    them, because an edited card needs a fresh check and its bytes are fixed
    here. A `FAIL`, or a report that `reportcheck` rejects, ends the task
    without a commit: the orchestrator reports ``Question: the editor check
    of `<card path>` in Task <N> of `docs/specs/S006-example-recipes.md`
    did not pass: <the blocking rows, or reportcheck's lines>; revise the
    spec?`` and leaves the card, the index, and the report in the working
    tree as they are. It does not start a second editor on the same bytes,
    which would be asking until one agrees, and it never edits or deletes a
    report. This replaces the `2-spec-execute` attempt loop from the moment
    an editor has been started; a mechanical gate that fails before that is
    retried as that skill says.
15. **Mechanical gates come before the editor (L002).** Each task runs its
    hash, lint, link, name, and privacy gates on the card and the packet
    first, and starts the editor only when they pass.
16. **Which bytes are hashed (L005).** The pinned SHA-256 of each card is
    of the bytes with line-feed endings, as `extract` writes them. The
    prerequisites require a checkout that does not convert line endings, so
    the file the editor hashes is the file git commits, and each task's last
    gate line runs the gate's default mode on the commit, which hashes the
    committed bytes as CI does. The general fix L005 asks for, in the gate
    or in a `.gitattributes` rule, belongs to the next spec that edits
    `scripts/check-qc.sh`, the report format, or `method/recipe-qc.md`, or
    that tells a cook to hash a card (T013 or T014); this spec edits none of
    them.
17. **No tests task.** Both tasks are `mechanical`: no script, test, or
    skill changes. The existing tests `test_this_repository_lints_clean` and
    `test_this_repository_index_is_current` run against the new cards in
    the unittest line of each gate.
18. **The editor may read this spec.** The editor's brief limits it to the
    repository, and this spec is in the repository. The packet and the card
    are its evidence, as its skill says; a report that leans on this spec's
    reasoning instead of the packet is a note for the reviewer, not a gate
    failure.

## Prerequisites

- Leg 2 starts from this spec's approval commit on
  `workstream/t012-example-recipes`, which already holds the claim commit
  for T012. Staging, the per-task commit with its `Spec-Task: S006/<N>`
  trailer, the push, the pull request, and the base-drift check are the
  `2-spec-execute` skill's standing procedure and the profile's ship tail.
  Each task's commit holds exactly that task's Touches.
- The executor's machine has Git 2.32 or later, Bash, Python 3, GNU
  coreutils (`sha256sum`), and an authenticated `gh` that has `gh run list
  --commit`. It is Linux x86_64, where `scripts/secret-scan.sh` fetches its
  pinned gitleaks, or `GITLEAKS_BIN` names an installed gitleaks of the
  pinned version (profile). `git config user.email` ends in
  `@users.noreply.github.com` (profile). `git rev-parse --verify
  origin/main` succeeds after `git fetch origin`.
- The checkout does not convert line endings (decision 16): `git config
  core.autocrlf` prints nothing, `false`, or `input`, and `git ls-files
  .gitattributes` prints nothing.
- Before Task 1, `git status --porcelain --untracked-files=all` prints
  nothing, and `ls .sources qc cook-logs 2>/dev/null` prints nothing: the
  checkout holds no packet, report, or cook log of its own.
- A Claude Code session in this repository runs the Stop hook of
  `.claude/settings.json` when it stops. Between writing a card and the
  editor's report it would keep the session open once, which is the hook
  working as intended. It is not part of any gate, and no task stops in
  that window.
- The editor subagents need to read and write files inside the repository
  and to run `bash`, `git`, and `python3` there. They need no web access
  and are told not to use it.
- `test -x "$(git rev-parse --git-common-dir)/info/privacy-sweep"` succeeds.
  `WAYFINDER` is set to the directory the harness prints when the wayfinder
  skill loads, and `test -f "$WAYFINDER/scripts/lint.py"` succeeds
  (profile). If either is missing, report ``Question: <the privacy sweep |
  the Wayfinder lint> that the profile requires is not on this machine;
  provide it?`` and stop.

### Writing a file from this spec

Each file under `## File contents`, and each helper below, is the text
inside the fenced block that follows its heading: every line between the
opening and closing fence, each ended by a line feed, with nothing added or
removed. The opening fence is a line of four backticks, with or without a
language name after them, and the closing fence is the next line that is
exactly four backticks. `block` prints one such block, and `extract` writes
one file from it. `SPEC` is set in the setup of `## Build plan — agent
loop`.

```bash
block() {
  python3 - "$SPEC" "$1" <<'PY'
import re, sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index(sys.argv[2])
opening = next(i for i in range(start + 1, len(lines)) if re.fullmatch(r"`{4,}[a-z]*", lines[i]))
fence = re.match(r"`+", lines[opening]).group(0)
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == fence)
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
}
extract() {
  mkdir -p "$(dirname "$1")"
  block "#### File: \`$1\`" > "$1"
}
```

Usage: `extract recipes/sides/butter-roasted-carrots.md`. The SHA-256 gates
decide whether a file is right, whichever way it was written.

### Gate helpers

Three helpers, not repository files, loaded as the setup of `## Build plan
— agent loop` says.

`linkcheck` is the helper of S002 to S005, unchanged. It reads the Markdown
files named on its command line, skips fenced code blocks, and requires the
target of every inline link with a relative target to be a path git tracks
or has staged. It prints one line per broken link and returns 1, or prints
nothing and returns 0.

`namecheck` reads the files named on its command line and prints one line,
`<path>:<line number>: names a person or a publisher`, for each line that
holds, in any letter case, a name on the council's roster, a publisher's
short name, or the maintainer's first name; it returns 1 when it prints any
line and 0 otherwise. The pattern is the roster of `kitchen/council.md` at
`base_sha`, written as the shortest part of each name that is not an
ordinary word.

`reportcheck <card path>` checks the editor report of one card. It requires
exactly one file under `qc/<category>/<slug>/`, named `<YYYY-MM-DD>.md` for
a real date; exactly one line that starts `VERDICT:`, reading `VERDICT:
PASS` or `VERDICT: PASS WITH NOTES`; exactly one line that starts
`Card-SHA256:`, giving the SHA-256 of the card file as it stands; a first
line `# Editor report: <the card's title> v1.1`; one Card line with the
card's path, one Date line with the date in the file's name, one Kind of
save line that starts `new card`, one Packet line that holds
`.sources/<slug>/2026-11-19.md`, one Source line, and one Editor line; the
three headings `Discrepancies`, `Additions`, and `Checks run` in that
order and no other `##` heading; no table row whose last cell is
`blocking`; and no line that `namecheck` would report. It prints `report
ok: <the verdict line> <the report's path>` and returns 0, or one line per
problem and returns 1.

#### Helper: `linkcheck`

````bash
linkcheck() {
  python3 - "$@" <<'PY'
import os, re, subprocess, sys
bad = 0
for path in sys.argv[1:]:
    fenced = False
    for line in open(path, encoding="utf-8"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for target in re.findall(r"\]\(([^)\s]+)\)", line):
            if re.match(r"[a-z]+:|#", target):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), target.split("#")[0]))
            listed = subprocess.run(
                ["git", "ls-files", "--", target], capture_output=True, text=True
            ).stdout.splitlines()
            if listed != [target]:
                print("%s: broken link %s" % (path, target))
                bad = 1
sys.exit(bad)
PY
}
````

#### Helper: `namecheck`

````bash
NAMES='kenji|l[oó]pez|test kitchen|(^|[^a-z])atk([^a-z]|$)|souza|heston|blumenthal|stella parks|saffitz|sohla|waylly|rick martinez|jaffrey|dunlop|samin|nosrat|p[eé]pin|ottolenghi|maangchi|hazan|charles'
namecheck() {
  NAMES="$NAMES" python3 - "$@" <<'PY'
import os, re, sys
names = re.compile(os.environ["NAMES"], re.I)
bad = 0
for path in sys.argv[1:]:
    for number, line in enumerate(open(path, encoding="utf-8"), 1):
        if names.search(line):
            print("%s:%d: names a person or a publisher" % (path, number))
            bad = 1
sys.exit(bad)
PY
}
````

#### Helper: `reportcheck`

````bash
reportcheck() {
  NAMES="$NAMES" python3 - "$1" <<'PY'
import datetime, glob, hashlib, os, re, sys
card = sys.argv[1]
match = re.fullmatch(r"recipes/([a-z0-9-]+)/([a-z0-9-]+)\.md", card)
if not match:
    sys.exit("reportcheck: %s is not a card path" % card)
category, slug = match.groups()
reports = sorted(glob.glob("qc/%s/%s/*" % (category, slug)))
if len(reports) != 1:
    sys.exit("reportcheck: expected one report under qc/%s/%s/, found %d" % (category, slug, len(reports)))
report = reports[0]
name = os.path.basename(report)
problems = []
day = name[:-3]
try:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\.md", name):
        raise ValueError
    datetime.date(int(day[:4]), int(day[5:7]), int(day[8:]))
except ValueError:
    problems.append("is not named <YYYY-MM-DD>.md for a real date")
card_bytes = open(card, "rb").read()
title = next(line[2:] for line in card_bytes.decode("utf-8").split("\n") if line.startswith("# "))
lines = [line.rstrip() for line in open(report, encoding="utf-8").read().split("\n")]
verdicts = [line for line in lines if line.startswith("VERDICT:")]
hashes = [line for line in lines if line.startswith("Card-SHA256:")]
if verdicts not in (["VERDICT: PASS"], ["VERDICT: PASS WITH NOTES"]):
    problems.append("the verdict lines are %r" % verdicts)
if hashes != ["Card-SHA256: " + hashlib.sha256(card_bytes).hexdigest()]:
    problems.append("the Card-SHA256 line is not the hash of the card")
if lines[0] != "# Editor report: %s v1.1" % title:
    problems.append("the first line is %r" % lines[0])
wanted = [
    ("Card", lambda rest: rest == "`%s`" % card),
    ("Date", lambda rest: rest == day),
    ("Kind of save", lambda rest: rest.startswith("new card")),
    ("Source", lambda rest: bool(rest)),
    ("Packet", lambda rest: ".sources/%s/2026-11-19.md" % slug in rest),
    ("Editor", lambda rest: bool(rest)),
]
for label, accepts in wanted:
    mark = "- **%s:** " % label
    found = [line[len(mark):] for line in lines if line.startswith(mark)]
    if len(found) != 1 or not accepts(found[0]):
        problems.append("the %s line is %r" % (label, found))
headings = [line for line in lines if line.startswith("## ")]
if headings != ["## Discrepancies", "## Additions", "## Checks run"]:
    problems.append("the headings are %r" % headings)
if any(re.search(r"\|\s*blocking\s*\|$", line) for line in lines):
    problems.append("a discrepancy row is blocking")
names = re.compile(os.environ["NAMES"], re.I)
for number, line in enumerate(lines, 1):
    if names.search(line):
        problems.append("line %d names a person or a publisher" % number)
if problems:
    for problem in problems:
        print("reportcheck: %s: %s" % (report, problem))
    sys.exit(1)
print("report ok: %s %s" % (verdicts[0], report))
PY
}
````

### The editor run

The check of each card is one fresh subagent, started through the harness's
agent tool at the orchestrator tier, of the general-purpose kind, briefed
with exactly the brief below and nothing else, with `<dir>` replaced by the
absolute path `git rev-parse --show-toplevel` prints, and `<packet>` and
`<card>` by the two paths the task names. The orchestrator tells it nothing
about how the card was written, does not show it this spec, and saves its
reply, exactly as returned, to a file outside the repository (`REPLY=$(mktemp)`).
The orchestrator writes no line of a report and changes no line of one.

```text
You are an AI agent starting a fresh session in the repository at <dir> . You did not write any file in it. Read AGENTS.md in that directory and follow it, then follow the recipe-editor skill it lists to check one recipe card. The source packet is at <packet> and the card is at <card> . Read and write only files inside that directory, and do not use the web. Return only your reply, exactly as the skill says to give it, with nothing before or after it.
```

The two tasks run one after the other, never at the same time: the second
card's index holds the first card's row.

## Build plan — agent loop

Run every command from the repository root, in one Bash shell in which the
setup has been run first: the three lines below, then the `block` and
`extract` definitions of `### Writing a file from this spec`, pasted as
written, then the three `eval` lines, which load the helpers from this
spec's own text.

```bash
OUT=$(mktemp)
SPEC="$(git rev-parse --show-toplevel)/docs/specs/S006-example-recipes.md"
BASE_SHA=e4fcbf0f1e81554d38eb455889dc48bf94645409
```

```bash
eval "$(block '#### Helper: `linkcheck`')"
eval "$(block '#### Helper: `namecheck`')"
eval "$(block '#### Helper: `reportcheck`')"
```

Afterward `type -t block extract linkcheck namecheck reportcheck` prints
`function` five times. A gate passes only when every command in it prints
what is stated. Where a gate ends in `; echo $?`, the printed status is part
of the expected output. The gate's commands run in the order listed.

Baseline, measured by leg 1 on 2026-11-19 in a scratch clone at `base_sha`:
`python3 -m unittest discover -s tests -v` exits 0 and ends `OK` with 225
tests; `python3 scripts/check-skills.py` prints `skills checked: 4`;
`python3 scripts/check-council.py` prints `council checked: 14 seated, 14
records`; `python3 scripts/lint-cards.py` prints `cards checked: 0`. Every
other gate line names a file this spec creates or changes, so it is red on
the base by design; none measures old debt. Leg 1 then built both tasks in
a scratch clone from this spec's text with `extract`, loading the helpers by
the setup above, and ran every gate line below on it except the lines that
need this run's own commits or `origin` (the two `git fetch origin` lines
ran against the clone's base tag with `--base`), and ran the privacy
sweep's `--text` on the four files this spec gives.

Editor rehearsal (L003), run by leg 1 on 2026-11-19 with fresh
orchestrator-tier subagents briefed exactly as `### The editor run` briefs
them, each in its own scratch clone at `base_sha` holding the card, the
packet, and the regenerated index, as its task leaves them before the
editor starts. There were two rounds for the carrots and one for the tuna
melt. In the first round the tuna melt's editor returned `VERDICT: PASS`
with no discrepancy and no addition, on the bytes this spec gives. The
carrots' editor returned `VERDICT: FAIL` with one blocking row: the status
`reviewed` beside a method step saying the cut dimension was not recovered,
which it read as an open gap and called the cook's call. Leg 1 changed
nothing on the card. It added decision 5 and quoted it in the carrots
packet's scope instruction, and a new fresh editor in a new clone then
returned `VERDICT: PASS` with no discrepancy, on the bytes this spec gives.
`reportcheck` printed `report ok: VERDICT: PASS` with the report's path for
both passing reports and listed the verdict and the blocking row for the
failed one, and `scripts/check-qc.sh --working-tree` against each clone's
base printed `qc checked: 1` for the passing carrots clone. Both editors
wrote their Source line in their own words ("a private cooking
repository"), which is why `reportcheck` asks only that the line is there.
One run is a sample: a `FAIL` in leg 2 is a question about this spec
(decision 14), not a reason to run a second editor.

### Task 1 — Add the butter-roasted carrots card v1.1 with its editor report
- **Work:** In this order.
  1. Run `extract .sources/butter-roasted-carrots/2026-11-19.md`, then
     `extract recipes/sides/butter-roasted-carrots.md`, then `python3
     scripts/build-index.py`, which prints `index written: 1`.
  2. Run the gate's lines "before the editor". Only when all pass, go on.
  3. Start the editor as `### The editor run` says, with `<packet>` as
     `.sources/butter-roasted-carrots/2026-11-19.md` and `<card>` as
     `recipes/sides/butter-roasted-carrots.md`. Save its reply.
  4. Run the gate's lines "after the editor". On any failure there, follow
     decision 14: report the `Question:` and commit nothing.
- **Touches:** `recipes/sides/butter-roasted-carrots.md`,
  `recipes/INDEX.md`, and the one report the editor writes,
  `qc/sides/butter-roasted-carrots/<YYYY-MM-DD>.md`. The packet,
  `.sources/butter-roasted-carrots/2026-11-19.md`, is written and is not
  committed: git ignores it.
- **Gate:**
  - Before the editor:
    - This prints three lines, each path followed by `: OK`:

      ```bash
      sha256sum -c - <<'SUMS'
      e60d5e8595b3a007c862cf35a10a1dac66575f1e268aa5f7081569ab003539e8  .sources/butter-roasted-carrots/2026-11-19.md
      5b2e933ff179eacfa7272507d4d353d0cbdedac2b178bd851c2bd2f945c7b16b  recipes/sides/butter-roasted-carrots.md
      b1953e11f9dcf89b0843bd846d8a8b579ec722ebe3b8779f73137fc919b58229  recipes/INDEX.md
      SUMS
      ```

    - `git check-ignore -q .sources/butter-roasted-carrots/2026-11-19.md;
      echo $?` prints `0`.
    - `python3 scripts/lint-cards.py; echo $?` prints `cards checked: 1`
      then `0`.
    - `linkcheck recipes/sides/butter-roasted-carrots.md recipes/INDEX.md;
      echo $?` prints `0` and nothing else, after `git add -N
      recipes/sides/butter-roasted-carrots.md`, which lets git list the new
      card without staging its content.
    - `namecheck recipes/sides/butter-roasted-carrots.md; echo $?` prints
      `0` and nothing else, and `grep -ci 'lens'
      recipes/sides/butter-roasted-carrots.md` prints `0`.
    - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
      recipes/sides/butter-roasted-carrots.md
      .sources/butter-roasted-carrots/2026-11-19.md` ends with a line
      beginning `privacy sweep: clean` and exits 0.
  - After the editor:
    - The `sha256sum -c` block above prints the same three `: OK` lines:
      the editor changed neither the card, the packet, nor the index.
    - `git status --porcelain --untracked-files=all | sed -E
      's#[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$#<date>.md#'` prints exactly:

      ```text
       M recipes/INDEX.md
       A recipes/sides/butter-roasted-carrots.md
      ?? qc/sides/butter-roasted-carrots/<date>.md
      ```

    - `reportcheck recipes/sides/butter-roasted-carrots.md; echo $?` prints
      `report ok: VERDICT: PASS
      qc/sides/butter-roasted-carrots/<YYYY-MM-DD>.md`, or the same line
      with `VERDICT: PASS WITH NOTES`, then `0`.
    - The orchestrator reads the report and answers yes: no row under
      Discrepancies and no line under Additions says that the card would
      have a cook do something the packet's approved text does not say.
    - After `git fetch origin`, `scripts/check-qc.sh --working-tree; echo
      $?` prints `qc checked: 1` then `0`.
    - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
      prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
      prints `225`.
    - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
      qc/sides/butter-roasted-carrots/*.md` ends with a line beginning
      `privacy sweep: clean` and exits 0.
    - After the task's commit, `git status --porcelain
      --untracked-files=all` prints nothing, `git ls-files .sources` prints
      nothing, and `scripts/check-qc.sh; echo $?` prints `qc checked: 1`
      then `0` (decision 16).
- **Nature:** mechanical

### Task 2 — Add the council tuna melt card v1.1 with its editor report
- **Work:** In this order.
  1. Run `extract .sources/council-tuna-melt/2026-11-19.md`, then `extract
     recipes/sandwiches/council-tuna-melt.md`, then `python3
     scripts/build-index.py`, which prints `index written: 2`.
  2. Run the gate's lines "before the editor". Only when all pass, go on.
  3. Start the editor as `### The editor run` says, with `<packet>` as
     `.sources/council-tuna-melt/2026-11-19.md` and `<card>` as
     `recipes/sandwiches/council-tuna-melt.md`. Save its reply.
  4. Run the gate's lines "after the editor". On any failure there, follow
     decision 14: report the `Question:` and commit nothing.
- **Touches:** `recipes/sandwiches/council-tuna-melt.md`,
  `recipes/INDEX.md`, and the one report the editor writes,
  `qc/sandwiches/council-tuna-melt/<YYYY-MM-DD>.md`. The packet,
  `.sources/council-tuna-melt/2026-11-19.md`, is written and is not
  committed: git ignores it.
- **Gate:**
  - Before the editor:
    - This prints three lines, each path followed by `: OK`:

      ```bash
      sha256sum -c - <<'SUMS'
      dd06e999bc2188fc65deb8c32b5b1998ebda7776559886ddd2a26a680a25fdfa  .sources/council-tuna-melt/2026-11-19.md
      54e66767555d226cb68acaf4ab5a11f9bff5b422687e9c48a458f04266ceef9d  recipes/sandwiches/council-tuna-melt.md
      b3b99dbbf85bbee404019f96c76864a83d9029d1099dead90e7891f29ad65130  recipes/INDEX.md
      SUMS
      ```

    - `git check-ignore -q .sources/council-tuna-melt/2026-11-19.md; echo
      $?` prints `0`.
    - `python3 scripts/lint-cards.py; echo $?` prints `cards checked: 2`
      then `0`.
    - `linkcheck recipes/sandwiches/council-tuna-melt.md recipes/INDEX.md;
      echo $?` prints `0` and nothing else, after `git add -N
      recipes/sandwiches/council-tuna-melt.md`.
    - `namecheck recipes/sandwiches/council-tuna-melt.md; echo $?` prints
      `0` and nothing else, `grep -ci 'lens'
      recipes/sandwiches/council-tuna-melt.md` prints `0`, and `grep -ciE
      'proved|150|sugar-free|no sugar|vinegar|hellmann|kewpie|leaner|flakier'
      recipes/sandwiches/council-tuna-melt.md` prints `0`.
    - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
      recipes/sandwiches/council-tuna-melt.md
      .sources/council-tuna-melt/2026-11-19.md` ends with a line beginning
      `privacy sweep: clean` and exits 0.
  - After the editor:
    - The `sha256sum -c` block above prints the same three `: OK` lines.
    - `git status --porcelain --untracked-files=all | sed -E
      's#[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$#<date>.md#'` prints exactly:

      ```text
       M recipes/INDEX.md
       A recipes/sandwiches/council-tuna-melt.md
      ?? qc/sandwiches/council-tuna-melt/<date>.md
      ```

    - `reportcheck recipes/sandwiches/council-tuna-melt.md; echo $?` prints
      `report ok: VERDICT: PASS
      qc/sandwiches/council-tuna-melt/<YYYY-MM-DD>.md`, or the same line
      with `VERDICT: PASS WITH NOTES`, then `0`.
    - The orchestrator reads the report and answers yes: no row under
      Discrepancies and no line under Additions says that the card would
      have a cook do something the packet's approved text does not say.
    - After `git fetch origin`, `scripts/check-qc.sh --working-tree; echo
      $?` prints `qc checked: 2` then `0`: both cards differ from
      `origin/main`, and the first card's report is in Task 1's commit.
    - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
      prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
      prints `225`.
    - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
      qc/sandwiches/council-tuna-melt/*.md` ends with a line beginning
      `privacy sweep: clean` and exits 0.
    - After the task's commit, `git status --porcelain
      --untracked-files=all` prints nothing, `git ls-files .sources` prints
      nothing, and `scripts/check-qc.sh; echo $?` prints `qc checked: 2`
      then `0` (decision 16).
- **Nature:** mechanical

## Repo profile

`.agents/spec-profile.md` governs, with no override. Three things it leaves
to this spec:

- **The pull request's Evidence section** also holds, for each card: the
  editor's reply as saved, the report's path, its verdict line, every row
  and note of a `PASS WITH NOTES`, and the sentence that the orchestrator
  wrote no line of the report. It says that the source packets are not
  committed and that this spec holds their bytes (decision 3), and it names
  decisions 5, 6, and 8 as the places where this spec departs from, or adds
  to, the design appendix the ticket cites.
- **Agent behavior.** The two editor runs are the profile's "fresh subagent
  through the harness's agent tool, briefed only with what the spec names".
  No provider call is made.
- **The profile's check lines** already cover this spec: `cards checked:
  <N>` and `qc checked: <N>` now print `2` on the work branch.

## Cross-examination

**In progress. This draft is not ready for approval.** The blind
cross-examination ran on 2026-11-19 through the profile's route: Meta,
`muse-wonder-full-1.0`, high reasoning effort, Muse Code 1.4.15
(1.4.15-R8339.1), read-only in the routes document's sandbox, on a dossier
of this draft, `AGENTS.md`, the profile, ticket T012, and the repository
files this spec leans on, with no private-source file. It returned 17
findings. Three of them turn on things only the cook can say, so leg 1
stopped to ask before editing: the text above is the draft as the reviewer
read it, and the cards, packets, hashes, and rehearsal record will change
with the answers. The dispositions below are leg 1's plan; each becomes
final, with its resulting edit, when the draft is revised.

1. **Commit, push, pull request, CI, and rendering have no owning task.**
   Planned: ACCEPT in part. Each task's Work gains a step saying that the
   commit is the `2-spec-execute` task loop's, followed by the "after the
   commit" lines. The ship tail stays that skill's and the profile's, as in
   S001 to S005.
2. **The editor is primed with the spec author's reasoning.** Planned:
   ACCEPT. A packet's scope instruction will hold only the ticket's lines
   and the cook's own answers; no decision of this spec is quoted to the
   editor, the brief keeps the editor out of `docs/specs/`, and decision 18
   goes.
3. **The tuna melt's `not-recorded` does not meet the rule's conditions.**
   Waiting on the cook (question 2 below).
4. **The carrots cannot be `reviewed` with an unrecovered cut dimension
   unless the cook says so.** Waiting on the cook (question 1 below).
   Decision 5, which argued the point to the editor, goes either way.
5. **The tuna melt describes its one cook two ways** (the variation says to
   skip the lemon juice; the changelog says lemon juice was used). Waiting
   on the cook (question 3 below). The private card holds both statements.
6. **Unsourced claims and an uncited storage time remain.** Planned: ACCEPT
   in part. "Pure fat and protein" is a composition under decision 8 and is
   reworded; the tuna salad's storage line cites the food-safety reference.
   REJECT for "with a sweeter mayo" and the albacore note: each is an
   instruction, and neither states a fact about a product.
7. **`reportcheck` does not check the report's form closely.** Planned:
   ACCEPT in part: the ten Checks run lines, `None.` under Discrepancies
   for `PASS`, only `minor` rows for `PASS WITH NOTES`, and `blocking` in
   any letter case. REJECT matching the Source line to the packet: both
   rehearsal editors reworded it, as the report format lets them.
8. **`namecheck` misses first names on the roster.** Planned: ACCEPT. Every
   roster heading's first name and surname, the extra name explained, and a
   `-style lens` check on the reports.
9. **The tuna melt's optional amounts differ from its variations'.**
   Planned: REJECT. Both are v1.0's, the ticket keeps the ingredient lines
   and quantities, and choosing between two of the cook's amounts would be
   inventing one.
10. **Two definition-of-done lines point at the profile instead of giving
    commands.** Planned: ACCEPT.
11. **The editor invocation and its no-verdict paths are underspecified.**
    Planned: ACCEPT: a run that ends with no report may be started again
    once; a `Not independent:` reply, or an editor that changed the card,
    the packet, or the index, is a question.
12. **A failed editor run leaves a state the spec cannot resume from.**
    Planned: ACCEPT in part: say what the tree holds and that the revised
    spec owns it. REJECT `-2` names in `reportcheck`: a passing run of this
    spec holds one report for each card.
13. **The editor's authorship is attested, not proven, and the replies have
    no gate.** Planned: ACCEPT in part: one named reply file for each card,
    with the name and privacy checks on both. The limit stays and is said:
    no harness proves which agent wrote a file.
14. **The orchestrator's reading of the report re-judges the editor.**
    Planned: ACCEPT. The reading question goes; finding 7's rules replace
    it.
15. **The CI and rendering lines hold a placeholder and count lines, not
    tables.** Planned: ACCEPT in part.
16. **Decision 16 narrows L005 and the line-ending guard is incomplete.**
    Planned: ACCEPT.
17. **Decision 3 says the packets are not committed while this spec
    publishes their bytes.** Planned: ACCEPT: it is said plainly as an
    exception for these two scrubbed example packets.

Questions for the cook, asked on 2026-11-19:

1. The carrots' v1.0 card says the original cut dimension was not
   recovered. Leg 1's first rehearsal editor failed the card for holding
   `reviewed` with that open. Is "similar-size roasting pieces, roasted
   until browned and tender" the complete instruction (the card stays
   `reviewed`), is there a cut size to give, or is the card a `draft` with
   the gap listed?
2. `cooked-once` needs a cook log, and a log holds only the cook's own
   words. The private card keeps one line about the 2026-08-01 cook, not
   written by the cook. Will the cook report that cook now, in their own
   words, so a log can be written? If not, is the evidence `untested`, with
   the cook kept as history in the changelog, or `not-recorded`?
3. Did the cooked dill-pickle version include the lemon juice?

## File contents

Four files, each the text inside the four-backtick fence under its heading
(`### Writing a file from this spec`). The two packets go to the ignored
`.sources/` folder and are never committed (decision 3).

#### File: `.sources/butter-roasted-carrots/2026-11-19.md`

````markdown
# Source packet: Butter-Roasted Carrots with Jaggery and Sumac

- **Card:** recipes/sides/butter-roasted-carrots.md
- **Kind of save:** new card
- **Date:** 2026-11-19
- **Where the approved text came from:** the v1.0 card in my private cooking repo, with the public-release edits that ticket T012 of map W001 and spec S006 of this repository name

## Approved text

~~~~
# Butter-Roasted Carrots with Jaggery and Sumac

**Version:** v1.1 | **Date:** 2026-11-19
**Status:** reviewed (final pressure-tested proposal) | **Kitchen evidence:** untested (not yet cooked as written)
**Source:** Original. Developed with the council on 2026-09-12 and pressure-tested; not yet cooked as written.
**Yield:** 2 lb carrots; servings not recorded | **Time:** 27–33 min roast, plus prep and oven preheat

## Equipment

- Sheet pan; use two if one is crowded
- Oven at 425°F

## Ingredients

### Roast

| Amount | Ingredient | Prep |
|--------|-----------|------|
| 2 lb | Carrots | Trimmed and cut into similar-size roasting pieces |
| 2 tbsp | Olive oil | — |
| 1 tsp | Kosher salt | — |
| ½ tsp | Garlic powder | — |
| ½ tsp | Dried thyme | — |
| ¼ tsp | Wild mountain cumin | — |
| ¼ tsp | Black pepper | — |

### Finish (after roasting)

| Amount | Ingredient | Prep |
|--------|-----------|------|
| 1 tbsp | Butter | — |
| 1½ tsp | Jaggery brown sugar | — |
| ¼–½ tsp | Sumac | To taste |

### Optional Enhancements

| Amount | Ingredient | Prep |
|--------|-----------|------|
| 1 tsp | Dried Tokyo negi scallions | Finishing addition, off heat |

## Method

1. **Season** — Heat the oven to **425°F**. Toss the carrots with the oil, salt, garlic powder, thyme, cumin, and pepper.
2. **Spread** — Single layer with space between pieces. Use a second pan if crowded.
3. **Roast** — **15 minutes**, flip, then another **12–18 minutes**, until browned and tender. Size governs the time; the original cut dimension was not recovered.
4. **Finish** — Toss the hot carrots with the butter and jaggery so they melt into a light coating.
5. **Season off heat** — Add sumac to taste and the dried negi if using. Serve.

## Why This Works

- **A restrained base** — thyme and a little cumin keep the sweet-savory center clear. Owning a spice is not a reason to add it.
- **Sugar after roasting** — the jaggery never spends the full high-heat roast on the pan, so it doesn't scorch.
- **Space on the pan** — crowded carrots steam instead of browning.

## Failure Modes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Pale, soft carrots | Crowded pan | Use two pans |
| Scorched sweetness | Sugar added before roasting | Add jaggery only at the finish |
| Uneven doneness | Mixed piece sizes | Cut to similar size; pull by tenderness |
| Muddy flavor | Extra pantry spices added | Keep to the listed base |

## Variations

- None recorded.

## Storage

- Refrigerate within 2 hours; use within 3–4 days. See rows K3 and K6 of the [food-safety reference](../../.agents/skills/chef-council/references/food-safety.md).

## Notes

- Dried scallions are a finish, not an oven coating.
- **For other kitchens:** Wild mountain cumin is a specialty cumin; ordinary ground cumin works.
- **Next experiment:** record the carrot cut, tenderness, sweetness, and the cook's verdict before this moves past reviewed.

## Changelog

- v1.1 (2026-11-19) — Public-release edits, with nothing a cook would do differently: the Source line no longer names a private conversation, a notes-app field and a pointer to a card that is not published here were removed, the storage line points to this repository's food-safety reference, the note on the cumin for other kitchens was added, and the next experiment asks for the cook's verdict. Not yet cooked as written.
- v1.0 (2026-10-10) — The final 2026-09-12 proposal, written down in my private cooking repo. No cooked result was recovered.
~~~~

## Scope instruction

~~~~
From the maintainer's build ticket for the example recipes, ticket T012 of map W001 (`docs/wayfinder/W001-public-chef-council/issues/T012-example-recipes.md`):

Ship two example cards, each run through the real editor with its QC report committed:

- Butter-Roasted Carrots with Jaggery and Sumac;
- Council Tuna Melt, with its unsourced claims removed and no real person credited as author;

both as v1.1 with the public-release edits in their changelogs, plus the generated `recipes/INDEX.md`.

Status: the carrots are reviewed and not yet cooked as written; the tuna melt is cooked once (the dill-pickle variant, 2026-08-01).

From the approved build spec for that ticket, spec S006, decision 4:

Each example card is saved as a new card in this repository. Its v1.0 exists only in my private cooking repo and is not published, so the packet holds no previous version. The card starts here at v1.1, not v1.0, because the approved text is v1.0 with the public-release edits, and its changelog keeps a line for each of the two versions.

From the same spec, decision 5:

The carrots keep the status `reviewed`, which the ticket gives them. The cut size is not an open gap: the v1.0 card held `reviewed` beside the same sentence about the cut dimension, and the instruction a cook follows is complete without a dimension, which is to cut the carrots into similar-size roasting pieces, roast for the stated range, and pull them when browned and tender. What the cut was at a given cook is for the next experiment to record.
~~~~

## Previous version

None: this is a new card.

## Paths

- Card: recipes/sides/butter-roasted-carrots.md
- Previous card: none
- Cook logs: none
- Index: recipes/INDEX.md
- This packet: .sources/butter-roasted-carrots/2026-11-19.md
````

#### File: `recipes/sides/butter-roasted-carrots.md`

````markdown
---
id: butter-roasted-carrots
version: v1.1
status: reviewed
evidence: untested
category: sides
mirrors: none
---

# Butter-Roasted Carrots with Jaggery and Sumac

- **Version:** v1.1
- **Date:** 2026-11-19
- **Status:** reviewed
- **Kitchen evidence:** untested
- **Source:** Original. Developed with the council on 2026-09-12 and pressure-tested; not yet cooked as written.
- **Yield:** 2 lb carrots; servings not recorded
- **Time:** 27–33 min roast, plus prep and oven preheat

## Equipment

- Sheet pan; use two if one is crowded
- Oven at 425°F

## Ingredients

### Roast

| Amount | Ingredient | Prep |
|---|---|---|
| 2 lb | Carrots | Trimmed and cut into similar-size roasting pieces |
| 2 tbsp | Olive oil | None |
| 1 tsp | Kosher salt | None |
| ½ tsp | Garlic powder | None |
| ½ tsp | Dried thyme | None |
| ¼ tsp | Wild mountain cumin | None |
| ¼ tsp | Black pepper | None |

### Finish (after roasting)

| Amount | Ingredient | Prep |
|---|---|---|
| 1 tbsp | Butter | None |
| 1½ tsp | Jaggery brown sugar | None |
| ¼–½ tsp | Sumac | To taste |

### Optional enhancements

| Amount | Ingredient | Prep |
|---|---|---|
| 1 tsp | Dried Tokyo negi scallions | Finishing addition, off heat |

## Method

1. **Season.** Heat the oven to **425°F**. Toss the carrots with the oil, salt, garlic powder, thyme, cumin, and pepper.
2. **Spread.** Single layer with space between pieces. Use a second pan if crowded.
3. **Roast.** **15 minutes**, flip, then another **12–18 minutes**, until browned and tender. Size governs the time; the original cut dimension was not recovered.
4. **Finish.** Toss the hot carrots with the butter and jaggery so they melt into a light coating.
5. **Season off heat.** Add sumac to taste and the dried negi if using. Serve.

## Why this works

- **A restrained base.** Thyme and a little cumin keep the sweet-savory center clear. Owning a spice is not a reason to add it.
- **Sugar after roasting.** The jaggery never spends the full high-heat roast on the pan, so it doesn't scorch.
- **Space on the pan.** Crowded carrots steam instead of browning.

## Failure modes

| Problem | Likely cause | Fix |
|---|---|---|
| Pale, soft carrots | Crowded pan | Use two pans |
| Scorched sweetness | Sugar added before roasting | Add jaggery only at the finish |
| Uneven doneness | Mixed piece sizes | Cut to similar size; pull by tenderness |
| Muddy flavor | Extra pantry spices added | Keep to the listed base |

## Variations

None recorded.

## Storage

- Refrigerate within 2 hours; use within 3–4 days. See rows K3 and K6 of the [food-safety reference](../../.agents/skills/chef-council/references/food-safety.md).

## Notes

- Dried scallions are a finish, not an oven coating.
- **For other kitchens:** Wild mountain cumin is a specialty cumin; ordinary ground cumin works.

## Next experiment

Record the carrot cut, tenderness, sweetness, and the cook's verdict before this moves past reviewed.

## Changelog

- v1.1 (2026-11-19): Public-release edits, with nothing a cook would do differently: the Source line no longer names a private conversation, a notes-app field and a pointer to a card that is not published here were removed, the storage line points to this repository's food-safety reference, the note on the cumin for other kitchens was added, and the next experiment asks for the cook's verdict. Not yet cooked as written.
- v1.0 (2026-10-10): The final 2026-09-12 proposal, written down in my private cooking repo. No cooked result was recovered.
````

#### File: `.sources/council-tuna-melt/2026-11-19.md`

````markdown
# Source packet: Council Tuna Melt

- **Card:** recipes/sandwiches/council-tuna-melt.md
- **Kind of save:** new card
- **Date:** 2026-11-19
- **Where the approved text came from:** the v1.0 card in my private cooking repo, with the public-release edits that ticket T012 of map W001 and spec S006 of this repository name

## Approved text

~~~~
# Council Tuna Melt

**Version:** v1.1 | **Date:** 2026-11-19
**Status:** reviewed | **Kitchen evidence:** not-recorded (cooked once, on 2026-08-01, with the dill-pickle variation; no cook log was written)
**Source:** Original. Developed with the council; no published recipe was adapted.
**Yield:** 2 sandwiches | **Time:** 10 min prep + 10 min cook

## Equipment

- Nonstick or cast iron skillet with lid
- Medium mixing bowl
- Can opener
- Spatula

## Ingredients

### Tuna Salad

| Amount | Ingredient | Prep |
|--------|-----------|------|
| 2 (5 oz) cans | Yellowtail tuna in avocado oil | Well drained |
| 3 Tbsp | Duke's mayonnaise | — |
| 1–2 tsp | Fresh lemon juice | — |
| 1–2 Tbsp | Celery or shallot | Finely minced (see variations) |
| To taste | Kosher salt | Diamond Crystal preferred |
| To taste | Fresh black pepper | — |

### Assembly

| Amount | Ingredient | Prep |
|--------|-----------|------|
| 4 slices | Sturdy bread (sourdough, country white, or rye) | — |
| 4 slices | Swiss cheese | — |
| ~1 Tbsp | Butter or mayonnaise | For grilling the bread |

### Optional Enhancements

| Amount | Ingredient | Prep |
|--------|-----------|------|
| ¼ tsp | Lemon zest | Microplaned, stirred into mayo |
| Pinch | Smoked paprika or cayenne | Stirred into mayo |
| ½ tsp | Dijon mustard | Stirred into mayo |
| 1 Tbsp | Dill pickle or capers | Finely chopped (replaces celery/shallot) |
| Dash | Fish sauce or Worcestershire | — |

## Method

### Prep

1. **Drain the tuna thoroughly** — press the lid into the can over the sink to expel the avocado oil. You want the tuna dry enough that the mayo binds rather than floats.

2. **Season the tuna first** — in a medium bowl, break up the tuna with a fork. Add salt, pepper, and lemon juice directly to the fish and mix. *Seasoning the protein before adding mayo ensures even distribution.*

3. **Add mix-ins** — stir in minced celery (or shallot, or pickle) and any optional mayo enhancements (Dijon, zest, paprika).

4. **Bind** — fold in the Duke's mayo. Mix until just combined — overmixing turns it to paste. The salad should hold together but still have visible flakes.

### Assembly

5. **Pre-toast the bread (inside faces only)** — place bread slices under the broiler or in a dry skillet for ~30 seconds on one side. This toasted face goes INWARD against the tuna. *This is the single best defense against a soggy-bottomed melt.*

6. **Butter the outsides** — spread butter or mayo on the UN-toasted faces of each slice. Mayo grills to an exceptionally even golden crust. Butter works perfectly too — pick your fat.

7. **Layer** — bottom bread (buttered side down) → Swiss cheese → tuna salad (half the mix) → Swiss cheese → top bread (buttered side up). *Cheese on both sides cements the tuna in place so it doesn't slide out when you flip.*

### Cook

8. **Low and slow** — heat skillet over medium-low. Place sandwiches in the pan and cover with a lid. The lid traps heat to melt the Swiss through without scorching the bread. ~3–4 minutes per side.

9. **Flip when golden** — check the bottom at 3 minutes. When deeply golden and the cheese on that side is visibly melting, flip. Cover again for 3–4 minutes until the second side is golden and all cheese is fully melted.

10. **Rest 1 minute** before cutting. This lets the cheese set slightly so it doesn't all run out on the first cut.

## Why This Works

- **Acid is non-negotiable** — tuna + mayo is pure fat and protein. Lemon juice (or pickle brine, or Dijon) provides the acid that cuts through the richness. Without it, the sandwich tastes flat no matter how well you sear the bread.
- **Pre-toasting the inside faces** creates a moisture barrier — the toasted inner surface of the bread can't absorb as much liquid from the tuna salad as raw bread can, so pre-toasting the inside faces limits sogginess.
- **Cheese on both sides** isn't just about more cheese — it acts as edible glue. The melted cheese on the bottom binds to the bread and the melted cheese on top binds to the top slice, so the tuna salad is encased rather than loose.
- **Low heat + lid** — on high heat, the bread burns before the cheese melts. Covered medium-low gives the heat time to penetrate without carbonizing the crust.
- **The mayonnaise** — this recipe was developed with Duke's. With a sweeter mayo, add ½ tsp more lemon juice.

## Failure Modes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Soggy, mushy sandwich | Tuna not drained enough | Press the lid hard — get that oil out |
| | Skipped pre-toasting inner faces | 30 seconds under the broiler is all it takes |
| Tuna slides out when flipping | No cheese on both sides | Swiss on bottom AND top of the tuna layer |
| | Overstuffed | Half the mix per sandwich max |
| Bread burns, cheese unmelted | Heat too high | Medium-low, lid on, be patient |
| Bland, tastes like nothing | Forgot acid | Lemon juice is step 2 — don't skip it |
| | Forgot salt | Season the tuna directly, not just the mayo |
| Tuna salad too wet | Added the avocado oil back | Drain and discard (or reserve for another use) |

## Variations

- **Dill Pickle Melt:** Replace celery with 1 Tbsp finely chopped dill pickle + 1 tsp pickle brine (skip the lemon juice). The version that was cooked.
- **Caper-Dijon Melt:** Replace celery with 2 tsp capers (rinsed, chopped) + ½ tsp Dijon in the mayo. A brighter variation (untested).
- **Spicy Smoked Melt:** Add ¼ tsp smoked paprika + pinch cayenne to the mayo. Use sharp cheddar instead of Swiss. Serve with pickled jalapeños on the side. Untested.
- **Open-Face Broiler Version:** Skip the pan entirely. Pre-toast bread, pile tuna + Swiss on top, broil until bubbly and browned (2–3 min). Faster, lighter. Untested.

## Storage

- Tuna salad keeps refrigerated 2–3 days in an airtight container
- Do not assemble sandwiches ahead of time — the bread will sog
- Cooked tuna melts don't reheat well — make only what you'll eat

## Notes

- **Bread matters.** Soft sandwich bread disintegrates. Sourdough, rye, or a sturdy country white is essential.
- **Albacore:** If you can only find albacore, drain it even more aggressively.
- **Avocado oil:** No need to add it back to the salad. There's already plenty of fat from the mayo and cheese. Reserve the oil for another use (salad dressing, roasting vegetables) if you like.
- **What was cooked:** Only the dill-pickle variation has been cooked. The base version with celery or shallot is untested.

## Changelog

- v1.1 (2026-11-19) — Public-release edits. The Source line, a heading, a step, and two variations no longer credit named people or a publisher. A publisher's test, a cheese's melting temperature, a mayonnaise's ingredients, and a comparison of two kinds of tuna were removed because no source for them was read. The status and kitchen-evidence lines were added, the variations nobody has cooked are marked untested, and the card moved to the sandwiches category. Nothing a cook would do differently, except that the extra ½ tsp of lemon juice is now for any sweeter mayo and no longer names two brands.
- v1.0 (2026-08-01) — Initial version, from a council deliberation, in my private cooking repo. Cooked once, on 2026-08-01, with lemon juice and the dill-pickle variation; the result was recorded as excellent.
~~~~

## Scope instruction

~~~~
From the maintainer's build ticket for the example recipes, ticket T012 of map W001 (`docs/wayfinder/W001-public-chef-council/issues/T012-example-recipes.md`):

Ship two example cards, each run through the real editor with its QC report committed:

- Butter-Roasted Carrots with Jaggery and Sumac;
- Council Tuna Melt, with its unsourced claims removed and no real person credited as author;

both as v1.1 with the public-release edits in their changelogs, plus the generated `recipes/INDEX.md`.

Status: the carrots are reviewed and not yet cooked as written; the tuna melt is cooked once (the dill-pickle variant, 2026-08-01).

From the approved build spec for that ticket, spec S006, decision 4:

Each example card is saved as a new card in this repository. Its v1.0 exists only in my private cooking repo and is not published, so the packet holds no previous version. The card starts here at v1.1, not v1.0, because the approved text is v1.0 with the public-release edits, and its changelog keeps a line for each of the two versions.

From the same spec, decision 6:

The tuna melt's kitchen evidence is `not-recorded`. It was cooked once, on 2026-08-01, and no cook log of that cook was written: my private cooking repo records the result only as one line of the card's changelog. No cook log is written for it now, because a log holds the cook's own words and those were not kept.
~~~~

## Previous version

None: this is a new card.

## Paths

- Card: recipes/sandwiches/council-tuna-melt.md
- Previous card: none
- Cook logs: none
- Index: recipes/INDEX.md
- This packet: .sources/council-tuna-melt/2026-11-19.md
````

#### File: `recipes/sandwiches/council-tuna-melt.md`

````markdown
---
id: council-tuna-melt
version: v1.1
status: reviewed
evidence: not-recorded
category: sandwiches
mirrors: none
---

# Council Tuna Melt

- **Version:** v1.1
- **Date:** 2026-11-19
- **Status:** reviewed
- **Kitchen evidence:** not-recorded
- **Source:** Original. Developed with the council; no published recipe was adapted.
- **Yield:** 2 sandwiches
- **Time:** 10 min prep + 10 min cook

## Equipment

- Nonstick or cast iron skillet with lid
- Medium mixing bowl
- Can opener
- Spatula

## Ingredients

### Tuna salad

| Amount | Ingredient | Prep |
|---|---|---|
| 2 (5 oz) cans | Yellowtail tuna in avocado oil | Well drained |
| 3 Tbsp | Duke's mayonnaise | None |
| 1–2 tsp | Fresh lemon juice | None |
| 1–2 Tbsp | Celery or shallot | Finely minced (see variations) |
| To taste | Kosher salt | Diamond Crystal preferred |
| To taste | Fresh black pepper | None |

### Assembly

| Amount | Ingredient | Prep |
|---|---|---|
| 4 slices | Sturdy bread (sourdough, country white, or rye) | None |
| 4 slices | Swiss cheese | None |
| ~1 Tbsp | Butter or mayonnaise | For grilling the bread |

### Optional enhancements

| Amount | Ingredient | Prep |
|---|---|---|
| ¼ tsp | Lemon zest | Microplaned, stirred into mayo |
| Pinch | Smoked paprika or cayenne | Stirred into mayo |
| ½ tsp | Dijon mustard | Stirred into mayo |
| 1 Tbsp | Dill pickle or capers | Finely chopped (replaces celery/shallot) |
| Dash | Fish sauce or Worcestershire | None |

## Method

### Prep

1. **Drain the tuna thoroughly.** Press the lid into the can over the sink to expel the avocado oil. You want the tuna dry enough that the mayo binds rather than floats.
2. **Season the tuna first.** In a medium bowl, break up the tuna with a fork. Add salt, pepper, and lemon juice directly to the fish and mix. Seasoning the protein before adding mayo ensures even distribution.
3. **Add mix-ins.** Stir in minced celery (or shallot, or pickle) and any optional mayo enhancements (Dijon, zest, paprika).
4. **Bind.** Fold in the Duke's mayo. Mix until just combined; overmixing turns it to paste. The salad should hold together but still have visible flakes.

### Assembly

5. **Pre-toast the bread (inside faces only).** Place bread slices under the broiler or in a dry skillet for ~30 seconds on one side. This toasted face goes INWARD against the tuna. This is the single best defense against a soggy-bottomed melt.
6. **Butter the outsides.** Spread butter or mayo on the UN-toasted faces of each slice. Mayo grills to an exceptionally even golden crust. Butter works perfectly too; pick your fat.
7. **Layer.** Bottom bread (buttered side down) → Swiss cheese → tuna salad (half the mix) → Swiss cheese → top bread (buttered side up). Cheese on both sides cements the tuna in place so it doesn't slide out when you flip.

### Cook

8. **Low and slow.** Heat skillet over medium-low. Place sandwiches in the pan and cover with a lid. The lid traps heat to melt the Swiss through without scorching the bread. ~3–4 minutes per side.
9. **Flip when golden.** Check the bottom at 3 minutes. When deeply golden and the cheese on that side is visibly melting, flip. Cover again for 3–4 minutes until the second side is golden and all cheese is fully melted.
10. **Rest 1 minute.** Rest before cutting. This lets the cheese set slightly so it doesn't all run out on the first cut.

## Why this works

- **Acid is non-negotiable.** Tuna + mayo is pure fat and protein. Lemon juice (or pickle brine, or Dijon) provides the acid that cuts through the richness. Without it, the sandwich tastes flat no matter how well you sear the bread.
- **Pre-toasting the inside faces.** It creates a moisture barrier: the toasted inner surface of the bread can't absorb as much liquid from the tuna salad as raw bread can, so pre-toasting the inside faces limits sogginess.
- **Cheese on both sides.** It isn't just about more cheese; it acts as edible glue. The melted cheese on the bottom binds to the bread and the melted cheese on top binds to the top slice, so the tuna salad is encased rather than loose.
- **Low heat + lid.** On high heat, the bread burns before the cheese melts. Covered medium-low gives the heat time to penetrate without carbonizing the crust.
- **The mayonnaise.** This recipe was developed with Duke's. With a sweeter mayo, add ½ tsp more lemon juice.

## Failure modes

| Problem | Likely cause | Fix |
|---|---|---|
| Soggy, mushy sandwich | Tuna not drained enough | Press the lid hard — get that oil out |
| Soggy, mushy sandwich | Skipped pre-toasting inner faces | 30 seconds under the broiler is all it takes |
| Tuna slides out when flipping | No cheese on both sides | Swiss on bottom AND top of the tuna layer |
| Tuna slides out when flipping | Overstuffed | Half the mix per sandwich max |
| Bread burns, cheese unmelted | Heat too high | Medium-low, lid on, be patient |
| Bland, tastes like nothing | Forgot acid | Lemon juice is step 2 — don't skip it |
| Bland, tastes like nothing | Forgot salt | Season the tuna directly, not just the mayo |
| Tuna salad too wet | Added the avocado oil back | Drain and discard (or reserve for another use) |

## Variations

- **Dill Pickle Melt.** Replace celery with 1 Tbsp finely chopped dill pickle + 1 tsp pickle brine (skip the lemon juice). The version that was cooked.
- **Caper-Dijon Melt.** Replace celery with 2 tsp capers (rinsed, chopped) + ½ tsp Dijon in the mayo. A brighter variation (untested).
- **Spicy Smoked Melt.** Add ¼ tsp smoked paprika + pinch cayenne to the mayo. Use sharp cheddar instead of Swiss. Serve with pickled jalapeños on the side. Untested.
- **Open-Face Broiler Version.** Skip the pan entirely. Pre-toast bread, pile tuna + Swiss on top, broil until bubbly and browned (2–3 min). Faster, lighter. Untested.

## Storage

- Tuna salad keeps refrigerated 2–3 days in an airtight container.
- Do not assemble sandwiches ahead of time; the bread will sog.
- Cooked tuna melts don't reheat well; make only what you'll eat.

## Notes

- **Bread matters.** Soft sandwich bread disintegrates. Sourdough, rye, or a sturdy country white is essential.
- **Albacore.** If you can only find albacore, drain it even more aggressively.
- **Avocado oil.** No need to add it back to the salad. There's already plenty of fat from the mayo and cheese. Reserve the oil for another use (salad dressing, roasting vegetables) if you like.
- **What was cooked.** Only the dill-pickle variation has been cooked. The base version with celery or shallot is untested.

## Next experiment

None recorded.

## Changelog

- v1.1 (2026-11-19): Public-release edits. The Source line, a heading, a step, and two variations no longer credit named people or a publisher. A publisher's test, a cheese's melting temperature, a mayonnaise's ingredients, and a comparison of two kinds of tuna were removed because no source for them was read. The status and kitchen-evidence lines were added, the variations nobody has cooked are marked untested, and the card moved to the sandwiches category. Nothing a cook would do differently, except that the extra ½ tsp of lemon juice is now for any sweeter mayo and no longer names two brands.
- v1.0 (2026-08-01): Initial version, from a council deliberation, in my private cooking repo. Cooked once, on 2026-08-01, with lemon juice and the dill-pickle variation; the result was recorded as excellent.
````
