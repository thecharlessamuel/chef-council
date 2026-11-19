"""Tests for the line-ending rule in .gitattributes.

The editor gate hashes a card's committed bytes, and scripts/check-qc.sh --hash
and scripts/build-chat-bundle.sh read the files as they are checked out. The
rule keeps the two the same on a machine whose git would otherwise check text
files out with Windows line endings. Each test builds a repository in a
temporary directory with that setting turned on, and runs git there with an
environment of its own, so that the caller's git settings and an exported
GIT_DIR cannot reach it.
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
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "true")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", self.root, *args], capture_output=True, check=True, env=self.env
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
            env=self.env,
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
