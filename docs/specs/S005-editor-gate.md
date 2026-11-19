---
date: 2026-11-19
id: S005
wayfinder: docs/wayfinder/W001-public-chef-council/issues/T011-editor-gate.md
target_release: none
status: ready-to-build
base_branch: main
base_sha: 492df7ced36c08e9de3e0efbf1311a37e7adc9ae
work_branch: workstream/t011-editor-gate
pr_base: main
prior_specs:
  - docs/specs/archive/S001-scaffold.md
  - docs/specs/archive/S002-council-roster-and-vetting.md
  - docs/specs/archive/S003-chef-council-skill.md
  - docs/specs/archive/S004-codify-and-cook-log.md
references:
  - docs/wayfinder/W001-public-chef-council/MAP.md
  - docs/wayfinder/W001-public-chef-council/issues/T002-named-chefs-with-guardrails.md
  - docs/wayfinder/W001-public-chef-council/issues/T005-privacy-rules.md
  - docs/wayfinder/W001-public-chef-council/issues/T012-example-recipes.md
  - docs/wayfinder/W001-public-chef-council/issues/T013-chat-path-and-adapters.md
  - docs/learnings/L001-scaffold.md
  - docs/learnings/L002-council-roster-and-vetting.md
  - docs/learnings/L003-chef-council-skill.md
  - docs/learnings/L004-codify-and-cook-log.md
  - .agents/spec-profile.md
cross_examined: meta/muse-wonder-full-1.0 (architect), 17 findings, 17 accepted
approved_by: human
approved_at: 2026-11-19T03:23Z
pr: none
kickbacks: 0
merged: none
harvested: none
---

# Editor gate: the recipe-editor skill, the hash-bound gate, the card linter, and their CI jobs

## Goal and definition of done

Ship ticket T011: the independent editor check as a gate that works with any
agent and is enforced in CI. That is the `recipe-editor` skill with its
report format, its Claude Code link, its line in `AGENTS.md`, and a thin
Claude Code subagent wrapper; `scripts/check-qc.sh`, the gate, which binds
each report to the SHA-256 of the card it checked; `scripts/lint-cards.py`;
the optional `scripts/install-git-hooks.sh` and the optional Claude Code Stop
hook in `.claude/settings.json`; `method/recipe-qc.md` for people and chat
users; the tests for the three scripts; and the CI steps that run the gate
and the linter.

Every new file is given byte for byte under `## File contents`, and the
changes to `AGENTS.md`, `.github/workflows/ci.yml`, and
`.agents/spec-profile.md` are given as exact insertions and replacements.
Leg 1 wrote and tested every file in a scratch clone at `base_sha`; the
executor does not rewrite any of them. Between that text and the merge stand
the unit tests (Tasks 1 and 2), the CI run on the pull request, and two
behavior checks by fresh subagents, each in its own scratch repository
(definition-of-done item 8).

Done means all of the following, each observed on the work branch's head
commit after Task 4, from the repository root, in a shell prepared as
`## Build plan — agent loop` says:

1. **The files.** `git ls-files .agents/skills/recipe-editor
   .claude/skills/recipe-editor .claude/agents .claude/settings.json
   method/recipe-qc.md scripts/check-qc.sh scripts/lint-cards.py
   scripts/install-git-hooks.sh tests/test_check_qc.py
   tests/test_lint_cards.py tests/test_install_git_hooks.py` prints exactly
   these twelve lines:

   ```text
   .agents/skills/recipe-editor/SKILL.md
   .agents/skills/recipe-editor/references/report-format.md
   .claude/agents/recipe-editor.md
   .claude/settings.json
   .claude/skills/recipe-editor
   method/recipe-qc.md
   scripts/check-qc.sh
   scripts/install-git-hooks.sh
   scripts/lint-cards.py
   tests/test_check_qc.py
   tests/test_install_git_hooks.py
   tests/test_lint_cards.py
   ```

   `git ls-files qc recipes` prints `recipes/INDEX.md` and nothing else: this
   spec adds no card and no report.

2. **The bytes.** This prints fourteen lines, each a path followed by `:
   OK`, one for each regular file this spec gives or changes (the link of
   item 1 has no content to hash, and item 6's `readlink` line checks it):

   ```bash
   sha256sum -c - <<'SUMS'
   4131bcd27fdd03e9b236babdc16cdc375ea717c002db3a78949bb1a16ac8acf9  .agents/skills/recipe-editor/SKILL.md
   29fa84b8c682f6444c5e90c425d0f909d88189be0390eb8b994b37c5191d2dd3  .agents/skills/recipe-editor/references/report-format.md
   39ec76d8042ca822bebc856255ec16ece3af8121c5ad22776f814dbb083fdbbd  .agents/spec-profile.md
   d2d9e928ceae66c94fed230fb4e7252d31ef37678e4848d1b66af70b49e132e9  .claude/agents/recipe-editor.md
   dacf9c6bb99e80c0494f243519dc24e25d9b2780e8126ddeaf0b5ebb0df7309e  .claude/settings.json
   3b1879f59b4357dec413d25017e81e8800e3fb627836aaefbf210c510aa42bf4  .github/workflows/ci.yml
   129f4344ea97173387d287cd31435537c6a3da468bb0d53970f9e281806bafaf  AGENTS.md
   3b08937672463f6242681f9a5178dc6b4fb845dd32dbfbe1434cbbf32f45cf2b  method/recipe-qc.md
   bd3451f41898a0407d67f4fdd399b4fd76a3c6b226189f1da0fc0a0430d98d17  scripts/check-qc.sh
   e810839e1e2c169db95b7936d841f1fd7344f0f3a537c81758886a3cfbb86490  scripts/install-git-hooks.sh
   8b7b18e00f7ad6c333638cb9e517f14806517fc2f05c8c100357edf93c0f8d1f  scripts/lint-cards.py
   2b188763c5acb7de4f5c5f8a6860e720e497874d615c8d66b674862b340a53ee  tests/test_check_qc.py
   92aa6f5dd590ea3e61174e2c75126afaea1dec62cc334cc73c69aa097c602ac8  tests/test_install_git_hooks.py
   37eac472a8a6251380f0ab0f2dd4781306611fefb3fda8a08cafe59aa75e1686  tests/test_lint_cards.py
   SUMS
   ```

3. **The repository's checks.** `python3 scripts/check-skills.py; echo $?`
   prints `skills checked: 4` then `0`. `python3 scripts/check-council.py;
   echo $?` prints `council checked: 14 seated, 14 records` then `0`.
   `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
   `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"` prints
   `225`. `python3 scripts/build-index.py --check; echo $?` prints `index
   current: 0` then `0`. `python3 scripts/lint-cards.py; echo $?` prints
   `cards checked: 0` then `0`. After `git fetch origin`,
   `scripts/check-qc.sh; echo $?` prints `qc checked: 0` then `0`.
   `scripts/secret-scan.sh; echo $?` ends with `0`. `python3
   "$WAYFINDER/scripts/lint.py" docs/wayfinder/*/MAP.md; echo $?` prints `0`
   and nothing else (`WAYFINDER` is set as `## Prerequisites` says). The
   three diff checks and the full privacy sweep pass as the profile's ship
   tail requires.
4. **Links.** `linkcheck AGENTS.md .agents/skills/recipe-editor/SKILL.md
   .agents/skills/recipe-editor/references/report-format.md
   method/recipe-qc.md; echo $?` prints `0` and nothing else.
5. **CI.** `gh pr checks <PR> --watch` returns once every check has
   finished; then `gh pr checks <PR>` reports every check passed, and lists
   three checks: `gitleaks (full history)`, `tests`, and `editor gate`. With
   `HEAD_SHA=$(gh pr view <PR> --json headRefOid --jq .headRefOid)` and
   `RUN=$(gh run list --commit "$HEAD_SHA" --workflow CI --event pull_request
   --json databaseId --jq '.[0].databaseId')`, `RUN` is not empty, `gh run
   view "$RUN" --log > "$OUT"` succeeds, and
   each of these three prints `0`: `grep -qF 'qc checked: 0' "$OUT"; echo
   $?`, `grep -qF 'cards checked: 0' "$OUT"; echo $?`, and `grep -qF
   'test_this_repository_lints_clean
   (test_lint_cards.LintCardsTest.test_this_repository_lints_clean) ... ok'
   "$OUT"; echo $?` (the quoted text of the third is one line). That is the ticket's "CI is green on this PR, which
   changes no card": the gate ran against the pull request's base and found
   no changed card.
6. **A fresh clone agrees.** Make a fresh clone of the pushed branch in a
   new temporary directory, from the repository root:

   ```bash
   CLONE=$(mktemp -d)
   git clone --quiet --branch workstream/t011-editor-gate "$(git remote get-url origin)" "$CLONE"
   ```

   Then, from inside `$CLONE`: `git rev-parse HEAD` equals the pull
   request's head commit; `readlink .claude/skills/recipe-editor` prints
   `../../.agents/skills/recipe-editor`; `cmp
   .claude/skills/recipe-editor/SKILL.md
   .agents/skills/recipe-editor/SKILL.md; echo $?` prints `0` and nothing
   else; `python3 scripts/check-skills.py` prints `skills checked: 4`;
   `python3 scripts/lint-cards.py` prints `cards checked: 0`;
   `scripts/check-qc.sh` prints `qc checked: 0` (the clone has
   `origin/main`); `git ls-files -s scripts/check-qc.sh
   scripts/install-git-hooks.sh` prints two lines, each beginning `100755`;
   `python3 -c 'import json; print(list(json.load(open(".claude/settings.json"))["hooks"]))'`
   prints `['Stop']`; and `echo '{"stop_hook_active": false}' |
   scripts/check-qc.sh --stop-hook; echo $?` prints `0` and nothing else.
   Afterward `git -C "$CLONE" status --porcelain` prints nothing.
7. **Rendered and read.** Render `AGENTS.md`,
   `.agents/skills/recipe-editor/SKILL.md`,
   `.agents/skills/recipe-editor/references/report-format.md`,
   `method/recipe-qc.md`, and `.claude/agents/recipe-editor.md` from the
   pushed branch with the profile's observation command and look at each
   result. It passes when every heading renders as a heading, every list as
   a list, and every table as a table (in `SKILL.md` the severity table; in
   `method/recipe-qc.md` the verdict table and the table of ways to run the
   editor); the example report in `report-format.md` renders as one code
   block that shows its own inner fence and its table as plain text; the
   editor prompt in `method/recipe-qc.md` renders as one code block; no raw
   Markdown markup is visible in the body below the front matter outside a
   code span or a code block; and each link added by this spec is a link.
   How GitHub displays the front matter is not judged (L001).
8. **Behavior.** The two checks of `### Behavior checks` each pass. The
   pull request's Evidence section holds each of the two replies verbatim in
   a collapsed `<details>` block, with its `editor check ok:` line above it,
   and below each the report the subagent wrote, verbatim in its own
   collapsed `<details>` block.

The ticket's done-conditions map onto these items. "The tests show the gate
failing a card change with no report, with a stale-hash report, and with a
FAIL report, and passing one with a current passing report" is the first
four tests of `tests/test_check_qc.py`, named for those four cases, red in
Task 1 and green in Task 2 and in CI (items 3 and 5). "CI is green on this
PR, which changes no card" is item 5.

## Decisions

Decisions T002 and T005 bind this spec; the profile's `## Pipeline
constraints` apply to every file, every commit message, and the pull
request.

1. **All content is fixed here.** Leg 1 wrote every file, built Tasks 1 to 4
   from this spec in a scratch clone at `base_sha`, and ran every gate line
   that needs no pushed branch. Every task is therefore `mechanical`
   (L014 of the pipeline: a tests task whose file is given byte for byte is
   mechanical).
2. **One spec.** The ticket is one spec of four tasks. Its engineering is
   three scripts and their tests, written and measured in leg 1; the rest is
   text. New tests appear at one point only, Task 1.
3. **Where a report lives.** The report for `recipes/<category>/<slug>.md`
   is `qc/<category>/<slug>/<YYYY-MM-DD>.md`, named for the day of the
   check; a second on the same day ends in `-2`. The private predecessor
   keyed reports by slug alone
   (`private-sources/cooking/context/recipe-qc.md`), which the design report
   lists as a collision (§3 items 8 and 9). The ticket asks for keys that
   cannot collide. Keying by the card's own path meets that without relying
   on any other check, and the linter also enforces one slug per card
   (decision 12), which the cook-log and source-packet paths rely on (S004
   decision 14). The folder is the key. The gate does not read the file's
   name: any Markdown file directly in the card's folder whose name does not
   start with a dot counts as a report, and the dated name is the report
   format's convention for people and agents, not a rule the gate enforces. No `qc/` folder, `qc/README.md`, or `templates/qc-report.md`
   is created: the ticket names none, the form of a report is given once in
   the skill's reference file, and the first reports are T012's.
4. **The two lines the gate reads.** A report holds exactly one line that
   starts with `VERDICT:` and exactly one that starts with `Card-SHA256:`,
   each at the start of a line with nothing before it. The gate reads those
   two lines and nothing else of a report. Trailing white space, including a
   carriage return, is ignored on every line. The verdict line must be
   exactly `VERDICT: PASS` or `VERDICT: PASS WITH NOTES` to pass; `VERDICT:
   FAIL` and anything else fail. The hash line must be `Card-SHA256: ` and
   64 lowercase hexadecimal digits equal to the SHA-256 of the card. In the
   report the two lines sit together in one fenced `text` block under the
   title, so they render one per line and no list marker or table bar ever
   precedes them. A second line starting with either prefix makes the report
   invalid rather than ambiguous.
5. **What the gate requires.** A card that was added or changed passes when
   at least one report for it that was also added or changed has a passing
   verdict and the card's current hash. This is the ticket's rule as
   written. Three consequences are intended. A failed report may sit beside
   the later passing one, so the record of a caught error is kept. A report
   that was not touched never counts, even when the card was changed back to
   bytes that report once described. Any change to a card file, a typo
   included, needs a fresh report, because the hash is of the whole file.
   The gate does not fail a card because some other report for the same
   bytes says FAIL; it cannot judge which check was honest, and
   `method/recipe-qc.md` says plainly what the gate does and does not prove.
6. **What a card is, for the gate.** Any changed path
   `recipes/<category>/<name>.md`, exactly one folder below `recipes/`,
   where neither part starts with a dot: the definition `scripts/build-index.py`
   uses (S004 decision 21). Paths are read from git with NUL separators, so a
   name with a space or a non-ASCII letter is still checked, and the folder
   and file names are compared as literal strings, never as patterns. A
   deleted card needs no report. Renames are not followed, so a moved card
   is a new card at its new path and needs a report there.
7. **Three things the gate can compare with the base.** By default it
   reads the last commit, which is what CI sees and what an agent should run
   before opening a pull request. `--staged` reads the index, for the
   pre-commit hook. `--working-tree` reads the files as they are, untracked
   but not ignored files included, for the Stop hook, because the
   `recipe-codify` skill does not commit a card until its check has passed.
   In every mode the changes are counted from the merge base of the base and
   `HEAD`, so commits the base gained after the branch left it are not
   counted. In `--working-tree` the card is hashed as the file stands, which
   differs from the committed bytes only when git converts line endings; the
   default mode, which CI runs, always hashes the committed bytes.
8. **The base, and failing closed.** The base is `--base`, else the
   `QC_BASE` environment variable, else `origin/main`. The ticket says the
   gate "fails closed when `CI=true` or the base ref is missing". This spec
   implements that as one rule that is stricter than either half: the script
   exits 0 only when it ran the comparison and every changed card passed. A
   base that does not resolve to a commit, no merge base, no repository, no
   commit, a failed git command, and no SHA-256 tool each end in one line on
   standard error and exit status 2, with or without `CI=true`. Exit status
   1 means a card lacks its report. The private predecessor exited 0 when
   the base was missing; nothing here does. `CI=true` changes one thing:
   under `--stop-hook`, where exit status 2 is Claude Code's signal to keep
   the session open, a check that could not run exits 1 (reported, and the
   session may stop) unless `CI=true`, when it exits 2. A base of forty
   zeros is what GitHub reports as the previous commit of a branch's first
   push; the script then compares with the empty tree, so every card in the
   repository needs a current passing report. That is the strict reading of
   a push with no earlier commit, and it keeps a first push from failing
   only because there is nothing to compare with.
9. **`--hash`.** `scripts/check-qc.sh --hash <file>` prints the
   `Card-SHA256:` line for a file, using `sha256sum` or, where that is
   missing, `shasum -a 256`. The editor runs it instead of choosing a tool
   per platform, and a chat user runs it before pasting the card into a new
   chat. The script uses no GNU-only option: it sorts its NUL-separated list
   of paths with a plain `sort`, by swapping NUL and newline around it. The `shasum` branch is not covered by a test, because the tests
   cannot remove `sha256sum` from the machine they run on; this gap is
   accepted.
10. **The Stop hook.** `.claude/settings.json` holds one `Stop` hook whose
    command is `cd "$CLAUDE_PROJECT_DIR" && scripts/check-qc.sh --stop-hook`.
    With `--stop-hook` the script reads the hook's JSON from standard input
    and exits 0 at once when `stop_hook_active` is true, wherever the line
    breaks in that JSON fall, so a session is held open at most once per
    stop; it prints nothing on a pass; and on a
    card without its report it prints the problems on standard error and
    exits 2, which Claude Code feeds back to the agent. These are the
    mechanics of the private predecessor's hook
    (`private-sources/cooking/.claude/hooks/recipe-qc-gate.sh` and its
    settings file), which ran in use; the difference is an explicit option
    in place of guessing from whether standard input is a terminal. The
    ticket calls the hook optional. This spec reads that as: it is an extra
    for Claude Code users on top of CI, it ships switched on in the
    committed settings file, and `method/recipe-qc.md` says how to remove
    it. No gate observes Claude Code firing the hook; the tests cover the
    script's side of the contract. A usage error exits 2 before the hook's
    input is read; the shipped command has none, so only a hand-edited
    command can reach that.
11. **The pre-commit hook.** `scripts/install-git-hooks.sh` takes no
    argument and writes one file, the `pre-commit` hook of the repository
    the script sits in, at the path `git rev-parse --git-path
    hooks/pre-commit` gives (so `core.hooksPath` is followed). The hook runs
    `scripts/check-qc.sh --staged` and then `python3 scripts/lint-cards.py`
    and stops the commit when either fails. The linter reads the working
    files, not the index; that is accepted for an optional convenience,
    since CI is the gate. An existing `pre-commit` hook that does not hold
    the line `# chef-council pre-commit hook` is never replaced: the script
    says so and exits 1. A hook that holds the line is rewritten, so a
    cook's own edits to the installed hook are lost on a second run, and
    `method/recipe-qc.md` says so. There is no uninstall option; the hook says to
    delete the file.
12. **The linter.** `python3 scripts/lint-cards.py [repository-root]`
    (standard library, mode 100644, root defaulting to its own repository)
    finds cards the way `scripts/build-index.py` does and prints one line
    per problem, `recipes/<category>/<slug>.md: <problem>`, in card order,
    then exits 1; or prints `cards checked: <N>` and exits 0. It is stricter
    than the index generator on purpose (S004 decisions 4 and 21 left its
    strictness to this ticket):
    - A card or a category folder that is a symbolic link is a problem. A
      linked card could change without its path changing, which would slip
      past the gate.
    - A card must be UTF-8, open with front matter that is closed, and have
      a title line. A card with one of the three problems the index
      generator also reports (`is not UTF-8 text`, `front matter is not
      closed`, `has no title line`) gets no further checks of its content;
      a slug it shares with another card is still reported.
    - The front matter holds `id`, `version`, `status`, `evidence`, and
      `category` exactly once each, and `mirrors` at most once. `id` equals
      the file name without `.md`; `category` equals the folder; `version`
      matches `v`, a number with no leading zero that is at least 1, a
      point, and a number with no leading zero; `status` is one of `draft`,
      `reviewed`, `testing`, `house`, `retired`; `evidence` is one of
      `untested`, `cooked-once`, `repeated`, `not-recorded`. The order of
      the lines is not checked and other keys are allowed, because the index
      generator reads the lines in any order and a fork may add its own.
    - The file name and the folder name are lowercase letters and digits in
      groups joined by single hyphens, the names S004's slug rule produces.
    - Between the title and the first `## ` heading, each of `- **Version:**`,
      `- **Date:**`, `- **Status:**`, `- **Kitchen evidence:**`, `-
      **Source:**`, `- **Yield:**`, and `- **Time:**` starts exactly one
      line. Version, Status, and Kitchen evidence equal the front matter's
      values; Date is a real date written `YYYY-MM-DD`; Source, Yield, and
      Time are not empty.
    - No two cards share a slug, whatever their folders.
    - Every inline link in the card leads to a file or folder that exists,
      after dropping any `#` or `?` part. The forms read are `[text](target)`,
      `[text](<target>)`, and either with a title in double quotation marks
      after the target; a target holds no white space. A target is read
      relative to the card, or relative to the repository root when it
      starts with `/`, as GitHub reads it. Targets with a scheme and targets
      that start with `#` are skipped, and so is everything inside a fenced
      block, which ends at a line of the same character at least as long as
      the line that opened it. Reference-style links are not read.
    - Last, unless a card had one of the three reading problems, it runs
      `scripts/build-index.py --check` on the same root (the script beside
      it) and prints that script's line when the index is stale or missing.
    It does not check a card's `##` sections, whether a status is earned, or
    the content of the `mirrors` line; the ticket lists none of those, and
    the editor reads the first two.
13. **The editor skill.** `recipe-editor/SKILL.md` is 64 lines with one
    reference file, `references/report-format.md`. Its front matter is
    `name` and `description` only, as S003's decision 2 fixed. The skill is
    generalized from `private-sources/cooking/context/recipe-qc.md` and
    `private-sources/cooking/.claude/agents/recipe-editor.md`: the checks
    (ingredients, method, equipment and yield, updates, additions,
    bookkeeping), the two severities, the three verdicts, "no verbatim
    source" as a FAIL, one file written and nothing edited, and the source
    recorded by where it came from and never copied. Dropped: the
    maintainer's name, the notes-app checks and tool, the sync map, and the
    names of other assistants. Added: the independence check as the first
    step, which is the ticket's "with no second agent available it says so
    and never self-certifies" from the editor's side (the writer's side is
    already in `recipe-codify`); the checks that S004's rules make possible
    (`Not stated.` for a gap, the version table, evidence counted from the
    logs in `cook-logs/<slug>/`, or from the logs the packet lists when the
    editor cannot list files); both paths given by whoever asks for the
    check, never chosen by the editor; a one-line `Not independent:` reply
    in place of the four headings when the editor must refuse; fixed values
    for the report's lines when there is no verbatim source; a fixed reply of four headings; and the rule
    that an unsettled difference is blocking.
14. **Each rule is stated once (L004).** What the editor compares, the
    severities, and the verdict rule are in `SKILL.md` only. The report's
    path, form, two gate lines, and what stays out of a report are in
    `references/report-format.md` only. What the gate requires is in
    `method/recipe-qc.md`, and the script's header comment documents the
    same behavior for a reader of the code. The other files refer and do not
    summarize. `method/status-and-versions.md`, the templates, and the two
    S004 skills are not edited, so L004's deferred notes on those files stay
    with the next spec that does edit them.
15. **Reports are public; packets are not.** A report is committed with the
    card. It therefore never copies the approved text (it quotes the few
    words a discrepancy turns on), names no person, holds no health detail,
    and never says or suggests that a person or a lens reviewed or approved
    the card (T002, T005). Its Editor line describes an agent.
16. **The wrapper.** `.claude/agents/recipe-editor.md` is a Claude Code
    subagent definition with `name`, `description`, and `tools: Read, Grep,
    Glob, Bash, Write`, whose body tells the subagent to read the skill and
    follow it. It carries no rule of its own. No gate observes Claude Code
    selecting it; the behavior checks exercise the skill through the
    harness's ordinary fresh subagent, which is the portable path.
17. **The chat path.** `method/recipe-qc.md` gives one prompt for a new
    chat. The cook pastes it, then the skill, the report format,
    `method/status-and-versions.md`, the packet, the card, and the
    `Card-SHA256:` line from `--hash`, so the rules a chat
    editor follows are the same bytes an agent reads and are not restated in
    the prompt. The cook saves the report alone, not the whole reply, whose
    Verdict heading repeats the verdict line. T013's `chat/README.md` points at this section.
18. **`AGENTS.md`** gets three added lines and no other change: the
    `recipe-editor` line after the `cook-log` line, and two lines in the
    list of checks. It is then 8,166 bytes, under the 8,192 limit S001's
    definition of done set, with 26 bytes to spare; a later ticket that adds
    to it must shorten something. `method/recipe-qc.md` is therefore not
    linked from `AGENTS.md`: the report format links it, the gate's failure
    message names it, and T014's README will.
19. **CI.** `.github/workflows/ci.yml` gains one step in the `tests` job,
    `python3 scripts/lint-cards.py`, and one job, `editor gate`, with a
    full-history checkout pinned to the same commit as the existing ones.
    On a pull request the job runs `scripts/check-qc.sh --base
    "origin/<base branch>"`; the checkout is GitHub's merge commit, whose
    merge base with the base branch is the base branch's tip. On a push to
    `main` it runs `--base` with the commit the branch pointed at before the
    push. The branch name and the commit come in through environment
    variables, never through interpolation into the script. The workflow
    already runs on every pull request and every push to `main`. The
    unit tests, which now include the three new modules, run in the `tests`
    job as before.
20. **The profile.** `.agents/spec-profile.md` records the two new local
    commands in its list of deterministic checks, as that list requires of
    the spec that adds a check.
21. **Tests.** Three modules under `tests/`, each observing one script only
    through its output, its exit status, and, for the installer, the hook
    file it writes and what git then does. Every test builds its own
    repository in a temporary directory, with git's global and system
    configuration switched off. Expected lines are literals written from
    decisions 4 to 12. The card hashes in the tests are literals; one is the
    FIPS 180-2 test vector for `abc`. Leg 1 ran a mutation probe of the
    three scripts (L004); `## Build plan — agent loop` records it.
22. **Behavior checks.** Two fresh subagents each follow the skill in a
    scratch repository with no remote: one on a card that matches its
    packet, one on the same card with three planted differences (an amount,
    a time, and an evidence value nobody reported). The fixture recipe is
    S004's, written for that spec; it adapts no publisher's recipe. Not
    exercised, and recorded as limits of this spec's evidence: an update to
    a saved card, a new variant, the editor refusing because it is not
    independent, a missing or summarized packet, the chat prompt in a real
    chat app, and the wrapper inside Claude Code.
23. **Private sources.** Leg 1 read
    `private-sources/design/design-report.md` (§3 items 8 and 9, §4, §6),
    `private-sources/cooking/context/recipe-qc.md`,
    `private-sources/cooking/.claude/agents/recipe-editor.md`,
    `private-sources/cooking/.claude/hooks/recipe-qc-gate.sh`,
    `private-sources/cooking/.github/workflows/recipe-qc-gate.yml`,
    `private-sources/cooking/.claude/settings.json`, and
    `private-sources/cooking/qc/README.md`, and generalized from them under
    the ledger's rows. No passage is copied. The executor opens nothing
    under `private-sources/`.
24. **Not touched.** `README.md` (T014), the chat bundle (T013), the example
    cards and their reports (T012), `scripts/build-index.py`, the S004
    skills and templates, and `method/status-and-versions.md`.

## Prerequisites

- Leg 2 starts from this spec's approval commit on
  `workstream/t011-editor-gate`, which already holds the claim commit for
  T011. Staging, the per-task commit with its `Spec-Task: S005/<N>` trailer,
  the push, the pull request, and the base-drift check are the
  `2-spec-execute` skill's standing procedure and the profile's ship tail.
  Each task's commit holds exactly that task's Touches.
- The executor's machine has Git 2.32 or later, Bash, Python 3, GNU
  coreutils (`sha256sum`, `readlink`), and an authenticated `gh` that has
  `gh run list --commit`. It is Linux x86_64, where `scripts/secret-scan.sh` fetches its
  pinned gitleaks, or `GITLEAKS_BIN` names an installed gitleaks of the
  pinned version (profile). `git config user.email` ends in
  `@users.noreply.github.com` (profile). `git config core.symlinks` does not
  print `false`. `git rev-parse --verify origin/main` succeeds after `git
  fetch origin`.
- Before Task 1, `git status --porcelain --untracked-files=all` prints
  nothing: the checkout holds no file of its own that git does not ignore,
  which Task 3's `git status` line relies on.
- From Task 4's commit on, a Claude Code session in this repository may run
  the Stop hook when it stops. With no card changed it prints nothing and
  exits 0. It is not part of any gate.
- The behavior subagents need to read and write files inside one directory
  and to run `bash`, `git`, and `python3` there. They need no web access and
  are told not to use it.
- No one opens anything under `private-sources/` for this spec (decision
  23).
- `test -x "$(git rev-parse --git-common-dir)/info/privacy-sweep"` succeeds.
  `WAYFINDER` is set to the directory the harness prints when the wayfinder
  skill loads, and `test -f "$WAYFINDER/scripts/lint.py"` succeeds
  (profile). If either is missing, report ``Question: <the privacy sweep |
  the Wayfinder lint> that the profile requires is not on this machine;
  provide it?`` and stop.

### Writing a file from this spec

Each file under `## File contents`, and each fixture and helper under `###
Behavior checks` and `### Link check`, is the text inside the fenced block
that follows its heading: every line between the opening and closing fence,
each ended by a line feed, with nothing added or removed. The opening fence
is a line of four or more backticks, with or without a language name after
them, and the closing fence is the next line that is exactly that many
backticks; one file below holds a four-backtick fence of its own, so its
block uses five. `block` prints one such block, and `extract` writes one
file from it; the executor may use them. `SPEC` is set in the setup of `##
Build plan — agent loop`.

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

Usage: `extract method/recipe-qc.md`; the setup of `### Behavior checks`
shows `block` writing a fixture. `extract` does not set a file's mode; the
tasks say which two files are executable. The SHA-256 gates decide whether a
file is right, whichever way it was written.

### Link check

A gate helper, not a repository file (the helper of S002 to S004,
unchanged), loaded as the setup of `## Build plan — agent loop` says. It
reads the Markdown files named on its command line, skips fenced code
blocks, and requires the target of every inline link `[text](target)` with a
relative target to be a path git tracks or has staged. A target that starts
with `#` or a scheme is skipped. It prints one line per broken link and
returns 1, or prints nothing and returns 0.

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

In `references/report-format.md` the example report sits in a four-backtick
fence with a three-backtick fence inside it. The helper toggles on each of
those four fence lines, so it ends outside a fence, and the example holds no
link.

### Behavior checks

The real-artifact observation for the skill (profile, agent behavior;
decision 22). The orchestrator runs them after the push and the pull
request, from the repository root of the work branch, in the shell of `##
Build plan — agent loop`.

**Setup.** Two scratch repositories under one temporary directory, each a
fresh clone of the pushed branch with no remote, holding a fixture card that
has been written and indexed but not committed, and its source packet:

```bash
SLUG=skillet-green-beans-with-lemon-and-garlic
fixture() {  # fixture <directory> <pass|fail>: make the scratch repository <directory>/<name>
  git clone --quiet --branch workstream/t011-editor-gate "$(git remote get-url origin)" "$1/$2"
  git -C "$1/$2" remote remove origin
  git -C "$1/$2" tag fixture-start
  mkdir -p "$1/$2/recipes/sides" "$1/$2/.sources/$SLUG"
  block '#### Fixture: `packet`' > "$1/$2/.sources/$SLUG/2026-11-10.md"
  if [ "$2" = pass ]; then
    block '#### Fixture: `card`' > "$1/$2/recipes/sides/$SLUG.md"
  else
    block '#### Fixture: `card`' | sed \
      -e 's#^| 1/4 tsp | Kosher salt | None |$#| 1/2 tsp | Kosher salt | None |#' \
      -e 's#crisp-tender, about 2 minutes\.$#crisp-tender, about 4 minutes.#' \
      -e 's#^evidence: untested$#evidence: cooked-once#' \
      -e 's#^- \*\*Kitchen evidence:\*\* untested$#- **Kitchen evidence:** cooked-once#' \
      > "$1/$2/recipes/sides/$SLUG.md"
  fi
  python3 "$1/$2/scripts/build-index.py" "$1/$2"
}
FIX=$(mktemp -d)
fixture "$FIX" pass
fixture "$FIX" fail
sha256sum "$FIX/pass/recipes/sides/$SLUG.md" "$FIX/fail/recipes/sides/$SLUG.md" "$FIX/pass/.sources/$SLUG/2026-11-10.md" | cut -d ' ' -f 1
```

Each `fixture` line prints `index written: 1`, and the last command prints
these three lines:

```text
5519fcf29eeecc3b13e17b0ed26771fa41940040785d045daf66a4b0d461330f
47bbfcee00ddf3d79197c3631d70336c45503b6f0d42a8ae0c56c5f95609f339
57c818c1e11c180ff52ef5f0cc31e1219cff306402631b1ac9afff8f3e3ee270
```

The card in `$FIX/fail` differs from the fixture in four lines, which are
three planted differences: the salt is `1/2 tsp` where the approved text
says `1/4 tsp`; the steam is `about 4 minutes` where it says `about 2
minutes`; and the evidence is `cooked-once`, in the front matter and under
the title, where the cook said the recipe has not been cooked and the packet
lists no cook log.

**The brief.** Each check starts one fresh subagent at the orchestrator
tier through the harness's agent tool, briefed with exactly the brief below
and nothing else, with `<dir>` replaced by the absolute path of the check's
scratch repository (`$FIX/pass` or `$FIX/fail`). The two subagents may run
at the same time. The orchestrator saves each reply, exactly as returned, to
`$FIX/pass-reply.md` or `$FIX/fail-reply.md`.

```text
You are an AI agent starting a fresh session in the repository at <dir> . You did not write any file in it. Read AGENTS.md in that directory and follow it, then follow the recipe-editor skill it lists to check one recipe card. The source packet is at .sources/skillet-green-beans-with-lemon-and-garlic/2026-11-10.md and the card is at recipes/sides/skillet-green-beans-with-lemon-and-garlic.md . Read and write only files inside that directory, and do not use the web. Return only your reply, exactly as the skill says to give it, with nothing before or after it.
```

**The two checks.**

1. **`pass`.** Passes when `editorcheck "$FIX/pass" "$FIX/pass-reply.md"
   pass; echo $?` prints `editor check ok: VERDICT: PASS
   qc/sides/skillet-green-beans-with-lemon-and-garlic/<date>.md` or the same
   line with `VERDICT: PASS WITH NOTES`, then `0`, and the orchestrator,
   reading the report, answers yes to this: no row of the discrepancy table
   reports a difference that is not there.
2. **`fail`.** Passes when `editorcheck "$FIX/fail" "$FIX/fail-reply.md"
   fail; echo $?` prints `editor check ok: VERDICT: FAIL
   qc/sides/skillet-green-beans-with-lemon-and-garlic/<date>.md` then `0`,
   and the orchestrator, reading the report and the reply, answers yes to
   both: the discrepancy table names the three planted differences and
   reports no difference that is not there; and the reply's Next step says
   that the writer fixes the card and a fresh editor checks it again.

What `editorcheck` proves, in order: exactly one file exists under `qc/`,
at `qc/sides/<slug>/<YYYY-MM-DD>.md`, named for a real date that is not the
packet's and that the report's own Date line repeats; `git status` shows only the fixture
card, the fixture's changed index, and the new report, no commit was made,
and the card, the packet, and the index are byte for byte what the setup
wrote, so the editor edited nothing; the report holds exactly one `VERDICT:`
line, a passing one for `pass` and `VERDICT: FAIL` for `fail`, and exactly
one `Card-SHA256:` line, equal to the card's hash; the report opens with
`# Editor report:` and the recipe's title, has the six labels above its
first heading, the three headings `Discrepancies`, `Additions`, and `Checks
run` in that order, the card's path, and ten lines under Checks run; for
`pass` no row of the table says `blocking`, and for `fail` one blocking row
holds both `1/4` and `1/2`, another holds both `2 min` and `4 min` (which
`2 minutes` and `4 minutes` satisfy), and a third holds `cooked-once`; no sentence of 70 characters or more from the approved
text appears in the report, and the Editor line names no chef or cook;
`scripts/check-qc.sh --working-tree --base fixture-start`, run in the
scratch repository, prints `qc checked: 1` and exits 0 for `pass`, and for
`fail` prints the card's path, the report's path, and `the verdict is FAIL`
and exits 1; and the reply has the four headings `Verdict`, `Report`,
`Discrepancies`, and `Next step` in that order, its Verdict section is the
report's verdict line, its Report section names the report's path, and, for
`fail`, its Next step holds the word `fresh` in any letter case.

A check that fails is not repaired by editing the scratch repository or the
reply. The orchestrator makes a new scratch repository for that one check in
a new directory, `RETRY=$(mktemp -d)` then `fixture "$RETRY" pass` or
`fixture "$RETRY" fail`, leaving `$FIX` and the other check's result as they
are, and starts a new fresh subagent there, once, saving its reply under
`$RETRY` and running `editorcheck` on `$RETRY/<name>`. A second failure of the same check is
reported as ``Question: the <pass | fail> behavior check of
`docs/specs/S005-editor-gate.md` failed twice: <the check's output>; revise
the spec?`` The skill files are not edited to make a check pass.

Leg 1 rehearsed both checks on 2026-11-19 with fresh orchestrator-tier
subagents briefed exactly as above, on files built in a scratch clone at
`base_sha` (L003). There were two rounds, and both checks passed on their
first run in each. On the first draft, `editorcheck` printed `editor check
ok: VERDICT: PASS
qc/sides/skillet-green-beans-with-lemon-and-garlic/2026-11-19.md` for `pass`
and the same line with `VERDICT: FAIL` for `fail`, whose table held exactly
the three planted rows, each `blocking`. After the cross-examination edits,
two new fresh subagents ran both checks on the files this spec gives,
against the stricter helper, with the same two lines and the same three
rows. Leg 1 answered yes to the three reading questions on
the passing runs. One run is a sample, which is why a failed check in leg 2
gets one more fresh run before it is a question.

#### Fixture: `packet`

````markdown
# Source packet: Skillet Green Beans with Lemon and Garlic

- **Card:** recipes/sides/skillet-green-beans-with-lemon-and-garlic.md
- **Kind of save:** new card
- **Date:** 2026-11-10
- **Where the approved text came from:** this conversation on 2026-11-10

## Approved text

~~~~
Skillet Green Beans with Lemon and Garlic (serves 2 as a side)

Equipment: 12-inch skillet with a lid.

Ingredients: 12 oz green beans, trimmed; 1 tbsp olive oil; 1/4 tsp kosher salt; 2 tbsp water; 2 cloves garlic, thinly sliced; 1 tbsp unsalted butter; 2 tsp lemon juice; black pepper to taste.

Method: 1. Heat the oil in the skillet over medium-high heat until it shimmers. Add the beans and the salt and cook, stirring once or twice, until blistered in spots, about 4 minutes. 2. Add the water, cover, and steam until the beans are bright green and crisp-tender, about 2 minutes. 3. Uncover, lower the heat to medium, add the garlic and the butter, and cook, stirring, until the garlic is fragrant and pale gold, about 1 minute. 4. Off the heat, stir in the lemon juice. Season with pepper, taste, and serve.

Time: about 15 minutes.

Why it works: the garlic goes in after the steam so it cannot scorch while the beans blister, and the lemon juice goes in off the heat so it stays bright.

Storage: refrigerate leftovers in a covered container and reheat them in a hot skillet.
~~~~

## Scope instruction

~~~~
The council pressure-tested this one with me and I approved the final text below. Save it as a new card in sides. I have not cooked it yet.
~~~~

## Previous version

None: this is a new card.

## Paths

- Card: recipes/sides/skillet-green-beans-with-lemon-and-garlic.md
- Previous card: none
- Cook logs: none
- Index: recipes/INDEX.md
- This packet: .sources/skillet-green-beans-with-lemon-and-garlic/2026-11-10.md
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

#### Helper: `editorcheck`

A gate helper, not a repository file.

````bash
editorcheck() {
  python3 - "$@" <<'PY'
import datetime, glob, hashlib, os, re, subprocess, sys
root, reply_path, want = sys.argv[1:4]
SLUG = "skillet-green-beans-with-lemon-and-garlic"
CARD = "recipes/sides/%s.md" % SLUG
PACKET = ".sources/%s/2026-11-10.md" % SLUG
CARD_SHA = {
    "pass": "5519fcf29eeecc3b13e17b0ed26771fa41940040785d045daf66a4b0d461330f",
    "fail": "47bbfcee00ddf3d79197c3631d70336c45503b6f0d42a8ae0c56c5f95609f339",
}[want]
bad = []
def fail(text):
    bad.append(text)
def read(path):
    return open(path, encoding="utf-8").read()
def run(*command):
    return subprocess.run(command, cwd=root, capture_output=True, text=True)
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
reply = read(reply_path)

# 1. One report, at the path the report format gives.
reports = sorted(
    os.path.relpath(path, root)
    for path in glob.glob(os.path.join(root, "qc", "**", "*"), recursive=True)
    if os.path.isfile(path)
)
if len(reports) != 1 or not re.fullmatch(r"qc/sides/%s/\d{4}-\d{2}-\d{2}\.md" % SLUG, reports[0]):
    print("expected one report qc/sides/%s/<YYYY-MM-DD>.md, found %s" % (SLUG, reports))
    sys.exit(1)
report_path = reports[0]
report_date = os.path.basename(report_path)[:-3]
try:
    datetime.date.fromisoformat(report_date)
except ValueError:
    fail("the report is named for %s, which is not a date" % report_date)
if report_date == "2026-11-10":
    fail("the report is named for the packet's date, not the day of the check")
report = read(os.path.join(root, report_path))
lines = [line.rstrip() for line in report.split("\n")]

# 2. The editor changed nothing else and committed nothing.
status = sorted(run("git", "status", "--porcelain", "--untracked-files=all").stdout.splitlines())
if status != sorted([" M recipes/INDEX.md", "?? " + CARD, "?? " + report_path]):
    fail("git status shows %s" % status)
if run("git", "rev-parse", "HEAD").stdout != run("git", "rev-parse", "fixture-start").stdout:
    fail("a commit was made")
card_sha = hashlib.sha256(open(os.path.join(root, CARD), "rb").read()).hexdigest()
if card_sha != CARD_SHA:
    fail("the card was changed")
if hashlib.sha256(open(os.path.join(root, PACKET), "rb").read()).hexdigest() != (
    "57c818c1e11c180ff52ef5f0cc31e1219cff306402631b1ac9afff8f3e3ee270"
):
    fail("the packet was changed")
if run("python3", "scripts/build-index.py", "--check").stdout != "index current: 1\n":
    fail("the index was changed")

# 3. The two lines the gate reads.
verdicts = [line for line in lines if line.startswith("VERDICT:")]
hashes = [line for line in lines if line.startswith("Card-SHA256:")]
passing = ["VERDICT: PASS", "VERDICT: PASS WITH NOTES"]
if len(verdicts) != 1:
    fail("the report has %d VERDICT lines" % len(verdicts))
elif want == "pass" and verdicts[0] not in passing:
    fail("the verdict line is %r, expected a pass" % verdicts[0])
elif want == "fail" and verdicts[0] != "VERDICT: FAIL":
    fail("the verdict line is %r, expected VERDICT: FAIL" % verdicts[0])
if hashes != ["Card-SHA256: " + CARD_SHA]:
    fail("the Card-SHA256 lines are %s" % hashes)

# 4. The form of the report.
if not lines[0].startswith("# Editor report: Skillet Green Beans with Lemon and Garlic"):
    fail("the report's first line is %r" % lines[0])
rsections, rorder = sections(report)
if rorder != ["Discrepancies", "Additions", "Checks run"]:
    fail("the report's ## headings are %s" % rorder)
top = report.split("\n## ")[0]
for label in ["Card", "Date", "Kind of save", "Source", "Packet", "Editor"]:
    if len(re.findall(r"(?m)^- \*\*%s:\*\* \S" % label, top)) != 1:
        fail("the report lacks one %s line above its first heading" % label)
if CARD not in top:
    fail("the report does not give the card's path")
if re.findall(r"(?m)^- \*\*Date:\*\* (.*)$", top) != [report_date]:
    fail("the report's Date line is not the date in its file name")
checks = [line for line in rsections.get("Checks run", "").split("\n") if line.startswith("- ")]
if len(checks) != 10:
    fail("Checks run has %d lines, expected 10" % len(checks))

# 5. The discrepancies.
rows = [
    line for line in rsections.get("Discrepancies", "").split("\n")
    if line.startswith("|") and not re.fullmatch(r"[|\s:-]+", line) and "Severity" not in line
]
blocking = [row for row in rows if "blocking" in row]
if want == "pass":
    if blocking:
        fail("a faithful card got blocking rows: %s" % blocking)
    if not rows and rsections.get("Discrepancies") != "None.":
        fail("Discrepancies is neither a table nor None.")
else:
    tests = [
        ("salt amount", lambda row: "1/4" in row and "1/2" in row),
        ("steam time", lambda row: re.search(r"\b2 min", row) and re.search(r"\b4 min", row)),
        ("evidence", lambda row: "cooked-once" in row),
    ]
    named = []
    for name, test in tests:
        hits = [row for row in blocking if test(row)]
        if not hits:
            fail("no blocking row names the planted %s" % name)
        named.append(hits[0] if hits else None)
    if len(set(named)) != 3:
        fail("the three planted differences do not each have a row of their own")

# 6. The approved text is not copied into the report, and no one is named.
packet = read(os.path.join(root, PACKET))
approved = packet.split("~~~~")[1]
for sentence in re.split(r"(?<=[.;])\s+", approved):
    if len(sentence) >= 70 and sentence in report:
        fail("the report copies the approved text: %r" % sentence[:40])
editor = re.findall(r"(?m)^- \*\*Editor:\*\* (.*)$", top)
if editor and re.search(r"(?i)\b(chef|cook|lens)\b", editor[0]):
    fail("the Editor line names a chef, a cook, or a lens: %r" % editor[0])

# 7. The gate agrees.
gate = run("bash", "scripts/check-qc.sh", "--working-tree", "--base", "fixture-start")
if want == "pass" and (gate.returncode, gate.stdout) != (0, "qc checked: 1\n"):
    fail("the gate printed %r and exited %d" % (gate.stdout + gate.stderr, gate.returncode))
if want == "fail" and (gate.returncode, gate.stdout) != (
    1, "%s: %s: the verdict is FAIL\n" % (CARD, report_path)
):
    fail("the gate printed %r and exited %d" % (gate.stdout + gate.stderr, gate.returncode))

# 8. The reply.
psections, porder = sections(reply)
if porder != ["Verdict", "Report", "Discrepancies", "Next step"]:
    fail("the reply's ## headings are %s" % porder)
if verdicts and psections.get("Verdict", "").strip("`\n ") != verdicts[0]:
    fail("the reply's Verdict section is %r" % psections.get("Verdict"))
if report_path not in psections.get("Report", ""):
    fail("the reply's Report section lacks the report's path")
if want == "fail" and "fresh" not in psections.get("Next step", "").lower():
    fail("the reply's Next step does not ask for a fresh check")

if bad:
    print("\n".join(bad)); sys.exit(1)
print("editor check ok: %s %s" % (verdicts[0], report_path))
PY
}
````

## Build plan — agent loop

Run every command from the repository root, in one Bash shell in which the
setup has been run first: the two lines below, then the `block` and
`extract` definitions of `### Writing a file from this spec`, pasted as
written, then the two `eval` lines, which load the other helpers from this
spec's own text.

```bash
OUT=$(mktemp)
SPEC="$(git rev-parse --show-toplevel)/docs/specs/S005-editor-gate.md"
```

```bash
eval "$(block '### Link check')"
eval "$(block '#### Helper: `editorcheck`')"
```

Afterward `type -t block extract linkcheck editorcheck` prints `function`
four times. A gate passes only when every command in it prints what is
stated. Where a gate ends in `; echo $?`, the printed status is part of the
expected output, and a non-zero status that is expected is not a failure.
The gate's commands run in the order listed, on the finished work before it
is committed; nothing is staged until a line says `after git add`, and from
that line on the task's Touches are staged. The commit follows the last
line, except where a line says it runs after the commit.

Baseline, measured by leg 1 on 2026-11-19 in a scratch clone at `base_sha`:
`python3 -m unittest discover -s tests -v` exits 0 and ends `OK` with 117
tests; `python3 scripts/check-skills.py` prints `skills checked: 3`;
`python3 scripts/check-council.py` prints `council checked: 14 seated, 14
records`; `python3 scripts/build-index.py --check` prints `index current:
0`; `linkcheck AGENTS.md` prints nothing. Every other gate line names a file
this spec creates or changes, so it is red on the base by design; none
measures old debt. Leg 1 then built Tasks 1 to 4 in that clone from this
spec with `extract` and ran every gate line below except the lines that need
the commits of this run (the `TASK1_SHA` lines), loading the helpers by the
setup above, and ran the privacy sweep's `--text` on every file this spec
gives.

Mutation probe (L004), run by leg 1 on 2026-11-19 in the same clone: 83
one-line changes to the first draft of the three scripts (40 to
`scripts/check-qc.sh`, 37 to `scripts/lint-cards.py`, 6 to
`scripts/install-git-hooks.sh`), each run against the three new test
modules. The first draft of the tests caught 71.
Leg 1 added six tests and extended two, which caught seven of the twelve
survivors (a gate line mentioned inside another line, a card-like path outside
`recipes/`, the default mode reading the commit, `--working-tree` from a
subfolder, one order for tracked and untracked cards, a base that names a
file, and the place of a linked folder in the output). The other five
survive because they change no output on any input leg 1 could build, and
are accepted: dropping `--no-renames` (with `--name-only` git prints the
new path either way); accepting a title line of `# ` and spaces, and
dropping `has no title line` beside `has no front matter` (the index check
that follows prints the same line for the same card); matching the date
pattern at the start only (the date parse then rejects the rest); and not
skipping a `#` target (it resolves to the card's own folder, which exists).
After the cross-examination edits, eight more changes to the lines those
edits touched (the Stop hook's JSON match, the portable sort, the closing
fence, the root-relative link, and the two link forms) were all caught.
Those edits added one test (a line break in a card's name) and extended
two.
One branch has no test: `shasum` in place of `sha256sum` (decision 9).

### Task 1 — Add the tests for the gate, the linter, and the hook installer
- **Work:** Create `tests/test_check_qc.py`, `tests/test_lint_cards.py`, and
  `tests/test_install_git_hooks.py` with exactly the content given under
  their `#### File:` headings. The seams under test are three commands,
  each observed only through its standard output, standard error, and exit
  status, in repositories the tests build in temporary directories:
  `scripts/check-qc.sh` (decisions 4 to 10), `python3 scripts/lint-cards.py`
  (decision 12), and `scripts/install-git-hooks.sh`, for which the hook file
  it writes and what `git commit` then does are observed too (decision 11).
  Expected lines are literals written from those decisions.
  - `tests/test_check_qc.py` catches: the ticket's four cases (no report, a
    stale hash, a FAIL report, a current passing report); `PASS WITH NOTES`
    passing; the hash of the edited card being the one that counts; a failed
    report beside a later passing one; every failing report named when none
    passes; a missing, repeated, unfilled, or misplaced verdict line; a
    missing, repeated, or malformed hash line; Windows line endings and
    trailing spaces; an untouched report not counting; the same slug in two
    categories needing two reports; a report keyed by slug alone, nested,
    hidden, not Markdown, or in a folder whose name only starts the same not
    counting; names with pattern characters, a space, or an accent; which
    paths are cards; a deleted and a moved card; changes counted from the
    merge base; uncommitted changes ignored by default; a missing base, the
    base from the environment and from the option, the default base, a base
    of zeros, unrelated histories, no repository, and no commit; running
    from a subfolder; the three `--staged` behaviors and the two
    `--working-tree` ones; the four `--stop-hook` behaviors; `--hash`; and
    the usage errors.
  - `tests/test_lint_cards.py` catches each problem line of decision 12,
    the values that are allowed, which files are cards, the order of the
    output, the index line, an unfilled copy of `templates/recipe-card.md`
    failing, the usage errors, and this repository's own cards linting
    clean.
  - `tests/test_install_git_hooks.py` catches: the hook's exact bytes and
    its executable bit; installing twice; installing from another folder; a
    foreign hook left alone; `core.hooksPath`; the usage error; no
    repository; and the installed hook stopping a card commit with no
    report, allowing one with a current passing report, and stopping one
    when the index is stale.
- **Touches:** `tests/test_check_qc.py`, `tests/test_lint_cards.py`,
  `tests/test_install_git_hooks.py`
- **Gate:**
  - This prints three lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    2b188763c5acb7de4f5c5f8a6860e720e497874d615c8d66b674862b340a53ee  tests/test_check_qc.py
    37eac472a8a6251380f0ab0f2dd4781306611fefb3fda8a08cafe59aa75e1686  tests/test_lint_cards.py
    92aa6f5dd590ea3e61174e2c75126afaea1dec62cc334cc73c69aa097c602ac8  tests/test_install_git_hooks.py
    SUMS
    ```

  - With the working tree differing from `base_sha` only under `docs/` and
    in these three test files, `python3 -m unittest discover -s tests -v >
    "$OUT" 2>&1; echo $?` prints `1`, `tail -1 "$OUT"` prints `FAILED (failures=153)`,
    and `grep -c ' ok$' "$OUT"` prints `117`. This is the recorded red:
    leg 1 measured it on 2026-11-19 in a scratch clone at `base_sha` with
    only the three test files applied. All 108 new test methods fail (56 in `CheckQcTest`, 41 in
    `LintCardsTest`, 11 in `InstallGitHooksTest`), each by assertion,
    because the three scripts do not exist yet: `bash` and `python3` exit
    with their own status for a missing file and print none of the expected
    lines. None is an error and none is an import error. `failures=153` is
    more than 108 because unittest counts each failing subtest, and ten of
    the methods loop over subtests. `grep -cE
    '\((test_check_qc|test_lint_cards|test_install_git_hooks)\..*\) \.\.\.
    ok$' "$OUT"` prints `0`: no new test passes on the base. The 117 `ok`
    lines are the tests the base already has.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
    tests/test_check_qc.py tests/test_lint_cards.py
    tests/test_install_git_hooks.py` ends with a line beginning `privacy
    sweep: clean` and exits 0.
- **Nature:** mechanical

### Task 2 — Add the editor gate, the card linter, and the hook installer
- **Work:** Create `scripts/check-qc.sh`, `scripts/lint-cards.py`, and
  `scripts/install-git-hooks.sh` with exactly the content given under their
  `#### File:` headings. Then run `chmod +x scripts/check-qc.sh
  scripts/install-git-hooks.sh`; `scripts/lint-cards.py` stays without the
  executable bit, like the other Python scripts. Do not run
  `scripts/install-git-hooks.sh` in this repository. Do not change anything
  under `tests/`; a test that seems to need a change is reported as
  ``Question: Task 2 of `docs/specs/S005-editor-gate.md` needs a test the
  tests task wrote changed; revise the spec?``
- **Touches:** `scripts/check-qc.sh`, `scripts/lint-cards.py`,
  `scripts/install-git-hooks.sh`
- **Gate:**
  - This prints three lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    bd3451f41898a0407d67f4fdd399b4fd76a3c6b226189f1da0fc0a0430d98d17  scripts/check-qc.sh
    8b7b18e00f7ad6c333638cb9e517f14806517fc2f05c8c100357edf93c0f8d1f  scripts/lint-cards.py
    e810839e1e2c169db95b7936d841f1fd7344f0f3a537c81758886a3cfbb86490  scripts/install-git-hooks.sh
    SUMS
    ```

  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
    prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
    prints `225`.
  - `python3 scripts/lint-cards.py; echo $?` prints `cards checked: 0` then
    `0`.
  - After `git fetch origin`, `scripts/check-qc.sh; echo $?` prints `qc
    checked: 0` then `0`, and `scripts/check-qc.sh --working-tree; echo $?`
    prints the same.
  - `scripts/check-qc.sh --base no-such-branch; echo $?` prints `check-qc:
    base no-such-branch not found: fetch it, or name another with --base or
    QC_BASE` then `2`.
  - `grep -qxF '# chef-council pre-commit hook' "$(git rev-parse --git-path
    hooks/pre-commit)" 2>/dev/null; echo $?` prints `1` or `2`, never `0`:
    this spec's hook was not installed here. A pre-commit hook of the
    maintainer's own is not this spec's concern.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
    scripts/check-qc.sh scripts/lint-cards.py scripts/install-git-hooks.sh`
    ends with a line beginning `privacy sweep: clean` and exits 0.
  - After `git add scripts/check-qc.sh scripts/lint-cards.py
    scripts/install-git-hooks.sh`, `git ls-files -s scripts/check-qc.sh
    scripts/install-git-hooks.sh scripts/lint-cards.py` prints three lines,
    beginning `100755`, `100755`, and `100644` in that order.
  - The tests are unchanged. Before the commit, `git status --porcelain --
    tests/` prints nothing. After it, this prints only `tests unchanged`:

    ```bash
    TASK1_SHA=$(git log --format=%H -1 --grep='^Spec-Task: S005/1$')
    [ -n "$TASK1_SHA" ] && git merge-base --is-ancestor "$TASK1_SHA" HEAD &&
      [ -z "$(git diff --name-only "$TASK1_SHA..HEAD" -- tests/)" ] &&
      echo "tests unchanged"
    ```
- **Nature:** mechanical

### Task 3 — Add the recipe-editor skill with its report format, wrapper, method page, link, and index line
- **Work:** Create `.agents/skills/recipe-editor/SKILL.md`,
  `.agents/skills/recipe-editor/references/report-format.md`,
  `.claude/agents/recipe-editor.md`, and `method/recipe-qc.md` with exactly
  the content given under their `#### File:` headings. Create the link, from
  the repository root:

  ```bash
  ln -s ../../.agents/skills/recipe-editor .claude/skills/recipe-editor
  ```

  In `AGENTS.md`, make exactly these two changes and nothing else.

  Directly after the line that begins ``- `cook-log`:``, insert this line:

  ```text
  - `recipe-editor`: [`.agents/skills/recipe-editor/SKILL.md`](.agents/skills/recipe-editor/SKILL.md). Use it only in a fresh context that did not write the card, to check a new or changed card against its source packet and write the editor report.
  ```

  Directly after the line that begins ``  - `scripts/secret-scan.sh`:``,
  insert these two lines, each indented by two spaces like that line:

  ```text
    - `python3 scripts/lint-cards.py`: the cards are well formed and the index is current.
    - `scripts/check-qc.sh`: each changed card has a current passing editor report.
  ```
- **Touches:** `.agents/skills/recipe-editor/SKILL.md`,
  `.agents/skills/recipe-editor/references/report-format.md`,
  `.claude/skills/recipe-editor`, `.claude/agents/recipe-editor.md`,
  `method/recipe-qc.md`, `AGENTS.md`
- **Gate:**
  - This prints five lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    4131bcd27fdd03e9b236babdc16cdc375ea717c002db3a78949bb1a16ac8acf9  .agents/skills/recipe-editor/SKILL.md
    29fa84b8c682f6444c5e90c425d0f909d88189be0390eb8b994b37c5191d2dd3  .agents/skills/recipe-editor/references/report-format.md
    d2d9e928ceae66c94fed230fb4e7252d31ef37678e4848d1b66af70b49e132e9  .claude/agents/recipe-editor.md
    3b08937672463f6242681f9a5178dc6b4fb845dd32dbfbe1434cbbf32f45cf2b  method/recipe-qc.md
    129f4344ea97173387d287cd31435537c6a3da468bb0d53970f9e281806bafaf  AGENTS.md
    SUMS
    ```

  - `readlink .claude/skills/recipe-editor` prints
    `../../.agents/skills/recipe-editor`.
  - `git diff --numstat HEAD -- AGENTS.md` prints one line: `3`, `0`, and
    `AGENTS.md`, separated by tabs. `wc -c < AGENTS.md` prints `8166`.
  - `git status --porcelain --untracked-files=all` prints exactly these six
    lines:

    ```text
     M AGENTS.md
    ?? .agents/skills/recipe-editor/SKILL.md
    ?? .agents/skills/recipe-editor/references/report-format.md
    ?? .claude/agents/recipe-editor.md
    ?? .claude/skills/recipe-editor
    ?? method/recipe-qc.md
    ```

  - `python3 scripts/check-skills.py; echo $?` prints `skills checked: 4`
    then `0`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
    prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
    prints `225`.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text AGENTS.md
    .agents/skills/recipe-editor/SKILL.md
    .agents/skills/recipe-editor/references/report-format.md
    .claude/agents/recipe-editor.md method/recipe-qc.md` ends with a line
    beginning `privacy sweep: clean` and exits 0.
  - After `git add` of the six Touches, `git ls-files -s
    .claude/skills/recipe-editor` prints a line beginning `120000`, and
    `linkcheck AGENTS.md .agents/skills/recipe-editor/SKILL.md
    .agents/skills/recipe-editor/references/report-format.md
    method/recipe-qc.md; echo $?` prints `0` and nothing else.
  - The tests are unchanged, checked as in Task 2: before the commit `git
    status --porcelain -- tests/` prints nothing, and after it the
    `TASK1_SHA` block of Task 2 prints only `tests unchanged`.
- **Nature:** mechanical

### Task 4 — Add the Stop hook, the CI steps for the gate and the linter, and the profile's check lines
- **Work:** Create `.claude/settings.json` with exactly the content given
  under its `#### File:` heading. In `.github/workflows/ci.yml`, append the
  text given under `#### Addition: .github/workflows/ci.yml` to the end of
  the file, directly after its last line (`        run: python3 -m unittest
  discover -s tests -v`), and change nothing else. In
  `.agents/spec-profile.md`, replace the one line

  ```text
      -v` (its last line is `OK`), and
  ```

  with these six lines, and change nothing else:

  ```text
      -v` (its last line is `OK`), `python3 scripts/lint-cards.py` (prints
      `cards checked: <N>` and exits 0), `scripts/check-qc.sh` (the editor
      gate against `origin/main`, after `git fetch origin`: prints `qc checked:
      <N>` and exits 0, exit 1 when a changed card lacks a current passing
      report, and exit 2 when the check could not run, which never counts as
      clean), and
  ```
- **Touches:** `.claude/settings.json`, `.github/workflows/ci.yml`,
  `.agents/spec-profile.md`
- **Gate:**
  - This prints three lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    dacf9c6bb99e80c0494f243519dc24e25d9b2780e8126ddeaf0b5ebb0df7309e  .claude/settings.json
    3b1879f59b4357dec413d25017e81e8800e3fb627836aaefbf210c510aa42bf4  .github/workflows/ci.yml
    39ec76d8042ca822bebc856255ec16ece3af8121c5ad22776f814dbb083fdbbd  .agents/spec-profile.md
    SUMS
    ```

  - `git diff --numstat HEAD -- .github/workflows/ci.yml
    .agents/spec-profile.md` prints two lines: `6`, `1`, and
    `.agents/spec-profile.md`, then `24`, `0`, and
    `.github/workflows/ci.yml`, each separated by tabs.
  - `grep -c 'uses: ' .github/workflows/ci.yml` prints `3`, and `grep -c
    'uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 #
    v7.0.1' .github/workflows/ci.yml` prints `3`: every action is pinned by
    commit.
  - `python3 -c 'import json; print(json.load(open(".claude/settings.json"))["hooks"]["Stop"][0]["hooks"][0]["command"])'`
    prints `cd "$CLAUDE_PROJECT_DIR" && scripts/check-qc.sh --stop-hook`.
  - `echo '{"stop_hook_active": false}' | scripts/check-qc.sh --stop-hook;
    echo $?` prints `0` and nothing else.
  - The two commands the new CI steps run pass here: `python3
    scripts/lint-cards.py; echo $?` prints `cards checked: 0` then `0`, and
    `EVENT_NAME=pull_request PR_BASE=main bash -c 'if [ "$EVENT_NAME" =
    "pull_request" ]; then scripts/check-qc.sh --base "origin/$PR_BASE";
    else scripts/check-qc.sh --base "$PUSH_BEFORE"; fi'; echo $?` prints `qc
    checked: 0` then `0`. With `PUSH_BEFORE` set to `git rev-parse
    origin/main`, `EVENT_NAME=push` in place of `pull_request` prints the
    same.
  - `"$(git rev-parse --git-common-dir)/info/privacy-sweep" --text
    .claude/settings.json .github/workflows/ci.yml .agents/spec-profile.md`
    ends with a line beginning `privacy sweep: clean` and exits 0.
  - The tests are unchanged, checked as in Task 2: before the commit `git
    status --porcelain -- tests/` prints nothing, and after it the
    `TASK1_SHA` block of Task 2 prints only `tests unchanged`.
- **Nature:** mechanical

After Task 4's commit, the push, and the pull request, the orchestrator
observes definition-of-done items 1 to 8. Items 5 to 8 need the pushed
branch, so they are not part of any task's gate.

## Repo profile

`.agents/spec-profile.md` applies as written, with the six lines Task 4
adds to its check list. Additions for this spec only:

- The pull request's Evidence section holds the two replies and the two
  reports as definition-of-done item 8 says, the recorded red of Task 1
  beside the green of Task 2 (the two `tail -1` lines), and the three `grep`
  results of item 5.
- The pull request's Merge Danger section says that the change adds files,
  three lines of `AGENTS.md`, six lines of the profile, and one CI job and
  one CI step, and removes nothing; that from the merge on, a pull request
  that adds or changes a card without a current passing editor report fails
  CI, and so does a card the linter rejects; that the push-to-`main` path of
  the `editor gate` job runs for the first time on the merge itself, where
  it compares the merge with the commit `main` pointed at before; that a
  Claude Code session in the repository runs the Stop hook from then on; and
  that reverting the merge removes the gate, the linter, the hooks, the
  skill, and the method page, and restores `AGENTS.md`, the workflow, and
  the profile.
- The cross-examination dossier holds this spec, `AGENTS.md`, the profile,
  the ticket, `.github/workflows/ci.yml`, `.agents/skills/README.md`, the
  `recipe-codify` skill's `SKILL.md` (its hand-off section is what the
  editor receives), `templates/source-packet.md`,
  `templates/recipe-card.md`, `method/status-and-versions.md`,
  `scripts/build-index.py`, `scripts/check-skills.py`, and `.gitignore`;
  every new file is already in the spec. It does not hold the other tests,
  `scripts/check-council.py`, or the vetting records, so the counts this
  spec states from them are leg 1's measurements in a scratch clone at
  `base_sha`: 117 tests before and 225 after, and `council checked: 14
  seated, 14 records`.

## Cross-examination

One round, on the complete first draft, on 2026-11-19: Meta
`muse-wonder-full-1.0` (architect tier) at high reasoning effort, through
Muse Code 1.4.15 (1.4.15-R8339.1) in the read-only sandbox of the
maintainer's routes document. The dossier held the draft, the ticket, and
the files `## Repo profile` lists, and passed the privacy sweep's `--text`
and a gitleaks scan before it was sent. The reviewer reported eleven tools,
all read-only or session-local, with no shell, write, or web tool, and it
could read only the dossier. It returned 17 findings and no finding on task
size. All 17 were accepted, two of them in part; none was dropped. After the
edits leg 1 rebuilt the scratch clone from this spec, ran every gate again,
re-measured the red and the green, and rehearsed both behavior checks again
on the final bytes.

1. **ACCEPT** (blocking: the chat path left out the status rules). The cook
   now pastes `method/status-and-versions.md` as a sixth item, and the
   prompt, the method page, and decision 17 say six.
2. **ACCEPT** (blocking: a refusing editor had no reply form, and the
   wrapper's "path is missing" could be read against the skill). The skill
   gives the refusal one line starting `Not independent:` and says the four
   headings do not apply; the wrapper stops only when the brief leaves a
   path out and defers to the skill when a named file is absent.
3. **ACCEPT** (blocking: no values for a report with no packet). The report
   format gives `not stated` for Kind of save and Source, the given path or
   `none` for Packet, and `not checked, because there is no verbatim source`
   for the checks that need the approved text.
4. **ACCEPT** (blocking: the linter's fence and link reading). A fence now
   closes at a line of the same character at least as long as its opening
   line; links with a title or in angle brackets are read; a target that
   starts with `/` is read from the repository root. Decision 12 names the
   forms read and says reference-style links are not. The link test covers
   each case.
5. **ACCEPT in part** (blocking: the helper's planted-row tests). The Next
   step test now ignores letter case. The other half is rejected: the
   pattern `2 min` already matches `2 minutes`, which is what both
   rehearsal reports wrote; the description of the helper now says so.
6. **ACCEPT** (the helper's date and rows). The report's name must be a real
   date, not the packet's, and equal to the report's Date line, and the
   three planted differences must be three different rows.
7. **ACCEPT in part** (the Stop hook's JSON). The script now joins the
   lines of its input before looking for `stop_hook_active`, and a test
   feeds it pretty-printed JSON. Reading the input before the arguments is
   rejected: the script cannot know it is a hook until it has read them,
   the shipped command has no usage error, and decision 10 records the
   case.
8. **ACCEPT** (`sort -z` is not portable). The script sorts with a plain
   `sort` by swapping NUL and newline around it; a test with a line break
   in a card's name covers the swap.
9. **ACCEPT** (the gate accepts any report file name). Decision 3 now says
   the folder is the key and the name is a convention the gate does not
   read.
10. **ACCEPT** (which packet, and which logs). The skill says the paths come
    from whoever asks and are never chosen by the editor, and that the logs
    counted are those in `cook-logs/<slug>/` when the editor can list files.
11. **ACCEPT** (two skill behaviors have no behavior check). Decision 22
    records the refusal and the missing packet as unexercised, beside the
    other limits.
12. **ACCEPT** (item 5 did not wait for CI). It now watches the checks and
    finds the run by the pull request's head commit.
13. **ACCEPT** (a retry would overwrite the other check). The setup is a
    `fixture` function, and a retry builds one repository in a new
    directory.
14. **ACCEPT** (a chat reply saved whole would hold two verdict lines). The
    method page says to save the report alone and where it starts and ends.
15. **ACCEPT** (the installer rewrites its own hook). The method page and
    decision 11 say so.
16. **ACCEPT** (an unreadable card still gets a duplicate-slug line).
    Decision 12 says so; the code is unchanged.
17. **ACCEPT** (gates assumed a clean checkout and no hook). A prerequisite
    requires a clean `git status` before Task 1, and Task 2's hook line now
    looks only for this spec's own hook.

## File contents

Each block below is one file, written as `### Writing a file from this
spec` says.

#### File: `tests/test_check_qc.py`

````python
"""Tests for scripts/check-qc.sh, observed through its output and its exit status.

Each test builds a small git repository in a temporary directory, with a
`main` branch as the base and a `work` branch holding the change, and runs the
gate inside it. The two card hashes are literals: `printf` the card's text into
`sha256sum` to check one.
"""

import os
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "check-qc.sh")
USAGE = (
    "usage: scripts/check-qc.sh [--staged | --working-tree | --stop-hook] "
    "[--base <revision>] | --hash <file>\n"
)
ZERO = "0" * 40

CARD = "# Rice\n\n1 cup rice, 2 cups water.\n"
CARD_SHA = "bc0feeb751693e214f4054db17543afff919bffeb32fca1458eec3ca7a1a7e2c"
EDITED = "# Rice\n\n1 cup rice, 3 cups water.\n"
EDITED_SHA = "ec1a382ed834b514954bd57e2e700984948a8748cf90e43267b7cf0328fc270a"
# SHA-256 of the three bytes "abc", from FIPS 180-2, appendix B.1.
ABC_SHA = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

RICE = "recipes/sides/rice.md"
RICE_REPORT = "qc/sides/rice/2026-11-19.md"
NO_REPORT = "%s: no editor report was added or changed under qc/sides/rice/"
STALE = "Card-SHA256 is not the hash of the card, so the card changed after this check"
ONE_VERDICT = "must hold exactly one line that starts with VERDICT:"
ONE_HASH = "must hold exactly one line that starts with Card-SHA256:"
BAD_VERDICT = "the VERDICT line is not PASS, PASS WITH NOTES, or FAIL"
BAD_HASH = "the Card-SHA256 line does not hold 64 lowercase hexadecimal digits"
SUMMARY = (
    "check-qc: %d of %d changed recipe cards lack a current passing editor report; "
    "method/recipe-qc.md says how to get one"
)
NO_BASE = "check-qc: base %s not found: fetch it, or name another with --base or QC_BASE"


def report(verdict="PASS", sha=CARD_SHA):
    return (
        "# Editor report: Rice v1.0\n"
        "\n"
        "```text\n"
        "VERDICT: %s\n"
        "Card-SHA256: %s\n"
        "```\n"
        "\n"
        "## Discrepancies\n"
        "\n"
        "None.\n"
    ) % (verdict, sha)


class CheckQcTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = os.path.realpath(self._tmp.name)
        self.root = os.path.join(self.tmp, "repo")
        os.makedirs(self.root)
        self.env = dict(os.environ)
        for name in ("QC_BASE", "CI", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            self.env.pop(name, None)
        self.env.update(
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_SYSTEM=os.devnull,
            GIT_AUTHOR_NAME="test",
            GIT_AUTHOR_EMAIL="test@example.invalid",
            GIT_COMMITTER_NAME="test",
            GIT_COMMITTER_EMAIL="test@example.invalid",
        )
        self.git("init", "-q", "-b", "main")
        self.write("README.md", "base\n")
        self.commit("Base")
        self.git("checkout", "-q", "-b", "work")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, env=self.env, capture_output=True, text=True, check=True
        ).stdout

    def write(self, path, text):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)

    def commit(self, message="Change"):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)

    def gate(self, *args, env=None, cwd=None, stdin=""):
        full = dict(self.env)
        full.update(env or {})
        return subprocess.run(
            ["bash", SCRIPT, *args],
            cwd=cwd or self.root,
            env=full,
            input=stdin,
            capture_output=True,
            text=True,
            check=False,
        )

    def passes(self, result, cards):
        self.assertEqual(result.stdout, "qc checked: %d\n" % cards)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 0)

    def fails(self, result, lines, lacking=1, cards=1):
        self.assertEqual(result.stdout.splitlines(), lines)
        self.assertEqual(result.stderr.splitlines(), [SUMMARY % (lacking, cards)])
        self.assertEqual(result.returncode, 1)

    def cannot_run(self, result, message):
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr.splitlines(), [message])
        self.assertEqual(result.returncode, 2)

    # The four cases the gate exists for.

    def test_card_change_with_no_report_fails(self):
        self.write(RICE, CARD)
        self.commit()
        self.fails(self.gate("--base", "main"), [NO_REPORT % RICE])

    def test_card_change_with_a_stale_hash_fails(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.commit()
        self.write(RICE, EDITED)
        self.commit("Edit the card after the check")
        self.fails(self.gate("--base", "main"), ["%s: %s: %s" % (RICE, RICE_REPORT, STALE)])

    def test_card_change_with_a_fail_report_fails(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report("FAIL"))
        self.commit()
        self.fails(
            self.gate("--base", "main"), ["%s: %s: the verdict is FAIL" % (RICE, RICE_REPORT)]
        )

    def test_card_change_with_a_current_passing_report_passes(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.commit()
        self.passes(self.gate("--base", "main"), 1)

    # What counts as a passing report.

    def test_pass_with_notes_passes(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report("PASS WITH NOTES"))
        self.commit()
        self.passes(self.gate("--base", "main"), 1)

    def test_the_hash_of_the_edited_card_is_the_one_that_counts(self):
        self.write(RICE, CARD)
        self.commit()
        self.write(RICE, EDITED)
        self.write(RICE_REPORT, report(sha=EDITED_SHA))
        self.commit()
        self.passes(self.gate("--base", "main"), 1)

    def test_a_fail_report_beside_a_later_passing_one_passes(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report("FAIL", sha=EDITED_SHA))
        self.write("qc/sides/rice/2026-11-19-2.md", report())
        self.commit()
        self.passes(self.gate("--base", "main"), 1)

    def test_every_failing_report_is_named_when_none_passes(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report("FAIL"))
        self.write("qc/sides/rice/2026-11-19-2.md", report(sha=EDITED_SHA))
        self.commit()
        self.fails(
            self.gate("--base", "main"),
            [
                "%s: qc/sides/rice/2026-11-19-2.md: %s" % (RICE, STALE),
                "%s: %s: the verdict is FAIL" % (RICE, RICE_REPORT),
            ],
        )

    def test_report_without_a_verdict_line_fails(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, "# Editor report\n\nCard-SHA256: %s\n" % CARD_SHA)
        self.commit()
        self.fails(
            self.gate("--base", "main"), ["%s: %s: %s" % (RICE, RICE_REPORT, ONE_VERDICT)]
        )

    def test_report_with_two_verdict_lines_fails(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, "VERDICT: FAIL\n" + report())
        self.commit()
        self.fails(
            self.gate("--base", "main"), ["%s: %s: %s" % (RICE, RICE_REPORT, ONE_VERDICT)]
        )

    def test_unfilled_or_misspelled_verdict_fails(self):
        for verdict in ("PASS | PASS WITH NOTES | FAIL", "pass", "PASSED", "PASS WITH NOTE", ""):
            with self.subTest(verdict=verdict):
                self.write(RICE, CARD)
                self.write(RICE_REPORT, report(verdict))
                self.commit()
                self.fails(
                    self.gate("--base", "main"),
                    ["%s: %s: %s" % (RICE, RICE_REPORT, BAD_VERDICT)],
                )

    def test_verdict_must_start_its_line(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, "- VERDICT: PASS\n- Card-SHA256: %s\n" % CARD_SHA)
        self.commit()
        self.fails(
            self.gate("--base", "main"), ["%s: %s: %s" % (RICE, RICE_REPORT, ONE_VERDICT)]
        )

    def test_mentions_inside_a_line_are_not_the_gate_lines(self):
        self.write(RICE, CARD)
        self.write(
            RICE_REPORT,
            report() + "\n| Report | the VERDICT: FAIL line | the Card-SHA256: line | minor |\n",
        )
        self.commit()
        self.passes(self.gate("--base", "main"), 1)

    def test_report_without_a_hash_line_fails(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, "VERDICT: PASS\n")
        self.commit()
        self.fails(self.gate("--base", "main"), ["%s: %s: %s" % (RICE, RICE_REPORT, ONE_HASH)])

    def test_report_with_two_hash_lines_fails(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report() + "Card-SHA256: %s\n" % CARD_SHA)
        self.commit()
        self.fails(self.gate("--base", "main"), ["%s: %s: %s" % (RICE, RICE_REPORT, ONE_HASH)])

    def test_hash_that_is_not_64_lowercase_hex_digits_fails(self):
        for sha in (CARD_SHA.upper(), CARD_SHA[:63], CARD_SHA + "0", "not computed", "sha256:" + CARD_SHA):
            with self.subTest(sha=sha):
                self.write(RICE, CARD)
                self.write(RICE_REPORT, report(sha=sha))
                self.commit()
                self.fails(
                    self.gate("--base", "main"), ["%s: %s: %s" % (RICE, RICE_REPORT, BAD_HASH)]
                )

    def test_windows_line_endings_and_trailing_spaces_are_read(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report().replace("PASS\n", "PASS  \n").replace("\n", "\r\n"))
        self.commit()
        self.passes(self.gate("--base", "main"), 1)

    # Which reports count for which card.

    def test_report_that_did_not_change_does_not_count(self):
        self.git("checkout", "-q", "main")
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.commit("Add the card on the base")
        self.git("checkout", "-q", "-B", "work")
        self.write(RICE, EDITED)
        self.commit()
        self.fails(self.gate("--base", "main"), [NO_REPORT % RICE])

    def test_same_slug_in_two_categories_needs_two_reports(self):
        self.write(RICE, CARD)
        self.write("recipes/mains/rice.md", CARD)
        self.write(RICE_REPORT, report())
        self.commit()
        self.fails(
            self.gate("--base", "main"),
            ["recipes/mains/rice.md: no editor report was added or changed under qc/mains/rice/"],
            lacking=1,
            cards=2,
        )
        self.write("qc/mains/rice/2026-11-19.md", report())
        self.commit()
        self.passes(self.gate("--base", "main"), 2)

    def test_report_keyed_by_slug_alone_does_not_count(self):
        self.write(RICE, CARD)
        self.write("qc/rice/2026-11-19.md", report())
        self.commit()
        self.fails(self.gate("--base", "main"), [NO_REPORT % RICE])

    def test_only_markdown_files_directly_in_the_report_folder_count(self):
        self.write(RICE, CARD)
        self.write("qc/sides/rice/old/2026-11-19.md", report())
        self.write("qc/sides/rice/2026-11-19.txt", report())
        self.write("qc/sides/rice/.2026-11-19.md", report())
        self.write("qc/sides/rice-pilaf/2026-11-19.md", report())
        self.commit()
        self.fails(self.gate("--base", "main"), [NO_REPORT % RICE])

    def test_slug_with_pattern_characters_is_matched_literally(self):
        card = "recipes/sides/r*ce.md"
        self.write(card, CARD)
        self.write(RICE_REPORT, report())
        self.commit()
        self.fails(
            self.gate("--base", "main"),
            ["%s: no editor report was added or changed under qc/sides/r*ce/" % card],
        )

    def test_card_with_a_line_break_in_its_name_is_checked(self):
        card = "recipes/sides/two\nlines.md"
        self.write(card, CARD)
        self.write("qc/sides/two\nlines/2026-11-19.md", report())
        self.write(RICE, CARD)
        self.commit()
        result = self.gate("--base", "main")
        self.assertEqual(result.stdout, NO_REPORT % RICE + "\n")
        self.assertEqual(result.stderr.splitlines(), [SUMMARY % (1, 2)])
        self.assertEqual(result.returncode, 1)

    def test_card_with_a_space_and_an_accent_in_its_name_is_checked(self):
        card = "recipes/sides/café rice.md"
        self.write(card, CARD)
        self.commit()
        self.fails(
            self.gate("--base", "main"),
            ["%s: no editor report was added or changed under qc/sides/café rice/" % card],
        )
        self.write("qc/sides/café rice/2026-11-19.md", report())
        self.commit()
        self.passes(self.gate("--base", "main"), 1)

    # Which files are cards, and which changes count.

    def test_no_card_changed_passes_with_zero(self):
        self.write("README.md", "changed\n")
        self.commit()
        self.passes(self.gate("--base", "main"), 0)

    def test_only_files_one_folder_down_are_cards(self):
        self.write("recipes/INDEX.md", "index\n")
        self.write("recipes/sides/deep/rice.md", CARD)
        self.write("recipes/.drafts/rice.md", CARD)
        self.write("recipes/sides/.rice.md", CARD)
        self.write("recipes/sides/rice.txt", CARD)
        self.write("templates/recipe-card.md", CARD)
        self.write("archive/recipes/sides/rice.md", CARD)
        self.commit()
        self.passes(self.gate("--base", "main"), 0)

    def test_deleted_card_needs_no_report(self):
        self.git("checkout", "-q", "main")
        self.write(RICE, CARD)
        self.commit("Add the card on the base")
        self.git("checkout", "-q", "-B", "work")
        self.git("rm", "-q", RICE)
        self.commit()
        self.passes(self.gate("--base", "main"), 0)

    def test_moved_card_needs_a_report_at_its_new_place(self):
        self.git("checkout", "-q", "main")
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.commit("Add the card on the base")
        self.git("checkout", "-q", "-B", "work")
        self.git("mv", RICE, "recipes/sides/plain-rice.md")
        self.commit()
        self.fails(
            self.gate("--base", "main"),
            ["recipes/sides/plain-rice.md: no editor report was added or changed under qc/sides/plain-rice/"],
        )

    def test_changes_are_counted_from_where_the_branch_left_the_base(self):
        self.git("checkout", "-q", "main")
        self.write("recipes/mains/stew.md", CARD)
        self.commit("Add an unchecked card on the base after the branch left")
        self.git("checkout", "-q", "work")
        self.write("README.md", "changed\n")
        self.commit()
        self.passes(self.gate("--base", "main"), 0)

    def test_uncommitted_changes_are_not_seen_by_default(self):
        self.write(RICE, CARD)
        self.passes(self.gate("--base", "main"), 0)
        self.git("add", "-A")
        self.passes(self.gate("--base", "main"), 0)

    def test_default_reads_the_commit_not_the_file(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.commit()
        self.write(RICE, EDITED)
        self.write(RICE_REPORT, report("FAIL"))
        self.passes(self.gate("--base", "main"), 1)

    # The base.

    def test_missing_base_cannot_run(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.commit()
        self.cannot_run(self.gate(), NO_BASE % "origin/main")
        self.cannot_run(self.gate(env={"CI": "true"}), NO_BASE % "origin/main")
        self.cannot_run(self.gate("--base", "no-such-branch"), NO_BASE % "no-such-branch")
        self.cannot_run(self.gate("--base", "main:README.md"), NO_BASE % "main:README.md")

    def test_base_comes_from_the_environment_and_the_option_wins(self):
        self.write(RICE, CARD)
        self.commit()
        self.fails(self.gate(env={"QC_BASE": "main"}), [NO_REPORT % RICE])
        self.passes(self.gate("--base", "work", env={"QC_BASE": "main"}), 0)
        self.cannot_run(self.gate(env={"QC_BASE": "no-such-branch"}), NO_BASE % "no-such-branch")

    def test_default_base_is_origin_main(self):
        self.git("update-ref", "refs/remotes/origin/main", "main")
        self.write(RICE, CARD)
        self.commit()
        self.fails(self.gate(), [NO_REPORT % RICE])

    def test_base_of_zeros_checks_every_card(self):
        self.git("checkout", "-q", "main")
        self.write(RICE, CARD)
        self.write("recipes/mains/stew.md", EDITED)
        self.write(RICE_REPORT, report())
        self.commit("Add two cards and one report")
        self.passes(self.gate("--base", "main"), 0)
        self.fails(
            self.gate("--base", ZERO),
            ["recipes/mains/stew.md: no editor report was added or changed under qc/mains/stew/"],
            lacking=1,
            cards=2,
        )
        self.write("qc/mains/stew/2026-11-19.md", report(sha=EDITED_SHA))
        self.commit()
        self.passes(self.gate("--base", ZERO), 2)

    def test_histories_with_no_common_commit_cannot_run(self):
        self.git("checkout", "-q", "--orphan", "island")
        self.commit("Unrelated")
        self.cannot_run(self.gate("--base", "main"), "check-qc: no merge base between main and HEAD")

    def test_outside_a_repository_cannot_run(self):
        outside = os.path.join(self.tmp, "plain")
        os.makedirs(outside)
        self.cannot_run(self.gate("--base", "main", cwd=outside), "check-qc: not inside a git repository")

    def test_repository_without_a_commit_cannot_run(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=empty, env=self.env, check=True)
        self.cannot_run(self.gate("--base", "main", cwd=empty), "check-qc: this repository has no commit yet")

    def test_runs_from_a_folder_inside_the_repository(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.commit()
        self.passes(self.gate("--base", "main", cwd=os.path.join(self.root, "recipes", "sides")), 1)

    # --staged.

    def test_staged_card_without_a_staged_report_fails(self):
        self.write(RICE, CARD)
        self.git("add", RICE)
        self.write(RICE_REPORT, report())
        self.fails(self.gate("--staged", "--base", "main"), [NO_REPORT % RICE])

    def test_staged_card_with_a_staged_report_passes(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.git("add", "-A")
        self.passes(self.gate("--staged", "--base", "main"), 1)

    def test_staged_reads_what_is_staged_not_the_file(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.git("add", "-A")
        self.write(RICE, EDITED)
        self.write(RICE_REPORT, report("FAIL"))
        self.passes(self.gate("--staged", "--base", "main"), 1)

    def test_staged_counts_the_commits_already_on_the_branch(self):
        self.write(RICE, CARD)
        self.commit()
        self.write("README.md", "changed\n")
        self.git("add", "-A")
        self.fails(self.gate("--staged", "--base", "main"), [NO_REPORT % RICE])

    # --working-tree.

    def test_working_tree_sees_untracked_and_unstaged_files(self):
        self.write(RICE, CARD)
        self.fails(self.gate("--working-tree", "--base", "main"), [NO_REPORT % RICE])
        self.write(RICE_REPORT, report())
        self.passes(self.gate("--working-tree", "--base", "main"), 1)
        self.commit()
        self.write(RICE, EDITED)
        self.fails(
            self.gate("--working-tree", "--base", "main"),
            ["%s: %s: %s" % (RICE, RICE_REPORT, STALE)],
        )

    def test_working_tree_runs_from_a_folder_inside_the_repository(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        self.write("recipes/mains/stew.md", EDITED)
        inside = os.path.join(self.root, "recipes", "sides")
        self.fails(
            self.gate("--working-tree", "--base", "main", cwd=inside),
            ["recipes/mains/stew.md: no editor report was added or changed under qc/mains/stew/"],
            lacking=1,
            cards=2,
        )

    def test_working_tree_lists_tracked_and_untracked_cards_in_one_order(self):
        self.write("recipes/sides/zucchini.md", CARD)
        self.commit()
        self.write("recipes/mains/apples.md", CARD)
        self.fails(
            self.gate("--working-tree", "--base", "main"),
            [
                "recipes/mains/apples.md: no editor report was added or changed under qc/mains/apples/",
                "recipes/sides/zucchini.md: no editor report was added or changed under qc/sides/zucchini/",
            ],
            lacking=2,
            cards=2,
        )

    def test_working_tree_skips_ignored_files(self):
        self.write(".gitignore", "recipes/sides/\n")
        self.commit()
        self.write(RICE, CARD)
        self.passes(self.gate("--working-tree", "--base", "main"), 0)

    # --stop-hook.

    def test_stop_hook_is_silent_on_a_pass(self):
        self.write(RICE, CARD)
        self.write(RICE_REPORT, report())
        result = self.gate("--stop-hook", "--base", "main", stdin='{"stop_hook_active": false}')
        self.assertEqual((result.stdout, result.stderr, result.returncode), ("", "", 0))

    def test_stop_hook_blocks_with_exit_two_and_the_problems_on_standard_error(self):
        self.write(RICE, CARD)
        result = self.gate("--stop-hook", "--base", "main", stdin='{"stop_hook_active": false}')
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr.splitlines(), [NO_REPORT % RICE, SUMMARY % (1, 1)])
        self.assertEqual(result.returncode, 2)

    def test_stop_hook_lets_the_session_stop_the_second_time(self):
        self.write(RICE, CARD)
        for stdin in (
            '{"stop_hook_active": true}',
            '{"stop_hook_active":true}',
            '{"stop_hook_active" : true}',
            '{\n  "hook_event_name": "Stop",\n  "stop_hook_active":\n    true\n}\n',
        ):
            with self.subTest(stdin=stdin):
                result = self.gate("--stop-hook", "--base", "main", stdin=stdin)
                self.assertEqual((result.stdout, result.stderr, result.returncode), ("", "", 0))

    def test_stop_hook_that_cannot_run_exits_one_and_two_in_ci(self):
        self.write(RICE, CARD)
        result = self.gate("--stop-hook", stdin="{}")
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr.splitlines(), [NO_BASE % "origin/main"])
        self.assertEqual(result.returncode, 1)
        result = self.gate("--stop-hook", stdin="{}", env={"CI": "true"})
        self.assertEqual(result.stderr.splitlines(), [NO_BASE % "origin/main"])
        self.assertEqual(result.returncode, 2)

    # --hash.

    def test_hash_prints_the_report_line(self):
        path = os.path.join(self.tmp, "abc.txt")
        with open(path, "wb") as handle:
            handle.write(b"abc")
        result = self.gate("--hash", path, cwd=self.tmp)
        self.assertEqual(result.stdout, "Card-SHA256: %s\n" % ABC_SHA)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 0)

    def test_hash_of_the_fixture_cards(self):
        self.write(RICE, CARD)
        self.assertEqual(self.gate("--hash", RICE).stdout, "Card-SHA256: %s\n" % CARD_SHA)
        self.write(RICE, EDITED)
        self.assertEqual(self.gate("--hash", RICE).stdout, "Card-SHA256: %s\n" % EDITED_SHA)

    def test_hash_of_a_missing_file_cannot_run(self):
        self.cannot_run(self.gate("--hash", "no-such-file.md"), "check-qc: no-such-file.md is not a file")

    # Usage.

    def test_usage_errors_exit_two(self):
        for args in (
            ["--unknown"],
            ["main"],
            ["--base"],
            ["--staged", "--working-tree"],
            ["--staged", "--staged"],
            ["--stop-hook", "--staged"],
            ["--hash"],
            ["--hash", "a", "b"],
            ["--staged", "--hash", "a"],
        ):
            with self.subTest(args=args):
                result = self.gate(*args)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, USAGE)
                self.assertEqual(result.returncode, 2)

    def test_script_is_executable(self):
        self.assertTrue(os.access(SCRIPT, os.X_OK))


if __name__ == "__main__":
    unittest.main()
````

#### File: `tests/test_lint_cards.py`

````python
"""Tests for scripts/lint-cards.py, observed through its output and its exit status.

Each test builds a repository root in a temporary directory. The index the
linter compares with is written by scripts/build-index.py, which has its own
tests; the stale and missing lines expected here are literals.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "lint-cards.py")
BUILD_INDEX = os.path.join(REPO, "scripts", "build-index.py")
USAGE = "usage: lint-cards.py [repository-root]\n"
STALE = "recipes/INDEX.md is stale: run python3 scripts/build-index.py"
MISSING = "recipes/INDEX.md is missing: run python3 scripts/build-index.py"
NAMES = "lowercase letters, digits, and single hyphens"

CARD = """---
id: roasted-carrots
version: v1.2
status: testing
evidence: cooked-once
category: sides
mirrors: none
---

# Roasted Carrots

- **Version:** v1.2
- **Date:** 2026-11-19
- **Status:** testing
- **Kitchen evidence:** cooked-once
- **Source:** Original.
- **Yield:** Serves 4
- **Time:** 40 minutes

## Equipment

- A rimmed baking sheet.

## Changelog

- v1.2 (2026-11-19): Lowered the oven temperature.
"""


def card(text=CARD, **changes):
    """Return the fixture card with whole lines replaced: key -> new line, or None to drop it."""
    lines = text.split("\n")
    for start, new in changes.items():
        start = start.replace("_", " ")
        found = [number for number, line in enumerate(lines) if line.startswith(start)]
        if not found:
            raise AssertionError("no line starts with %r" % start)
        if new is None:
            del lines[found[0]]
        else:
            lines[found[0]] = new
    return "\n".join(lines)


class LintCardsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

    def write(self, path, text, raw=None):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if raw is not None:
            with open(full, "wb") as handle:
                handle.write(raw)
            return
        with open(full, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)

    def index(self):
        subprocess.run(
            [sys.executable, BUILD_INDEX, self.root], capture_output=True, text=True, check=False
        )

    def lint(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, *(args or (self.root,))],
            capture_output=True,
            text=True,
            check=False,
        )

    def clean(self, cards):
        result = self.lint()
        self.assertEqual(result.stdout, "cards checked: %d\n" % cards)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 0)

    def problems(self, lines):
        result = self.lint()
        self.assertEqual(result.stdout.splitlines(), lines)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 1)

    def one(self, text, *problems, path="recipes/sides/roasted-carrots.md"):
        """Write one card, build the index, and expect exactly these problems for it."""
        self.write(path, text)
        self.index()
        self.problems(["%s: %s" % (path, problem) for problem in problems])

    # Clean repositories.

    def test_clean_card_passes(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.index()
        self.clean(1)

    def test_no_cards_passes_with_zero(self):
        self.index()
        self.clean(0)

    def test_card_without_the_mirrors_line_passes(self):
        self.write("recipes/sides/roasted-carrots.md", card(mirrors=None))
        self.index()
        self.clean(1)

    def test_extra_front_matter_lines_are_allowed(self):
        self.write("recipes/sides/roasted-carrots.md", card(mirrors="mirrors: none\ntags: weeknight"))
        self.index()
        self.clean(1)

    def test_windows_line_endings_are_read(self):
        self.write("recipes/sides/roasted-carrots.md", CARD.replace("\n", "\r\n"))
        self.index()
        self.clean(1)

    def test_only_files_one_folder_down_are_cards(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.write("recipes/notes.md", "not a card\n")
        self.write("recipes/sides/deep/notes.md", "not a card\n")
        self.write("recipes/.drafts/notes.md", "not a card\n")
        self.write("recipes/sides/.notes.md", "not a card\n")
        self.write("recipes/sides/notes.txt", "not a card\n")
        self.write("templates/recipe-card.md", "not a card\n")
        self.index()
        self.clean(1)

    # A card that cannot be read.

    def test_card_that_is_not_utf8(self):
        self.write("recipes/sides/roasted-carrots.md", "", raw=b"---\nid: \xff\n---\n# Carrots\n")
        self.problems(["recipes/sides/roasted-carrots.md: is not UTF-8 text"])

    def test_card_without_front_matter(self):
        self.one("# Roasted Carrots\n", "has no front matter")

    def test_empty_card(self):
        self.write("recipes/sides/roasted-carrots.md", "")
        self.problems(
            [
                "recipes/sides/roasted-carrots.md: has no front matter",
                "recipes/sides/roasted-carrots.md: has no title line",
            ]
        )

    def test_unclosed_front_matter(self):
        self.write("recipes/sides/roasted-carrots.md", "---\nid: roasted-carrots\n\n# Roasted Carrots\n")
        self.problems(["recipes/sides/roasted-carrots.md: front matter is not closed"])

    def test_card_without_a_title(self):
        self.write("recipes/sides/roasted-carrots.md", card(**{"#_Roasted": "Roasted Carrots"}))
        self.problems(["recipes/sides/roasted-carrots.md: has no title line"])

    def test_title_line_with_no_text_does_not_count(self):
        self.write("recipes/sides/roasted-carrots.md", card(**{"#_Roasted": "#  "}))
        self.problems(["recipes/sides/roasted-carrots.md: has no title line"])

    def test_unreadable_card_is_reported_once_and_the_index_is_not_checked(self):
        self.write("recipes/mains/stew.md", "---\nid: stew\n")
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.problems(["recipes/mains/stew.md: front matter is not closed"])

    def test_symbolic_link_card(self):
        self.write("elsewhere/roasted-carrots.md", CARD)
        os.makedirs(os.path.join(self.root, "recipes", "sides"))
        os.symlink(
            os.path.join("..", "..", "elsewhere", "roasted-carrots.md"),
            os.path.join(self.root, "recipes", "sides", "roasted-carrots.md"),
        )
        self.index()
        self.problems(["recipes/sides/roasted-carrots.md: is a symbolic link"])

    def test_symbolic_link_folder(self):
        self.write("elsewhere/roasted-carrots.md", CARD)
        os.makedirs(os.path.join(self.root, "recipes"))
        os.symlink(os.path.join("..", "elsewhere"), os.path.join(self.root, "recipes", "sides"))
        self.index()
        self.problems(["recipes/sides: is a symbolic link"])

    # Front matter.

    def test_missing_front_matter_lines(self):
        self.one(
            card(id=None, version=None, status=None, evidence=None, category=None),
            "front matter has no id line",
            "front matter has no version line",
            "front matter has no status line",
            "front matter has no evidence line",
            "front matter has no category line",
        )

    def test_repeated_front_matter_lines(self):
        self.one(
            card(id="id: roasted-carrots\nid: roasted-carrots", mirrors="mirrors: none\nmirrors: none"),
            "front matter has more than one id line",
            "front matter has more than one mirrors line",
        )

    def test_id_must_be_the_file_name(self):
        self.one(card(id="id: carrots"), "front matter id is carrots, expected the file name roasted-carrots")

    def test_category_must_be_the_folder(self):
        self.one(card(category="category: mains"), "front matter category is mains, expected the folder sides")

    def test_empty_values_are_named(self):
        self.one(
            card(id="id:", status="status: "),
            "front matter id is empty, expected the file name roasted-carrots",
            "front matter status is empty, expected one of draft, reviewed, testing, house, retired",
            "Status line is testing, but the front matter says empty",
        )

    def test_version_form(self):
        for version in ("1.2", "v1", "v1.02", "v0.1", "V1.2", "v1.2.1", "v1.2 "):
            with self.subTest(version=version):
                text = card(version="version: " + version, **{"-_**Version": "- **Version:** " + version.strip()})
                if version.strip() == "v1.2":
                    self.write("recipes/sides/roasted-carrots.md", text)
                    self.index()
                    self.clean(1)
                else:
                    self.one(text, "front matter version is %s, expected the form v1.0" % version)

    def test_version_does_not_roll_over(self):
        text = card(version="version: v1.10", **{"-_**Version": "- **Version:** v1.10"})
        self.write("recipes/sides/roasted-carrots.md", text)
        self.index()
        self.clean(1)

    def test_status_values(self):
        for status in ("draft", "reviewed", "testing", "house", "retired"):
            with self.subTest(status=status):
                text = card(status="status: " + status, **{"-_**Status": "- **Status:** " + status})
                self.write("recipes/sides/roasted-carrots.md", text)
                self.index()
                self.clean(1)
        self.one(
            card(status="status: tested", **{"-_**Status": "- **Status:** tested"}),
            "front matter status is tested, expected one of draft, reviewed, testing, house, retired",
        )

    def test_evidence_values(self):
        for evidence in ("untested", "cooked-once", "repeated", "not-recorded"):
            with self.subTest(evidence=evidence):
                text = card(
                    evidence="evidence: " + evidence,
                    **{"-_**Kitchen": "- **Kitchen evidence:** " + evidence},
                )
                self.write("recipes/sides/roasted-carrots.md", text)
                self.index()
                self.clean(1)
        self.one(
            card(evidence="evidence: cooked once", **{"-_**Kitchen": "- **Kitchen evidence:** cooked once"}),
            "front matter evidence is cooked once, expected one of untested, cooked-once, repeated, not-recorded",
        )

    # Names.

    def test_file_and_folder_names(self):
        for folder, name in (("sides", "Roasted-Carrots"), ("sides", "roasted--carrots"), ("sides", "roasted_carrots"), ("sides", "-carrots")):
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as root:
                    self.root = root
                    self.one(
                        card(id="id: " + name),
                        "file name is not " + NAMES,
                        path="recipes/%s/%s.md" % (folder, name),
                    )
        with tempfile.TemporaryDirectory() as root:
            self.root = root
            self.one(
                card(category="category: Side Dishes"),
                "folder name is not " + NAMES,
                path="recipes/Side Dishes/roasted-carrots.md",
            )

    def test_two_cards_with_one_slug(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.write("recipes/mains/roasted-carrots.md", card(category="category: mains"))
        self.index()
        self.problems(
            [
                "recipes/mains/roasted-carrots.md: slug is also used by recipes/sides/roasted-carrots.md",
                "recipes/sides/roasted-carrots.md: slug is also used by recipes/mains/roasted-carrots.md",
            ]
        )

    # The lines under the title.

    def test_missing_header_lines(self):
        self.one(
            card(
                **{
                    "-_**Version": None,
                    "-_**Date": None,
                    "-_**Status": None,
                    "-_**Kitchen": None,
                    "-_**Source": None,
                    "-_**Yield": None,
                    "-_**Time": None,
                }
            ),
            "has no Version line under the title",
            "has no Date line under the title",
            "has no Status line under the title",
            "has no Kitchen evidence line under the title",
            "has no Source line under the title",
            "has no Yield line under the title",
            "has no Time line under the title",
        )

    def test_repeated_header_line(self):
        self.one(
            card(**{"-_**Yield": "- **Yield:** Serves 4\n- **Yield:** Serves 6"}),
            "has more than one Yield line under the title",
        )

    def test_header_lines_after_the_first_section_do_not_count(self):
        text = card(**{"-_**Time": None}).replace("## Equipment\n", "## Equipment\n\n- **Time:** 40 minutes\n")
        self.one(text, "has no Time line under the title")

    def test_header_must_agree_with_the_front_matter(self):
        self.one(
            card(
                **{
                    "-_**Version": "- **Version:** v1.1",
                    "-_**Status": "- **Status:** house",
                    "-_**Kitchen": "- **Kitchen evidence:** repeated",
                }
            ),
            "Version line is v1.1, but the front matter says v1.2",
            "Status line is house, but the front matter says testing",
            "Kitchen evidence line is repeated, but the front matter says cooked-once",
        )

    def test_date_form(self):
        for date in ("YYYY-MM-DD", "2026-13-01", "2026-02-30", "19 November 2026", "2026-11-19 (updated)", ""):
            with self.subTest(date=date):
                self.one(
                    card(**{"-_**Date": "- **Date:** " + date}),
                    "Date line is %s, expected a date as YYYY-MM-DD" % (date or "empty"),
                )

    def test_empty_source_yield_and_time(self):
        self.one(
            card(**{"-_**Source": "- **Source:**", "-_**Yield": "- **Yield:** ", "-_**Time": "- **Time:**"}),
            "Source line is empty",
            "Yield line is empty",
            "Time line is empty",
        )

    # Links.

    def test_links(self):
        self.write("method/status-and-versions.md", "rules\n")
        self.write("recipes/mains/stew.md", card(id="id: stew", category="category: mains"))
        self.write("cook-logs/roasted-carrots/2026-11-18.md", "log\n")
        text = CARD + (
            "\n## Notes\n\n"
            "- Good: [rules](../../method/status-and-versions.md#versions), [stew](../mains/stew.md), "
            "[logs](../../cook-logs/roasted-carrots/), [top](#equipment), "
            "[a site](https://example.com/a), [mail](mailto:cook@example.com).\n"
            "- Good: [titled](../mains/stew.md \"Stew\"), [angled](<../mains/stew.md>), "
            "[from the root](/method/status-and-versions.md).\n"
            "- Bad: [gone](../mains/gone.md) and [also gone](missing.md#part).\n"
            "- Bad: [titled](titled.md \"A title\"), [angled](<angled.md>), [from the root](/gone-root.md).\n"
            "\n```markdown\n[in a fence](fenced.md)\n```\n"
            "\n~~~~\n[in tildes](tilde.md)\n```\n[still in tildes](tilde-2.md)\n~~~~\n"
            "\n```\n[in a fence closed by a longer one](long.md)\n`````\n"
            "\n[after the fences](after.md)\n"
        )
        self.write("recipes/sides/roasted-carrots.md", text)
        self.index()
        self.problems(
            [
                "recipes/sides/roasted-carrots.md: broken link ../mains/gone.md",
                "recipes/sides/roasted-carrots.md: broken link missing.md",
                "recipes/sides/roasted-carrots.md: broken link titled.md",
                "recipes/sides/roasted-carrots.md: broken link angled.md",
                "recipes/sides/roasted-carrots.md: broken link /gone-root.md",
                "recipes/sides/roasted-carrots.md: broken link after.md",
            ]
        )

    # The index, and several problems at once.

    def test_stale_index(self):
        self.index()
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.problems([STALE])

    def test_missing_index(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.problems([MISSING])

    def test_problems_come_in_card_order_and_the_index_line_is_last(self):
        self.write("recipes/sides/roasted-carrots.md", card(id="id: carrots"))
        self.write("recipes/mains/stew.md", card(id="id: stew", category="category: sides"))
        self.problems(
            [
                "recipes/mains/stew.md: front matter category is sides, expected the folder mains",
                "recipes/sides/roasted-carrots.md: front matter id is carrots, expected the file name roasted-carrots",
                MISSING,
            ]
        )

    def test_linked_folder_is_reported_in_folder_order(self):
        self.write("elsewhere/roasted-carrots.md", CARD)
        self.write("recipes/mains/stew.md", card(id="id: stew"))
        os.symlink(os.path.join("..", "elsewhere"), os.path.join(self.root, "recipes", "sides"))
        self.index()
        self.problems(
            [
                "recipes/mains/stew.md: front matter category is sides, expected the folder mains",
                "recipes/sides: is a symbolic link",
            ]
        )

    def test_unfilled_template_fails(self):
        with open(os.path.join(REPO, "templates", "recipe-card.md"), encoding="utf-8") as handle:
            template = handle.read()
        self.write("recipes/sides/roasted-carrots.md", template)
        self.index()
        self.problems(
            [
                "recipes/sides/roasted-carrots.md: front matter id is recipe-slug, expected the file name roasted-carrots",
                "recipes/sides/roasted-carrots.md: front matter category is category-folder, expected the folder sides",
                "recipes/sides/roasted-carrots.md: Date line is YYYY-MM-DD, expected a date as YYYY-MM-DD",
                "recipes/sides/roasted-carrots.md: broken link ../method/status-and-versions.md",
            ]
        )

    # Usage, and this repository.

    def test_usage_errors_exit_two(self):
        for args in (["--check"], [self.root, self.root], ["-h"]):
            with self.subTest(args=args):
                result = self.lint(*args)
                self.assertEqual((result.stdout, result.stderr, result.returncode), ("", USAGE, 2))

    def test_root_that_is_not_a_directory_exits_two(self):
        missing = os.path.join(self.root, "no-such-folder")
        result = self.lint(missing)
        self.assertEqual(
            (result.stdout, result.stderr, result.returncode),
            ("", "lint-cards: %s is not a directory\n" % missing, 2),
        )

    def test_this_repository_lints_clean(self):
        result = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, check=False)
        self.assertEqual(result.stderr, "")
        self.assertRegex(result.stdout, r"\Acards checked: [0-9]+\n\Z")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
````

#### File: `tests/test_install_git_hooks.py`

````python
"""Tests for scripts/install-git-hooks.sh, observed through the hook it writes and what that hook does.

Each test copies this repository's scripts into a small git repository in a
temporary directory and runs the copy, so the hook is never installed here.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = ("install-git-hooks.sh", "check-qc.sh", "lint-cards.py", "build-index.py")
HOOK = """#!/bin/sh
# chef-council pre-commit hook
# Installed by scripts/install-git-hooks.sh. Delete this file to remove it.
root=$(git rev-parse --show-toplevel) || exit 1
"$root/scripts/check-qc.sh" --staged || exit 1
python3 "$root/scripts/lint-cards.py" || exit 1
"""
CARD = """---
id: rice
version: v1.0
status: draft
evidence: untested
category: sides
---

# Rice

- **Version:** v1.0
- **Date:** 2026-11-19
- **Status:** draft
- **Kitchen evidence:** untested
- **Source:** Original.
- **Yield:** Serves 2
- **Time:** 20 minutes
"""
CARD_SHA = "4ee674546a749879292695ef6d13ab5f5dbecbcb813eda034eee2f79e72ba389"
REPORT = "VERDICT: PASS\nCard-SHA256: %s\n" % CARD_SHA


class InstallGitHooksTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(os.path.realpath(self._tmp.name), "repo")
        os.makedirs(os.path.join(self.root, "scripts"))
        for name in SCRIPTS:
            source = os.path.join(REPO, "scripts", name)
            if os.path.exists(source):
                shutil.copy(source, os.path.join(self.root, "scripts", name))
        self.env = dict(os.environ)
        for name in ("QC_BASE", "CI", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            self.env.pop(name, None)
        self.env.update(
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_SYSTEM=os.devnull,
            GIT_AUTHOR_NAME="test",
            GIT_AUTHOR_EMAIL="test@example.invalid",
            GIT_COMMITTER_NAME="test",
            GIT_COMMITTER_EMAIL="test@example.invalid",
            QC_BASE="main",
        )
        self.git("init", "-q", "-b", "main")
        self.run_in_repo("python3", "scripts/build-index.py")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Base")
        self.git("checkout", "-q", "-b", "work")
        self.hook = os.path.join(self.root, ".git", "hooks", "pre-commit")

    def run_in_repo(self, *command):
        return subprocess.run(
            command, cwd=self.root, env=self.env, capture_output=True, text=True, check=False
        )

    def git(self, *args):
        result = self.run_in_repo("git", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def install(self, *args, cwd=None):
        return subprocess.run(
            ["bash", os.path.join(self.root, "scripts", "install-git-hooks.sh"), *args],
            cwd=cwd or self.root,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )

    def write(self, path, text):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)

    def read_hook(self):
        with open(self.hook, encoding="utf-8") as handle:
            return handle.read()

    def test_installs_an_executable_hook(self):
        result = self.install()
        self.assertEqual(result.stdout, "pre-commit hook installed: .git/hooks/pre-commit\n")
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.read_hook(), HOOK)
        self.assertTrue(os.access(self.hook, os.X_OK))

    def test_installing_twice_is_the_same(self):
        self.install()
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.read_hook(), HOOK)

    def test_installs_into_its_own_repository_from_any_folder(self):
        result = self.install(cwd=os.path.dirname(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.read_hook(), HOOK)

    def test_another_hook_is_left_alone(self):
        os.makedirs(os.path.dirname(self.hook), exist_ok=True)
        with open(self.hook, "w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\necho mine\n")
        result = self.install()
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            "install-git-hooks: .git/hooks/pre-commit already exists and was not written by this script; "
            "it was left as it is\n",
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.read_hook(), "#!/bin/sh\necho mine\n")

    def test_hooks_path_setting_is_followed(self):
        self.git("config", "core.hooksPath", "custom-hooks")
        result = self.install()
        self.assertEqual(result.stdout, "pre-commit hook installed: custom-hooks/pre-commit\n")
        with open(os.path.join(self.root, "custom-hooks", "pre-commit"), encoding="utf-8") as handle:
            self.assertEqual(handle.read(), HOOK)
        self.assertFalse(os.path.exists(self.hook))

    def test_an_argument_is_a_usage_error(self):
        result = self.install("--force")
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "install-git-hooks: usage: scripts/install-git-hooks.sh\n")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(os.path.exists(self.hook))

    def test_outside_a_repository_exits_two(self):
        shutil.rmtree(os.path.join(self.root, ".git"))
        result = self.install()
        self.assertEqual(result.stderr, "install-git-hooks: %s is not a git repository\n" % self.root)
        self.assertEqual(result.returncode, 2)

    def test_the_hook_stops_a_card_commit_without_a_report(self):
        self.assertEqual(self.install().returncode, 0)
        self.write("recipes/sides/rice.md", CARD)
        self.run_in_repo("python3", "scripts/build-index.py")
        self.git("add", "-A")
        result = self.run_in_repo("git", "commit", "-q", "-m", "Add the rice card")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "recipes/sides/rice.md: no editor report was added or changed under qc/sides/rice/",
            result.stdout + result.stderr,
        )
        self.assertEqual(self.git("log", "--format=%s"), "Base\n")

    def test_the_hook_allows_a_card_commit_with_a_current_passing_report(self):
        self.assertEqual(self.install().returncode, 0)
        self.write("recipes/sides/rice.md", CARD)
        self.write("qc/sides/rice/2026-11-19.md", REPORT)
        self.run_in_repo("python3", "scripts/build-index.py")
        self.git("add", "-A")
        result = self.run_in_repo("git", "commit", "-q", "-m", "Add the rice card")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git("log", "--format=%s"), "Add the rice card\nBase\n")

    def test_the_hook_stops_a_commit_when_the_cards_do_not_lint(self):
        self.assertEqual(self.install().returncode, 0)
        self.write("recipes/sides/rice.md", CARD)
        self.write("qc/sides/rice/2026-11-19.md", REPORT)
        self.git("add", "-A")
        result = self.run_in_repo("git", "commit", "-q", "-m", "Add the rice card")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "recipes/INDEX.md is stale: run python3 scripts/build-index.py", result.stdout + result.stderr
        )
        self.assertEqual(self.git("log", "--format=%s"), "Base\n")

    def test_script_is_executable(self):
        self.assertTrue(os.access(os.path.join(REPO, "scripts", "install-git-hooks.sh"), os.X_OK))


if __name__ == "__main__":
    unittest.main()
````

#### File: `scripts/check-qc.sh`

````bash
#!/usr/bin/env bash
# The editor gate: every recipe card that changed needs a current, passing
# editor report.
#
# Usage: scripts/check-qc.sh [--staged | --working-tree | --stop-hook] [--base <revision>]
#        scripts/check-qc.sh --hash <file>
#
# A card is recipes/<category>/<slug>.md. A card that was added or changed
# since the base passes only when a report qc/<category>/<slug>/<name>.md was
# added or changed too, holds exactly one line that starts with "VERDICT:",
# reading "VERDICT: PASS" or "VERDICT: PASS WITH NOTES", and holds exactly one
# line that starts with "Card-SHA256:", giving the SHA-256 of the card's bytes.
# Any later edit to the card changes its hash, so an old PASS stops counting.
#
# What is compared with the base:
#   (default)        the last commit, which is what CI sees
#   --staged         what is staged, for a pre-commit hook
#   --working-tree   the files as they are now, untracked ones included
#   --stop-hook      --working-tree, as a Claude Code Stop hook (see below)
#
# The base is --base, else $QC_BASE, else origin/main. Changes are counted
# from the commit where the branch left the base. A base of forty zeros,
# which is what a first push reports, means every card is checked.
#
# --hash prints the "Card-SHA256:" line for a file, for a report.
#
# Exit status: 0 every changed card has a current passing report; 1 one does
# not; 2 the check could not run, which never counts as a pass. A missing
# base is one such case: the check never passes without a base to compare.
# With --stop-hook the script prints nothing on success, exits 2 with the
# problems on standard error when a card lacks its report (which keeps the
# session open), and exits 1 when the check could not run (2 when CI=true).
# See method/recipe-qc.md.
set -uo pipefail

USAGE="usage: scripts/check-qc.sh [--staged | --working-tree | --stop-hook] [--base <revision>] | --hash <file>"
ZERO=0000000000000000000000000000000000000000

usage() {
  echo "$USAGE" >&2
  exit 2
}

mode=""
hook=0
base=${QC_BASE:-origin/main}

# The check could not run. Never exits 0.
fail() {
  echo "check-qc: $1" >&2
  if [ "$hook" = 1 ] && [ "${CI:-}" != "true" ]; then
    exit 1
  fi
  exit 2
}

sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum | cut -d ' ' -f 1
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 | cut -d ' ' -f 1
  else
    return 1
  fi
}

if [ "${1:-}" = "--hash" ]; then
  [ "$#" -eq 2 ] || usage
  [ -f "$2" ] || fail "$2 is not a file"
  digest=$(sha256 < "$2") && [ -n "$digest" ] || fail "needs sha256sum or shasum"
  echo "Card-SHA256: $digest"
  exit 0
fi

while [ "$#" -gt 0 ]; do
  case "$1" in
    --staged | --working-tree | --stop-hook)
      [ -z "$mode" ] || usage
      mode=$1
      ;;
    --base)
      [ "$#" -ge 2 ] || usage
      base=$2
      shift
      ;;
    *) usage ;;
  esac
  shift
done
[ -n "$mode" ] || mode=--head
if [ "$mode" = "--stop-hook" ]; then
  hook=1
  mode=--working-tree
  # Claude Code sends the hook a JSON object. When this hook has already kept
  # the session open once, let it stop, so the session cannot loop forever.
  if [ ! -t 0 ]; then
    input=$(cat || true)
    if printf '%s' "$input" | tr '\n' ' ' | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
      exit 0
    fi
  fi
fi

root=$(git rev-parse --show-toplevel 2>/dev/null) || fail "not inside a git repository"
cd "$root" || fail "cannot enter $root"
git rev-parse --verify -q "HEAD^{commit}" >/dev/null || fail "this repository has no commit yet"

if [ "$base" = "$ZERO" ]; then
  from=$(git hash-object -t tree /dev/null) || fail "cannot name the empty tree"
else
  git rev-parse --verify -q "$base^{commit}" >/dev/null ||
    fail "base $base not found: fetch it, or name another with --base or QC_BASE"
  from=$(git merge-base "$base" HEAD 2>/dev/null) || fail "no merge base between $base and HEAD"
fi

list=$(mktemp) || fail "cannot create a temporary file"
trap 'rm -f "$list" "$list.sorted"' EXIT
case "$mode" in
  --head)
    git diff --no-renames --name-only -z --diff-filter=d "$from" HEAD > "$list" ||
      fail "git diff failed"
    ;;
  --staged)
    git diff --cached --no-renames --name-only -z --diff-filter=d "$from" > "$list" ||
      fail "git diff failed"
    ;;
  --working-tree)
    git diff --no-renames --name-only -z --diff-filter=d "$from" > "$list" ||
      fail "git diff failed"
    git ls-files --others --exclude-standard -z >> "$list" || fail "git ls-files failed"
    ;;
esac
# Sort the NUL-separated list with a plain sort, by swapping NUL and newline.
tr '\0\n' '\n\0' < "$list" | LC_ALL=C sort -u | tr '\0\n' '\n\0' > "$list.sorted" || fail "sort failed"

changed=()
while IFS= read -r -d '' path; do
  changed+=("$path")
done < "$list.sorted"

# Print the candidate content of one path.
show() {
  case "$mode" in
    --head) git show "HEAD:$1" ;;
    --staged) git show ":$1" ;;
    --working-tree) cat -- "$1" ;;
  esac
}

# Print why the report $1 does not pass for a card whose hash is $2, or nothing.
judge() {
  local text verdict stated
  text=$(show "$1" | sed 's/[[:space:]]*$//') || { echo "cannot be read"; return; }
  if [ "$(printf '%s\n' "$text" | grep -c '^VERDICT:')" != 1 ]; then
    echo "must hold exactly one line that starts with VERDICT:"
    return
  fi
  verdict=$(printf '%s\n' "$text" | grep '^VERDICT:')
  case "$verdict" in
    "VERDICT: PASS" | "VERDICT: PASS WITH NOTES") ;;
    "VERDICT: FAIL")
      echo "the verdict is FAIL"
      return
      ;;
    *)
      echo "the VERDICT line is not PASS, PASS WITH NOTES, or FAIL"
      return
      ;;
  esac
  if [ "$(printf '%s\n' "$text" | grep -c '^Card-SHA256:')" != 1 ]; then
    echo "must hold exactly one line that starts with Card-SHA256:"
    return
  fi
  stated=$(printf '%s\n' "$text" | grep '^Card-SHA256:')
  if ! printf '%s\n' "$stated" | grep -Eq '^Card-SHA256: [0-9a-f]{64}$'; then
    echo "the Card-SHA256 line does not hold 64 lowercase hexadecimal digits"
    return
  fi
  if [ "$stated" != "Card-SHA256: $2" ]; then
    echo "Card-SHA256 is not the hash of the card, so the card changed after this check"
  fi
}

cards=0
lacking=0
problems=()
for path in ${changed[@]+"${changed[@]}"}; do
  [[ "$path" =~ ^recipes/([^/]+)/([^/]+)\.md$ ]] || continue
  category=${BASH_REMATCH[1]}
  slug=${BASH_REMATCH[2]}
  case "$category" in .*) continue ;; esac
  case "$slug" in .*) continue ;; esac
  cards=$((cards + 1))
  digest=$(show "$path" | sha256) && [ -n "$digest" ] || fail "cannot hash $path: needs sha256sum or shasum"
  prefix="qc/$category/$slug/"
  passed=0
  found=()
  for report in "${changed[@]}"; do
    name=${report#"$prefix"}
    [ "$name" != "$report" ] || continue
    case "$name" in
      */* | .*) continue ;;
      *.md) ;;
      *) continue ;;
    esac
    reason=$(judge "$report" "$digest")
    if [ -z "$reason" ]; then
      passed=1
      break
    fi
    found+=("$path: $report: $reason")
  done
  [ "$passed" = 0 ] || continue
  lacking=$((lacking + 1))
  if [ "${#found[@]}" -eq 0 ]; then
    problems+=("$path: no editor report was added or changed under $prefix")
  else
    problems+=("${found[@]}")
  fi
done

if [ "$lacking" -gt 0 ]; then
  if [ "$hook" = 1 ]; then
    printf '%s\n' "${problems[@]}" >&2
  else
    printf '%s\n' "${problems[@]}"
  fi
  echo "check-qc: $lacking of $cards changed recipe cards lack a current passing editor report; method/recipe-qc.md says how to get one" >&2
  if [ "$hook" = 1 ]; then
    exit 2
  fi
  exit 1
fi
[ "$hook" = 1 ] || echo "qc checked: $cards"
exit 0
````

#### File: `scripts/lint-cards.py`

````python
#!/usr/bin/env python3
"""Lint the recipe cards.

Usage: python3 scripts/lint-cards.py [repository-root]

A card is a file recipes/<category>/<slug>.md, as scripts/build-index.py
finds them. For each card this checks that it is a regular UTF-8 file with
closed front matter and a title; that the front matter holds id, version,
status, evidence, and category once each, with id equal to the file name,
category equal to the folder, a version such as v1.0, and a status and an
evidence value that method/status-and-versions.md lists; that the lines
under the title give Version, Date, Status, Kitchen evidence, Source, Yield,
and Time once each and agree with the front matter; that the slug and the
category are lowercase letters, digits, and single hyphens; that no two
cards share a slug; and that every inline link in the card that is not a
web address leads to a file or a folder, read from the card's folder, or
from the repository root when it starts with "/". Then it runs
scripts/build-index.py --check, so a stale index fails.

Prints one line per problem and exits 1, or prints "cards checked: <N>" and
exits 0.
"""

import datetime
import os
import re
import subprocess
import sys

USAGE = "usage: lint-cards.py [repository-root]"
FIELD = re.compile(r"([a-z_]+):[ \t]*(.*)")
NAME = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
VERSION = re.compile(r"v[1-9][0-9]*\.(0|[1-9][0-9]*)")
LINK = re.compile(r'\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')
FENCE = re.compile(r"\s*(`{3,}|~{3,})")
REQUIRED = ["id", "version", "status", "evidence", "category"]
STATUSES = ["draft", "reviewed", "testing", "house", "retired"]
EVIDENCE = ["untested", "cooked-once", "repeated", "not-recorded"]
LABELS = ["Version", "Date", "Status", "Kitchen evidence", "Source", "Yield", "Time"]
AGREE = [("Version", "version"), ("Status", "status"), ("Kitchen evidence", "evidence")]
UNREADABLE = ("is not UTF-8 text", "front matter is not closed", "has no title line")


def find_cards(root):
    """Return (cards, problems): (category, slug) pairs in order, and the folders that are links."""
    recipes = os.path.join(root, "recipes")
    cards = []
    problems = []
    if not os.path.isdir(recipes):
        return cards, problems
    for category in sorted(os.listdir(recipes)):
        folder = os.path.join(recipes, category)
        if category.startswith(".") or not os.path.isdir(folder):
            continue
        if os.path.islink(folder):
            problems.append((category, "", "recipes/%s: is a symbolic link" % category))
            continue
        for name in os.listdir(folder):
            if name.startswith(".") or not name.endswith(".md"):
                continue
            path = os.path.join(folder, name)
            if os.path.islink(path) or os.path.isfile(path):
                cards.append((category, name[: -len(".md")]))
    return sorted(cards), problems


def shown(value):
    return value if value else "empty"


def is_date(text):
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text):
        return False
    try:
        datetime.date(int(text[:4]), int(text[5:7]), int(text[8:]))
    except ValueError:
        return False
    return True


def lint_card(root, category, slug):
    """Return the problems of one card, without the path in front."""
    path = os.path.join(root, "recipes", category, slug + ".md")
    if os.path.islink(path):
        return ["is a symbolic link"]
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except UnicodeDecodeError:
        return ["is not UTF-8 text"]
    fields = {}
    body = lines
    bare = not lines or lines[0] != "---"
    if not bare:
        if "---" not in lines[1:]:
            return ["front matter is not closed"]
        end = lines.index("---", 1)
        for line in lines[1:end]:
            match = FIELD.fullmatch(line)
            if match:
                fields.setdefault(match.group(1), []).append(match.group(2).strip())
        body = lines[end + 1 :]
    title = None
    for number, line in enumerate(body):
        if line.startswith("# ") and line[2:].strip():
            title = number
            break
    if bare or title is None:
        return ["has no front matter"] * bare + ["has no title line"] * (title is None)

    problems = []
    for key in REQUIRED + ["mirrors"]:
        count = len(fields.get(key, []))
        if count == 0 and key != "mirrors":
            problems.append("front matter has no %s line" % key)
        elif count > 1:
            problems.append("front matter has more than one %s line" % key)
    single = {key: values[0] for key, values in fields.items() if len(values) == 1}
    if "id" in single and single["id"] != slug:
        problems.append("front matter id is %s, expected the file name %s" % (shown(single["id"]), slug))
    if "category" in single and single["category"] != category:
        problems.append(
            "front matter category is %s, expected the folder %s" % (shown(single["category"]), category)
        )
    if "version" in single and not VERSION.fullmatch(single["version"]):
        problems.append("front matter version is %s, expected the form v1.0" % shown(single["version"]))
    if "status" in single and single["status"] not in STATUSES:
        problems.append(
            "front matter status is %s, expected one of %s" % (shown(single["status"]), ", ".join(STATUSES))
        )
    if "evidence" in single and single["evidence"] not in EVIDENCE:
        problems.append(
            "front matter evidence is %s, expected one of %s"
            % (shown(single["evidence"]), ", ".join(EVIDENCE))
        )
    if not NAME.fullmatch(slug):
        problems.append("file name is not lowercase letters, digits, and single hyphens")
    if not NAME.fullmatch(category):
        problems.append("folder name is not lowercase letters, digits, and single hyphens")

    header = {}
    for line in body[title + 1 :]:
        if line.startswith("## "):
            break
        for label in LABELS:
            mark = "- **%s:**" % label
            if line.startswith(mark):
                header.setdefault(label, []).append(line[len(mark) :].strip())
    for label in LABELS:
        count = len(header.get(label, []))
        if count == 0:
            problems.append("has no %s line under the title" % label)
        elif count > 1:
            problems.append("has more than one %s line under the title" % label)
    stated = {label: values[0] for label, values in header.items() if len(values) == 1}
    for label, key in AGREE:
        if label in stated and key in single and stated[label] != single[key]:
            problems.append(
                "%s line is %s, but the front matter says %s"
                % (label, shown(stated[label]), shown(single[key]))
            )
    if "Date" in stated and not is_date(stated["Date"]):
        problems.append("Date line is %s, expected a date as YYYY-MM-DD" % shown(stated["Date"]))
    for label in ["Source", "Yield", "Time"]:
        if label in stated and not stated[label]:
            problems.append("%s line is empty" % label)

    fence = None
    for line in body:
        mark = FENCE.match(line)
        if fence is None and mark:
            fence = mark.group(1)
            continue
        if fence is not None:
            closing = line.strip()
            if len(closing) >= len(fence) and set(closing) == {fence[0]}:
                fence = None
            continue
        for target in LINK.findall(line):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|#", target):
                continue
            target = target.split("#")[0].split("?")[0]
            start = root if target.startswith("/") else os.path.dirname(path)
            if not os.path.exists(os.path.join(start, target.lstrip("/"))):
                problems.append("broken link %s" % target)
    return problems


def main(argv):
    arguments = argv[1:]
    if len(arguments) > 1 or any(argument.startswith("-") for argument in arguments):
        print(USAGE, file=sys.stderr)
        return 2
    if arguments:
        root = arguments[0]
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(root):
        print("lint-cards: %s is not a directory" % root, file=sys.stderr)
        return 2

    cards, found = find_cards(root)
    unreadable = False
    for category, slug in cards:
        relative = "recipes/%s/%s.md" % (category, slug)
        for problem in lint_card(root, category, slug):
            found.append((category, slug, "%s: %s" % (relative, problem)))
            if problem in UNREADABLE:
                unreadable = True
        for other, other_slug in cards:
            if other_slug == slug and other != category:
                found.append(
                    (category, slug, "%s: slug is also used by recipes/%s/%s.md" % (relative, other, slug))
                )
    lines = [text for _, _, text in sorted(found, key=lambda problem: problem[:2])]

    if not unreadable:
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-index.py")
        index = subprocess.run(
            [sys.executable, script, "--check", root], capture_output=True, text=True, check=False
        )
        if index.returncode != 0:
            lines.extend((index.stdout + index.stderr).splitlines())

    if lines:
        for line in lines:
            print(line)
        return 1
    print("cards checked: %d" % len(cards))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
````

#### File: `scripts/install-git-hooks.sh`

````bash
#!/usr/bin/env bash
# Install an optional git pre-commit hook that runs the editor gate and the
# card linter before every commit in this repository.
#
# Usage: scripts/install-git-hooks.sh
#
# The hook runs scripts/check-qc.sh --staged and python3 scripts/lint-cards.py
# and stops the commit when either fails. CI runs the same two checks on every
# pull request, so the hook is a convenience and not the gate. An existing
# pre-commit hook that this script did not write is never replaced. To remove
# the hook, delete the file this script names when it finishes.
#
# Exit status: 0 the hook is installed; 1 another pre-commit hook is in the
# way; 2 the script could not run.
set -euo pipefail

MARK="# chef-council pre-commit hook"

fail() {
  echo "install-git-hooks: $1" >&2
  exit 2
}

[ "$#" -eq 0 ] || fail "usage: scripts/install-git-hooks.sh"
repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo"
git rev-parse --git-dir >/dev/null 2>&1 || fail "$repo is not a git repository"
hook=$(git rev-parse --git-path hooks/pre-commit)

if [ -e "$hook" ] || [ -L "$hook" ]; then
  if ! grep -qxF "$MARK" "$hook" 2>/dev/null; then
    echo "install-git-hooks: $hook already exists and was not written by this script; it was left as it is" >&2
    exit 1
  fi
fi

mkdir -p "$(dirname "$hook")"
cat > "$hook" <<'HOOK'
#!/bin/sh
# chef-council pre-commit hook
# Installed by scripts/install-git-hooks.sh. Delete this file to remove it.
root=$(git rev-parse --show-toplevel) || exit 1
"$root/scripts/check-qc.sh" --staged || exit 1
python3 "$root/scripts/lint-cards.py" || exit 1
HOOK
chmod +x "$hook"
echo "pre-commit hook installed: $hook"
````

#### File: `.agents/skills/recipe-editor/SKILL.md`

````markdown
---
name: recipe-editor
description: Independently checks a new or changed recipe card one for one against the verbatim source packet the cook approved, and writes an editor report with a PASS, PASS WITH NOTES, or FAIL verdict, a discrepancy table, and the hash of the card it read. Never edits a recipe. Use after any recipe card is added or changed and before it is committed, and only in a fresh context that did not write the card.
---

# Recipe Editor

The editor exists because the agent that writes a recipe card is the wrong one to check it. You compare the card with the exact text the cook approved and write down every place where they differ. You do not improve the card, defend it, or fix it.

Paths in this file are relative to the repository root, except `references/report-format.md`, which sits beside this file.

## Before you start

1. **Check that you are independent.** You are independent only when you did not write or change the card, and the conversation in which it was written is not in your context. If you wrote the card, or you can see the writer's reasoning about it, stop. Write no report and give no verdict. Reply with one line that starts `Not independent:` and gives the reason, and tell the cook to start a fresh agent, a new session, or a new chat. The four headings under What to tell the writer do not apply to that reply. Never certify your own work.
2. **Find your two inputs.** They are the source packet, at `.sources/<slug>/<YYYY-MM-DD>.md`, and the card, at `recipes/<category>/<slug>.md`. Whoever asked for the check gives you both paths. If one is missing from what you were asked, ask for it. Do not pick a packet yourself, because a card can have several. If you were also given the writer's summary, explanation, or opinion of the card, do not use it. The packet and the card are the evidence.
3. **Check that the packet is usable.** `templates/source-packet.md` shows its form. A usable packet holds the approved text itself between the tilde lines under `## Approved text`, and the cook's own words under `## Scope instruction`. When there is no packet, or it holds a summary, a description, or the template's own text where the approved text should be, you have nothing to compare the card with. The verdict is then `FAIL`, with the one discrepancy `no verbatim source`, and you still write the report.
4. **Read the rules.** Read `method/status-and-versions.md`, which the card's version, status, and evidence are held to, and `references/report-format.md`.

## Compare the card with the packet

Go through the approved text one item at a time and find each item on the card. Then go through the card one line at a time and find where each line came from. Rewording a step is allowed, and so is arranging the recipe into the card's tables and headings. Changing what gets cooked is not.

- **Ingredients.** Every ingredient in the approved text is on the card with the same amount, unit, and prep. An amount that is divided between two uses adds up to the approved total. The card adds no ingredient and drops none. A converted unit is a difference, unless the cook asked for the conversion.
- **Method.** Every step is on the card, in the same order, with the same heat, temperature, time, size, pan or pot, cue, and doneness check. The card adds no step and drops none.
- **Equipment, yield, and time.** Each one matches the approved text.
- **Gaps.** Where the approved text leaves out something a cook needs, the card says `Not stated.` in its place, lists the gap under Notes, and has the status `draft`. A number on the card that the approved text does not hold was invented.
- **The other sections.** Why this works, Failure modes, Variations, Storage, Notes, and Next experiment hold what the approved text or the cook's instruction says, or `None recorded.` Anything else there is an addition by the writer. List each addition in the report, and treat one that could change what a cook does as a discrepancy.
- **An update or a new variant.** Compare the card with the previous version in the packet as well. Every difference between the two traces to a correction in the approved text or to the scope instruction. A difference that nobody asked for is a discrepancy, even when it reads like an improvement.
- **Version, status, and evidence.** The version is the one `method/status-and-versions.md` gives for this kind of save. The status and the kitchen evidence are no higher than that page allows. Count the cook logs the way that page says. If you can list files, read the logs in `cook-logs/<slug>/` themselves. If you cannot, read the logs the packet lists. The block at the top of the card and the lines under its title agree with each other.
- **Source and people.** The Source line credits only what the packet shows the recipe came from. The card does not say or suggest that any person reviewed, approved, endorsed, or wrote it, and it does not name a lens as an author or a source.
- **The index.** `recipes/INDEX.md` has a row for the card with the card's version, status, and evidence. If you can run commands, `python3 scripts/build-index.py --check` tells you whether the index is current.
- **The scope.** The save is the kind the cook's scope instruction asked for: a new card, a change to a saved card, or a separate version.

## Decide the verdict

Give every discrepancy one of two severities.

| Severity | What it covers |
|---|---|
| `blocking` | The card would have a cook do something the approved text does not say: a different amount, unit, ingredient, step, order, time, temperature, or doneness check. Or the card states something the packet does not support: an invented number, a status or an evidence value higher than the rules allow, a credit to a source or a person, or a difference from the previous version that nobody asked for. Or there is no verbatim source. |
| `minor` | Anything else worth fixing that changes nothing a cook would do and claims nothing untrue: wording, a label, the layout, or an index that needs regenerating. |

- One or more blocking discrepancies: the verdict is `FAIL`.
- Minor discrepancies only: the verdict is `PASS WITH NOTES`.
- No discrepancy: the verdict is `PASS`.

When you cannot tell whether a difference changes what gets cooked, it is blocking, and the report says what you could not settle. Do not pass a card because its differences are few, and do not fail one because a step was reworded.

## Write the report

Write one file, the report, at the path and in the form `references/report-format.md` gives. Write nothing else.

- Never edit the card, the packet, the index, a cook log, or any other file, even to fix something small. A fix is the writer's job, and a fixed card needs a fresh check.
- Never commit, push, or open a pull request.
- If you cannot write files, return the complete report with its path for the cook to save, and say that nothing was saved.

## What to tell the writer

Reply under these four headings, in this order:

1. `## Verdict`: the report's `VERDICT:` line and nothing else.
2. `## Report`: the path of the report you wrote. If you wrote none, `Not written:` with the reason, then the complete report.
3. `## Discrepancies`: the table from the report, or `None.`
4. `## Next step`: the one thing that happens next, and who does it. After a `FAIL`, the writer fixes the card from the packet, and a fresh editor, not you, checks it again. After a `PASS` or a `PASS WITH NOTES`, the writer commits the card, the index, and this report together. Fixing a note changes the card, and a changed card needs a fresh check before it is committed.
````

#### File: `.agents/skills/recipe-editor/references/report-format.md`

`````markdown
# The editor report

One report records one check of one card. The editor writes it, and nobody else changes it afterwards.

## Where it goes

The report for the card `recipes/<category>/<slug>.md` goes at `qc/<category>/<slug>/<YYYY-MM-DD>.md`, named for the day of the check. A second report for the same card on the same day ends in `-2`, and the next in `-3`. Never edit or delete an earlier report. A `FAIL` that was later fixed stays where it is, as the record of what the check caught.

## The form

A report looks like this. Keep the title, the two lines inside the fence, the six labels, and the three headings, and replace everything else.

````markdown
# Editor report: Recipe title v1.0

```text
VERDICT: PASS WITH NOTES
Card-SHA256: 0000000000000000000000000000000000000000000000000000000000000000
```

- **Card:** `recipes/category-folder/recipe-slug.md`
- **Date:** YYYY-MM-DD
- **Kind of save:** new card
- **Source:** this conversation on YYYY-MM-DD
- **Packet:** `.sources/recipe-slug/YYYY-MM-DD.md`
- **Editor:** a fresh agent session that did not write the card

## Discrepancies

| Where | Approved text says | Card says | Severity |
|---|---|---|---|
| Method, step 2 | until crisp-tender | until tender | minor |

## Additions

- Notes: a line on substitutions that the approved text does not hold. It sits outside the recipe.

## Checks run

- Ingredients: checked.
- Method: checked.
- Equipment, yield, and time: checked.
- Gaps: checked.
- The other sections: checked.
- Update or new variant: not applicable, this is a new card.
- Version, status, and evidence: checked.
- Source and people: checked.
- The index: not checked, because no command could be run.
- The scope: checked.
````

## The two lines the gate reads

`scripts/check-qc.sh` reads two lines of a report and nothing else. [`method/recipe-qc.md`](../../../../method/recipe-qc.md) says what it does with them.

- **`VERDICT:`** is followed by one space and exactly one of `PASS`, `PASS WITH NOTES`, or `FAIL`. The skill's `## Decide the verdict` section says which.
- **`Card-SHA256:`** is followed by one space and the SHA-256 of the card file, as 64 lowercase hexadecimal digits. After you have read the card, run `scripts/check-qc.sh --hash recipes/<category>/<slug>.md` and copy the line it prints. If you cannot run commands, use the `Card-SHA256:` line you were given with the card. If you were given none, write `Card-SHA256: not computed` and say in your reply that the cook must run that command and put its line in place of yours, without changing the card.

Each of the two starts a line of its own, with nothing in front of it, and appears once in the report. Never start another line of the report with `VERDICT:` or `Card-SHA256:`.

The hash ties the report to the card as you read it. If the card changes afterwards by even one character, the hash no longer matches, and the report stops counting. That is intended: a changed card needs a fresh check.

## The rest of the report

- **Title.** The card's title and version.
- **Card, Date, Kind of save, Source, Packet.** The card's path, the day of the check, and three lines from the top of the packet: the kind of save, where the approved text came from, and the packet's own path. For Source, say where the text came from, never what it said. When there is no packet, or the packet does not say, write `not stated` for Kind of save and for Source, and for Packet write the path you were given, or `none`.
- **Editor.** What ran the check, such as a fresh agent session and the model's name if you know it. It is never a person's name and never a lens.
- **Discrepancies.** One row for each. Where: the section and the item. Then what the approved text says and what the card says, in as few words as show the difference, and the severity, `blocking` or `minor`. Write `None.` in place of the table when there is none. For a missing or summarized packet, the one row reads `no verbatim source` under Where.
- **Additions.** Each thing on the card that the approved text does not hold, and whether it sits outside the Equipment, Ingredients, and Method. Write `None.` when there is none.
- **Checks run.** One line for each check in the skill's `## Compare the card with the packet` section, in that order, saying `checked`, `not applicable` with the reason, or `not checked` with the reason. With no verbatim source, every check that needs the approved text reads `not checked, because there is no verbatim source`.

## What stays out of a report

A report is committed with the card, and a public fork publishes it. The packet is not committed, because it can hold a private conversation or a publisher's recipe.

- Do not copy the approved text into the report. Quote only the few words a discrepancy turns on.
- Name no person: not the cook, not anyone the cook's words mention, and not a chef. Leave out any health detail.
- Never say or suggest that a person or a lens reviewed, checked, or approved the card. An agent ran this check.
`````

#### File: `.claude/agents/recipe-editor.md`

````markdown
---
name: recipe-editor
description: Independent editor for recipe cards. Use after any card under recipes/ is added or changed and before it is committed. Give it the path of the source packet and the path of the card, and nothing about how the card was written. It writes an editor report under qc/ and never edits a recipe.
tools: Read, Grep, Glob, Bash, Write
---

You are the recipe editor for this repository, running in a fresh context. You did not write the card you are about to check.

Read `.agents/skills/recipe-editor/SKILL.md` in full, then follow it exactly. It says what to read, what counts as a discrepancy, how to decide the verdict, and how to write the report.

Your brief gives you two paths: the source packet and the card. If it also tells you how the card was written or what the writer thinks of it, do not rely on that. If the brief leaves out either path, say which one and stop. A path that was given but leads to no file is different, and the skill says what to do then.
````

#### File: `method/recipe-qc.md`

````markdown
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
````

#### File: `.claude/settings.json`

````json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$CLAUDE_PROJECT_DIR\" && scripts/check-qc.sh --stop-hook"
          }
        ]
      }
    ]
  }
}
````

#### Addition: `.github/workflows/ci.yml`

````yaml
      - name: Lint the recipe cards and check the index
        run: python3 scripts/lint-cards.py

  editor-gate:
    name: editor gate
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - name: Check out the full history
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          fetch-depth: 0
          persist-credentials: false
      - name: Require a current passing editor report for every changed card
        env:
          EVENT_NAME: ${{ github.event_name }}
          PR_BASE: ${{ github.base_ref }}
          PUSH_BEFORE: ${{ github.event.before }}
        run: |
          if [ "$EVENT_NAME" = "pull_request" ]; then
            scripts/check-qc.sh --base "origin/$PR_BASE"
          else
            scripts/check-qc.sh --base "$PUSH_BEFORE"
          fi
````
