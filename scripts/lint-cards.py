#!/usr/bin/env python3
"""Lint the recipe cards.

Usage: python3 scripts/lint-cards.py [repository-root]

A card is a file recipes/<category>/<slug>.md, as scripts/build-index.py
finds them. For each card this checks that it is a regular UTF-8 file with
closed front matter and a title; that the front matter holds id, version,
status, evidence, and category once each, with id equal to the file name,
category equal to the folder, a version such as v1.0, and a status and an
evidence value that method/status-and-versions.md lists; that the lines
under the title give Version, Date, Status, Kitchen evidence, Source, Yield,
and Time once each and agree with the front matter; that the slug and the
category are lowercase letters, digits, and single hyphens; that no two
cards share a slug; and that every inline link in the card that is not a
web address leads to a file or a folder, read from the card's folder, or
from the repository root when it starts with "/". Then it runs
scripts/build-index.py --check, so a stale index fails.

Prints one line per problem and exits 1, or prints "cards checked: <N>" and
exits 0.
"""

import datetime
import os
import re
import subprocess
import sys

USAGE = "usage: lint-cards.py [repository-root]"
FIELD = re.compile(r"([a-z_]+):[ \t]*(.*)")
NAME = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
VERSION = re.compile(r"v[1-9][0-9]*\.(0|[1-9][0-9]*)")
LINK = re.compile(r'\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')
FENCE = re.compile(r"\s*(`{3,}|~{3,})")
REQUIRED = ["id", "version", "status", "evidence", "category"]
STATUSES = ["draft", "reviewed", "testing", "house", "retired"]
EVIDENCE = ["untested", "cooked-once", "repeated", "not-recorded"]
LABELS = ["Version", "Date", "Status", "Kitchen evidence", "Source", "Yield", "Time"]
AGREE = [("Version", "version"), ("Status", "status"), ("Kitchen evidence", "evidence")]
UNREADABLE = ("is not UTF-8 text", "front matter is not closed", "has no title line")


def find_cards(root):
    """Return (cards, problems): (category, slug) pairs in order, and the folders that are links."""
    recipes = os.path.join(root, "recipes")
    cards = []
    problems = []
    if not os.path.isdir(recipes):
        return cards, problems
    for category in sorted(os.listdir(recipes)):
        folder = os.path.join(recipes, category)
        if category.startswith(".") or not os.path.isdir(folder):
            continue
        if os.path.islink(folder):
            problems.append((category, "", "recipes/%s: is a symbolic link" % category))
            continue
        for name in os.listdir(folder):
            if name.startswith(".") or not name.endswith(".md"):
                continue
            path = os.path.join(folder, name)
            if os.path.islink(path) or os.path.isfile(path):
                cards.append((category, name[: -len(".md")]))
    return sorted(cards), problems


def shown(value):
    return value if value else "empty"


def is_date(text):
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text):
        return False
    try:
        datetime.date(int(text[:4]), int(text[5:7]), int(text[8:]))
    except ValueError:
        return False
    return True


def lint_card(root, category, slug):
    """Return the problems of one card, without the path in front."""
    path = os.path.join(root, "recipes", category, slug + ".md")
    if os.path.islink(path):
        return ["is a symbolic link"]
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except UnicodeDecodeError:
        return ["is not UTF-8 text"]
    fields = {}
    body = lines
    bare = not lines or lines[0] != "---"
    if not bare:
        if "---" not in lines[1:]:
            return ["front matter is not closed"]
        end = lines.index("---", 1)
        for line in lines[1:end]:
            match = FIELD.fullmatch(line)
            if match:
                fields.setdefault(match.group(1), []).append(match.group(2).strip())
        body = lines[end + 1 :]
    title = None
    for number, line in enumerate(body):
        if line.startswith("# ") and line[2:].strip():
            title = number
            break
    if bare or title is None:
        return ["has no front matter"] * bare + ["has no title line"] * (title is None)

    problems = []
    for key in REQUIRED + ["mirrors"]:
        count = len(fields.get(key, []))
        if count == 0 and key != "mirrors":
            problems.append("front matter has no %s line" % key)
        elif count > 1:
            problems.append("front matter has more than one %s line" % key)
    single = {key: values[0] for key, values in fields.items() if len(values) == 1}
    if "id" in single and single["id"] != slug:
        problems.append("front matter id is %s, expected the file name %s" % (shown(single["id"]), slug))
    if "category" in single and single["category"] != category:
        problems.append(
            "front matter category is %s, expected the folder %s" % (shown(single["category"]), category)
        )
    if "version" in single and not VERSION.fullmatch(single["version"]):
        problems.append("front matter version is %s, expected the form v1.0" % shown(single["version"]))
    if "status" in single and single["status"] not in STATUSES:
        problems.append(
            "front matter status is %s, expected one of %s" % (shown(single["status"]), ", ".join(STATUSES))
        )
    if "evidence" in single and single["evidence"] not in EVIDENCE:
        problems.append(
            "front matter evidence is %s, expected one of %s"
            % (shown(single["evidence"]), ", ".join(EVIDENCE))
        )
    if not NAME.fullmatch(slug):
        problems.append("file name is not lowercase letters, digits, and single hyphens")
    if not NAME.fullmatch(category):
        problems.append("folder name is not lowercase letters, digits, and single hyphens")

    header = {}
    for line in body[title + 1 :]:
        if line.startswith("## "):
            break
        for label in LABELS:
            mark = "- **%s:**" % label
            if line.startswith(mark):
                header.setdefault(label, []).append(line[len(mark) :].strip())
    for label in LABELS:
        count = len(header.get(label, []))
        if count == 0:
            problems.append("has no %s line under the title" % label)
        elif count > 1:
            problems.append("has more than one %s line under the title" % label)
    stated = {label: values[0] for label, values in header.items() if len(values) == 1}
    for label, key in AGREE:
        if label in stated and key in single and stated[label] != single[key]:
            problems.append(
                "%s line is %s, but the front matter says %s"
                % (label, shown(stated[label]), shown(single[key]))
            )
    if "Date" in stated and not is_date(stated["Date"]):
        problems.append("Date line is %s, expected a date as YYYY-MM-DD" % shown(stated["Date"]))
    for label in ["Source", "Yield", "Time"]:
        if label in stated and not stated[label]:
            problems.append("%s line is empty" % label)

    fence = None
    for line in body:
        mark = FENCE.match(line)
        if fence is None and mark:
            fence = mark.group(1)
            continue
        if fence is not None:
            closing = line.strip()
            if len(closing) >= len(fence) and set(closing) == {fence[0]}:
                fence = None
            continue
        for target in LINK.findall(line):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:|#", target):
                continue
            target = target.split("#")[0].split("?")[0]
            start = root if target.startswith("/") else os.path.dirname(path)
            if not os.path.exists(os.path.join(start, target.lstrip("/"))):
                problems.append("broken link %s" % target)
    return problems


def main(argv):
    arguments = argv[1:]
    if len(arguments) > 1 or any(argument.startswith("-") for argument in arguments):
        print(USAGE, file=sys.stderr)
        return 2
    if arguments:
        root = arguments[0]
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isdir(root):
        print("lint-cards: %s is not a directory" % root, file=sys.stderr)
        return 2

    cards, found = find_cards(root)
    unreadable = False
    for category, slug in cards:
        relative = "recipes/%s/%s.md" % (category, slug)
        for problem in lint_card(root, category, slug):
            found.append((category, slug, "%s: %s" % (relative, problem)))
            if problem in UNREADABLE:
                unreadable = True
        for other, other_slug in cards:
            if other_slug == slug and other != category:
                found.append(
                    (category, slug, "%s: slug is also used by recipes/%s/%s.md" % (relative, other, slug))
                )
    lines = [text for _, _, text in sorted(found, key=lambda problem: problem[:2])]

    if not unreadable:
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-index.py")
        index = subprocess.run(
            [sys.executable, script, "--check", root], capture_output=True, text=True, check=False
        )
        if index.returncode != 0:
            lines.extend((index.stdout + index.stderr).splitlines())

    if lines:
        for line in lines:
            print(line)
        return 1
    print("cards checked: %d" % len(cards))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
