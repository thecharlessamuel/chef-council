---
id: L009
date: 2026-11-19
spec: docs/specs/archive/S009-stranger-test.md
pr: 34
merged: 2026-11-19
status: active
counts: {decisions: 0, lessons: 3, patterns: 0, surprises: 1}
supersedes: []
---

# Stranger test: a run pinned to a head that status commits move, a lint line that cannot run, fixes worded for one path, and a pressure-test fix that disagrees with AGENTS.md

## Lessons

### Pinning the second run to the pull request's head collided with the pipeline's own status commits

- **Context:** Decision 7 and definition-of-done item 8 required the pull
  request's `headRefOid` to be the commit the stranger cloned, and said that
  a commit added after the run means the run is made again. But leg 2 pushes
  a commit that sets the spec to `pr-open` after the pull request opens, and
  leg 3 pushes one that sets it to `approved`. Neither changes a file the
  stranger reads. The executor reordered its steps as a declared deviation:
  it opened the pull request, pushed the `pr-open` commit, and only then made
  the run, on `18148f0`. The reviewer's own status commit, `412435d`, then
  moved the head again, and the reviewer read decision 7 as covering only
  commits that change what the stranger clones. So item 8 as written did not
  hold at the merge. S008's executor had already met the same problem for its
  rendered pages and proved it another way: `git diff --quiet` over the
  observed files, from the rendered commit to the head. PR 34 did the same
  from `c125588` to `18148f0`. The profile's artifact locator also requires a
  fresh clone's `HEAD` to equal the pull request's head commit, and the
  review's status commit breaks that every time.
- **Changes:** A spec that pins an observation to a commit (a fresh clone, a
  stranger run, a rendered page) requires the observed files to be unchanged
  from that commit to the pull request's head, checked with `git diff --quiet
  <commit> HEAD -- <paths>`, and does not require the head to equal it.
- **Source:** archived S009, decision 7 (lines 216 to 221) and
  definition-of-done item 8 (lines 132 to 140); PR 34 body, Deviations
  (order of the pull request and the second run) and Artifact locator;
  [review](https://github.com/thecharlessamuel/chef-council/pull/34#issuecomment-7013600381),
  acknowledged deviation 1, cross-examination A1, and "After the status
  commit"; commits `18148f0` and `412435d`; PR 32 body, Artifact locator;
  `.agents/spec-profile.md`, Artifact locator (lines 88 to 90).

### The Wayfinder lint gate, as S008 and S009 word it, runs `/scripts/lint.py`

- **Context:** S008's cross-examination finding 1 wrote the gate with
  `WAYFINDER=<dir>` "written before `python3` on the same command line", and
  S009 copied that into definition-of-done item 5. The shell expands
  `"$WAYFINDER/scripts/lint.py"` before a prefix assignment takes effect. In a
  shell where `WAYFINDER` is not already set, the command therefore runs
  `/scripts/lint.py` and exits 2; the harvest confirmed the expansion. PR 34's
  executor and its reviewer each hit this and ran `WAYFINDER=<dir>; python3
  ...` instead. Neither spec's cross-examiner had a shell to run the line.
  Every spec in this repository carries this gate, because the profile
  requires the lint and the setup file cannot know the skill's directory.
- **Changes:** A spec writes the lint gate as `WAYFINDER=<dir>; python3
  "$WAYFINDER/scripts/lint.py" docs/wayfinder/*/MAP.md; echo $?`, with the
  assignment ended by `;`, and does not copy S008's or S009's wording.
- **Source:** archived S009, definition-of-done item 5 (lines 103 to 107);
  archived S008, definition-of-done item 9 (lines 119 to 123) and
  `## Cross-examination` finding 1 (lines 829 to 831); PR 34 body, Deviations
  (Wayfinder lint invocation);
  [review](https://github.com/thecharlessamuel/chef-council/pull/34#issuecomment-7013600381),
  acknowledged deviation 2 and cross-examination A2.

### Fixes worded for the stranger's one path left gaps one step away, and the byte pins could not see them

- **Context:** Each of the eleven edits answers its trip on the path the
  stranger walked. The spec's gates (hashes, links, and anchors) and leg 1's
  two rehearsals prove the bytes and that path. They do not check the section
  an edit lands in, or the case beside the stranger's. The review left four
  notes for a later spec. First, the hand-off paragraph (`chef-council` skill,
  line 179) now puts two skills' headings in one reply, beside "Do not add
  other headings" (line 80), and it refers to "item 4" by position. Second,
  `method/recipe-qc.md` (line 67) says that before a commit the default gate
  "prints `qc checked: 0`", which is true only for the first card on a branch.
  Third, the bundle rebuild (skill, line 39) is tied to the first-run
  interview, but any later write to a kitchen file makes `chat/bundle.md`
  stale the same way. Fourth, the Troubleshoot preamble (line 133) and its
  item 1 (line 135) both ask for one fact, so they must now change together.
  The review also listed the second run's seven trips, which are recorded
  only in PR 34's body. The review could record these only as notes, because
  the bytes were the spec's.
- **Changes:** Leg 1 of a spec that fixes trips found by a fresh reader
  words each fix for the case its trip is one instance of, and reads it
  against the whole section it lands in before the cross-examination; the
  next spec that edits the `chef-council` skill or `method/recipe-qc.md`
  settles these four notes and reads the second run's trips in PR 34's body.
- **Source:**
  [review](https://github.com/thecharlessamuel/chef-council/pull/34#issuecomment-7013600381),
  "Non-blocking notes for a later spec"; archived S009, decision 10 and the
  `apply` helper (lines 240 to 283 and 383 to 463); PR 34 body,
  `## Stranger runs` (Run 2); `.agents/skills/chef-council/SKILL.md`, lines
  39, 80, 133, 135, and 179; `method/recipe-qc.md`, line 67.

## Surprises

### Making the pressure test an offer turned the first run's guess into a mismatch with `AGENTS.md`

- **Impact:** The first run's R5 was a `guessed` trip: the loop puts a
  pressure test before the cook, and the README path had no place for it.
  Edits 3 and 9 settled it by making the test an offer that the cook takes up
  ("Pressure-test it."). But `AGENTS.md` loop step 4 still says the test
  happens "Before anyone cooks". Decisions 8 and 10 held that no edit changed
  a rule, so the restatement search of decision 9 (after L008) left
  `AGENTS.md` out. Later runs tripped on the same seam: whether the pressure
  test, and with it the cook's approval of a text, is a step or an offer. The
  second rehearsal's R6 was one, the second run's R3 was a `mismatch`, and
  the second run's R5 was another: a text approved before the cook still
  called the recipe uncooked when it was saved after one cook. The review's
  cross-examination raised it (A4) and accepted it as a note, because the
  bytes were the spec's. Another trip was left because `AGENTS.md` had no
  room for the note: the README's "nothing to install" against the secret
  scan's download (second rehearsal R7). It came back as the second run's R6.
  `AGENTS.md` is at 8,156 of 8,192 bytes, so a trip that needs it is now
  settled outside it or not at all.
- **Changes:** A spec that edits a skill or the README treats an edit that
  makes an `AGENTS.md` loop step optional or required as a rule change under
  L007 and searches `AGENTS.md` for it, alongside L008's list; the next spec
  that touches the five-minute path first decides whether the pressure test
  is a loop step or an offer, and makes room in `AGENTS.md` for that answer.
- **Source:** archived S009, `### The first run` (R5), decisions 8, 9, and
  10 (lines 222 to 239 and 275), the `apply` helper's edits 3 and 9 (lines
  397 to 403 and 431 to 435), and the second rehearsal's R6 and R7 (lines 701
  and 702); `AGENTS.md`, line 31; `README.md`, lines 19 and 25; PR 34 body,
  `## Stranger runs` (Run 2, R3, R5, and R6);
  [review](https://github.com/thecharlessamuel/chef-council/pull/34#issuecomment-7013600381),
  cross-examination A4.
