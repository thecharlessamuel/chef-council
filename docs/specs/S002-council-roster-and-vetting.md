---
date: 2026-11-18
id: S002
wayfinder: docs/wayfinder/W001-public-chef-council/issues/T008-council-roster-and-vetting.md
target_release: none
status: ready-to-build
base_branch: main
base_sha: d1e13fdb70c2d30109a83cb5042723b0d4c8e680
work_branch: workstream/t008-council-roster-and-vetting
pr_base: main
prior_specs:
  - docs/specs/archive/S001-scaffold.md
references:
  - docs/wayfinder/W001-public-chef-council/MAP.md
  - docs/wayfinder/W001-public-chef-council/issues/T002-named-chefs-with-guardrails.md
  - docs/wayfinder/W001-public-chef-council/issues/T005-privacy-rules.md
  - docs/wayfinder/W001-public-chef-council/issues/T006-private-repository-names.md
  - docs/learnings/L001-scaffold.md
  - .agents/spec-profile.md
cross_examined: meta/muse-wonder-full-1.0 (architect), 22 findings, 22 accepted
approved_by: autonomous
approved_at: 2026-11-18T19:33Z
pr: none
kickbacks: 0
merged: none
harvested: none
---

# Council roster and vetting: the rule, the check, fourteen records, and the roster

## Goal and definition of done

Seat the named council under decision T002. The repository gains the vetting
rule (`kitchen/council-vetting.md`), the record template
(`templates/lens-vetting-record.md`), one vetting record for each of the
fourteen names (`kitchen/vetting/<slug>.md`), the roster
(`kitchen/council.md`), and a check, `scripts/check-council.py`, that CI runs
so the roster can never seat a lens its record does not support.

The rule, the template, the check, its tests, the roster's fixed text, and the
edits to the entry files are given byte for byte under `## File contents`. The
fourteen records and the roster's lens entries are not: they are research that
must be done in the executing session, because a record may cite only pages
read in the session that wrote it, with that day's date (profile, real-people
constraint). For those this spec fixes the shape, the fixed lines, the
procedure, and the gates.

Done means all of the following, each observed on the work branch's head
commit after the last task, from the repository root, in a shell prepared as
`## Build plan — agent loop` says:

1. **Fourteen records.** `ls kitchen/vetting/` prints exactly the fourteen
   file names `<slug>.md` for the slugs of decision 4, and nothing else.
2. **The check passes.** `python3 scripts/check-council.py; echo $?` prints
   one line of the form `council checked: <S> seated, 14 records`, with `<S>`
   between 0 and 14, and then `0`.
3. **The roster seats exactly the seated records, in order.** `lenscheck`
   with no arguments prints one line beginning `lens check ok:` and ending
   `; <S> seated` with the same `<S>` as item 2. (The check of item 2 proves
   the roster seats exactly the records whose verdict is `seat` or `seat
   narrower`; `lenscheck` proves the entries are in decision 4's order and
   the roster's fixed text is unchanged.)
4. **The fixed lines hold, and nothing claims approval.** With `TODAY`
   unset, `lenscheck` followed by the fourteen slugs in decision 4's order
   prints one `lens check ok:` line naming all fourteen. (Each record task
   ran it with `TODAY` set, which also ties the dates to the day of the
   task.) And `grep -n '"' kitchen/vetting/*.md kitchen/council.md` prints
   nothing.
5. **Every citation was verified, and the evidence is kept.** Each record
   task's `verifycheck` printed its `verification ok:` line. The pull
   request's Evidence section holds, for each of the seven record tasks, the
   verifier's report verbatim (the content of that task's `$VERIFY`) in a
   collapsed `<details>` block, with the `verification ok:` line and the two
   verdicts above it. The orchestrator copies each `$VERIFY` to a file
   outside the repository as soon as its task's gate passes, so a lost shell
   does not lose it; a report that is lost before the pull request is opened
   is produced again by a new fresh verifier.
6. **Tests.** `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo
   $?` prints `0` and `tail -1 "$OUT"` prints `OK`; `grep -c '^test_.* ok$'
   "$OUT"` prints `88` (the 26 tests of the base and the 62 of Task 1).
7. **The other checks.** `python3 scripts/check-skills.py` prints `skills
   checked: 0`; `scripts/secret-scan.sh` exits 0; the Wayfinder lint, the
   three diff checks, and the full privacy sweep pass as the profile's ship
   tail requires.
8. **Links.** `linkcheck AGENTS.md kitchen/README.md kitchen/council.md
   kitchen/council-vetting.md templates/lens-vetting-record.md
   kitchen/vetting/*.md; echo $?` prints `0` and nothing else.
9. **CI.** `gh pr checks <PR>` reports every check passed, and the log of the
   `tests` job shows the step `Check the council roster against the vetting
   records` printing the same `council checked:` line as item 2.
10. **Rendered and read.** For `kitchen/council.md`,
    `kitchen/council-vetting.md`, `templates/lens-vetting-record.md`, and the
    first and the last record in decision 4's order whose verdict seats a
    lens, render the file from the pushed branch with the profile's
    observation command and look at the result. It passes when every heading
    renders as a heading, every list as a list, no raw Markdown markup is
    visible in the body below the front matter, each lens entry's heading in
    the roster is a link, and each cited URL in a record is a link. How
    GitHub displays the front matter is not judged (L001). When one lens is
    seated its record is rendered once, and when none is, the two record
    renders are skipped and the pull request says so.
11. **A fresh clone agrees.** In a fresh clone of the pushed branch in a new
    temporary directory, `git rev-parse HEAD` equals the pull request's head
    commit and `python3 scripts/check-council.py` prints the line of item 2.

## Decisions

Decisions T002, T005, and T006 bind this spec; the profile's
`## Pipeline constraints` apply to every file, every commit message, and the
pull request.

1. **Where things live.** `kitchen/council-vetting.md` holds the rule and no
   records. Each record is its own file, `kitchen/vetting/<slug>.md`, so an
   agent loads only the records of the lenses it consults, a cook removes a
   lens by removing one file, and no two tasks edit the same record. The
   roster is `kitchen/council.md`. The design report's tree
   (`private-sources/design/design-report.md` §6) put the rule file in
   `kitchen/` and the template in `templates/`; both are kept. Its "empty
   rule file, archetype default" recommendation is overridden by T002.
2. **A record's shape** is the template under `## File contents`: front matter
   with exactly the keys `lens`, `name`, `seat`, `job`, `question`, `verdict`,
   `scope`, `checked`, in that order; a title line `# <lens>`; then exactly
   the sections Official site, Published work, Independent sources, What the
   published work shows, Where this lens can mislead, Verdict, and Access
   notes. It is the private template
   (`private-sources/home-design/templates/vetting-record.md`) with the seat
   made a job, the "reasoning style" line made the `question` field, a
   "where this lens can mislead" section added (T002), and "replace with"
   dropped from the verdicts (the ticket lists seat, seat narrower, cut).
   The check reads the front matter itself, line by line, as `key: value`
   text; no YAML reader is involved. The value rules only keep out the forms
   L001 warns about: each value starts with a letter or digit, holds no
   double quote, no colon followed by a space, and no space followed by `#`,
   and is never a YAML boolean or null word. `checked` is a date by design.
   No claim is made about how any YAML reader types the other values.
3. **The check** is `scripts/check-council.py` (Python 3 standard library),
   run as `python3 scripts/check-council.py [repository-root]`; the root
   defaults to the script's own repository. Its behavior is exactly the file
   under `## File contents`, and its messages are the literals in
   `tests/test_check_council.py`. In words:
   - More than one argument prints `usage: check-council.py
     [repository-root]` on standard error and exits 2.
   - Every file in `kitchen/vetting/` whose name does not start with a dot is
     a record; a missing folder is no records. A name that is not `<slug>.md`
     with a lowercase, hyphenated slug is a problem.
   - A record is checked for: the front matter of decision 2; `lens` ending
     `-style lens`; `seat` being `core` or `specialist`; `question` ending in
     a question mark; `verdict` being `seat`, `seat narrower`, or `cut`;
     `scope` being `none` exactly when the verdict is `cut`; `checked` being
     a real date; the title line `# <lens>` as the only text before the
     first section; the seven sections, each non-empty; in the three cited
     sections, nothing but list items and their indented continuation lines,
     starting with an item; exactly one Official site item; every cited item
     holding an `https://` link and `(checked YYYY-MM-DD)`, except an
     Official site item that starts `No official site` and, in a cut record
     only, an item that starts `None found`, which need only the date; no
     link cited twice in one record; and, for a seated record, at least two
     Published work items, at least one Independent sources item (two when
     there is no official site), and three to five numbered tendencies with
     nothing else beside them. A record or roster that is not readable UTF-8
     text is a problem, not a crash.
   - No line of a record or of the roster may hold a double quotation mark
     (straight or curly) or start with `>`. This is how "never invent a
     quote" is made checkable: titles are set in italics, and nothing is
     quoted at all.
   - The roster must exist and hold the headings `## Core lenses` and
     `## On-demand specialists` in that order. Under them, every `###`
     heading must be a lens entry `### [<Name>-style lens](vetting/<slug>.md)`
     followed by exactly four top-level list items, in this order, that
     begin `- **Job:**`, `- **Typical question:**`, `- **Scope:**`, and
     `- **Where it can mislead:**`, each with its text on the same line.
     Nothing else may follow a lens heading but blank lines and indented
     continuation lines, and a `###` heading anywhere else in the roster is
     a problem, so a lens cannot be listed outside the two groups.
   - Roster against records: an entry needs a record; a cut record must not
     be seated; a record whose verdict seats it must have an entry; the entry
     sits under the heading that matches the record's `seat`; and the entry's
     lens name, Job, Typical question, and Scope equal the record's `lens`,
     `job`, `question`, and `scope` exactly. A record with problems of its
     own is not compared with the roster. Two records may not share a `lens`.
   - Problems print one per line as `<path>: <problem>`, sorted by path, with
     exit 1. No problem prints `council checked: <S> seated, <R> records` and
     exits 0.

   The check does not open any URL, does not judge whether a tendency is
   true, does not compare titles or tendencies for near-duplicates, and does
   not read `kitchen/council-vetting.md`. Those are the
   citation verification's job (`### Citation verification`).
4. **The fourteen lenses: fixed lines.** The slug, `lens`, `name`, `seat`,
   `job`, and `question` of every record are fixed here, and so is the
   default scope a full seat carries. The lens name follows the profile's
   form, the name and then `-style lens`: the given name alone where the
   published work itself goes by it (Kenji, Maangchi), the publisher's name
   for America's Test Kitchen, and the full name otherwise. The jobs and
   questions are the seats' (design report §5, reworded); the eight
   specialists' are one per cuisine or subject. This table is the order of
   the roster. The `lenscheck` helper carries the same values and is the
   authority if a character here differs.

   | # | slug | `lens` | `name` | `seat` | `job` | `question` | default `scope` |
   |---|---|---|---|---|---|---|---|
   | 1 | `kenji-lopez-alt` | Kenji-style lens | J. Kenji López-Alt | core | Heat, ingredient function, and which variables matter | Which variables actually change the result? | Savory cooking technique and troubleshooting in a home kitchen |
   | 2 | `americas-test-kitchen` | America's Test Kitchen-style lens | America's Test Kitchen / Dan Souza | core | Reliability, repeatability, and failure prevention | Where will a home cook most likely fail? | Any home recipe that has to work the first time |
   | 3 | `heston-blumenthal` | Heston Blumenthal-style lens | Heston Blumenthal | core | Aroma, texture, and the finishing touch | Which one change most improves eating it? | Flavor, aroma, and texture improvements a home cook can add in one optional step |
   | 4 | `stella-parks` | Stella Parks-style lens | Stella Parks | core | Baking formulas, sugar, fat, and leavening | Does the formula work structurally? | Baking and dessert formulas |
   | 5 | `claire-saffitz` | Claire Saffitz-style lens | Claire Saffitz | core | Baking workflow, dough handling, and doneness cues | Is the method clear and practical for a home baker? | Pastry, doughs, cakes, and dessert assembly |
   | 6 | `sohla-el-waylly` | Sohla El-Waylly-style lens | Sohla El-Waylly | core | Substitutions, leftovers, and pantry cooking | How do we make what is here work coherently? | Adapting a recipe to the pantry, substitutions, and leftovers |
   | 7 | `rick-martinez` | Rick Martinez-style lens | Rick Martinez | specialist | Regional Mexican cooking | Which regional version of this dish are we making, and is the adaptation defensible? | Mexican dishes |
   | 8 | `madhur-jaffrey` | Madhur Jaffrey-style lens | Madhur Jaffrey | specialist | Indian home cooking and spice layering | Are the spices added in an order and form that builds the flavor this dish needs? | Indian dishes |
   | 9 | `fuchsia-dunlop` | Fuchsia Dunlop-style lens | Fuchsia Dunlop | specialist | Chinese regional cooking and wok technique | Does the technique fit the regional dish this claims to be? | Chinese dishes |
   | 10 | `samin-nosrat` | Samin Nosrat-style lens | Samin Nosrat | specialist | Balance of salt, fat, acid, and heat | What is missing from the balance? | Seasoning and balance in any dish |
   | 11 | `jacques-pepin` | Jacques Pépin-style lens | Jacques Pépin | specialist | Classical French technique and knife work | Is the basic technique sound before anything is added? | French technique and basic knife work |
   | 12 | `yotam-ottolenghi` | Yotam Ottolenghi-style lens | Yotam Ottolenghi | specialist | Vegetable-forward cooking with bold flavor | What gives this dish contrast and a strong flavor of its own? | Vegetable and grain dishes with Mediterranean and Middle Eastern flavors |
   | 13 | `maangchi` | Maangchi-style lens | Maangchi | specialist | Korean home cooking | Would this be recognized as the Korean dish it is named for? | Korean dishes |
   | 14 | `marcella-hazan` | Marcella Hazan-style lens | Marcella Hazan | specialist | Italian home cooking and restraint | What can be taken out so the main ingredient is clear? | Italian dishes |

5. **The verdict is decided by the evidence, by this rule.** A tendency is
   supported when a page cited in the record, opened and read, says something
   the tendency restates; the independent verifier is the judge of that
   (`### Citation verification`). The parts of each default scope are:

   | slug | parts of the default scope |
   |---|---|
   | `kenji-lopez-alt` | savory cooking technique; troubleshooting |
   | `americas-test-kitchen` | recipes that work the first time (one part) |
   | `heston-blumenthal` | flavor; aroma; texture |
   | `stella-parks` | baking and dessert formulas (one part) |
   | `claire-saffitz` | pastry and doughs; cakes; dessert assembly |
   | `sohla-el-waylly` | adapting to the pantry; substitutions; leftovers |
   | `jacques-pepin` | French technique; basic knife work |
   | `yotam-ottolenghi` | vegetable dishes; grain dishes; Mediterranean and Middle Eastern flavors |
   | the other six | the whole default scope is one part |

   - `cut` when, after the search steps of `### Writing a record` with their
     minimum searches, any of these is true: fewer than two published works
     relevant to the job have a page that was opened and read; no
     independent source was opened and read (two are needed when there is no
     official site); fewer than three supported tendencies can be written;
     or no supported tendency is about the fixed `job`. `scope` is `none`,
     the Verdict section gives which of these reasons applies, and the
     roster gets no entry. A cut is a valid outcome of a task, not a
     failure, and it is not a question for the human.
   - `seat` when the record is not a cut and every part of the default scope
     has at least one supported tendency about it. `scope` is the default
     scope, character for character.
   - `seat narrower` otherwise. `scope` is one line, written by the worker,
     that names only the parts the supported tendencies are about, and the
     Verdict section says what the lens may not argue.

   The Verdict section of a seated record ends with one line of the form
   `Parts covered: <part> (tendency <n>); <part> (tendencies <n> and <n>).`
   naming every part the scope keeps. The job and the question are never
   reworded by the executor. If the published work points to a different
   job, the record is cut or seated narrower under this rule, and the pull
   request's Evidence section says so.
6. **America's Test Kitchen / Dan Souza is one record about a publisher.**
   Its tendencies describe the publisher's published work (the magazine, the
   books, the recipe site, the television programs). Dan Souza is named in
   the `name` line because T002 names him; the body says what he publishes
   there only if a page read in the session states it, and otherwise the
   access notes say his role was not confirmed. The record describes no
   company history, ownership, or staffing.
7. **Marcella Hazan.** The Official site section is exactly `- No official
   site (checked <TODAY>).`, the record rests on her books and on two or more
   independent sources, and the access notes say there is no official site
   (ticket T008). The record says nothing of her life or death. If the
   worker's search finds a site that presents itself as her official site,
   the worker stops and the orchestrator reports ``Question: a site
   presenting itself as Marcella Hazan's official site was found, which
   ticket T008 and S002 say does not exist; cite it or keep the fixed
   line?``
8. **An official site that exists but could not be opened**, after two
   attempts with the page-fetch tool, is recorded as `- No official site
   could be read (checked <TODAY>).` The access notes then hold one line of
   the form `Official site not read: <address>`, with the address written
   without `https://` so it is not a citation, and the record needs two
   independent sources. The verifier tries the address too.
9. **Independent** is about who wrote the cited content: someone other than
   the person, the person's own site or company, and the publisher of the
   work the source is cited about. A publisher's description reprinted by a
   bookseller, a library catalog, or any other site is not independent. For
   America's Test Kitchen it means not written or published by America's
   Test Kitchen or its magazines. A review, a profile of the work in a
   publication the person does not write for in that piece, and an award
   body's own listing are independent.
10. **Nothing is carried from the private chef profiles but names, roles, and
    domains** (ticket T008), and those are already in decision 4. No worker,
    verifier, or orchestrator opens anything under `private-sources/` for
    this spec. In particular no "weaknesses" line is carried over in any
    form: each "where this lens can mislead" text is written fresh from the
    record's own tendencies and is about the lens, never the person.
11. **The roster's fixed text** (everything outside the lens entries) is the
    `kitchen/council.md` block under `## File contents`. It carries T002's
    plain no-affiliation statement, the attribution rule, "standards, not
    lenses, for numbers", and named disagreement with stated dissent (design
    report §5.1). A lens entry is exactly this shape, with one blank line
    before the heading and one after it, appended as the last entry under its
    group heading:

    ```markdown
    ### [Kenji-style lens](vetting/kenji-lopez-alt.md)

    - **Job:** <the record's job>
    - **Typical question:** <the record's question>
    - **Scope:** <the record's scope>
    - **Where it can mislead:** <one sentence, on one line, summarizing the record's section of that name>
    ```

    The file never has two blank lines in a row and ends with the last
    line's line feed, with no blank line after it. So an entry added under
    `## Core lenses` goes after the last line of that group's text or of its
    last entry, with exactly one blank line before its heading and exactly
    one blank line between its last item and `## On-demand specialists`; an
    entry added under `## On-demand specialists` goes at the end of the
    file after exactly one blank line. Entries appear in decision 4's
    order; each record task appends its entries, so the order holds without
    sorting. The fixed text names no lens, so a cut leaves no trace in it. A cut record has no entry
    and is not mentioned in the roster.
12. **`AGENTS.md`, `kitchen/README.md`, CI, and the profile.** `AGENTS.md`
    gains a read-order line for the roster, two sentences on the lens rule
    (argue only from the record; vet a proposed name first), and the check in
    its list of checks; it stays under 8 KB (6,725 bytes). `kitchen/README.md`
    gains a short section pointing at the roster and the rule. The CI `tests`
    job gains one step that runs the check; the job's name, which is the
    check name on a pull request, does not change. The profile's list of CI
    commands gains the check, as the profile requires of the spec that adds
    one. The skill index line in `AGENTS.md` is not touched (no skill is
    added here).
13. **Dates and who read the page.** Each record task fixes `TODAY` once, in
    UTC, when it starts. Every `(checked ...)` and the `checked:` field in
    that task's two records is `TODAY`. If the UTC date changes before the
    task's gate has passed, or the attempt is retried on a later day, a new
    `TODAY` is set and every cited page is opened again. A worker that
    changes a record it did not write (a retry by a new worker) opens every
    citation the record keeps before it writes, because a record cites only
    pages read by the session that wrote it.
14. **`README.md`, the reading list, and the behavior checks are not touched**
    (ticket T014), and neither is any skill (T009).

## Prerequisites

- Leg 2 starts from this spec's approval commit on
  `workstream/t008-council-roster-and-vetting`, which already holds the claim
  commit for T008. Staging, the per-task commit with its `Spec-Task: S002/<N>`
  trailer, the push, the pull request, and the base-drift check are the
  `2-spec-execute` skill's standing procedure and the profile's ship tail. A
  task's commit holds exactly that task's Touches.
- The executor's machine is Linux x86_64 with Git, Bash, Python 3, GNU
  coreutils, and an authenticated `gh`. `git config user.email` ends in
  `@users.noreply.github.com` (profile).
- Tasks 4 to 10 need a web search tool and a page-fetch tool in the worker
  subagent and in the verifier subagent. If the harness offers neither,
  report ``Question: this session has no web search or page-fetch tool, which
  Tasks 4 to 10 of `docs/specs/S002-council-roster-and-vetting.md` need;
  provide one?`` and stop. Using those tools to read public pages is this
  spec's requirement, not a provider call.
- No one opens anything under `private-sources/` for this spec (decision 10).
- `test -x "$(git rev-parse --git-common-dir)/info/privacy-sweep"` succeeds,
  and the wayfinder skill's `scripts/lint.py` is found in the directory the
  harness prints when that skill loads (profile). If either is missing,
  report ``Question: <the privacy sweep | the Wayfinder lint> that the
  profile requires is not on this machine; provide it?`` and stop.
- GitHub Actions is enabled for the repository (measured 2026-11-18: enabled,
  all actions allowed).

### Writing a file from this spec

Each file under `## File contents` is the text inside the fenced block that
follows its `#### File:` heading: every line between the opening and closing
fence, each ended by a line feed, with nothing added or removed. This helper
writes one such file exactly, and the executor may use it:

```bash
extract() {
  mkdir -p "$(dirname "$1")"
  python3 - docs/specs/S002-council-roster-and-vetting.md "$1" > "$1" <<'PY'
import sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index("#### File: `%s`" % sys.argv[2])
opening = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("````"))
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "````")
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
}
```

Usage: `extract kitchen/council.md`. The SHA-256 gates decide whether a file
is right, whichever way it was written.

### Link check

A gate helper, not a repository file. It reads the Markdown files named on its
command line, skips fenced code blocks, and requires the target of every
inline link `[text](target)` with a relative target to be a path git tracks or
has staged. It prints one line per broken link and returns 1, or prints
nothing and returns 0.

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

### Lens check

A gate helper, not a repository file. `lenscheck <slug>...` checks, for each
named record: lines 1 to 6 against decision 4; exactly one title line
`# <lens>`; every `(checked ...)` equal to the record's `checked:` field,
and that field equal to `TODAY` when `TODAY` is set; a full seat carrying
the default scope and a narrower seat a different one; and no line holding
`approv`, `endors`, `contribut`, or `weakness` in any case, outside a link
and outside an italic title (a source's own address or title is never
reworded). Then, with or without arguments, it checks the roster: no such
word from `## Core lenses` on, no two blank lines in a row and none at the
end, the text outside the lens entries unchanged from the block under
`## File contents`, and the entries being exactly the seated records in
decision 4's order. It prints one line per problem and returns 1, or prints
`lens check ok: <slugs>; <S> seated` and returns 0. A banned word in prose is
fixed by rewording (for example `writes for` instead of a word built on
`contribut`), never by an exemption. The word list is a net for T002's
rule, not the rule: the verifier reads for the meaning.

````bash
lenscheck() {
  TODAY="${TODAY:-}" python3 - "$@" <<'PY'
import hashlib, os, re, sys
SKELETON = "6fd7a185d8ba1715bbbda52da98526d999aae936df3baef7ad6f1fb058f0871d"
LENSES = [
    ("kenji-lopez-alt", "Kenji-style lens", "J. Kenji López-Alt", "core",
     "Heat, ingredient function, and which variables matter",
     "Which variables actually change the result?",
     "Savory cooking technique and troubleshooting in a home kitchen"),
    ("americas-test-kitchen", "America's Test Kitchen-style lens", "America's Test Kitchen / Dan Souza", "core",
     "Reliability, repeatability, and failure prevention",
     "Where will a home cook most likely fail?",
     "Any home recipe that has to work the first time"),
    ("heston-blumenthal", "Heston Blumenthal-style lens", "Heston Blumenthal", "core",
     "Aroma, texture, and the finishing touch",
     "Which one change most improves eating it?",
     "Flavor, aroma, and texture improvements a home cook can add in one optional step"),
    ("stella-parks", "Stella Parks-style lens", "Stella Parks", "core",
     "Baking formulas, sugar, fat, and leavening",
     "Does the formula work structurally?",
     "Baking and dessert formulas"),
    ("claire-saffitz", "Claire Saffitz-style lens", "Claire Saffitz", "core",
     "Baking workflow, dough handling, and doneness cues",
     "Is the method clear and practical for a home baker?",
     "Pastry, doughs, cakes, and dessert assembly"),
    ("sohla-el-waylly", "Sohla El-Waylly-style lens", "Sohla El-Waylly", "core",
     "Substitutions, leftovers, and pantry cooking",
     "How do we make what is here work coherently?",
     "Adapting a recipe to the pantry, substitutions, and leftovers"),
    ("rick-martinez", "Rick Martinez-style lens", "Rick Martinez", "specialist",
     "Regional Mexican cooking",
     "Which regional version of this dish are we making, and is the adaptation defensible?",
     "Mexican dishes"),
    ("madhur-jaffrey", "Madhur Jaffrey-style lens", "Madhur Jaffrey", "specialist",
     "Indian home cooking and spice layering",
     "Are the spices added in an order and form that builds the flavor this dish needs?",
     "Indian dishes"),
    ("fuchsia-dunlop", "Fuchsia Dunlop-style lens", "Fuchsia Dunlop", "specialist",
     "Chinese regional cooking and wok technique",
     "Does the technique fit the regional dish this claims to be?",
     "Chinese dishes"),
    ("samin-nosrat", "Samin Nosrat-style lens", "Samin Nosrat", "specialist",
     "Balance of salt, fat, acid, and heat",
     "What is missing from the balance?",
     "Seasoning and balance in any dish"),
    ("jacques-pepin", "Jacques Pépin-style lens", "Jacques Pépin", "specialist",
     "Classical French technique and knife work",
     "Is the basic technique sound before anything is added?",
     "French technique and basic knife work"),
    ("yotam-ottolenghi", "Yotam Ottolenghi-style lens", "Yotam Ottolenghi", "specialist",
     "Vegetable-forward cooking with bold flavor",
     "What gives this dish contrast and a strong flavor of its own?",
     "Vegetable and grain dishes with Mediterranean and Middle Eastern flavors"),
    ("maangchi", "Maangchi-style lens", "Maangchi", "specialist",
     "Korean home cooking",
     "Would this be recognized as the Korean dish it is named for?",
     "Korean dishes"),
    ("marcella-hazan", "Marcella Hazan-style lens", "Marcella Hazan", "specialist",
     "Italian home cooking and restraint",
     "What can be taken out so the main ingredient is clear?",
     "Italian dishes"),
]
BANNED = re.compile(r"approv|endors|contribut|weakness", re.I)
def banned(line):
    """True when a banned word stands outside a link and outside an italic title."""
    return BANNED.search(re.sub(r"https://\S+|\*[^*]+\*", " ", line)) is not None
today = os.environ.get("TODAY", "")
bad = 0
def fail(text):
    global bad
    bad = 1
    print(text)
by_slug = {row[0]: row for row in LENSES}
for slug in sys.argv[1:]:
    path = "kitchen/vetting/%s.md" % slug
    if slug not in by_slug or not os.path.isfile(path):
        fail("%s: no such lens or record" % slug)
        continue
    _, lens, name, seat, job, question, scope = by_slug[slug]
    lines = open(path, encoding="utf-8").read().split("\n")
    fixed = ["---", "lens: " + lens, "name: " + name, "seat: " + seat,
             "job: " + job, "question: " + question]
    if lines[:6] != fixed:
        fail("%s: front matter lines 1 to 6 differ from the lens table" % slug)
    if lines.count("# " + lens) != 1:
        fail("%s: needs exactly one title line: # %s" % (slug, lens))
    checked = [l[9:] for l in lines[6:10] if l.startswith("checked: ")]
    if today and checked != [today]:
        fail("%s: checked is not TODAY (%s)" % (slug, today))
    verdicts = [l for l in lines[6:10] if l.startswith("verdict: ")]
    if verdicts == ["verdict: seat"] and "scope: " + scope not in lines[6:10]:
        fail("%s: a full seat carries the default scope from the lens table" % slug)
    if verdicts == ["verdict: seat narrower"] and "scope: " + scope in lines[6:10]:
        fail("%s: a narrower seat needs a scope narrower than the default" % slug)
    dates = set(re.findall(r"\(checked (\d{4}-\d{2}-\d{2})\)", "\n".join(lines)))
    if dates != set(checked):
        fail("%s: a citation's date differs from the record's checked date" % slug)
    for number, line in enumerate(lines, 1):
        if banned(line):
            fail("%s: line %d uses a banned word" % (slug, number))
roster = open("kitchen/council.md", encoding="utf-8").read().split("\n")
start = roster.index("## Core lenses")
for number, line in enumerate(roster[start:], start + 1):
    if banned(line):
        fail("kitchen/council.md: line %d uses a banned word" % number)
kept = []
skipping = False
for line in roster:
    if line.startswith("### ["):
        skipping = True
    elif line.startswith("#"):
        skipping = False
    if not skipping:
        kept.append(line)
skeleton = "\n".join(kept).rstrip("\n") + "\n"
if hashlib.sha256(skeleton.encode("utf-8")).hexdigest() != SKELETON:
    fail("kitchen/council.md: the text outside the lens entries has changed")
expected = []
for row in LENSES:
    path = "kitchen/vetting/%s.md" % row[0]
    if os.path.isfile(path) and re.search(
            r"^verdict: seat( narrower)?$", open(path, encoding="utf-8").read(), re.M):
        expected.append(row[0])
actual = [m.group(1) for m in (re.match(r"### \[.*\]\(vetting/(.*)\.md\)$", l) for l in roster) if m]
if any(a == "" and b == "" for a, b in zip(roster, roster[1:])) or roster[-2:-1] == [""]:
    fail("kitchen/council.md: two blank lines in a row, or a blank line at the end")
if actual != expected:
    fail("kitchen/council.md: seats %s, expected %s" % (actual, expected))
if not bad:
    print("lens check ok: %s; %d seated" % (" ".join(sys.argv[1:]), len(actual)))
sys.exit(bad)
PY
}
````

### Writing a record

This is the whole instruction for the worker of one record. Each record has
its own fresh worker subagent, so one name's pages are never in the context
that researches the next. The worker is given this section, decisions 4 to
11 and 13, the task, the slug, `TODAY`, and the files
`kitchen/council-vetting.md`, `templates/lens-vetting-record.md`, and
`kitchen/council.md`. It does the following, in order:

1. **Find the official site.** Run at least one search for it and open it
   with the page-fetch tool. Read the page that describes the person's or
   publisher's work. Decisions 7 and 8 cover a missing or unreadable site.
2. **Find published work relevant to the job.** Start from the leads below.
   For each lead, run at least one search and open a page about that work:
   the person's own page for it, else its publisher's page. A lead is only a
   lead; it was not read by this spec's author, and a lead that no opened
   page confirms is not cited. Another work found on the official site may
   be used instead. Stop at four works.
3. **Find independent sources** (decision 9): a review, a profile of the
   work, or an award body's listing. Run at least two different searches and
   open each candidate. Stop at three sources.
4. **Write three to five tendencies**, each a plain statement in your own
   words of how the published work approaches cooking, each supported by
   something an opened page says. Attach no citation to a tendency; the
   verifier matches tendencies to pages. Write nothing from memory that no
   opened page supports.
5. **Decide the verdict** by decision 5, and write the record at
   `kitchen/vetting/<slug>.md` from the template: lines 1 to 6 from decision
   4, the title line `# <lens>`, and the sections, with nothing else before
   the first section. Each cited item is one list item of the form `- *Title
   or site name* (publisher, year where known): <URL> (checked <TODAY>).
   <One sentence on what it is and why it is relevant.>`, with a space after
   the URL and each URL cited once. Cite a URL only if it was opened with
   the page-fetch tool by this worker and its content was read; a page that
   would not load, a paywall with no content, and anything seen only in
   search results go in Access notes, described in words without a link.
   Access notes also list every search run, one per line, as `Searched:
   <query>`. The Verdict section ends with the `Parts covered:` line of
   decision 5 when the lens is seated.
6. **Write "Where this lens can mislead"** in two to four sentences: where
   advice argued from the listed tendencies goes wrong for a home cook, and
   what to check when it does. It follows from the tendencies and is about
   the lens.
7. **When the verdict seats the lens, append its roster entry** exactly as
   decision 11 says, under `## Core lenses` or `## On-demand specialists`.
   Change nothing else in `kitchen/council.md`.

Rules for every line the worker writes: no quotation and no double quotation
mark, with titles in italics; nothing about personal life (family, health,
home, relationships, religion, politics, money, or biography beyond what was
published and where); no statement that anyone approved, reviewed, endorsed,
or took part in this repository; no judgment of the person; no recipe text
from any publisher (no ingredient list, method, or headnote); no temperature,
ratio, or other number offered as guidance; and long lines left unwrapped, as
the repository's other Markdown is.

Leads, by slug (titles only, unverified):

| slug | leads |
|---|---|
| `kenji-lopez-alt` | *The Food Lab*; *The Wok*; his column at Serious Eats |
| `americas-test-kitchen` | *Cook's Illustrated* magazine; the America's Test Kitchen recipe site and television program; its test-kitchen cookbooks |
| `heston-blumenthal` | *The Fat Duck Cookbook*; *Heston Blumenthal at Home*; *In Search of Perfection* |
| `stella-parks` | *BraveTart*; her baking column at Serious Eats |
| `claire-saffitz` | *Dessert Person*; *What's for Dessert* |
| `sohla-el-waylly` | *Start Here*; her recipe columns and video series |
| `rick-martinez` | *Mi Cocina*; his recipe columns and video series |
| `madhur-jaffrey` | *An Invitation to Indian Cooking*; *Madhur Jaffrey's Indian Cooking* |
| `fuchsia-dunlop` | *The Food of Sichuan*; *Every Grain of Rice* |
| `samin-nosrat` | *Salt, Fat, Acid, Heat* (the book and the series) |
| `jacques-pepin` | *Jacques Pépin's New Complete Techniques*; *Essential Pépin* |
| `yotam-ottolenghi` | *Plenty*; *Ottolenghi Simple*; *Jerusalem* |
| `maangchi` | *Maangchi's Real Korean Cooking*; *Maangchi's Big Book of Korean Cooking*; her recipe site |
| `marcella-hazan` | *Essentials of Classic Italian Cooking*; *The Classic Italian Cook Book* |

### Citation verification

The gate for the research. After both workers of a record task have
finished, the orchestrator starts a fresh subagent that wrote neither record
(the verifier), with a web search tool and a page-fetch tool, briefed with
exactly: this section, decisions 4 to 11 and 13, the rules paragraph of
`### Writing a record` (the one beginning `Rules for every line`), the paths
of the task's two records, and `kitchen/council.md`. The verifier writes
nothing in the repository and returns only lines of the forms below, with no
other text, which the orchestrator saves to `$VERIFY`.

1. For every distinct `https://` URL in the two records, open it with the
   page-fetch tool. Print `ok <url>` when the page loads and its content is
   about the work, site, or source the item says it is. Otherwise print
   `fail <url> <reason>`: it did not load, it showed a login or paywall with
   no content, or it is about something else.
2. For every item under Independent sources, print `independent <url>
   <who wrote or published the content>` when it is independent under
   decision 9, naming what on the page shows it, or `fail <url> not
   independent`.
3. For every numbered tendency, print `supported <slug> <n> <url>` naming
   one of the record's cited pages whose content supports it, or
   `unsupported <slug> <n>`.
4. For a record whose Official site item starts `No official site could be
   read`, try `https://` followed by the address in its access notes. Print
   `unreadable <slug> confirmed` when it does not load, or `fail <slug>
   official site loads`.
5. For a record whose verdict is `cut` or `seat narrower`, run at least two
   searches of your own for evidence the worker missed (a published work, an
   independent source, or a page about a part of the scope the record drops)
   and print one `searched <slug> <query>` line for each. If a search finds
   such evidence, print `fail <slug> verdict <what was found and where>`.
6. For each record, print `verdict <slug> agrees` when the verdict follows
   decision 5 from what the pages support and the `Parts covered:` line of a
   seated record matches the supported tendencies, or `fail <slug> verdict
   <reason>`.
7. For each record and its roster entry, read every line and print `clean
   <slug>` when none of these is present: a quotation or words presented as
   the person's own; a statement that anyone approved, reviewed, endorsed, or
   took part in this repository; personal life; a judgment of the person
   rather than of the lens; recipe text; a number offered as guidance; or
   anything decisions 6 and 7 exclude. Otherwise print `fail <slug>
   <which>`.

The verification passes when `verifycheck "$VERIFY" <slug-a> <slug-b>; echo
$?` prints one line beginning `verification ok:` and then `0`. The helper
fails on any `fail` or `unsupported` line and on any line that is not one of
the forms above, and it requires: an `ok` line for exactly the records'
URLs; an `independent` line for exactly the URLs under Independent sources;
a `supported` line for exactly each tendency of each seated record, naming a
URL that record cites; `verdict ... agrees` and `clean` for exactly the two
slugs; two `searched` lines for each record that is not a full seat; and an
`unreadable` line for exactly the records of step 4.

````bash
verifycheck() {
  python3 - "$@" <<'PY'
import re, sys
report, slugs = sys.argv[1], sys.argv[2:]
FORMS = [
    r"ok (https://\S+)",
    r"independent (https://\S+) \S.*",
    r"supported (\S+) (\d+) (https://\S+)",
    r"verdict (\S+) agrees",
    r"clean (\S+)",
    r"searched (\S+) \S.*",
    r"unreadable (\S+) confirmed",
]
bad = 0
def fail(text):
    global bad
    bad = 1
    print(text)
seen = {form: [] for form in FORMS}
for number, line in enumerate(open(report, encoding="utf-8").read().split("\n"), 1):
    if not line.strip():
        continue
    if re.match(r"(fail|unsupported) ", line):
        fail("line %d: %s" % (number, line))
        continue
    for form in FORMS:
        match = re.fullmatch(form, line)
        if match:
            seen[form].append(match.groups())
            break
    else:
        fail("line %d: not one of the verifier's line forms" % number)
def same(label, found, wanted):
    if sorted(found) != sorted(wanted):
        fail("%s: the report has %s, the records need %s" % (label, sorted(found), sorted(wanted)))
urls, independent, tendencies, searches, unreadable = [], [], [], [], []
for slug in slugs:
    text = open("kitchen/vetting/%s.md" % slug, encoding="utf-8").read()
    record_urls = sorted(set(re.findall(r"https://\S+", text)))
    urls += [(url,) for url in record_urls]
    section = text.split("\n## Independent sources\n")[1].split("\n## ")[0]
    independent += [(url,) for url in sorted(set(re.findall(r"https://\S+", section)))]
    verdict = re.search(r"^verdict: (.*)$", text, re.M).group(1)
    if verdict != "cut":
        shown = text.split("\n## What the published work shows\n")[1].split("\n## ")[0]
        count = len(re.findall(r"^\d+\. \S", shown, re.M))
        tendencies += [(slug, str(n)) for n in range(1, count + 1)]
        for found_slug, n, url in seen[FORMS[2]]:
            if found_slug == slug and url not in record_urls:
                fail("supported %s %s names a link that is not in the record" % (slug, n))
    if verdict != "seat" and len([s for s in seen[FORMS[5]] if s[0] == slug]) < 2:
        fail("%s: a %s needs two searched lines from the verifier" % (slug, verdict))
    if "\n- No official site could be read" in text:
        unreadable.append((slug,))
same("ok lines", seen[FORMS[0]], urls)
same("independent lines", [(g[0],) for g in seen[FORMS[1]]], independent)
same("supported lines", [(g[0], g[1]) for g in seen[FORMS[2]]], tendencies)
same("verdict lines", seen[FORMS[3]], [(slug,) for slug in slugs])
same("clean lines", seen[FORMS[4]], [(slug,) for slug in slugs])
same("unreadable lines", seen[FORMS[6]], unreadable)
if not bad:
    print("verification ok: %s; %d links" % (" ".join(slugs), len(urls)))
sys.exit(bad)
PY
}
````

On a failure the task attempt has failed. The record is fixed from the
`fail` and `unsupported` lines by replacing a citation, moving it to Access
notes, rewording or dropping a tendency, or changing the verdict under
decision 5 (decision 13 says what a new worker must reopen), and a new fresh
verifier runs on the result. A verifier is never asked to re-check its own
earlier output.

### The record task

Each of Tasks 4 to 10 vets two names. Its Work, Touches, and Gate are the
following (called the shared work and the shared gate in the build plan),
with `<slug-a>` and `<slug-b>` the task's two slugs in order and `<R>` the
task's record count (2 for Task 4, then 4, 6, 8, 10, 12, and 14 for Task
10).

- **Work:** Set `TODAY=$(date -u +%F)`. A fresh worker subagent follows
  `### Writing a record` for `<slug-a>`; when it has finished, a second
  fresh worker does the same for `<slug-b>`. Each writes its record and,
  when its verdict seats the lens, appends the entry to `kitchen/council.md`.
  Then the orchestrator runs `### Citation verification` on the pair.
- **Touches:** `kitchen/vetting/<slug-a>.md`, `kitchen/vetting/<slug-b>.md`,
  `kitchen/council.md`
- **Gate:**
  - `python3 scripts/check-council.py; echo $?` prints `council checked: <S>
    seated, <R> records`, for some `<S>` no greater than `<R>`, then `0`.
  - `TODAY="$TODAY" lenscheck <slug-a> <slug-b>; echo $?` prints `lens check
    ok: <slug-a> <slug-b>; <S> seated` with the same `<S>`, then `0`.
  - `git status --porcelain --untracked-files=all` lists only the task's
    Touches (the roster is absent from the list when both records are
    cuts).
  - The citation verification passes: `verifycheck "$VERIFY" <slug-a>
    <slug-b>; echo $?` prints its `verification ok:` line, then `0`.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
    kitchen/vetting/<slug-a>.md kitchen/vetting/<slug-b>.md
    kitchen/council.md` ends with a line beginning `privacy sweep: clean` and
    exits 0.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0` and `tail -1 "$OUT"` prints `OK`.
  - After `git add` of the Touches, `linkcheck kitchen/council.md; echo $?`
    prints `0` and nothing else.
  - The tests are unchanged (the block in `## Build plan — agent loop`).
- **Nature:** copy

## Build plan — agent loop

Run every command from the repository root, in one Bash shell per task in
which the setup has been run first: `OUT=$(mktemp)` and `VERIFY=$(mktemp)`
(temporary files outside the repository) and the `extract`, `linkcheck`,
`lenscheck`, and `verifycheck` function definitions above, pasted as
written. A gate passes only when every command in it prints what is stated.
Where a gate ends in `; echo $?`, the printed status is part of the expected
output. A gate's commands run in the order listed, on the finished work
before it is committed; nothing is staged until a line says `after git add`,
and from that line on the task's Touches are staged. The commit follows the
last line, and the one check that runs after the commit is the second half
of the tests-unchanged block below.

Baseline, measured by leg 1 on 2026-11-18 in a scratch clone at `base_sha`:
`python3 -m unittest discover -s tests -v` ends `OK` with 26 tests;
`python3 scripts/check-skills.py` prints `skills checked: 0`;
`scripts/secret-scan.sh` exits 0 with `no leaks found`. Every other gate
below names a file this spec creates or changes, so it is red on the base by
design; none measures old debt. Leg 1 also built Tasks 1 to 3 in that clone
from this spec with `extract`, ran their gates, and ran the check,
`lenscheck`, and `verifycheck` against placeholder records, entries in the
shape of decision 11, and a placeholder verifier report.

Every task's gate ends with this block, called "the tests are unchanged" in
Tasks 2 to 10. Before the commit, `git status --porcelain -- tests/` prints
nothing. After it, this prints only `tests unchanged`:

```bash
TASK1_SHA=$(git log --format=%H -1 --grep='^Spec-Task: S002/1$')
[ -n "$TASK1_SHA" ] && git merge-base --is-ancestor "$TASK1_SHA" HEAD &&
  [ -z "$(git diff --name-only "$TASK1_SHA..HEAD" -- tests/)" ] &&
  echo "tests unchanged"
```

A task that seems to need a test changed is reported as ``Question: Task <N>
of `docs/specs/S002-council-roster-and-vetting.md` needs a test the tests
task wrote changed; revise the spec?``

### Task 1 — Add the tests for the council check
- **Work:** Create `tests/test_check_council.py` with exactly the content
  given under its `#### File:` heading. The seam under test is one command,
  `python3 scripts/check-council.py [repository-root]` (decision 3), observed
  only through standard output, standard error, and exit status. Each test
  builds a repository root in a temporary directory from literal fixture text
  and expects literal lines. The tests catch: an empty council, a seated
  record, a mix of core, specialist, and cut records, a record with no
  official site, and this repository all pass; each malformed-record case of
  decision 3 fails with its literal line (file name, front matter, each
  field rule, the title line, sections, cited items, a repeated link,
  counts, quotation marks, a file that is not UTF-8 text); the shipped
  template copied unfilled is not a seated record; each roster case fails
  with its literal line (missing roster, headings, entry heading, a lens
  seated twice, a lens heading outside the groups, text inside an entry,
  entry items, no record, a cut record seated, wrong group,
  each field differing, a seated record missing, a shared lens name,
  quotation marks); problems print in path order; and an extra argument is a
  usage error.
- **Touches:** `tests/test_check_council.py`
- **Gate:**
  - `sha256sum tests/test_check_council.py` prints
    `eef38de2c7a6fbbde23927f2da133ca4899db9e6bf7f321ba092e46dbbe6c305  tests/test_check_council.py`.
  - With the working tree differing from `base_sha` only under `docs/` and in
    this test file, `python3 -m unittest discover -s tests -v > "$OUT" 2>&1;
    echo $?` prints `1`, and `tail -1 "$OUT"` prints `FAILED (failures=61,
    errors=1)`. This is the recorded red: leg 1 measured it on 2026-11-18 in
    a scratch clone at `base_sha` with only this test file applied. All 62
    methods of `CheckCouncilTest` are red because the script does not exist,
    and the 26 tests of the base pass. 61 fail by assertion. One,
    `test_unfilled_template_is_not_a_seated_record`, is an error: a
    `FileNotFoundError` opening `templates/lens-vetting-record.md`, which
    Task 2 creates. None is an import error. `grep -cE '^test_.*
    \(test_check_council\..*\) \.\.\. (FAIL|ERROR)$' "$OUT"` prints `62`.
- **Nature:** mechanical

### Task 2 — Add the council check, the vetting rule, and the empty roster
- **Work:** Create `scripts/check-council.py`, `kitchen/council-vetting.md`,
  `kitchen/council.md`, and `templates/lens-vetting-record.md` with exactly
  the content given under their `#### File:` headings. The script is not
  made executable (it is run with `python3`, like `scripts/check-skills.py`).
  The roster is the fixed text with no lens entry yet. Do not create
  `kitchen/vetting/`.
- **Touches:** `scripts/check-council.py`, `kitchen/council-vetting.md`,
  `kitchen/council.md`, `templates/lens-vetting-record.md`
- **Gate:**
  - This prints four lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    a89e87ef5cc181f01a4c234fecd66dac78bb6c8b98235558a432d491194313ad  scripts/check-council.py
    12b4707a82c627ed5cf927323c274db46ce9715af0e0e8bb9bc08bd597593bb8  kitchen/council-vetting.md
    6fd7a185d8ba1715bbbda52da98526d999aae936df3baef7ad6f1fb058f0871d  kitchen/council.md
    79e5452171227da113f46c49a28f36e64cd357d5ea8930e2d2327182e1296677  templates/lens-vetting-record.md
    SUMS
    ```

  - After `git add scripts/check-council.py`, `git ls-files -s
    scripts/check-council.py` prints a line beginning `100644`.
  - `python3 scripts/check-council.py; echo $?` prints `council checked: 0
    seated, 0 records` then `0`.
  - `lenscheck; echo $?` prints `lens check ok: ; 0 seated` then `0`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0` and `tail -1 "$OUT"` prints `OK`.
  - The tests are unchanged.
- **Nature:** mechanical

### Task 3 — Point the entry files, CI, and the profile at the council check
- **Work:** Replace `AGENTS.md`, `kitchen/README.md`, and
  `.github/workflows/ci.yml` with exactly the content given under their
  `#### File:` headings. In `.agents/spec-profile.md`, replace the one line

  ```text
      0), `python3 -m unittest discover -s tests -v` (its last line is `OK`), and
  ```

  with these three lines (each starts with four spaces), and change nothing
  else in that file:

  ```text
      0), `python3 scripts/check-council.py` (prints `council checked: <S>
      seated, <R> records` and exits 0), `python3 -m unittest discover -s tests
      -v` (its last line is `OK`), and
  ```

- **Touches:** `AGENTS.md`, `kitchen/README.md`, `.github/workflows/ci.yml`,
  `.agents/spec-profile.md`
- **Gate:**
  - This prints four lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    967664ba66d859a4cde15c328463650c3b537da1e5bf93ddf070bc7a3a4caf20  AGENTS.md
    3e8a85ed2e9989bfefe04ba7435886726f86c6244f57e3ddf668b314d4f0df91  kitchen/README.md
    700c04977af29261a6b185c42d61c1f5f4eab13940a71dd331e29457f1e3221b  .github/workflows/ci.yml
    de28afc0685bf73926d80f14bd8dcab22b602aef69e11330026ddeb3ce5eadc4  .agents/spec-profile.md
    SUMS
    ```

  - `git diff --numstat HEAD -- .agents/spec-profile.md` prints one line:
    `3`, `1`, and `.agents/spec-profile.md`, separated by tabs.
  - `wc -c < AGENTS.md` prints `6725`.
  - After `git add` of the four files, `linkcheck AGENTS.md kitchen/README.md
    kitchen/council.md kitchen/council-vetting.md
    templates/lens-vetting-record.md; echo $?` prints `0` and nothing else.
  - `python3 scripts/check-skills.py; echo $?` prints `skills checked: 0`
    then `0`, and `python3 scripts/check-council.py; echo $?` prints `council
    checked: 0 seated, 0 records` then `0`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0` and `tail -1 "$OUT"` prints `OK`.
  - The tests are unchanged.
- **Nature:** mechanical

### Task 4 — Vet the Kenji-style and America's Test Kitchen-style lenses
- **Work:** The shared work, with `<slug-a>` = `kenji-lopez-alt`, `<slug-b>`
  = `americas-test-kitchen`, and `<R>` = 2. Decision 6 applies.
- **Touches:** `kitchen/vetting/kenji-lopez-alt.md`,
  `kitchen/vetting/americas-test-kitchen.md`, `kitchen/council.md`
- **Gate:** The shared gate.
- **Nature:** copy

### Task 5 — Vet the Heston Blumenthal-style and Stella Parks-style lenses
- **Work:** The shared work, with `<slug-a>` = `heston-blumenthal`,
  `<slug-b>` = `stella-parks`, and `<R>` = 4.
- **Touches:** `kitchen/vetting/heston-blumenthal.md`,
  `kitchen/vetting/stella-parks.md`, `kitchen/council.md`
- **Gate:** The shared gate.
- **Nature:** copy

### Task 6 — Vet the Claire Saffitz-style and Sohla El-Waylly-style lenses
- **Work:** The shared work, with `<slug-a>` = `claire-saffitz`, `<slug-b>` =
  `sohla-el-waylly`, and `<R>` = 6.
- **Touches:** `kitchen/vetting/claire-saffitz.md`,
  `kitchen/vetting/sohla-el-waylly.md`, `kitchen/council.md`
- **Gate:** The shared gate.
- **Nature:** copy

### Task 7 — Vet the Rick Martinez-style and Madhur Jaffrey-style lenses
- **Work:** The shared work, with `<slug-a>` = `rick-martinez`, `<slug-b>` =
  `madhur-jaffrey`, and `<R>` = 8.
- **Touches:** `kitchen/vetting/rick-martinez.md`,
  `kitchen/vetting/madhur-jaffrey.md`, `kitchen/council.md`
- **Gate:** The shared gate.
- **Nature:** copy

### Task 8 — Vet the Fuchsia Dunlop-style and Samin Nosrat-style lenses
- **Work:** The shared work, with `<slug-a>` = `fuchsia-dunlop`, `<slug-b>` =
  `samin-nosrat`, and `<R>` = 10.
- **Touches:** `kitchen/vetting/fuchsia-dunlop.md`,
  `kitchen/vetting/samin-nosrat.md`, `kitchen/council.md`
- **Gate:** The shared gate.
- **Nature:** copy

### Task 9 — Vet the Jacques Pépin-style and Yotam Ottolenghi-style lenses
- **Work:** The shared work, with `<slug-a>` = `jacques-pepin`, `<slug-b>` =
  `yotam-ottolenghi`, and `<R>` = 12.
- **Touches:** `kitchen/vetting/jacques-pepin.md`,
  `kitchen/vetting/yotam-ottolenghi.md`, `kitchen/council.md`
- **Gate:** The shared gate.
- **Nature:** copy

### Task 10 — Vet the Maangchi-style and Marcella Hazan-style lenses
- **Work:** The shared work, with `<slug-a>` = `maangchi`, `<slug-b>` =
  `marcella-hazan`, and `<R>` = 14. Decision 7 applies.
- **Touches:** `kitchen/vetting/maangchi.md`,
  `kitchen/vetting/marcella-hazan.md`, `kitchen/council.md`
- **Gate:** The shared gate, and then, with the Touches still staged,
  definition-of-done items 1, 2, 3, 4, 6, and 8, which need no push.
- **Nature:** copy

## Repo profile

`.agents/spec-profile.md` applies as written. Additions for this spec only:

- The pull request's Evidence section lists, for each record, its verdict
  and, for a `seat narrower` or `cut`, the reason in one line; and for each
  record task the verifier's report as definition-of-done item 5 says. It
  quotes no record text beyond that.
- The pull request's Merge Danger section says that the records characterize
  real people's published work and become public when the repository does,
  and that reverting the merge removes them.
- The cross-examination dossier holds this spec, `AGENTS.md`, the profile,
  and the files of the touch set that exist on the base (`kitchen/README.md`,
  `.github/workflows/ci.yml`); every new file is already in the spec.

## Cross-examination

Blind review by `meta/muse-wonder-full-1.0` (architect tier, reasoning effort
high, Muse Code 1.4.15, read-only, sandboxed to the dossier) on 2026-11-18.
The dossier held the draft spec, `AGENTS.md`, the profile,
`kitchen/README.md`, and `.github/workflows/ci.yml`, and passed the privacy
sweep's `--text` and a gitleaks scan before it was sent. 22 findings; every
one was accepted, six of them in part, with the rejected remainder stated.
After the edits leg 1 rebuilt Tasks 1 to 3 from this text in a fresh clone
at `base_sha`, re-ran their gates, and re-measured the red.

1. **ACCEPT.** The verification's pass conditions only counted lines. The
   `verifycheck` helper now requires exact sets (URLs, tendencies, slugs)
   and rejects any line outside the verifier's forms.
2. **ACCEPT.** The verifier is now briefed with decisions 4 to 11 and 13 and
   the writing rules, has a search tool, and runs two searches of its own
   for every `cut` and `seat narrower`.
3. **ACCEPT in part.** Decision 5 now lists the parts of each default scope,
   `### Writing a record` sets minimum searches, and a seated record's
   Verdict section ends with a `Parts covered:` line. Rejected: a mechanical
   test of whether a page supports a tendency. That is a reading judgment,
   and the spec assigns it to an independent verifier instead of pretending
   a command can make it.
4. **ACCEPT.** The check now requires the title line and nothing else before
   the first section, only numbered items among a seated record's
   tendencies, nothing but the four items after a lens heading, and no `###`
   heading outside the two groups, each with a test.
5. **ACCEPT in part.** A link cited twice in one record is now a problem,
   and the fixture that duplicated a source was replaced. Rejected:
   normalized-title and near-duplicate-tendency matching in the check; the
   verifier reads for that, and decision 3 says the check does not.
6. **ACCEPT.** A continuation line before the first item of a cited section
   is now a problem, with a test.
7. **ACCEPT.** Fixed by finding 4's change: text inside an entry fails the
   check, so the skeleton comparison cannot hide it.
8. **ACCEPT.** Decision 11 now states the blank-line rule exactly, and
   `lenscheck` rejects two blank lines in a row and a blank line at the end.
9. **ACCEPT.** The roster's fixed text no longer names any lens.
10. **ACCEPT.** `lenscheck` now compares citation dates with the record's own
    `checked` field, so definition-of-done item 4 re-runs it for all
    fourteen at the end, and item 5 keeps every verifier report verbatim in
    the pull request.
11. **ACCEPT.** Item 10 says what is rendered when one lens or none is
    seated.
12. **ACCEPT in part.** Each record now has its own fresh worker. Rejected:
    fourteen separate tasks. The pair stays the unit of commit and of
    verification, which bounds the orchestrator's context instead.
13. **ACCEPT.** Decision 13 now covers a date change mid-task and a worker
    changing a record it did not write.
14. **ACCEPT.** The banned-word net skips links and italic titles, and the
    spec says the verifier, not the word list, is the rule.
15. **ACCEPT.** Decision 7 gains a `Question:` for a site presenting itself
    as official; decision 8 gains two fetch attempts, a fixed access-notes
    line, and a verifier step that tries the address.
16. **ACCEPT.** Decision 9 defines independence by who wrote the content and
    excludes reprinted publisher descriptions; the verifier names what shows
    it on an `independent` line.
17. **ACCEPT in part.** The roster's link check now runs in every record
    task's gate. Rejected: titled links and worktree-existence checks. No
    file in the touch set uses a link title, the check runs on staged work,
    and external links are the citation verification's job, as the link
    check's description says.
18. **ACCEPT.** The shipped rule now says to set `scope: none` when cutting
    and to reopen the links and update every date when changing a record.
19. **ACCEPT.** A record or roster that cannot be read as UTF-8 text is now a
    problem line, with tests for a directory and for invalid bytes.
20. **ACCEPT in part.** Prerequisites now require the privacy sweep and the
    Wayfinder lint to be present, with a `Question:` if not. Rejected: a
    prerequisite for `2-spec-execute` itself, which is the leg reading this
    spec.
21. **ACCEPT.** The build plan now states the order: gate commands in listed
    order before the commit, staging where a line says so, and one check
    after the commit.
22. **ACCEPT.** Decision 2 no longer claims the values are YAML-proof; it
    says the check reads them as text and which forms the rules keep out.

## File contents

Each block is one file, written as `### Writing a file from this spec` says.

#### File: `tests/test_check_council.py`

````python
"""Tests for scripts/check-council.py, observed through its output and exit status."""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "check-council.py")

ROSTER_HEAD = "# The council\n\nA test roster.\n"

FIELDS = {
    "lens": "Example-style lens",
    "name": "Example Cook",
    "seat": "core",
    "job": "Heat and ingredient function",
    "question": "Which variable changes the result?",
    "verdict": "seat",
    "scope": "Savory technique at home",
    "checked": "2026-11-18",
}
KEYS = ["lens", "name", "seat", "job", "question", "verdict", "scope", "checked"]

SITE = "- Example site: https://example.com/ (checked 2026-11-18). The author's own site.\n"
WORK = (
    "- *First Book* (Example Press, 2015): https://example.com/first (checked 2026-11-18). Technique.\n"
    "- *Second Book* (Example Press, 2022): https://example.com/second (checked 2026-11-18).\n"
    "  A continuation line.\n"
)
SOURCES = "- *A review*: https://example.org/review (checked 2026-11-18). Confirms the method.\n"
SECOND_SOURCE = "- *A profile*: https://example.net/profile (checked 2026-11-18). Describes the books.\n"
SHOWS = "1. Tests one variable at a time.\n2. Explains why a step works.\n3. Writes for home equipment.\n"
MISLEAD = "It can add steps a weeknight cook does not need.\n"
VERDICT = "Seat. The published work covers the job.\n"
NOTES = "Nothing was behind a paywall.\n"

SECTIONS = [
    "Official site",
    "Published work",
    "Independent sources",
    "What the published work shows",
    "Where this lens can mislead",
    "Verdict",
    "Access notes",
]
SECTION_LIST = ", ".join(SECTIONS)


def run(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        check=False,
    )


def record(front=None, **changes):
    """Build a record. Field names change the front matter; section names
    (with spaces as underscores) replace a section's text."""
    fields = dict(FIELDS)
    bodies = {
        "Official site": SITE,
        "Published work": WORK,
        "Independent sources": SOURCES,
        "What the published work shows": SHOWS,
        "Where this lens can mislead": MISLEAD,
        "Verdict": VERDICT,
        "Access notes": NOTES,
    }
    for key, value in changes.items():
        if key in fields:
            fields[key] = value
        else:
            bodies[key.replace("_", " ")] = value
    if front is None:
        front = "".join("%s: %s\n" % (key, fields[key]) for key in KEYS)
    text = "---\n%s---\n\n# %s\n" % (front, fields["lens"])
    for name in SECTIONS:
        text += "\n## %s\n\n%s" % (name, bodies[name])
    return text


def entry(slug="example", **changes):
    values = dict(FIELDS, mislead="It can add steps.")
    values.update(changes)
    return (
        "\n### [%(lens)s](vetting/" % values + slug + ".md)\n\n"
        "- **Job:** %(job)s\n"
        "- **Typical question:** %(question)s\n"
        "- **Scope:** %(scope)s\n"
        "- **Where it can mislead:** %(mislead)s\n" % values
    )


def roster(core="", specialists=""):
    return (
        ROSTER_HEAD
        + "\n## Core lenses\n" + core
        + "\n## On-demand specialists\n" + specialists
    )


class CheckCouncilTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name
        self.write("kitchen/council.md", roster(core=entry()))

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def check(self, expected_lines, expected_status):
        result = run(self.root)
        self.assertEqual(result.stdout.splitlines(), expected_lines)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, expected_status)

    def check_record(self, text, *problems):
        """Write the one seated record and expect exactly these problems."""
        self.write("kitchen/vetting/example.md", text)
        if problems:
            self.check(["kitchen/vetting/example.md: %s" % p for p in problems], 1)
        else:
            self.check(["council checked: 1 seated, 1 records"], 0)

    def check_roster(self, text, *problems):
        """Write the roster beside one good record and expect these problems."""
        self.write("kitchen/vetting/example.md", record())
        self.write("kitchen/council.md", text)
        self.check(["kitchen/council.md: %s" % p for p in problems], 1)

    # The passing shapes.

    def test_empty_council_passes(self):
        self.write("kitchen/council.md", roster())
        self.check(["council checked: 0 seated, 0 records"], 0)

    def test_seated_record_passes(self):
        self.check_record(record())

    def test_core_specialist_and_cut_records_pass(self):
        self.write("kitchen/vetting/example.md", record())
        self.write(
            "kitchen/vetting/second-cook.md",
            record(
                lens="Second Cook-style lens",
                seat="specialist",
                verdict="seat narrower",
                scope="Regional home cooking",
            ),
        )
        self.write(
            "kitchen/vetting/third-cook.md",
            record(
                lens="Third Cook-style lens",
                verdict="cut",
                scope="none",
                Published_work="- None found (checked 2026-11-18).\n",
                Independent_sources="- None found (checked 2026-11-18).\n",
                What_the_published_work_shows="Not established.\n",
            ),
        )
        self.write(
            "kitchen/council.md",
            roster(
                core=entry(),
                specialists=entry(
                    "second-cook",
                    lens="Second Cook-style lens",
                    scope="Regional home cooking",
                ),
            ),
        )
        self.check(["council checked: 2 seated, 3 records"], 0)

    def test_no_official_site_passes_with_two_independent_sources(self):
        self.check_record(
            record(
                Official_site="- No official site (checked 2026-11-18).\n",
                Independent_sources=SOURCES + SECOND_SOURCE,
            )
        )

    def test_dot_files_in_the_records_folder_are_ignored(self):
        self.write("kitchen/vetting/.gitkeep", "")
        self.check_record(record())

    def test_this_repository_passes(self):
        result = run()
        self.assertEqual(result.stderr, "")
        self.assertRegex(result.stdout, r"\Acouncil checked: \d+ seated, \d+ records\n\Z")
        self.assertEqual(result.returncode, 0)

    # A malformed record.

    def test_bad_file_name_fails(self):
        self.write("kitchen/vetting/example.md", record())
        self.write("kitchen/vetting/Example_Two.md", record())
        self.check(
            [
                "kitchen/vetting/Example_Two.md: file name is not <slug>.md "
                "with a lowercase, hyphenated slug"
            ],
            1,
        )

    def test_missing_front_matter_fails(self):
        self.check_record("# Example-style lens\n", "front matter is missing")

    def test_unclosed_front_matter_fails(self):
        self.check_record("---\nlens: Example-style lens\n", "front matter is missing")

    def test_front_matter_line_without_a_value_fails(self):
        front = "".join("%s: %s\n" % (key, FIELDS[key]) for key in KEYS)
        self.check_record(
            record(front=front.replace("job: Heat and ingredient function\n", "job:\n")),
            "front matter line 5 is not key: value",
        )

    def test_front_matter_keys_out_of_order_fail(self):
        front = "".join("%s: %s\n" % (key, FIELDS[key]) for key in reversed(KEYS))
        self.check_record(
            record(front=front),
            "front matter keys must be exactly: lens, name, seat, job, question, "
            "verdict, scope, checked",
        )

    def test_missing_front_matter_key_fails(self):
        front = "".join("%s: %s\n" % (key, FIELDS[key]) for key in KEYS[:-1])
        self.check_record(
            record(front=front),
            "front matter keys must be exactly: lens, name, seat, job, question, "
            "verdict, scope, checked",
        )

    def test_value_yaml_reads_as_a_boolean_fails(self):
        self.check_record(
            record(scope="No"), "scope must not be a YAML boolean or null word"
        )

    def test_value_with_colon_space_fails(self):
        self.check_record(
            record(job="Heat: and ingredient function"),
            "job must start with a letter or digit and hold no double quote, "
            "colon-space, or space-hash",
        )

    def test_value_starting_with_a_symbol_fails(self):
        self.check_record(
            record(name="*Example Cook*"),
            "name must start with a letter or digit and hold no double quote, "
            "colon-space, or space-hash",
        )

    def test_lens_without_the_suffix_fails(self):
        self.check_record(record(lens="Example Cook"), "lens must end with -style lens")

    def test_unknown_seat_fails(self):
        self.check_record(record(seat="guest"), "seat must be core or specialist")

    def test_unknown_verdict_fails(self):
        self.check_record(
            record(verdict="replace"), "verdict must be seat, seat narrower, or cut"
        )

    def test_question_without_a_question_mark_fails(self):
        self.check_record(
            record(question="Which variable changes the result"),
            "question must end with a question mark",
        )

    def test_seated_record_with_scope_none_fails(self):
        self.check_record(
            record(scope="none"), "scope must not be none unless the verdict is cut"
        )

    def test_cut_record_with_a_scope_fails(self):
        self.write("kitchen/council.md", roster())
        self.write("kitchen/vetting/example.md", record(verdict="cut"))
        self.check(
            ["kitchen/vetting/example.md: scope must be none when the verdict is cut"], 1
        )

    def test_impossible_date_fails(self):
        self.check_record(
            record(checked="2026-02-30"), "checked must be a date written YYYY-MM-DD"
        )

    def test_missing_section_fails(self):
        text = record().replace("\n## Verdict\n\n" + VERDICT, "")
        self.check_record(text, "sections must be exactly, in order: " + SECTION_LIST)

    def test_extra_section_fails(self):
        self.check_record(
            record() + "\n## Weaknesses\n\nNone.\n",
            "sections must be exactly, in order: " + SECTION_LIST,
        )

    def test_empty_section_fails(self):
        self.check_record(record(Access_notes="\n"), "section Access notes is empty")

    def test_prose_in_a_cited_section_fails(self):
        self.check_record(
            record(Published_work=WORK + "\nAlso well known for a third book.\n"),
            "Published work: every line must be a list item or its indented continuation",
        )

    def test_two_official_sites_fail(self):
        self.check_record(
            record(Official_site=SITE + SITE.replace("example.com/", "example.com/about")),
            "Official site: expected one list item, found 2",
        )

    def test_continuation_before_the_first_item_fails(self):
        self.check_record(
            record(Published_work="  Also a third book, uncited.\n" + WORK),
            "Published work: every line must be a list item or its indented continuation",
        )

    def test_repeated_link_fails(self):
        self.check_record(
            record(Independent_sources=SOURCES + SOURCES),
            "Independent sources: item 2 repeats a link already cited in this record",
        )

    def test_missing_title_fails(self):
        self.check_record(
            record().replace("# Example-style lens\n", ""),
            "the text before the first section must be the title line # <lens> "
            "and nothing else",
        )

    def test_text_beside_the_title_fails(self):
        self.check_record(
            record().replace(
                "# Example-style lens\n", "# Example-style lens\n\nA famous cook.\n"
            ),
            "the text before the first section must be the title line # <lens> "
            "and nothing else",
        )

    def test_prose_beside_the_tendencies_fails(self):
        self.check_record(
            record(What_the_published_work_shows=SHOWS + "\nAlso widely admired.\n"),
            "What the published work shows: a seated lens lists numbered items "
            "and nothing else",
        )

    def test_record_that_is_not_text_fails(self):
        os.makedirs(os.path.join(self.root, "kitchen", "vetting", "example.md"))
        self.check(["kitchen/vetting/example.md: cannot be read as UTF-8 text"], 1)

    def test_record_that_is_not_utf8_fails(self):
        self.write("kitchen/vetting/example.md", record())
        with open(os.path.join(self.root, "kitchen", "vetting", "example.md"), "wb") as handle:
            handle.write(b"---\nlens: \xff\n")
        self.check(["kitchen/vetting/example.md: cannot be read as UTF-8 text"], 1)

    def test_citation_without_a_link_fails(self):
        self.check_record(
            record(Independent_sources="- *A review* (checked 2026-11-18).\n"),
            "Independent sources: item 1 needs an https:// link and (checked YYYY-MM-DD)",
        )

    def test_citation_without_a_date_fails(self):
        self.check_record(
            record(Published_work=WORK + "- *Third Book*: https://example.com/third\n"),
            "Published work: item 3 needs an https:// link and (checked YYYY-MM-DD)",
        )

    def test_no_official_site_without_a_date_fails(self):
        self.check_record(
            record(
                Official_site="- No official site.\n",
                Independent_sources=SOURCES + SECOND_SOURCE,
            ),
            "Official site: item 1 needs (checked YYYY-MM-DD)",
        )

    def test_no_official_site_needs_two_independent_sources(self):
        self.check_record(
            record(Official_site="- No official site (checked 2026-11-18).\n"),
            "Independent sources: a seated lens needs at least 2 items, found 1",
        )

    def test_one_published_work_fails(self):
        self.check_record(
            record(Published_work=WORK.split("\n")[0] + "\n"),
            "Published work: a seated lens needs at least 2 items, found 1",
        )

    def test_none_found_does_not_seat_a_lens(self):
        self.check_record(
            record(Independent_sources="- None found (checked 2026-11-18).\n"),
            "Independent sources: item 1 needs an https:// link and (checked YYYY-MM-DD)",
        )

    def test_two_tendencies_fail(self):
        self.check_record(
            record(What_the_published_work_shows="1. One.\n2. Two.\n"),
            "What the published work shows: a seated lens needs 3 to 5 numbered "
            "items, found 2",
        )

    def test_six_tendencies_fail(self):
        shows = "".join("%d. Tendency.\n" % n for n in range(1, 7))
        self.check_record(
            record(What_the_published_work_shows=shows),
            "What the published work shows: a seated lens needs 3 to 5 numbered "
            "items, found 6",
        )

    def test_quotation_marks_and_blockquotes_fail(self):
        text = record(
            Where_this_lens_can_mislead='It says "always".\n> A quoted line.\n“Curly.”\n'
        )
        first = text.split("\n").index('It says "always".') + 1
        self.check_record(
            text,
            *[
                "line %d: double quotation marks and blockquotes are not allowed" % n
                for n in (first, first + 1, first + 2)
            ]
        )

    def test_unfilled_template_is_not_a_seated_record(self):
        self.write("kitchen/council.md", roster())
        with open(
            os.path.join(REPO, "templates", "lens-vetting-record.md"), encoding="utf-8"
        ) as handle:
            self.write("kitchen/vetting/new-lens.md", handle.read())
        result = run(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "kitchen/vetting/new-lens.md: verdict must be seat, seat narrower, or cut",
            result.stdout.splitlines(),
        )

    # The roster.

    def test_missing_roster_fails(self):
        os.remove(os.path.join(self.root, "kitchen", "council.md"))
        self.check(["kitchen/council.md: file is missing"], 1)

    def test_roster_without_both_headings_fails(self):
        self.write("kitchen/council.md", ROSTER_HEAD + "\n## Core lenses\n")
        self.check(
            [
                "kitchen/council.md: needs the headings ## Core lenses and "
                "## On-demand specialists, in that order"
            ],
            1,
        )

    def test_roster_headings_in_the_wrong_order_fail(self):
        self.write(
            "kitchen/council.md",
            ROSTER_HEAD + "\n## On-demand specialists\n\n## Core lenses\n",
        )
        self.check(
            [
                "kitchen/council.md: needs the headings ## Core lenses and "
                "## On-demand specialists, in that order"
            ],
            1,
        )

    def test_lens_heading_without_a_record_link_fails(self):
        text = roster(core=entry() + "\n### Budget-style lens\n\n- **Job:** Cost\n")
        line = text.split("\n").index("### Budget-style lens") + 1
        self.check_roster(
            text,
            "line %d: lens heading must be ### [<Name>-style lens](vetting/<slug>.md)"
            % line,
        )

    def test_lens_heading_outside_the_groups_fails(self):
        text = roster(core=entry()).replace(
            "\n## Core lenses\n", "\n### [Example-style lens](vetting/example.md)\n\n## Core lenses\n"
        )
        line = text.split("\n").index("### [Example-style lens](vetting/example.md)") + 1
        self.check_roster(
            text,
            "line %d: a ### heading must be under ## Core lenses or "
            "## On-demand specialists" % line,
        )

    def test_text_inside_an_entry_fails(self):
        text = roster(core=entry() + "\nA paragraph about the cook.\n")
        line = text.split("\n").index("A paragraph about the cook.") + 1
        self.check_roster(
            text, "line %d: only the four items may follow a lens heading" % line
        )

    def test_lens_seated_twice_fails(self):
        self.check_roster(
            roster(core=entry(), specialists=entry()), "example: seated more than once"
        )

    def test_entry_items_out_of_order_fail(self):
        text = roster(core=entry()).replace(
            "- **Job:** Heat and ingredient function\n"
            "- **Typical question:** Which variable changes the result?\n",
            "- **Typical question:** Which variable changes the result?\n"
            "- **Job:** Heat and ingredient function\n",
        )
        self.check_roster(
            text,
            "example: expected the items Job, Typical question, Scope, "
            "Where it can mislead, in that order",
        )

    def test_entry_with_a_missing_item_fails(self):
        text = roster(core=entry()).replace(
            "- **Where it can mislead:** It can add steps.\n", ""
        )
        self.check_roster(
            text,
            "example: expected the items Job, Typical question, Scope, "
            "Where it can mislead, in that order",
        )

    def test_entry_without_a_record_fails(self):
        self.check_roster(
            roster(core=entry() + entry("ghost", lens="Ghost-style lens")),
            "ghost: no record at kitchen/vetting/ghost.md",
        )

    def test_seating_a_cut_record_fails(self):
        self.write(
            "kitchen/vetting/example.md", record(verdict="cut", scope="none")
        )
        self.write("kitchen/council.md", roster(core=entry(scope="none")))
        self.check(
            ["kitchen/council.md: example: seated, but its record's verdict is cut"], 1
        )

    def test_entry_under_the_wrong_heading_fails(self):
        self.check_roster(
            roster(specialists=entry()),
            "example: listed under On-demand specialists, but its record says "
            "seat: core",
        )

    def test_entry_that_differs_from_its_record_fails(self):
        self.check_roster(
            roster(
                core=entry(
                    lens="Sample-style lens",
                    job="Everything",
                    question="Why?",
                    scope="All cooking",
                )
            ),
            "example: Lens name differs from its record",
            "example: Job differs from its record",
            "example: Typical question differs from its record",
            "example: Scope differs from its record",
        )

    def test_seated_record_missing_from_the_roster_fails(self):
        self.write("kitchen/council.md", roster())
        self.write("kitchen/vetting/example.md", record(verdict="seat narrower"))
        self.check(
            [
                "kitchen/vetting/example.md: verdict is seat narrower, but "
                "kitchen/council.md does not seat it"
            ],
            1,
        )

    def test_two_records_with_one_lens_name_fail(self):
        self.write("kitchen/vetting/example.md", record())
        self.write("kitchen/vetting/other.md", record())
        self.write("kitchen/council.md", roster(core=entry() + entry("other")))
        self.check(
            [
                "kitchen/vetting/other.md: lens Example-style lens is also used by "
                "kitchen/vetting/example.md"
            ],
            1,
        )

    def test_quotation_marks_in_the_roster_fail(self):
        text = roster(core=entry(mislead='It says "always".'))
        line = text.split("\n").index('- **Where it can mislead:** It says "always".') + 1
        self.check_roster(
            text,
            "line %d: double quotation marks and blockquotes are not allowed" % line,
        )

    # The command.

    def test_every_problem_is_reported_in_path_order(self):
        self.write("kitchen/vetting/example.md", record(seat="guest"))
        self.write("kitchen/vetting/zed.md", "no front matter\n")
        self.write(
            "kitchen/council.md", roster(core=entry() + entry("ghost", lens="Ghost-style lens"))
        )
        self.check(
            [
                "kitchen/council.md: ghost: no record at kitchen/vetting/ghost.md",
                "kitchen/vetting/example.md: seat must be core or specialist",
                "kitchen/vetting/zed.md: front matter is missing",
            ],
            1,
        )

    def test_extra_argument_is_a_usage_error(self):
        result = run(self.root, "extra")
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "usage: check-council.py [repository-root]\n")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
````

#### File: `scripts/check-council.py`

````python
#!/usr/bin/env python3
"""Check the council roster against the lens vetting records.

Usage: python3 scripts/check-council.py [repository-root]

A record is a file kitchen/vetting/<slug>.md in the shape of
templates/lens-vetting-record.md. The roster, kitchen/council.md, seats a lens
with a heading that links its record. The check fails when a record is
malformed, when the roster seats a lens with no record or a cut record, when
a record that says seat is not on the roster, and when the roster and a
record disagree. kitchen/council-vetting.md states the rule in words.

Prints one line per problem and exits 1, or prints
"council checked: <S> seated, <R> records" and exits 0.
"""

import datetime
import os
import re
import sys

KEYS = ["lens", "name", "seat", "job", "question", "verdict", "scope", "checked"]
SECTIONS = [
    "Official site",
    "Published work",
    "Independent sources",
    "What the published work shows",
    "Where this lens can mislead",
    "Verdict",
    "Access notes",
]
CITED = SECTIONS[:3]
ITEMS = ["Job", "Typical question", "Scope", "Where it can mislead"]
GROUPS = {"Core lenses": "core", "On-demand specialists": "specialist"}
YAML_WORDS = {"yes", "no", "true", "false", "on", "off", "null", "y", "n"}
ROSTER = "kitchen/council.md"
CHECKED = re.compile(r"\(checked (\d{4}-\d{2}-\d{2})\)")
ENTRY = re.compile(r"^### \[(.+-style lens)\]\(vetting/([a-z0-9]+(?:-[a-z0-9]+)*)\.md\)$")
ITEM = re.compile(r"^- \*\*(.+?):\*\* (.*\S)\s*$")
LINK = re.compile(r"https://\S+")


def is_date(text):
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return re.fullmatch(r"\d{4}-\d{2}-\d{2}", text) is not None


def has_checked(text):
    return any(is_date(found) for found in CHECKED.findall(text))


def quote_problems(lines):
    problems = []
    for number, line in enumerate(lines, 1):
        if line.startswith(">") or any(mark in line for mark in '"“”'):
            problems.append(
                "line %d: double quotation marks and blockquotes are not allowed"
                % number
            )
    return problems


def top_items(lines):
    """Join each top-level list item with its indented continuation lines."""
    items = []
    for line in lines:
        if line.startswith("- "):
            items.append(line[2:])
        elif items and line.startswith("  "):
            items[-1] += " " + line.strip()
    return items


def check_record(lines):
    """Return (fields or None, problems) for one record's lines."""
    problems = []
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return None, ["front matter is missing"]
    end = lines.index("---", 1)
    fields = {}
    order = []
    for number, line in enumerate(lines[1:end], 2):
        match = re.fullmatch(r"([a-z_]+): (.*\S)", line)
        if not match:
            problems.append("front matter line %d is not key: value" % number)
            continue
        order.append(match.group(1))
        fields[match.group(1)] = match.group(2)
    if problems:
        return None, problems
    if order != KEYS:
        return None, ["front matter keys must be exactly: %s" % ", ".join(KEYS)]

    for key in KEYS:
        value = fields[key]
        if not value[0].isalnum() or '"' in value or ": " in value or " #" in value:
            problems.append(
                "%s must start with a letter or digit and hold no double quote, "
                "colon-space, or space-hash" % key
            )
        if value.lower() in YAML_WORDS:
            problems.append("%s must not be a YAML boolean or null word" % key)
    if not fields["lens"].endswith("-style lens"):
        problems.append("lens must end with -style lens")
    if fields["seat"] not in ("core", "specialist"):
        problems.append("seat must be core or specialist")
    if not fields["question"].endswith("?"):
        problems.append("question must end with a question mark")
    verdict = fields["verdict"]
    if verdict not in ("seat", "seat narrower", "cut"):
        problems.append("verdict must be seat, seat narrower, or cut")
    elif verdict == "cut" and fields["scope"] != "none":
        problems.append("scope must be none when the verdict is cut")
    elif verdict != "cut" and fields["scope"] == "none":
        problems.append("scope must not be none unless the verdict is cut")
    if not is_date(fields["checked"]):
        problems.append("checked must be a date written YYYY-MM-DD")

    body = lines[end + 1:]
    title = []
    for line in body:
        if line.startswith("## "):
            break
        if line.strip():
            title.append(line)
    if title != ["# " + fields["lens"]]:
        problems.append(
            "the text before the first section must be the title line "
            "# <lens> and nothing else"
        )
    names = [line[3:] for line in body if line.startswith("## ")]
    if names != SECTIONS:
        problems.append("sections must be exactly, in order: %s" % ", ".join(SECTIONS))
        return fields, problems + quote_problems(lines)
    sections = {}
    current = None
    for line in body:
        if line.startswith("## "):
            current = sections.setdefault(line[3:], [])
        elif current is not None:
            current.append(line)

    seated = verdict in ("seat", "seat narrower")
    counts = {}
    links = set()
    for name in SECTIONS:
        content = [line for line in sections[name] if line.strip()]
        if not content:
            problems.append("section %s is empty" % name)
            continue
        if name not in CITED:
            continue
        if not content[0].startswith("- ") or any(
            not line.startswith(("- ", "  ")) for line in content
        ):
            problems.append(
                "%s: every line must be a list item or its indented continuation"
                % name
            )
        items = top_items(content)
        counts[name] = len(items)
        for number, item in enumerate(items, 1):
            if name == "Official site" and item.startswith("No official site"):
                plain = True
                counts["no site"] = 1
            else:
                plain = not seated and item.startswith("None found")
            if plain:
                if not has_checked(item):
                    problems.append("%s: item %d needs (checked YYYY-MM-DD)" % (name, number))
            elif "https://" not in item or not has_checked(item):
                problems.append(
                    "%s: item %d needs an https:// link and (checked YYYY-MM-DD)"
                    % (name, number)
                )
            else:
                link = LINK.search(item).group(0)
                if link in links:
                    problems.append(
                        "%s: item %d repeats a link already cited in this record"
                        % (name, number)
                    )
                links.add(link)
    if counts.get("Official site", 1) != 1:
        problems.append(
            "Official site: expected one list item, found %d" % counts["Official site"]
        )
    if seated:
        if counts.get("Published work", 2) < 2:
            problems.append(
                "Published work: a seated lens needs at least 2 items, found %d"
                % counts["Published work"]
            )
        need = 2 if counts.get("no site") else 1
        if counts.get("Independent sources", need) < need:
            problems.append(
                "Independent sources: a seated lens needs at least %d items, found %d"
                % (need, counts["Independent sources"])
            )
        shown = sections["What the published work shows"]
        tendencies = sum(1 for line in shown if re.match(r"\d+\. \S", line))
        if any(line.strip() for line in shown) and not 3 <= tendencies <= 5:
            problems.append(
                "What the published work shows: a seated lens needs 3 to 5 "
                "numbered items, found %d" % tendencies
            )
        if any(
            line.strip() and not re.match(r"\d+\. \S|  ", line) for line in shown
        ):
            problems.append(
                "What the published work shows: a seated lens lists numbered "
                "items and nothing else"
            )
    return fields, problems + quote_problems(lines)


def check_roster(lines):
    """Return (entries, problems); an entry is (slug, group, lens, items)."""
    problems = []
    headings = [line[3:] for line in lines if line.startswith("## ")]
    if [name for name in headings if name in GROUPS] != list(GROUPS):
        problems.append(
            "needs the headings ## Core lenses and ## On-demand specialists, "
            "in that order"
        )
        return [], problems + quote_problems(lines)
    entries = []
    group = None
    current = None
    for number, line in enumerate(lines, 1):
        if line.startswith("## "):
            group = line[3:] if line[3:] in GROUPS else None
            current = None
        elif line.startswith("### ") and not group:
            problems.append(
                "line %d: a ### heading must be under ## Core lenses or "
                "## On-demand specialists" % number
            )
        elif line.startswith("### "):
            match = ENTRY.match(line)
            if match:
                current = []
                entries.append((match.group(2), group, match.group(1), current))
            else:
                current = None
                problems.append(
                    "line %d: lens heading must be "
                    "### [<Name>-style lens](vetting/<slug>.md)" % number
                )
        elif current is not None and line.startswith("- "):
            current.append(line)
        elif current is not None and line.strip() and not line.startswith("  "):
            problems.append(
                "line %d: only the four items may follow a lens heading" % number
            )
    return entries, problems + quote_problems(lines)


def read_lines(path):
    """Return the file's lines, or None when it is not readable UTF-8 text."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read().split("\n")
    except (OSError, UnicodeDecodeError):
        return None


def main(argv):
    if len(argv) > 2:
        print("usage: check-council.py [repository-root]", file=sys.stderr)
        return 2
    if len(argv) == 2:
        root = argv[1]
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    problems = []
    records = {}
    lenses = {}
    count = 0
    vetting = os.path.join(root, "kitchen", "vetting")
    names = sorted(os.listdir(vetting)) if os.path.isdir(vetting) else []
    for name in names:
        if name.startswith("."):
            continue
        path = "kitchen/vetting/%s" % name
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.md", name):
            problems.append(
                (path, "file name is not <slug>.md with a lowercase, hyphenated slug")
            )
            continue
        count += 1
        slug = name[:-3]
        lines = read_lines(os.path.join(vetting, name))
        if lines is None:
            fields, found = None, ["cannot be read as UTF-8 text"]
        else:
            fields, found = check_record(lines)
        problems.extend((path, text) for text in found)
        if fields is None or found:
            # A record with problems of its own is not compared with the roster.
            records[slug] = None
            continue
        records[slug] = fields
        if fields["lens"] in lenses:
            problems.append(
                (path, "lens %s is also used by kitchen/vetting/%s.md"
                 % (fields["lens"], lenses[fields["lens"]]))
            )
        else:
            lenses[fields["lens"]] = slug

    roster_path = os.path.join(root, "kitchen", "council.md")
    if not os.path.isfile(roster_path):
        problems.append((ROSTER, "file is missing"))
        entries = None
    else:
        lines = read_lines(roster_path)
        if lines is None:
            entries, found = None, ["cannot be read as UTF-8 text"]
        else:
            entries, found = check_roster(lines)
        problems.extend((ROSTER, text) for text in found)

    seated = []
    for slug, group, lens, items in entries or []:
        if slug in seated:
            problems.append((ROSTER, "%s: seated more than once" % slug))
            continue
        seated.append(slug)
        values = {}
        labels = []
        for line in items:
            match = ITEM.match(line)
            labels.append(match.group(1) if match else None)
            if match:
                values[match.group(1)] = match.group(2)
        if labels != ITEMS:
            problems.append(
                (ROSTER, "%s: expected the items %s, in that order"
                 % (slug, ", ".join(ITEMS)))
            )
        if slug not in records:
            problems.append(
                (ROSTER, "%s: no record at kitchen/vetting/%s.md" % (slug, slug))
            )
            continue
        fields = records[slug]
        if fields is None:
            continue
        if fields["verdict"] == "cut":
            problems.append((ROSTER, "%s: seated, but its record's verdict is cut" % slug))
        if GROUPS[group] != fields["seat"]:
            problems.append(
                (ROSTER, "%s: listed under %s, but its record says seat: %s"
                 % (slug, group, fields["seat"]))
            )
        pairs = [("Lens name", lens, "lens")]
        pairs += [(label, values.get(label), key) for label, key in
                  (("Job", "job"), ("Typical question", "question"), ("Scope", "scope"))]
        for label, value, key in pairs:
            if value is not None and value != fields[key]:
                problems.append((ROSTER, "%s: %s differs from its record" % (slug, label)))
    if entries is not None:
        for slug in sorted(records):
            fields = records[slug]
            if fields and fields["verdict"] in ("seat", "seat narrower") and slug not in seated:
                problems.append(
                    ("kitchen/vetting/%s.md" % slug,
                     "verdict is %s, but kitchen/council.md does not seat it"
                     % fields["verdict"])
                )

    if problems:
        for path, text in sorted(problems, key=lambda problem: problem[0]):
            print("%s: %s" % (path, text))
        return 1
    print("council checked: %d seated, %d records" % (len(seated), count))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
````

#### File: `kitchen/council-vetting.md`

````markdown
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
````

#### File: `kitchen/council.md`

````markdown
# The council

The council is a set of lenses: ways of looking at a recipe, each built from one cook's or one publisher's published work. Each lens is named `<Name>-style lens`. Every lens here has a vetting record in the `kitchen/vetting/` folder, and the lens argues only from the tendencies that record lists and only inside its scope. [`council-vetting.md`](council-vetting.md) is the rule for seating one.

No one named here is affiliated with this repository, and no one named here has reviewed, approved, endorsed, or contributed to anything in it. A lens is a reading of published work. It is not the person and does not speak for them.

## How the council argues

- **Relevance first.** Consult the lenses whose job fits the question. The core lenses are the default. A specialist joins only when the dish is in its scope.
- **Lenses, not people.** Attribute advice to the lens, by the name it has below. Never write that a person says, thinks, or would do something, and never invent a quotation.
- **Stay inside the record.** A lens does not argue outside its scope. When no seated lens covers a question, say so instead of stretching one.
- **Standards, not lenses, for numbers.** A safe temperature, a ratio, a pressure-cooker minimum, or a nutrition figure comes from a cited standard, a tested source, or the equipment manual. Food safety is a constraint on every lens, not a seat.
- **Disagree by name, then resolve.** When lenses pull in different directions, say which lens argues what, give one resolved recommendation, and name any dissent that still stands.
- **The cook decides.** The council advises.

## Changing the roster

This roster is yours to edit. To add, change, or remove a lens, follow [`council-vetting.md`](council-vetting.md): the record comes first, and the entry here repeats it. Each entry below is a heading that links the lens to its record, followed by a blank line and four one-line items in this order: Job, Typical question, Scope, and Where it can mislead. `python3 scripts/check-council.py` checks the roster against the records.

## Core lenses

Consulted by default, each for its own job.

## On-demand specialists

Consulted only when the dish is in the lens's scope.
````

#### File: `templates/lens-vetting-record.md`

````markdown
---
lens: Name-style lens
name: Full name as published
seat: core or specialist
job: The job this lens does on the council, in a few words
question: The one question this lens always asks?
verdict: seat, seat narrower, or cut
scope: What this lens may argue about, or none when the verdict is cut
checked: YYYY-MM-DD
---

# Name-style lens

Copy this file to `kitchen/vetting/<slug>.md` and replace every line. [`kitchen/council-vetting.md`](../kitchen/council-vetting.md) is the rule this record has to meet. Delete this paragraph when the record is filled in.

## Official site

- Site name: https://example.com/ (checked YYYY-MM-DD). What the site is and what was read there.

## Published work

- *Title of a book, series, or column* (publisher, year): https://example.com/ (checked YYYY-MM-DD). Why it is relevant to the seat.
- *A second published work*: https://example.com/ (checked YYYY-MM-DD). Why it is relevant to the seat.

## Independent sources

- *Publication, review, award listing, or a book by someone else*: https://example.com/ (checked YYYY-MM-DD). What it confirms about the published work.

## What the published work shows

1. A tendency the published work shows, in your own words.
2. A second tendency.
3. A third tendency. Five at most.

## Where this lens can mislead

Where advice argued from these tendencies goes wrong for a home cook, and what to check when it does. This describes the lens, never the person.

## Verdict

Seat, seat narrower, or cut, and the reason. A narrower seat says what the lens may not argue.

## Access notes

Pages that were not read, paywalls, pages that would not load, and anything known only from a search result.
````

#### File: `AGENTS.md`

````markdown
# Agent entry point: Chef Council

This repository is a system for cooking with AI agents: a council of cooking lenses that develops and pressure-tests recipes, plain-text recipe cards and cook logs, and an independent editor check on every recipe change. Read this file first, then the files it points to. It applies to every agent, whichever harness runs it.

The person you are working with is called the cook here. If you cannot read or write files in this repository (a chat app, for example), say so once, and when asked to save something return the complete file and its path for the cook to save.

## Read in this order

1. [`kitchen/README.md`](kitchen/README.md), then [`kitchen/profile.md`](kitchen/profile.md), [`kitchen/equipment.md`](kitchen/equipment.md), and [`kitchen/pantry.md`](kitchen/pantry.md): who is being cooked for, their constraints and standing corrections, the equipment, and a dated pantry snapshot. A file whose front matter says `filled_in: no` is still a blank template: ask the cook, and never treat a placeholder as a fact.
2. [`kitchen/council.md`](kitchen/council.md): the lenses on the council, what each one is for, its scope, and where it can mislead. Each lens has a vetting record in `kitchen/vetting/`, and [`kitchen/council-vetting.md`](kitchen/council-vetting.md) is the rule for seating one.
3. The skill for the job, from [Skills](#skills) below. Read its `SKILL.md` in full before acting on it.
4. The saved recipe card, and its most recent cook log, before changing that recipe or cooking from it.

## Rules that are easy to get wrong

- **The latest correction beats a saved card.** When the cook's most recent explicit instruction disagrees with a saved card, name the conflict, follow the correction, and update the card. The standing corrections in `kitchen/profile.md` beat a card in the same way.
- **Status is several separate facts:** how far the recipe has been developed, whether it has been cooked and how that went, whether the card is saved in the repository, and whether any copy outside the repository is up to date. Writing a card does not make it cooked, and cooking it once does not make it a house recipe. Never raise any of these without a logged cook or the cook saying so.
- **Never report a save, sync, or check that did not happen.** Say "saved" only after the file is written, "synced" only after reading the other copy back, and "checked" only when the check ran and you read its result. When a step failed or was skipped, say which one and why.
- **Do not invent** quantities, times, temperatures, cook outcomes, allergies, equipment limits, or sources. When a number is missing, say so on the card.
- **Keep the old version when testing a new one.** A small edit is a version bump on the same card. A changed technique or a variant is its own card, and the original stays.
- **The council is a set of lenses, not people.** Attribute advice to a lens, written `<Name>-style lens`. No real chef has reviewed, approved, endorsed, or contributed to anything here, so never say or imply one did, and never invent a quote. A lens argues only from the tendencies in its vetting record and only inside its scope. Asked to add a name to the council, vet it first under `kitchen/council-vetting.md`, then seat it or decline with the reason.
- **Food safety is a constraint, not a lens's opinion.** A safety number comes from a cited standard. When `higher_risk_diners` in `kitchen/profile.md` is `yes`, use the stricter endpoints; when it is `unknown`, ask before giving one.
- **Every recipe change gets an independent editor check.** A separate agent, in a fresh context that did not write the card, compares the card one for one with the exact text the cook approved. A failed check blocks the change. With no second agent available, say so; never certify your own work.
- **Copy no third-party recipe text:** no ingredient lists, methods, or headnotes from any publisher. Credit a source by title and link only when it was actually read.

## The loop

1. **Idea.** The cook says what they want to make or what they have on hand.
2. **Baseline.** Recover the current card and its last cook log, if they exist.
3. **Council.** Pick the lenses that matter, then give one recommendation, or two or three directions when the choice changes the dish. The cook chooses the direction.
4. **Pressure test.** Before anyone cooks, check the recipe: each ingredient's role, stacked salt, sugar and acid, cut and thickness, crowding, liquid, scaling, and whether the ingredient list matches the method. Reprint the corrected recipe in full.
5. **Live cook.** Guide one step at a time: do this now, the cue to look for, what comes next. The cook cooks and may substitute.
6. **Report back.** The cook says what they actually did and how it turned out. That report is the evidence.
7. **Codify.** Write or update the card and the cook log from what was approved and reported, with an honest status. The cook sets the scope of the save.
8. **Editor check.** A fresh agent checks the card against the approved text. On a fail, fix the card and run a fresh check.
9. **Pull request.** Open one; the cook merges it.
10. **Mirror, on request only.** Copy a card to a notes app only when the cook asks or calls the recipe final, then read the copy back.
11. **Promote.** Only the cook calls a recipe a house recipe.

What stays with the cook: choosing a direction, the scope of a save, what was cooked and how it tasted, promoting a recipe, and the merge.

## Skills

Skills live in `.agents/skills/<name>/`, and Claude Code finds them through the links in `.claude/skills/`. If your harness did not load a skill on its own, open the path given here and follow it. [`.agents/skills/README.md`](.agents/skills/README.md) explains how a skill is added.

- No skill is installed yet. The first skill added replaces this line.

## Making changes

- Work on a branch and open a pull request against `main`, so the checks run before the merge.
- Write commit subjects in the imperative mood, such as `Add the roasted carrots card v1.0`.
- Before opening a pull request, run the checks CI runs:
  - `python3 scripts/check-skills.py`: every skill has its link and its line above.
  - `python3 scripts/check-council.py`: the council roster matches the vetting records.
  - `python3 -m unittest discover -s tests -v`: the tests for the scripts.
  - `scripts/secret-scan.sh`: gitleaks over the full history.
- Never commit a secret, a credential, or a token. Source packets, the exact text a cook approved, stay in the git-ignored `.sources/` folder.
- Everything committed to a public fork is public, including `kitchen/` and the history. Keep out anything the cook would not publish.
````

#### File: `kitchen/README.md`

````markdown
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
````

#### File: `.github/workflows/ci.yml`

````yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  secret-scan:
    name: gitleaks (full history)
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - name: Check out the full history
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          fetch-depth: 0
          persist-credentials: false
      - name: Scan every commit for secrets
        run: scripts/secret-scan.sh

  checks:
    name: tests
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - name: Check out
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - name: Check every skill has its link and its AGENTS.md line
        run: python3 scripts/check-skills.py
      - name: Check the council roster against the vetting records
        run: python3 scripts/check-council.py
      - name: Run the tests
        run: python3 -m unittest discover -s tests -v
````
