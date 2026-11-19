#!/usr/bin/env python3
"""Check the council roster against the lens vetting records.

Usage: python3 scripts/check-council.py [repository-root]

A record is a file kitchen/vetting/<slug>.md in the shape of
templates/lens-vetting-record.md. The roster, kitchen/council.md, seats a lens
with a heading that links its record. The check fails when a record is
malformed, when a record holds a web link or names its lens <Name>-style lens,
when the roster seats a lens with no record or a cut record, when a record
that says seat is not on the roster, and when the roster and a record
disagree. kitchen/council-vetting.md states the rule in words.

Prints one line per problem and exits 1, or prints
"council checked: <S> seated, <R> records" and exits 0.
"""

import datetime
import os
import re
import sys

KEYS = ["lens", "seat", "job", "question", "verdict", "scope", "checked"]
HOLDS = "What this lens holds"
SECTIONS = [HOLDS, "Where this lens can mislead", "Verdict"]
ITEMS = ["Job", "Typical question", "Scope", "Where it can mislead"]
GROUPS = {"Core lenses": "core", "On-demand specialists": "specialist"}
YAML_WORDS = {"yes", "no", "true", "false", "on", "off", "null", "y", "n"}
ROSTER = "kitchen/council.md"
ENTRY = re.compile(r"^### \[(.+ lens)\]\(vetting/([a-z0-9]+(?:-[a-z0-9]+)*)\.md\)$")
ITEM = re.compile(r"^- \*\*(.+?):\*\* (.*\S)\s*$")
LINK = re.compile(r"https?://", re.IGNORECASE)
LENS_FORM = "lens must be <Descriptor> lens, and never <Name>-style lens"


def is_date(text):
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return re.fullmatch(r"\d{4}-\d{2}-\d{2}", text) is not None


def lens_ok(text):
    return text.endswith(" lens") and not text.endswith("-style lens")


def quote_problems(lines):
    problems = []
    for number, line in enumerate(lines, 1):
        if line.startswith(">") or any(mark in line for mark in '"“”'):
            problems.append(
                "line %d: double quotation marks and blockquotes are not allowed"
                % number
            )
    return problems


def link_problems(lines):
    return [
        "line %d: a record holds no web link" % number
        for number, line in enumerate(lines, 1)
        if LINK.search(line)
    ]


def check_record(lines):
    """Return (fields or None, problems) for one record's lines."""
    problems = []
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return None, ["front matter is missing"] + link_problems(lines)
    end = lines.index("---", 1)
    fields = {}
    order = []
    for number, line in enumerate(lines[1:end], 2):
        match = re.fullmatch(r"([a-z_]+): (.*\S)", line)
        if not match:
            problems.append("front matter line %d is not key: value" % number)
            continue
        order.append(match.group(1))
        fields[match.group(1)] = match.group(2)
    if problems:
        return None, problems + link_problems(lines)
    if order != KEYS:
        return None, [
            "front matter keys must be exactly: %s" % ", ".join(KEYS)
        ] + link_problems(lines)

    for key in KEYS:
        value = fields[key]
        if not value[0].isalnum() or '"' in value or ": " in value or " #" in value:
            problems.append(
                "%s must start with a letter or digit and hold no double quote, "
                "colon-space, or space-hash" % key
            )
        if value.lower() in YAML_WORDS:
            problems.append("%s must not be a YAML boolean or null word" % key)
    if not lens_ok(fields["lens"]):
        problems.append(LENS_FORM)
    if fields["seat"] not in ("core", "specialist"):
        problems.append("seat must be core or specialist")
    if not fields["question"].endswith("?"):
        problems.append("question must end with a question mark")
    verdict = fields["verdict"]
    if verdict not in ("seat", "seat narrower", "cut"):
        problems.append("verdict must be seat, seat narrower, or cut")
    elif verdict == "cut" and fields["scope"] != "none":
        problems.append("scope must be none when the verdict is cut")
    elif verdict != "cut" and fields["scope"] == "none":
        problems.append("scope must not be none unless the verdict is cut")
    if not is_date(fields["checked"]):
        problems.append("checked must be a date written YYYY-MM-DD")

    body = lines[end + 1:]
    title = []
    for line in body:
        if line.startswith("## "):
            break
        if line.strip():
            title.append(line)
    if title != ["# " + fields["lens"]]:
        problems.append(
            "the text before the first section must be the title line "
            "# <lens> and nothing else"
        )
    names = [line[3:] for line in body if line.startswith("## ")]
    if names != SECTIONS:
        problems.append("sections must be exactly, in order: %s" % ", ".join(SECTIONS))
        return fields, problems + quote_problems(lines) + link_problems(lines)
    sections = {}
    current = None
    for line in body:
        if line.startswith("## "):
            current = sections.setdefault(line[3:], [])
        elif current is not None:
            current.append(line)

    for name in SECTIONS:
        if not any(line.strip() for line in sections[name]):
            problems.append("section %s is empty" % name)
    if verdict in ("seat", "seat narrower"):
        shown = sections[HOLDS]
        tendencies = sum(1 for line in shown if re.match(r"\d+\. \S", line))
        if any(line.strip() for line in shown) and not 3 <= tendencies <= 5:
            problems.append(
                "%s: a seated lens needs 3 to 5 numbered items, found %d"
                % (HOLDS, tendencies)
            )
        if any(
            line.strip() and not re.match(r"\d+\. \S|  ", line) for line in shown
        ):
            problems.append(
                "%s: a seated lens lists numbered items and nothing else" % HOLDS
            )
    return fields, problems + quote_problems(lines) + link_problems(lines)


def check_roster(lines):
    """Return (entries, problems); an entry is (slug, group, lens, items)."""
    problems = []
    headings = [line[3:] for line in lines if line.startswith("## ")]
    if [name for name in headings if name in GROUPS] != list(GROUPS):
        problems.append(
            "needs the headings ## Core lenses and ## On-demand specialists, "
            "in that order"
        )
        return [], problems + quote_problems(lines)
    entries = []
    group = None
    current = None
    for number, line in enumerate(lines, 1):
        if line.startswith("## "):
            group = line[3:] if line[3:] in GROUPS else None
            current = None
        elif line.startswith("### ") and not group:
            problems.append(
                "line %d: a ### heading must be under ## Core lenses or "
                "## On-demand specialists" % number
            )
        elif line.startswith("### "):
            match = ENTRY.match(line)
            if match and lens_ok(match.group(1)):
                current = []
                entries.append((match.group(2), group, match.group(1), current))
            else:
                current = None
                problems.append(
                    "line %d: lens heading must be "
                    "### [<Descriptor> lens](vetting/<slug>.md), and never "
                    "<Name>-style lens" % number
                )
        elif current is not None and line.startswith("- "):
            current.append(line)
        elif current is not None and line.strip() and not line.startswith("  "):
            problems.append(
                "line %d: only the four items may follow a lens heading" % number
            )
    return entries, problems + quote_problems(lines)


def read_lines(path):
    """Return the file's lines, or None when it is not readable UTF-8 text."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read().split("\n")
    except (OSError, UnicodeDecodeError):
        return None


def main(argv):
    if len(argv) > 2:
        print("usage: check-council.py [repository-root]", file=sys.stderr)
        return 2
    if len(argv) == 2:
        root = argv[1]
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    problems = []
    records = {}
    lenses = {}
    count = 0
    vetting = os.path.join(root, "kitchen", "vetting")
    names = sorted(os.listdir(vetting)) if os.path.isdir(vetting) else []
    for name in names:
        if name.startswith("."):
            continue
        path = "kitchen/vetting/%s" % name
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.md", name):
            problems.append(
                (path, "file name is not <slug>.md with a lowercase, hyphenated slug")
            )
            continue
        count += 1
        slug = name[:-3]
        lines = read_lines(os.path.join(vetting, name))
        if lines is None:
            fields, found = None, ["cannot be read as UTF-8 text"]
        else:
            fields, found = check_record(lines)
        problems.extend((path, text) for text in found)
        if fields is None or found:
            # A record with problems of its own is not compared with the roster.
            records[slug] = None
            continue
        records[slug] = fields
        if fields["lens"] in lenses:
            problems.append(
                (path, "lens %s is also used by kitchen/vetting/%s.md"
                 % (fields["lens"], lenses[fields["lens"]]))
            )
        else:
            lenses[fields["lens"]] = slug

    roster_path = os.path.join(root, "kitchen", "council.md")
    if not os.path.isfile(roster_path):
        problems.append((ROSTER, "file is missing"))
        entries = None
    else:
        lines = read_lines(roster_path)
        if lines is None:
            entries, found = None, ["cannot be read as UTF-8 text"]
        else:
            entries, found = check_roster(lines)
        problems.extend((ROSTER, text) for text in found)

    seated = []
    for slug, group, lens, items in entries or []:
        if slug in seated:
            problems.append((ROSTER, "%s: seated more than once" % slug))
            continue
        seated.append(slug)
        values = {}
        labels = []
        for line in items:
            match = ITEM.match(line)
            labels.append(match.group(1) if match else None)
            if match:
                values[match.group(1)] = match.group(2)
        if labels != ITEMS:
            problems.append(
                (ROSTER, "%s: expected the items %s, in that order"
                 % (slug, ", ".join(ITEMS)))
            )
        if slug not in records:
            problems.append(
                (ROSTER, "%s: no record at kitchen/vetting/%s.md" % (slug, slug))
            )
            continue
        fields = records[slug]
        if fields is None:
            continue
        if fields["verdict"] == "cut":
            problems.append((ROSTER, "%s: seated, but its record's verdict is cut" % slug))
        if GROUPS[group] != fields["seat"]:
            problems.append(
                (ROSTER, "%s: listed under %s, but its record says seat: %s"
                 % (slug, group, fields["seat"]))
            )
        pairs = [("Lens name", lens, "lens")]
        pairs += [(label, values.get(label), key) for label, key in
                  (("Job", "job"), ("Typical question", "question"), ("Scope", "scope"))]
        for label, value, key in pairs:
            if value is not None and value != fields[key]:
                problems.append((ROSTER, "%s: %s differs from its record" % (slug, label)))
    if entries is not None:
        for slug in sorted(records):
            fields = records[slug]
            if fields and fields["verdict"] in ("seat", "seat narrower") and slug not in seated:
                problems.append(
                    ("kitchen/vetting/%s.md" % slug,
                     "verdict is %s, but kitchen/council.md does not seat it"
                     % fields["verdict"])
                )

    if problems:
        for path, text in sorted(problems, key=lambda problem: problem[0]):
            print("%s: %s" % (path, text))
        return 1
    print("council checked: %d seated, %d records" % (len(seated), count))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
