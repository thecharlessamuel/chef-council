---
id: L007
date: 2026-11-19
spec: docs/specs/archive/S007-chat-path-and-adapters.md
pr: 30
merged: 2026-11-19
status: active
counts: {decisions: 1, lessons: 1, patterns: 0, surprises: 1}
supersedes: []
---

# Chat path and adapters: two copies of the agent rules, tests that depend on the machine, and a claim check that failed a correct reply

## Decisions

### `AGENTS.md` and `chat/project-instructions.md` are two copies of one rule set, and only S007 says they move together

- **Rationale:** A chat app cannot open `AGENTS.md`, and the bundle leaves
  it out (decision 4), so `chat/project-instructions.md` restates its rules,
  in `AGENTS.md`'s own wording wherever the rule is the same (decision 3).
  This is the one pair of files where L004's rule (state a rule once, refer
  to it from elsewhere) cannot hold: a reference would send the chat to a
  file it cannot read. The two copies differ in one place on purpose. The
  instructions give the `chef-council` skill's full test for a blank kitchen
  file, and `AGENTS.md` keeps the short form (decisions 3 and 18). Decision 3
  says a later spec that changes a rule in `AGENTS.md` changes the same rule
  in the instructions file in the same pull request. The review found that
  no file, test, or CI check in the repository carries that rule (note 6).
  Space is also tight. `AGENTS.md` is 8,156 bytes against the 8,192-byte
  limit S001 set, a limit only spec gates have checked, and S007 cut two
  sentences to fit (decision 15). The instructions file is 6,779
  characters, and a test holds it under 8,000.
- **Changes:** A spec that changes a rule in `AGENTS.md` or in
  `chat/project-instructions.md` (T014's docs and T015's fixes among them)
  changes the same rule in the other file in the same pull request. It
  keeps the one intended difference, and it plans the bytes before it adds
  to `AGENTS.md`.
- **Source:** archived S007, decisions 3, 4, 15, and 18 (lines 218 to 260
  and 474 to 511);
  [review](https://github.com/thecharlessamuel/chef-council/pull/30#issuecomment-7001694358),
  note 6; archived S001, definition of done item 2 (the 8,192-byte limit).

## Lessons

### Two of S007's tests only work on a machine set up like the one that wrote them

- **Context:** `tests/test_line_endings.py` runs `git` in its temporary
  repositories with the caller's whole environment (lines 37 and 66).
  `tests/test_check_qc.py` and `tests/test_install_git_hooks.py` do it
  differently: they drop `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`,
  and point `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` at the null device
  (`tests/test_check_qc.py`, lines 67 to 75). The review reproduced three
  failures. A global `commit.gpgsign=true` with no usable key makes four of
  the five tests error. A global `core.safecrlf=true` makes two error. An
  exported `GIT_DIR`, as inside a git hook, sends the test's `init`,
  `config`, and `commit` to that repository. The harvest reproduced the
  signing case: `FAILED (errors=4)`, while `tests/test_check_qc.py` passed
  under the same config. The second problem is in the locale test. Removing
  `export LC_ALL=C` from `scripts/build-chat-bundle.sh` (line 23) fails only
  `test_bundle_does_not_depend_on_the_locale`, and only through its
  `en_US.UTF-8` row, where the sort order changes. Decision 6 cites the test
  for a name that is not UTF-8 for that line (after L005), but that test
  still passes when the line is removed. The prerequisites require only
  `C.UTF-8`. On a machine without `en_US.UTF-8`, nothing tests the guard and
  the suite still ends `OK`. None of the checks could see either problem.
  Leg 1's scratch-clone build, its 39-mutant probe, the cross-examination,
  and CI all ran with a clean git config and both locales installed.
- **Changes:** A spec that gives a test that runs `git` builds that test's
  environment the way `tests/test_check_qc.py` does and passes it to every
  `git` call. A spec that guards a locale names the test that fails without
  the guard, and its prerequisites require that test's locale. The next
  spec that touches `tests/` fixes `tests/test_line_endings.py` first.
- **Source:**
  [review](https://github.com/thecharlessamuel/chef-council/pull/30#issuecomment-7001694358),
  notes 1 and 4; `tests/test_line_endings.py`, lines 37 and 66;
  `tests/test_check_qc.py`, lines 67 to 75;
  `tests/test_build_chat_bundle.py`, lines 153 to 164 and 257 to 263;
  archived S007, decision 6 and `## Prerequisites` (lines 272 to 296 and
  532 to 535).

## Surprises

### `chatcheck` failed a correct reply, because the denial it requires also reads as a claim

- **Impact:** `chatcheck` flags any line, except the last, that matches its
  claim pattern (`was saved`, `have committed`, and similar). The last line
  the instructions require, `Nothing was saved: I cannot write files
  here.`, matches the same pattern and passes only because of where it sits.
  The review's second chat run returned a reply with every listed property.
  It wrote "Nothing was saved here." on a status line, so `chatcheck`
  printed `line 140 claims a save` and returned 1. Leg 1 had run the helper
  on two correct replies and six broken ones, and neither correct reply
  repeated the denial before its end. Suppose leg 2's run, and then its one
  retry, had worded a status line that way. Decision 17 would then have
  stopped the pipeline with a question asking whether to revise the
  instructions, blaming the deliverable for the checker's false failure.
  Item 9 stands on the executor's run, which passed.
- **Changes:** A spec that checks a fresh writer's reply for claims of a
  save, sync, or check first runs the checker in leg 1 on a correct reply
  that repeats the required denial in other words before the end. Its stop
  question after a second failed run asks whether the checker or the
  deliverable is wrong.
- **Source:**
  [review](https://github.com/thecharlessamuel/chef-council/pull/30#issuecomment-7001694358),
  note 2; archived S007, `#### Helper: chatcheck` (lines 722 to 726 and 774
  to 778), decision 17 (lines 494 to 507), and the chat-run rehearsal
  (lines 894 to 916).
