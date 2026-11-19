"""Tests for scripts/lint-cards.py, observed through its output and its exit status.

Each test builds a repository root in a temporary directory. The index the
linter compares with is written by scripts/build-index.py, which has its own
tests; the stale and missing lines expected here are literals.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "lint-cards.py")
BUILD_INDEX = os.path.join(REPO, "scripts", "build-index.py")
USAGE = "usage: lint-cards.py [repository-root]\n"
STALE = "recipes/INDEX.md is stale: run python3 scripts/build-index.py"
MISSING = "recipes/INDEX.md is missing: run python3 scripts/build-index.py"
NAMES = "lowercase letters, digits, and single hyphens"

CARD = """---
id: roasted-carrots
version: v1.2
status: testing
evidence: cooked-once
category: sides
mirrors: none
---

# Roasted Carrots

- **Version:** v1.2
- **Date:** 2026-11-19
- **Status:** testing
- **Kitchen evidence:** cooked-once
- **Source:** Original.
- **Yield:** Serves 4
- **Time:** 40 minutes

## Equipment

- A rimmed baking sheet.

## Changelog

- v1.2 (2026-11-19): Lowered the oven temperature.
"""


def card(text=CARD, **changes):
    """Return the fixture card with whole lines replaced: key -> new line, or None to drop it."""
    lines = text.split("\n")
    for start, new in changes.items():
        start = start.replace("_", " ")
        found = [number for number, line in enumerate(lines) if line.startswith(start)]
        if not found:
            raise AssertionError("no line starts with %r" % start)
        if new is None:
            del lines[found[0]]
        else:
            lines[found[0]] = new
    return "\n".join(lines)


class LintCardsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

    def write(self, path, text, raw=None):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if raw is not None:
            with open(full, "wb") as handle:
                handle.write(raw)
            return
        with open(full, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)

    def index(self):
        subprocess.run(
            [sys.executable, BUILD_INDEX, self.root], capture_output=True, text=True, check=False
        )

    def lint(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, *(args or (self.root,))],
            capture_output=True,
            text=True,
            check=False,
        )

    def clean(self, cards):
        result = self.lint()
        self.assertEqual(result.stdout, "cards checked: %d\n" % cards)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 0)

    def problems(self, lines):
        result = self.lint()
        self.assertEqual(result.stdout.splitlines(), lines)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 1)

    def one(self, text, *problems, path="recipes/sides/roasted-carrots.md"):
        """Write one card, build the index, and expect exactly these problems for it."""
        self.write(path, text)
        self.index()
        self.problems(["%s: %s" % (path, problem) for problem in problems])

    # Clean repositories.

    def test_clean_card_passes(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.index()
        self.clean(1)

    def test_no_cards_passes_with_zero(self):
        self.index()
        self.clean(0)

    def test_card_without_the_mirrors_line_passes(self):
        self.write("recipes/sides/roasted-carrots.md", card(mirrors=None))
        self.index()
        self.clean(1)

    def test_extra_front_matter_lines_are_allowed(self):
        self.write("recipes/sides/roasted-carrots.md", card(mirrors="mirrors: none\ntags: weeknight"))
        self.index()
        self.clean(1)

    def test_windows_line_endings_are_read(self):
        self.write("recipes/sides/roasted-carrots.md", CARD.replace("\n", "\r\n"))
        self.index()
        self.clean(1)

    def test_only_files_one_folder_down_are_cards(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.write("recipes/notes.md", "not a card\n")
        self.write("recipes/sides/deep/notes.md", "not a card\n")
        self.write("recipes/.drafts/notes.md", "not a card\n")
        self.write("recipes/sides/.notes.md", "not a card\n")
        self.write("recipes/sides/notes.txt", "not a card\n")
        self.write("templates/recipe-card.md", "not a card\n")
        self.index()
        self.clean(1)

    # A card that cannot be read.

    def test_card_that_is_not_utf8(self):
        self.write("recipes/sides/roasted-carrots.md", "", raw=b"---\nid: \xff\n---\n# Carrots\n")
        self.problems(["recipes/sides/roasted-carrots.md: is not UTF-8 text"])

    def test_card_without_front_matter(self):
        self.one("# Roasted Carrots\n", "has no front matter")

    def test_empty_card(self):
        self.write("recipes/sides/roasted-carrots.md", "")
        self.problems(
            [
                "recipes/sides/roasted-carrots.md: has no front matter",
                "recipes/sides/roasted-carrots.md: has no title line",
            ]
        )

    def test_unclosed_front_matter(self):
        self.write("recipes/sides/roasted-carrots.md", "---\nid: roasted-carrots\n\n# Roasted Carrots\n")
        self.problems(["recipes/sides/roasted-carrots.md: front matter is not closed"])

    def test_card_without_a_title(self):
        self.write("recipes/sides/roasted-carrots.md", card(**{"#_Roasted": "Roasted Carrots"}))
        self.problems(["recipes/sides/roasted-carrots.md: has no title line"])

    def test_title_line_with_no_text_does_not_count(self):
        self.write("recipes/sides/roasted-carrots.md", card(**{"#_Roasted": "#  "}))
        self.problems(["recipes/sides/roasted-carrots.md: has no title line"])

    def test_unreadable_card_is_reported_once_and_the_index_is_not_checked(self):
        self.write("recipes/mains/stew.md", "---\nid: stew\n")
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.problems(["recipes/mains/stew.md: front matter is not closed"])

    def test_symbolic_link_card(self):
        self.write("elsewhere/roasted-carrots.md", CARD)
        os.makedirs(os.path.join(self.root, "recipes", "sides"))
        os.symlink(
            os.path.join("..", "..", "elsewhere", "roasted-carrots.md"),
            os.path.join(self.root, "recipes", "sides", "roasted-carrots.md"),
        )
        self.index()
        self.problems(["recipes/sides/roasted-carrots.md: is a symbolic link"])

    def test_symbolic_link_folder(self):
        self.write("elsewhere/roasted-carrots.md", CARD)
        os.makedirs(os.path.join(self.root, "recipes"))
        os.symlink(os.path.join("..", "elsewhere"), os.path.join(self.root, "recipes", "sides"))
        self.index()
        self.problems(["recipes/sides: is a symbolic link"])

    # Front matter.

    def test_missing_front_matter_lines(self):
        self.one(
            card(id=None, version=None, status=None, evidence=None, category=None),
            "front matter has no id line",
            "front matter has no version line",
            "front matter has no status line",
            "front matter has no evidence line",
            "front matter has no category line",
        )

    def test_repeated_front_matter_lines(self):
        self.one(
            card(id="id: roasted-carrots\nid: roasted-carrots", mirrors="mirrors: none\nmirrors: none"),
            "front matter has more than one id line",
            "front matter has more than one mirrors line",
        )

    def test_id_must_be_the_file_name(self):
        self.one(card(id="id: carrots"), "front matter id is carrots, expected the file name roasted-carrots")

    def test_category_must_be_the_folder(self):
        self.one(card(category="category: mains"), "front matter category is mains, expected the folder sides")

    def test_empty_values_are_named(self):
        self.one(
            card(id="id:", status="status: "),
            "front matter id is empty, expected the file name roasted-carrots",
            "front matter status is empty, expected one of draft, reviewed, testing, house, retired",
            "Status line is testing, but the front matter says empty",
        )

    def test_version_form(self):
        for version in ("1.2", "v1", "v1.02", "v0.1", "V1.2", "v1.2.1", "v1.2 "):
            with self.subTest(version=version):
                text = card(version="version: " + version, **{"-_**Version": "- **Version:** " + version.strip()})
                if version.strip() == "v1.2":
                    self.write("recipes/sides/roasted-carrots.md", text)
                    self.index()
                    self.clean(1)
                else:
                    self.one(text, "front matter version is %s, expected the form v1.0" % version)

    def test_version_does_not_roll_over(self):
        text = card(version="version: v1.10", **{"-_**Version": "- **Version:** v1.10"})
        self.write("recipes/sides/roasted-carrots.md", text)
        self.index()
        self.clean(1)

    def test_status_values(self):
        for status in ("draft", "reviewed", "testing", "house", "retired"):
            with self.subTest(status=status):
                text = card(status="status: " + status, **{"-_**Status": "- **Status:** " + status})
                self.write("recipes/sides/roasted-carrots.md", text)
                self.index()
                self.clean(1)
        self.one(
            card(status="status: tested", **{"-_**Status": "- **Status:** tested"}),
            "front matter status is tested, expected one of draft, reviewed, testing, house, retired",
        )

    def test_evidence_values(self):
        for evidence in ("untested", "cooked-once", "repeated", "not-recorded"):
            with self.subTest(evidence=evidence):
                text = card(
                    evidence="evidence: " + evidence,
                    **{"-_**Kitchen": "- **Kitchen evidence:** " + evidence},
                )
                self.write("recipes/sides/roasted-carrots.md", text)
                self.index()
                self.clean(1)
        self.one(
            card(evidence="evidence: cooked once", **{"-_**Kitchen": "- **Kitchen evidence:** cooked once"}),
            "front matter evidence is cooked once, expected one of untested, cooked-once, repeated, not-recorded",
        )

    # Names.

    def test_file_and_folder_names(self):
        for folder, name in (("sides", "Roasted-Carrots"), ("sides", "roasted--carrots"), ("sides", "roasted_carrots"), ("sides", "-carrots")):
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as root:
                    self.root = root
                    self.one(
                        card(id="id: " + name),
                        "file name is not " + NAMES,
                        path="recipes/%s/%s.md" % (folder, name),
                    )
        with tempfile.TemporaryDirectory() as root:
            self.root = root
            self.one(
                card(category="category: Side Dishes"),
                "folder name is not " + NAMES,
                path="recipes/Side Dishes/roasted-carrots.md",
            )

    def test_two_cards_with_one_slug(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.write("recipes/mains/roasted-carrots.md", card(category="category: mains"))
        self.index()
        self.problems(
            [
                "recipes/mains/roasted-carrots.md: slug is also used by recipes/sides/roasted-carrots.md",
                "recipes/sides/roasted-carrots.md: slug is also used by recipes/mains/roasted-carrots.md",
            ]
        )

    # The lines under the title.

    def test_missing_header_lines(self):
        self.one(
            card(
                **{
                    "-_**Version": None,
                    "-_**Date": None,
                    "-_**Status": None,
                    "-_**Kitchen": None,
                    "-_**Source": None,
                    "-_**Yield": None,
                    "-_**Time": None,
                }
            ),
            "has no Version line under the title",
            "has no Date line under the title",
            "has no Status line under the title",
            "has no Kitchen evidence line under the title",
            "has no Source line under the title",
            "has no Yield line under the title",
            "has no Time line under the title",
        )

    def test_repeated_header_line(self):
        self.one(
            card(**{"-_**Yield": "- **Yield:** Serves 4\n- **Yield:** Serves 6"}),
            "has more than one Yield line under the title",
        )

    def test_header_lines_after_the_first_section_do_not_count(self):
        text = card(**{"-_**Time": None}).replace("## Equipment\n", "## Equipment\n\n- **Time:** 40 minutes\n")
        self.one(text, "has no Time line under the title")

    def test_header_must_agree_with_the_front_matter(self):
        self.one(
            card(
                **{
                    "-_**Version": "- **Version:** v1.1",
                    "-_**Status": "- **Status:** house",
                    "-_**Kitchen": "- **Kitchen evidence:** repeated",
                }
            ),
            "Version line is v1.1, but the front matter says v1.2",
            "Status line is house, but the front matter says testing",
            "Kitchen evidence line is repeated, but the front matter says cooked-once",
        )

    def test_date_form(self):
        for date in ("YYYY-MM-DD", "2026-13-01", "2026-02-30", "19 November 2026", "2026-11-19 (updated)", ""):
            with self.subTest(date=date):
                self.one(
                    card(**{"-_**Date": "- **Date:** " + date}),
                    "Date line is %s, expected a date as YYYY-MM-DD" % (date or "empty"),
                )

    def test_empty_source_yield_and_time(self):
        self.one(
            card(**{"-_**Source": "- **Source:**", "-_**Yield": "- **Yield:** ", "-_**Time": "- **Time:**"}),
            "Source line is empty",
            "Yield line is empty",
            "Time line is empty",
        )

    # Links.

    def test_links(self):
        self.write("method/status-and-versions.md", "rules\n")
        self.write("recipes/mains/stew.md", card(id="id: stew", category="category: mains"))
        self.write("cook-logs/roasted-carrots/2026-11-18.md", "log\n")
        text = CARD + (
            "\n## Notes\n\n"
            "- Good: [rules](../../method/status-and-versions.md#versions), [stew](../mains/stew.md), "
            "[logs](../../cook-logs/roasted-carrots/), [top](#equipment), "
            "[a site](https://example.com/a), [mail](mailto:cook@example.com).\n"
            "- Good: [titled](../mains/stew.md \"Stew\"), [angled](<../mains/stew.md>), "
            "[from the root](/method/status-and-versions.md).\n"
            "- Bad: [gone](../mains/gone.md) and [also gone](missing.md#part).\n"
            "- Bad: [titled](titled.md \"A title\"), [angled](<angled.md>), [from the root](/gone-root.md).\n"
            "\n```markdown\n[in a fence](fenced.md)\n```\n"
            "\n~~~~\n[in tildes](tilde.md)\n```\n[still in tildes](tilde-2.md)\n~~~~\n"
            "\n```\n[in a fence closed by a longer one](long.md)\n`````\n"
            "\n[after the fences](after.md)\n"
        )
        self.write("recipes/sides/roasted-carrots.md", text)
        self.index()
        self.problems(
            [
                "recipes/sides/roasted-carrots.md: broken link ../mains/gone.md",
                "recipes/sides/roasted-carrots.md: broken link missing.md",
                "recipes/sides/roasted-carrots.md: broken link titled.md",
                "recipes/sides/roasted-carrots.md: broken link angled.md",
                "recipes/sides/roasted-carrots.md: broken link /gone-root.md",
                "recipes/sides/roasted-carrots.md: broken link after.md",
            ]
        )

    # The index, and several problems at once.

    def test_stale_index(self):
        self.index()
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.problems([STALE])

    def test_missing_index(self):
        self.write("recipes/sides/roasted-carrots.md", CARD)
        self.problems([MISSING])

    def test_problems_come_in_card_order_and_the_index_line_is_last(self):
        self.write("recipes/sides/roasted-carrots.md", card(id="id: carrots"))
        self.write("recipes/mains/stew.md", card(id="id: stew", category="category: sides"))
        self.problems(
            [
                "recipes/mains/stew.md: front matter category is sides, expected the folder mains",
                "recipes/sides/roasted-carrots.md: front matter id is carrots, expected the file name roasted-carrots",
                MISSING,
            ]
        )

    def test_linked_folder_is_reported_in_folder_order(self):
        self.write("elsewhere/roasted-carrots.md", CARD)
        self.write("recipes/mains/stew.md", card(id="id: stew"))
        os.symlink(os.path.join("..", "elsewhere"), os.path.join(self.root, "recipes", "sides"))
        self.index()
        self.problems(
            [
                "recipes/mains/stew.md: front matter category is sides, expected the folder mains",
                "recipes/sides: is a symbolic link",
            ]
        )

    def test_unfilled_template_fails(self):
        with open(os.path.join(REPO, "templates", "recipe-card.md"), encoding="utf-8") as handle:
            template = handle.read()
        self.write("recipes/sides/roasted-carrots.md", template)
        self.index()
        self.problems(
            [
                "recipes/sides/roasted-carrots.md: front matter id is recipe-slug, expected the file name roasted-carrots",
                "recipes/sides/roasted-carrots.md: front matter category is category-folder, expected the folder sides",
                "recipes/sides/roasted-carrots.md: Date line is YYYY-MM-DD, expected a date as YYYY-MM-DD",
                "recipes/sides/roasted-carrots.md: broken link ../method/status-and-versions.md",
            ]
        )

    # Usage, and this repository.

    def test_usage_errors_exit_two(self):
        for args in (["--check"], [self.root, self.root], ["-h"]):
            with self.subTest(args=args):
                result = self.lint(*args)
                self.assertEqual((result.stdout, result.stderr, result.returncode), ("", USAGE, 2))

    def test_root_that_is_not_a_directory_exits_two(self):
        missing = os.path.join(self.root, "no-such-folder")
        result = self.lint(missing)
        self.assertEqual(
            (result.stdout, result.stderr, result.returncode),
            ("", "lint-cards: %s is not a directory\n" % missing, 2),
        )

    def test_this_repository_lints_clean(self):
        result = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, check=False)
        self.assertEqual(result.stderr, "")
        self.assertRegex(result.stdout, r"\Acards checked: [0-9]+\n\Z")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
