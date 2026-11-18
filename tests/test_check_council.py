"""Tests for scripts/check-council.py, observed through its output and exit status."""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "check-council.py")

ROSTER_HEAD = "# The council\n\nA test roster.\n"

FIELDS = {
    "lens": "Example-style lens",
    "name": "Example Cook",
    "seat": "core",
    "job": "Heat and ingredient function",
    "question": "Which variable changes the result?",
    "verdict": "seat",
    "scope": "Savory technique at home",
    "checked": "2026-11-18",
}
KEYS = ["lens", "name", "seat", "job", "question", "verdict", "scope", "checked"]

SITE = "- Example site: https://example.com/ (checked 2026-11-18). The author's own site.\n"
WORK = (
    "- *First Book* (Example Press, 2015): https://example.com/first (checked 2026-11-18). Technique.\n"
    "- *Second Book* (Example Press, 2022): https://example.com/second (checked 2026-11-18).\n"
    "  A continuation line.\n"
)
SOURCES = "- *A review*: https://example.org/review (checked 2026-11-18). Confirms the method.\n"
SECOND_SOURCE = "- *A profile*: https://example.net/profile (checked 2026-11-18). Describes the books.\n"
SHOWS = "1. Tests one variable at a time.\n2. Explains why a step works.\n3. Writes for home equipment.\n"
MISLEAD = "It can add steps a weeknight cook does not need.\n"
VERDICT = "Seat. The published work covers the job.\n"
NOTES = "Nothing was behind a paywall.\n"

SECTIONS = [
    "Official site",
    "Published work",
    "Independent sources",
    "What the published work shows",
    "Where this lens can mislead",
    "Verdict",
    "Access notes",
]
SECTION_LIST = ", ".join(SECTIONS)


def run(*args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        check=False,
    )


def record(front=None, **changes):
    """Build a record. Field names change the front matter; section names
    (with spaces as underscores) replace a section's text."""
    fields = dict(FIELDS)
    bodies = {
        "Official site": SITE,
        "Published work": WORK,
        "Independent sources": SOURCES,
        "What the published work shows": SHOWS,
        "Where this lens can mislead": MISLEAD,
        "Verdict": VERDICT,
        "Access notes": NOTES,
    }
    for key, value in changes.items():
        if key in fields:
            fields[key] = value
        else:
            bodies[key.replace("_", " ")] = value
    if front is None:
        front = "".join("%s: %s\n" % (key, fields[key]) for key in KEYS)
    text = "---\n%s---\n\n# %s\n" % (front, fields["lens"])
    for name in SECTIONS:
        text += "\n## %s\n\n%s" % (name, bodies[name])
    return text


def entry(slug="example", **changes):
    values = dict(FIELDS, mislead="It can add steps.")
    values.update(changes)
    return (
        "\n### [%(lens)s](vetting/" % values + slug + ".md)\n\n"
        "- **Job:** %(job)s\n"
        "- **Typical question:** %(question)s\n"
        "- **Scope:** %(scope)s\n"
        "- **Where it can mislead:** %(mislead)s\n" % values
    )


def roster(core="", specialists=""):
    return (
        ROSTER_HEAD
        + "\n## Core lenses\n" + core
        + "\n## On-demand specialists\n" + specialists
    )


class CheckCouncilTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name
        self.write("kitchen/council.md", roster(core=entry()))

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def check(self, expected_lines, expected_status):
        result = run(self.root)
        self.assertEqual(result.stdout.splitlines(), expected_lines)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, expected_status)

    def check_record(self, text, *problems):
        """Write the one seated record and expect exactly these problems."""
        self.write("kitchen/vetting/example.md", text)
        if problems:
            self.check(["kitchen/vetting/example.md: %s" % p for p in problems], 1)
        else:
            self.check(["council checked: 1 seated, 1 records"], 0)

    def check_roster(self, text, *problems):
        """Write the roster beside one good record and expect these problems."""
        self.write("kitchen/vetting/example.md", record())
        self.write("kitchen/council.md", text)
        self.check(["kitchen/council.md: %s" % p for p in problems], 1)

    # The passing shapes.

    def test_empty_council_passes(self):
        self.write("kitchen/council.md", roster())
        self.check(["council checked: 0 seated, 0 records"], 0)

    def test_seated_record_passes(self):
        self.check_record(record())

    def test_core_specialist_and_cut_records_pass(self):
        self.write("kitchen/vetting/example.md", record())
        self.write(
            "kitchen/vetting/second-cook.md",
            record(
                lens="Second Cook-style lens",
                seat="specialist",
                verdict="seat narrower",
                scope="Regional home cooking",
            ),
        )
        self.write(
            "kitchen/vetting/third-cook.md",
            record(
                lens="Third Cook-style lens",
                verdict="cut",
                scope="none",
                Published_work="- None found (checked 2026-11-18).\n",
                Independent_sources="- None found (checked 2026-11-18).\n",
                What_the_published_work_shows="Not established.\n",
            ),
        )
        self.write(
            "kitchen/council.md",
            roster(
                core=entry(),
                specialists=entry(
                    "second-cook",
                    lens="Second Cook-style lens",
                    scope="Regional home cooking",
                ),
            ),
        )
        self.check(["council checked: 2 seated, 3 records"], 0)

    def test_no_official_site_passes_with_two_independent_sources(self):
        self.check_record(
            record(
                Official_site="- No official site (checked 2026-11-18).\n",
                Independent_sources=SOURCES + SECOND_SOURCE,
            )
        )

    def test_dot_files_in_the_records_folder_are_ignored(self):
        self.write("kitchen/vetting/.gitkeep", "")
        self.check_record(record())

    def test_this_repository_passes(self):
        result = run()
        self.assertEqual(result.stderr, "")
        self.assertRegex(result.stdout, r"\Acouncil checked: \d+ seated, \d+ records\n\Z")
        self.assertEqual(result.returncode, 0)

    # A malformed record.

    def test_bad_file_name_fails(self):
        self.write("kitchen/vetting/example.md", record())
        self.write("kitchen/vetting/Example_Two.md", record())
        self.check(
            [
                "kitchen/vetting/Example_Two.md: file name is not <slug>.md "
                "with a lowercase, hyphenated slug"
            ],
            1,
        )

    def test_missing_front_matter_fails(self):
        self.check_record("# Example-style lens\n", "front matter is missing")

    def test_unclosed_front_matter_fails(self):
        self.check_record("---\nlens: Example-style lens\n", "front matter is missing")

    def test_front_matter_line_without_a_value_fails(self):
        front = "".join("%s: %s\n" % (key, FIELDS[key]) for key in KEYS)
        self.check_record(
            record(front=front.replace("job: Heat and ingredient function\n", "job:\n")),
            "front matter line 5 is not key: value",
        )

    def test_front_matter_keys_out_of_order_fail(self):
        front = "".join("%s: %s\n" % (key, FIELDS[key]) for key in reversed(KEYS))
        self.check_record(
            record(front=front),
            "front matter keys must be exactly: lens, name, seat, job, question, "
            "verdict, scope, checked",
        )

    def test_missing_front_matter_key_fails(self):
        front = "".join("%s: %s\n" % (key, FIELDS[key]) for key in KEYS[:-1])
        self.check_record(
            record(front=front),
            "front matter keys must be exactly: lens, name, seat, job, question, "
            "verdict, scope, checked",
        )

    def test_value_yaml_reads_as_a_boolean_fails(self):
        self.check_record(
            record(scope="No"), "scope must not be a YAML boolean or null word"
        )

    def test_value_with_colon_space_fails(self):
        self.check_record(
            record(job="Heat: and ingredient function"),
            "job must start with a letter or digit and hold no double quote, "
            "colon-space, or space-hash",
        )

    def test_value_starting_with_a_symbol_fails(self):
        self.check_record(
            record(name="*Example Cook*"),
            "name must start with a letter or digit and hold no double quote, "
            "colon-space, or space-hash",
        )

    def test_lens_without_the_suffix_fails(self):
        self.check_record(record(lens="Example Cook"), "lens must end with -style lens")

    def test_unknown_seat_fails(self):
        self.check_record(record(seat="guest"), "seat must be core or specialist")

    def test_unknown_verdict_fails(self):
        self.check_record(
            record(verdict="replace"), "verdict must be seat, seat narrower, or cut"
        )

    def test_question_without_a_question_mark_fails(self):
        self.check_record(
            record(question="Which variable changes the result"),
            "question must end with a question mark",
        )

    def test_seated_record_with_scope_none_fails(self):
        self.check_record(
            record(scope="none"), "scope must not be none unless the verdict is cut"
        )

    def test_cut_record_with_a_scope_fails(self):
        self.write("kitchen/council.md", roster())
        self.write("kitchen/vetting/example.md", record(verdict="cut"))
        self.check(
            ["kitchen/vetting/example.md: scope must be none when the verdict is cut"], 1
        )

    def test_impossible_date_fails(self):
        self.check_record(
            record(checked="2026-02-30"), "checked must be a date written YYYY-MM-DD"
        )

    def test_missing_section_fails(self):
        text = record().replace("\n## Verdict\n\n" + VERDICT, "")
        self.check_record(text, "sections must be exactly, in order: " + SECTION_LIST)

    def test_extra_section_fails(self):
        self.check_record(
            record() + "\n## Weaknesses\n\nNone.\n",
            "sections must be exactly, in order: " + SECTION_LIST,
        )

    def test_empty_section_fails(self):
        self.check_record(record(Access_notes="\n"), "section Access notes is empty")

    def test_prose_in_a_cited_section_fails(self):
        self.check_record(
            record(Published_work=WORK + "\nAlso well known for a third book.\n"),
            "Published work: every line must be a list item or its indented continuation",
        )

    def test_two_official_sites_fail(self):
        self.check_record(
            record(Official_site=SITE + SITE.replace("example.com/", "example.com/about")),
            "Official site: expected one list item, found 2",
        )

    def test_continuation_before_the_first_item_fails(self):
        self.check_record(
            record(Published_work="  Also a third book, uncited.\n" + WORK),
            "Published work: every line must be a list item or its indented continuation",
        )

    def test_repeated_link_fails(self):
        self.check_record(
            record(Independent_sources=SOURCES + SOURCES),
            "Independent sources: item 2 repeats a link already cited in this record",
        )

    def test_missing_title_fails(self):
        self.check_record(
            record().replace("# Example-style lens\n", ""),
            "the text before the first section must be the title line # <lens> "
            "and nothing else",
        )

    def test_text_beside_the_title_fails(self):
        self.check_record(
            record().replace(
                "# Example-style lens\n", "# Example-style lens\n\nA famous cook.\n"
            ),
            "the text before the first section must be the title line # <lens> "
            "and nothing else",
        )

    def test_prose_beside_the_tendencies_fails(self):
        self.check_record(
            record(What_the_published_work_shows=SHOWS + "\nAlso widely admired.\n"),
            "What the published work shows: a seated lens lists numbered items "
            "and nothing else",
        )

    def test_record_that_is_not_text_fails(self):
        os.makedirs(os.path.join(self.root, "kitchen", "vetting", "example.md"))
        self.check(["kitchen/vetting/example.md: cannot be read as UTF-8 text"], 1)

    def test_record_that_is_not_utf8_fails(self):
        self.write("kitchen/vetting/example.md", record())
        with open(os.path.join(self.root, "kitchen", "vetting", "example.md"), "wb") as handle:
            handle.write(b"---\nlens: \xff\n")
        self.check(["kitchen/vetting/example.md: cannot be read as UTF-8 text"], 1)

    def test_citation_without_a_link_fails(self):
        self.check_record(
            record(Independent_sources="- *A review* (checked 2026-11-18).\n"),
            "Independent sources: item 1 needs an https:// link and (checked YYYY-MM-DD)",
        )

    def test_citation_without_a_date_fails(self):
        self.check_record(
            record(Published_work=WORK + "- *Third Book*: https://example.com/third\n"),
            "Published work: item 3 needs an https:// link and (checked YYYY-MM-DD)",
        )

    def test_no_official_site_without_a_date_fails(self):
        self.check_record(
            record(
                Official_site="- No official site.\n",
                Independent_sources=SOURCES + SECOND_SOURCE,
            ),
            "Official site: item 1 needs (checked YYYY-MM-DD)",
        )

    def test_no_official_site_needs_two_independent_sources(self):
        self.check_record(
            record(Official_site="- No official site (checked 2026-11-18).\n"),
            "Independent sources: a seated lens needs at least 2 items, found 1",
        )

    def test_one_published_work_fails(self):
        self.check_record(
            record(Published_work=WORK.split("\n")[0] + "\n"),
            "Published work: a seated lens needs at least 2 items, found 1",
        )

    def test_none_found_does_not_seat_a_lens(self):
        self.check_record(
            record(Independent_sources="- None found (checked 2026-11-18).\n"),
            "Independent sources: item 1 needs an https:// link and (checked YYYY-MM-DD)",
        )

    def test_two_tendencies_fail(self):
        self.check_record(
            record(What_the_published_work_shows="1. One.\n2. Two.\n"),
            "What the published work shows: a seated lens needs 3 to 5 numbered "
            "items, found 2",
        )

    def test_six_tendencies_fail(self):
        shows = "".join("%d. Tendency.\n" % n for n in range(1, 7))
        self.check_record(
            record(What_the_published_work_shows=shows),
            "What the published work shows: a seated lens needs 3 to 5 numbered "
            "items, found 6",
        )

    def test_quotation_marks_and_blockquotes_fail(self):
        text = record(
            Where_this_lens_can_mislead='It says "always".\n> A quoted line.\n“Curly.”\n'
        )
        first = text.split("\n").index('It says "always".') + 1
        self.check_record(
            text,
            *[
                "line %d: double quotation marks and blockquotes are not allowed" % n
                for n in (first, first + 1, first + 2)
            ]
        )

    def test_unfilled_template_is_not_a_seated_record(self):
        self.write("kitchen/council.md", roster())
        with open(
            os.path.join(REPO, "templates", "lens-vetting-record.md"), encoding="utf-8"
        ) as handle:
            self.write("kitchen/vetting/new-lens.md", handle.read())
        result = run(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "kitchen/vetting/new-lens.md: verdict must be seat, seat narrower, or cut",
            result.stdout.splitlines(),
        )

    # The roster.

    def test_missing_roster_fails(self):
        os.remove(os.path.join(self.root, "kitchen", "council.md"))
        self.check(["kitchen/council.md: file is missing"], 1)

    def test_roster_without_both_headings_fails(self):
        self.write("kitchen/council.md", ROSTER_HEAD + "\n## Core lenses\n")
        self.check(
            [
                "kitchen/council.md: needs the headings ## Core lenses and "
                "## On-demand specialists, in that order"
            ],
            1,
        )

    def test_roster_headings_in_the_wrong_order_fail(self):
        self.write(
            "kitchen/council.md",
            ROSTER_HEAD + "\n## On-demand specialists\n\n## Core lenses\n",
        )
        self.check(
            [
                "kitchen/council.md: needs the headings ## Core lenses and "
                "## On-demand specialists, in that order"
            ],
            1,
        )

    def test_lens_heading_without_a_record_link_fails(self):
        text = roster(core=entry() + "\n### Budget-style lens\n\n- **Job:** Cost\n")
        line = text.split("\n").index("### Budget-style lens") + 1
        self.check_roster(
            text,
            "line %d: lens heading must be ### [<Name>-style lens](vetting/<slug>.md)"
            % line,
        )

    def test_lens_heading_outside_the_groups_fails(self):
        text = roster(core=entry()).replace(
            "\n## Core lenses\n", "\n### [Example-style lens](vetting/example.md)\n\n## Core lenses\n"
        )
        line = text.split("\n").index("### [Example-style lens](vetting/example.md)") + 1
        self.check_roster(
            text,
            "line %d: a ### heading must be under ## Core lenses or "
            "## On-demand specialists" % line,
        )

    def test_text_inside_an_entry_fails(self):
        text = roster(core=entry() + "\nA paragraph about the cook.\n")
        line = text.split("\n").index("A paragraph about the cook.") + 1
        self.check_roster(
            text, "line %d: only the four items may follow a lens heading" % line
        )

    def test_lens_seated_twice_fails(self):
        self.check_roster(
            roster(core=entry(), specialists=entry()), "example: seated more than once"
        )

    def test_entry_items_out_of_order_fail(self):
        text = roster(core=entry()).replace(
            "- **Job:** Heat and ingredient function\n"
            "- **Typical question:** Which variable changes the result?\n",
            "- **Typical question:** Which variable changes the result?\n"
            "- **Job:** Heat and ingredient function\n",
        )
        self.check_roster(
            text,
            "example: expected the items Job, Typical question, Scope, "
            "Where it can mislead, in that order",
        )

    def test_entry_with_a_missing_item_fails(self):
        text = roster(core=entry()).replace(
            "- **Where it can mislead:** It can add steps.\n", ""
        )
        self.check_roster(
            text,
            "example: expected the items Job, Typical question, Scope, "
            "Where it can mislead, in that order",
        )

    def test_entry_without_a_record_fails(self):
        self.check_roster(
            roster(core=entry() + entry("ghost", lens="Ghost-style lens")),
            "ghost: no record at kitchen/vetting/ghost.md",
        )

    def test_seating_a_cut_record_fails(self):
        self.write(
            "kitchen/vetting/example.md", record(verdict="cut", scope="none")
        )
        self.write("kitchen/council.md", roster(core=entry(scope="none")))
        self.check(
            ["kitchen/council.md: example: seated, but its record's verdict is cut"], 1
        )

    def test_entry_under_the_wrong_heading_fails(self):
        self.check_roster(
            roster(specialists=entry()),
            "example: listed under On-demand specialists, but its record says "
            "seat: core",
        )

    def test_entry_that_differs_from_its_record_fails(self):
        self.check_roster(
            roster(
                core=entry(
                    lens="Sample-style lens",
                    job="Everything",
                    question="Why?",
                    scope="All cooking",
                )
            ),
            "example: Lens name differs from its record",
            "example: Job differs from its record",
            "example: Typical question differs from its record",
            "example: Scope differs from its record",
        )

    def test_seated_record_missing_from_the_roster_fails(self):
        self.write("kitchen/council.md", roster())
        self.write("kitchen/vetting/example.md", record(verdict="seat narrower"))
        self.check(
            [
                "kitchen/vetting/example.md: verdict is seat narrower, but "
                "kitchen/council.md does not seat it"
            ],
            1,
        )

    def test_two_records_with_one_lens_name_fail(self):
        self.write("kitchen/vetting/example.md", record())
        self.write("kitchen/vetting/other.md", record())
        self.write("kitchen/council.md", roster(core=entry() + entry("other")))
        self.check(
            [
                "kitchen/vetting/other.md: lens Example-style lens is also used by "
                "kitchen/vetting/example.md"
            ],
            1,
        )

    def test_quotation_marks_in_the_roster_fail(self):
        text = roster(core=entry(mislead='It says "always".'))
        line = text.split("\n").index('- **Where it can mislead:** It says "always".') + 1
        self.check_roster(
            text,
            "line %d: double quotation marks and blockquotes are not allowed" % line,
        )

    # The command.

    def test_every_problem_is_reported_in_path_order(self):
        self.write("kitchen/vetting/example.md", record(seat="guest"))
        self.write("kitchen/vetting/zed.md", "no front matter\n")
        self.write(
            "kitchen/council.md", roster(core=entry() + entry("ghost", lens="Ghost-style lens"))
        )
        self.check(
            [
                "kitchen/council.md: ghost: no record at kitchen/vetting/ghost.md",
                "kitchen/vetting/example.md: seat must be core or specialist",
                "kitchen/vetting/zed.md: front matter is missing",
            ],
            1,
        )

    def test_extra_argument_is_a_usage_error(self):
        result = run(self.root, "extra")
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "usage: check-council.py [repository-root]\n")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
