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
