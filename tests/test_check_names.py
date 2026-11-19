"""Tests for scripts/check-names.py, observed through its output and exit status.

Each test builds a small git repository in a temporary directory. Its first
commit, the base, holds a roster and two vetting records that name invented
people, titles, outlets, and sites. Its second commit removes them, as the
real repository did. The script is then run with --base on files a test
writes. No name in this file belongs to a real cook, publisher, or outlet.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "check-names.py")
ALLOWLIST = "scripts/names-allowlist.txt"

ROSTER = """# The council

## Core lenses

### [Zed-style lens](vetting/zed-quillfeather.md)

- **Job:** Heat and timing
- **Typical question:** What changes the result?
- **Scope:** Savory cooking
- **Where it can mislead:** It assumes what the works kitchen has tried, and a harbor is far away.

### [Morrow Kitchen Works-style lens](vetting/morrow-kitchen-works.md)

- **Job:** Reliability
- **Typical question:** Where will it fail?
- **Scope:** Any recipe
- **Where it can mislead:** It can add steps.
"""

RECORD_ONE = """---
lens: Zed-style lens
name: Zed Quillfeather
seat: core
---

# Zed-style lens

## Official site

- Zed Quillfeather: https://www.ZedQuillfeather.example/about (checked 2026-01-01). Her own site.

## Published work

- *The Copper Ladle: Notes* (Tidewater House, 2020): https://tidewater.example/ladle (checked 2026-01-01). A book.
- *Brine* (Tidewater House, 2022): https://tidewater.example/brine (checked 2026-01-01). A second book.
- *Simmer* (Tidewater House, 2023): https://tidewater.example/simmer (checked 2026-01-01). A third book, and things simmer in it.

## Independent sources

- *A review* (Harbor Gazette, 2021): https://harborgazette.example/review (checked 2026-01-01). Praise from Odalys Brindlemoor.

## Access notes

The Harbor Gazette page loaded. A Lanternfish review was not opened. Vexley's listing refused to load.
Not cited: a Korvath profile.
Seen: The Kitchen Review Works page.
"""

RECORD_TWO = """---
lens: Morrow Kitchen Works-style lens
name: Morrow Kitchen Works / Dov Tárn / Al Bo
seat: core
---

# Morrow Kitchen Works-style lens

## Official site

- Morrow Kitchen Works: https://morrowkitchenworks.example/ (checked 2026-01-01). The publisher's site.

## Access notes

Searched: Dov Tarn Morrow Kitchen Works host
"""

CLEAN = """# The council

Lenses are named for approaches. The works kitchen is ordinary, and so is a harbor.
"""


def git_environment():
    env = dict(os.environ)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    env.update(
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_CONFIG_SYSTEM=os.devnull,
        GIT_AUTHOR_NAME="test",
        GIT_AUTHOR_EMAIL="test@example.invalid",
        GIT_COMMITTER_NAME="test",
        GIT_COMMITTER_EMAIL="test@example.invalid",
    )
    return env


class CheckNamesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = os.path.realpath(self._tmp.name)
        self.root = os.path.join(self.tmp, "repo")
        os.makedirs(self.root)
        self.env = git_environment()
        self.git("init", "-q", "-b", "main")
        self.write("kitchen/council.md", ROSTER)
        self.write("kitchen/vetting/zed-quillfeather.md", RECORD_ONE)
        self.write("kitchen/vetting/morrow-kitchen-works.md", RECORD_TWO)
        self.write(".gitignore", "ignored/\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Base")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.git("rm", "-q", "-r", "kitchen/vetting")
        self.write("kitchen/council.md", CLEAN)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "Remove the names")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", self.root, *args],
            capture_output=True, text=True, check=True, env=self.env,
        ).stdout

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def run_script(self, *args, base=None, root=None):
        command = [sys.executable, SCRIPT, *args]
        if base is not False:
            command += ["--base", base or self.base]
        command.append(root or self.root)
        return subprocess.run(
            command, capture_output=True, text=True, check=False, env=self.env
        )

    def hits(self, text, path="notes.md", show=False):
        """Write one file and return the lines the script prints about it."""
        self.write(path, text)
        result = self.run_script(*(["--show"] if show else []))
        self.assertEqual(result.stderr, "")
        lines = result.stdout.splitlines()
        if result.returncode == 0:
            self.assertRegex(lines[-1], r"\Anames checked: \d+ files, \d+ terms\Z")
            self.assertEqual(len(lines), 1)
            return []
        self.assertEqual(result.returncode, 1)
        self.assertEqual(lines[-1], "names check: %d hit(s)" % (len(lines) - 1))
        return lines[:-1]

    # The passing tree.

    def test_tree_without_the_names_passes(self):
        result = self.run_script()
        self.assertEqual(result.stderr, "")
        self.assertRegex(result.stdout, r"\Anames checked: 2 files, \d+ terms\n\Z")
        self.assertEqual(result.returncode, 0)

    def test_the_base_commit_itself_fails(self):
        self.git("checkout", "-q", self.base)
        result = self.run_script()
        self.assertEqual(result.returncode, 1)
        lines = result.stdout.splitlines()
        self.assertIn("kitchen/council.md:5: name", lines)
        self.assertIn("kitchen/vetting/zed-quillfeather.md: name in the path", lines)
        self.assertIn("kitchen/vetting/morrow-kitchen-works.md: name in the path", lines)

    def test_ordinary_text_passes(self):
        self.assertEqual(
            self.hits("Roast the carrots. Review the kitchen. Things simmer. About the site.\n"),
            [],
        )

    # Names.

    def test_lens_name_fails(self):
        self.assertEqual(self.hits("Ask the Zed-style lens.\n"), ["notes.md:1: name"])

    def test_name_fails_in_any_letter_case(self):
        self.assertEqual(
            self.hits("first\nby ZED QUILLFEATHER\nby dov tarn\n"),
            ["notes.md:2: name", "notes.md:3: name"],
        )

    def test_surname_alone_fails(self):
        self.assertEqual(self.hits("Quillfeather's trick.\n"), ["notes.md:1: name"])

    def test_each_part_of_a_name_line_is_a_name(self):
        self.assertEqual(self.hits("by Al Bo\n"), ["notes.md:1: name"])

    def test_name_inside_a_longer_word_passes(self):
        self.assertEqual(self.hits("The quillfeathers and a tarnish.\n"), [])

    def test_three_letter_name_word_is_matched_exactly(self):
        self.assertEqual(self.hits("Dov says so.\n"), ["notes.md:1: name"])
        self.assertEqual(self.hits("a dov and a zed\n"), ["notes.md:1: name"])
        self.assertEqual(self.hits("a dov\n"), [])

    def test_name_word_the_roster_uses_as_an_ordinary_word_passes(self):
        self.assertEqual(self.hits("The Works Kitchen is busy.\n"), [])
        self.assertEqual(self.hits("Morrow is busy.\n"), ["notes.md:1: name"])

    def test_initials_of_a_long_name_fail(self):
        self.assertEqual(self.hits("(MKW Method)\n"), ["notes.md:1: name"])
        self.assertEqual(self.hits("an mkw method\n"), [])

    def test_accents_and_curly_apostrophes_are_folded(self):
        self.assertEqual(self.hits("Tarn wrote it.\n"), ["notes.md:1: name"])
        self.assertEqual(self.hits("Tárn wrote it.\n"), ["notes.md:1: name"])
        self.assertEqual(self.hits("Quíllfeather’s book.\n"), ["notes.md:1: name"])

    def test_record_file_name_fails_in_text(self):
        self.assertEqual(
            self.hits("See kitchen/vetting/morrow-kitchen-works.md.\n"), ["notes.md:1: name"]
        )

    def test_record_file_name_fails_in_a_path(self):
        self.assertEqual(
            self.hits("Nothing.\n", path="old/zed-quillfeather.md"),
            ["old/zed-quillfeather.md: name in the path"],
        )

    def test_name_after_a_word_boundary_escape_fails(self):
        self.assertEqual(self.hits("NAMES='\\bquillfeather\\b'\n"), ["notes.md:1: name"])

    def test_name_split_over_two_lines_fails_on_its_first_line(self):
        self.assertEqual(self.hits("one\nMorrow Kitchen\nWorks\n"), ["notes.md:2: name"])

    # Hosts.

    def test_host_fails_anywhere_and_in_any_letter_case(self):
        self.assertEqual(
            self.hits(
                "See https://www.zedquillfeather.example/books.\n"
                "TIDEWATER.EXAMPLE\n"
                "at zedquillfeather.example\n"
            ),
            ["notes.md:1: host", "notes.md:2: host", "notes.md:3: host"],
        )

    def test_other_host_passes(self):
        self.assertEqual(self.hits("See https://example.org/tidewater.\n"), [])

    # Titles.

    def test_title_of_several_words_fails_exactly(self):
        self.assertIn("notes.md:1: title", self.hits("I read The Copper Ladle: Notes.\n"))
        self.assertEqual(self.hits("I own a copper ladle.\n"), [])
        self.assertEqual(self.hits("It was A review.\n"), ["notes.md:1: title"])
        self.assertEqual(self.hits("It was a review.\n"), [])
        self.assertEqual(self.hits("It was A\n  review.\n"), ["notes.md:1: title"])

    def test_one_word_title_fails_in_italics(self):
        self.assertEqual(self.hits("I read *Simmer* twice.\n"), ["notes.md:1: title"])
        self.assertEqual(self.hits("Simmer the stock. **Simmer** it.\n"), [])

    def test_one_word_title_that_is_no_ordinary_word_fails_anywhere(self):
        self.assertEqual(self.hits("Brine the bird.\n"), ["notes.md:1: proper"])
        self.assertEqual(
            self.hits("I read *Brine*.\n"), ["notes.md:1: title", "notes.md:1: proper"]
        )

    # Proper names in the prose of a record.

    def test_run_of_capitalized_words_fails(self):
        self.assertEqual(self.hits("The Harbor Gazette said so.\n"), ["notes.md:1: proper"])
        self.assertEqual(self.hits("Tidewater House printed it.\n"), ["notes.md:1: proper"])

    def test_single_capitalized_word_fails(self):
        self.assertEqual(self.hits("Lanternfish said so.\n"), ["notes.md:1: proper"])
        self.assertEqual(self.hits("Gazette\n"), ["notes.md:1: proper"])
        self.assertEqual(self.hits("a gazette and a lanternfish\n"), [])

    def test_word_written_in_lowercase_in_the_base_passes(self):
        # "Harbor" opens no run alone, and the base roster says "a harbor".
        self.assertEqual(self.hits("Harbor views.\n"), [])

    def test_possessive_and_search_line_words_fail(self):
        self.assertEqual(self.hits("Vexley's page.\n"), ["notes.md:1: proper"])
        self.assertEqual(self.hits("Vexley’s page.\n"), ["notes.md:1: proper"])
        self.assertEqual(self.hits("Vexley wrote.\n"), ["notes.md:1: proper"])
        self.assertEqual(self.hits("Korvath wrote.\n"), ["notes.md:1: proper"])

    def test_run_that_opens_a_sentence_loses_an_ordinary_first_word(self):
        # The base has "Seen: The Kitchen Review Works page." and each of its
        # four capitalized words in lowercase, so only the run can be a hit.
        self.assertEqual(self.hits("In Kitchen Review Works.\n"), ["notes.md:1: proper"])
        self.assertEqual(self.hits("The Kitchen Review. The Works.\n"), [])

    # The allowlist.

    def test_allowlist_allows_a_proper_term(self):
        self.write(ALLOWLIST, "# Ordinary words.\n\nLanternfish\nHarbor Gazette\nGazette\n")
        self.assertEqual(self.hits("Lanternfish, and the Harbor Gazette.\n"), [])

    def test_allowlist_cannot_allow_a_name_a_host_or_a_title(self):
        self.write(ALLOWLIST, "Quillfeather\nzed quillfeather\ntidewater.example\nA review\n*Simmer*\n")
        lines = self.hits("Nothing.\n")
        self.assertEqual(
            lines[:5],
            [
                "%s: line %d: a name, a host, or a title cannot be allowed" % (ALLOWLIST, n)
                for n in (1, 2, 3, 4, 5)
            ],
        )
        # The allowlist is itself a file of the tree, so the names in it are hits.
        self.assertEqual(
            lines[5:],
            [
                "%s:1: name" % ALLOWLIST,
                "%s:2: name" % ALLOWLIST,
                "%s:3: host" % ALLOWLIST,
                "%s:4: title" % ALLOWLIST,
                "%s:5: title" % ALLOWLIST,
            ],
        )

    def test_allowlist_line_that_allows_nothing_fails(self):
        self.write(ALLOWLIST, "Lanternfish\nCarrot\nlanternfish\n")
        self.assertEqual(
            self.hits("Nothing.\n"),
            [
                "%s: line 2: allows nothing this check looks for; remove it" % ALLOWLIST,
                "%s: line 3: allows nothing this check looks for; remove it" % ALLOWLIST,
            ],
        )

    def test_allowlist_that_is_not_text_fails(self):
        os.makedirs(os.path.join(self.root, "scripts"))
        with open(os.path.join(self.root, ALLOWLIST), "wb") as handle:
            handle.write(b"\xff\xfe\n")
        self.assertEqual(
            self.hits("Nothing.\n"), ["%s: cannot be read as UTF-8 text" % ALLOWLIST]
        )

    def test_allowlist_line_that_repeats_fails(self):
        self.write(ALLOWLIST, "Lanternfish\nLanternfish\n")
        self.assertEqual(
            self.hits("Nothing.\n"), ["%s: line 2: repeats an earlier line" % ALLOWLIST]
        )

    # What is printed.

    def test_names_are_printed_only_with_show(self):
        text = "Zed Quillfeather wrote Brine.\nSee tidewater.example now.\n"
        self.write("notes.md", text)
        quiet = self.run_script().stdout
        for secret in ("Zed", "Quillfeather", "Brine", "tidewater"):
            self.assertNotIn(secret, quiet)
        self.assertEqual(
            self.hits(text, show=True),
            [
                "notes.md:1: name: Zed Quillfeather",
                "notes.md:1: proper: Brine",
                "notes.md:2: host: tidewater.example",
            ],
        )

    def test_one_line_for_each_kind_on_a_line(self):
        self.assertEqual(
            self.hits("Quillfeather and Tarn and Morrow.\nTarn.\n"),
            ["notes.md:1: name", "notes.md:2: name"],
        )

    def test_files_are_reported_in_path_order(self):
        self.write("b.md", "Tarn.\n")
        self.assertEqual(self.hits("Tarn.\n", path="a/z.md"), ["a/z.md:1: name", "b.md:1: name"])

    # Which files are read.

    def test_untracked_file_is_read_and_ignored_file_is_not(self):
        self.write("ignored/notes.md", "Quillfeather.\n")
        self.assertEqual(self.hits("Quillfeather.\n", path="new/notes.md"), ["new/notes.md:1: name"])

    def test_file_that_is_not_text_is_skipped_but_its_path_is_checked(self):
        for name in ("data.bin", "tarn.bin"):
            with open(os.path.join(self.root, name), "wb") as handle:
                handle.write(b"\xff\xfe Quillfeather\n")
        self.assertEqual(self.hits("Nothing.\n"), ["tarn.bin: name in the path"])

    def test_symbolic_link_is_not_followed(self):
        outside = os.path.join(self.tmp, "outside.md")
        with open(outside, "w", encoding="utf-8") as handle:
            handle.write("Quillfeather.\n")
        os.symlink(outside, os.path.join(self.root, "link.md"))
        self.assertEqual(self.hits("Nothing.\n"), [])

    # When the check cannot run.

    def cannot_run(self, result, message):
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "check-names: %s\n" % message)
        self.assertEqual(result.returncode, 2)

    def test_missing_base_commit_cannot_run(self):
        missing = "1" * 40
        self.cannot_run(
            self.run_script(base=missing),
            "commit %s is not in this clone; fetch the full history "
            "(git fetch --unshallow)" % missing,
        )

    def test_shallow_clone_cannot_run(self):
        shallow = os.path.join(self.tmp, "shallow")
        subprocess.run(
            ["git", "clone", "-q", "--depth", "1", "file://" + self.root, shallow],
            capture_output=True, check=True, env=self.env,
        )
        self.cannot_run(
            self.run_script(root=shallow),
            "commit %s is not in this clone; fetch the full history "
            "(git fetch --unshallow)" % self.base,
        )

    def test_base_without_a_roster_or_a_record_cannot_run(self):
        head = self.git("rev-parse", "HEAD").strip()
        self.cannot_run(
            self.run_script(base=head),
            "commit %s holds no roster or no vetting record" % head,
        )

    def test_folder_that_is_no_repository_cannot_run(self):
        plain = os.path.join(self.tmp, "plain")
        os.makedirs(plain)
        self.cannot_run(self.run_script(root=plain), "%s is not a git working tree" % plain)

    def test_usage_errors(self):
        usage = "usage: check-names.py [--show] [--base <commit>] [repository-root]\n"
        for args in (["--verbose"], ["--base"], ["one", "two"], ["--base", "", "one"]):
            with self.subTest(args=args):
                result = subprocess.run(
                    [sys.executable, SCRIPT, *args],
                    capture_output=True, text=True, check=False, env=self.env,
                )
                self.assertEqual((result.stdout, result.stderr, result.returncode), ("", usage, 2))

    # This repository.

    def test_this_repository_allows_only_these_ordinary_words(self):
        # A new line in the allowlist is a change to this test, so it is reviewed.
        with open(os.path.join(REPO, ALLOWLIST), encoding="utf-8") as handle:
            lines = handle.read().split("\n")
        self.assertEqual(
            lines,
            [
                "American", "Asian", "Chinese", "Classical", "Classical French",
                "English", "French", "Indian", "Italian", "Korean", "Mediterranean",
                "Mexican", "Mexico", "Middle Eastern", "Nature", "Regional Mexican", "United",
                "",
            ],
        )

    def test_this_repository_holds_no_removed_name(self):
        result = subprocess.run(
            [sys.executable, SCRIPT], capture_output=True, text=True, check=False, env=self.env
        )
        if result.returncode == 2:
            self.skipTest("the base commit is not in this checkout: " + result.stderr.strip())
        self.assertEqual(result.stderr, "")
        self.assertRegex(result.stdout, r"\Anames checked: \d+ files, \d+ terms\n\Z")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
