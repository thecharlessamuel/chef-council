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
