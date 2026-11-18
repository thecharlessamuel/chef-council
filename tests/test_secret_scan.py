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
