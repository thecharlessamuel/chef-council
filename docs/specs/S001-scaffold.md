---
date: 2026-11-18
id: S001
wayfinder: docs/wayfinder/W001-public-chef-council/issues/T007-scaffold.md
target_release: none
status: ready-to-build
base_branch: main
base_sha: 32fbe81f22c0d080e51574d5edd41ef9490a1e9f
work_branch: workstream/t007-scaffold
pr_base: main
prior_specs: []
references:
  - docs/wayfinder/W001-public-chef-council/MAP.md
  - docs/wayfinder/W001-public-chef-council/issues/T001-repository-and-launch-scope.md
  - docs/wayfinder/W001-public-chef-council/issues/T003-license.md
  - docs/wayfinder/W001-public-chef-council/issues/T005-privacy-rules.md
  - .agents/spec-profile.md
cross_examined: meta/muse-wonder-full-1.0 (architect), 16 findings, 15 accepted
approved_by: autonomous
approved_at: 2026-11-18T18:12Z
pr: none
kickbacks: 0
merged: none
harvested: none
---

# Scaffold: agent entry files, kitchen templates, skills home, and CI

## Goal and definition of done

Build the skeleton any agent finds its way into (ticket T007): the canonical
`AGENTS.md` with its one-line `CLAUDE.md` and `GEMINI.md` imports, an MIT
`LICENSE`, the `kitchen/` fill-in templates, the `.agents/skills/` home with
its `.claude/skills/` link convention and a check for it, a `.gitignore`, and
CI that runs gitleaks over the full history.

Every file this spec adds is given byte for byte in `## File contents`, with
two exceptions that the tasks state exactly: the empty file
`.claude/skills/.gitkeep`, and `.agents/spec-profile.md`, an existing file
that gains eight inserted lines. Each task's gate checks the resulting bytes
with SHA-256. The executor transcribes; it does not redesign.

Done when all of these hold. `PR` is the pull request leg 2 opens from
`workstream/t007-scaffold` to `main`, and `HEAD_SHA` is its head commit.

1. **Fresh clone.** In a new temporary directory, `gh repo clone
   thecharlessamuel/chef-council <dir> -- --branch workstream/t007-scaffold`
   gives a checkout whose `git rev-parse HEAD` equals `HEAD_SHA`, and in it
   this prints nothing and exits 0:

   ```bash
   git ls-files --error-unmatch AGENTS.md CLAUDE.md GEMINI.md LICENSE .gitignore \
     kitchen/README.md kitchen/profile.md kitchen/equipment.md kitchen/pantry.md \
     .agents/skills/README.md .claude/skills/.gitkeep scripts/check-skills.py \
     scripts/secret-scan.sh tests/test_check_skills.py tests/test_secret_scan.py \
     .github/workflows/ci.yml README.md .agents/spec-profile.md > /dev/null
   ```

2. **Checks in the fresh clone.** In that clone, `python3
   scripts/check-skills.py; echo $?` prints `skills checked: 0` then `0`;
   `python3 -m unittest discover -s tests -v 2>&1 | tail -1` prints `OK`; and
   `wc -c < AGENTS.md` prints a number below 8192.
3. **CI is green.** `gh pr checks <PR>` lists exactly two checks, `gitleaks
   (full history)` and `skill links and tests`, both `pass`, and `gh pr view
   <PR> --json headRefOid --jq .headRefOid` prints `HEAD_SHA`.
4. **gitleaks fails on a planted secret.** The observation in
   `### Planted-secret observation` below, run in the fresh clone, prints
   exactly `planted: 1` and `clean: 0`, and `git status --porcelain` in the
   clone prints nothing afterwards. The fixture lives only in a temporary
   directory outside every clone, and is never committed to this repository
   or pushed anywhere.
5. **Rendered Markdown.** Render each file below from the pushed branch with
   the profile's Markdown observation method and look at the result. Every
   listed item must be visible; a missing item fails.
   - `AGENTS.md`: the five `##` headings (`Read in this order`, `Rules that
     are easy to get wrong`, `The loop`, `Skills`, `Making changes`); a
     three-item and an eleven-item numbered list; and the literal text
     `<Name>-style lens` in code style, angle brackets included.
   - `kitchen/README.md`: the three `##` headings and the three-item numbered
     list linking `profile.md`, `equipment.md`, and `pantry.md`.
   - `kitchen/profile.md`: the front matter visible at the top (GitHub
     renders it as a table), showing `filled_in`, `updated`, `units`, and
     `higher_risk_diners` with the values `no`, `none`, `none`, and
     `unknown`; six `##` sections; and an
     italic placeholder sentence under each of them (in `Standing
     corrections`, the italic example line).
   - `kitchen/equipment.md`: the front matter visible at the top (`filled_in`, `updated`);
     a four-column table with three example rows whose example text is
     italic; and the `Not owned` section with its italic placeholder.
   - `kitchen/pantry.md`: the front matter visible at the top (`filled_in`,
     `snapshot_date`) and a two-column table with ten rows whose second
     column is italic.
   - `.agents/skills/README.md`: a four-item numbered list holding three code
     blocks, with `<name>` visible, angle brackets included, in the first
     two.
6. **The one-line README is untouched.** `git diff --quiet
   32fbe81f22c0d080e51574d5edd41ef9490a1e9f HEAD -- README.md; echo $?`
   prints `0`.
7. **Sweeps.** On the committed, pushed branch with a clean working tree,
   after `git fetch origin`: the profile's committed-branch diff check with
   `BASE_SHA=32fbe81f22c0d080e51574d5edd41ef9490a1e9f` prints nothing; the
   Wayfinder lint, run as the profile says, exits 0; and the full privacy
   sweep exits 0 with a last line beginning `privacy sweep: clean`.

### Planted-secret observation

Run from the root of a checkout of this branch. It builds a throwaway git
repository in a temporary directory, commits a file holding a randomly
generated string in the shape of a GitHub personal access token (so no
secret-shaped text is ever written in this repository), scans it, scans the
checkout, and deletes the fixture.

```bash
FIXTURE=$(mktemp -d)
git -C "$FIXTURE" init -q
TOKEN=$(LC_ALL=C tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 36)
[ "${#TOKEN}" -eq 36 ] || echo "token generation failed"
printf 'token = ghp_%s\n' "$TOKEN" > "$FIXTURE/config.txt"
git -C "$FIXTURE" add config.txt
git -C "$FIXTURE" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m 'Plant a fake token'
planted=0; scripts/secret-scan.sh "$FIXTURE" > /dev/null 2>&1 || planted=$?
clean=0; scripts/secret-scan.sh > /dev/null 2>&1 || clean=$?
rm -rf "$FIXTURE"
echo "planted: $planted"; echo "clean: $clean"
if [ -e "$FIXTURE" ]; then echo "fixture still exists"; fi
```

Expected output is exactly the two lines `planted: 1` and `clean: 0`. Leg 1
measured exactly that on 2026-11-18, with this spec's files applied in a
scratch clone at `base_sha`.

## Decisions

Decisions T001, T003, and T005 bind this spec; the profile's
`## Pipeline constraints` apply to every file and every commit message.

1. **All content is fixed here.** Leg 1 wrote and tested every file in a
   scratch clone at `base_sha` (the tests, both scripts, the link check, the
   secret scan on clean and planted history, and the privacy sweep's `--text`
   on every file), then ran every task gate below against a second scratch
   clone built from this spec with the `extract` helper. Every task is
   therefore `mechanical`.
2. **`AGENTS.md`** generalizes `private-sources/cooking/AGENTS.md` under the
   design report's ledger row (`private-sources/design/design-report.md` §4):
   its structure is kept (read order, rules that are easy to get wrong, making
   changes), and the maintainer's name, the rules specific to the maintainer's
   notes app, the archive rule, and the personal standing corrections are
   dropped. What stays of mirroring is generic and comes from the ticket and
   the design loop (§2): never report a sync that did not happen, and mirror
   a card to a notes app only on request. It adds the loop and the skill
   index (design §6). It is 6,144 bytes, under the 8 KB limit.
3. **`AGENTS.md` names only what exists.** It links only to files this spec
   creates. Paths that later tickets introduce (the roster, the templates, the
   cards, the reports) are described in words, not paths; each later ticket
   adds its own paths. The skill index starts with one placeholder line that
   the first skill ticket replaces. Each index line has the form shown in
   `.agents/skills/README.md`.
4. **Real people.** `AGENTS.md` carries the profile's real-people rule in
   general form and names no chef: a lens is written `<Name>-style lens`, in
   a code span so the angle brackets render.
5. **`CLAUDE.md` is exactly `@AGENTS.md` and `GEMINI.md` exactly
   `@./AGENTS.md`**, each one line ending in a line feed (design §6).
6. **`LICENSE`** is the standard MIT text with the notice `Copyright (c) 2026
   Charles Samuel`: the name on the repository owner's GitHub account and on
   every commit. T003 fixes the license; the notice line is the only wording
   it left open.
7. **Kitchen templates.** Each of `profile.md`, `equipment.md`, and
   `pantry.md` opens with YAML front matter whose `filled_in: no` marks a
   blank template; `kitchen/README.md` tells the cook to set it to `yes`.
   This is the signal a later first-run interview reads. `profile.md` carries
   `updated`, `units` (`us`, `metric`, `both`; `none` until set), and
   `higher_risk_diners` (`yes`, `no`; `unknown` until answered).
   `equipment.md` carries `updated`; `pantry.md` carries `snapshot_date`.
   Placeholders in the kitchen files are italic text, never angle brackets,
   because GitHub drops unknown HTML tags. The council roster and its vetting
   file are a later ticket's and are not created or mentioned here.
8. **No household detail and no safety numbers in the templates.** The
   examples are invented and generic. `profile.md` describes higher-risk
   diners by example, without ages or a complete list; the later, cited
   food-safety reference owns the full list and every number. The templates
   also tell a forker that a public fork publishes `kitchen/`.
9. **Skills home.** `.agents/skills/README.md` documents the convention; an
   empty `.claude/skills/.gitkeep` makes the link directory exist. A skill is
   any directory under `.agents/skills/` whose name does not start with a
   dot.
10. **The check is `scripts/check-skills.py`** (Python 3 standard library),
    run as `python3 scripts/check-skills.py [repository-root]`; the root
    defaults to the script's own repository. More than one argument prints
    `usage: check-skills.py [repository-root]` on standard error and exits 2.
    When `.agents/skills` is not a directory it prints the single line
    `.agents/skills is missing` and exits 1. Otherwise, for each skill in
    name order, it reports these problems, in this order, each as
    `<name>: <problem>` on standard output:
    - `.agents/skills/<name>/SKILL.md is missing`;
    - one of `.claude/skills/<name> is missing`, `.claude/skills/<name> is
      not a symbolic link`, or `.claude/skills/<name> points to <target>,
      expected ../../.agents/skills/<name>` (the stored link target must be
      exactly that relative path);
    - `AGENTS.md does not name .agents/skills/<name>/SKILL.md` when that
      path does not occur in `AGENTS.md` (a missing `AGENTS.md` counts as
      empty).

    Every entry of `.claude/skills/` whose name does not start with a dot and
    has no skill is reported as `<name>: .claude/skills/<name> has no skill
    at .agents/skills/<name>`. All lines are sorted by name, a name's own
    lines keeping the order above. Any problem exits 1; none prints `skills
    checked: <N>` and exits 0. A missing `.claude/skills/` directory is not a
    problem by itself: with no skills the check passes, and with skills each
    one is reported as missing its link. The check does not validate
    `SKILL.md` front matter, and an `AGENTS.md` that exists but cannot be read
    is not handled (the traceback's non-zero exit still fails the check). The
    `AGENTS.md` requirement goes one step beyond the ticket's "every skill
    has its link" because the map requires each skill ticket to add both.
11. **Tests.** `tests/test_check_skills.py` observes the check only through
    its output and exit status, on temporary directories the tests build,
    with expected lines written as literals from decision 10.
    `tests/test_secret_scan.py` observes `scripts/secret-scan.sh` the same
    way, with a stub script standing in for gitleaks through `GITLEAKS_BIN`,
    so no test downloads anything; its expected values are the literals of
    decision 12. The tests create symbolic links and run Bash, so they are
    for Linux and macOS; CI runs them on Linux.
12. **Secret scan.** `scripts/secret-scan.sh [repository-directory]` is the
    one mechanism for CI and for a local run. It runs gitleaks 8.30.1 as
    `gitleaks git --log-opts=--all --redact --no-banner --verbose <repo>`:
    every commit reachable from any ref, with matched text redacted in the
    log. With no `GITLEAKS_BIN`, it downloads the release archive for Linux
    x86_64 into a private directory, checks it against the pinned SHA-256
    `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb` (the
    digest GitHub reports for the release asset, read on 2026-11-18), and
    moves the binary into `GITLEAKS_CACHE`, which defaults to
    `gitleaks-8.30.1` under the runner's temporary directory in CI and under
    `~/.cache/chef-council` elsewhere. Before every scan the binary, cached
    or supplied, must report version `8.30.1`. Exit 0 is clean and 1 is a
    leak. Exit 2, with one `secret-scan: <reason>` line on standard error,
    means the scan could not run: more than one argument (`usage:
    scripts/secret-scan.sh [repository-directory]`), `<dir> is not a git
    repository`, `<bin> is not an executable gitleaks`, `<bin> is gitleaks
    <version>, expected 8.30.1`, a failed download, checksum, or unpack, or
    `gitleaks exited with status <N>` for any other gitleaks status. The
    cached binary is not re-hashed on later runs: the cache is the user's own
    directory, and CI starts from an empty runner. The gitleaks GitHub Action
    is not used: on a pull request it scans only the pull request's commits,
    and the ticket requires the full history.
13. **CI** is one workflow, `.github/workflows/ci.yml`, on every pull request
    and every push to `main`, with two jobs: `gitleaks (full history)`
    (checkout with `fetch-depth: 0`, then the script) and `skill links and
    tests` (the check and the unit tests). The only action used is
    `actions/checkout`, pinned to commit
    `3d3c42e5aac5ba805825da76410c181273ba90b1` (tag `v7.0.1`, read on
    2026-11-18), with `persist-credentials: false`; the workflow's permission
    is `contents: read`. The second job goes beyond the ticket's gitleaks
    requirement so the link check and the tests run on every change. The
    Wayfinder lint is not in CI because its script lives outside this
    repository.
14. **`.gitignore`** ignores `.sources/` (source packets), local agent
    settings and overrides, `.env` files, Python caches, and operating-system
    and editor files. It names nothing maintainer-specific.
15. **Profile.** The profile says the spec that adds a check records its
    local command, so Task 5 adds one bullet to `.agents/spec-profile.md`.
16. **`README.md` is not touched** (a later ticket replaces it).

## Prerequisites

- Leg 2 starts from this spec's approval commit on `workstream/t007-scaffold`,
  which already holds the claim commit for T007. Staging, the per-task commit
  with its `Spec-Task: S001/<N>` trailer, the push, the pull request, and the
  base-drift check are the `2-spec-execute` skill's standing procedure and
  the profile's ship tail; this spec adds nothing to them. A task's commit
  holds exactly that task's Touches.
- The executor's machine is Linux x86_64 with Git, Bash, Python 3, GNU
  coreutils (`sha256sum`, `mktemp`, `head`, `tr`), `curl`, `tar`, and an
  authenticated `gh`. The gates are not written for another platform.
- `git config user.email` ends in `@users.noreply.github.com` (profile).
- `origin` is reached over SSH, so pushing a workflow file needs no `workflow`
  token scope. If the push of `.github/workflows/ci.yml` is rejected, report
  ``Question: the push of `workstream/t007-scaffold` was rejected: <reason>.``
- GitHub Actions is enabled for the repository (measured 2026-11-18:
  enabled, all actions allowed). If no check run appears on the pull request,
  that is a question for the human (profile).
- Network access to `github.com` release downloads for the first
  `scripts/secret-scan.sh` run on a machine.

### Writing a file from this spec

Each file under `## File contents` is the text inside the fenced block that
follows its `#### File:` heading: every line between the opening and closing
fence, each ended by a line feed, with nothing added or removed. This helper
writes one such file exactly, and the executor may use it:

```bash
extract() {
  mkdir -p "$(dirname "$1")"
  python3 - docs/specs/S001-scaffold.md "$1" > "$1" <<'PY'
import sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index("#### File: `%s`" % sys.argv[2])
opening = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("````"))
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "````")
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
}
```

Usage: `extract kitchen/profile.md`. It covers the `#### File:` blocks only;
the two exceptions named in the goal are written as their tasks say. The
SHA-256 gates decide whether a file is right, whichever way it was written.

### Link check

A gate helper, not a repository file. It reads the Markdown files named on its
command line, skips fenced code blocks, and requires the target of every
inline link of the form `[text](target)` with a relative target to be a path
git tracks or has staged. That is the only link form these files use; it does
not understand reference-style links or link titles. It prints one line per
broken link and returns 1, or prints nothing and returns 0.

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

## Build plan — agent loop

Run every command from the repository root, in one Bash shell per task in
which the gate's setup has been run first: `OUT=$(mktemp)` (a temporary file
outside the repository) and, where a gate uses them, the `extract` and
`linkcheck` function definitions above, pasted as written. A gate passes only
when every command in it prints what is stated. Where a gate ends in `; echo
$?`, the printed status is part of the expected output, and a non-zero status
that is expected is not a failure.

### Task 1 — Tests for the two scripts
- **Work:** Create `tests/test_check_skills.py` and
  `tests/test_secret_scan.py` with exactly the content given under their
  `#### File:` headings. The seams under test are two commands, observed only
  through standard output, standard error, and exit status.
  - `python3 scripts/check-skills.py [repository-root]` (decision 10). Each
    test builds a repository root in a temporary directory and catches one
    behavior: no skills passes with `skills checked: 0`, also with no
    `.claude/skills/`; linked and indexed skills pass; a missing link, a
    copied directory, a text file in place of a link, a wrong target, and an
    absolute target each fail with their literal line; a link with no skill
    fails; a missing `SKILL.md` fails; a missing `AGENTS.md` line fails, also
    when a longer skill name is indexed; several problems print in name
    order; a missing `.agents/skills` fails; a missing `AGENTS.md` fails; an
    extra argument is a usage error; and the check passes on this repository.
  - `bash scripts/secret-scan.sh [repository-directory]` (decision 12), with
    a stub gitleaks supplied through `GITLEAKS_BIN`. The tests catch: stub
    status 0 gives 0 and 1 gives 1; another status gives 2 with its message;
    the stub receives exactly `git --log-opts=--all --redact --no-banner
    --verbose <repo>`; the default target is this repository; a directory
    that is not a repository, an extra argument, a stub reporting another
    version, and a missing binary each give 2 with their literal message.
- **Touches:** `tests/test_check_skills.py`, `tests/test_secret_scan.py`
- **Gate:**
  - This prints `tests/test_check_skills.py: OK` and
    `tests/test_secret_scan.py: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    ab44ed9175cd5a90722ca005b7ce25d73559ca374f3c3f1fc34bdce46ecf6b37  tests/test_check_skills.py
    c8aa3f174097b53643260b1c4df250baca8d115868e75c72c7cf6736420ff80e  tests/test_secret_scan.py
    SUMS
    ```

  - With the working tree differing from `base_sha` only under `docs/` and in
    these two test files, `python3 -m unittest discover -s tests -v > "$OUT"
    2>&1; echo $?` prints `1`, and `tail -1 "$OUT"` prints `FAILED
    (failures=24, errors=2)`. This is the recorded red: leg 1 measured it on
    2026-11-18 in a scratch clone at `base_sha` with only the two test files
    applied. All 26 tests are red because neither script exists yet. 24 fail
    by assertion. Two, `test_default_target_is_this_repository` and
    `test_scans_every_ref_with_redaction` of `SecretScanTest`, are errors: a
    `FileNotFoundError` reading the stub's argument file, which the absent
    script never caused to be written. None is an import error. The 24
    failures are all 17 methods of `CheckSkillsTest`
    (`test_absolute_target_fails`, `test_copied_directory_is_not_a_link`,
    `test_every_problem_is_reported_in_name_order`,
    `test_extra_argument_is_a_usage_error`, `test_link_without_skill_fails`,
    `test_linked_and_indexed_skills_pass`, `test_missing_agents_file_fails`,
    `test_missing_index_line_fails`, `test_missing_link_fails`,
    `test_missing_skill_file_fails`, `test_missing_skills_home_fails`,
    `test_no_links_home_passes_without_skills`, `test_no_skills_passes`,
    `test_similar_skill_name_is_not_an_index_line`,
    `test_text_file_is_not_a_link`, `test_this_repository_passes`,
    `test_wrong_target_fails`) and 7 methods of `SecretScanTest`
    (`test_clean_scan_exits_zero`,
    `test_directory_that_is_not_a_repository_exits_two`,
    `test_extra_argument_exits_two`, `test_leak_exits_one`,
    `test_missing_binary_exits_two`, `test_scanner_error_exits_two`,
    `test_wrong_version_exits_two`).
- **Nature:** mechanical

### Task 2 — The two scripts and the skills home
- **Work:** Create `scripts/check-skills.py`, `scripts/secret-scan.sh`, and
  `.agents/skills/README.md` with exactly the content given under their
  `#### File:` headings; make the scan executable (`chmod 755
  scripts/secret-scan.sh`); and create `.claude/skills/.gitkeep` as an empty
  file (`mkdir -p .claude/skills && : > .claude/skills/.gitkeep`). Do not
  change anything under `tests/`; a test that seems to need a change is
  reported as ``Question: Task 2 of `docs/specs/S001-scaffold.md` needs a
  test the tests task wrote changed; revise the spec?``
- **Touches:** `scripts/check-skills.py`, `scripts/secret-scan.sh`,
  `.agents/skills/README.md`, `.claude/skills/.gitkeep`
- **Gate:**
  - This prints four lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    0b8b37cfdce07d1aa269cf271f86d95cd180442d35272cb5fc3810d37d78e9dd  scripts/check-skills.py
    28cb8babfd8fa6c1259e53c56fa4d667f7df83e3349d241b71648a2ae7cf6c54  scripts/secret-scan.sh
    a2375746a71f91b952b1d6830d48001eb71d5cb4283762f5e06b7f7d22914b76  .agents/skills/README.md
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  .claude/skills/.gitkeep
    SUMS
    ```

  - After `git add scripts/secret-scan.sh`, `git ls-files -s
    scripts/secret-scan.sh` prints a line beginning `100755`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0` and `tail -1 "$OUT"` prints `OK`.
  - `python3 scripts/check-skills.py; echo $?` prints `skills checked: 0` then
    `0`.
  - `scripts/secret-scan.sh > "$OUT" 2>&1; echo $?` prints `0`, and `grep -c
    'no leaks found' "$OUT"` prints `1`. Leg 1 measured exit 0 on the base
    history on 2026-11-18.
  - The planted-secret observation under `## Goal and definition of done`
    prints exactly `planted: 1` and `clean: 0`.
  - The tests are unchanged. Before the commit, `git status --porcelain --
    tests/` prints nothing. After it, this prints only `tests unchanged`:

    ```bash
    TASK1_SHA=$(git log --format=%H -1 --grep='^Spec-Task: S001/1$')
    [ -n "$TASK1_SHA" ] && git merge-base --is-ancestor "$TASK1_SHA" HEAD &&
      [ -z "$(git diff --name-only "$TASK1_SHA..HEAD" -- tests/)" ] &&
      echo "tests unchanged"
    ```
- **Nature:** mechanical

### Task 3 — Kitchen templates
- **Work:** Create `kitchen/README.md`, `kitchen/profile.md`,
  `kitchen/equipment.md`, and `kitchen/pantry.md` with exactly the content
  given under their `#### File:` headings.
- **Touches:** `kitchen/README.md`, `kitchen/profile.md`,
  `kitchen/equipment.md`, `kitchen/pantry.md`
- **Gate:**
  - This prints four lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    f8cb74687da39eafca79961d3d95fe3e8285cf869ca6f9eb118f2ba9cb57a4fb  kitchen/README.md
    034d44edce778fabf04f399bae7f71822ce2e69b9f47673b1f46ac86ef96fd06  kitchen/profile.md
    5f02780f4faf7812d45b0d8d5f505f1885fc03e8c0d494b3aa92cb0e68debefa  kitchen/equipment.md
    322e7530db91b96bb486fe0e1ccbe3aa9886c5df8c216f77e988c895a7fd61b1  kitchen/pantry.md
    SUMS
    ```

  - `grep -c '^filled_in: no$' kitchen/profile.md kitchen/equipment.md
    kitchen/pantry.md` prints `kitchen/profile.md:1`,
    `kitchen/equipment.md:1`, and `kitchen/pantry.md:1`, and `grep -c
    '^higher_risk_diners: unknown$' kitchen/profile.md` prints `1`.
  - `grep -n '<' kitchen/*.md; echo $?` prints only `1` (no angle-bracket
    placeholder).
  - After `git add kitchen`, `linkcheck kitchen/README.md kitchen/profile.md
    kitchen/equipment.md kitchen/pantry.md; echo $?` prints only `0`.
- **Nature:** mechanical

### Task 4 — Entry files, license, and ignore rules
- **Work:** Create `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `LICENSE`, and
  `.gitignore` with exactly the content given under their `#### File:`
  headings. Do not change `README.md`.
- **Touches:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `LICENSE`, `.gitignore`
- **Gate:**
  - This prints five lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    486e2a0c9bca8e98fd6856d870c8123ab5271e017e07919b9b77897e94cfbe75  AGENTS.md
    336cc4fbf19beaada7ccf9986414fa91851a8d7a07dfb3ccbe800a69eed0ab49  CLAUDE.md
    42fbbc9d55ee0d149c90e4bf93abe8b7278a5482b232be6f5bfc59cc0465e694  GEMINI.md
    04fa2dc87edd6d2b7feb8e218780ac5b528380afceba4d9111cb7eefd5d5981d  LICENSE
    d7198d437178a35986f529c297bd0dc7ad8cccfd9af10c11a0907b6f6ce45201  .gitignore
    SUMS
    ```

  - `wc -c < AGENTS.md` prints `6144`, which is below 8192.
  - `git check-ignore -q .sources/packet.md; echo $?` prints `0`, and `git
    check-ignore -q kitchen/profile.md; echo $?` prints `1`.
  - After `git add AGENTS.md CLAUDE.md GEMINI.md LICENSE .gitignore`,
    `linkcheck AGENTS.md .agents/skills/README.md; echo $?` prints only `0`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0`, and `python3 scripts/check-skills.py` prints `skills checked: 0`.
  - `git diff --quiet 32fbe81f22c0d080e51574d5edd41ef9490a1e9f -- README.md;
    echo $?` prints `0`.
- **Nature:** mechanical

### Task 5 — CI workflow and the profile's check list
- **Work:**
  1. Create `.github/workflows/ci.yml` with exactly the content given under
     its `#### File:` heading.
  2. In `.agents/spec-profile.md`, insert exactly the eight lines given under
     `#### Insert: .agents/spec-profile.md` directly after the line that
     reads `command in this list.` behind four spaces of indentation. That
     line occurs once, under `## Verify`, and ends the first bullet of
     `Deterministic checks`. Change nothing else in the profile.
- **Touches:** `.github/workflows/ci.yml`, `.agents/spec-profile.md`
- **Gate:**
  - This prints two lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    38617a826a486bc7ed25c580dc3d51e91e21863cc57e4f36fdc2d81ebfa6769d  .github/workflows/ci.yml
    67f40bc17a20b4d5a8d75f6854fadf61bb1df91c50027085c8e97aebe0b3e6b3  .agents/spec-profile.md
    SUMS
    ```

  - `git diff --numstat 32fbe81f22c0d080e51574d5edd41ef9490a1e9f --
    .agents/spec-profile.md` prints one line whose tab-separated fields are
    `8`, `0`, and `.agents/spec-profile.md`.
  - Every action is pinned by commit SHA. This prints `2` (the `uses:` lines
    in the workflow), then `0` (those not pinned to a 40-character commit
    SHA), then `1` (the status of the last `grep`, which matched nothing):

    ```bash
    grep -chE '^[[:space:]]*(- )?uses:' .github/workflows/ci.yml
    grep -hE '^[[:space:]]*(- )?uses:' .github/workflows/*.yml | grep -vcE 'uses: [^@[:space:]]+@[0-9a-f]{40}( #.*)?$'; echo $?
    ```

  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0`, `python3 scripts/check-skills.py` prints `skills checked: 0`, and
    `scripts/secret-scan.sh > "$OUT" 2>&1; echo $?` prints `0`.
- **Nature:** mechanical

## File contents`, and
each task's gate checks the bytes with SHA-256. The executor transcribes; it
does not redesign.

Done when all of these hold. `PR` is the pull request leg 2 opens from
`workstream/t007-scaffold` to `main`, and `HEAD_SHA` is its head commit.

1. **Fresh clone.** In a new temporary directory, `gh repo clone
   thecharlessamuel/chef-council <dir> -- --branch workstream/t007-scaffold`
   gives a checkout whose `git rev-parse HEAD` equals `HEAD_SHA`, and in it
   this prints nothing and exits 0:

   ```bash
   git ls-files --error-unmatch AGENTS.md CLAUDE.md GEMINI.md LICENSE .gitignore \
     kitchen/README.md kitchen/profile.md kitchen/equipment.md kitchen/pantry.md \
     .agents/skills/README.md .claude/skills/.gitkeep scripts/check-skills.py \
     scripts/secret-scan.sh tests/test_check_skills.py .github/workflows/ci.yml \
     README.md .agents/spec-profile.md > /dev/null
   ```

2. **Checks in the fresh clone.** In that clone, `python3
   scripts/check-skills.py` prints `skills checked: 0` and exits 0;
   `python3 -m unittest discover -s tests -v` ends with the line `OK`; and
   `wc -c < AGENTS.md` prints a number below 8192.
3. **CI is green.** `gh pr checks <PR>` lists exactly two checks, `gitleaks
   (full history)` and `skill links and tests`, both `pass`, for `HEAD_SHA`.
4. **gitleaks fails on a planted secret.** The observation in
   `### Planted-secret observation` below, run in the fresh clone, prints
   exactly `planted: 1` and `clean: 0`, and `git status --porcelain` in the
   clone prints nothing afterwards. The fixture lives only in a temporary directory outside every clone, and is
   never committed to this repository or pushed anywhere.
5. **Rendered Markdown.** Render `AGENTS.md`, `kitchen/README.md`,
   `kitchen/profile.md`, `kitchen/equipment.md`, `kitchen/pantry.md`, and
   `.agents/skills/README.md` from the pushed branch with the profile's
   Markdown observation method and look at each result: every heading, list,
   and table renders as such; every placeholder is visible as italic text (no
   text has vanished as an unknown HTML tag); and each of the three kitchen
   templates shows its front matter fields.
6. **The one-line README is untouched.** `git diff --quiet
   32fbe81f22c0d080e51574d5edd41ef9490a1e9f HEAD -- README.md` exits 0.
7. **Sweeps.** The profile's diff checks, the Wayfinder lint, and the full
   privacy sweep (`privacy sweep: clean`) pass on the branch.

### Planted-secret observation

Run from the root of the fresh clone. It builds a throwaway git repository in
a temporary directory, commits a file holding a randomly generated string in
the shape of a GitHub personal access token (so no secret-shaped text is ever
written in this repository), scans it, scans the clone, and deletes the
fixture.

```bash
FIXTURE=$(mktemp -d)
git -C "$FIXTURE" init -q
printf 'token = ghp_%s\n' "$(head -c 256 /dev/urandom | LC_ALL=C tr -dc 'A-Za-z0-9' | head -c 36)" > "$FIXTURE/config.txt"
git -C "$FIXTURE" add config.txt
git -C "$FIXTURE" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m 'Plant a fake token'
planted=0; scripts/secret-scan.sh "$FIXTURE" > /dev/null 2>&1 || planted=$?
clean=0; scripts/secret-scan.sh > /dev/null 2>&1 || clean=$?
rm -rf "$FIXTURE"
echo "planted: $planted"; echo "clean: $clean"
if [ -e "$FIXTURE" ]; then echo "fixture still exists"; fi
```

Expected output is exactly the two lines `planted: 1` and `clean: 0`. Measured
by leg 1 on 2026-11-18 with the prototype of this spec's files in a scratch
clone at `base_sha`: `planted: 1`, `clean: 0`.

## Decisions

Decisions T001, T003, and T005 bind this spec; the profile's
`## Pipeline constraints` apply to every file and every commit message.

1. **All content is fixed here.** Leg 1 wrote and tested every file in a
   scratch clone at `base_sha` (the tests, both scripts, the link check, the
   secret scan on clean and planted history, and the privacy sweep's `--text`
   on every file). Every task is therefore `mechanical`.
2. **`AGENTS.md`** generalizes `private-sources/cooking/AGENTS.md` under the
   design report's ledger row (`private-sources/design/design-report.md` §4):
   its structure is kept (read order, rules that are easy to get wrong, making
   changes), and the maintainer's name, the notes-app rules, the archive rule,
   and the personal standing corrections are dropped. It adds the loop (design
   §2) and the skill index (design §6). It is 6,144 bytes, under the 8 KB
   limit.
3. **`AGENTS.md` names only what exists.** It links only to files this spec
   creates. Paths that later tickets introduce (the roster, the templates, the
   cards, the reports) are described in words, not paths; each later ticket
   adds its own paths. The skill index starts with one placeholder line that
   the first skill ticket replaces. Each index line has the form shown in
   `.agents/skills/README.md`.
4. **Real people.** `AGENTS.md` carries the T002 rule in general form and
   names no chef: a lens is written `<Name>-style lens`, in a code span so the
   angle brackets render.
5. **`CLAUDE.md` is exactly `@AGENTS.md` and `GEMINI.md` exactly
   `@./AGENTS.md`**, each one line ending in a newline (design §6).
6. **`LICENSE`** is the standard MIT text with the notice `Copyright (c) 2026
   Charles Samuel`: the name on the repository owner's GitHub account and on
   every commit. T003 fixes the license; the notice line is the only wording
   it left open.
7. **Kitchen templates.** Each of `profile.md`, `equipment.md`, and
   `pantry.md` opens with YAML front matter whose `filled_in: no` marks a
   blank template; `kitchen/README.md` tells the cook to set it to `yes`.
   This is the signal T009's first-run interview reads. `profile.md` carries
   `updated`, `units` (`us`, `metric`, `both`; `none` until set), and
   `higher_risk_diners` (`yes`, `no`; `unknown` until answered).
   `equipment.md` carries `updated`; `pantry.md` carries `snapshot_date`.
   Placeholders are italic text, never angle brackets, because GitHub drops
   unknown HTML tags. `kitchen/council.md` and `kitchen/council-vetting.md`
   are T008's and are not created or mentioned here.
8. **No household detail and no safety numbers in the templates.** The
   examples are invented and generic. `profile.md` describes higher-risk
   diners by example without ages or a complete list; T009's cited
   food-safety reference owns the full list and every number. The templates
   also tell a forker that a public fork publishes `kitchen/`.
9. **Skills home.** `.agents/skills/README.md` documents the convention; an
   empty `.claude/skills/.gitkeep` makes the link directory exist. A skill is
   any directory under `.agents/skills/` whose name does not start with a
   dot.
10. **The check is `scripts/check-skills.py`** (Python 3 standard library).
    For every skill it requires `.agents/skills/<name>/SKILL.md`, a symbolic
    link `.claude/skills/<name>` whose stored target is exactly
    `../../.agents/skills/<name>`, and the text
    `.agents/skills/<name>/SKILL.md` somewhere in `AGENTS.md`; and it rejects
    any non-dot entry in `.claude/skills/` with no skill behind it. The
    `AGENTS.md` requirement goes one step beyond the ticket's "every skill
    has its link" because the map requires each skill ticket to add both, and
    one check for both is cheaper than two. It prints one line per problem,
    `<name>: <problem>`, sorted by name, and exits 1; with none it prints
    `skills checked: <N>` and exits 0; a usage error exits 2. It takes an
    optional repository root and defaults to its own repository. It does not
    validate `SKILL.md` front matter.
11. **Tests.** `tests/test_check_skills.py` observes the check only through
    its standard output and exit status, on temporary directories built by
    the tests, with expected lines written as literals from decision 10.
12. **Secret scan.** `scripts/secret-scan.sh` is the one mechanism for CI
    and for a local run. It runs gitleaks 8.30.1 as `gitleaks git
    --log-opts=--all --redact --no-banner --verbose <repo>`: every commit
    reachable from any ref, with matched text redacted in the log. With no
    `GITLEAKS_BIN`, it downloads the release archive for Linux x86_64, checks
    it against the pinned SHA-256
    `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb` (the
    digest GitHub reports for the release asset, read on 2026-11-18), and
    caches the binary. Exit 0 is clean, 1 is a leak, 2 is a scan that could
    not run. The gitleaks GitHub Action is not used: on a pull request it
    scans only the pull request's commits, and the ticket requires the full
    history.
13. **CI** is one workflow, `.github/workflows/ci.yml`, on every pull request
    and every push to `main`, with two jobs: `gitleaks (full history)`
    (checkout with `fetch-depth: 0`, then the script) and `skill links and
    tests` (the check and the unit tests). The only action used is
    `actions/checkout`, pinned to commit
    `3d3c42e5aac5ba805825da76410c181273ba90b1` (tag `v7.0.1`, read on
    2026-11-18), with `persist-credentials: false`; the workflow's permission
    is `contents: read`. The second job goes beyond the ticket's gitleaks
    requirement so the link check and its tests run on every change. The
    Wayfinder lint is not in CI because its script lives outside this
    repository.
14. **`.gitignore`** ignores `.sources/` (source packets), local agent
    settings and overrides, `.env` files, Python caches, and operating-system
    and editor files. It names nothing maintainer-specific.
15. **Profile.** The profile says the spec that adds a check records its
    local command, so Task 5 adds one bullet to `.agents/spec-profile.md`.
16. **`README.md` is not touched** (T014 replaces it).

## Prerequisites

- Leg 2 starts from this spec's approval commit on `workstream/t007-scaffold`,
  which already holds the claim commit for T007.
- `git config user.email` ends in `@users.noreply.github.com` (profile).
- `origin` is reached over SSH, so pushing a workflow file needs no `workflow`
  token scope. If the push of `.github/workflows/ci.yml` is rejected, report
  ``Question: the push of `workstream/t007-scaffold` was rejected: <reason>.``
- GitHub Actions is enabled for the repository (measured 2026-11-18:
  enabled, all actions allowed). If no check run appears on the pull request,
  that is a question for the human (profile).
- Network access to `github.com` release downloads for the first
  `scripts/secret-scan.sh` run on a machine, on Linux x86_64. On another
  platform set `GITLEAKS_BIN` to an installed gitleaks 8.30.1.

### Writing a file from this spec

Each file under `## File contents` is the text inside the fenced block that
follows its `#### File:` heading: every line between the opening and closing
fence, each ended by a line feed, with nothing added or removed. This helper
writes one such file exactly, and the executor may use it:

```bash
extract() {
  mkdir -p "$(dirname "$1")"
  python3 - docs/specs/S001-scaffold.md "$1" > "$1" <<'PY'
import sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index("#### File: `%s`" % sys.argv[2])
opening = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("````"))
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "````")
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
}
```

Usage: `extract kitchen/profile.md`. The SHA-256 gates decide whether a file
is right, whichever way it was written.

## Build plan — agent loop

Run every command from the repository root. `OUT` is a temporary file outside
the repository (`OUT=$(mktemp)`). A gate passes only when every command in it
behaves as stated.

### Task 1 — Tests for the skill check
- **Work:** Create `tests/test_check_skills.py` with exactly the content
  given under `#### File: tests/test_check_skills.py`. The seam under test is
  the command `python3 scripts/check-skills.py [repository-root]`: its
  standard output lines and its exit status. Each test builds a repository
  root in a temporary directory and catches one behavior from decision 10: no
  skills passes with `skills checked: 0`; linked and indexed skills pass; a
  missing link, a copied directory, a text file in place of a link, a wrong
  target, and an absolute target each fail with their literal line; a link
  with no skill fails; a missing `SKILL.md` fails; a missing `AGENTS.md` line
  fails, also when a longer skill name is indexed; several problems print in
  name order; a missing `.agents/skills` fails; a missing `AGENTS.md` fails;
  and the check passes on this repository itself.
- **Touches:** `tests/test_check_skills.py`
- **Gate:**
  - `sha256sum -c` on this line prints `tests/test_check_skills.py: OK`:

    ```text
    ab44ed9175cd5a90722ca005b7ce25d73559ca374f3c3f1fc34bdce46ecf6b37  tests/test_check_skills.py
    ```

  - With the working tree differing from `base_sha` only under `docs/` and in
    this test file, `python3 -m unittest discover -s tests -v > "$OUT" 2>&1;
    echo $?` prints `1`, and `tail -1 "$OUT"` prints `FAILED (failures=15)`.
    This is the recorded red: leg 1 measured it on 2026-11-18 in a scratch
    clone at `base_sha` with only the test file applied. All 15 tests fail
    by assertion (`grep -c '^FAIL:' "$OUT"` prints `15`, `grep -c '^ERROR:'
    "$OUT"` prints `0`), because the script does not exist yet and the
    interpreter exits 2 with empty standard output; no test fails on import.
    The failing tests are every method of `CheckSkillsTest`:
    `test_absolute_target_fails`, `test_copied_directory_is_not_a_link`,
    `test_every_problem_is_reported_in_name_order`,
    `test_link_without_skill_fails`, `test_linked_and_indexed_skills_pass`,
    `test_missing_agents_file_fails`, `test_missing_index_line_fails`,
    `test_missing_link_fails`, `test_missing_skill_file_fails`,
    `test_missing_skills_home_fails`, `test_no_skills_passes`,
    `test_similar_skill_name_is_not_an_index_line`,
    `test_text_file_is_not_a_link`, `test_this_repository_passes`, and
    `test_wrong_target_fails`.
- **Nature:** mechanical

### Task 2 — The skill check and the skills home
- **Work:** Create `scripts/check-skills.py` and `.agents/skills/README.md`
  with exactly the content given under their `#### File:` headings, and
  create `.claude/skills/.gitkeep` as an empty file (`mkdir -p .claude/skills
  && : > .claude/skills/.gitkeep`). Do not change anything under `tests/`; a
  test that seems to need a change is reported as ``Question: Task 2 of
  `docs/specs/S001-scaffold.md` needs a test the tests task wrote changed;
  revise the spec?``
- **Touches:** `scripts/check-skills.py`, `.agents/skills/README.md`,
  `.claude/skills/.gitkeep`
- **Gate:**
  - `sha256sum -c` on these lines prints `OK` for each:

    ```text
    0b8b37cfdce07d1aa269cf271f86d95cd180442d35272cb5fc3810d37d78e9dd  scripts/check-skills.py
    a2375746a71f91b952b1d6830d48001eb71d5cb4283762f5e06b7f7d22914b76  .agents/skills/README.md
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  .claude/skills/.gitkeep
    ```

  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0` and `tail -1 "$OUT"` prints `OK`.
  - `python3 scripts/check-skills.py; echo $?` prints `skills checked: 0` then
    `0`.
  - Before the commit, `git status --porcelain -- tests/` prints nothing;
    after it, `git diff --name-only "$(git log --format=%H -1
    --grep='^Spec-Task: S001/1$')"..HEAD -- tests/` prints nothing.
- **Nature:** mechanical

### Task 3 — Kitchen templates
- **Work:** Create `kitchen/README.md`, `kitchen/profile.md`,
  `kitchen/equipment.md`, and `kitchen/pantry.md` with exactly the content
  given under their `#### File:` headings.
- **Touches:** `kitchen/README.md`, `kitchen/profile.md`,
  `kitchen/equipment.md`, `kitchen/pantry.md`
- **Gate:**
  - `sha256sum -c` on these lines prints `OK` for each:

    ```text
    f8cb74687da39eafca79961d3d95fe3e8285cf869ca6f9eb118f2ba9cb57a4fb  kitchen/README.md
    034d44edce778fabf04f399bae7f71822ce2e69b9f47673b1f46ac86ef96fd06  kitchen/profile.md
    5f02780f4faf7812d45b0d8d5f505f1885fc03e8c0d494b3aa92cb0e68debefa  kitchen/equipment.md
    322e7530db91b96bb486fe0e1ccbe3aa9886c5df8c216f77e988c895a7fd61b1  kitchen/pantry.md
    ```

  - `grep -c '^filled_in: no$' kitchen/profile.md kitchen/equipment.md
    kitchen/pantry.md` prints `1` for each of the three files, and `grep -c
    '^higher_risk_diners: unknown$' kitchen/profile.md` prints `1`.
  - `grep -n '<' kitchen/*.md` prints nothing (no angle-bracket placeholder).
  - With the four files staged (`git add kitchen`), the link check in
    `### Link check` below, run as `linkcheck kitchen/README.md
    kitchen/profile.md kitchen/equipment.md kitchen/pantry.md; echo $?`,
    prints only `0`.
- **Nature:** mechanical

### Task 4 — Entry files, license, and ignore rules
- **Work:** Create `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `LICENSE`, and
  `.gitignore` with exactly the content given under their `#### File:`
  headings. Do not change `README.md`.
- **Touches:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `LICENSE`, `.gitignore`
- **Gate:**
  - `sha256sum -c` on these lines prints `OK` for each:

    ```text
    486e2a0c9bca8e98fd6856d870c8123ab5271e017e07919b9b77897e94cfbe75  AGENTS.md
    336cc4fbf19beaada7ccf9986414fa91851a8d7a07dfb3ccbe800a69eed0ab49  CLAUDE.md
    42fbbc9d55ee0d149c90e4bf93abe8b7278a5482b232be6f5bfc59cc0465e694  GEMINI.md
    04fa2dc87edd6d2b7feb8e218780ac5b528380afceba4d9111cb7eefd5d5981d  LICENSE
    d7198d437178a35986f529c297bd0dc7ad8cccfd9af10c11a0907b6f6ce45201  .gitignore
    ```

  - `wc -c < AGENTS.md` prints `6144`, which is below 8192.
  - `git check-ignore -q .sources/packet.md; echo $?` prints `0`, and `git
    check-ignore -q kitchen/profile.md; echo $?` prints `1`.
  - With the five files staged, `linkcheck AGENTS.md .agents/skills/README.md;
    echo $?` (`### Link check`) prints only `0`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0`, and `python3 scripts/check-skills.py` prints `skills checked: 0`.
  - `git diff --quiet 32fbe81f22c0d080e51574d5edd41ef9490a1e9f -- README.md;
    echo $?` prints `0`.
- **Nature:** mechanical

### Task 5 — Secret scan, CI workflow, and the profile's check list
- **Work:**
  1. Create `scripts/secret-scan.sh` with exactly the content given under its
     `#### File:` heading and make it executable (`chmod 755
     scripts/secret-scan.sh`).
  2. Create `.github/workflows/ci.yml` with exactly the content given under
     its `#### File:` heading.
  3. In `.agents/spec-profile.md`, under `## Verify`, directly after the
     bullet that ends `The spec that adds a check records its local` /
     `command in this list.` and before the bullet that begins `- The
     wayfinder skill's`, insert exactly the eight lines given under `####
     Insert: .agents/spec-profile.md`. Change nothing else in the profile.
- **Touches:** `scripts/secret-scan.sh`, `.github/workflows/ci.yml`,
  `.agents/spec-profile.md`
- **Gate:**
  - `sha256sum -c` on these lines prints `OK` for each:

    ```text
    28cb8babfd8fa6c1259e53c56fa4d667f7df83e3349d241b71648a2ae7cf6c54  scripts/secret-scan.sh
    38617a826a486bc7ed25c580dc3d51e91e21863cc57e4f36fdc2d81ebfa6769d  .github/workflows/ci.yml
    67f40bc17a20b4d5a8d75f6854fadf61bb1df91c50027085c8e97aebe0b3e6b3  .agents/spec-profile.md
    ```

  - `git diff --numstat 32fbe81f22c0d080e51574d5edd41ef9490a1e9f --
    .agents/spec-profile.md` prints one line whose tab-separated fields are
    `8`, `0`, and `.agents/spec-profile.md`.
  - After `git add scripts/secret-scan.sh`, `git ls-files -s
    scripts/secret-scan.sh` prints a line beginning `100755`.
  - `grep -hE '^[[:space:]]*(- )?uses:' .github/workflows/*.yml | grep -vcE
    'uses: [^@[:space:]]+@[0-9a-f]{40}( #.*)?$'` prints `0`, and `grep -chE
    '^[[:space:]]*(- )?uses:' .github/workflows/ci.yml` prints `2`.
  - `scripts/secret-scan.sh > "$OUT" 2>&1; echo $?` prints `0` and `grep -c
    'no leaks found' "$OUT"` prints `1`. Leg 1 measured exit 0 on the base
    history on 2026-11-18.
  - The planted-secret observation under `## Goal and definition of done`,
    run from the repository root, prints exactly `planted: 1` and `clean: 0`.
  - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?` prints
    `0`, and `python3 scripts/check-skills.py` prints `skills checked: 0`.
- **Nature:** mechanical

### Link check

A gate helper, not a repository file. It reads the Markdown files named on its
command line, skips fenced code blocks, and requires every relative link
target to be a file git tracks or has staged. It prints one line per broken
link and returns 1, or prints nothing and returns 0.

```bash
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
            if subprocess.run(["git", "ls-files", "--error-unmatch", target], capture_output=True).returncode:
                print("%s: broken link %s" % (path, target))
                bad = 1
sys.exit(bad)
PY
}
```

## File contents

Each block below is one file, byte for byte (see `### Writing a file from this
spec` for how to read a block). The fences are four backticks because some files contain
three-backtick blocks of their own.

#### File: `tests/test_check_skills.py`

````python
"""Tests for scripts/check-skills.py, observed through its output and exit status."""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "check-skills.py")


def run(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        check=False,
    )


class CheckSkillsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name
        os.makedirs(os.path.join(self.root, ".agents", "skills"))
        os.makedirs(os.path.join(self.root, ".claude", "skills"))
        self.write(".agents/skills/README.md", "# Skills\n")
        self.write(".claude/skills/.gitkeep", "")
        self.write("AGENTS.md", "# Agent entry point\n")

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def add_skill(self, name, skill_file=True, link="default", index=True):
        os.makedirs(os.path.join(self.root, ".agents", "skills", name))
        if skill_file:
            self.write(
                ".agents/skills/%s/SKILL.md" % name,
                "---\nname: %s\ndescription: A test skill.\n---\n" % name,
            )
        if link == "default":
            link = "../../.agents/skills/%s" % name
        if link is not None:
            os.symlink(link, os.path.join(self.root, ".claude", "skills", name))
        if index:
            with open(
                os.path.join(self.root, "AGENTS.md"), "a", encoding="utf-8"
            ) as handle:
                handle.write(
                    "- `%s`: [`.agents/skills/%s/SKILL.md`](.agents/skills/%s/SKILL.md)\n"
                    % (name, name, name)
                )

    def check(self, expected_lines, expected_status):
        result = run(self.root)
        self.assertEqual(result.stdout.splitlines(), expected_lines)
        self.assertEqual(result.returncode, expected_status)

    def test_no_skills_passes(self):
        self.check(["skills checked: 0"], 0)

    def test_linked_and_indexed_skills_pass(self):
        self.add_skill("alpha")
        self.add_skill("beta")
        self.check(["skills checked: 2"], 0)

    def test_missing_link_fails(self):
        self.add_skill("alpha", link=None)
        self.check(["alpha: .claude/skills/alpha is missing"], 1)

    def test_copied_directory_is_not_a_link(self):
        self.add_skill("alpha", link=None)
        os.makedirs(os.path.join(self.root, ".claude", "skills", "alpha"))
        self.check(["alpha: .claude/skills/alpha is not a symbolic link"], 1)

    def test_text_file_is_not_a_link(self):
        self.add_skill("alpha", link=None)
        self.write(".claude/skills/alpha", "../../.agents/skills/alpha")
        self.check(["alpha: .claude/skills/alpha is not a symbolic link"], 1)

    def test_wrong_target_fails(self):
        self.add_skill("alpha", link="../../.agents/skills/beta")
        self.check(
            [
                "alpha: .claude/skills/alpha points to ../../.agents/skills/beta,"
                " expected ../../.agents/skills/alpha"
            ],
            1,
        )

    def test_absolute_target_fails(self):
        target = os.path.join(self.root, ".agents", "skills", "alpha")
        self.add_skill("alpha", link=target)
        self.check(
            [
                "alpha: .claude/skills/alpha points to %s,"
                " expected ../../.agents/skills/alpha" % target
            ],
            1,
        )

    def test_link_without_skill_fails(self):
        os.symlink(
            "../../.agents/skills/ghost",
            os.path.join(self.root, ".claude", "skills", "ghost"),
        )
        self.check(
            ["ghost: .claude/skills/ghost has no skill at .agents/skills/ghost"], 1
        )

    def test_missing_skill_file_fails(self):
        self.add_skill("alpha", skill_file=False)
        self.check(["alpha: .agents/skills/alpha/SKILL.md is missing"], 1)

    def test_missing_index_line_fails(self):
        self.add_skill("alpha", index=False)
        self.check(
            ["alpha: AGENTS.md does not name .agents/skills/alpha/SKILL.md"], 1
        )

    def test_similar_skill_name_is_not_an_index_line(self):
        self.add_skill("alpha", index=False)
        self.add_skill("alpha-two")
        self.check(
            ["alpha: AGENTS.md does not name .agents/skills/alpha/SKILL.md"], 1
        )

    def test_every_problem_is_reported_in_name_order(self):
        self.add_skill("beta", link=None, index=False)
        self.add_skill("alpha", skill_file=False)
        os.symlink(
            "../../.agents/skills/ghost",
            os.path.join(self.root, ".claude", "skills", "ghost"),
        )
        self.check(
            [
                "alpha: .agents/skills/alpha/SKILL.md is missing",
                "beta: .claude/skills/beta is missing",
                "beta: AGENTS.md does not name .agents/skills/beta/SKILL.md",
                "ghost: .claude/skills/ghost has no skill at .agents/skills/ghost",
            ],
            1,
        )

    def test_missing_skills_home_fails(self):
        os.remove(os.path.join(self.root, ".agents", "skills", "README.md"))
        os.rmdir(os.path.join(self.root, ".agents", "skills"))
        self.check([".agents/skills is missing"], 1)

    def test_missing_agents_file_fails(self):
        self.add_skill("alpha")
        os.remove(os.path.join(self.root, "AGENTS.md"))
        self.check(
            ["alpha: AGENTS.md does not name .agents/skills/alpha/SKILL.md"], 1
        )

    def test_extra_argument_is_a_usage_error(self):
        result = run(self.root, self.root)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr.splitlines(), ["usage: check-skills.py [repository-root]"]
        )

    def test_no_links_home_passes_without_skills(self):
        os.remove(os.path.join(self.root, ".claude", "skills", ".gitkeep"))
        os.rmdir(os.path.join(self.root, ".claude", "skills"))
        self.check(["skills checked: 0"], 0)

    def test_this_repository_passes(self):
        result = run()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertRegex(result.stdout, r"\Askills checked: [0-9]+\n\Z")


if __name__ == "__main__":
    unittest.main()
````

#### File: `tests/test_secret_scan.py`

````python
"""Tests for scripts/secret-scan.sh, observed through its exit status and output.

A stub stands in for gitleaks, so no test downloads anything or scans for real
secrets. The real scan is exercised in CI and by the planted-secret observation.
"""

import os
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "secret-scan.sh")

STUB = """#!/usr/bin/env bash
if [ "$1" = "version" ]; then
  echo "$STUB_VERSION"
  exit 0
fi
printf '%s\\n' "$@" > "$STUB_ARGS"
exit "$STUB_STATUS"
"""


class SecretScanTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name
        self.stub = os.path.join(self.tmp, "gitleaks-stub")
        with open(self.stub, "w", encoding="utf-8") as handle:
            handle.write(STUB)
        os.chmod(self.stub, 0o755)
        self.args_file = os.path.join(self.tmp, "args.txt")
        self.target = os.path.join(self.tmp, "target")
        os.makedirs(self.target)
        subprocess.run(["git", "init", "-q", self.target], check=True)

    def scan(self, *args, status="0", version="8.30.1", stub=None):
        env = dict(os.environ)
        env["GITLEAKS_BIN"] = self.stub if stub is None else stub
        env["STUB_ARGS"] = self.args_file
        env["STUB_STATUS"] = status
        env["STUB_VERSION"] = version
        return subprocess.run(
            ["bash", SCRIPT, *args], capture_output=True, text=True, env=env, check=False
        )

    def stub_args(self):
        with open(self.args_file, encoding="utf-8") as handle:
            return handle.read().splitlines()

    def test_clean_scan_exits_zero(self):
        result = self.scan(self.target, status="0")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_leak_exits_one(self):
        result = self.scan(self.target, status="1")
        self.assertEqual(result.returncode, 1, result.stderr)

    def test_scanner_error_exits_two(self):
        result = self.scan(self.target, status="126")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            result.stderr.splitlines()[-1],
            "secret-scan: gitleaks exited with status 126",
        )

    def test_scans_every_ref_with_redaction(self):
        self.scan(self.target)
        self.assertEqual(
            self.stub_args(),
            ["git", "--log-opts=--all", "--redact", "--no-banner", "--verbose", self.target],
        )

    def test_default_target_is_this_repository(self):
        self.scan()
        self.assertEqual(self.stub_args()[-1], REPO)

    def test_directory_that_is_not_a_repository_exits_two(self):
        outside = os.path.join(self.tmp, "plain")
        os.makedirs(outside)
        result = self.scan(outside)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            result.stderr.splitlines(),
            ["secret-scan: %s is not a git repository" % outside],
        )
        self.assertFalse(os.path.exists(self.args_file))

    def test_extra_argument_exits_two(self):
        result = self.scan(self.target, self.target)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            result.stderr.splitlines(),
            ["secret-scan: usage: scripts/secret-scan.sh [repository-directory]"],
        )

    def test_wrong_version_exits_two(self):
        result = self.scan(self.target, version="8.0.0")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            result.stderr.splitlines(),
            ["secret-scan: %s is gitleaks 8.0.0, expected 8.30.1" % self.stub],
        )
        self.assertFalse(os.path.exists(self.args_file))

    def test_missing_binary_exits_two(self):
        missing = os.path.join(self.tmp, "no-such-gitleaks")
        result = self.scan(self.target, stub=missing)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            result.stderr.splitlines(),
            ["secret-scan: %s is not an executable gitleaks" % missing],
        )


if __name__ == "__main__":
    unittest.main()
````

#### File: `scripts/check-skills.py`

````python
#!/usr/bin/env python3
"""Check that every skill is linked for Claude Code and named in AGENTS.md.

Usage: python3 scripts/check-skills.py [repository-root]

A skill is a directory under .agents/skills/. Each one needs a SKILL.md, a
symbolic link .claude/skills/<name> -> ../../.agents/skills/<name>, and its
path .agents/skills/<name>/SKILL.md written in AGENTS.md. Prints one line per
problem and exits 1, or prints "skills checked: <N>" and exits 0.
"""

import os
import sys


def main(argv):
    if len(argv) > 2:
        print("usage: check-skills.py [repository-root]", file=sys.stderr)
        return 2
    if len(argv) == 2:
        root = argv[1]
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    skills_dir = os.path.join(root, ".agents", "skills")
    links_dir = os.path.join(root, ".claude", "skills")
    if not os.path.isdir(skills_dir):
        print(".agents/skills is missing")
        return 1

    skills = sorted(
        name
        for name in os.listdir(skills_dir)
        if not name.startswith(".")
        and os.path.isdir(os.path.join(skills_dir, name))
    )
    links = []
    if os.path.isdir(links_dir):
        links = sorted(
            name for name in os.listdir(links_dir) if not name.startswith(".")
        )
    try:
        with open(os.path.join(root, "AGENTS.md"), encoding="utf-8") as handle:
            index = handle.read()
    except FileNotFoundError:
        index = ""

    problems = []
    for name in skills:
        skill_path = ".agents/skills/%s/SKILL.md" % name
        link_path = ".claude/skills/%s" % name
        expected = "../../.agents/skills/%s" % name
        link = os.path.join(links_dir, name)
        if not os.path.isfile(os.path.join(skills_dir, name, "SKILL.md")):
            problems.append((name, "%s is missing" % skill_path))
        if os.path.islink(link):
            target = os.readlink(link)
            if target != expected:
                problems.append(
                    (name, "%s points to %s, expected %s" % (link_path, target, expected))
                )
        elif os.path.lexists(link):
            problems.append((name, "%s is not a symbolic link" % link_path))
        else:
            problems.append((name, "%s is missing" % link_path))
        if skill_path not in index:
            problems.append((name, "AGENTS.md does not name %s" % skill_path))
    for name in links:
        if name not in skills:
            problems.append(
                (name, ".claude/skills/%s has no skill at .agents/skills/%s" % (name, name))
            )

    if problems:
        for name, text in sorted(problems, key=lambda problem: problem[0]):
            print("%s: %s" % (name, text))
        return 1
    print("skills checked: %d" % len(skills))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
````

#### File: `.agents/skills/README.md`

````markdown
# Skills

Each skill is one folder here, `.agents/skills/<name>/`, holding a `SKILL.md` in the Agent Skills format. Codex, Cursor, Gemini CLI, and Pi find skills in this folder on their own. Claude Code looks in `.claude/skills/`, so every skill also has a symbolic link there.

## Adding a skill

1. Create `.agents/skills/<name>/SKILL.md`. Use a lowercase, hyphenated name that matches the folder. Keep the front matter to `name` and `description`, plus the optional `license`, `compatibility`, and `metadata`.
2. Link it for Claude Code, from the repository root:

   ```bash
   ln -s ../../.agents/skills/<name> .claude/skills/<name>
   ```

3. Add one line for it under "Skills" in [`AGENTS.md`](../../AGENTS.md), so an agent that discovers nothing can still find it. The line gives the path and says when to use the skill:

   ```markdown
   - `<name>`: [`.agents/skills/<name>/SKILL.md`](.agents/skills/<name>/SKILL.md). <When to use it.>
   ```
4. Run the check, which CI also runs:

   ```bash
   python3 scripts/check-skills.py
   ```

The check fails when a skill has no `SKILL.md`, no link, a link that is not a symbolic link to `../../.agents/skills/<name>`, or no line in `AGENTS.md`, and when a link has no skill behind it.

## Windows

Git on Windows checks symbolic links out as small text files unless `core.symlinks` is enabled. If the check reports "is not a symbolic link" on a fresh clone, run `git config core.symlinks true` and check the files out again, or read the skills from `.agents/skills/` directly.
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

## Before you publish a fork

If your fork is public, these files are public too, along with their history. You do not have to name anyone or give a medical detail: "two adults and a small child" and `higher_risk_diners: yes` tell an agent all it needs.
````

#### File: `kitchen/profile.md`

````markdown
---
filled_in: no
updated: none
units: none
higher_risk_diners: unknown
---

# Kitchen profile

Fill in each section, then set the fields above:

- `filled_in`: `yes` once this file describes your kitchen.
- `updated`: the date you last changed it, as `YYYY-MM-DD`.
- `units`: `us` (cups, ounces, °F), `metric` (grams, millilitres, °C), or `both`.
- `higher_risk_diners`: `yes` if you ever cook for someone at higher risk from foodborne illness, such as a young child, an older adult, or someone with a weakened immune system; `no` if you do not; `unknown` until you have answered. `yes` turns on the stricter food-safety endpoints.

## Who you cook for

_How many people, and roughly who: adults, children, guests. Names are not needed._

## Priorities

_What matters most, in order. For example: weeknight speed, leftovers that reheat well, more protein, learning why a technique works._

## Constraints

_Allergies, intolerances, diets, and firm dislikes. Write "none known" if there are none. Agents never guess these._

## Higher-risk diners

_Optional detail behind the `higher_risk_diners` field, such as "until March" or "only when my parents visit". The field alone is enough._

## Skill and time

_How comfortable you are at the stove, and how long a normal weeknight cook can take._

## Standing corrections

Rules you have already settled, which win over any saved recipe card. One per line, each tied to the dish it came from.

- _Example: the weeknight chili has no beans; do not add them._
````

#### File: `kitchen/equipment.md`

````markdown
---
filled_in: no
updated: none
---

# Equipment

List what you cook with. The status column is the important one:

- **verified**: you checked the item and its manual yourself.
- **assumed**: mentioned in passing or guessed. Agents confirm it with you before relying on it.

Put limits from the manual in the limits column, such as a pressure cooker's minimum liquid and maximum fill line, or an oven's highest temperature. Agents never invent a limit. When a recipe depends on one that is not written here, they ask.

| Item | Status | Limits from the manual | Notes |
|---|---|---|---|
| _Example: 6-quart electric pressure cooker_ | assumed | _minimum liquid, maximum fill_ | _model, quirks_ |
| _Example: oven_ | verified | _highest temperature_ | _runs hot or cool, convection_ |
| _Example: instant-read thermometer_ | verified | | |

## Not owned

_Tools you do not have and do not want recipes to depend on, such as a stand mixer or a grill._
````

#### File: `kitchen/pantry.md`

````markdown
---
filled_in: no
snapshot_date: none
---

# Pantry snapshot

A dated record of what you usually have, not a live inventory. Set `snapshot_date` above, as `YYYY-MM-DD`, each time you update it. Agents confirm an ingredient is on hand before building a recipe around it, and they do not reach for a specialty ingredient just because it is listed here.

| Group | Usually on hand |
|---|---|
| Grains, pasta, bread | _rice, flour, tortillas_ |
| Fresh aromatics | _garlic, ginger, onions_ |
| Oils and fats | _olive oil, butter_ |
| Acids and condiments | _vinegars, soy sauce, mustard_ |
| Sweeteners | _sugar, honey_ |
| Canned and jarred | _tomatoes, coconut milk, stock_ |
| Spices and dried herbs | _the ones you actually use_ |
| Dairy and eggs | _milk, yogurt, eggs_ |
| Freezer | _what is usually in it_ |
| Specialty | _anything unusual you like to cook with_ |
````

#### File: `AGENTS.md`

````markdown
# Agent entry point: Chef Council

This repository is a system for cooking with AI agents: a council of cooking lenses that develops and pressure-tests recipes, plain-text recipe cards and cook logs, and an independent editor check on every recipe change. Read this file first, then the files it points to. It applies to every agent, whichever harness runs it.

The person you are working with is called the cook here. If you cannot read or write files in this repository (a chat app, for example), say so once, and when asked to save something return the complete file and its path for the cook to save.

## Read in this order

1. [`kitchen/README.md`](kitchen/README.md), then [`kitchen/profile.md`](kitchen/profile.md), [`kitchen/equipment.md`](kitchen/equipment.md), and [`kitchen/pantry.md`](kitchen/pantry.md): who is being cooked for, their constraints and standing corrections, the equipment, and a dated pantry snapshot. A file whose front matter says `filled_in: no` is still a blank template: ask the cook, and never treat a placeholder as a fact.
2. The skill for the job, from [Skills](#skills) below. Read its `SKILL.md` in full before acting on it.
3. The saved recipe card, and its most recent cook log, before changing that recipe or cooking from it.

## Rules that are easy to get wrong

- **The latest correction beats a saved card.** When the cook's most recent explicit instruction disagrees with a saved card, name the conflict, follow the correction, and update the card. The standing corrections in `kitchen/profile.md` beat a card in the same way.
- **Status is several separate facts:** how far the recipe has been developed, whether it has been cooked and how that went, whether the card is saved in the repository, and whether any copy outside the repository is up to date. Writing a card does not make it cooked, and cooking it once does not make it a house recipe. Never raise any of these without a logged cook or the cook saying so.
- **Never report a save, sync, or check that did not happen.** Say "saved" only after the file is written, "synced" only after reading the other copy back, and "checked" only when the check ran and you read its result. When a step failed or was skipped, say which one and why.
- **Do not invent** quantities, times, temperatures, cook outcomes, allergies, equipment limits, or sources. When a number is missing, say so on the card.
- **Keep the old version when testing a new one.** A small edit is a version bump on the same card. A changed technique or a variant is its own card, and the original stays.
- **The council is a set of lenses, not people.** Attribute advice to a lens, written `<Name>-style lens`. No real chef has reviewed, approved, endorsed, or contributed to anything here, so never say or imply one did, and never invent a quote.
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
  - `python3 -m unittest discover -s tests -v`: the tests for the scripts.
  - `scripts/secret-scan.sh`: gitleaks over the full history.
- Never commit a secret, a credential, or a token. Source packets, the exact text a cook approved, stay in the git-ignored `.sources/` folder.
- Everything committed to a public fork is public, including `kitchen/` and the history. Keep out anything the cook would not publish.
````

#### File: `CLAUDE.md`

````markdown
@AGENTS.md
````

#### File: `GEMINI.md`

````markdown
@./AGENTS.md
````

#### File: `LICENSE`

````text
MIT License

Copyright (c) 2026 Charles Samuel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

#### File: `.gitignore`

````text
# Source packets: the verbatim text a cook approved, kept for the editor check.
# They can hold private conversation text, so they are never committed.
.sources/

# Local agent settings and overrides
.claude/settings.local.json
CLAUDE.local.md
AGENTS.override.md

# Secrets
.env
.env.*

# Python
__pycache__/
*.pyc

# Operating system and editor files
.DS_Store
Thumbs.db
*.swp
````

#### File: `scripts/secret-scan.sh`

````bash
#!/usr/bin/env bash
# Scan the full git history of a repository for secrets with a pinned gitleaks.
#
# Usage: scripts/secret-scan.sh [repository-directory]   (default: this repository)
#
# Exit status: 0 no leaks, 1 leaks found, 2 the scan could not run.
# Set GITLEAKS_BIN to use a gitleaks of the pinned version that you installed
# yourself. Otherwise the pinned release is downloaded once, checked against
# its SHA-256, and kept in GITLEAKS_CACHE (default: the runner's temporary
# directory in CI, else ~/.cache/chef-council). Only Linux x86_64 is pinned.
set -euo pipefail

GITLEAKS_VERSION=8.30.1
GITLEAKS_SHA256_LINUX_X64=551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb

fail() {
  echo "secret-scan: $1" >&2
  exit 2
}

[ "$#" -le 1 ] || fail "usage: scripts/secret-scan.sh [repository-directory]"
repo=${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 || fail "$repo is not a git repository"

bin=${GITLEAKS_BIN:-}
if [ -z "$bin" ]; then
  cache=${GITLEAKS_CACHE:-${RUNNER_TEMP:-${XDG_CACHE_HOME:-$HOME/.cache}/chef-council}/gitleaks-$GITLEAKS_VERSION}
  bin=$cache/gitleaks
  if [ ! -x "$bin" ]; then
    [ "$(uname -s)-$(uname -m)" = "Linux-x86_64" ] ||
      fail "only Linux x86_64 is pinned; install gitleaks $GITLEAKS_VERSION and set GITLEAKS_BIN"
    archive=gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz
    mkdir -p "$cache"
    work=$(mktemp -d "$cache/download.XXXXXX")
    trap 'rm -rf "$work"' EXIT
    curl -sSfL --retry 3 -o "$work/$archive" \
      "https://github.com/gitleaks/gitleaks/releases/download/v$GITLEAKS_VERSION/$archive" ||
      fail "could not download $archive"
    echo "$GITLEAKS_SHA256_LINUX_X64  $work/$archive" | sha256sum -c - >/dev/null ||
      fail "$archive does not match its pinned SHA-256"
    tar -xzf "$work/$archive" -C "$work" gitleaks || fail "could not unpack $archive"
    mv "$work/gitleaks" "$bin"
  fi
fi
[ -x "$bin" ] || fail "$bin is not an executable gitleaks"
version=$("$bin" version 2>/dev/null) || fail "$bin did not report a version"
[ "$version" = "$GITLEAKS_VERSION" ] ||
  fail "$bin is gitleaks $version, expected $GITLEAKS_VERSION"

status=0
"$bin" git --log-opts=--all --redact --no-banner --verbose "$repo" || status=$?
case "$status" in
  0 | 1) exit "$status" ;;
  *) fail "gitleaks exited with status $status" ;;
esac
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
    name: skill links and tests
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - name: Check out
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - name: Check every skill has its link and its AGENTS.md line
        run: python3 scripts/check-skills.py
      - name: Run the tests
        run: python3 -m unittest discover -s tests -v
````

#### Insert: `.agents/spec-profile.md`

The eight lines Task 5 inserts, each indented exactly as shown:

````markdown
  - The CI checks' local commands, run from the repository root:
    `python3 scripts/check-skills.py` (prints `skills checked: <N>` and exits
    0), `python3 -m unittest discover -s tests -v` (its last line is `OK`), and
    `scripts/secret-scan.sh` (gitleaks over the full local history: exit 0
    with `no leaks found`, exit 1 on a leak, and exit 2 when the scan could
    not run, which never counts as clean). The scan downloads the pinned
    gitleaks release on Linux x86_64 on first use; elsewhere, set
    `GITLEAKS_BIN` to an installed gitleaks.
````

## Repo profile

`.agents/spec-profile.md` applies as written, with these notes:

- **Tests task.** Every task is `mechanical`, so neither the profile nor the
  spec-writing skill requires a tests task; this spec opens with one anyway
  because it adds two scripts, and Task 2 carries the tests-pass and
  tests-unchanged gates.
- **Deterministic checks.** After Task 5 the profile's list includes this
  spec's three local commands; leg 2 and leg 3 run them with the sweeps.
- **Real artifact and observation.** Definition-of-done items 1 to 5 are the
  observation: the fresh clone, the CI checks, the planted secret, and the
  rendered Markdown. No skill exists yet, so the profile's skills observation
  reduces to `skills checked: 0`.
- **Private sources.** No task reads a private source: the generalization is
  already done in `## File contents`. The cross-examination dossier held this
  spec, the profile, and `README.md` only.

## Cross-examination

Blind review on 2026-11-18 by `muse-wonder-full-1.0` (provider `meta`,
architect tier, reasoning effort high, Muse Code 1.4.15 (1.4.15-R8339.1)),
through the sandboxed read-only route, on a dossier holding the draft spec,
the profile, and `README.md`. 16 findings, 15 accepted (two in part), 1
rejected. After the edits, leg 1 re-measured the red and re-ran every task
gate from this spec's text in a fresh scratch clone at `base_sha`.

1. **Missing commit, push, and pull request choreography.** ACCEPT, by
   citation: `## Prerequisites` now says these steps and the `Spec-Task`
   trailer are the `2-spec-execute` skill's standing procedure and the
   profile's ship tail, and that a task's commit holds exactly its Touches.
   The spec does not restate another leg's procedure.
2. **The tests-unchanged gate could pass with no Task 1 commit.** ACCEPT:
   the Task 2 gate captures the commit, requires it to be non-empty and an
   ancestor of `HEAD`, and prints `tests unchanged` only then.
3. **The shell script had no committed test.** ACCEPT: added
   `tests/test_secret_scan.py` (nine tests through a stub gitleaks), moved
   `scripts/secret-scan.sh` into Task 2 so one task turns every test green,
   and re-measured the red (`FAILED (failures=24, errors=2)`).
4. **A cached or supplied gitleaks was trusted unchecked.** ACCEPT in part:
   the script now downloads into a private directory and moves the binary
   into place, checks the reported version of the cached or supplied binary
   before every scan, and keeps its default cache under `~/.cache` instead
   of a shared temporary directory. REJECT the per-run hash stamp of the
   cached binary: the cache is the user's own directory and CI starts
   empty, as decision 12 records.
5. **No base-drift or mergeability gate.** REJECT: base drift is leg 2's
   standing check and mergeability is enforced when the pull request is
   merged; the pipeline works one ticket at a time in a repository with one
   maintainer, so `main` moves only through this pipeline. The citation
   added for finding 1 names where the drift check lives.
6. **The sweep item was not reproducible.** ACCEPT: item 7 now fixes the
   state (committed, pushed, clean tree, after a fetch), the `BASE_SHA`
   value, and the privacy result as exit 0 with a last line beginning
   `privacy sweep: clean`. The lint's path stays "as the profile says"
   because the profile owns it.
7. **The rendered-Markdown item was subjective.** ACCEPT: item 5 is now a
   per-file checklist that separates italic placeholders from code-span
   ones and says what the front matter must show.
8. **The check's error contract was incomplete.** ACCEPT in part: decision
   10 now lists every literal line, the order, the usage error, the
   missing-home line, and the missing link directory; two tests were added
   (the usage error and no link directory). REJECT handling an unreadable
   `AGENTS.md`: decision 10 records that it is not handled and still fails.
9. **Gate helpers depended on unstated shell state.** ACCEPT: both helpers
   now precede the build plan, whose introduction says to define `OUT` and
   the helpers in the task's shell first.
10. **The SHA-256 gates were not literal commands.** ACCEPT: each is now a
    complete `sha256sum -c -` command with a here-document.
11. **Platform and tools were under-specified.** ACCEPT: `## Prerequisites`
    pins the executor to Linux x86_64 and names the tools; decision 11 says
    the tests are for Linux and macOS.
12. **The planted token could come out short.** ACCEPT: it is now cut from
    an unbounded random stream and its length is checked.
13. **Grep gates misstated output or status.** ACCEPT: the gates state the
    exact lines with file names and print the expected non-zero status.
14. **The link check overclaimed.** ACCEPT: its description is narrowed to
    the inline form these files use, and it now requires `git ls-files --`
    to list exactly the target.
15. **"Notes-app rules dropped" read as contradicting `AGENTS.md`.** ACCEPT:
    decision 2 now says the app-specific rules are dropped and the generic
    mirror rules are kept, and why.
16. **"Every file byte for byte" had two unnamed exceptions.** ACCEPT: the
    goal and the `extract` helper's text name `.claude/skills/.gitkeep` and
    the profile insert.
