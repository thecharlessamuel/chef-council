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
