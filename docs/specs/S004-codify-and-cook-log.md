---
date: 2026-11-19
id: S004
wayfinder: docs/wayfinder/W001-public-chef-council/issues/T010-codify-and-cook-log.md
target_release: none
status: executing
base_branch: main
base_sha: bec1b67b158e384d52414e731be051a80e54f0cf
work_branch: workstream/t010-codify-and-cook-log
pr_base: main
prior_specs:
  - docs/specs/archive/S001-scaffold.md
  - docs/specs/archive/S002-council-roster-and-vetting.md
  - docs/specs/archive/S003-chef-council-skill.md
references:
  - docs/wayfinder/W001-public-chef-council/MAP.md
  - docs/wayfinder/W001-public-chef-council/issues/T003-license.md
  - docs/wayfinder/W001-public-chef-council/issues/T005-privacy-rules.md
  - docs/wayfinder/W001-public-chef-council/issues/T011-editor-gate.md
  - docs/learnings/L001-scaffold.md
  - docs/learnings/L002-council-roster-and-vetting.md
  - docs/learnings/L003-chef-council-skill.md
  - .agents/spec-profile.md
cross_examined: meta/muse-wonder-full-1.0 (architect), 27 findings, 27 accepted
approved_by: autonomous
approved_at: 2026-11-19T01:46Z
pr: none
kickbacks: 0
merged: none
harvested: none
---

# Codify and cook log: two skills, three templates, the status rules, and the index generator

## Goal and definition of done

Ship ticket T010: the `recipe-codify` and `cook-log` skills, each with its
Claude Code link and its line in the index in `AGENTS.md`, and what they
write with: `templates/recipe-card.md`, `templates/cook-log.md`,
`templates/source-packet.md`, `method/status-and-versions.md`, and
`scripts/build-index.py` with its tests and the `recipes/INDEX.md` it
generates.

Every text file is given byte for byte under `## File contents`, and the
`AGENTS.md` change is two lines replaced and two added. Leg 1 wrote and
tested every file in a scratch clone at `base_sha`; the executor does not
rewrite any of them. Between that text and the merge stand the unit tests
(Tasks 1 and 2) and two behavior checks by fresh subagents, each in its own
scratch repository (definition-of-done item 8).

Done means all of the following, each observed on the work branch's head
commit after Task 4, from the repository root, in a shell prepared as
`## Build plan — agent loop` says:

1. **The files.** `git ls-files .agents/skills/recipe-codify
   .agents/skills/cook-log .claude/skills/recipe-codify
   .claude/skills/cook-log templates/recipe-card.md templates/cook-log.md
   templates/source-packet.md method recipes scripts/build-index.py
   tests/test_build_index.py` prints exactly these eleven lines:

   ```text
   .agents/skills/cook-log/SKILL.md
   .agents/skills/recipe-codify/SKILL.md
   .claude/skills/cook-log
   .claude/skills/recipe-codify
   method/status-and-versions.md
   recipes/INDEX.md
   scripts/build-index.py
   templates/cook-log.md
   templates/recipe-card.md
   templates/source-packet.md
   tests/test_build_index.py
   ```

2. **The bytes.** This prints ten lines, each a path followed by `: OK`,
   one for each regular file this spec gives or changes (the two links of
   item 1 have no content to hash, and item 6's `readlink` lines check
   them):

   ```bash
   sha256sum -c - <<'SUMS'
   77ca8a64980fa2a82c3197733dae95f943672ca4e0db4ed01ae134aa28ce4bb3  .agents/skills/cook-log/SKILL.md
   86cb5d65d692c3f0971c6514035eefa84dd2985c1dd2342c7c5b82fcc315ee04  .agents/skills/recipe-codify/SKILL.md
   de0d3cfe5b4c4526de27556f1d9d4195bb2425f734a232d02b5ab0e6e7aa3532  AGENTS.md
   70706acbaf730af38629f8c4c9d2e290d10cbfd6a44339543751033580170579  method/status-and-versions.md
   36b42ea72e1889a4098d55c6439ef86bd343dc51d15f7996b4c8e4f0702609f0  recipes/INDEX.md
   5036f021d743a415319575a96258814f4b8bb75561047ed37c9eda443a48406d  scripts/build-index.py
   2033381f6c7842d5c7441e1e7b5cd3a745192d2d0bf8bdf247c3b374506c5fce  templates/cook-log.md
   00853d062827f33402fab046714c80592b1b963ea47a0f1888ef1cb2063e4939  templates/recipe-card.md
   c063566e59e32564599c99168b384f5d13c168fe91f79aef318bd783a39ebaa7  templates/source-packet.md
   0b59a9d2730a6efc1b5061a87ff65abedb4c00d666a9d0f7fe21cbd11b426568  tests/test_build_index.py
   SUMS
   ```

3. **The repository's checks.** `python3 scripts/check-skills.py; echo $?`
   prints `skills checked: 3` then `0`. `python3 scripts/check-council.py;
   echo $?` prints `council checked: 14 seated, 14 records` then `0`.
   `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
   `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"` prints
   `117`. `python3 scripts/build-index.py --check; echo $?` prints `index
   current: 0` then `0`. `scripts/secret-scan.sh; echo $?` ends with `0`.
   `python3 "$WAYFINDER/scripts/lint.py" docs/wayfinder/*/MAP.md; echo $?`
   prints `0` and nothing else (`WAYFINDER` is set as `## Prerequisites`
   says). The three diff checks and the full privacy sweep pass as the
   profile's ship tail requires.
4. **Links.** `linkcheck AGENTS.md .agents/skills/recipe-codify/SKILL.md
   .agents/skills/cook-log/SKILL.md templates/recipe-card.md
   templates/cook-log.md templates/source-packet.md
   method/status-and-versions.md recipes/INDEX.md; echo $?` prints `0` and
   nothing else.
5. **CI.** `gh pr checks <PR>` reports every check passed, and the log of
   the `tests` job holds the line `test_this_repository_index_is_current
   (test_build_index.BuildIndexTest.test_this_repository_index_is_current)
   ... ok`.
6. **A fresh clone agrees.** Make a fresh clone of the pushed branch in a
   new temporary directory, from the repository root:

   ```bash
   CLONE=$(mktemp -d)
   git clone --quiet --branch workstream/t010-codify-and-cook-log "$(git remote get-url origin)" "$CLONE"
   ```

   Then, from inside `$CLONE`: `git rev-parse HEAD` equals the pull
   request's head commit (`gh pr view <PR> --json headRefOid --jq
   .headRefOid`); `readlink .claude/skills/recipe-codify` prints
   `../../.agents/skills/recipe-codify` and `readlink
   .claude/skills/cook-log` prints `../../.agents/skills/cook-log`; `cmp
   .claude/skills/recipe-codify/SKILL.md
   .agents/skills/recipe-codify/SKILL.md; echo $?` and `cmp
   .claude/skills/cook-log/SKILL.md .agents/skills/cook-log/SKILL.md; echo
   $?` each print `0` and nothing else; `python3 scripts/check-skills.py`
   prints `skills checked: 3`; and `python3 scripts/build-index.py --check`
   prints `index current: 0`. Afterward `git -C "$CLONE" status --porcelain`
   prints nothing.
7. **Rendered and read.** Render `AGENTS.md`, the two `SKILL.md` files, the
   three templates, `method/status-and-versions.md`, and `recipes/INDEX.md`
   from the pushed branch with the profile's observation command and look at
   each result. It passes when every heading renders as a heading, every
   list as a list, and every table as a table (in `recipe-codify/SKILL.md`
   the kinds-of-save table; in `templates/recipe-card.md` the ingredient
   table and the failure-modes table; in `method/status-and-versions.md`
   the four tables); the seven lines under the title of
   `templates/recipe-card.md` render as seven list items; the three pairs of
   tilde lines in `templates/source-packet.md` render as three code blocks
   holding `Paste here.`; no raw Markdown markup is visible in the body
   below the front matter outside a code span or a code block; and each
   link added by this spec is a link. How GitHub displays the front matter
   is not judged (L001).
8. **Behavior.** The two checks of `### Behavior checks` each pass. The
   pull request's Evidence section holds each of the two replies verbatim in
   a collapsed `<details>` block, with its `codify check ok:` or `log check
   ok:` line above it, and below the first the card and the source packet
   the subagent wrote, and below the second the log it wrote, each verbatim
   in its own collapsed `<details>` block.

The ticket's two done-conditions map onto item 8. "Following codify on a
fixture produces a card, a regenerated index, and a source packet ready for
the editor" is the `codify` check. "Following cook-log produces a log that
separates the cook's words from inference" is the `log` check.

## Decisions

Decisions T003 and T005 bind this spec; the profile's `## Pipeline
constraints` apply to every file, every commit message, and the pull
request.

1. **All content is fixed here.** Leg 1 wrote every file, built Tasks 1 to 4
   from this spec in a scratch clone at `base_sha`, and ran every gate line
   that needs no pushed branch. Every task is therefore `mechanical`.
2. **Layout.** Each skill is one `SKILL.md` with no references:
   `recipe-codify/SKILL.md` is 85 lines and `cook-log/SKILL.md` is 54, far
   under the Agent Skills guidance of 500. The design tree's
   `cook-logs/README.md`, `templates/qc-report.md`, and
   `templates/research-brief.md` (`private-sources/design/design-report.md`
   §6) are not created: the ticket does not name them, the editor's report
   format is T011's, and the place of a cook log is stated in the skill, the
   template, and the method page.
3. **Skill front matter.** Exactly `name` and `description`, in that order,
   each on one line, as S003's decision 2 fixed: `name` equals the folder
   name, and the description is one plain line of at most 1024 characters
   that holds no colon followed by a space, no space followed by `#`, and no
   quotation mark (L001). The design report's draft descriptions (§6) are
   reworded to drop their quotation marks. No skill file names a person or a
   lens.
4. **The card's front matter.** Six lines in this order: `id`, `version`,
   `status`, `evidence`, `category`, `mirrors`. They are read as plain `key:
   value` lines, not through a YAML library, and every value this spec
   defines is a plain word that no YAML reader turns into a boolean (L001).
   That is the rule for writing a card: six lines, this order, one space
   after the colon. Reading is more tolerant on purpose. The ticket calls
   the front matter optional, and this spec reads that as follows: the
   template and the `recipe-codify` skill always write it, and the index
   generator lists a card that lacks it, or lacks a line of it, with `not
   stated` instead of failing, and accepts the lines in any order (decision
   21). `codifycheck` holds a card the skill wrote to the writing rule: the
   keys in this order, each once, with `mirrors` allowed to be absent. How
   strict the linter is about it is T011's decision.
5. **The lines under the title.** Seven list items, one fact each: Version,
   Date, Status, Kitchen evidence, Source, Yield, Time. The private
   predecessor put two facts on a line with a bar between them
   (`private-sources/cooking/templates/recipe-card.md`), and consecutive
   lines of that form fall into one paragraph when Markdown is rendered; one
   list item per fact renders on its own line and gives T011's linter one
   line per field. The predecessor's recipe-ID line is dropped, since `id`
   is in the front matter and equals the file name. Its notes-app field
   becomes the optional `mirrors` line, which holds `none` or destination
   names separated by commas and never an account's ID or URL (T005); the
   IDs belong to the sync map T013 defines.
6. **The card's sections.** Ten `##` headings in this order: Equipment,
   Ingredients, Method, Why this works, Failure modes, Variations, Storage,
   Notes, Next experiment, Changelog. Next experiment is its own heading
   because the ticket lists it as a section; in the predecessor it was a
   line inside Notes. The predecessor's Optional Enhancements table is
   dropped; an optional addition is a variation. A heading with nothing to
   hold gets `None recorded.`, and something a cook needs that the approved
   text leaves out gets `Not stated.`, a line under Notes, and the status
   `draft`.
7. **Placeholders are example text.** No template uses angle brackets
   outside a code span, because GitHub drops unknown HTML tags (S001's
   decision 7). Each template opens with a paragraph that says where to copy
   it and to delete that paragraph.
8. **Codifying adds nothing.** The card's Equipment, Ingredients, Method,
   Yield, and Time carry the approved text and nothing else; the other
   sections hold only what the approved text or the cook said. The skill
   forbids a new quantity, time, temperature, ingredient, step, or piece of
   advice, and forbids converting a unit unless the cook asks (L003 records
   what an unprinted conversion cost). Rewording a step and arranging the
   recipe into the template's tables and stages are allowed. This is what
   lets T011's editor compare the card with the packet one for one.
9. **Third-party text and credit.** The skill restates the repository's
   rule: no publisher's ingredient list, method, or headnote goes into a
   card, a source is credited by title and link only when it was read, a
   lens is never an author or a source, and no card says a person reviewed
   or approved it. When the approved text is a publisher's recipe, the skill
   says so and asks the cook what of their own to save. The packet may hold
   such text, which is one reason it is never committed.
10. **Status is four facts** (the design report's §3 item 4, generalized
    from `private-sources/cooking/context/publishing-workflow.md`).
    Development is the card's `status` line: `draft`, `reviewed`, `testing`,
    `house`, `retired`. Kitchen evidence is the card's `evidence` line:
    `untested`, `cooked-once`, `repeated`, `not-recorded`. Saved is a fact
    about git, not written on the card, with four stages a report names:
    `written`, `committed`, `in a pull request`, `merged`; the word "saved"
    alone is never the report. Mirrored is the card's `mirrors` line. `not-recorded` is written with a hyphen so every
    value is one word; it is for a recipe brought in from elsewhere that was
    cooked with no log. Only the cook sets `house` (which needs a logged
    cook) and `retired`. A new card is `reviewed` when nothing is open, the
    cook approved the text, and the recipe was checked for coherence, which
    the cook's word or a `chef-council` hand-off with every Ready to save
    line at `yes` shows; otherwise it is `draft`.
11. **Evidence counts logs.** Kitchen evidence counts the logs in
    `cook-logs/<slug>/` for the recipe as the card now states it: none is
    `untested`, one is `cooked-once`, two or more is `repeated`. A cook
    counts once it has a log, so a reported cook is logged first. The count
    is the logs whose Recipe line names the card's current version; a cook
    that departed from the card counts, and its log says how. A new version
    does not inherit the old one's evidence: a log of an earlier version, or
    a log written before the dish had a card, counts only when the changelog
    line for the current version names it as the cook the change came from.
    `not-recorded` is used only when the cook says the recipe has been
    cooked and cannot give a day or a report to log.
12. **Versions.** `vX.Y` from `v1.0`; the minor number counts up without
    rolling over (`v1.9` then `v1.10`). The decision table is the design
    report's (§3 item 4) with each row made exact and one row added:
    wording, layout, or a typo with nothing a cook would do differently is
    the same version; a quantity, time, temperature, ingredient, step,
    yield, source credit, or a note a cook relies on is one minor version up
    with a changelog line; a changed technique, cut, or appliance, or a
    variant to test beside the original, is a new card, and the original
    stays; a change of status or evidence alone keeps the version and adds a
    changelog line (the added row); promotion to `house` is the cook's alone
    and needs a logged cook. A second-version card takes the original's slug
    with `-v2` and starts at `v2.0`; the next takes `-v3` and `v3.0`, always
    the next unused number added to the original's slug, never to another
    variant's. A title whose own slug happens to end in `-v` and a digit is
    not treated specially; no card in sight has one. The cook sets the scope of a save
    (design §2), so when the cook's instruction and the table disagree, the
    skill says what the table would do and follows the cook.
13. **When sources disagree.** The order, generalized from the same private
    file: the cook's latest explicit instruction; the standing corrections
    in `kitchen/profile.md`; the saved card on the default branch; the cook
    logs, which are evidence and do not change a card; then copies outside
    the repository, uploaded snapshots, and an agent's memory of an earlier
    conversation, none of which is a source for a missing quantity.
    Food-safety standards and equipment-manual limits are constraints on
    every entry, not entries. The page's one worked example is invented.
14. **Names and places.** A card is `recipes/<category>/<slug>.md`. One
    rule makes a slug, stated once in the method page and referred to by
    both skills: the title in lowercase, each accented letter written
    without its accent, every run of characters other than `a` to `z` and
    the digits turned into one hyphen, and no hyphen at the start or the
    end. A category name is made the same way from the name the cook
    chooses. No two cards share a slug, whatever their categories, and the
    skill looks at the card files themselves to check, not only at the
    index; that lets a cook log live at
    `cook-logs/<slug>/<YYYY-MM-DD>.md` and a source packet at
    `.sources/<slug>/<YYYY-MM-DD>.md` with no category in the path. A log is
    named for the day of the cook, a packet for the day it is written, and a
    second one for the same slug on the same day ends in `-2`. This spec
    states the uniqueness rule in the method page and the skill; enforcing
    it is T011's linter (the ticket lists unique slugs there), and
    `scripts/build-index.py` does not check it. There is no fixed list of
    categories.
15. **The source packet.** Four lines at the top (Card, Kind of save, Date,
    Where the approved text came from) and the four parts the ticket names
    as `##` headings: Approved text, Scope instruction, Previous version,
    Paths. The rule is the ticket's, word for word: paste the approved text
    verbatim; never summarize. Each pasted part sits between two lines of
    four tildes, because approved text can hold its own `##` headings (the
    hand-off of the `chef-council` skill does) and code fences; text that
    itself holds a line of four or more tildes gets longer tilde lines. A
    new card's Previous version is the line `None: this is a new card.` For
    an update or a variant it is the card as `git show main:<path>` prints
    it, with the commit `git rev-parse main` prints named on a line above
    the tildes; when the card is not on the default branch or git cannot be
    run, the file as it stands is pasted and the packet says which. A filled
    packet keeps the title, the four top lines, the four headings, and the
    tilde lines, and none of the template's sentences of instruction. `.gitignore`
    already ignores `.sources/` (S001). The skill writes the packet before
    the card and writes the card from the packet.
16. **The cook log.** Three lines at the top (Date cooked, Recipe,
    Reported) and four `##` headings: What the cook reported, Inference,
    Next controlled change, Card follow-up. Under the first are ten labeled
    lines, in a fixed order, and a filled log keeps the title, the three
    top lines, the headings, and the labels, and none of the template's
    sentences of instruction. Reported is the day the cook told the writer,
    which is today unless the cook says otherwise. The labels are
    generalized from
    `private-sources/cooking/templates/cook-log.md` with its personal fields
    dropped. Each holds the cook's own words inside straight double
    quotation marks, or `Not reported.` and nothing else. A quotation is an
    exact, unbroken piece of what the cook wrote, which is what makes the
    ticket's done-condition checkable by a command: every quoted span must
    occur in the cook's message. What the writer concluded goes under
    Inference, each line starting `Inference:`. Next controlled change holds
    one change on one line: the cook's words in quotation marks and nothing
    else when it is the cook's idea, or a line starting `Proposed:` when it
    is not. Advice on how to run the change goes in the reply, not the
    log. The Recipe line gives the card's path in a code span and
    not as a link, so the template holds no link to a file that does not
    exist.
17. **One writer of cards.** The `cook-log` skill never changes a card. Its
    Card follow-up section says what the card needs (the new evidence value,
    and each change the cook asked for, quoted), and the change is made
    through `recipe-codify`, so every card change takes one path to the
    editor check. The `cook-log` skill writes the log from what was reported
    without stopping to ask for more, lists what was not reported in its
    reply, and does not commit in the same turn. A log names no one: when
    the cook's words name a person or give a health detail, the skill quotes
    the part that leaves it out or asks first, because a public fork
    publishes its logs (T005).
18. **Codify's order of work.** Source packet, card, index, hand-off to the
    editor, then the save. The `recipe-editor` skill is T011's and does not
    exist yet, so `recipe-codify` refers to "the recipe-editor skill listed
    under Skills in `AGENTS.md`" and, when none is listed or no second agent
    can be started, says the check has not been run and never certifies its
    own card. S003 used the same forward reference for `recipe-codify`
    itself. Until a check passes the skill does not commit the card, open a
    pull request, or copy the card outside the repository. When the check
    cannot be run, that decision is the cook's: if the cook then says to
    save anyway, the skill saves by the same steps and says in the commit
    message and the pull request that the editor check was not run. It never
    saves after a failed check.
19. **The save.** The ticket's evidence says: never push `main`; hand off to
    the editor; a pull request, or a direct commit when working alone. This
    spec reads the last clause as follows. The default is a branch and a
    pull request that the cook merges; the branch is the one the cook
    names, or one the skill creates and names for the card, such as
    `card/roasted-carrots`. When the cook works alone and asks
    for no pull request, the skill commits on the branch the cook names and
    stops, and the cook pushes. In neither case does the skill push `main`.
    A card is copied to a notes app only when the cook asks or calls the
    recipe final, and `mirrors` stays `none` until a copy was written and
    read back; the adapters that do it are T013's.
20. **Fixed reply shapes.** `recipe-codify` replies under `## Files
    written`, `## Status`, `## Editor check`, and `## Next step`; `cook-log` replies under
    `## Logged`, `## Not reported`, `## Next controlled change`, and `##
    Card follow-up`. With no file access each returns the complete files
    with their paths and says nothing was saved (`AGENTS.md`).
21. **The index generator** is `scripts/build-index.py` (Python 3 standard
    library, mode 100644 like the other Python scripts), run as `python3
    scripts/build-index.py [--check] [repository-root]`; the root defaults
    to the script's own repository, and `--check` may come before or after
    it.
    - A card is every file `recipes/<category>/<name>.md` where neither the
      folder nor the file name starts with a dot. A symbolic link to a
      folder or to a file is followed and counts like what it points to. The slug is
      the file name without `.md`. Files directly in `recipes/`, files more
      than one folder down, and files without the `.md` ending are not
      cards. A missing `recipes/` folder is zero cards.
    - A card is read as UTF-8 and split into lines at any line ending. If
      its first line is `---`, the lines up to the next `---` line are front
      matter: each one that matches `key: value` in full, with a key of
      lowercase letters and underscores, sets that key to the value with
      surrounding white space removed, the first occurrence winning, and
      every other line is ignored. The title is the first line after the
      front matter that starts with `# ` and has text after it, with
      surrounding white space removed.
    - Three problems are reported, each as `recipes/<category>/<slug>.md:
      <problem>` on standard output: `is not UTF-8 text`, `front matter is
      not closed` (a first line `---` with no later `---` line), and `has no
      title line`. With any problem the script prints every problem line in
      card order, writes nothing, and exits 1, with or without `--check`.
    - The index is the heading `# Recipe index`, a blank line, one paragraph
      (given exactly in the script's `HEADER`), a blank line, and then
      either the line `No recipe cards yet.` or a table with the header `|
      Recipe | Category | Version | Status | Kitchen evidence |` and one row
      per card, ordered by category and then by slug, comparing the strings
      themselves (so `rice` sorts before `rice-pilaf`). A row is `|
      [<title>](<category>/<slug>.md) | <category> | <version> | <status> |
      <evidence> |`. The category and the slug come from the path; the
      front matter's `id` and `category` lines are not read. `version`,
      `status`, and `evidence` come from the front matter, and a missing or
      empty one is written `not stated`. A `|` in a title, a category, or a
      value is written `\|`. The index holds no date, so it changes only
      when a card does.
    - Without `--check` the script writes `recipes/INDEX.md` (creating
      `recipes/` when it is missing), with line feeds, prints `index
      written: <N>`, and exits 0. With `--check` it writes nothing: it
      prints `index current: <N>` and exits 0 when the file's bytes equal
      what would be written, prints `recipes/INDEX.md is stale: run python3
      scripts/build-index.py` and exits 1 when they differ, and prints
      `recipes/INDEX.md is missing: run python3 scripts/build-index.py` and
      exits 1 when there is no file. `<N>` is the number of cards.
    - More than one path, a second `--check`, or any other argument that
      starts with `-` prints `usage: build-index.py [--check]
      [repository-root]` on standard error and exits 2. A root that is not a
      directory prints `build-index: <root> is not a directory` on standard
      error and exits 2.
    - The script writes the category and the file name into the link as
      they are and does not encode them; names made by decision 14's rule
      need no encoding, and a name that breaks the link is the linter's to
      report.
    - Only the three problems above are handled. A card that cannot be
      opened, a `recipes` that is a file, or an `INDEX.md` that cannot be
      written ends in Python's traceback and a non-zero exit, which still
      fails the check (S001's decision 10 took the same position).
    - The script does not judge a card: whether a status is a known value,
      whether the front matter agrees with the lines under the title,
      whether `id` equals the slug, and whether slugs are unique are the
      linter's checks (T011).
22. **`recipes/INDEX.md` ships now, generated from zero cards**, so `--check`
    passes from this spec's merge and T012 regenerates it with the example
    cards. The test `test_this_repository_index_is_current` runs `--check`
    on the repository itself, inside the `Run the tests` step CI already
    has, so a stale index fails CI with no change to
    `.github/workflows/ci.yml`. The profile's check list already holds the
    unit-test command, so `.agents/spec-profile.md` is not changed either.
    T011's linter runs `--check` as well, as its ticket says.
23. **`AGENTS.md`** gets four changed lines and stays under the design
    report's 8 KB limit at 7,748 bytes: item 4 of the read order now links
    `recipes/INDEX.md` and names `cook-logs/`; the status rule now links
    `method/status-and-versions.md`; and the two skills get their index
    lines after the `chef-council` line (the map requires each skill ticket
    to add its own). S001's decision 3 left each later ticket to add its own
    paths.
24. **Tests.** `tests/test_build_index.py` observes the script only through
    its standard output, standard error, exit status, and the
    `recipes/INDEX.md` it writes, on temporary directories the tests build.
    Every expected index is a literal in the test file, written from
    decision 21, and none is computed the way the script computes it.
25. **Behavior checks.** The real-artifact observation for a skill is a
    fresh subagent following it (profile). Each of the two checks runs in
    its own scratch repository made from the pushed branch with its `origin`
    remote removed, so a subagent that tried to push could reach nothing.
    The recipe in the fixtures is this spec's own, written for the purpose:
    it adapts no publisher's recipe and holds no safety number. The fixture
    card is not shipped in the repository; the example cards are T012's. The
    checks cover a new card and one cook log. An update to a saved card, a
    new variant, and a commit after a passing editor check are not exercised
    here, because the editor does not exist until T011.
26. **Private sources.** Leg 1 read `private-sources/design/design-report.md`
    (§2, §3, §4, §6), `private-sources/cooking/templates/recipe-card.md`,
    `private-sources/cooking/templates/cook-log.md`,
    `private-sources/cooking/context/publishing-workflow.md`,
    `private-sources/cooking/context/recipe-qc.md`, and the opening of
    `private-sources/cooking/context/recipe-index.md`, and generalized from
    them under the ledger's rows (§4: keep and generalize the two templates;
    generalize the publishing workflow into the status page). The section
    names of the card and the idea of each cook-log field are kept; the
    maintainer's name, the notes-app fields, the named-feedback fields, the
    household examples, and the private repository's identity are dropped.
    The executor opens nothing under `private-sources/`.
27. **`README.md`, CI, and the profile are not touched.** T014 writes the
    README; T011 adds the gate and the linter to CI.

## Prerequisites

- Leg 2 starts from this spec's approval commit on
  `workstream/t010-codify-and-cook-log`, which already holds the claim
  commit for T010. Staging, the per-task commit with its `Spec-Task:
  S004/<N>` trailer, the push, the pull request, and the base-drift check
  are the `2-spec-execute` skill's standing procedure and the profile's
  ship tail. Each task's commit holds exactly that task's Touches.
- The executor's machine has Git, Bash, Python 3, GNU coreutils
  (`sha256sum`, `readlink`), and an authenticated `gh`. It is Linux x86_64,
  where `scripts/secret-scan.sh` fetches its pinned gitleaks, or
  `GITLEAKS_BIN` names an installed gitleaks of the pinned version
  (profile). `git
  config user.email` ends in `@users.noreply.github.com` (profile). `git
  config core.symlinks` does not print `false`.
- The behavior subagents need to read and write files inside one directory
  and to run `python3` there. They need no web access and are told not to
  use it.
- No one opens anything under `private-sources/` for this spec (decision
  26).
- `test -x "$(git rev-parse --git-common-dir)/info/privacy-sweep"` succeeds.
  `WAYFINDER` is set to the directory the harness prints when the wayfinder
  skill loads, and `test -f "$WAYFINDER/scripts/lint.py"` succeeds (profile).
  If either is missing,
  report ``Question: <the privacy sweep | the Wayfinder lint> that the
  profile requires is not on this machine; provide it?`` and stop.

### Writing a file from this spec

Each file under `## File contents` and each fixture under `### Behavior
checks` is the text inside the fenced block that follows its `#### File:`
or `#### Fixture:` heading: every line between the opening and closing
fence, each ended by a line feed, with nothing added or removed. `block`
prints one such block, and `extract` writes one file from it; the executor
may use them. `SPEC` is set in the setup of `## Build plan — agent loop`.

```bash
block() {
  python3 - "$SPEC" "$1" <<'PY'
import sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index(sys.argv[2])
opening = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("````"))
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "````")
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
}
extract() {
  mkdir -p "$(dirname "$1")"
  block "#### File: \`$1\`" > "$1"
}
```

Usage: `extract templates/recipe-card.md`; the setup of `### Behavior
checks` shows `block` writing a fixture. The SHA-256 gates decide whether a
file is right, whichever way it was written.

### Link check

A gate helper, not a repository file (the helper of S002 and S003,
unchanged), loaded as the setup of `## Build plan — agent loop` says. It reads the Markdown files named on its command line, skips
fenced code blocks, and requires the target of every inline link
`[text](target)` with a relative target to be a path git tracks or has
staged. A target that starts with `#` or a scheme is skipped. It prints one
line per broken link and returns 1, or prints nothing and returns 0.

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

### Behavior checks

The real-artifact observation for the two skills (profile, agent behavior;
decision 25). The orchestrator runs them after the push and the pull
request, from the repository root of the work branch, in the shell of `##
Build plan — agent loop`.

**Setup.** Two scratch repositories under one temporary directory, each a
fresh clone of the pushed branch with no remote, and the three fixtures:

```bash
FIX=$(mktemp -d)
for name in codify log; do
  git clone --quiet --branch workstream/t010-codify-and-cook-log "$(git remote get-url origin)" "$FIX/$name"
  git -C "$FIX/$name" remote remove origin
done
git -C "$FIX/codify" tag fixture-start
block '#### Fixture: `log-message`' > "$FIX/log-message.txt"
mkdir -p "$FIX/log/recipes/sides"
block '#### Fixture: `card`' > "$FIX/log/recipes/sides/skillet-green-beans-with-lemon-and-garlic.md"
python3 "$FIX/log/scripts/build-index.py" "$FIX/log"
git -C "$FIX/log" add recipes
git -C "$FIX/log" -c user.name=fixture -c user.email=fixture@example.invalid commit --quiet -m "Add the fixture card"
git -C "$FIX/log" tag fixture-start
```

The `build-index.py` line prints `index written: 1`. The fixture commit
exists only in the scratch repository `$FIX/log`, which has no remote.

The `codify` message carries today's date, so write it immediately before
starting that check's subagent:

```bash
block '#### Fixture: `codify-message`' | sed "s/<today>/$(date +%F)/" > "$FIX/codify-message.txt"
```

If the date changes before the subagent replies, that run is void: make the
scratch repository and the message again and start a new subagent. A void
run is not a failed check.

**The brief.** Each check starts one fresh subagent at the orchestrator
tier through the harness's agent tool, briefed with exactly the brief below
and nothing else, with `<dir>` replaced by the absolute path of the check's
scratch repository (`$FIX/codify` or `$FIX/log`) and `<message>` by the
content of the check's message file (`$FIX/codify-message.txt` or
`$FIX/log-message.txt`). The two subagents may run at the same time. The
orchestrator saves each reply, exactly as returned, to
`$FIX/codify-reply.md` or `$FIX/log-reply.md`.

```text
You are an AI cooking assistant working in the repository at <dir> . Read AGENTS.md in that directory and follow it, including the files and the skill it points to. Read and write only files inside that directory, and do not use the web. Reply to the cook's message below, and return only your reply to the cook, exactly as you would send it, with nothing before or after it.

The cook says:

<message>
```

**The two checks.**

1. **`codify`.** Passes when `codifycheck "$FIX/codify"
   "$FIX/codify-message.txt" "$FIX/codify-reply.md"; echo $?` prints
   `codify check ok: recipes/sides/<slug>.md` (with the slug the subagent
   chose) then `0`, and the orchestrator, reading the card beside the
   fixture, answers yes to both: the card's Method holds the fixture's four
   steps in the fixture's order with nothing added or left out that changes
   what gets cooked; and nothing in the reply says the card was checked,
   verified, or approved by an editor.

   What `codifycheck` proves, in order: exactly one card exists, under
   `recipes/sides/`, with a lowercase hyphenated slug; its front matter is
   plain `key: value` lines giving `id` as the slug, `version: v1.0`,
   `status: reviewed`, `evidence: untested`, `category: sides`, and
   `mirrors` absent or `none`, in that order and each once; the title line and the Version, Status,
   Kitchen evidence, and Source lines under it agree (the Source is
   `Original.`); the ten `##` headings are present in order and no other;
   Failure modes, Variations, Notes, and Next experiment are exactly `None
   recorded.`, since the fixture says nothing for them, while Why this
   works and Storage carry the fixture's lines; no template text and no
   `Not stated.` remains; the Ingredients table holds eight rows, each
   pairing a fixture ingredient with its amount; Equipment holds the
   skillet; Method holds four numbered steps and the fixture's three times;
   the Yield and Time lines hold the fixture's figures; the Changelog has a
   `v1.0` line with the date; no number appears in Equipment,
   Ingredients, Method, Yield, or Time that the cook's message does not
   hold (a converted unit would fail here); `python3 scripts/build-index.py
   --check` prints `index current: 1` and the index holds the card's row;
   exactly one source packet exists, at
   `.sources/<slug>/<YYYY-MM-DD>.md` with the date the message gave, which
   is also the card's Date; the packet has its four headings and no others
   outside the tilde lines; between the tilde lines under Approved text sits
   the whole of the message after its first paragraph, unbroken and in
   order; between the tilde lines under Scope instruction sits the cook's
   scope sentence; the packet holds `None: this is a new card.`, the card's
   path, and no template text, and git ignores it; `git status` shows only the new card
   and the changed index, and no commit was made; and the reply has the
   four headings of decision 20, names the card's path under Files written,
   and
   opens its Editor check section with `Not run` and gives the packet's
   path there.

2. **`log`.** Passes when `logcheck "$FIX/log" "$FIX/log-message.txt"
   "$FIX/log-reply.md"; echo $?` prints `log check ok:
   cook-logs/skillet-green-beans-with-lemon-and-garlic/2026-11-17.md` then
   `0`, and the orchestrator, reading the log, answers yes to this: no line
   under `## What the cook reported` states a cause, a judgment, or a fact
   that the cook's message does not state.

   What `logcheck` proves, in order: exactly one log exists, at the path
   the date of the cook gives; it has the title, the four headings of
   decision 16, the Date cooked line, a Reported line holding one date, and
   a Recipe line naming `v1.0` and the card's path, and no template text; the ten labels are present in order, and every
   line under them is `Not reported.` or nothing but quotations, each of
   which occurs in the cook's message (typographic quotation marks and runs
   of white space are folded before comparing); the four things the message
   never mentions (equipment, times, doneness checks, storage) are `Not
   reported.`, although the fixture card states an equipment item and
   three times, which is the trap; the three things it does mention are
   quoted under their own labels (the weight of beans under Main ingredient,
   the oil under Changes from the card, the soft beans under Taste and
   texture), while Yield and portions, Verdict, and Problems and rescues are
   left to the writer's reading; no line under the first heading or under
   Card follow-up is anything but a labeled item; every Inference line starts with `Inference:`, or the section is
   `None.`; Next controlled change is one line that quotes the cook's own
   idea about the lemon; Card follow-up gives the evidence change from
   `untested` to `cooked-once` and, for the changes the cook asked for, either `None
   requested.` or the cook's words; `git status` shows only the new log, so
   the card is untouched, and no commit was made; and the reply has the
   four headings of decision 20, names the log's path under Logged, and
   names `recipe-codify` under Card follow-up.

A check that fails is not repaired by editing the scratch repository or the
reply. The orchestrator makes a new scratch repository as the setup says and
starts a new fresh subagent, once. A second failure of the same check is
reported as ``Question: the <codify | log> behavior check of
`docs/specs/S004-codify-and-cook-log.md` failed twice: <the check's
output>; revise the spec?`` The skill files are not edited to make a check
pass.

Leg 1 rehearsed both checks on 2026-11-19 with fresh orchestrator-tier
subagents briefed exactly as above, on files built in a scratch clone at
`base_sha` (L003). There were three rounds, and the record is given whole:

- **First draft.** Both checks passed on their first run, against the first
  draft's helpers.
- **After the cross-examination edits.** `codify` passed: `codifycheck`
  printed `codify check ok:
  recipes/sides/skillet-green-beans-with-lemon-and-garlic.md`. The reply
  opened its Editor check section with `Not run.` where the skill's text
  shows `Not run:`, so the helper accepts either. `log` failed: under Next
  controlled change the writer put its own advice on the same line as the
  cook's quotation, which the helper, stricter since finding 5, rejects.
  Leg 1 read that as a gap in the skill's wording, not a bad run, and
  changed the `cook-log` skill and template to say that the line holds the
  cook's words and nothing else, with advice going in the reply.
- **Final bytes.** A new fresh subagent ran `log` on the files this spec
  gives, and `logcheck` printed `log check ok:
  cook-logs/skillet-green-beans-with-lemon-and-garlic/2026-11-17.md`. The
  passing `codify` run was made on files that differ from the final ones
  only in `.agents/skills/cook-log/SKILL.md` and `templates/cook-log.md`,
  which the `codify` check does not read; it was not run again.

Leg 1 answered yes to the three reading questions on the passing runs. Each
check has now passed once on its final wording; one run is a sample, which
is why a failed check in leg 2 gets one more fresh run before it is a
question.

#### Fixture: `codify-message`' | sed "s/<today>/$(date +%F)/" > "$FIX/codify-message.txt"
```

If the date changes before the subagent replies, that run is void: make the
scratch repository and the message again and start a new subagent. A void
run is not a failed check.

**The brief.** Each check starts one fresh subagent at the orchestrator
tier through the harness's agent tool, briefed with exactly the brief below
and nothing else, with `<dir>` replaced by the absolute path of the check's
scratch repository (`$FIX/codify` or `$FIX/log`) and `<message>` by the
content of the check's message file (`$FIX/codify-message.txt` or
`$FIX/log-message.txt`). The two subagents may run at the same time. The
orchestrator saves each reply, exactly as returned, to
`$FIX/codify-reply.md` or `$FIX/log-reply.md`.

```text
You are an AI cooking assistant working in the repository at <dir> . Read AGENTS.md in that directory and follow it, including the files and the skill it points to. Read and write only files inside that directory, and do not use the web. Reply to the cook's message below, and return only your reply to the cook, exactly as you would send it, with nothing before or after it.

The cook says:

<message>
```

**The two checks.**

1. **`codify`.** Passes when `codifycheck "$FIX/codify"
   "$FIX/codify-message.txt" "$FIX/codify-reply.md"; echo $?` prints
   `codify check ok: recipes/sides/<slug>.md` (with the slug the subagent
   chose) then `0`, and the orchestrator, reading the card beside the
   fixture, answers yes to both: the card's Method holds the fixture's four
   steps in the fixture's order with nothing added or left out that changes
   what gets cooked; and nothing in the reply says the card was checked,
   verified, or approved by an editor.

   What `codifycheck` proves, in order: exactly one card exists, under
   `recipes/sides/`, with a lowercase hyphenated slug; its front matter is
   plain `key: value` lines giving `id` as the slug, `version: v1.0`,
   `status: reviewed`, `evidence: untested`, `category: sides`, and
   `mirrors` absent or `none`, in that order and each once; the title line and the Version, Status,
   Kitchen evidence, and Source lines under it agree (the Source is
   `Original.`); the ten `##` headings are present in order and no other;
   Failure modes, Variations, Notes, and Next experiment are exactly `None
   recorded.`, since the fixture says nothing for them, while Why this
   works and Storage carry the fixture's lines; no template text and no
   `Not stated.` remains; the Ingredients table holds eight rows, each
   pairing a fixture ingredient with its amount; Equipment holds the
   skillet; Method holds four numbered steps and the fixture's three times;
   the Yield and Time lines hold the fixture's figures; the Changelog has a
   `v1.0` line with the date; no number appears in Equipment,
   Ingredients, Method, Yield, or Time that the cook's message does not
   hold (a converted unit would fail here); `python3 scripts/build-index.py
   --check` prints `index current: 1` and the index holds the card's row;
   exactly one source packet exists, at
   `.sources/<slug>/<YYYY-MM-DD>.md` with the date the message gave, which
   is also the card's Date; the packet has its four headings and no others
   outside the tilde lines; between the tilde lines under Approved text sits
   the whole of the message after its first paragraph, unbroken and in
   order; between the tilde lines under Scope instruction sits the cook's
   scope sentence; the packet holds `None: this is a new card.`, the card's
   path, and no template text, and git ignores it; `git status` shows only the new card
   and the changed index, and no commit was made; and the reply has the
   four headings of decision 20, names the card's path under Files written,
   and
   opens its Editor check section with `Not run` and gives the packet's
   path there.

2. **`log`.** Passes when `logcheck "$FIX/log" "$FIX/log-message.txt"
   "$FIX/log-reply.md"; echo $?` prints `log check ok:
   cook-logs/skillet-green-beans-with-lemon-and-garlic/2026-11-17.md` then
   `0`, and the orchestrator, reading the log, answers yes to this: no line
   under `## What the cook reported` states a cause, a judgment, or a fact
   that the cook's message does not state.

   What `logcheck` proves, in order: exactly one log exists, at the path
   the date of the cook gives; it has the title, the four headings of
   decision 16, the Date cooked line, a Reported line holding one date, and
   a Recipe line naming `v1.0` and the card's path, and no template text; the ten labels are present in order, and every
   line under them is `Not reported.` or nothing but quotations, each of
   which occurs in the cook's message (typographic quotation marks and runs
   of white space are folded before comparing); the four things the message
   never mentions (equipment, times, doneness checks, storage) are `Not
   reported.`, although the fixture card states an equipment item and
   three times, which is the trap; the three things it does mention are
   quoted under their own labels (the weight of beans under Main ingredient,
   the oil under Changes from the card, the soft beans under Taste and
   texture), while Yield and portions, Verdict, and Problems and rescues are
   left to the writer's reading; no line under the first heading or under
   Card follow-up is anything but a labeled item; every Inference line starts with `Inference:`, or the section is
   `None.`; Next controlled change is one line that quotes the cook's own
   idea about the lemon; Card follow-up gives the evidence change from
   `untested` to `cooked-once` and, for the changes the cook asked for, either `None
   requested.` or the cook's words; `git status` shows only the new log, so
   the card is untouched, and no commit was made; and the reply has the
   four headings of decision 20, names the log's path under Logged, and
   names `recipe-codify` under Card follow-up.

A check that fails is not repaired by editing the scratch repository or the
reply. The orchestrator makes a new scratch repository as the setup says and
starts a new fresh subagent, once. A second failure of the same check is
reported as ``Question: the <codify | log> behavior check of
`docs/specs/S004-codify-and-cook-log.md` failed twice: <the check's
output>; revise the spec?`` The skill files are not edited to make a check
pass.

Leg 1 rehearsed both checks on 2026-11-19 on the files this spec gives,
built in a scratch clone at `base_sha`, with fresh orchestrator-tier
subagents briefed exactly as above (L003). Both passed on their first run:
`codifycheck` printed `codify check ok:
recipes/sides/skillet-green-beans-with-lemon-and-garlic.md` and `logcheck`
printed `log check ok:
cook-logs/skillet-green-beans-with-lemon-and-garlic/2026-11-17.md`, and
leg 1 answered yes to the three reading questions.

#### Fixture: `codify-message`

````text
The council pressure-tested this one with me and I approved the final text below. Save it as a new card in sides. I have not cooked it yet. Today is <today>.

Skillet Green Beans with Lemon and Garlic (serves 2 as a side)

Equipment: 12-inch skillet with a lid.

Ingredients: 12 oz green beans, trimmed; 1 tbsp olive oil; 1/4 tsp kosher salt; 2 tbsp water; 2 cloves garlic, thinly sliced; 1 tbsp unsalted butter; 2 tsp lemon juice; black pepper to taste.

Method: 1. Heat the oil in the skillet over medium-high heat until it shimmers. Add the beans and the salt and cook, stirring once or twice, until blistered in spots, about 4 minutes. 2. Add the water, cover, and steam until the beans are bright green and crisp-tender, about 2 minutes. 3. Uncover, lower the heat to medium, add the garlic and the butter, and cook, stirring, until the garlic is fragrant and pale gold, about 1 minute. 4. Off the heat, stir in the lemon juice. Season with pepper, taste, and serve.

Time: about 15 minutes.

Why it works: the garlic goes in after the steam so it cannot scorch while the beans blister, and the lemon juice goes in off the heat so it stays bright.

Storage: refrigerate leftovers in a covered container and reheat them in a hot skillet.
````

#### Fixture: `log-message`

````text
I made the skillet green beans with lemon and garlic on November 17, 2026. I only had 10 oz of beans, so I used those and kept everything else the same. I was out of butter and used another tablespoon of olive oil instead. The beans were a little soft for me, but the garlic was perfect, not bitter at all. We ate all of it at dinner. Next time I want to try it with a squeeze more lemon. Log it.
````

#### Fixture: `card`

````markdown
---
id: skillet-green-beans-with-lemon-and-garlic
version: v1.0
status: reviewed
evidence: untested
category: sides
mirrors: none
---

# Skillet Green Beans with Lemon and Garlic

- **Version:** v1.0
- **Date:** 2026-11-10
- **Status:** reviewed
- **Kitchen evidence:** untested
- **Source:** Original.
- **Yield:** Serves 2 as a side
- **Time:** About 15 minutes

## Equipment

- 12-inch skillet with a lid

## Ingredients

| Amount | Ingredient | Prep |
|---|---|---|
| 12 oz | Green beans | Trimmed |
| 1 tbsp | Olive oil | None |
| 1/4 tsp | Kosher salt | None |
| 2 tbsp | Water | None |
| 2 cloves | Garlic | Thinly sliced |
| 1 tbsp | Unsalted butter | None |
| 2 tsp | Lemon juice | None |
| To taste | Black pepper | None |

## Method

1. **Blister.** Heat the oil in the skillet over medium-high heat until it shimmers. Add the beans and the salt and cook, stirring once or twice, until blistered in spots, about 4 minutes.
2. **Steam.** Add the water, cover, and steam until the beans are bright green and crisp-tender, about 2 minutes.
3. **Add the garlic.** Uncover, lower the heat to medium, add the garlic and the butter, and cook, stirring, until the garlic is fragrant and pale gold, about 1 minute.
4. **Finish.** Off the heat, stir in the lemon juice. Season with pepper, taste, and serve.

## Why this works

- **Garlic after the steam.** The garlic goes in after the steam so it cannot scorch while the beans blister.
- **Lemon off the heat.** The lemon juice goes in off the heat so it stays bright.

## Failure modes

None recorded.

## Variations

None recorded.

## Storage

- Refrigerate leftovers in a covered container and reheat them in a hot skillet.

## Notes

None recorded.

## Next experiment

None recorded.

## Changelog

- v1.0 (2026-11-10): First card. Not yet cooked.
````

#### Helper: `codifycheck`

A gate helper, not a repository file.

````bash
codifycheck() {
  python3 - "$@" <<'PY'
import glob, os, re, subprocess, sys
root, message_path, reply_path = sys.argv[1:4]
bad = []
def fail(text):
    bad.append(text)
def read(path):
    return open(path, encoding="utf-8").read()
def git(*args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True).stdout
def sections(text):
    """Map each ## heading outside a fenced block to its body, and return the headings in order."""
    found, order, name, fence = {}, [], None, None
    for line in text.split("\n"):
        mark = re.match(r"(~{3,}|`{3,})", line)
        if fence is None and mark:
            fence = mark.group(1)
        elif fence is not None and line.strip() == fence:
            fence = None
        if fence is None and not mark and line.startswith("## "):
            name = line[3:].strip()
            order.append(name)
            found[name] = []
        elif name is not None:
            found[name].append(line)
    return {key: "\n".join(value).strip() for key, value in found.items()}, order
def fenced(text):
    """Return the text between the first pair of tilde lines, or None."""
    lines = text.split("\n")
    for start, line in enumerate(lines):
        if re.fullmatch(r"~{4,}", line):
            for end in range(start + 1, len(lines)):
                if lines[end] == line:
                    return "\n".join(lines[start + 1:end])
    return None
def numbers(text):
    text = re.sub(r"(?m)^\s*\d+\.\s", "", text)
    return set(re.findall(r"\d+(?:/\d+)?", text))
message = read(message_path)
reply = read(reply_path)
TITLE = "Skillet Green Beans with Lemon and Garlic"
HEADINGS = ["Equipment", "Ingredients", "Method", "Why this works", "Failure modes",
            "Variations", "Storage", "Notes", "Next experiment", "Changelog"]

# 1. One card, in sides, with a slug.
cards = sorted(path for path in glob.glob(os.path.join(root, "recipes", "*", "*.md")))
slug = None
if len(cards) != 1 or os.path.basename(os.path.dirname(cards[0])) != "sides":
    fail("expected exactly one card, under recipes/sides/")
else:
    slug = os.path.basename(cards[0])[:-3]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        fail("the card's file name is not a lowercase hyphenated slug")
if bad:
    print("\n".join(bad)); sys.exit(1)
card_path = "recipes/sides/%s.md" % slug
card = read(cards[0])
lines = card.split("\n")

# 2. The block at the top.
fields = {}
if lines[0] == "---" and "---" in lines[1:]:
    end = lines.index("---", 1)
    keys = []
    for line in lines[1:end]:
        match = re.fullmatch(r"([a-z_]+): (.*\S)", line)
        if match:
            keys.append(match.group(1))
            fields[match.group(1)] = match.group(2)
        else:
            fail("front matter line is not a plain key: value line: %s" % line)
    if keys not in (["id", "version", "status", "evidence", "category", "mirrors"],
                    ["id", "version", "status", "evidence", "category"]):
        fail("front matter keys are %s" % keys)
    body = "\n".join(lines[end + 1:])
else:
    fail("the card has no front matter")
    body = card
want = {"id": slug, "version": "v1.0", "status": "reviewed", "evidence": "untested", "category": "sides"}
for key, value in want.items():
    if fields.get(key) != value:
        fail("front matter %s is %s, expected %s" % (key, fields.get(key), value))
if fields.get("mirrors", "none") != "none":
    fail("front matter mirrors is not none")

# 3. The title and the lines under it.
if "# " + TITLE not in body.split("\n"):
    fail("the title line is not '# %s'" % TITLE)
packets = sorted(glob.glob(os.path.join(root, ".sources", "*", "*.md")))
date = os.path.basename(packets[0])[:-3] if len(packets) == 1 else None
for line in ["- **Version:** v1.0", "- **Status:** reviewed", "- **Kitchen evidence:** untested"]:
    if line not in body.split("\n"):
        fail("the card lacks the line: %s" % line)
if not any(re.fullmatch(r"- \*\*Source:\*\* Original\.?", line) for line in body.split("\n")):
    fail("the Source line is not Original.")

# 4. Headings, and nothing invented.
found, order = sections(body)
if order != HEADINGS:
    fail("the card's ## headings are %s" % order)
for name in ["Failure modes", "Variations", "Notes", "Next experiment"]:
    if found.get(name) != "None recorded.":
        fail("%s is not 'None recorded.'" % name)
if "garlic" not in found.get("Why this works", "") or "None recorded." in found.get("Why this works", ""):
    fail("Why this works does not carry the approved reason")
if "skillet" not in found.get("Storage", ""):
    fail("Storage does not carry the approved line")
for leftover in ["Copy this file", "YYYY-MM-DD", "Not stated.", "recipe-slug", "category-folder"]:
    if leftover in card:
        fail("the card still holds template text or an open blank: %s" % leftover)
for amount in ["12 oz", "1 tbsp", "1/4 tsp", "2 tbsp", "2 cloves", "2 tsp"]:
    if amount not in found.get("Ingredients", ""):
        fail("Ingredients lacks %s" % amount)
for time in ["4 minutes", "2 minutes", "1 minute"]:
    if time not in found.get("Method", ""):
        fail("Method lacks %s" % time)
rows = [line for line in found.get("Ingredients", "").split("\n") if line.startswith("|")]
for amount, ingredient in [("12 oz", "green beans"), ("1 tbsp", "olive oil"), ("1/4 tsp", "kosher salt"),
                           ("2 tbsp", "water"), ("2 cloves", "garlic"), ("1 tbsp", "unsalted butter"),
                           ("2 tsp", "lemon juice"), ("to taste", "black pepper")]:
    if not any(amount in row.lower() and ingredient in row.lower() for row in rows):
        fail("no Ingredients row pairs %s with %s" % (amount, ingredient))
if len(rows) != 10:
    fail("the Ingredients table holds %d lines, expected a header, a rule, and 8 rows" % len(rows))
if "12-inch skillet with a lid" not in found.get("Equipment", ""):
    fail("Equipment lacks the 12-inch skillet with a lid")
if len(re.findall(r"(?m)^\d+\. ", found.get("Method", ""))) != 4:
    fail("Method does not hold exactly four numbered steps")
for label, word in [("Yield", "2"), ("Time", "15 minutes")]:
    if not any(line.startswith("- **%s:**" % label) and word in line for line in body.split("\n")):
        fail("the %s line lacks %s" % (label, word))
core = "\n".join(found.get(name, "") for name in ["Equipment", "Ingredients", "Method"])
core += "\n".join(line for line in body.split("\n") if line.startswith(("- **Yield:**", "- **Time:**")))
extra = numbers(core) - numbers(message)
if extra:
    fail("numbers in the card that the approved text does not hold: %s" % sorted(extra))

# 5. The index.
result = subprocess.run([sys.executable, os.path.join(root, "scripts", "build-index.py"), "--check", root],
                        capture_output=True, text=True)
if result.stdout != "index current: 1\n" or result.returncode != 0:
    fail("build-index.py --check printed %r" % result.stdout)
row = "| [%s](sides/%s.md) | sides | v1.0 | reviewed | untested |" % (TITLE, slug)
if row not in read(os.path.join(root, "recipes", "INDEX.md")).split("\n"):
    fail("recipes/INDEX.md lacks the card's row")

# 6. The source packet.
packet_path = ".sources/%s/%s.md" % (slug, date)
if date is None or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) or not os.path.isfile(os.path.join(root, packet_path)):
    fail("expected exactly one packet, at .sources/%s/<YYYY-MM-DD>.md" % slug)
else:
    packet = read(os.path.join(root, packet_path))
    if date not in message:
        fail("the packet's date %s is not the date the cook gave" % date)
    if "- **Date:** %s" % date not in body.split("\n"):
        fail("the card's Date line is not %s" % date)
    if not any(re.fullmatch(r"- v1\.0 \(%s\): .+" % date, line) for line in found.get("Changelog", "").split("\n")):
        fail("the Changelog lacks a line starting '- v1.0 (%s): '" % date)
    approved = "\n".join(message.split("\n")[2:]).strip("\n")
    psections, porder = sections(packet)
    if porder != ["Approved text", "Scope instruction", "Previous version", "Paths"]:
        fail("the packet's ## headings are %s" % porder)
    pasted = fenced(psections.get("Approved text", ""))
    if pasted is None or approved not in pasted:
        fail("the approved text is not pasted whole and in order between tilde lines under Approved text")
    scope = fenced(psections.get("Scope instruction", ""))
    if scope is None or "Save it as a new card in sides." not in scope:
        fail("the cook's scope sentence is not between tilde lines under Scope instruction")
    if "None: this is a new card." not in psections.get("Previous version", ""):
        fail("the packet's Previous version is not 'None: this is a new card.'")
    if card_path not in psections.get("Paths", ""):
        fail("the packet's Paths lacks %s" % card_path)
    for leftover in ["Paste here.", "Copy this file", "YYYY-MM-DD", "recipe-slug"]:
        if leftover in packet:
            fail("the packet still holds template text: %s" % leftover)
    if subprocess.run(["git", "-C", root, "check-ignore", "-q", packet_path]).returncode != 0:
        fail("git does not ignore the packet")

# 7. Nothing committed, and nothing else written.
status = sorted(git("status", "--porcelain", "--untracked-files=all").splitlines())
if status != sorted([" M recipes/INDEX.md", "?? " + card_path]):
    fail("git status shows %s" % status)
if git("rev-parse", "HEAD") != git("rev-parse", "fixture-start"):
    fail("a commit was made")

# 8. The reply.
rsections, rorder = sections(reply)
if rorder != ["Files written", "Status", "Editor check", "Next step"]:
    fail("the reply's ## headings are %s" % rorder)
if card_path not in rsections.get("Files written", ""):
    fail("the reply's Files written section lacks the card's path")
check = rsections.get("Editor check", "")
if not check.startswith("Not run") or packet_path not in check:
    fail("the reply's Editor check section does not start with 'Not run' or lacks the packet's path")

if bad:
    print("\n".join(bad)); sys.exit(1)
print("codify check ok: %s" % card_path)
PY
}
````

#### Helper: `logcheck`

A gate helper, not a repository file.

````bash
logcheck() {
  python3 - "$@" <<'PY'
import glob, hashlib, os, re, subprocess, sys
root, message_path, reply_path = sys.argv[1:4]
bad = []
def fail(text):
    bad.append(text)
def read(path):
    return open(path, encoding="utf-8").read()
def git(*args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True).stdout
def plain(text):
    """Fold typographic quotation marks and runs of white space."""
    for mark in "‘’":
        text = text.replace(mark, "'")
    for mark in "“”":
        text = text.replace(mark, '"')
    return " ".join(text.split())
def sections(text):
    found, order, name = {}, [], None
    for line in text.split("\n"):
        if line.startswith("## "):
            name = line[3:].strip()
            order.append(name)
            found[name] = []
        elif name is not None:
            found[name].append(line)
    return {key: "\n".join(value).strip() for key, value in found.items()}, order
def quoted(value, where):
    """True when value is one or more quotations of the cook and nothing else."""
    value = plain(value)
    spans = re.findall(r'"([^"]*)"', value)
    rest = re.sub(r'"[^"]*"', "", value).strip()
    if not spans or rest:
        fail("%s holds words outside quotation marks: %s" % (where, value[:60]))
        return False
    for span in spans:
        if not span.strip() or span.strip() not in message:
            fail("%s quotes words the cook did not write: %s" % (where, span[:60]))
            return False
    return True
message = plain(read(message_path))
reply = read(reply_path)
SLUG = "skillet-green-beans-with-lemon-and-garlic"
LOG = "cook-logs/%s/2026-11-17.md" % SLUG
CARD = "recipes/sides/%s.md" % SLUG
LABELS = ["Main ingredient, weight and cut", "Changes from the card", "Equipment used", "Times",
          "Doneness checks and temperatures", "Yield and portions", "Taste and texture",
          "Verdict from the people who ate it", "Storage and reheating", "Problems and rescues"]
SILENT = ["Equipment used", "Times", "Doneness checks and temperatures", "Storage and reheating"]
SPOKEN = ["Main ingredient, weight and cut", "Changes from the card", "Taste and texture"]

# 1. One log, at the path the date of the cook gives.
logs = sorted(os.path.relpath(path, root) for path in glob.glob(os.path.join(root, "cook-logs", "**", "*.md"), recursive=True))
if logs != [LOG]:
    print("expected exactly one log, at %s; found %s" % (LOG, logs)); sys.exit(1)
log = read(os.path.join(root, LOG))
found, order = sections(log)
if order != ["What the cook reported", "Inference", "Next controlled change", "Card follow-up"]:
    fail("the log's ## headings are %s" % order)
head = log.split("\n## ")[0]
if head.split("\n")[0] != "# Cook log: Skillet Green Beans with Lemon and Garlic":
    fail("the log's first line is not '# Cook log: Skillet Green Beans with Lemon and Garlic'")
if not any(re.fullmatch(r"- \*\*Reported:\*\* \d{4}-\d{2}-\d{2}", line) for line in head.split("\n")):
    fail("the log lacks a Reported line holding one date")
if "- **Date cooked:** 2026-11-17" not in head.split("\n"):
    fail("the log lacks the line '- **Date cooked:** 2026-11-17'")
if not any(line.startswith("- **Recipe:**") and "v1.0" in line and CARD in line for line in head.split("\n")):
    fail("the Recipe line does not name v1.0 and %s" % CARD)
for leftover in ["Copy this file", "YYYY-MM-DD", "recipe-slug", "category-folder"]:
    if leftover in log:
        fail("the log still holds template text: %s" % leftover)

# 2. Every reported line is the cook's words or Not reported.
items = re.findall(r"(?m)^- \*\*(.+?):\*\* (.*)$", found.get("What the cook reported", ""))
if [label for label, _ in items] != LABELS:
    fail("the reported labels are %s" % [label for label, _ in items])
values = dict(items)
for label, value in items:
    if value.strip() != "Not reported.":
        quoted(value, label)
for label in SILENT:
    if values.get(label, "").strip() != "Not reported.":
        fail("%s is not 'Not reported.' though the cook did not report it" % label)
for label in SPOKEN:
    if values.get(label, "Not reported.").strip() == "Not reported.":
        fail("%s is 'Not reported.' though the cook reported it" % label)
for label, word in [("Main ingredient, weight and cut", "10 oz"), ("Changes from the card", "olive oil"),
                    ("Taste and texture", "soft")]:
    if word not in values.get(label, ""):
        fail("%s does not quote the cook's words about: %s" % (label, word))
for name in ["What the cook reported", "Card follow-up"]:
    extra = [line for line in found.get(name, "").split("\n") if line.strip() and not line.startswith("- **")]
    if extra:
        fail("%s holds a line that is not a labeled item: %s" % (name, extra[0][:60]))

# 3. Inference is labeled.
inference = [line.strip() for line in found.get("Inference", "").split("\n") if line.strip()]
if not inference or not (inference == ["None."] or all(re.match(r"(- )?Inference:", line) for line in inference)):
    fail("each Inference line must start with 'Inference:', or the section is 'None.'")

# 4. One next change, in the cook's words because the idea was the cook's.
change = [line.strip() for line in found.get("Next controlled change", "").split("\n") if line.strip()]
if len(change) != 1:
    fail("Next controlled change holds %d lines, expected 1" % len(change))
elif "lemon" not in change[0] or not quoted(re.sub(r"^- ", "", change[0]), "Next controlled change"):
    fail("Next controlled change does not quote the cook's own idea")

# 5. The card follow-up.
follow = dict(re.findall(r"(?m)^- \*\*(.+?):\*\* (.*)$", found.get("Card follow-up", "")))
evidence = follow.get("Evidence", "")
if "untested" not in evidence or "cooked-once" not in evidence or "repeated" in evidence:
    fail("Card follow-up does not give the evidence change untested to cooked-once")
asked = follow.get("Changes the cook asked for", "").strip()
if asked != "None requested." and not quoted(asked, "Changes the cook asked for"):
    fail("Changes the cook asked for is neither 'None requested.' nor the cook's words")

# 6. The card is untouched, and nothing is committed.
status = git("status", "--porcelain", "--untracked-files=all").splitlines()
if status != ["?? " + LOG]:
    fail("git status shows %s" % status)
if git("rev-parse", "HEAD") != git("rev-parse", "fixture-start"):
    fail("a commit was made")

# 7. The reply.
rsections, rorder = sections(reply)
if rorder != ["Logged", "Not reported", "Next controlled change", "Card follow-up"]:
    fail("the reply's ## headings are %s" % rorder)
if LOG not in rsections.get("Logged", ""):
    fail("the reply's Logged section lacks the log's path")
if "recipe-codify" not in rsections.get("Card follow-up", ""):
    fail("the reply's Card follow-up section does not name recipe-codify")

if bad:
    print("\n".join(bad)); sys.exit(1)
print("log check ok: %s" % LOG)
PY
}
````

## Build plan — agent loop

Run every command from the repository root, in one Bash shell in which the
setup has been run first: the two lines below, then the `block` and `extract` definitions of
`### Writing a file from this spec`, pasted as written, then the three
`eval` lines, which load the other helpers from this spec's own text.

```bash
OUT=$(mktemp)
SPEC="$(git rev-parse --show-toplevel)/docs/specs/S004-codify-and-cook-log.md"
```

```bash
eval "$(block '### Link check')"
eval "$(block '#### Helper: `codifycheck`')"
eval "$(block '#### Helper: `logcheck`')"
```

Afterward `type -t block extract linkcheck codifycheck logcheck` prints
`function` five times. A gate passes only when every command in it
prints what is stated. Where a gate ends in `; echo $?`, the printed status
is part of the expected output, and a non-zero status that is expected is
not a failure. The gate's commands run in the order listed, on the finished
work before it is committed; nothing is staged until a line says `after git
add`, and from that line on the task's Touches are staged. The commit
follows the last line, except where a line says it runs after the commit.

Baseline, measured by leg 1 on 2026-11-19 in a scratch clone at `base_sha`:
`python3 -m unittest discover -s tests -v` exits 0 and ends `OK` with 88
tests; `python3 scripts/check-skills.py` prints `skills checked: 1`;
`python3 scripts/check-council.py` prints `council checked: 14 seated, 14
records`; `linkcheck AGENTS.md` prints nothing. Every other gate line names
a file this spec creates or changes, so it is red on the base by design;
none measures old debt. Leg 1 then built Tasks 1 to 4 in that clone from
this spec with `extract` and ran every gate line below except the lines
that need the commits of this run (the `TASK1_SHA` lines), loading the
helpers by the setup above, and ran the privacy sweep's `--text` on every
file this spec gives.

### Task 1 — Add the tests for the index generator
- **Work:** Create `tests/test_build_index.py` with exactly the content
  given under its `#### File:` heading. The seam under test is one command,
  `python3 scripts/build-index.py [--check] [repository-root]` (decision
  21), observed only through its standard output, standard error, exit
  status, and the `recipes/INDEX.md` it writes. Each test builds a
  repository root in a temporary directory, and each expected index is a
  literal written from decision 21. The tests catch: no `recipes/` folder
  writes the empty index; cards are listed by category and then slug, with
  slugs compared as slugs and not as file names; a card with no front
  matter, with a missing line, or with an empty value is `not stated`; the
  category and the slug come from the path even when the front matter
  disagrees; a `|` in a title is escaped; Windows line endings are read;
  files directly in `recipes/`, in a dot folder, with a dot name, without
  `.md`, or one folder too deep are not cards; a card with no title, a
  title only inside the front matter, or unclosed front matter is a
  problem; several problems print in card order; a problem leaves an
  existing index alone; a card that is not UTF-8 is a problem; a `|` in a
  value is escaped; the first of a repeated front-matter line wins; writing
  twice gives the same index; `--check`
  passes on a current index, fails on a stale, hand-edited, or missing one
  and writes nothing, reports card problems, and may follow the root; two
  roots, a repeated `--check`, and an unknown option are usage errors; a root that is not a
  directory exits 2; and this repository's own index is current.
- **Touches:** `tests/test_build_index.py`
- **Gate:**
  - This prints `tests/test_build_index.py: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    0b59a9d2730a6efc1b5061a87ff65abedb4c00d666a9d0f7fe21cbd11b426568  tests/test_build_index.py
    SUMS
    ```

  - With the working tree differing from `base_sha` only under `docs/` and
    in this test file, `python3 -m unittest discover -s tests -v > "$OUT"
    2>&1; echo $?` prints `1`, `tail -1 "$OUT"` prints `FAILED
    (failures=29)`, and `grep -c ' ok$' "$OUT"` prints `88`. This is the
    recorded red: leg 1 measured it on 2026-11-19 in a scratch clone at
    `base_sha` with only the test file applied. All 29 methods of
    `BuildIndexTest` fail by assertion, because the script does not exist
    yet and each run of it exits 2 with nothing on standard output; none is
    an error and none is an import error. The 29 are
    `test_a_problem_leaves_the_old_index_alone`,
    `test_card_that_is_not_utf8_is_a_problem`,
    `test_card_without_a_title_is_a_problem`,
    `test_card_without_front_matter_is_not_stated`,
    `test_cards_are_listed_by_category_then_slug`,
    `test_category_and_slug_come_from_the_path`,
    `test_check_fails_on_a_hand_edited_index`,
    `test_check_fails_on_a_missing_index_and_writes_nothing`,
    `test_check_fails_on_a_stale_index_and_writes_nothing`,
    `test_check_may_follow_the_root`,
    `test_check_passes_on_a_current_index`,
    `test_check_reports_card_problems`,
    `test_every_problem_is_reported_in_card_order`,
    `test_first_of_a_repeated_field_wins`,
    `test_missing_and_empty_fields_are_not_stated`,
    `test_no_recipes_folder_writes_the_empty_index`,
    `test_only_cards_one_folder_down_are_listed`,
    `test_pipe_in_a_title_is_escaped`,
    `test_pipe_in_a_value_is_escaped`,
    `test_repeated_check_is_a_usage_error`,
    `test_root_that_is_not_a_directory_exits_two`,
    `test_slugs_sort_as_slugs_not_as_file_names`,
    `test_this_repository_index_is_current`,
    `test_title_inside_the_front_matter_does_not_count`,
    `test_two_roots_are_a_usage_error`,
    `test_unclosed_front_matter_is_a_problem`,
    `test_unknown_option_is_a_usage_error`,
    `test_windows_line_endings_are_read`, and
    `test_writing_twice_gives_the_same_index`.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
    tests/test_build_index.py` ends with a line beginning `privacy sweep:
    clean` and exits 0.
- **Nature:** mechanical

### Task 2 — Add the index generator and the empty index
- **Work:** Create `scripts/build-index.py` with exactly the content given
  under its `#### File:` heading, without the executable bit. Then run
  `python3 scripts/build-index.py` from the repository root, which prints
  `index written: 0` and creates `recipes/INDEX.md`; do not write that file
  by hand. Do not change anything under `tests/`; a test that seems to need
  a change is reported as ``Question: Task 2 of
  `docs/specs/S004-codify-and-cook-log.md` needs a test the tests task
  wrote changed; revise the spec?``
- **Touches:** `scripts/build-index.py`, `recipes/INDEX.md`
- **Gate:**
  - This prints two lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    5036f021d743a415319575a96258814f4b8bb75561047ed37c9eda443a48406d  scripts/build-index.py
    36b42ea72e1889a4098d55c6439ef86bd343dc51d15f7996b4c8e4f0702609f0  recipes/INDEX.md
    SUMS
    ```

  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
    prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
    prints `117`.
  - `python3 scripts/build-index.py --check; echo $?` prints `index current:
    0` then `0`.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
    scripts/build-index.py recipes/INDEX.md` ends with a line beginning
    `privacy sweep: clean` and exits 0.
  - After `git add scripts/build-index.py recipes/INDEX.md`, `git ls-files
    -s scripts/build-index.py` prints a line beginning `100644`.
  - The tests are unchanged. Before the commit, `git status --porcelain --
    tests/` prints nothing. After it, this prints only `tests unchanged`:

    ```bash
    TASK1_SHA=$(git log --format=%H -1 --grep='^Spec-Task: S004/1$')
    [ -n "$TASK1_SHA" ] && git merge-base --is-ancestor "$TASK1_SHA" HEAD &&
      [ -z "$(git diff --name-only "$TASK1_SHA..HEAD" -- tests/)" ] &&
      echo "tests unchanged"
    ```
- **Nature:** mechanical

### Task 3 — Add the card, cook-log, and source-packet templates and the status rules
- **Work:** Create `templates/recipe-card.md`, `templates/cook-log.md`,
  `templates/source-packet.md`, and `method/status-and-versions.md` with
  exactly the content given under their `#### File:` headings.
- **Touches:** `templates/recipe-card.md`, `templates/cook-log.md`,
  `templates/source-packet.md`, `method/status-and-versions.md`
- **Gate:**
  - This prints four lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    00853d062827f33402fab046714c80592b1b963ea47a0f1888ef1cb2063e4939  templates/recipe-card.md
    2033381f6c7842d5c7441e1e7b5cd3a745192d2d0bf8bdf247c3b374506c5fce  templates/cook-log.md
    c063566e59e32564599c99168b384f5d13c168fe91f79aef318bd783a39ebaa7  templates/source-packet.md
    70706acbaf730af38629f8c4c9d2e290d10cbfd6a44339543751033580170579  method/status-and-versions.md
    SUMS
    ```

  - `python3 scripts/build-index.py --check; echo $?` prints `index current:
    0` then `0` (the templates are not cards).
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
    templates/recipe-card.md templates/cook-log.md
    templates/source-packet.md method/status-and-versions.md` ends with a
    line beginning `privacy sweep: clean` and exits 0.
  - After `git add` of the four Touches, `linkcheck templates/recipe-card.md
    templates/cook-log.md templates/source-packet.md
    method/status-and-versions.md recipes/INDEX.md; echo $?` prints `0` and
    nothing else. `recipes/INDEX.md` is checked here because its one link
    points at `method/status-and-versions.md`, which this task creates.
- **Nature:** mechanical

### Task 4 — Add the recipe-codify and cook-log skills with their links and index lines
- **Work:** Create `.agents/skills/recipe-codify/SKILL.md` and
  `.agents/skills/cook-log/SKILL.md` with exactly the content given under
  their `#### File:` headings. Create the two links, from the repository
  root:

  ```bash
  ln -s ../../.agents/skills/recipe-codify .claude/skills/recipe-codify
  ln -s ../../.agents/skills/cook-log .claude/skills/cook-log
  ```

  In `AGENTS.md`, make exactly these three changes and nothing else.

  Replace the one line

  ```text
  4. The saved recipe card, and its most recent cook log, before changing that recipe or cooking from it.
  ```

  with

  ```text
  4. The saved recipe card, listed in [`recipes/INDEX.md`](recipes/INDEX.md), and its most recent cook log in `cook-logs/`, before changing that recipe or cooking from it.
  ```

  In the line that begins `- **Status is several separate facts:**`,
  replace its last sentence

  ```text
  Never raise any of these without a logged cook or the cook saying so.
  ```

  with these two sentences, leaving the rest of the line as it is:

  ```text
  Never raise any of these without a logged cook or the cook saying so. [`method/status-and-versions.md`](method/status-and-versions.md) is the full rule, with the version table.
  ```

  Directly after the line that begins ``- `chef-council`:``, insert these
  two lines:

  ```text
  - `recipe-codify`: [`.agents/skills/recipe-codify/SKILL.md`](.agents/skills/recipe-codify/SKILL.md). Use it to save an approved recipe as a card, change a saved card, or start a separate version to test. It writes the card with its version and an honest status, regenerates the index, and saves the source packet for the editor check.
  - `cook-log`: [`.agents/skills/cook-log/SKILL.md`](.agents/skills/cook-log/SKILL.md). Use it when the cook reports back after cooking. It logs what happened in the cook's own words, marks everything else as not reported, and says what the card needs next.
  ```
- **Touches:** `.agents/skills/recipe-codify/SKILL.md`,
  `.agents/skills/cook-log/SKILL.md`, `.claude/skills/recipe-codify`,
  `.claude/skills/cook-log`, `AGENTS.md`
- **Gate:**
  - This prints three lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    86cb5d65d692c3f0971c6514035eefa84dd2985c1dd2342c7c5b82fcc315ee04  .agents/skills/recipe-codify/SKILL.md
    77ca8a64980fa2a82c3197733dae95f943672ca4e0db4ed01ae134aa28ce4bb3  .agents/skills/cook-log/SKILL.md
    de0d3cfe5b4c4526de27556f1d9d4195bb2425f734a232d02b5ab0e6e7aa3532  AGENTS.md
    SUMS
    ```

  - `readlink .claude/skills/recipe-codify` prints
    `../../.agents/skills/recipe-codify`, and `readlink
    .claude/skills/cook-log` prints `../../.agents/skills/cook-log`.
  - `git diff --numstat HEAD -- AGENTS.md` prints one line: `4`, `2`, and
    `AGENTS.md`, separated by tabs. `wc -c < AGENTS.md` prints `7748`.
  - `git status --porcelain --untracked-files=all` prints exactly these
    five lines:

    ```text
     M AGENTS.md
    ?? .agents/skills/cook-log/SKILL.md
    ?? .agents/skills/recipe-codify/SKILL.md
    ?? .claude/skills/cook-log
    ?? .claude/skills/recipe-codify
    ```

  - `python3 scripts/check-skills.py; echo $?` prints `skills checked: 3`
    then `0`, and `python3 scripts/check-council.py; echo $?` prints
    `council checked: 14 seated, 14 records` then `0`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
    prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
    prints `117`.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text AGENTS.md
    .agents/skills/recipe-codify/SKILL.md .agents/skills/cook-log/SKILL.md`
    ends with a line beginning `privacy sweep: clean` and exits 0.
  - After `git add` of the five Touches, `git ls-files -s
    .claude/skills/recipe-codify .claude/skills/cook-log` prints two lines,
    each beginning `120000`, and `linkcheck AGENTS.md
    .agents/skills/recipe-codify/SKILL.md .agents/skills/cook-log/SKILL.md;
    echo $?` prints `0` and nothing else.
- **Nature:** mechanical

After Task 4's commit, the push, and the pull request, the orchestrator
observes definition-of-done items 1 to 8. Items 5 to 8 need the pushed
branch, so they are not part of any task's gate.

## Repo profile

`.agents/spec-profile.md` applies as written. Additions for this spec only:

- The pull request's Evidence section holds the two replies, the card, the
  packet, and the log as definition-of-done item 8 says, and the recorded
  red of Task 1 beside the green of Task 2 (the two `tail -1` lines). The
  source packet is shown there although packets are never committed,
  because this one holds only the spec's own fixture text.
- The pull request's Merge Danger section says that the change adds files
  and four lines of `AGENTS.md` and removes nothing; that from the merge on
  a stale `recipes/INDEX.md` fails the unit tests in CI; that the
  `recipe-codify` skill refers to an editor skill that does not exist until
  T011, and says the check was not run until then; and that reverting the
  merge removes the two skills, the templates, the method page, the
  generator, its tests, and the index, and restores `AGENTS.md`.
- The cross-examination dossier holds this spec, `AGENTS.md`, the profile,
  the ticket, `.agents/skills/README.md`, the `chef-council` skill's
  `SKILL.md` (its hand-off section is the interface `recipe-codify`
  receives), `kitchen/profile.md`, `scripts/check-skills.py`,
  `tests/test_check_skills.py`, `.gitignore`, and
  `.github/workflows/ci.yml`; every new file is already in the spec. It
  does not hold the other tests, `scripts/check-council.py`, or the vetting
  records, so the counts this spec states from them are leg 1's
  measurements in a scratch clone at `base_sha`: 88 tests before and 117
  after, and `council checked: 14 seated, 14 records`.

## Cross-examination

One round, on the complete first draft, on 2026-11-19: Meta
`muse-wonder-full-1.0` (architect tier) at high reasoning effort, through
Muse Code 1.4.15 (1.4.15-R8339.1) in the read-only sandbox of the
maintainer's routes document. The dossier held the draft, the ticket, and
the files `## Repo profile` lists, and passed the privacy sweep's `--text`
and a gitleaks scan before it was sent. The reviewer reported that it had
read-only file, search, and memory tools and a workflow tool, with shell and
writes disabled, and that it read only the dossier. It returned 27 findings.
All 27 were accepted, five of them in part; none was dropped. After the
edits leg 1 rebuilt the scratch clone, ran every gate again, and rehearsed
both behavior checks again on the final bytes.

1. **ACCEPT** (blocking: a blank `kitchen/profile.md` could stop codify).
   `recipe-codify` step 4 now says a blank profile holds no corrections and
   is no reason to stop or to interview before saving.
2. **ACCEPT** (blocking: `codifycheck` did not prove order, placement, or
   the tilde lines). The helper's section parser now skips fenced blocks,
   and the approved text must sit whole and in order between the tilde
   lines under Approved text, with the scope sentence between those under
   Scope instruction.
3. **ACCEPT in part** (blocking: no exact command loads the helpers). The
   setup now pastes only `block` and `extract` and loads `linkcheck`,
   `codifycheck`, and `logcheck` with three `eval "$(block ...)"` lines,
   followed by a `type -t` line. A hash of the helpers is rejected: they are
   read from this spec's own text, which is the thing approved.
4. **ACCEPT** (major: `codifycheck` let wrong cards pass). It now requires
   eight ingredient rows each pairing the ingredient with its amount, the
   skillet under Equipment, four numbered steps, the Yield and Time figures,
   and a dated `v1.0` changelog line. The reading question on the Method
   stays.
5. **ACCEPT** (major: `logcheck` gaps). It now requires the title line, a
   Reported line with one date, the cook's own words under the right label
   for the three things the cook reported, and an evidence line that names
   `untested` and `cooked-once` and not `repeated`.
6. **ACCEPT** (major: the `log` fixture's sentence about the pan read as
   equipment). The sentence is now `We ate all of it at dinner.`, and the
   spec says Yield and portions, Verdict, and Problems and rescues are left
   to the writer's reading.
7. **ACCEPT** (major: which template paragraphs survive). The cook-log and
   source-packet templates now say what a filled file keeps (title, top
   lines, headings, labels or tilde lines) and that every sentence of
   instruction goes; decisions 15 and 16 say the same, and `logcheck`
   rejects any line that is not a labeled item under the first heading and
   under Card follow-up.
8. **ACCEPT** (major: three wordings of the slug rule). One rule, stated in
   the method page under Names and places and in decision 14; both skills
   refer to it.
9. **ACCEPT** (major: how evidence is counted). The method page, the
   `recipe-codify` skill, the `cook-log` skill, and decision 11 now give the
   procedure: count the logs whose Recipe line names the current version;
   an earlier log or a no-card log counts only when the current version's
   changelog line names it; `not-recorded` only when the cook cannot give a
   day or a report.
10. **ACCEPT** (major: how to read the card on the default branch). The
    skill and decision 15 now give `git show main:<path>` and `git
    rev-parse main`, and the fallback when the card is not there or git
    cannot be run.
11. **ACCEPT** (major: no path for a save without a check, and no branch
    rule). The Save section and decisions 18 and 19 now give both: the cook
    may say to save unchecked, which the commit and the pull request then
    state, never after a failed check; the branch is the cook's, or one
    named for the card.
12. **ACCEPT** (major: "saved" meant four things). Saved now has four named
    stages (`written`, `committed`, `in a pull request`, `merged`), the
    reply's first heading is `## Files written`, and decisions 10 and 20
    follow.
13. **ACCEPT** (major: `reviewed` without a check). `reviewed` now needs the
    cook's word or a hand-off with every Ready to save line at `yes`, in
    the method page, the skill, and decision 10.
14. **ACCEPT in part** (major: filesystem errors in the generator).
    Decision 21 now says which three problems are handled and that any
    other filesystem error ends in a traceback and a non-zero exit, which
    still fails the check. Handling them in code is rejected: S001's
    decision 10 took the same position for the skill check, and each added
    branch would need its own test for a case no cook's repository meets.
15. **ACCEPT in part** (major: characters that break the link). Decision 21
    now says the generator writes names as they are and does not encode
    them. Encoding is rejected: decision 14's rule makes names that need
    none, and a name that breaks it is the linter's finding (T011).
16. **ACCEPT** (major: symbolic links). Decision 21 now says a link is
    followed and counts like what it points to, which is what the code does.
17. **ACCEPT** (major: missing tests). Four tests added: a card that is not
    UTF-8, a `|` in a value, the first of a repeated front-matter line
    winning, and a repeated `--check`. The recorded red is now 29 failures
    and the suite 117 tests.
18. **ACCEPT** (major: lint and secret scan not runnable as written).
    Definition-of-done item 3 gives the lint command, and the prerequisites
    set `WAYFINDER` and require Linux x86_64 or `GITLEAKS_BIN`.
19. **ACCEPT** (major: category names). A category name is made from the
    cook's chosen name by the slug rule (method page, skill, decision 14).
20. **ACCEPT in part** (major: save kinds and variant numbers). The skill's
    table now has one row for a status or evidence change alone, covering a
    recorded cook, `house`, and `retired`; variants take the next unused
    number on the original's slug. A title whose own slug ends in `-v` and
    a digit is not given a rule, and decision 12 says so.
21. **ACCEPT** (major: the card template's `None recorded.` sentence). It
    now names the six sections it applies to and gives `Not stated.` for a
    missing amount or time.
22. **ACCEPT** (major: the template's `###` lines and example steps). The
    template and the skill now say the `###` lines are only for a recipe
    with more than one component or stage and that the three steps show
    form and are not steps to keep.
23. **ACCEPT** (major: the Reported line). The skill and decision 16 define
    it as the day the cook told the writer, today unless the cook says
    otherwise.
24. **ACCEPT** (major: a stale index hides a slug collision). The skill now
    looks at the card files in every folder under `recipes/`.
25. **ACCEPT** (minor: longer tilde lines). Decision 15 and the skill now
    carry the template's exception.
26. **ACCEPT** (minor: writing rule against tolerant reading). Decision 4
    now separates the two, and `codifycheck` requires the keys in order,
    each once.
27. **ACCEPT** (minor: a run that crosses midnight). The `codify` message
    is now written immediately before its subagent starts, and a run during
    which the date changes is void and run again.

## File contents

Each block is one file, written as `### Writing a file from this spec`
says. `recipes/INDEX.md` is not among them: Task 2 generates it, and its
hash is in Task 2's gate.

#### File: `tests/test_build_index.py`

````python
"""Tests for scripts/build-index.py, observed through its output, its exit status, and the file it writes."""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "build-index.py")
USAGE = "usage: build-index.py [--check] [repository-root]\n"
HEADER = (
    "# Recipe index\n"
    "\n"
    "Generated by `scripts/build-index.py` from the recipe cards. Do not edit this file by hand: "
    "run `python3 scripts/build-index.py` after adding or changing a card. "
    "[`method/status-and-versions.md`](../method/status-and-versions.md) explains the status and evidence values.\n"
    "\n"
)
TABLE = (
    "| Recipe | Category | Version | Status | Kitchen evidence |\n"
    "|---|---|---|---|---|\n"
)
EMPTY = HEADER + "No recipe cards yet.\n"
CARROTS = (
    "---\n"
    "id: roasted-carrots\n"
    "version: v1.2\n"
    "status: testing\n"
    "evidence: cooked-once\n"
    "category: sides\n"
    "mirrors: none\n"
    "---\n"
    "\n"
    "# Roasted Carrots\n"
    "\n"
    "- **Version:** v1.2\n"
)
CHILI = (
    "---\n"
    "id: bean-chili\n"
    "version: v1.0\n"
    "status: draft\n"
    "evidence: untested\n"
    "category: mains\n"
    "---\n"
    "\n"
    "# Bean Chili\n"
)
TWO_CARDS = (
    HEADER
    + TABLE
    + "| [Bean Chili](mains/bean-chili.md) | mains | v1.0 | draft | untested |\n"
    + "| [Roasted Carrots](sides/roasted-carrots.md) | sides | v1.2 | testing | cooked-once |\n"
)
STALE = "recipes/INDEX.md is stale: run python3 scripts/build-index.py"
MISSING = "recipes/INDEX.md is missing: run python3 scripts/build-index.py"


def run(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        check=False,
    )


class BuildIndexTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)

    def index(self):
        path = os.path.join(self.root, "recipes", "INDEX.md")
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8", newline="") as handle:
            return handle.read()

    def two_cards(self):
        self.write("recipes/sides/roasted-carrots.md", CARROTS)
        self.write("recipes/mains/bean-chili.md", CHILI)

    def build(self, expected_lines, expected_status, *options):
        result = run(*options, self.root)
        self.assertEqual(result.stdout.splitlines(), expected_lines)
        self.assertEqual(result.returncode, expected_status)
        return result

    def test_no_recipes_folder_writes_the_empty_index(self):
        self.build(["index written: 0"], 0)
        self.assertEqual(self.index(), EMPTY)

    def test_cards_are_listed_by_category_then_slug(self):
        self.two_cards()
        self.build(["index written: 2"], 0)
        self.assertEqual(self.index(), TWO_CARDS)

    def test_slugs_sort_as_slugs_not_as_file_names(self):
        self.write("recipes/sides/rice-pilaf.md", "# Rice Pilaf\n")
        self.write("recipes/sides/rice.md", "# Rice\n")
        self.build(["index written: 2"], 0)
        self.assertEqual(
            self.index(),
            HEADER
            + TABLE
            + "| [Rice](sides/rice.md) | sides | not stated | not stated | not stated |\n"
            + "| [Rice Pilaf](sides/rice-pilaf.md) | sides | not stated | not stated | not stated |\n",
        )

    def test_card_without_front_matter_is_not_stated(self):
        self.write("recipes/sides/plain-rice.md", "# Plain Rice\n\n- **Version:** v1.0\n")
        self.build(["index written: 1"], 0)
        self.assertEqual(
            self.index(),
            HEADER
            + TABLE
            + "| [Plain Rice](sides/plain-rice.md) | sides | not stated | not stated | not stated |\n",
        )

    def test_missing_and_empty_fields_are_not_stated(self):
        self.write(
            "recipes/sides/plain-rice.md",
            "---\nid: plain-rice\nversion: v2.0\nstatus:\ntags:\n  - weeknight\n---\n# Plain Rice\n",
        )
        self.build(["index written: 1"], 0)
        self.assertEqual(
            self.index(),
            HEADER
            + TABLE
            + "| [Plain Rice](sides/plain-rice.md) | sides | v2.0 | not stated | not stated |\n",
        )

    def test_category_and_slug_come_from_the_path(self):
        self.write(
            "recipes/sides/plain-rice.md",
            "---\nid: something-else\ncategory: mains\nversion: v1.0\nstatus: house\nevidence: repeated\n---\n# Plain Rice\n",
        )
        self.build(["index written: 1"], 0)
        self.assertEqual(
            self.index(),
            HEADER
            + TABLE
            + "| [Plain Rice](sides/plain-rice.md) | sides | v1.0 | house | repeated |\n",
        )

    def test_pipe_in_a_title_is_escaped(self):
        self.write("recipes/sides/rice.md", "# Rice | Two Ways\n")
        self.build(["index written: 1"], 0)
        self.assertEqual(
            self.index(),
            HEADER
            + TABLE
            + "| [Rice \\| Two Ways](sides/rice.md) | sides | not stated | not stated | not stated |\n",
        )

    def test_pipe_in_a_value_is_escaped(self):
        self.write("recipes/sides/rice.md", "---\nversion: v1.0\nstatus: draft | testing\nevidence: untested\n---\n# Rice\n")
        self.build(["index written: 1"], 0)
        self.assertEqual(
            self.index(),
            HEADER + TABLE + "| [Rice](sides/rice.md) | sides | v1.0 | draft \\| testing | untested |\n",
        )

    def test_first_of_a_repeated_field_wins(self):
        self.write("recipes/sides/rice.md", "---\nversion: v1.0\nversion: v9.9\nstatus: draft\nevidence: untested\n---\n# Rice\n")
        self.build(["index written: 1"], 0)
        self.assertEqual(
            self.index(),
            HEADER + TABLE + "| [Rice](sides/rice.md) | sides | v1.0 | draft | untested |\n",
        )

    def test_windows_line_endings_are_read(self):
        self.write("recipes/mains/bean-chili.md", CHILI.replace("\n", "\r\n"))
        self.build(["index written: 1"], 0)
        self.assertEqual(
            self.index(),
            HEADER + TABLE + "| [Bean Chili](mains/bean-chili.md) | mains | v1.0 | draft | untested |\n",
        )

    def test_only_cards_one_folder_down_are_listed(self):
        self.two_cards()
        self.write("recipes/README.md", "# Recipes\n")
        self.write("recipes/sides/notes.txt", "# Not a card\n")
        self.write("recipes/sides/.hidden.md", "# Hidden\n")
        self.write("recipes/.drafts/idea.md", "# Idea\n")
        self.write("recipes/sides/old/roasted-carrots.md", "# Old Carrots\n")
        self.build(["index written: 2"], 0)
        self.assertEqual(self.index(), TWO_CARDS)

    def test_card_without_a_title_is_a_problem(self):
        self.two_cards()
        self.write("recipes/sides/untitled.md", "---\nid: untitled\n---\n\nNo heading here.\n")
        self.build(["recipes/sides/untitled.md: has no title line"], 1)
        self.assertIsNone(self.index())

    def test_title_inside_the_front_matter_does_not_count(self):
        self.write("recipes/sides/untitled.md", "---\n# A comment\nid: untitled\n---\n\nNo heading here.\n")
        self.build(["recipes/sides/untitled.md: has no title line"], 1)

    def test_unclosed_front_matter_is_a_problem(self):
        self.write("recipes/sides/open.md", "---\nid: open\n\n# Open\n")
        self.build(["recipes/sides/open.md: front matter is not closed"], 1)
        self.assertIsNone(self.index())

    def test_card_that_is_not_utf8_is_a_problem(self):
        path = os.path.join(self.root, "recipes", "sides", "latin.md")
        os.makedirs(os.path.dirname(path))
        with open(path, "wb") as handle:
            handle.write(b"# Cr\xe8me\n")
        self.build(["recipes/sides/latin.md: is not UTF-8 text"], 1)
        self.assertIsNone(self.index())

    def test_every_problem_is_reported_in_card_order(self):
        self.write("recipes/sides/open.md", "---\nid: open\n")
        self.write("recipes/mains/untitled.md", "Just text.\n")
        self.write("recipes/mains/bean-chili.md", CHILI)
        self.build(
            [
                "recipes/mains/untitled.md: has no title line",
                "recipes/sides/open.md: front matter is not closed",
            ],
            1,
        )

    def test_a_problem_leaves_the_old_index_alone(self):
        self.two_cards()
        self.build(["index written: 2"], 0)
        self.write("recipes/sides/untitled.md", "Just text.\n")
        self.build(["recipes/sides/untitled.md: has no title line"], 1)
        self.assertEqual(self.index(), TWO_CARDS)

    def test_writing_twice_gives_the_same_index(self):
        self.two_cards()
        self.build(["index written: 2"], 0)
        self.build(["index written: 2"], 0)
        self.assertEqual(self.index(), TWO_CARDS)

    def test_check_passes_on_a_current_index(self):
        self.two_cards()
        self.build(["index written: 2"], 0)
        self.build(["index current: 2"], 0, "--check")
        self.assertEqual(self.index(), TWO_CARDS)

    def test_check_fails_on_a_stale_index_and_writes_nothing(self):
        self.two_cards()
        self.build(["index written: 2"], 0)
        self.write("recipes/mains/bean-chili.md", CHILI.replace("version: v1.0", "version: v1.1"))
        self.build([STALE], 1, "--check")
        self.assertEqual(self.index(), TWO_CARDS)

    def test_check_fails_on_a_hand_edited_index(self):
        self.two_cards()
        self.write("recipes/INDEX.md", TWO_CARDS + "\nA note added by hand.\n")
        self.build([STALE], 1, "--check")

    def test_check_fails_on_a_missing_index_and_writes_nothing(self):
        self.two_cards()
        self.build([MISSING], 1, "--check")
        self.assertIsNone(self.index())

    def test_check_reports_card_problems(self):
        self.write("recipes/INDEX.md", EMPTY)
        self.write("recipes/sides/untitled.md", "Just text.\n")
        self.build(["recipes/sides/untitled.md: has no title line"], 1, "--check")

    def test_check_may_follow_the_root(self):
        self.write("recipes/INDEX.md", EMPTY)
        result = run(self.root, "--check")
        self.assertEqual(result.stdout.splitlines(), ["index current: 0"])
        self.assertEqual(result.returncode, 0)

    def test_two_roots_are_a_usage_error(self):
        result = run(self.root, self.root)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, USAGE)
        self.assertEqual(result.returncode, 2)

    def test_repeated_check_is_a_usage_error(self):
        result = run("--check", "--check", self.root)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, USAGE)
        self.assertEqual(result.returncode, 2)

    def test_unknown_option_is_a_usage_error(self):
        result = run("--fix", self.root)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, USAGE)
        self.assertEqual(result.returncode, 2)
        self.assertIsNone(self.index())

    def test_root_that_is_not_a_directory_exits_two(self):
        missing = os.path.join(self.root, "nowhere")
        result = run(missing)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "build-index: %s is not a directory\n" % missing)
        self.assertEqual(result.returncode, 2)

    def test_this_repository_index_is_current(self):
        result = run("--check")
        self.assertRegex(result.stdout, r"\Aindex current: [0-9]+\n\Z")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
````

#### File: `scripts/build-index.py`

````python
#!/usr/bin/env python3
"""Generate recipes/INDEX.md from the recipe cards.

Usage: python3 scripts/build-index.py [--check] [repository-root]

A card is a file recipes/<category>/<slug>.md. Its title is the first line
that starts with "# " after the front matter, and its version, status, and
evidence are read from the front matter as plain "key: value" lines. A card
with no front matter, or without one of those three lines, is listed with
"not stated" in that column. Files directly in recipes/ and files more than
one folder down are not cards.

Without --check, writes recipes/INDEX.md and prints "index written: <N>".
With --check, writes nothing: prints "index current: <N>" and exits 0 when
recipes/INDEX.md is already what would be written, or says that it is stale
or missing and exits 1. A card that cannot be read prints one line per
problem and exits 1 with nothing written. method/status-and-versions.md
explains the values the index shows.
"""

import os
import re
import sys

USAGE = "usage: build-index.py [--check] [repository-root]"
INDEX = "recipes/INDEX.md"
FIELD = re.compile(r"([a-z_]+):[ \t]*(.*)")
COLUMNS = ["version", "status", "evidence"]
HEADER = """# Recipe index

Generated by `scripts/build-index.py` from the recipe cards. Do not edit this file by hand: run `python3 scripts/build-index.py` after adding or changing a card. [`method/status-and-versions.md`](../method/status-and-versions.md) explains the status and evidence values.
"""
TABLE = """
| Recipe | Category | Version | Status | Kitchen evidence |
|---|---|---|---|---|
"""
EMPTY = """
No recipe cards yet.
"""


def find_cards(root):
    """Return (category, slug) for every card, in category then slug order."""
    recipes = os.path.join(root, "recipes")
    cards = []
    if not os.path.isdir(recipes):
        return cards
    for category in os.listdir(recipes):
        folder = os.path.join(recipes, category)
        if category.startswith(".") or not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            if name.startswith(".") or not name.endswith(".md"):
                continue
            if os.path.isfile(os.path.join(folder, name)):
                cards.append((category, name[: -len(".md")]))
    return sorted(cards)


def read_card(path):
    """Return (title, fields, problem); problem is None when the card reads."""
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except UnicodeDecodeError:
        return None, None, "is not UTF-8 text"
    fields = {}
    if lines and lines[0] == "---":
        if "---" not in lines[1:]:
            return None, None, "front matter is not closed"
        end = lines.index("---", 1)
        for line in lines[1:end]:
            match = FIELD.fullmatch(line)
            if match and match.group(1) not in fields:
                fields[match.group(1)] = match.group(2).strip()
        lines = lines[end + 1 :]
    for line in lines:
        if line.startswith("# ") and line[2:].strip():
            return line[2:].strip(), fields, None
    return None, None, "has no title line"


def cell(text):
    return text.replace("|", "\\|")


def build(root):
    """Return (index text, card count, problems)."""
    rows = []
    problems = []
    cards = find_cards(root)
    for category, slug in cards:
        relative = "recipes/%s/%s.md" % (category, slug)
        title, fields, problem = read_card(os.path.join(root, "recipes", category, slug + ".md"))
        if problem:
            problems.append("%s: %s" % (relative, problem))
            continue
        values = [fields.get(key) or "not stated" for key in COLUMNS]
        rows.append(
            "| [%s](%s/%s.md) | %s | %s |\n"
            % (cell(title), category, slug, cell(category), " | ".join(cell(value) for value in values))
        )
    if rows:
        return HEADER + TABLE + "".join(rows), len(cards), problems
    return HEADER + EMPTY, len(cards), problems


def main(argv):
    arguments = argv[1:]
    check = "--check" in arguments
    paths = [argument for argument in arguments if argument != "--check"]
    if len(paths) > 1 or arguments.count("--check") > 1 or any(path.startswith("-") for path in paths):
        print(USAGE, file=sys.stderr)
        return 2
    if paths:
        root = paths[0]
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(root):
        print("build-index: %s is not a directory" % root, file=sys.stderr)
        return 2

    text, count, problems = build(root)
    if problems:
        for problem in problems:
            print(problem)
        return 1
    index_path = os.path.join(root, "recipes", "INDEX.md")
    if check:
        try:
            with open(index_path, encoding="utf-8", newline="") as handle:
                current = handle.read()
        except FileNotFoundError:
            print("%s is missing: run python3 scripts/build-index.py" % INDEX)
            return 1
        except UnicodeDecodeError:
            current = None
        if current != text:
            print("%s is stale: run python3 scripts/build-index.py" % INDEX)
            return 1
        print("index current: %d" % count)
        return 0
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print("index written: %d" % count)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
````

#### File: `templates/recipe-card.md`

````markdown
---
id: recipe-slug
version: v1.0
status: draft
evidence: untested
category: category-folder
mirrors: none
---

# Recipe title

- **Version:** v1.0
- **Date:** YYYY-MM-DD
- **Status:** draft
- **Kitchen evidence:** untested
- **Source:** Original. Or: adapted from, or technique informed by, a source that was actually read, credited by title and link.
- **Yield:** Servings or pieces
- **Time:** Total time, including preheating, coming up to pressure and releasing it, reducing, and resting

Copy this file to `recipes/<category>/<slug>.md` and replace every line. The block at the top repeats the version, status, and evidence lines for scripts, so keep the two in step, and write each value as a plain word with no quotation marks. `id` is the file name without `.md`, and `category` is the folder. [`method/status-and-versions.md`](../method/status-and-versions.md) gives the values each line can hold and the rule for version numbers. Under Why this works, Failure modes, Variations, Storage, Notes, or Next experiment, write `None recorded.` when the approved recipe says nothing for that heading. Where the approved recipe leaves out something a cook needs, such as an amount or a time, write `Not stated.` in its place. Never fill a gap from memory. The `###` lines under Ingredients and Method are for a recipe with more than one component or stage, so leave them out of a recipe with one. The three steps under Method show the form of a step and are not steps to keep. Delete this paragraph when the card is filled in.

## Equipment

- An item, with its size or model where that changes the result.

## Ingredients

### Component name

| Amount | Ingredient | Prep |
|---|---|---|
| The amount, in the units the cook approved | Ingredient | Prep, or none |

## Method

### Stage name

1. **Step name.** The action, the heat, the time range, and the cue to look for.
2. **Check doneness.** The doneness check, with the temperature when the approved recipe gives one.
3. **Finish.** Taste and adjust, in the order the approved recipe gives.

## Why this works

- **A decision in the recipe.** The reason it matters to the result.

## Failure modes

| Problem | Likely cause | Fix |
|---|---|---|
| What goes wrong | Why it happens | What to do about it |

## Variations

- **Variation name.** What changes. Mark a variation nobody has cooked as untested.

## Storage

- Cooling, the refrigerator or freezer plan, and reheating.

## Notes

- Substitutions with their tradeoffs, what does not scale with the batch, and anything the recipe leaves open.

## Next experiment

One open question to settle at the next cook, or `None recorded.`

## Changelog

- v1.0 (YYYY-MM-DD): First card. Say whether it has been cooked, when, and how it went, or that it has not.
````

#### File: `templates/cook-log.md`

````markdown
# Cook log: Recipe title

- **Date cooked:** YYYY-MM-DD
- **Recipe:** Recipe title, v1.0, at `recipes/category-folder/recipe-slug.md`. Or: No card yet.
- **Reported:** YYYY-MM-DD, the day the cook reported back

Copy this file to `cook-logs/<slug>/<YYYY-MM-DD>.md`, named for the day of the cook, and replace every line. A second cook of the same recipe on the same day ends in `-2`. Log what happened, not what the recipe recommended. Keep the title, the three lines above, the four headings, and the labels. Delete this paragraph and the sentences of instruction under each heading when the log is filled in, so that each heading holds only what you wrote.

## What the cook reported

Each line holds the cook's own words inside double quotation marks, or `Not reported.` and nothing else. Never fill a line from the recipe card, and never reword what the cook said.

- **Main ingredient, weight and cut:** Not reported.
- **Changes from the card:** Not reported.
- **Equipment used:** Not reported.
- **Times:** Not reported.
- **Doneness checks and temperatures:** Not reported.
- **Yield and portions:** Not reported.
- **Taste and texture:** Not reported.
- **Verdict from the people who ate it:** Not reported.
- **Storage and reheating:** Not reported.
- **Problems and rescues:** Not reported.

## Inference

What the writer of this log concluded and the cook did not say. Each line starts with `Inference:`. Write `None.` when there is nothing to add.

- Inference: A likely cause or a reading of the report, with what it rests on.

## Next controlled change

One change to try at the next cook, on one line, so its effect can be seen. When the idea is the cook's, the line is the cook's words inside quotation marks and nothing else. When it is not, the line starts with `Proposed:`. Or write `None proposed.`

- Proposed: The one change, and what it should show.

## Card follow-up

What the recipe card needs after this cook. The card itself is changed through the recipe-codify skill, never from this log.

- **Evidence:** The kitchen-evidence value the card holds now and the one it should hold, such as `untested` to `cooked-once`. Or: No card yet.
- **Changes the cook asked for:** Each change in the cook's words, inside quotation marks, or `None requested.`
````

#### File: `templates/source-packet.md`

````markdown
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
````

#### File: `method/status-and-versions.md`

````markdown
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
````

#### File: `.agents/skills/recipe-codify/SKILL.md`

````markdown
---
name: recipe-codify
description: Turns a recipe the cook approved into a standalone recipe card from templates/recipe-card.md, assigns the version, sets an honest status and kitchen-evidence line, regenerates the recipe index, and saves a verbatim source packet for the independent editor check. Use when someone asks to save a recipe, make a card, make a separate second version, record a change to a saved card, or calls a recipe final.
---

# Recipe Codify

Codifying writes down what the cook approved. It does not improve the recipe, fill its gaps, or decide what the cook meant. If the recipe still needs work, that is the council's job, not this skill's.

Paths in this file are relative to the repository root.

## Before you write

1. **Find the approved text.** It is the complete recipe the cook approved, or, for a change to a saved card, the cook's exact corrections. It may come from the chef-council skill's hand-off, under its `## Approved text` heading, or from the cook directly. If you cannot point to the text and to the cook approving it, ask. Never rebuild a recipe from memory or from a summary.
2. **Find the scope instruction.** The cook's own words about what to save: a new card, a change to a saved one, or a separate version to test. The cook sets the scope. If the cook has not said, ask that one question and wait.
3. **Read the rules.** Read `method/status-and-versions.md`. For a change to a saved card, find the card in `recipes/INDEX.md` and read it and its most recent log in `cook-logs/<slug>/`.
4. **Check the standing corrections** in `kitchen/profile.md`. If the approved text conflicts with one, name the conflict and ask the cook which stands before writing anything. A profile whose `filled_in` line is not exactly `filled_in: yes` is a blank template: it holds no corrections, and it is no reason to stop or to interview the cook before saving.

## Decide the kind of save

| The cook wants | Kind | What you write |
|---|---|---|
| A recipe that has no card | New card | `recipes/<category>/<slug>.md` at `v1.0` |
| A change to a saved card | Update | The same file, with the version `method/status-and-versions.md` gives for that change |
| A changed technique, cut, or appliance, or a version to test beside the original | New variant | A new file, the original's slug with `-v2` at `v2.0`, or the next unused number. Do not touch the original |
| A status or evidence change and nothing else, such as a cook recorded on a saved card, or the cook making a recipe `house` or `retired` | Update | The same file at the same version, with the new value and a changelog line that starts with the version and the date |

When the cook's instruction and the version table disagree, say what the table would do, then follow the cook. Only the cook makes a recipe `house` or `retired`, and `house` needs a logged cook.

## Write the source packet first

Copy `templates/source-packet.md` to `.sources/<slug>/<YYYY-MM-DD>.md`, using today's date, and fill it in before you write the card. Then write the card from the packet, not from your memory of the conversation.

- Paste the approved text verbatim; never summarize. Do not tidy it, reorder it, fix its spelling, or convert its units.
- Paste the scope instruction in the cook's own words.
- Put each pasted part between two lines of four tildes, or longer lines of tildes when the text itself holds a line of four or more.
- For an update or a new variant, paste the saved card whole as it stands on the default branch, `main` unless the repository uses another: `git show main:recipes/<category>/<slug>.md` prints it, and `git rev-parse main` prints the commit to name. If the card is not on the default branch yet, or you cannot run git, paste the file as it stands and say in the packet which of the two it is.
- List the paths the template asks for.
- Never commit a packet. Git ignores `.sources/` because a packet can hold private conversation text or a publisher's recipe.

## Write the card

Copy `templates/recipe-card.md` to `recipes/<category>/<slug>.md` and replace every line.

- **Slug and category.** Make the slug from the title as `method/status-and-versions.md` says under Names and places. No two cards share a slug, whatever their categories, so look at the card files in every folder under `recipes/` first, not only at the index. Use the category the cook names, made into a folder name the same way a slug is made. If the cook names none, use the folder that already holds similar cards, or ask.
- **The block at the top.** Write `id`, `version`, `status`, `evidence`, `category`, and `mirrors` as plain words with no quotation marks. `id` is the slug and `category` is the folder. The lines under the title repeat the version, status, and evidence, and the two must agree. The date is today's.
- **The recipe itself.** Equipment, Ingredients, Method, Yield, and Time carry what the approved text says and nothing else. Every ingredient keeps its amount, unit, and prep. Every step keeps its order, heat, time, cue, and doneness check. You may reword a step and arrange the recipe into the template's tables. Use a `###` component or stage line only when the approved text has more than one component or stage, and add no step: the template's three steps show the form of a step. You may not change what gets cooked.
- **Do not invent.** Never add a quantity, a time, a temperature, an ingredient, or a step. Never convert a unit unless the cook asks for it. Where the approved text leaves out something a cook needs, write `Not stated.` in its place, list it under Notes as open, and set the status to `draft`.
- **The other sections.** Why this works, Failure modes, Variations, Storage, Notes, and Next experiment hold only what the approved text or the cook said. Under a heading with nothing to hold, write `None recorded.` Do not write new advice into a card.
- **Source.** Write `Original.` for a recipe developed here. Credit a published source by title and link only when it was actually read, as `adapted from` or `technique informed by`. A lens is never an author or a source, and no card says a person reviewed or approved it. Do not copy a publisher's ingredient list, method, or headnote into a card: when the approved text is a publisher's recipe, say so and ask the cook what of their own to save.
- **Status and evidence.** Take both from `method/status-and-versions.md`. A new card is `reviewed` when nothing is open, the cook approved the text, and the recipe was checked for coherence, which the cook's word or a chef-council hand-off with every Ready to save line at `yes` shows. Otherwise it is `draft`. Evidence counts the logs in `cook-logs/<slug>/` as that page says: read each log's Recipe line and count the ones that name the card's current version, plus an earlier one only when the changelog line for the current version names it. When the cook says they cooked the recipe and there is no log, the cook-log skill writes the log first; use `not-recorded` only when the cook cannot give a day or a report to log. Never raise either value on your own.
- **Changelog.** Add one line for this save: the version, the date, what changed, and why. For a new card, say whether it has been cooked.

## Regenerate the index

Run `python3 scripts/build-index.py`. It rewrites `recipes/INDEX.md` from the cards and prints `index written:` with the number of cards. Never edit the index by hand. If it prints a problem with a card, fix the card and run it again. If you cannot run commands, say that the index was not regenerated and give the cook the command.

## Hand off to the editor

A card is not checked by the agent that wrote it. Hand the packet's path and the card's path, and nothing of your own reasoning, to the recipe-editor skill listed under Skills in `AGENTS.md`, run by a fresh agent that did not write the card.

- If no such skill is listed there, or you cannot start a second agent, say that the editor check has not been run and give the packet's path. Do not write a report yourself, and do not call the card checked, verified, or approved.
- On a failed check, fix the card from the packet and ask for a fresh check.
- Until a check passes, do not commit the card, open a pull request, or copy the card anywhere outside the repository. If the check cannot be run, leave that decision to the cook.

## Save

Save after a passing check. When the check could not be run and the cook then tells you to save anyway, follow the same steps, and say in the commit message and in the pull request that the editor check was not run. Never save after a failed check.

- Work on a branch, and never push `main`. Use the branch the cook names, or create one named for the card, such as `card/roasted-carrots`.
- Commit the card, the regenerated index, any new cook log, and the editor's report when there is one, together, with a subject such as `Add the roasted carrots card v1.0`.
- Open a pull request against `main`. The cook merges it.
- When the cook works alone and asks for no pull request, commit on the branch the cook names and stop there. The cook pushes.
- Copy a card to a notes app only when the cook asks or calls the recipe final. `mirrors` stays `none` until a copy has been written and read back.

## What to tell the cook

Reply under these four headings, in this order:

1. `## Files written`: each file you wrote, with its path, and each file you did not write, with the reason. Never list a file you have not written.
2. `## Status`: four lines. Development and Kitchen evidence, as the card states them. Saved: the stage the card has reached, which is `written`, `committed` with the branch, `in a pull request`, or `merged`. Mirrored: `none`, or each copy and whether it was read back.
3. `## Editor check`: who the card was handed to and the result, or `Not run:` with the reason and the packet's path.
4. `## Next step`: the one thing that happens next, and who does it.

If you cannot write files, return the complete card and the complete packet, each with its path, for the cook to save, give the index command, and say that nothing was saved.
````

#### File: `.agents/skills/cook-log/SKILL.md`

````markdown
---
name: cook-log
description: Records what actually happened when a recipe was cooked, using only what the cook reported and marking everything else as not reported, keeps the writer's inferences apart from the cook's words, and proposes one next controlled change. Use when someone reports back after cooking, such as saying they made it tonight, that it came out dry, or that everyone liked it.
---

# Cook Log

A cook log is the evidence a recipe's status rests on, so it holds what the cook said happened and nothing else. What the recipe recommended is not evidence, and neither is what probably happened.

Paths in this file are relative to the repository root.

## Before you write

1. **Find the card.** Look the recipe up in `recipes/INDEX.md` and read the card, so you know its slug and the version that was cooked. A dish with no card can still be logged: make the slug from the dish's name as `method/status-and-versions.md` says under Names and places, and write `No card yet.` on the Recipe line.
2. **Find the date of the cook.** Use the date the cook gives. Work out a date such as last night from today's date when you know it. If you cannot tell the date, ask, because the file is named for it. The Reported line holds the day the cook told you, which is today unless the cook says otherwise.
3. **Gather the report.** The report is everything the cook has said about this cook in the conversation. Nothing else goes into the log as fact.

## Write the log

Copy `templates/cook-log.md` to `cook-logs/<slug>/<YYYY-MM-DD>.md`, named for the day of the cook, and replace every line. A second cook of the same recipe on the same day ends in `-2`. Keep the template's title, its three top lines, its four headings, and its ten labels, in their order, and delete its sentences of instruction, so that each heading holds only what you wrote.

Under `## What the cook reported`:

- Each line holds the cook's own words inside straight double quotation marks, or `Not reported.` and nothing else. No paraphrase, no summary, and no words of yours beside a quotation.
- A quotation is an exact, unbroken piece of what the cook wrote, with the cook's spelling and units. Quote as much as the line needs, and put two pieces on one line as two quotations. Write a double quotation mark inside the cook's words as a single one.
- Never fill a line from the recipe card. If the card says twelve minutes and the cook did not mention the time, the line is `Not reported.`
- Write the log from what you have. Do not hold it back to ask for more: the reply lists what was not reported, and the cook can add to it.
- A log is committed with the repository, and a public fork publishes it. When the cook's words name a person or give a health detail, quote the part that leaves it out, or ask the cook before writing it down.

Under `## Inference`, write what you concluded and the cook did not say, such as a likely cause. Start each line with `Inference:` and say what it rests on. Write `None.` when you have nothing to add. An inference never moves up into the report.

Under `## Next controlled change`, give one change on one line, so that its effect can be seen at the next cook. When the idea is the cook's, the line is the cook's words in quotation marks and nothing else. When it is yours, the line starts with `Proposed:`. Write `None proposed.` when the cook wants the recipe left alone or nothing suggests a change. Advice on how to run the change belongs in your reply, not in the log.

## Card follow-up

This skill never changes a recipe card. Under `## Card follow-up`, write what the card needs:

- **Evidence.** The kitchen-evidence value the card holds now and the one it should hold, such as `untested` to `cooked-once`, counted as `method/status-and-versions.md` says: this log and each earlier log in `cook-logs/<slug>/` whose Recipe line names the same version. For a dish with no card, write `No card yet.`
- **Changes the cook asked for.** Each one in the cook's words, in quotation marks, or `None requested.`

The card is changed through the recipe-codify skill listed under Skills in `AGENTS.md`, which takes the change through the editor check. Only the cook makes a recipe `house`. Never raise a status because a cook went well.

## Save

Write the file and stop. Do not commit it in the same turn: a log travels with the card's change when there is one, and otherwise the cook says when to commit it, on a branch and never on `main`.

## What to tell the cook

Reply under these four headings, in this order:

1. `## Logged`: the path of the log, and that it is written and not committed. If you cannot write files, return the complete log with its path for the cook to save, and say that nothing was saved.
2. `## Not reported`: the labels that hold `Not reported.`, so the cook can fill in any that matter.
3. `## Next controlled change`: the one change, as the log has it.
4. `## Card follow-up`: what the card needs, and that the recipe-codify skill makes the change.
````
