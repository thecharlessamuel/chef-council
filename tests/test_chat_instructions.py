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
