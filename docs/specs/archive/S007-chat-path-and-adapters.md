---
date: 2026-11-19
id: S007
wayfinder: docs/wayfinder/W001-public-chef-council/issues/T013-chat-path-and-adapters.md
target_release: none
status: shipped
base_branch: main
base_sha: 8b3e43e8ea034efa3378216c70f6b55a89dd4ceb
work_branch: workstream/t013-chat-path-and-adapters
pr_base: main
prior_specs:
  - docs/specs/archive/S001-scaffold.md
  - docs/specs/archive/S002-council-roster-and-vetting.md
  - docs/specs/archive/S003-chef-council-skill.md
  - docs/specs/archive/S004-codify-and-cook-log.md
  - docs/specs/archive/S005-editor-gate.md
  - docs/specs/archive/S006-example-recipes.md
references:
  - docs/wayfinder/W001-public-chef-council/MAP.md
  - docs/wayfinder/W001-public-chef-council/issues/T005-privacy-rules.md
  - docs/wayfinder/W001-public-chef-council/issues/T006-private-repository-names.md
  - docs/learnings/L001-scaffold.md
  - docs/learnings/L002-council-roster-and-vetting.md
  - docs/learnings/L003-chef-council-skill.md
  - docs/learnings/L004-codify-and-cook-log.md
  - docs/learnings/L005-editor-gate.md
  - docs/learnings/L006-example-recipes.md
  - .agents/spec-profile.md
cross_examined: meta/muse-wonder-full-1.0 (architect), 21 findings, 21 accepted
approved_by: autonomous
approved_at: 2026-11-19T06:08Z
pr: 30
kickbacks: 0
merged: 2026-11-19
harvested: 2026-11-19 (3 learnings)
---

# Chat path and adapters: paste-in instructions, a generated chat bundle with a CI check, setup notes, and the sync contract

## Goal and definition of done

Ship ticket T013. A cook whose assistant is a chat app with no file access
gets the same system as a cook with a coding agent: one paste-in
instructions file under 8,000 characters, one generated knowledge file
(`chat/bundle.md`) that CI keeps current, and setup notes for four chat
apps that only say where to paste. A cook who keeps copies of cards in a
notes app gets a written sync contract, an empty sync map, and one worked
example that holds no ID, link, or collection name.

Every file this spec adds or changes is given byte for byte under `## File
contents`, except `chat/bundle.md`, which the script generates and whose
hash is pinned, and `.agents/spec-profile.md`, which Task 3 changes by one
exact replacement. Leg 1 wrote the files, built them in a scratch clone at
`base_sha`, ran a mutation probe of the script, and rehearsed the chat run
(`## Build plan — agent loop`). The executor writes the files from this
spec and does not reword one.

Done means all of the following, each observed on the work branch's head
commit after Task 3, from the repository root, with the setup file of `##
Build plan — agent loop` sourced:

1. **The files.** `git diff --name-only "$BASE_SHA"...HEAD -- . ':!docs/'
   | LC_ALL=C sort` prints exactly these fourteen lines:

   ```text
   .agents/spec-profile.md
   .gitattributes
   .github/workflows/ci.yml
   AGENTS.md
   adapters/README.md
   adapters/mem.md
   adapters/sync-map.md
   chat/README.md
   chat/bundle.md
   chat/project-instructions.md
   scripts/build-chat-bundle.sh
   tests/test_build_chat_bundle.py
   tests/test_chat_instructions.py
   tests/test_line_endings.py
   ```

2. **The bytes.** This prints fourteen lines, each a path followed by `:
   OK`:

   ```bash
   sha256sum -c - <<'SUMS'
   8d9a5e9587401cd523be5df6e19ad9a8c7f0a814c71bf9ae6f945c15714cffad  .agents/spec-profile.md
   8359e7ee50f6fbb373e464f1b57ae6d78917bba0a9b8e7aaa65888b80c586905  .gitattributes
   33a5c25a161906fceb4313b38ec75875f8613ecba0abc6aebe592869da394b15  .github/workflows/ci.yml
   9b04e18c43d5f69b0fd2dafc35851d7f42fc962616f2d656c768fe11a762d1e0  AGENTS.md
   82e3d6e05b6c1dabca26bfee368dd94fd4456ddccf086d0625d99f5a6af24b1c  adapters/README.md
   849bb250b5eadef3393eaf3425b325e4c040a86c59d471a3793759feec48b7fe  adapters/mem.md
   6e5e6f3684d8291db7f11164616184043b4b4f70255e2b796df01a9f640c390c  adapters/sync-map.md
   365e26109e6639a2c81406721ac0dac2923a5721a4ac7135c0afd13118b1af93  chat/README.md
   230861b9a3ef2333edad693ea5bd8114df865aade79271512d0731a12bbc6355  chat/bundle.md
   043cadfed60a9dc8998bd008d44c7f4aa9bfeefaffb593a592b8627163832ecc  chat/project-instructions.md
   b5c68621e794123ae173543074bc058332eefb0229c48bad3026108a74f10f48  scripts/build-chat-bundle.sh
   98b88d9f14819e6f529dfa95cf639e8c3f88674b08431e60252e3e9ef7ccbbeb  tests/test_build_chat_bundle.py
   58aabb3fc7a5b429a485fe0515842298685c0dc700b4bcfdf9e607b0282cda0e  tests/test_chat_instructions.py
   056fc75ccf55af4d5f970db6c24d0e1533ef0e4bc862abfaffb3c24f83de2d23  tests/test_line_endings.py
   SUMS
   ```

   `git ls-files -s scripts/build-chat-bundle.sh` prints a line that begins
   `100755 `.
3. **The instructions are under the limit.** `python3 -c
   "print(len(open('chat/project-instructions.md', encoding='utf-8').read()))"`
   prints `6779`, which is below 8000 (decision 2).
4. **The bundle regenerates byte for byte.** `scripts/build-chat-bundle.sh
   --check; echo $?` prints `chat bundle checked: 33 files` then `0`. Then
   `scripts/build-chat-bundle.sh; echo $?` prints `chat bundle written: 33
   files` then `0`, and `git status --porcelain --untracked-files=all`
   still prints nothing: the regenerated file is the committed one.
5. **A stale bundle fails the check.** In a fresh clone of the pushed
   branch in a new temporary directory, whose `git rev-parse HEAD` equals
   the pull request's head commit: `scripts/build-chat-bundle.sh --check;
   echo $?` prints `chat bundle checked: 33 files` then `0`; then, after
   `printf 'one more line\n' >> kitchen/pantry.md`,
   `scripts/build-chat-bundle.sh --check; echo $?` prints `chat bundle is
   out of date: run scripts/build-chat-bundle.sh` then `1`. The clone is
   then deleted; nothing in it is committed.
6. **No adapter file holds a link or an ID.** `idcheck adapters/README.md
   adapters/mem.md adapters/sync-map.md; echo $?` prints `0` and nothing
   else, and `"$SWEEP" --text adapters/README.md adapters/mem.md
   adapters/sync-map.md` ends with a line beginning `privacy sweep: clean`
   and exits 0. The sweep's private denylist is what covers the names of
   a real account's collections (decision 14).
7. **The setup notes add nothing to the instructions.** `grep -c '^```'
   chat/README.md` prints `0`: the notes hold no block of text to paste,
   so the only text a cook pastes is `chat/project-instructions.md`
   (decision 3). `grep -c -E '^\| (Claude Projects|ChatGPT Projects|Gemini
   Gems|Muse) \|' chat/README.md` prints `4`.
8. **The links.** `linkcheck AGENTS.md chat/README.md
   chat/project-instructions.md adapters/README.md adapters/mem.md
   adapters/sync-map.md; echo $?` prints `0` and nothing else. `grep -c
   '^### The editor prompt for a new chat$' method/recipe-qc.md` prints
   `1`, the heading the one anchored link in `chat/README.md` points to.
9. **The chat run.** Task 2's chat run passed: `chatcheck "$REPLY"; echo
   $?` printed `chat ok` then `0` on the reply of a fresh subagent that was
   given only the instructions and the bundle (`### The chat run`). That
   shows the properties `### Gate helpers` lists for `chatcheck`, on one
   reply, and nothing wider. The pull request's Evidence section holds
   that reply as saved.
10. **The repository's checks.** `python3 scripts/check-skills.py; echo $?`
    prints `skills checked: 4` then `0`. `python3 scripts/check-council.py;
    echo $?` prints `council checked: 14 seated, 14 records` then `0`.
    `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
    prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
    prints `269`. `python3 scripts/lint-cards.py; echo $?` prints `cards
    checked: 2` then `0`. After `git fetch origin`, `scripts/check-qc.sh;
    echo $?` prints `qc checked: 0` then `0`. `scripts/secret-scan.sh >
    "$OUT" 2>&1; echo $?` prints `0`, and `grep -c 'no leaks found' "$OUT"`
    prints `1` or more. `python3 "$WAYFINDER/scripts/lint.py"
    docs/wayfinder/*/MAP.md; echo $?` prints `0` and nothing else. `git
    diff --check; echo $?`, `git diff --cached --check; echo $?`, and `git
    diff --check "$BASE_SHA"...HEAD -- .; echo $?` each print `0` and
    nothing else. `wc -c < AGENTS.md` prints `8156`, which is below 8192
    (decision 15). After `git fetch origin`, `"$SWEEP" > "$OUT" 2>&1; echo
    $?` prints `0`, and `tail -1 "$OUT"` begins `privacy sweep: clean`. The
    profile's ship tail says when these run: before every push, and again
    before the pull request is reported ready.
11. **CI.** This one command, run after the ship tail has opened the pull
    request and its checks have finished (`gh pr checks <number> --watch`
    returns), prints a number that is `1` or more:

    ```bash
    PR=$(gh pr view workstream/t013-chat-path-and-adapters --json number --jq .number) && HEAD_SHA=$(gh pr view "$PR" --json headRefOid --jq .headRefOid) && RUN=$(gh run list --commit "$HEAD_SHA" --workflow CI --event pull_request --json databaseId --jq '.[0].databaseId') && JOB=$(gh run view "$RUN" --json jobs --jq '.jobs[] | select(.name=="tests") | .databaseId') && gh run view "$RUN" --job "$JOB" --log | grep -c 'chat bundle checked: 33 files'
    ```

    It finds the `CI` workflow's pull-request run on the head commit, then
    its `tests` job, and counts the line the new step prints. `gh pr checks
    "$PR"` then reports every check passed and lists three checks:
    `gitleaks (full history)`, `tests`, and `editor gate`.
12. **The rendered pages, looked at.** The orchestrator renders each of
    the five new Markdown pages from the pushed branch with the profile's
    command, `gh api
    "repos/{owner}/{repo}/contents/<path>?ref=workstream/t013-chat-path-and-adapters"
    -H 'Accept: application/vnd.github.html'`, and looks at the result.
    This item requires rendering and looking. The pull request states each
    of these seven observations as seen or not seen:
    - `chat/README.md`: the table of apps shows a header and four rows,
      and both links in its last column are links.
    - `chat/README.md`: the two numbered lists show as numbered lists.
    - `chat/project-instructions.md`: the three steps under Saving show as
      a numbered list, and the two marker lines show as code.
    - `adapters/README.md`: the six rules show as a numbered list from 1
      to 6, and the table of states shows a header and four rows.
    - `adapters/mem.md`: the table inside the worked example shows a
      header and one row.
    - `adapters/sync-map.md`: the table shows a header and no row.
    - In all five, no heading shows its `#` characters and no link shows
      its square brackets.
    An observation that is "not seen" is a finding for the pull request,
    not a silent pass. This spec predicts nothing else about how GitHub
    renders these files (L001).

## Decisions

1. **One spec, three tasks, and what is left to later tickets.** The
   ticket's five deliverables ship together: the instructions, the bundle
   script with its CI check, the setup notes, and the three adapter files.
   The root `README.md`, the behavior-checks page, and the pattern
   document are T014's. This spec adds one behavior check of its own, the
   chat run (decision 17), because the profile's real artifact names "the
   chat bundle a chat-app user pastes in" and nothing else would observe
   it.
2. **The instructions file is the paste-in, whole.**
   `chat/project-instructions.md` has no wrapper, no front matter, and no
   note to the cook: a cook pastes it from its first line to its last. The
   ticket's limit, under 8,000 characters, is counted as the number of
   Unicode characters in the whole file (`len` of the decoded text in
   Python), and a test holds every later edit to it
   (`tests/test_chat_instructions.py`). The file as given holds
   6779 characters, all of them ASCII, so its byte count is the
   same. The spec names no vendor's limit as the reason for 8,000: only
   the ticket's number is asserted, and the setup notes say "so that it
   fits an instructions field" and no more.
3. **Canonical, and nothing diverges from it.** The instructions file is
   the only text a cook pastes. `chat/README.md` says where to paste it in
   each app and holds no second copy, no extra instruction, and no fenced
   block (definition-of-done item 7). To change how a chat behaves, a cook
   edits the instructions file and pastes it again; the notes say so. The
   instructions restate the rules of `AGENTS.md` for a reader that cannot
   open files, in `AGENTS.md`'s own wording wherever the rule is the same,
   and change only what a chat changes: it reads the bundle in place of
   the repository, it returns files in place of saving them, it asks for
   cards and cook logs to be pasted, it gives a command in place of
   running one, and it makes no copy in a notes app (decision 13). One
   sentence differs on purpose: `AGENTS.md` calls a kitchen file blank when
   its front matter says `filled_in: no`, and the instructions give the
   `chef-council` skill's fuller test (decision 18). `AGENTS.md`'s sentence
   is the short form of that test and is not edited here. `AGENTS.md` stays the entry point for an agent that can
   read the repository; the instructions file is the entry point for one
   that cannot. A later spec that changes a rule in `AGENTS.md` changes
   the same rule in the instructions file in the same pull request.
4. **What the bundle holds.** Every regular file whose name ends in `.md`
   (lowercase) under four places, in this order: `kitchen/`, the skill
   folders `.agents/skills/<name>/` (their files at any depth), `method/`,
   and `templates/`. Inside each place the files come in the byte order of
   their full paths (`LC_ALL=C sort`). At `base_sha` that is 33 files and
   the bundle is 221,094 bytes.
   - `method/` is added to the ticket's three sources. The skills name
     `method/status-and-versions.md` as the full rule for versions, status,
     and names, and the instructions send a cook to
     `method/recipe-qc.md` for the editor prompt, so a bundle without the
     two pages would leave a chat unable to follow its own skills.
   - `.agents/skills/README.md` is left out: it tells a maintainer how to
     add a skill and link it, which a chat cannot do. That is why the
     skill folders are read from depth two.
   - The recipe cards, `recipes/INDEX.md`, and cook logs are left out. They
     change with every cook, and a bundle that held them would be stale
     after every save. The instructions tell the chat to ask for a card
     and its latest cook log, and the setup notes tell the cook to upload
     or paste them.
   - `AGENTS.md`, `chat/`, `adapters/`, `qc/`, `docs/`, and the scripts
     are left out. The instructions file stands in for `AGENTS.md`, and
     the rest is not something a chat reads to cook.
   - A symbolic link is never followed and never bundled, so a link cannot
     pull a file from outside the four places into a file that is
     uploaded to a third party.
5. **The bundle's format.** The header given in
   `scripts/build-chat-bundle.sh`, then a `## Files` list with one `- <path>`
   line per file, then each file: one blank line, the line `===== FILE:
   <path> =====`, the file's bytes unchanged, one line feed added only when
   a file that is not empty does not end with one, and the line `===== END
   FILE: <path> =====`. The files are not fenced, because they hold fences
   of their own. The bundle holds no date, commit, or host name, so the
   same files give the same bytes on every machine. A bundled file that
   holds a line starting `===== FILE: ` or `===== END FILE: ` would make
   the markers ambiguous, so the script refuses it and exits 2. A file
   name that holds a line break is refused the same way.
6. **The script's interface.** `scripts/build-chat-bundle.sh` takes no
   argument or the one option `--check`, and finds the repository from its
   own location, so it runs from any folder.
   - With no argument it writes `chat/bundle.md`, making `chat/` when it is
     missing, prints `chat bundle written: <N> files`, and exits 0.
   - With `--check` it writes nothing. It prints `chat bundle checked: <N>
     files` and exits 0 when the file is byte-identical to what it would
     write; it prints `chat bundle is missing: run
     scripts/build-chat-bundle.sh` or `chat bundle is out of date: run
     scripts/build-chat-bundle.sh` on standard output and exits 1
     otherwise.
   - It exits 2, with nothing on standard output and a last line on
     standard error that starts `build-chat-bundle: `, when it cannot run:
     any other argument, a missing place, no file to bundle, a marker line
     inside a bundled file, a file name with a line break, or a file it
     cannot list or read. For the first five that line is the only one.
     For a file it cannot list, read, or write, the tool that failed may
     print its own message first. Exit 2 never counts as current, the rule of
     `scripts/check-qc.sh` and `scripts/secret-scan.sh`.
   - It sets `LC_ALL=C` before it lists or matches a path (L005), and the
     tests bundle a file whose name holds a byte that is not valid UTF-8
     under a UTF-8 locale.
   - It is Bash, as the ticket names it. Beside the shell's own commands
     it runs `dirname`, `find`, `sort -z`, `grep`, `cat`, `tail`, `od`,
     `tr`, `cmp`, `cp`, `mkdir`, `mktemp`, and `rm`.
7. **CI and the lists of checks.** The `tests` job of
   `.github/workflows/ci.yml` gains one step, `scripts/build-chat-bundle.sh
   --check`, placed before the unit-test step.
   `tests/test_build_chat_bundle.py` also runs the check on the repository
   itself, so the unit tests fail on a stale bundle too. The separate step
   comes first because a failed step stops the job, and its one line names
   the fix where a unit-test failure would not. `AGENTS.md` lists the command under "Making changes",
   and the profile's list of CI commands gains it, as the profile requires
   of the spec that adds a check.
8. **What the check costs, said plainly.** From this spec on, a change to
   any `.md` file under the four places fails CI until
   `scripts/build-chat-bundle.sh` has been run and `chat/bundle.md`
   committed with it. That includes a cook filling in `kitchen/profile.md`
   on a fork. The ticket asks for exactly this ("with CI failing when the
   bundle is stale"), the failure line names the command, and `AGENTS.md`
   and `chat/README.md` both say it. Every later spec of this map whose
   touch set holds a file under `kitchen/`, `.agents/skills/<name>/`,
   `method/`, or `templates/` regenerates the bundle in the same task and
   pins the new hash. The pre-commit hook of `scripts/install-git-hooks.sh`
   is not changed.
9. **Line endings (L005).** L005 asks the spec that tells a cook to hash a
   card on the chat path to settle first which bytes are hashed on a
   checkout that converts line endings, and to test that case. This spec
   settles it with a new `.gitattributes` holding the one rule `* text=auto
   eol=lf`: git then checks every text file out with line feeds whatever
   `core.autocrlf` says, so the file `scripts/check-qc.sh --hash` reads,
   and the files the bundle script reads, are the committed bytes.
   `tests/test_line_endings.py` builds a repository with
   `core.autocrlf=true`, shows that without the rule a card is checked out
   with Windows line endings (the control), and that with the repository's
   own `.gitattributes` it is checked out with line feeds, `--hash` prints
   the hash of the committed bytes, and a card saved with Windows line
   endings is committed with line feeds. At `base_sha` no tracked file
   holds a carriage return (`git grep -Il $'\r'` prints nothing), and
   `git add --renormalize .` stages no tracked file, so the rule changes
   no committed byte.
   - One case stays open and is named here as accepted: a card that an
     editor program saved with Windows line endings has a working-file
     hash that differs from its committed hash until it is committed and
     checked out again. `--hash` still reads the working file. Closing
     that means changing `scripts/check-qc.sh`, which this spec does not
     touch; the gate fails closed on it, as L005 records. A chat user is
     the cook most likely to meet it, because the card arrives by paste, so
     `chat/README.md` tells the cook to save each file with line feeds and
     says why.
   - This spec does not edit `scripts/check-qc.sh`, `method/recipe-qc.md`,
     or the report format, so the rest of L005's list (the locale hole in
     the gate's own match) stays with the next spec that edits the gate.
10. **The editor check in a chat is stated once.** `method/recipe-qc.md`
    already holds "The editor prompt for a new chat": the prompt, the six
    things to paste, and what to save. `chat/README.md` links to that
    section and the instructions name it; neither repeats the prompt or
    summarizes the steps beside the reference (L004). They add only what
    that section does not say: that the editor is a new chat and never a
    later message in the writing chat; that a new chat in the same project
    works, because the instructions tell a chat that opens with the
    editor's message to be the editor and nothing else; and that the hash
    line needs a terminal and a copy of the repository, without which the
    report has no hash and the gate fails for that change.
11. **How a chat returns a file.** For each file, a line `File to save:
    <path>`, then the complete file inside a fence of four backticks; after
    the last file, any command the skill says to run next; and, as the
    reply's last line, exactly `Nothing was saved: I cannot write files
    here.` The four skills already say "return the complete file with its
    path, and say that nothing was saved"; the instructions fix the form so
    that a cook can see at a glance, and the chat run can check, that the
    reply is a file to save and not a claim that it was saved. The
    `recipe-codify` and `cook-log` skills also ask for headings of their
    own in a reply. The instructions say how the two combine: the skill's
    headings are kept, the `File to save:` blocks go under the heading
    that reports the files, and the nothing-was-saved line is still last.
    The instructions give no second way to save: a chat hands every file
    back, whatever tools its app offers.
12. **The four apps, and what was actually read.** The ticket names Claude
    Projects, ChatGPT Projects, Gemini Gems, and Muse. The design report
    marks its knowledge of them as inferred. Leg 1 read two vendor help
    pages on 2026-11-19, and `chat/README.md` says, row by row, what was
    read and what was not:
    - Claude Projects: the page "How can I create and manage projects?" on
      Claude's help site was read; it names "Set project instructions" and
      the "project knowledge base" with its "+" button. It does not mention
      connecting a GitHub repository, so the notes do not either.
    - Gemini Gems: the page "Tips for creating custom Gems" on Google's
      Gemini help site was read; it names an "instructions box" and
      "Knowledge", then "Add files".
    - ChatGPT Projects: the help page returned an error to leg 1's reader.
      The row says the names are not checked and may be wrong.
    - Muse: a search found no official page that describes instructions or
      knowledge files for a Muse chat. The row says "Not known" and points
      to the fallback: paste the instructions as the first message and
      attach the bundle.
    The notes link the two pages that were read and no other. Nothing in
    the notes states a vendor's file-size limit, plan, or price.
13. **The sync contract.** `adapters/README.md` holds the ticket's six
    rules, each with the reason it exists. The ticket lists "report each
    destination separately" before "read back before claiming success";
    the contract numbers them the other way, read back fifth and report
    sixth, because the rules are followed in order and the report has to
    say what the read-back found. It also holds the following, which the
    ticket leaves open:
    - **What is copied** is the card from its title line (`# `) to its end.
      The block of fields above the title is left out.
    - **What counts as the copy.** A note whose title is exactly the
      card's title, in the trash or not. A note that only resembles it is
      not the copy. A search that finds nothing after a failed create does
      not license a second create: the agent asks the cook first.
    - **When.** `method/status-and-versions.md` already holds the rule (only
      when the cook asks or calls the recipe final) and is linked, not
      restated as a second rule. The contract adds that the copy is made
      from the card file in the repository and only when the card's latest
      editor report passes for the card as it stands, which is the order of
      the loop in `AGENTS.md` (editor check, pull request, then mirror). It
      says how to tell: the newest report in the card's folder under `qc/`
      has a passing verdict, and its `Card-SHA256:` line is the one
      `scripts/check-qc.sh --hash` prints for the card. The gate itself
      checks only cards that changed since a base, so it cannot answer
      this for a merged card.
    - **The `mirrors` line** is set after a read-back that matches, by the
      `recipe-codify` skill, and that is a change to the card, so it gets
      an editor check like any other. This follows from the gate as S005
      shipped it: the gate hashes the whole card file. This spec does not
      change that. A save that sets only the `mirrors` line does not
      change the card's version, and a row is stale only when the version
      has moved, so the copy stays current even if that save also adds a
      changelog line. The read-back compares ingredients, amounts, steps,
      times, and temperatures, none of which such a save touches.
    - **The sync map** has six columns: Card, Destination, External ID,
      Version copied, Read back, State. The four states are `current`,
      `stale`, `unverified`, and `failed`. A row is stale whenever its
      version is older than the card's, whatever its State cell says, so no
      skill has to be changed to mark rows stale. A copy that was found by
      search and not yet written by a sync gets a row with the version
      `unknown`, the read-back `never`, and the state `unverified`. The
      baseline for spotting a hand edit is the card at the row's version,
      read from git's history of the card file; with `unknown` there is no
      baseline, so every difference is shown to the cook.
      `adapters/sync-map.md` ships with the header row and no other row.
    - **IDs on a public fork.** The sync map is committed, so its IDs are
      public on a public fork. The contract says so, forbids a password, a
      token, a key, or a link that carries one, tells the cook to check
      whether knowing an ID is enough to open the copy in their app, and
      tells a cook who would not publish an ID to keep the fork private. There is no git-ignored
      second sync map: two places to look is how a duplicate gets made.
    - **Nothing outside `adapters/` is the contract.** No skill is edited.
      `AGENTS.md` step 10 points to the contract (decision 15).
    - **A chat makes no copy.** The contract needs the sync map, the card
      file, and the editor reports, which a chat cannot read or write. The
      instructions therefore tell a chat not to create or update a copy
      even when its app offers a tool that could, and the setup notes say
      mirroring is a job for an agent that works in the repository.
14. **The Mem example, and what came from the private sources.**
    `adapters/mem.md` maps the six rules onto the tool names the Mem
    connector offered to leg 1's session on 2026-11-19, read from the
    connector's tool definitions and not from any account: `search_notes`,
    `get_note`, `create_note`, `update_note`, `search_collections`, and
    `add_note_to_collection`. The definitions say that the first line of a
    note's content is its title; that `create_note` gives the new note an
    ID, which later calls take; that an update replaces the whole note and
    needs the `version` that `get_note` returns; that a trashed note is
    still returned with a mark; that search is ranked and bounded; and
    that a collection is a group a note can be added to, found with
    `search_collections` and filled with `add_note_to_collection`. The
    page says those things and no other fact about Mem. It does not say
    how Mem lays out a table or a list; it says only that a different
    layout is formatting and not a difference. It says the
    names can change and that the repository is not affiliated with Mem.
    Its worked example uses a made-up card path and writes the ID as `<the
    ID Mem returned>`. From
    `private-sources/council-skills/recipe-publish/` this spec keeps only
    the two ideas the ticket names, in its own words: a write is not a
    copy until it was read back by its ID, and an update needs the current
    version. It drops, as the ticket says, the IDs, the raw links, pushing
    the default branch, and the title decoration. No passage of a private
    source is copied. Whether a file holds a collection name from a real
    account cannot be checked by a public pattern, so the privacy sweep's
    denylist is the gate for that part of the ticket's "done"; `idcheck`
    covers links and anything shaped like an ID.
15. **`AGENTS.md`: two lines changed, two sentences removed, still under
    8,192 bytes.** Step 10 of the loop now ends "by
    [`adapters/README.md`](adapters/README.md)" in place of "then read the
    copy back" (the contract holds the read-back), and the list of checks
    gains the bundle check. S001 set the file's size below 8,192 bytes and
    it stood at 8,166, so these additions did not fit. Two sentences of the
    first paragraph are removed to make room: "Read this file first, then
    the files it points to." and "It applies to every agent, whichever
    harness runs it." Both are framing: the heading "Read in this order"
    says the first, and no rule depends on the second. The file is 8,156
    bytes. The sentence about an agent that cannot read or write files
    stays as it is.
16. **No skill, template, or method page is edited.** L004 and L005 attach
    open notes to the next spec that edits either skill, the templates,
    `method/status-and-versions.md`, `method/recipe-qc.md`, the report
    format, or the gate. This spec edits none of them, so those notes stay
    open for that spec, and the bundle is built from those files as they
    are at `base_sha`. L006's note about the tuna melt's report does not
    apply here: this spec neither points to that report nor seeds anything
    from it.
17. **The chat run.** One fresh subagent stands in for a chat app's
    assistant: it may read only `chat/project-instructions.md` and
    `chat/bundle.md`, and it answers one cook's message that asks for a
    made-up recipe to be saved as a new card (`### The chat run`).
    `chatcheck` then checks the reply mechanically, for the properties `###
    Gate helpers` lists and no others. A reply that fails is not retried on
    the same subagent. The executor
    starts one more fresh subagent with the same brief; if that reply
    fails too, it commits nothing for Task 2 and reports ``Question: the
    chat run of `docs/specs/S007-chat-path-and-adapters.md` failed twice
    (<the lines chatcheck printed>); revise the instructions?`` The
    instructions and the bundle are never edited to make a run pass. One
    run is a sample, not a proof of how every chat app behaves, and the
    pull request says so.
18. **Kitchen front matter is matched as plain text.** The instructions
    call a kitchen file blank when its `filled_in` line is not exactly
    `filled_in: yes`, the plain-text rule the `chef-council` skill settled
    after L001. Nothing here parses YAML.
19. **Task names are commit subjects** (L001), and each `##` heading and
    each `### Task` heading occurs once, with no paragraph of 80 or more
    characters repeated outside the fenced blocks (L001, L004); leg 1
    checked both after its last edit.

## Prerequisites

- Leg 2 starts from this spec's approval commit on
  `workstream/t013-chat-path-and-adapters`, which already holds the claim
  commit for T013. Staging, the per-task commit with its `Spec-Task:
  S007/<N>` trailer, the push, the pull request, and the base-drift check
  are the `2-spec-execute` skill's standing procedure and the profile's
  ship tail. Each task's commit holds exactly that task's Touches.
- The executor's machine has Git 2.32 or later, Bash 4.4 or later, Python
  3, GNU coreutils (`sha256sum`, `sort -z`), and an authenticated `gh`. It
  is Linux x86_64, where `scripts/secret-scan.sh` fetches its pinned
  gitleaks, or `GITLEAKS_BIN` names an installed gitleaks of the pinned
  version (profile). `git config user.email` ends in
  `@users.noreply.github.com` (profile). `git rev-parse --verify
  origin/main` succeeds after `git fetch origin`.
- `locale -a` lists `C.utf8` or `C.UTF-8`. (One test runs the script under
  that locale. On a machine without it the script still passes, because
  it sets its own locale, but Bash prints a warning the test does not
  read.)
- The file system of the checkout and of the temporary directory accepts
  a file name that is not valid UTF-8, as Linux file systems do: `python3
  -c "import os, tempfile; d = tempfile.mkdtemp(); open(os.path.join(os.fsencode(d), b'caf\xe9.md'), 'w').close(); print('ok')"`
  prints `ok`. One test needs it, and skips itself elsewhere, which would
  change the suite's last line from `OK`; every count in this spec assumes
  it runs. If the command fails, report ``Question: this machine's file
  system refuses a file name that is not UTF-8, which one test of
  `docs/specs/S007-chat-path-and-adapters.md` needs; run leg 2 on Linux?``
  and stop.
- Before Task 1, `git status --porcelain --untracked-files=all` prints
  nothing, `git ls-files chat adapters .gitattributes` prints nothing, and
  `git grep -Il $'\r'; echo $?` prints `1` and nothing else.
- `test -x "$(git rev-parse --git-common-dir)/info/privacy-sweep"` succeeds.
  `WAYFINDER` is set to the directory the harness prints when the wayfinder
  skill loads, and `test -f "$WAYFINDER/scripts/lint.py"` succeeds
  (profile). If either is missing, report ``Question: <the privacy sweep |
  the Wayfinder lint> that the profile requires is not on this machine;
  provide it?`` and stop.
- The harness has an agent tool that can start a fresh subagent able to
  read files (`### The chat run`). A session without one reports
  ``Question: this harness cannot start the fresh subagent that the chat
  run of `docs/specs/S007-chat-path-and-adapters.md` requires; run leg 2
  in one that can?`` and stops.

### Writing a file from this spec

Each file under `## File contents`, and each helper under `### Gate
helpers`, is the text inside the fenced block that follows its heading:
every line between the opening and closing fence, each ended by a line
feed, with nothing added or removed. The opening fence is a line of four
backticks, with or without a language name after them, and the closing
fence is the next line that is exactly four backticks. `block` prints one
such block, and `extract` writes one file from it; both are defined in the
setup file. Usage: `extract chat/README.md`. The SHA-256 gates decide
whether a file is right, whichever way it was written.

### Gate helpers

Four blocks, none of them a repository file. The first is the setup file;
it loads the other three.

`setup` sets the fixed paths every gate uses and defines `block` and
`extract`. `S007` is a folder outside the repository; `OUT` and `REPLY` are
files in it, at fixed paths, because the harness starts a new shell for
each command and a path made by `mktemp` would be a new, empty file each
time (L006).

`linkcheck` is the helper of S002 to S006, unchanged. It reads the Markdown
files named on its command line, skips fenced code blocks, and requires the
target of every inline link with a relative target to be a path git tracks
or has staged. It prints one line per broken link and returns 1, or prints
nothing and returns 0.

`idcheck` reads the files named on its command line and prints one line,
`<path>:<line number>: holds a link or something shaped like an ID`, for
each line that holds a web address, a host name ending in one of six
common endings, a UUID, a run of sixteen or more hexadecimal characters, a
run of nine or more digits, or an unbroken run of twenty-four or more
letters, digits, hyphens, and underscores. It returns 1 when it prints any
line and 0 otherwise.

`chatcheck <reply file>` checks the reply of the chat run. It prints `chat
ok` and returns 0 when all of these hold, and otherwise prints one line per
problem and returns 1:

- the reply's last line that is not blank is exactly `Nothing was saved: I
  cannot write files here.`;
- one line is exactly `File to save: recipes/sides/lemon-rice.md`, the
  path the rules of `method/status-and-versions.md` give the fixture;
- exactly one `File to save:` line names a file directly under
  `.sources/lemon-rice/` that ends `.md`, the source packet the
  `recipe-codify` skill requires, and its block holds the lines `##
  Approved text`, `- 1/4 teaspoon salt`, and `## Scope instruction`;
- no path has two `File to save:` blocks;
- every `File to save:` line is followed, as the next line that is not
  blank, by a line of exactly four backticks, with or without a language
  name, and that fence is closed by a later line of exactly four
  backticks;
- the card's block holds the lines `id: lemon-rice`, `version: v1.0`,
  `evidence: untested`, `category: sides`, and `mirrors: none`, and holds
  each of `status: draft`, `- **Status:** draft`, and `- **Kitchen
  evidence:** untested` exactly once. The status is `draft` and not
  `reviewed`, because the fixture gives no total time and nothing shows the
  recipe was checked (`method/status-and-versions.md`);
- the card's block holds each of the fixture's amounts and times: `1 cup`,
  `1 tablespoon`, `1/2 teaspoon`, `1/4 teaspoon`, `30 seconds`, and `3
  minutes`;
- the reply names the index command, `python3 scripts/build-index.py`, and
  names `method/recipe-qc.md`, where the editor prompt is;
- no line other than the last says that something was saved, committed,
  synced, or mirrored, by the pattern in the helper;
- the card's Source line does not name a lens.

`chatcheck` proves these properties of one reply and no others. It does not
read the rest of the packet or the card, the order of the reply's parts, or
whether the reply is good advice.

#### Helper: `setup`

````bash
S007="${TMPDIR:-/tmp}/s007"
OUT="$S007/out.txt"
REPLY="$S007/reply.txt"
SPEC="$(git rev-parse --show-toplevel)/docs/specs/S007-chat-path-and-adapters.md"
BASE_SHA=8b3e43e8ea034efa3378216c70f6b55a89dd4ceb
SWEEP="$(git rev-parse --git-common-dir)/info/privacy-sweep"
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
eval "$(block '#### Helper: `linkcheck`')"
eval "$(block '#### Helper: `idcheck`')"
eval "$(block '#### Helper: `chatcheck`')"
````

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

#### Helper: `idcheck`

````bash
idcheck() {
  python3 - "$@" <<'PY'
import re, sys
PATTERN = re.compile(
    r"https?:|www\.|[a-z0-9.-]+\.(com|ai|io|net|org|app)\b"
    r"|[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    r"|\b[0-9a-fA-F]{16,}\b|\b[0-9]{9,}\b|\b[A-Za-z0-9_-]{24,}\b"
)
bad = 0
for path in sys.argv[1:]:
    for number, line in enumerate(open(path, encoding="utf-8"), 1):
        if PATTERN.search(line):
            print("%s:%d: holds a link or something shaped like an ID" % (path, number))
            bad = 1
sys.exit(bad)
PY
}
````

#### Helper: `chatcheck`

````bash
chatcheck() {
  python3 - "$1" <<'PY'
import re, sys
LAST = "Nothing was saved: I cannot write files here."
CARD = "File to save: recipes/sides/lemon-rice.md"
CLAIM = re.compile(
    r"\b(i|i have|i've|we|we have|we've) (saved|committed|synced|mirrored|checked in)\b"
    r"|\b(has|have|was|were|is now|are now|been) (saved|committed|synced|mirrored)\b",
    re.I,
)
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
problems = []
filled = [i for i, line in enumerate(lines) if line.strip()]
if not filled or lines[filled[-1]] != LAST:
    problems.append("the last line is not the nothing-was-saved line")
blocks = {}
for i, line in enumerate(lines):
    if not line.startswith("File to save: "):
        continue
    path = line[len("File to save: "):]
    following = [j for j in filled if j > i]
    if not following or not re.fullmatch(r"````[a-z]*", lines[following[0]]):
        problems.append("no fence of four backticks after: " + line)
        continue
    closing = [j for j in range(following[0] + 1, len(lines)) if lines[j] == "````"]
    if not closing:
        problems.append("the fence is not closed after: " + line)
        continue
    if path in blocks:
        problems.append("two blocks for: " + line)
    blocks[path] = lines[following[0] + 1:closing[0]]
if CARD[len("File to save: "):] not in blocks and CARD not in lines:
    problems.append("no line: " + CARD)
packets = [path for path in blocks if re.fullmatch(r"\.sources/lemon-rice/[^/]+\.md", path)]
if len(packets) != 1:
    problems.append("not exactly one source packet under .sources/lemon-rice/")
for path in packets:
    for wanted in ("## Approved text", "- 1/4 teaspoon salt", "## Scope instruction"):
        if wanted not in blocks[path]:
            problems.append("the packet has no line: " + wanted)
card = blocks.get("recipes/sides/lemon-rice.md", [])
for wanted in ("id: lemon-rice", "version: v1.0", "evidence: untested", "category: sides", "mirrors: none"):
    if wanted not in card:
        problems.append("the card has no line: " + wanted)
for wanted in ("status: draft", "- **Status:** draft", "- **Kitchen evidence:** untested"):
    if card.count(wanted) != 1:
        problems.append("the card does not hold exactly one line: " + wanted)
text = "\n".join(card)
for wanted in ("1 cup", "1 tablespoon", "1/2 teaspoon", "1/4 teaspoon", "30 seconds", "3 minutes"):
    if wanted not in text:
        problems.append("the card does not hold: " + wanted)
if any(line.startswith("- **Source:**") and "lens" in line.lower() for line in card):
    problems.append("the card's Source line names a lens")
if "python3 scripts/build-index.py" not in "\n".join(lines):
    problems.append("the reply does not give the index command")
if "method/recipe-qc.md" not in "\n".join(lines):
    problems.append("the reply does not point to method/recipe-qc.md for the editor check")
for i, line in enumerate(lines):
    if filled and i == filled[-1]:
        continue
    if CLAIM.search(line):
        problems.append("line %d claims a save: %s" % (i + 1, line.strip()[:80]))
for problem in problems:
    print(problem)
if not problems:
    print("chat ok")
sys.exit(1 if problems else 0)
PY
}
````

### The chat run

The chat run is one fresh subagent, started through the harness's agent
tool: the harness's general-purpose agent type, on the model the global
rules' tier table gives the orchestrator tier for the session's provider.
It is briefed with exactly the brief below and nothing else, with `<dir>`
replaced by the absolute path `git rev-parse --show-toplevel` prints. The
orchestrator saves the subagent's reply to `$REPLY`, exactly as returned
except for what the harness adds around it: an indentation the harness
puts before every line is removed, and so are a line of the harness's own
before the reply and one after it, such as a usage or agent-ID line
(L006). The orchestrator changes no other character of the reply.

````text
You are standing in for a chat app's assistant in a test. In this test you have no repository and no terminal. You may use exactly one tool, the file reader, on exactly two files, which stand for what a chat app would give its assistant:

- `<dir>/chat/project-instructions.md` is your instructions, the text in the app's instructions field. Read all of it first and follow it.
- `<dir>/chat/bundle.md` is your knowledge file. It is long, so read it in parts, and read every part your instructions and the job below need.

Use no other tool, read no other file, and write no file. Then reply to the cook's message below exactly as the assistant would reply in the chat. Your whole final message is that reply: add nothing about the test, and nothing before or after the reply.

The cook's message:

Skip the kitchen interview for now. I want this saved as a new card, exactly as written, in a category called sides.

Lemon Rice

Serves 2.

- 1 cup cooked long-grain rice, cold
- 1 tablespoon neutral oil
- 1/2 teaspoon mustard seeds
- 1 tablespoon lemon juice
- 1/4 teaspoon salt

1. Heat the oil in a skillet over medium heat until it shimmers.
2. Add the mustard seeds and cook until they pop, about 30 seconds.
3. Add the rice and the salt and stir until hot, about 3 minutes.
4. Take the pan off the heat and stir in the lemon juice.

I have not cooked it yet. Save it.
````

The recipe in the brief is a fixture written for this spec. It comes from
no publisher and no private source, and it is never saved as a card.

## Build plan — agent loop

Run every command from the repository root. The harness starts a new shell
for each command, so every gate command begins by sourcing the setup file
(L006). Write the setup file once, before Task 1, with this command, which
reads the `setup` block out of this spec:

```bash
mkdir -p "${TMPDIR:-/tmp}/s007" && python3 - docs/specs/S007-chat-path-and-adapters.md > "${TMPDIR:-/tmp}/s007/setup.sh" <<'PY'
import re, sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index("#### Helper: `setup`")
opening = next(i for i in range(start + 1, len(lines)) if re.fullmatch(r"`{4,}[a-z]*", lines[i]))
closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "````")
sys.stdout.write("".join(line + "\n" for line in lines[opening + 1:closing]))
PY
```

Every gate command is then run as `. "${TMPDIR:-/tmp}/s007/setup.sh" &&
<the command>`. After sourcing, `type -t block extract linkcheck idcheck
chatcheck` prints `function` five times, and `sha256sum
"${TMPDIR:-/tmp}/s007/setup.sh"` prints a line that begins
`1b93639dc4d29cc66d1f9d8791f833306977b032a0265bf576133bdc7a25a4d5`. A gate passes only when every command in it prints what is
stated. Where a gate ends in `; echo $?`, the printed status is part of the
expected output. The gate's commands run in the order listed. `$OUT` and
`$REPLY` keep their content from one command to the next, because their
paths are fixed.

Baseline, measured by leg 1 on 2026-11-19 in a scratch clone at
`base_sha`: `python3 -m unittest discover -s tests -v` exits 0 and ends
`OK` with 225 tests; `python3 scripts/check-skills.py` prints `skills
checked: 4`; `python3 scripts/check-council.py` prints `council checked:
14 seated, 14 records`; `python3 scripts/lint-cards.py` prints `cards
checked: 2`; `wc -c < AGENTS.md` prints `8166`. Every other gate line names
a file this spec creates or changes, so it is red on the base by design;
none measures old debt. Leg 1 then built all three tasks in a second
scratch clone from this spec's text with `extract`, sourcing the setup
file as above, and ran every gate line below on it except the lines that
need this run's own commits, `origin`, or the pull request.

Mutation probe (L004), run by leg 1 on 2026-11-19 in the first clone: 39
one-line mutants of `scripts/build-chat-bundle.sh`, each run against
`tests/test_build_chat_bundle.py`. They covered the locale, the sort and
its direction, the depth of the skill folders, the name and type tests of
`find`, following links, the order of the four places and a dropped place,
each part of the marker pattern, the line-break and no-file refusals, the
added line feed, the blank line and the two marker lines, each branch of
`--check` and its exit statuses, a `--check` that writes, the argument
handling, the error stream and status of `fail`, the list's bullet, a copy
that strips carriage returns, the temporary folder's removal, and a write
that appends. The first run left two alive; a test for the temporary
folder was added, and 38 of the 39 are now killed. The one survivor is
accepted: removing `|| fail "could not read $path"` after `cat`. Testing
it needs a file the script can list and cannot read, which a test run as
root cannot make, and a skipped test would change the suite's last line
from `OK`. The branch stays in the script. For the same reason no test
reaches the branch that exits 2 when `grep` itself cannot read a file,
which was added after the cross-examination (finding 11); the probe was
run again on the script as given here, with the same 38 killed.

Chat-run rehearsal (L003), run by leg 1 on 2026-11-19 with fresh
orchestrator-tier subagents, each briefed exactly as `### The chat run`
briefs it, on the instructions and the bundle this spec gives:

- The first run, on the first draft of the instructions, returned the
  source packet and the card, each under a `File to save:` line and inside
  a fence of four backticks, gave the index command, pointed the cook to
  "The editor prompt for a new chat", and ended with the nothing-was-saved
  line. The card carried `status: draft` and `evidence: untested` and wrote
  `Not stated.` for the total time the fixture does not give.
- The cross-examination then changed the instructions (findings 3, 4, and
  5), so a second fresh subagent ran on the instructions as given here. Its
  reply had the same parts, with the skill's own headings kept around the
  two files as the instructions now ask. `chatcheck`, as given here,
  printed `chat ok` and returned 0 on that reply as saved, with the
  harness's two-space indentation removed. It also prints `chat ok` on the
  first run's reply.
- `chatcheck` was run on six altered copies of the second reply, and it
  printed a problem and returned 1 for each: the last line removed; the
  card's `File to save:` line removed; a fence of three backticks; the
  evidence line changed to `cooked-once`; `1/4 teaspoon` changed to `1/2
  teaspoon` in the card's table; and a sentence `I have saved the card.`
  added.

One run is a sample. Decision 17 says what a failed run in leg 2 means.

### Task 1 — Add the tests for the chat bundle script, the instructions limit, and the line-ending rule
- **Work:** Run `extract tests/test_build_chat_bundle.py`, `extract
  tests/test_chat_instructions.py`, and `extract
  tests/test_line_endings.py`. The seams under test are observed only from
  outside:
  - `tests/test_build_chat_bundle.py`: the command
    `scripts/build-chat-bundle.sh`, through its exit status, its two
    output streams, and the bytes of the `chat/bundle.md` it writes, in
    small trees the tests build in temporary directories. The expected
    bundle is a literal written from decisions 4 and 5. It catches: the
    exact bytes of a four-file bundle; `chat/` made when missing; an old
    bundle replaced; two runs giving the same bytes; running from another
    folder; the same bundle under three locales; no temporary file left
    behind; the order of the four places and the byte order inside each;
    the files following the order of the list; a file that is not
    lowercase `.md` left out; `.agents/skills/README.md` left out; other
    folders left out; a symbolic link to a file or a folder not bundled; a
    folder named like a Markdown file; a name with a space and an accent;
    a name with a byte that is not UTF-8 under a UTF-8 locale; a file
    copied byte for byte; a missing final line feed added; an empty file;
    Windows line endings kept; marker text allowed inside a line; `--check`
    passing and writing nothing; `--check` failing on a missing bundle, a
    changed file, an added or removed file, a hand edit, and Windows line
    endings in the bundle; `--check` from another folder; each of the four
    places missing; no file to bundle; a line that starts like a marker; a
    file name with a line break; an unknown option or an extra argument;
    the script's executable bit; and this repository's own bundle being
    current.
  - `tests/test_chat_instructions.py`: the file
    `chat/project-instructions.md`. It catches a file of 8,000 characters
    or more (the literal limit of decision 2), an empty file, a missing or
    doubled final line feed, a carriage return, and instructions that no
    longer name the two marker lines the script writes.
  - `tests/test_line_endings.py`: the file `.gitattributes`, through what
    `git` and `scripts/check-qc.sh --hash` do in a repository built with
    `core.autocrlf=true`. Its expected hash is the SHA-256 of the bytes
    `git show` prints for the committed card, which is an independent
    reading of the committed bytes and not the script's own. It catches
    the four cases of decision 9, the first of which is a control that
    passes with or without the rule.
- **Touches:** `tests/test_build_chat_bundle.py`,
  `tests/test_chat_instructions.py`, `tests/test_line_endings.py`
- **Gate:**
  - This prints three lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    98b88d9f14819e6f529dfa95cf639e8c3f88674b08431e60252e3e9ef7ccbbeb  tests/test_build_chat_bundle.py
    58aabb3fc7a5b429a485fe0515842298685c0dc700b4bcfdf9e607b0282cda0e  tests/test_chat_instructions.py
    056fc75ccf55af4d5f970db6c24d0e1533ef0e4bc862abfaffb3c24f83de2d23  tests/test_line_endings.py
    SUMS
    ```

  - With the working tree differing from `base_sha` only under `docs/` and
    in these three test files, `python3 -m unittest discover -s tests -v >
    "$OUT" 2>&1; echo $?` prints `1`, `tail -1 "$OUT"` prints `FAILED
    (failures=50)`, and `grep -c ' ok$' "$OUT"` prints `226`. This is the
    recorded red: leg 1 measured it on 2026-11-19 in a scratch clone at
    `base_sha` with only the three test files applied. The three files
    hold 44 test methods (35, 4, and 5). 43 of them fail, each by
    assertion, because the script, the instructions file, and
    `.gitattributes` do not exist yet: `bash` exits with its own status
    for a missing script and prints none of the expected lines, and the
    other two files are asserted to exist before they are read. None is
    an error and none is an import error. `failures=50` is more than 43
    because unittest counts each failing subtest, and four of the methods
    loop over subtests. The one new test that passes on the base is the
    control, `test_without_the_rule_the_setting_changes_the_checked_out_bytes`,
    which is why `ok` is counted 226 times and not 225: `grep -E
    'test_(build_chat_bundle|chat_instructions|line_endings)\..*\.\.\. ok$'
    "$OUT" | wc -l` prints `1`.
  - `"$SWEEP" --text tests/test_build_chat_bundle.py
    tests/test_chat_instructions.py tests/test_line_endings.py` ends with
    a line beginning `privacy sweep: clean` and exits 0.
- **Nature:** mechanical

### Task 2 — Add the chat bundle script, the bundle, the paste-in instructions, and the line-ending rule
- **Work:** In this order.
  1. Run `extract .gitattributes`, `extract scripts/build-chat-bundle.sh`,
     `chmod 755 scripts/build-chat-bundle.sh`, and `extract
     chat/project-instructions.md`.
  2. Run `scripts/build-chat-bundle.sh`, which prints `chat bundle written:
     33 files` and writes `chat/bundle.md`.
  3. Run the gate's lines "before the chat run". Only when all pass, go
     on (L002: every mechanical gate before the fresh reader).
  4. Start the chat run as `### The chat run` says and save its reply to
     `$REPLY`. Run the gate's lines "after the chat run". On a failure
     there, follow decision 17.
  5. Commit as the `2-spec-execute` task loop says, with this task's name
     as the subject and the trailer `Spec-Task: S007/2`, then run the
     gate's last line, "after the task's commit".
- **Touches:** `.gitattributes`, `scripts/build-chat-bundle.sh`,
  `chat/project-instructions.md`, `chat/bundle.md`
- **Gate:**
  - Before the chat run:
    - This prints four lines, each path followed by `: OK`:

      ```bash
      sha256sum -c - <<'SUMS'
      8359e7ee50f6fbb373e464f1b57ae6d78917bba0a9b8e7aaa65888b80c586905  .gitattributes
      b5c68621e794123ae173543074bc058332eefb0229c48bad3026108a74f10f48  scripts/build-chat-bundle.sh
      043cadfed60a9dc8998bd008d44c7f4aa9bfeefaffb593a592b8627163832ecc  chat/project-instructions.md
      230861b9a3ef2333edad693ea5bd8114df865aade79271512d0731a12bbc6355  chat/bundle.md
      SUMS
      ```

    - `test -x scripts/build-chat-bundle.sh; echo $?` prints `0`, and
      `bash -n scripts/build-chat-bundle.sh; echo $?` prints `0`.
    - `scripts/build-chat-bundle.sh --check; echo $?` prints `chat bundle
      checked: 33 files` then `0`. `grep -c '^===== FILE: ' chat/bundle.md`
      prints `33`, and `wc -c < chat/bundle.md` prints `221094`.
    - `python3 -c "print(len(open('chat/project-instructions.md',
      encoding='utf-8').read()))"` prints `6779`.
    - `python3 -m unittest discover -s tests -v > "$OUT" 2>&1; echo $?`
      prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$' "$OUT"`
      prints `269`. `git status --porcelain -- tests/` prints nothing.
    - `git add .gitattributes scripts/build-chat-bundle.sh chat`, then
      `git add --renormalize . && git diff --cached --name-only
      --diff-filter=M` prints nothing: the rule changes no file that is
      already committed (decision 9). `git grep -Il $'\r'; echo $?` prints
      `1` and nothing else.
    - `git check-attr text eol -- recipes/sides/butter-roasted-carrots-with-jaggery-and-sumac.md
      chat/bundle.md` prints four lines, two ending `text: auto` and two
      ending `eol: lf`.
    - `linkcheck chat/project-instructions.md; echo $?` prints `0` and
      nothing else.
    - `"$SWEEP" --text .gitattributes scripts/build-chat-bundle.sh
      chat/project-instructions.md chat/bundle.md` ends with a line
      beginning `privacy sweep: clean` and exits 0.
  - After the chat run:
    - `chatcheck "$REPLY"; echo $?` prints `chat ok` then `0`.
    - The `sha256sum -c` block above prints the same four `: OK` lines,
      and `git status --porcelain --untracked-files=all` prints exactly
      four lines: `A  .gitattributes`, `A  chat/bundle.md`, `A
      chat/project-instructions.md`, and `A
      scripts/build-chat-bundle.sh`, each with two spaces after the `A`.
      The subagent wrote no file.
    - `"$SWEEP" --text "$REPLY"` ends with a line beginning `privacy
      sweep: clean` and exits 0.
  - After the task's commit: `git status --porcelain
    --untracked-files=all` prints nothing; `git ls-files -s
    scripts/build-chat-bundle.sh` prints a line that begins `100755 `; and
    `git diff --name-only "$(git log --format=%H -1 --grep='^Spec-Task:
    S007/1$')"..HEAD -- tests/` prints nothing.
- **Nature:** mechanical

### Task 3 — Add the chat setup notes and the adapters, and run the bundle check in CI
- **Work:** In this order.
  1. Run `extract chat/README.md`, `extract adapters/README.md`, `extract
     adapters/sync-map.md`, `extract adapters/mem.md`, `extract AGENTS.md`,
     and `extract .github/workflows/ci.yml`.
  2. Change `.agents/spec-profile.md` by the one replacement under `####
     Edit: `.agents/spec-profile.md``: the text of its first block, which
     occurs exactly once in the file, becomes the text of its second
     block. This command does it and prints `1`, the number of
     occurrences it found before the change:

     ```bash
     python3 - <<'PY'
     import subprocess
     def block(heading):
         return subprocess.run(["bash", "-c", '. "${TMPDIR:-/tmp}/s007/setup.sh" && block "$1"', "_", heading], capture_output=True, text=True, check=True).stdout
     old = block("##### Before")[:-1]
     new = block("##### After")[:-1]
     path = ".agents/spec-profile.md"
     text = open(path, encoding="utf-8").read()
     print(text.count(old))
     if text.count(old) == 1:
         open(path, "w", encoding="utf-8").write(text.replace(old, new))
     PY
     ```

  3. Run the gate, commit as the `2-spec-execute` task loop says with this
     task's name as the subject and the trailer `Spec-Task: S007/3`, then
     run the gate's last line.
- **Touches:** `chat/README.md`, `adapters/README.md`,
  `adapters/sync-map.md`, `adapters/mem.md`, `AGENTS.md`,
  `.github/workflows/ci.yml`, `.agents/spec-profile.md`
- **Gate:**
  - This prints seven lines, each path followed by `: OK`:

    ```bash
    sha256sum -c - <<'SUMS'
    365e26109e6639a2c81406721ac0dac2923a5721a4ac7135c0afd13118b1af93  chat/README.md
    82e3d6e05b6c1dabca26bfee368dd94fd4456ddccf086d0625d99f5a6af24b1c  adapters/README.md
    6e5e6f3684d8291db7f11164616184043b4b4f70255e2b796df01a9f640c390c  adapters/sync-map.md
    849bb250b5eadef3393eaf3425b325e4c040a86c59d471a3793759feec48b7fe  adapters/mem.md
    9b04e18c43d5f69b0fd2dafc35851d7f42fc962616f2d656c768fe11a762d1e0  AGENTS.md
    33a5c25a161906fceb4313b38ec75875f8613ecba0abc6aebe592869da394b15  .github/workflows/ci.yml
    8d9a5e9587401cd523be5df6e19ad9a8c7f0a814c71bf9ae6f945c15714cffad  .agents/spec-profile.md
    SUMS
    ```

  - `git diff --stat -- .agents/spec-profile.md | tail -1` prints ` 1 file
    changed, 4 insertions(+), 1 deletion(-)`, and `git diff --stat --
    .github/workflows/ci.yml | tail -1` prints ` 1 file changed, 2
    insertions(+)`, and `grep -n -E '^      - name: (Check the chat bundle is current|Run the tests)$'
    .github/workflows/ci.yml | cut -d: -f2-` prints the bundle step's line
    first and `      - name: Run the tests` second. `git diff --stat -- AGENTS.md | tail -1` prints ` 1
    file changed, 3 insertions(+), 2 deletions(-)`, and `wc -c <
    AGENTS.md` prints `8156`.
  - `git add -N chat/README.md adapters`, then `linkcheck AGENTS.md
    chat/README.md adapters/README.md adapters/mem.md adapters/sync-map.md;
    echo $?` prints `0` and nothing else.
  - `idcheck adapters/README.md adapters/mem.md adapters/sync-map.md; echo
    $?` prints `0` and nothing else.
  - `grep -c '^```' chat/README.md` prints `0`, and `grep -c -E '^\|
    (Claude Projects|ChatGPT Projects|Gemini Gems|Muse) \|' chat/README.md`
    prints `4`. `tail -1 adapters/sync-map.md` prints
    `|---|---|---|---|---|---|`: the table has no row.
  - `scripts/build-chat-bundle.sh --check; echo $?` prints `chat bundle
    checked: 33 files` then `0`: nothing this task touches is in the
    bundle.
  - `python3 scripts/check-skills.py; echo $?` prints `skills checked: 4`
    then `0`. `python3 -m unittest discover -s tests -v > "$OUT" 2>&1;
    echo $?` prints `0`, `tail -1 "$OUT"` prints `OK`, and `grep -c ' ok$'
    "$OUT"` prints `269`. `git status --porcelain -- tests/` prints
    nothing.
  - `python3 -c "import sys, re; t = open('.github/workflows/ci.yml').read();
    print(len(re.findall(r'^        run: scripts/build-chat-bundle\.sh --check$', t, re.M)))"`
    prints `1`.
  - `"$SWEEP" --text chat/README.md adapters/README.md adapters/mem.md
    adapters/sync-map.md AGENTS.md .github/workflows/ci.yml
    .agents/spec-profile.md` ends with a line beginning `privacy sweep:
    clean` and exits 0.
  - After the task's commit: `git status --porcelain
    --untracked-files=all` prints nothing, and `git diff --name-only
    "$(git log --format=%H -1 --grep='^Spec-Task: S007/1$')"..HEAD --
    tests/` prints nothing.
- **Nature:** mechanical

## Repo profile

`.agents/spec-profile.md` governs. This spec adds to it and leaves four
things for the pull request:

- **One addition.** Task 3 adds the bundle check's local command to the
  profile's list of CI commands, as the profile asks of the spec that adds
  a check. Nothing else in the profile changes.
- **The pull request's Evidence section** also holds: the chat run's reply
  as saved, the line `chatcheck` printed, and the sentence that one run is
  a sample (decision 17); the two output lines of definition-of-done item
  5; what the orchestrator saw in each rendered page (item 12); and the
  mutation probe's one accepted survivor.
- **Merge Danger** names decision 8: after this merge, a change under
  `kitchen/`, a skill folder, `method/`, or `templates/` fails CI until
  the bundle is rebuilt, on this repository and on every fork that takes
  the change. It also names `.gitattributes`, which applies to every path.
- **Agent behavior.** The chat run is the profile's "fresh subagent
  through the harness's agent tool, briefed only with what the spec
  names". No provider call is made.
- **Provider facts.** The vendor names in `chat/README.md` and the tool
  names in `adapters/mem.md` were read on 2026-11-19 as decisions 12 and
  14 say. The executor does not re-read them and changes no word of
  either file.

## Cross-examination

The blind cross-examination ran on 2026-11-19 through the profile's route:
Meta, `muse-wonder-full-1.0`, high reasoning effort, Muse Code 1.4.15
(1.4.15-R8339.1), read-only in the routes document's sandbox, on a dossier
of the first draft, `AGENTS.md`, the profile, ticket T013, and the
repository files this spec leans on (the CI workflow, the two method
pages, the `recipe-codify` and `chef-council` skills, `kitchen/README.md`,
`kitchen/profile.md`, the card and packet templates, `scripts/check-qc.sh`,
and learnings L004 to L006), privacy-swept and secret-scanned, with no
private-source file. It returned 21 findings. All 21 are accepted, two of
them in part. The files, hashes, helpers, counts, and rehearsals above are
the ones made after these edits; the reviewer read the draft before them,
and it could not run the script or the tests.

1. **A mirrors-only save changes the copied text.** ACCEPT. The claim that
   the copy cannot go stale because the block of fields is left out was
   wrong: such a save may add a changelog line below the title. The
   contract and decision 13 now rest on the version: a row is stale only
   when the card's version has moved, and the read-back compares
   ingredients, amounts, steps, times, and temperatures.
2. **`chatcheck` accepted `status: reviewed`.** ACCEPT. It now requires
   `status: draft`, and the status and evidence lines under the title,
   each exactly once.
3. **Two reply shapes with no precedence.** ACCEPT. The instructions now
   say that a skill's headings are kept, the `File to save:` blocks go
   under the heading that reports the files, and the nothing-was-saved
   line is last (decision 11). The chat run was rehearsed again on the
   new text.
4. **A chat with a notes-app tool cannot follow the contract.** ACCEPT. A
   chat now makes no copy at all; the instructions and the setup notes
   say so (decision 13).
5. **The file-tool paragraph contradicted the no-save rule.** ACCEPT. The
   paragraph is removed. A chat hands every file back (decision 11).
6. **The line-ending trap on the chat path.** ACCEPT. `chat/README.md` now
   tells the cook to save each file with line feeds and says why. The
   change to `--hash` that would close the case stays out of scope
   (decision 9).
7. **The CI gate could not run in fresh shells.** ACCEPT. Item 11 is one
   command that assigns `PR`, `HEAD_SHA`, `RUN`, and `JOB`, filters the
   run to the `CI` workflow's pull-request event, and passes the run to
   `gh run view`.
8. **The named step was skipped when the bundle was stale.** ACCEPT. The
   step now comes before the unit tests, and Task 3's gate checks the
   order (decision 7).
9. **The rendered-pages item was not binary.** ACCEPT. Item 12 names the
   command and seven observations, each tied to its file.
10. **`chatcheck` proves less than the run was said to show.** ACCEPT in
    part. Added: exactly one packet, three lines the packet must hold, no
    path with two blocks, and the pointer to `method/recipe-qc.md`. Not
    added: the order of the reply's parts and a full reading of the
    packet, which would pin wording the skills leave to the writer.
    Decision 17, item 9, and `### Gate helpers` now say the check proves
    its listed properties and nothing wider.
11. **Exit 2 was not always one line.** ACCEPT. The script now tells a
    `grep` that could not read a file from one that found no marker and
    exits 2 on the first. Decision 6 says a failing tool's own message may
    come before the script's line. The tests' helper is unchanged: the
    five cases it checks still print one line.
12. **Report came before read-back.** ACCEPT. The contract numbers
    read-back fifth and report sixth, and decision 13 says why this
    departs from the ticket's order of words.
13. **No way to tell that a merged card's report passes.** ACCEPT. The
    contract names the report, the verdict, and the hash comparison.
14. **A title search cannot rule out a duplicate.** ACCEPT. The contract
    defines the copy as a note whose title is exactly the card's, counts a
    trashed one, and requires asking the cook before a second create when
    a search finds nothing after a failed create.
15. **Undefined first row and baseline.** ACCEPT. A found copy gets
    `unknown`, `never`, and `unverified`; the baseline is the card at the
    row's version from git's history, and with `unknown` every difference
    is shown.
16. **Uploaded cards go stale.** ACCEPT. The setup notes now prefer
    pasting the card and log for each job, and say to replace or remove
    an uploaded copy after every change.
17. **Decision 14 listed fewer Mem facts than the page states.** ACCEPT.
    The decision lists every fact the page takes from the tool
    definitions. The sentence about how Mem lays out tables is reworded to
    claim nothing about Mem, and "a folder of notes" became "a named group
    of notes".
18. **A skipped test would change the pinned counts.** ACCEPT. A
    prerequisite now checks that the file system takes such a name, with a
    `Question:` when it does not. The skip stays in the test for other
    machines.
19. **`AGENTS.md` and the instructions define a blank file differently.**
    ACCEPT in part. Decision 3 now names the difference and says
    `AGENTS.md`'s sentence is the short form of the skill's test.
    `AGENTS.md` is not edited for it: the sentence shipped with S001 and
    S003, and the skill's test already governs.
20. **"An ID is not a secret" claimed too much.** ACCEPT. The contract now
    says "usually", and tells the cook to check whether knowing the ID is
    enough to open the copy.
21. **The command list left out `dirname` and `rm`.** ACCEPT. Decision 6
    lists both and no longer says "only".

## File contents

Each block below is one file, whole, as `### Writing a file from this
spec` says. The profile edit at the end is two blocks, the text before and
the text after.

#### File: `tests/test_build_chat_bundle.py`

````python
"""Tests for scripts/build-chat-bundle.sh, observed through its exit status,
its output, and the bundle file it writes.

Each test copies the script into a small tree it builds in a temporary
directory, so the expected bundles are literals written out here. The last
test runs the script's check on this repository itself.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "build-chat-bundle.sh")

HEADER = (
    "# Chef Council chat bundle\n"
    "\n"
    "This file is generated by `scripts/build-chat-bundle.sh`. Do not edit it: "
    "change the file it came from and run the script again.\n"
    "\n"
    "It holds the kitchen files, the skills, the method pages, and the templates "
    "of one Chef Council repository, for a chat app that cannot read the "
    "repository. Each file below starts at a line `===== FILE: <path> =====` and "
    "ends at a line `===== END FILE: <path> =====`. When an instruction names a "
    "path, read the file between those two lines. A link inside a file points to "
    "a path in the repository, and a path that is not listed here is a file you "
    "have not been given.\n"
    "\n"
    "## Files\n"
    "\n"
)

SMALL = (
    HEADER
    + "- kitchen/profile.md\n"
    + "- .agents/skills/chef-council/SKILL.md\n"
    + "- method/recipe-qc.md\n"
    + "- templates/recipe-card.md\n"
    + "\n"
    + "===== FILE: kitchen/profile.md =====\n"
    + "# Kitchen profile\n"
    + "===== END FILE: kitchen/profile.md =====\n"
    + "\n"
    + "===== FILE: .agents/skills/chef-council/SKILL.md =====\n"
    + "# Chef Council\n"
    + "===== END FILE: .agents/skills/chef-council/SKILL.md =====\n"
    + "\n"
    + "===== FILE: method/recipe-qc.md =====\n"
    + "# The editor check\n"
    + "===== END FILE: method/recipe-qc.md =====\n"
    + "\n"
    + "===== FILE: templates/recipe-card.md =====\n"
    + "# Recipe title\n"
    + "===== END FILE: templates/recipe-card.md =====\n"
)

USAGE = "build-chat-bundle: usage: scripts/build-chat-bundle.sh [--check]\n"
MISSING = "chat bundle is missing: run scripts/build-chat-bundle.sh\n"
STALE = "chat bundle is out of date: run scripts/build-chat-bundle.sh\n"


class BuildChatBundleTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(os.path.realpath(self._tmp.name), "repo")
        os.makedirs(os.path.join(self.root, "scripts"))
        self.script = os.path.join(self.root, "scripts", "build-chat-bundle.sh")
        if os.path.isfile(SCRIPT):
            shutil.copy(SCRIPT, self.script)
        self.write("kitchen/profile.md", "# Kitchen profile\n")
        self.write(".agents/skills/chef-council/SKILL.md", "# Chef Council\n")
        self.write("method/recipe-qc.md", "# The editor check\n")
        self.write("templates/recipe-card.md", "# Recipe title\n")

    def path(self, relative):
        if isinstance(relative, bytes):
            return os.path.join(os.fsencode(self.root), relative)
        return os.path.join(self.root, relative)

    def write(self, relative, content):
        target = self.path(relative)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        data = content if isinstance(content, bytes) else content.encode("utf-8")
        with open(target, "wb") as handle:
            handle.write(data)

    def run_script(self, *args, cwd=None, env=None):
        return subprocess.run(
            ["bash", self.script, *args],
            capture_output=True,
            cwd=self.root if cwd is None else cwd,
            env=env,
            check=False,
        )

    def bundle(self):
        with open(self.path("chat/bundle.md"), "rb") as handle:
            return handle.read()

    def build(self):
        result = self.run_script()
        self.assertEqual(
            (result.returncode, result.stderr), (0, b""), result.stdout + result.stderr
        )
        return result

    def listed(self):
        """The paths in the bundle's own list of files, in order."""
        lines = self.bundle().split(b"\n")
        start = lines.index(b"## Files") + 2
        end = lines.index(b"", start)
        return [line[2:] for line in lines[start:end]]

    def assert_cannot_run(self, result, message):
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (2, b"", ("build-chat-bundle: " + message + "\n").encode("utf-8")),
        )

    # Writing the bundle

    def test_small_tree_gives_the_expected_bundle(self):
        result = self.build()
        self.assertEqual(result.stdout, b"chat bundle written: 4 files\n")
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_chat_folder_is_made_when_it_is_missing(self):
        self.assertFalse(os.path.exists(self.path("chat")))
        self.build()
        self.assertTrue(os.path.isfile(self.path("chat/bundle.md")))

    def test_an_old_bundle_is_replaced(self):
        self.write("chat/bundle.md", "old\n")
        self.build()
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_two_runs_give_the_same_bytes(self):
        self.build()
        first = self.bundle()
        self.build()
        self.assertEqual(self.bundle(), first)

    def test_running_from_another_folder_gives_the_same_bundle(self):
        result = self.run_script(cwd=os.path.dirname(self.root))
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(self.root), "chat")))

    def test_bundle_does_not_depend_on_the_locale(self):
        self.write("kitchen/Zebra.md", "z\n")
        self.write("kitchen/apple.md", "a\n")
        bundles = []
        for locale in ("C", "C.UTF-8", "en_US.UTF-8"):
            env = dict(os.environ)
            env["LC_ALL"] = locale
            result = self.run_script(env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            bundles.append(self.bundle())
        self.assertEqual(bundles[0], bundles[1])
        self.assertEqual(bundles[0], bundles[2])

    def test_no_temporary_file_is_left_behind(self):
        scratch = os.path.join(os.path.dirname(self.root), "scratch")
        os.makedirs(scratch)
        env = dict(os.environ)
        env["TMPDIR"] = scratch
        self.assertEqual(self.run_script(env=env).returncode, 0)
        self.assertEqual(self.run_script("--check", env=env).returncode, 0)
        self.write("kitchen/profile.md", "changed\n")
        self.assertEqual(self.run_script("--check", env=env).returncode, 1)
        self.assertEqual(self.run_script("--chek", env=env).returncode, 2)
        self.assertEqual(os.listdir(scratch), [])

    # Which files, in which order

    def test_places_come_in_a_fixed_order_and_paths_in_byte_order(self):
        self.write("kitchen/vetting/b.md", "b\n")
        self.write("kitchen/Zebra.md", "z\n")
        self.write("kitchen/apple.md", "a\n")
        self.write(".agents/skills/cook-log/SKILL.md", "log\n")
        self.write(".agents/skills/chef-council/references/food-safety.md", "safe\n")
        self.write("method/a.md", "a\n")
        self.write("templates/cook-log.md", "log\n")
        self.build()
        self.assertEqual(
            self.listed(),
            [
                b"kitchen/Zebra.md",
                b"kitchen/apple.md",
                b"kitchen/profile.md",
                b"kitchen/vetting/b.md",
                b".agents/skills/chef-council/SKILL.md",
                b".agents/skills/chef-council/references/food-safety.md",
                b".agents/skills/cook-log/SKILL.md",
                b"method/a.md",
                b"method/recipe-qc.md",
                b"templates/cook-log.md",
                b"templates/recipe-card.md",
            ],
        )

    def test_files_follow_the_order_of_the_list(self):
        self.write("kitchen/apple.md", "a\n")
        self.build()
        markers = [
            line[len(b"===== FILE: ") : -len(b" =====")]
            for line in self.bundle().split(b"\n")
            if line.startswith(b"===== FILE: ")
        ]
        self.assertEqual(markers, self.listed())
        self.assertEqual(len(markers), 5)

    def test_file_that_is_not_markdown_is_left_out(self):
        self.write("kitchen/notes.txt", "notes\n")
        self.write("kitchen/photo.MD", "upper\n")
        self.write("templates/card.md.bak", "old\n")
        self.build()
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_markdown_file_beside_the_skill_folders_is_left_out(self):
        self.write(".agents/skills/README.md", "# Skills\n")
        self.build()
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_other_folders_are_left_out(self):
        self.write("recipes/sides/carrots.md", "# Carrots\n")
        self.write("chat/project-instructions.md", "# Instructions\n")
        self.write("adapters/README.md", "# Adapters\n")
        self.write("README.md", "# Readme\n")
        self.build()
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_symbolic_link_is_not_bundled(self):
        self.write("private.md", "private\n")
        os.symlink(self.path("private.md"), self.path("kitchen/link.md"))
        os.symlink(self.path("recipes"), self.path("templates/more"))
        self.write("recipes/sides/carrots.md", "# Carrots\n")
        self.build()
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_folder_named_like_a_markdown_file_is_not_bundled(self):
        self.write("kitchen/folder.md/inside.txt", "text\n")
        self.build()
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_name_with_a_space_and_an_accent_is_bundled(self):
        self.write("kitchen/café notes.md", "café\n")
        self.build()
        expected = "===== FILE: kitchen/café notes.md =====\ncafé\n===== END FILE: kitchen/café notes.md =====\n"
        self.assertIn(expected.encode("utf-8"), self.bundle())
        self.assertEqual(self.listed()[0], "kitchen/café notes.md".encode("utf-8"))

    def test_name_with_a_byte_that_is_not_utf8_is_bundled_in_a_utf8_locale(self):
        try:
            self.write(b"kitchen/caf\xe9.md", "latin\n")
        except OSError:
            self.skipTest("this file system refuses a name that is not UTF-8")
        env = dict(os.environ)
        env["LC_ALL"] = "C.UTF-8"
        result = self.run_script(env=env)
        self.assertEqual((result.returncode, result.stdout), (0, b"chat bundle written: 5 files\n"))
        self.assertIn(
            b"===== FILE: kitchen/caf\xe9.md =====\nlatin\n===== END FILE: kitchen/caf\xe9.md =====\n",
            self.bundle(),
        )

    # How a file is copied

    def test_file_is_copied_byte_for_byte(self):
        content = b"---\nfilled_in: no\n---\n\n\tTabbed \xc2\xb0F line  \n\n```text\nfenced\n```\n\n"
        self.write("kitchen/profile.md", content)
        self.build()
        self.assertIn(
            b"===== FILE: kitchen/profile.md =====\n" + content + b"===== END FILE: kitchen/profile.md =====\n",
            self.bundle(),
        )

    def test_file_without_a_final_line_feed_gets_one(self):
        self.write("kitchen/profile.md", "# Kitchen profile")
        self.build()
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_empty_file_is_bundled_as_nothing_between_its_markers(self):
        self.write("kitchen/empty.md", "")
        self.build()
        self.assertIn(
            b"\n===== FILE: kitchen/empty.md =====\n===== END FILE: kitchen/empty.md =====\n",
            self.bundle(),
        )

    def test_windows_line_endings_are_kept_as_they_are(self):
        self.write("kitchen/profile.md", b"# Kitchen profile\r\nline\r\n")
        self.build()
        self.assertIn(
            b"===== FILE: kitchen/profile.md =====\n# Kitchen profile\r\nline\r\n===== END FILE:",
            self.bundle(),
        )

    def test_marker_text_inside_a_line_is_allowed(self):
        self.write("method/recipe-qc.md", "A line `===== FILE: x =====` in prose.\n")
        self.build()
        self.assertIn(b"A line `===== FILE: x =====` in prose.\n", self.bundle())

    # The check

    def test_check_passes_on_a_current_bundle_and_writes_nothing(self):
        self.build()
        before = os.stat(self.path("chat/bundle.md")).st_mtime_ns
        result = self.run_script("--check")
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, b"chat bundle checked: 4 files\n", b""),
        )
        self.assertEqual(os.stat(self.path("chat/bundle.md")).st_mtime_ns, before)

    def test_check_fails_when_the_bundle_is_missing_and_does_not_write_it(self):
        result = self.run_script("--check")
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr), (1, MISSING.encode(), b"")
        )
        self.assertFalse(os.path.exists(self.path("chat")))

    def test_check_fails_when_a_bundled_file_changed(self):
        self.build()
        self.write("kitchen/profile.md", "# Kitchen profile\nfilled in\n")
        result = self.run_script("--check")
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr), (1, STALE.encode(), b"")
        )
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_check_fails_when_a_file_was_added_or_removed(self):
        self.build()
        self.write("templates/cook-log.md", "log\n")
        self.assertEqual(self.run_script("--check").returncode, 1)
        os.remove(self.path("templates/cook-log.md"))
        self.assertEqual(self.run_script("--check").returncode, 0)
        os.remove(self.path("templates/recipe-card.md"))
        self.write("templates/other.md", "# Recipe title\n")
        self.assertEqual(self.run_script("--check").stdout, STALE.encode())

    def test_check_fails_when_the_bundle_was_edited_by_hand(self):
        self.build()
        for edited in (SMALL + "\n", SMALL[:-1], SMALL.replace("Recipe title", "Recipe  title")):
            with self.subTest(edited=edited[-30:]):
                self.write("chat/bundle.md", edited)
                result = self.run_script("--check")
                self.assertEqual((result.returncode, result.stdout), (1, STALE.encode()))

    def test_check_fails_when_the_bundle_has_windows_line_endings(self):
        self.write("chat/bundle.md", SMALL.replace("\n", "\r\n"))
        result = self.run_script("--check")
        self.assertEqual((result.returncode, result.stdout), (1, STALE.encode()))

    def test_check_passes_from_another_folder(self):
        self.build()
        result = self.run_script("--check", cwd=os.path.dirname(self.root))
        self.assertEqual((result.returncode, result.stdout), (0, b"chat bundle checked: 4 files\n"))

    # When the script cannot run

    def test_missing_place_cannot_run(self):
        for place in ("kitchen", ".agents/skills", "method", "templates"):
            with self.subTest(place=place):
                shutil.move(self.path(place), self.path("moved"))
                for args in ((), ("--check",)):
                    self.assert_cannot_run(
                        self.run_script(*args), place + " is not a folder of " + self.root
                    )
                shutil.move(self.path("moved"), self.path(place))
        self.assertFalse(os.path.exists(self.path("chat")))

    def test_no_file_to_bundle_cannot_run(self):
        for relative in (
            "kitchen/profile.md",
            ".agents/skills/chef-council/SKILL.md",
            "method/recipe-qc.md",
            "templates/recipe-card.md",
        ):
            os.remove(self.path(relative))
        self.assert_cannot_run(self.run_script(), "found no file to bundle")
        self.assertFalse(os.path.exists(self.path("chat")))

    def test_line_that_starts_like_a_marker_cannot_run(self):
        self.build()
        for line in ("===== FILE: kitchen/other.md =====", "===== END FILE: x", "===== FILE: "):
            with self.subTest(line=line):
                self.write("templates/recipe-card.md", "# Recipe title\n" + line + "\n")
                for args in ((), ("--check",)):
                    self.assert_cannot_run(
                        self.run_script(*args),
                        "templates/recipe-card.md holds a line that starts like a bundle marker",
                    )
        self.assertEqual(self.bundle(), SMALL.encode("utf-8"))

    def test_file_name_with_a_line_break_cannot_run(self):
        self.write("kitchen/two\nlines.md", "x\n")
        self.assert_cannot_run(self.run_script(), "a file name holds a line break")
        self.assertFalse(os.path.exists(self.path("chat")))

    def test_unknown_option_and_extra_argument_cannot_run(self):
        for args in (("--chek",), ("--check", "--check"), ("chat/bundle.md",), ("",), ("--help",)):
            with self.subTest(args=args):
                result = self.run_script(*args)
                self.assertEqual(
                    (result.returncode, result.stdout, result.stderr), (2, b"", USAGE.encode())
                )
        self.assertFalse(os.path.exists(self.path("chat")))

    # This repository

    def test_script_is_executable(self):
        self.assertTrue(os.path.isfile(SCRIPT), "scripts/build-chat-bundle.sh is missing")
        self.assertTrue(os.access(SCRIPT, os.X_OK), "scripts/build-chat-bundle.sh is not executable")

    def test_this_repositorys_bundle_is_current(self):
        result = subprocess.run(
            ["bash", SCRIPT, "--check"], capture_output=True, text=True, cwd=REPO, check=False
        )
        self.assertEqual((result.returncode, result.stderr), (0, ""), result.stdout + result.stderr)
        self.assertRegex(result.stdout, r"\Achat bundle checked: [1-9][0-9]* files\n\Z")


if __name__ == "__main__":
    unittest.main()
````

#### File: `tests/test_chat_instructions.py`

````python
"""Tests for chat/project-instructions.md, the text a cook pastes into the
instructions field of a chat app.

The limit is the one the file promises: under 8,000 characters, so that it
fits an instructions field. The numbers here are literals from that promise.
"""

import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTRUCTIONS = os.path.join(REPO, "chat", "project-instructions.md")
LIMIT = 8000


class ChatInstructionsTest(unittest.TestCase):
    def read(self):
        self.assertTrue(os.path.isfile(INSTRUCTIONS), "chat/project-instructions.md is missing")
        with open(INSTRUCTIONS, "rb") as handle:
            return handle.read()

    def test_instructions_are_under_the_limit(self):
        text = self.read().decode("utf-8")
        self.assertLess(
            len(text),
            LIMIT,
            "chat/project-instructions.md holds %d characters; the limit is under %d" % (len(text), LIMIT),
        )

    def test_instructions_are_not_empty_and_end_with_one_line_feed(self):
        data = self.read()
        self.assertTrue(data.strip(), "chat/project-instructions.md is empty")
        self.assertTrue(data.endswith(b"\n") and not data.endswith(b"\n\n"))

    def test_instructions_hold_no_windows_line_endings(self):
        self.assertNotIn(b"\r", self.read())

    def test_instructions_name_the_markers_the_bundle_script_writes(self):
        text = self.read().decode("utf-8")
        self.assertIn("`===== FILE: <path> =====`", text)
        self.assertIn("`===== END FILE: <path> =====`", text)


if __name__ == "__main__":
    unittest.main()
````

#### File: `tests/test_line_endings.py`

````python
"""Tests for the line-ending rule in .gitattributes.

The editor gate hashes a card's committed bytes, and scripts/check-qc.sh --hash
and scripts/build-chat-bundle.sh read the files as they are checked out. The
rule keeps the two the same on a machine whose git would otherwise check text
files out with Windows line endings. Each test builds a repository in a
temporary directory with that setting turned on.
"""

import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTRIBUTES = os.path.join(REPO, ".gitattributes")
CHECK_QC = os.path.join(REPO, "scripts", "check-qc.sh")

CARD = b"# Roasted Carrots\n\n- **Version:** v1.0\n\nRoast until tender.\n"
CARD_PATH = "recipes/sides/roasted-carrots.md"


class LineEndingsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(self._tmp.name, "repo")
        os.makedirs(os.path.join(self.root, "recipes", "sides"))
        self.git("init", "-q")
        self.git("config", "user.name", "Test Cook")
        self.git("config", "user.email", "cook@example.invalid")
        self.git("config", "core.autocrlf", "true")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", self.root, *args], capture_output=True, check=True
        ).stdout

    def commit_and_check_out_again(self, with_rule):
        if with_rule:
            self.assertTrue(os.path.isfile(ATTRIBUTES), ".gitattributes is missing")
            shutil.copy(ATTRIBUTES, os.path.join(self.root, ".gitattributes"))
        card = os.path.join(self.root, CARD_PATH)
        with open(card, "wb") as handle:
            handle.write(CARD)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Add a card")
        os.remove(card)
        self.git("checkout", "--", CARD_PATH)
        with open(card, "rb") as handle:
            return handle.read()

    def test_without_the_rule_the_setting_changes_the_checked_out_bytes(self):
        # The control: it shows that these tests would notice a missing rule.
        self.assertEqual(self.commit_and_check_out_again(False), CARD.replace(b"\n", b"\r\n"))

    def test_with_the_rule_a_card_is_checked_out_with_line_feeds(self):
        self.assertEqual(self.commit_and_check_out_again(True), CARD)

    def test_with_the_rule_the_hash_of_the_working_file_is_the_committed_hash(self):
        self.commit_and_check_out_again(True)
        committed = self.git("show", "HEAD:" + CARD_PATH)
        self.assertEqual(committed, CARD)
        result = subprocess.run(
            ["bash", CHECK_QC, "--hash", CARD_PATH],
            capture_output=True,
            text=True,
            cwd=self.root,
            check=False,
        )
        self.assertEqual(
            (result.returncode, result.stdout),
            (0, "Card-SHA256: " + hashlib.sha256(committed).hexdigest() + "\n"),
        )

    def test_with_the_rule_a_card_saved_with_windows_line_endings_is_committed_with_line_feeds(self):
        self.commit_and_check_out_again(True)
        card = os.path.join(self.root, CARD_PATH)
        with open(card, "wb") as handle:
            handle.write(CARD.replace(b"\n", b"\r\n") + b"More.\r\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Change the card")
        self.assertEqual(self.git("show", "HEAD:" + CARD_PATH), CARD + b"More.\n")

    def test_the_rule_covers_every_path(self):
        self.assertTrue(os.path.isfile(ATTRIBUTES), ".gitattributes is missing")
        with open(ATTRIBUTES, encoding="utf-8") as handle:
            rules = [line for line in handle.read().split("\n") if line and not line.startswith("#")]
        self.assertIn("* text=auto eol=lf", rules)


if __name__ == "__main__":
    unittest.main()
````

#### File: `.gitattributes`

````text
# Line endings: every text file is checked out with line feeds, on every
# machine, whatever core.autocrlf says. A card's hash and the chat bundle are
# taken from the bytes of the files, so those bytes must be the committed ones.
* text=auto eol=lf
````

#### File: `scripts/build-chat-bundle.sh`

````bash
#!/usr/bin/env bash
# Build chat/bundle.md: one file that gives a chat app with no file access
# the kitchen files, the skills, the method pages, and the templates.
#
# Usage: scripts/build-chat-bundle.sh [--check]
#
# The bundle holds every regular file whose name ends in .md under four
# places, in this order: kitchen/, the skill folders .agents/skills/<name>/,
# method/, and templates/. Inside each place the files come in the byte
# order of their paths. A symbolic link is never followed or bundled.
# Each file is copied as it is, between a line "===== FILE: <path> =====" and
# a line "===== END FILE: <path> =====", so the same files always give the
# same bundle, byte for byte. The bundle holds no date and no commit.
#
# With no option the script writes chat/bundle.md. With --check it writes
# nothing and compares the bundle that is there with the one it would write.
#
# Exit status: 0 the bundle was written, or with --check it is current;
# 1 with --check, the bundle is missing or out of date; 2 the script could
# not run, which never counts as current.
# See chat/README.md.
set -euo pipefail
export LC_ALL=C

USAGE="usage: scripts/build-chat-bundle.sh [--check]"
BUNDLE=chat/bundle.md

fail() {
  echo "build-chat-bundle: $1" >&2
  exit 2
}

check=0
case "$#" in
  0) ;;
  1) [ "$1" = "--check" ] || fail "$USAGE"
     check=1 ;;
  *) fail "$USAGE" ;;
esac

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd) || fail "could not find the repository root"
cd "$root" || fail "could not enter $root"

for place in kitchen .agents/skills method templates; do
  [ -d "$place" ] || fail "$place is not a folder of $root"
done

work=$(mktemp -d) || fail "could not make a temporary folder"
trap 'rm -rf "$work"' EXIT

list() {
  find "$@" -type f -name '*.md' -print0 | sort -z >> "$work/paths" ||
    fail "could not list the files under $1"
}
: > "$work/paths"
list kitchen
list .agents/skills -mindepth 2
list method
list templates

paths=()
while IFS= read -r -d '' path; do
  case "$path" in
    *$'\n'*) fail "a file name holds a line break" ;;
  esac
  found=0
  grep -a -q -E '^===== (END )?FILE: ' "$path" || found=$?
  case "$found" in
    0) fail "$path holds a line that starts like a bundle marker" ;;
    1) ;;
    *) fail "could not read $path" ;;
  esac
  paths+=("$path")
done < "$work/paths"
count=${#paths[@]}
[ "$count" -gt 0 ] || fail "found no file to bundle"

{
  printf '%s\n' "# Chef Council chat bundle"
  printf '\n'
  printf '%s\n' "This file is generated by \`scripts/build-chat-bundle.sh\`. Do not edit it: change the file it came from and run the script again."
  printf '\n'
  printf '%s\n' "It holds the kitchen files, the skills, the method pages, and the templates of one Chef Council repository, for a chat app that cannot read the repository. Each file below starts at a line \`===== FILE: <path> =====\` and ends at a line \`===== END FILE: <path> =====\`. When an instruction names a path, read the file between those two lines. A link inside a file points to a path in the repository, and a path that is not listed here is a file you have not been given."
  printf '\n'
  printf '%s\n' "## Files"
  printf '\n'
  for path in "${paths[@]}"; do
    printf -- '- %s\n' "$path"
  done
  for path in "${paths[@]}"; do
    printf '\n'
    printf '===== FILE: %s =====\n' "$path"
    cat "$path" || fail "could not read $path"
    if [ -s "$path" ] && [ "$(tail -c 1 "$path" | od -An -tx1 | tr -d ' \n')" != "0a" ]; then
      printf '\n'
    fi
    printf '===== END FILE: %s =====\n' "$path"
  done
} > "$work/bundle"

if [ "$check" -eq 1 ]; then
  if [ ! -f "$BUNDLE" ]; then
    echo "chat bundle is missing: run scripts/build-chat-bundle.sh"
    exit 1
  fi
  if ! cmp -s "$work/bundle" "$BUNDLE"; then
    echo "chat bundle is out of date: run scripts/build-chat-bundle.sh"
    exit 1
  fi
  echo "chat bundle checked: $count files"
  exit 0
fi

mkdir -p chat || fail "could not make the chat folder"
cp "$work/bundle" "$BUNDLE" || fail "could not write $BUNDLE"
echo "chat bundle written: $count files"
````

#### File: `chat/project-instructions.md`

````markdown
# Chef Council: instructions for a chat app

You are a cooking collaborator working from one Chef Council repository: a council of cooking lenses that develops and pressure-tests recipes, plain-text recipe cards and cook logs, and an independent editor check on every recipe change. The person you are working with is called the cook.

## What you have

- You cannot read or write the repository's files, and you cannot run a command. Say so once, the first time it matters.
- Your knowledge holds the chat bundle, a file named `bundle.md`. It holds the kitchen files, the skills, the method pages, and the templates. Each file in it sits between a line `===== FILE: <path> =====` and a line `===== END FILE: <path> =====`. When these instructions or a skill name a path, read that file in the bundle.
- If you cannot find the bundle, say so and ask the cook to upload `chat/bundle.md`. Do not work from what you suppose it holds.
- The bundle is a copy made when the cook last built it. When the cook pastes or uploads a newer copy of a file, the newer copy wins.
- Recipe cards, the recipe index, and cook logs are not in the bundle. Before you change a recipe or cook from it, ask the cook to paste the saved card and its most recent cook log, unless they are already in this chat or in your knowledge. Never rebuild a card from memory.
- When a file or a skill tells you to run a script, give the cook the exact command and say that you did not run it.

## Read in this order

1. `kitchen/README.md`, then `kitchen/profile.md`, `kitchen/equipment.md`, and `kitchen/pantry.md`. A file whose `filled_in` line is not exactly `filled_in: yes` is a blank template: ask the cook, and never treat a placeholder as a fact.
2. `kitchen/council.md`: the lenses, what each is for, its scope, and where it can mislead. Each lens has a record in `kitchen/vetting/`.
3. The skill for the job, in full, before acting on it:
   - `.agents/skills/chef-council/SKILL.md`: develop, adapt, pressure-test, cook live from, troubleshoot, or research a recipe, and run the first-run kitchen interview when the profile is blank.
   - `.agents/skills/recipe-codify/SKILL.md`: turn an approved recipe into a card, change a saved card, or start a separate version.
   - `.agents/skills/cook-log/SKILL.md`: log what happened when the cook reports back.
   - `.agents/skills/recipe-editor/SKILL.md`: only in the editor's chat, described below.
4. The saved card and its most recent cook log, pasted by the cook, before changing that recipe or cooking from it.

## Rules that are easy to get wrong

- **The latest correction beats a saved card.** When the cook's most recent explicit instruction disagrees with a saved card, name the conflict, follow the correction, and return the updated card. The standing corrections in `kitchen/profile.md` beat a card in the same way.
- **Status is several separate facts:** how far the recipe has been developed, whether it has been cooked and how that went, whether the card is saved in the repository, and whether any copy outside the repository is up to date. Writing a card does not make it cooked, and cooking it once does not make it a house recipe. Never raise any of these without a logged cook or the cook saying so. `method/status-and-versions.md` is the full rule.
- **Do not invent** quantities, times, temperatures, cook outcomes, allergies, equipment limits, or sources. When a number is missing, say so on the card.
- **Keep the old version when testing a new one.** `method/status-and-versions.md` says when a change is a new version of the same card and when it is a new card.
- **The council is a set of lenses, not people.** Attribute advice to a lens, written `<Name>-style lens`. No real chef has reviewed, approved, endorsed, or contributed to anything here, so never say or imply one did, and never invent a quote. A lens argues only from the tendencies in its vetting record and only inside its scope. Asked to add a name to the council, follow `kitchen/council-vetting.md`. If you cannot open web pages, you cannot vet a name: say so, and seat no one.
- **Food safety is a constraint, not a lens's opinion.** A safety number comes from a cited standard. When `higher_risk_diners` in `kitchen/profile.md` is `yes`, use the stricter endpoints; when it is `unknown`, ask before giving one.
- **Copy no third-party recipe text:** no ingredient lists, methods, or headnotes from any publisher. Credit a source by title and link only when you actually read it in this chat.

## Saving

You cannot save anything, so never say or imply that a file was saved, committed, synced, or checked. When the cook asks you to save, or a skill tells you to write a file:

1. For each file, write a line `File to save: <path>`, then the complete file inside a fence of four backticks. Give the whole file every time, never a fragment or a list of changes.
2. After the last file, give any command the skill says to run next, such as `python3 scripts/build-index.py`.
3. End with this line, exactly: `Nothing was saved: I cannot write files here.`

A skill may ask for its own headings in a reply. Keep them: the `File to save:` blocks go under the heading that reports the files, and the line of step 3 is still the last line of the reply.

A kitchen file changed this way also changes the bundle. Tell the cook to run `scripts/build-chat-bundle.sh` after saving it and to upload the new `chat/bundle.md` in place of the old one.

## The editor check

Every recipe card that is added or changed gets an independent check before it is committed, and the writer of a card never checks it. In the chat where you wrote or changed a card:

- Do not check the card, grade it, or write an editor report, even when asked. Say that the check needs a new chat.
- Point the cook to "The editor prompt for a new chat" in `method/recipe-qc.md`, which gives the prompt and the things to paste after it.

When a chat opens with a message saying that you are an independent recipe editor, you are the editor for that whole chat. Follow that message and the `recipe-editor` skill only. Do no other work in that chat, and change nothing on the card.

## Copies outside the repository

A copy of a card in a notes app is made by an agent that works in the repository, under the sync contract in the repository's `adapters/README.md`. That contract needs the repository's sync map and editor reports, which you cannot read or write. So do not create or update a copy from this chat, even when the chat app gives you a tool that could. Say so, and never say that a card was mirrored or synced.

## What stays with the cook

Choosing a direction, the scope of a save, what was cooked and how it tasted, promoting a recipe to a house recipe, and merging a change into the repository.
````

#### File: `chat/README.md`

````markdown
# Chef Council in a chat app

Use this folder when your assistant is a chat app that cannot read this repository: a project in Claude or ChatGPT, a Gem in Gemini, or a chat in Muse. You get the same council, the same rules, and the same editor check. What changes is that you carry the files in and out by hand, because the chat cannot save anything.

## What is here

- [`project-instructions.md`](project-instructions.md) is the text you paste into the app's instructions field. It is the one set of instructions for every chat app. The steps on this page only say where to paste it: they add nothing to it and change nothing in it. To change how your chat behaves, edit that file first, then paste it again everywhere you use it. It stays under 8,000 characters so that it fits an instructions field, and a test fails when it does not.
- [`bundle.md`](bundle.md) is the knowledge file you upload. It holds your kitchen files, the skills, the method pages, and the templates in one file. It is generated, so never edit it: run `scripts/build-chat-bundle.sh` from the repository root, which prints `chat bundle written:` and the number of files.

Your recipe cards and cook logs are not in the bundle, because they change more often than the rest. Upload or paste the ones you want the chat to work on.

## Set it up

These steps are the same in every app. The table below says what each app calls the two places.

1. Fill in the three files in [`kitchen/`](../kitchen/README.md), or leave them blank and let the chat interview you the first time you use it.
2. From the repository root, run `scripts/build-chat-bundle.sh`.
3. In the chat app, create a project, or whatever the app calls a saved set of instructions with files.
4. Paste the whole of `project-instructions.md` into the instructions field, from its first line to its last.
5. Upload `chat/bundle.md` as a knowledge file.
6. For each job, paste the recipe card and its most recent cook log into the chat. You can upload them as files instead, but an uploaded copy goes out of date the moment the card changes.
7. Try it. Ask it to save a card for a recipe you make up on the spot. A chat that is set up correctly returns the complete file under a line that starts `File to save:` and ends with the line `Nothing was saved: I cannot write files here.`

| App | Where the instructions go | Where the bundle goes | How this was checked |
|---|---|---|---|
| Claude Projects | "Set project instructions" on the project's page | The project knowledge base, with its "+" button | Read on 2026-11-19: [How can I create and manage projects?](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects) |
| ChatGPT Projects | The project's instructions | The project's files | Not checked. The help page could not be read on 2026-11-19, so these names may be wrong. |
| Gemini Gems | The instructions box of a new Gem | "Knowledge", then "Add files" | Read on 2026-11-19: [Tips for creating custom Gems](https://support.google.com/gemini/answer/15235603) |
| Muse | Not known | Not known | Not checked. No official page describing instructions or knowledge files for a Muse chat was found on 2026-11-19. Use the fallback below. |

Apps rename their screens. When a name above is not there, look for the place the app keeps instructions that apply to every chat, and the place it keeps files that every chat can read.

**The fallback, for an app with neither place.** Start a chat, paste `project-instructions.md` as your first message, and attach `chat/bundle.md` to it. If the app takes no file, paste from the bundle the files the job needs. Each one sits between a line that starts `===== FILE:` and a line that starts `===== END FILE:`. Say which files you left out, because the chat is told to treat a missing file as one it was not given.

## Keep it current

- After you change anything in `kitchen/`, a skill, `method/`, or `templates/`, run `scripts/build-chat-bundle.sh` again and upload the new `bundle.md` in place of the old one. The chat only knows the copy you uploaded.
- `scripts/build-chat-bundle.sh --check` prints `chat bundle checked:` when `bundle.md` matches the files it is built from, and `chat bundle is out of date:` when it does not. CI runs it on every pull request, so a change to one of those files without a rebuilt bundle fails the checks.
- After you change `project-instructions.md`, paste it again.
- If you uploaded a recipe card or a cook log as a file, replace it after every change to it, or remove it and paste the current one when you need it. The chat trusts the copy it has.

## Saving what the chat writes

The chat cannot write to your repository. When you ask it to save, it returns each file whole, under a line `File to save:` with the path, and tells you that nothing was saved. Saving is yours:

1. Put each file at the path given, replacing the whole file if it exists. Save it with plain line feeds, which some editors call Unix line endings. Git commits a card with line feeds, so a hash taken from a card saved with Windows line endings stops matching once the card is committed.
2. Run any command the chat gives after the files, such as `python3 scripts/build-index.py`.
3. Have the card checked, as the next section says.
4. Commit on a branch and open a pull request, as [`AGENTS.md`](../AGENTS.md) says under "Making changes".

A source packet goes under `.sources/`, which git ignores. Keep it there, and never commit one.

## The editor check, in a new chat

Every card that is added or changed is checked by an editor that did not write it. In a chat app the editor is a new chat: not the chat that wrote the card, and not a later message in it.

Open a new chat and follow [The editor prompt for a new chat](../method/recipe-qc.md#the-editor-prompt-for-a-new-chat). That section holds the prompt, the things to paste after it, and what to save from the reply. A new chat in the same project works: the instructions tell a chat that opens with that prompt to act as the editor and nothing else.

One of the things you paste is the card's hash line, which comes from a command. That step needs a copy of the repository and a terminal. Without them the report has no hash, and the editor gate in CI fails for that change, which is accurate: nothing shows which bytes were checked.

## What a chat cannot do

- Run a script. It gives you the command and says it did not run it. The index, the card linter, and the editor gate run in your terminal or in CI.
- See a file you changed after you built the bundle, until you upload a new one or paste the file.
- Open a web page, unless your app gives it a browsing tool. Without one it cannot research a source or vet a new name for the council, and it is told to say so.
- Copy a card to a notes app. That is a job for an agent that works in the repository, under [`adapters/README.md`](../adapters/README.md).
````

#### File: `adapters/README.md`

````markdown
# Adapters: copies outside the repository

The repository is the home of every recipe card. An adapter is a page that tells an agent how to keep a copy of a card somewhere else, such as a notes app you read from while you cook. Copies are optional, and nothing else in this repository depends on one.

This page is the sync contract, which every adapter follows. [`mem.md`](mem.md) is one worked example, and [`sync-map.md`](sync-map.md) is where an agent records what it copied.

## When a copy is made

- Only when the cook asks for one or calls the recipe final. [`method/status-and-versions.md`](../method/status-and-versions.md) holds that rule, under "Saved and mirrored".
- Only from the card file as it stands in the repository, never from a draft in a conversation.
- Only when the card's latest editor report passes for the card as it now stands: the newest report in the card's folder under `qc/` reads `VERDICT: PASS` or `VERDICT: PASS WITH NOTES`, and its `Card-SHA256:` line is the line `scripts/check-qc.sh --hash` prints for the card. A card with a failed check, an old check, or no check is not copied.
- Only cards. A cook log, a source packet, and an editor report stay in the repository.

## What is copied

The copy is the card from its title line (the line that starts with `# `) to its end, unchanged. The block of fields above the title is for scripts and is left out. The copy's title is the card's title, with nothing added to it.

A destination has a short lowercase name, such as `mem`. That name is what the card's `mirrors` line and the sync map use.

## The sync contract

An agent follows these six rules in this order, for one destination at a time. A copy is found when its title is exactly the card's title. A note that only resembles it is not the copy, and a copy in the trash is still a copy.

1. **Search before creating.** Look in the sync map for a row with this card and this destination. If there is none, search the destination for a copy by the card's title. One copy found, either way, means this is an update of that copy. A copy found only by the search gets its row in the sync map first, with `unknown` as its version, `never` as its read-back, and the state `unverified`. Several found means stop: list them for the cook and ask which one is the copy. Create a new copy only when both looks find nothing.
2. **Store the external ID in the sync map.** As soon as the destination returns the ID of a new copy, write the row in `sync-map.md`, before doing anything else. An ID that is only in a conversation is lost when the conversation ends, and the next sync then creates a second copy.
3. **Read the live version before updating.** Fetch the copy as it stands now, by its ID. If the destination gives a version with it, the update uses that version. Compare it with the card as it was at the version in the row, which git's history of the card file holds. Anything in the copy that is not in that version was put there by hand: show it to the cook and ask before replacing it. When the row's version is `unknown`, show every difference from the current card and ask. If the copy is gone or in the trash, say so and ask. Do not create another without being asked.
4. **Never create a duplicate as a retry.** When a create or an update fails, times out, or returns something you cannot read, find out first whether it landed: read by the ID if you have one, and search if you do not. Retry only what did not land. A search that finds nothing does not prove that a create failed, because a search can miss a new copy: tell the cook what happened and ask before creating again. An update is retried as an update of the same ID, and never as a new copy.
5. **Read back before claiming success.** After a create or an update, fetch the copy by its ID and compare it with the card: every ingredient with its amount, every step, every time and temperature. Formatting that the destination changed is not a difference. A missing or altered line is, and it makes the copy `failed`. A reply that says the write worked is not a read-back, and neither is an ID. Say "synced" only after this comparison.
6. **Report each destination separately.** Say what happened in the repository, in the words of `method/status-and-versions.md`, and then give one line for each destination: created, updated, unchanged, failed with the reason, or not attempted with the reason. Never fold them into one "saved". The report comes last, so that it says what the read-back found.

After a read-back that matches:

- Set the row in the sync map: the version copied, today's date, and the state `current`.
- If the card's `mirrors` line does not name the destination yet, add it by the `recipe-codify` skill. That changes the card, so the card gets its editor check like any other change. It does not change the card's version, so the copy is not stale.

## The sync map

[`sync-map.md`](sync-map.md) has one row for each copy: the card, the destination, the ID the destination gave, the version last copied, the date it was last read back, and a state.

| State | Meaning |
|---|---|
| `current` | The copy was read back and matched the card at the version in the row. |
| `stale` | The card has changed what a cook would do since the version in the row. |
| `unverified` | A copy was written and has not been read back, or the read-back could not be done. |
| `failed` | The last write did not land, or the read-back did not match. |

A row whose version is older than the card's version is stale, whatever its State cell says. The next sync corrects the cell.

The sync map is committed with your cards, so on a public fork it is public. Write only the ID in it: never a password, a token, a key, or a link that carries one. An ID is usually not a secret, but check how your app treats one: if knowing the ID is enough to open the copy, it is a secret. If you would not publish it, keep your fork private.

## What an adapter never does

- Create a copy to see whether a copy exists.
- Say a copy was made, updated, or checked when that step did not run and return a result.
- Write an account's ID, link, or folder name into a card. The card's `mirrors` line names destinations only.
- Change the title or the text of the card on the way out.
- Change the repository's default branch directly. The row in the sync map and the `mirrors` line travel on a branch and a pull request, like any change.

## Adding an adapter

Copy `mem.md` to `adapters/<destination>.md` and rewrite each section for the app: how to search, how to read, how to create, how to update, and how to read back. Put in no ID, link, or folder name from your account. If the app cannot do one of the six rules, such as reading a copy back, say so on the page. The state for that destination then never gets past `unverified`.
````

#### File: `adapters/sync-map.md`

````markdown
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
````

#### File: `adapters/mem.md`

````markdown
# Adapter: Mem

A worked example of the [sync contract](README.md) for Mem, a notes app. It holds no ID, link, or collection name from any account, and yours do not belong in it either: an ID goes in [`sync-map.md`](sync-map.md) and nowhere else.

This repository is not affiliated with Mem. The tool names below are the ones the Mem connector offered to an agent when this page was written, read from the connector's own tool list on 2026-11-19. Connectors change. Go by the tool list your agent has, and if a tool named here is gone, find the one that does the same job before you go on.

- **Destination name:** `mem`
- **What a copy is:** one note. Mem takes a note's title from the first line of its content, so the card's title line becomes the note's title, as it is.

## The six rules in Mem

1. **Search before creating.** Look for a `mem` row for the card in the sync map. If there is none, run `search_notes` with the card's title, and look for a note whose title is exactly the card's title. The search is ranked and bounded, so it can miss a note. That is why the sync map comes first.
2. **Store the external ID.** `create_note` returns the new note's ID. Write the sync-map row with that ID and the state `unverified` before the next step.
3. **Read the live version before updating.** `get_note` with the ID returns the note as it stands and its `version`. `update_note` needs that `version`, so an update without a fresh `get_note` is not possible. Compare what `get_note` returned with the card at the version in the row. If the note says it is in the trash, stop and ask the cook.
4. **Never create a duplicate as a retry.** If `create_note` fails or times out, run `search_notes` again. If it still finds nothing, tell the cook and ask before a second `create_note`. If `update_note` is refused, run `get_note` again and start rule 3 over.
5. **Read back before claiming success.** Run `get_note` with the ID after the write and compare the note with the card. A table or a list that is laid out differently is formatting. What counts is that every ingredient, amount, step, time, and temperature is there and unchanged.
6. **Report each destination separately.** One line for the repository and one for `mem`.

`update_note` replaces the whole note. Send the whole card from its title line to its end, never a part of it.

## Collections

A collection is a named group of notes in Mem. Putting recipe notes in one is optional. If the cook wants it, ask which collection, find it with `search_collections`, and add the note with `add_note_to_collection`. Do not create a collection, or choose one, without being asked. Do not write a collection's name or ID into a card or into this page.

## A worked example

The cook says the roasted carrots are final and asks for a copy in Mem. The card is `recipes/sides/roasted-carrots.md` at `v1.1`, merged, and its latest editor report passes.

1. The sync map has no `mem` row for the card. `search_notes` for "Roasted Carrots" finds no note.
2. `create_note` is called with the card from its title line to its end. It returns an ID.
3. The row goes into the sync map at once:

   | Card | Destination | External ID | Version copied | Read back | State |
   |---|---|---|---|---|---|
   | `recipes/sides/roasted-carrots.md` | `mem` | `<the ID Mem returned>` | `v1.1` | `never` | `unverified` |

4. `get_note` with that ID returns the note. Every ingredient, amount, step, time, and temperature matches the card. The row's Read back becomes today's date and its State becomes `current`.
5. The card's `mirrors` line becomes `mirrors: mem` by the `recipe-codify` skill, and the card gets its editor check.
6. The report to the cook has two lines: the repository, with the stage the change has reached, and `mem: created and read back at v1.1`.

Three weeks later the card is at `v1.2`, and the cook asks for the copy to be brought up to date.

1. The sync map has the row, so nothing is searched and nothing is created.
2. `get_note` with the ID returns the note and its `version`. The note has a line the card never had: the cook typed "double the sumac next time" into it. The agent shows the cook that line and asks. The cook says to leave it out of the copy.
3. `update_note` is called with the ID, the `version` from step 2, and the whole card at `v1.2`.
4. `get_note` again, and the comparison matches. The row becomes `v1.2`, today's date, and `current`.
5. The report: the repository unchanged apart from the sync map, and `mem: updated and read back at v1.2`.
````

#### File: `AGENTS.md`

````markdown
# Agent entry point: Chef Council

This repository is a system for cooking with AI agents: a council of cooking lenses that develops and pressure-tests recipes, plain-text recipe cards and cook logs, and an independent editor check on every recipe change.

The person you are working with is called the cook here. If you cannot read or write files in this repository (a chat app, for example), say so once, and when asked to save something return the complete file and its path for the cook to save.

## Read in this order

1. [`kitchen/README.md`](kitchen/README.md), then [`kitchen/profile.md`](kitchen/profile.md), [`kitchen/equipment.md`](kitchen/equipment.md), and [`kitchen/pantry.md`](kitchen/pantry.md): who is being cooked for, their constraints and standing corrections, the equipment, and a dated pantry snapshot. A file whose front matter says `filled_in: no` is still a blank template: ask the cook, and never treat a placeholder as a fact.
2. [`kitchen/council.md`](kitchen/council.md): the lenses on the council, what each one is for, its scope, and where it can mislead. Each lens has a vetting record in `kitchen/vetting/`, and [`kitchen/council-vetting.md`](kitchen/council-vetting.md) is the rule for seating one.
3. The skill for the job, from [Skills](#skills) below. Read its `SKILL.md` in full before acting on it.
4. The saved recipe card, listed in [`recipes/INDEX.md`](recipes/INDEX.md), and its most recent cook log in `cook-logs/`, before changing that recipe or cooking from it.

## Rules that are easy to get wrong

- **The latest correction beats a saved card.** When the cook's most recent explicit instruction disagrees with a saved card, name the conflict, follow the correction, and update the card. The standing corrections in `kitchen/profile.md` beat a card in the same way.
- **Status is several separate facts:** how far the recipe has been developed, whether it has been cooked and how that went, whether the card is saved in the repository, and whether any copy outside the repository is up to date. Writing a card does not make it cooked, and cooking it once does not make it a house recipe. Never raise any of these without a logged cook or the cook saying so. [`method/status-and-versions.md`](method/status-and-versions.md) is the full rule, with the version table.
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
10. **Mirror, on request only.** Copy a card to a notes app only when the cook asks or calls the recipe final, by [`adapters/README.md`](adapters/README.md).
11. **Promote.** Only the cook calls a recipe a house recipe.

What stays with the cook: choosing a direction, the scope of a save, what was cooked and how it tasted, promoting a recipe, and the merge.

## Skills

Skills live in `.agents/skills/<name>/`, and Claude Code finds them through the links in `.claude/skills/`. If your harness did not load a skill on its own, open the path given here and follow it. [`.agents/skills/README.md`](.agents/skills/README.md) explains how a skill is added.

- `chef-council`: [`.agents/skills/chef-council/SKILL.md`](.agents/skills/chef-council/SKILL.md). Use it to develop, adapt, pressure-test, cook live from, troubleshoot, or research a recipe with the council, to hand a finished recipe off to be saved, and to run the first-run kitchen interview when `kitchen/profile.md` is blank.
- `recipe-codify`: [`.agents/skills/recipe-codify/SKILL.md`](.agents/skills/recipe-codify/SKILL.md). Use it to save an approved recipe as a card, change a saved card, or start a separate version to test. It writes the card with its version and an honest status, regenerates the index, and saves the source packet for the editor check.
- `cook-log`: [`.agents/skills/cook-log/SKILL.md`](.agents/skills/cook-log/SKILL.md). Use it when the cook reports back after cooking. It logs what happened in the cook's own words, marks everything else as not reported, and says what the card needs next.
- `recipe-editor`: [`.agents/skills/recipe-editor/SKILL.md`](.agents/skills/recipe-editor/SKILL.md). Use it only in a fresh context that did not write the card, to check a new or changed card against its source packet and write the editor report.

## Making changes

- Work on a branch and open a pull request against `main`, so the checks run before the merge.
- Write commit subjects in the imperative mood, such as `Add the roasted carrots card v1.0`.
- Before opening a pull request, run the checks CI runs:
  - `python3 scripts/check-skills.py`: every skill has its link and its line above.
  - `python3 scripts/check-council.py`: the council roster matches the vetting records.
  - `python3 -m unittest discover -s tests -v`: the tests for the scripts.
  - `scripts/secret-scan.sh`: gitleaks over the full history.
  - `python3 scripts/lint-cards.py`: the cards are well formed and the index is current.
  - `scripts/check-qc.sh`: each changed card has a current passing editor report.
  - `scripts/build-chat-bundle.sh --check`: `chat/bundle.md` is current.
- Never commit a secret, a credential, or a token. Source packets, the exact text a cook approved, stay in the git-ignored `.sources/` folder.
- Everything committed to a public fork is public, including `kitchen/` and the history. Keep out anything the cook would not publish.
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
      - name: Check the chat bundle is current
        run: scripts/build-chat-bundle.sh --check
      - name: Run the tests
        run: python3 -m unittest discover -s tests -v
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

#### Edit: `.agents/spec-profile.md`

##### Before

````text
which never counts as
    clean), and
    `scripts/secret-scan.sh`
````

##### After

````text
which never counts as
    clean), `scripts/build-chat-bundle.sh --check` (prints `chat bundle
    checked: <N> files` and exits 0, exit 1 when `chat/bundle.md` is missing
    or out of date, and exit 2 when the check could not run, which never
    counts as clean), and
    `scripts/secret-scan.sh`
````
