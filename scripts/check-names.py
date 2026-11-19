#!/usr/bin/env python3
"""Check that no name the lenses once carried is back in the tree.

Usage: python3 scripts/check-names.py [--show] [--base <commit>] [repository-root]

Until 2026-11-19 each lens carried the name of a real cook or publisher, and
its vetting record cited books, shows, sites, and the outlets that reviewed
them. The names were removed before the repository was made public. This
check keeps them out. It holds none of them: it reads them, each time it
runs, from the roster and the vetting records of the last commit that had
them (--base, by default the commit named in BASE below), and then looks for
them in every file of the working tree that git tracks or would track.

What it derives from that commit, after folding accents and curly
apostrophes to plain letters:

  name    each lens name (the roster heading and the record's lens line,
          without "-style lens"), each part of a record's name line, each
          word of those names of three letters or more that the roster does
          not also use as an ordinary lowercase word, the initials of a name
          of three or more words, and each record's file name. Matched in
          any letter case, except a three-letter word or set of initials.
  host    the host of every web link in a record, without a leading "www.".
          Matched in any letter case, anywhere.
  title   every title a record sets in italics: a title of more than one
          word wherever it is written, and a one-word title where it is set
          in italics. Matched exactly.
  proper  every run of two or more capitalized words in a record (a run of
          three or more that opens a sentence loses its first word when
          that word is an ordinary one), every capitalized word of three
          letters or more in a record, with and without a closing 's, and
          every one-word title. A single
          word is left out when the same word is written in lowercase
          somewhere in that commit, which marks it as an ordinary word.
          Matched exactly.

A proper term that is an ordinary word or place name can be allowed by
putting it on a line of its own in scripts/names-allowlist.txt. A name, a
host, or a title can never be allowed, and a line that allows nothing is an
error, so the list cannot grow stale or hide a name.

Prints one line per hit, "<path>:<line>: <kind>", or "<path>: <kind> in the
path", and never the name itself unless --show is given, because the output
of CI is public. Then "names check: <N> hit(s)" and exit 1, or
"names checked: <F> files, <T> terms" and exit 0. Exit 2 means the check
could not run, which never counts as clean: the base commit is not in this
clone (a shallow clone has no history; run git fetch --unshallow), or it
holds no roster or no record.
"""

import os
import re
import subprocess
import sys
import unicodedata

BASE = "38dfcceca709b025624c08327f87791871a3605f"
ROSTER = "kitchen/council.md"
RECORDS = "kitchen/vetting/"
ALLOWLIST = "scripts/names-allowlist.txt"
SUFFIX = "-style lens"

URL = re.compile(r"https?://[^\s)>\]]+")
ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
HEADING = re.compile(r"^### \[(.+)\]\(vetting/([^)]+)\.md\)$", re.M)
FIELD = re.compile(r"^(lens|name): (.*\S)\s*$", re.M)
WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
CAPITAL = re.compile(r"[A-Z]\.(?= )|[A-Z][A-Za-z0-9]*(?:'[A-Za-z]+)?|&")
LOWER = re.compile(
    r"(?<![A-Za-z0-9_'./\-])[a-z]+(?:'[a-z]+)?(?![A-Za-z0-9_'/\-])(?!\.[A-Za-z0-9])"
)
LIST_MARK = re.compile(r"(?:[-+]|\d+\.|#+)?")
INITIAL = re.compile(r"(?:^|[^A-Za-z])[A-Z]\.$")
EDGE = r"(?:(?<![A-Za-z0-9])|(?<=\\b))(?:%s)(?![A-Za-z0-9])"
KINDS = ("name", "host", "title", "proper")


class CannotRun(Exception):
    pass


def fold(text):
    text = text.replace("’", "'").replace("‘", "'")
    return "".join(
        char for char in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(char)
    )


def git(root, *args):
    return subprocess.run(
        ["git", "-C", root, *args], capture_output=True, check=False
    )


def show(root, base, path):
    result = git(root, "show", "%s:%s" % (base, path))
    if result.returncode != 0:
        return None
    try:
        return fold(result.stdout.decode("utf-8"))
    except UnicodeDecodeError:
        return None


def phrase(text):
    """A pattern for the words of text, with any white space between them."""
    return r"\s+".join(re.escape(word) for word in text.split())


def starts_sentence(line, index):
    before = line[:index].rstrip()
    if LIST_MARK.fullmatch(before):
        return True
    return before[-1] in ".?!:;" and not INITIAL.search(before)


def proper_terms(text, common):
    """Return (runs, words): capitalized runs and single capitalized words."""
    runs = set()
    words = set()
    for line in text.replace("*", "").split("\n"):
        run = []
        end = None
        found = list(CAPITAL.finditer(line)) + [None]
        for match in found:
            if match is not None and run and line[end:match.start()] == " ":
                run.append(match)
                end = match.end()
                continue
            if run:
                tokens = [item.group(0) for item in run]
                if (
                    len(tokens) > 2
                    and starts_sentence(line, run[0].start())
                    and tokens[0].lower() in common
                ):
                    tokens = tokens[1:]
                while tokens and tokens[0] == "&":
                    tokens = tokens[1:]
                while tokens and tokens[-1] == "&":
                    tokens = tokens[:-1]
                if len(tokens) > 1:
                    runs.add(" ".join(tokens))
                for item in run:
                    word = item.group(0).rstrip(".")
                    for form in (word, word[:-2] if word.endswith("'s") else word):
                        if len(form) > 2 and form.lower() not in common:
                            words.add(form)
            run = [] if match is None else [match]
            end = None if match is None else match.end()
    return runs, words


def derive(root, base=BASE):
    """Return {kind: set of terms} read from the roster and records at base."""
    if git(root, "rev-parse", "--is-inside-work-tree").stdout.strip() != b"true":
        raise CannotRun("%s is not a git working tree" % root)
    if git(root, "cat-file", "-e", "%s^{commit}" % base).returncode != 0:
        raise CannotRun(
            "commit %s is not in this clone; fetch the full history "
            "(git fetch --unshallow)" % base
        )
    listed = git(root, "ls-tree", "-r", "-z", "--name-only", base)
    paths = [path for path in listed.stdout.decode("utf-8", "replace").split("\0") if path]
    roster = show(root, base, ROSTER) if ROSTER in paths else None
    records = {}
    for path in paths:
        if path.startswith(RECORDS) and path.endswith(".md") and "/" not in path[len(RECORDS):]:
            text = show(root, base, path)
            if text is not None:
                records[path[len(RECORDS):-3]] = text
    if roster is None or not records:
        raise CannotRun("commit %s holds no roster or no vetting record" % base)

    common = set()
    for path in paths:
        text = show(root, base, path)
        if text is not None:
            common.update(LOWER.findall(URL.sub(" ", text)))
    roster_words = set(LOWER.findall(roster))

    names = set()
    slugs = set(records)
    for lens, slug in HEADING.findall(roster):
        names.add(lens[:-len(SUFFIX)] if lens.endswith(SUFFIX) else lens)
        slugs.add(slug)
    hosts = set()
    titles = set()
    runs = set()
    words = set()
    for text in records.values():
        for key, value in FIELD.findall(text.split("\n---\n")[0]):
            if key == "lens" and value.endswith(SUFFIX):
                value = value[:-len(SUFFIX)]
            names.update(part.strip() for part in value.split(" / ") if part.strip())
        for link in URL.findall(text):
            host = re.sub(r"^https?://(?:www\.)?", "", link, flags=re.I).split("/")[0]
            hosts.add(host.lower().rstrip(".,;:"))
        plain = URL.sub(" ", text)
        for title in ITALIC.findall(plain):
            title = " ".join(title.split())
            if " " in title:
                titles.add(title)
            else:
                titles.add("*%s*" % title)
                if len(title) > 2 and title.lower() not in common:
                    words.add(title)
        found_runs, found_words = proper_terms(plain, common)
        runs.update(found_runs)
        words.update(found_words)
    name_words = set()
    for name in names:
        found = WORD.findall(name)
        initials = "".join(word[0] for word in found if word[0].isupper())
        if len(initials) > 2:
            name_words.add(initials)
        for word in found:
            if len(word) > 2 and word.lower() not in roster_words:
                name_words.add(word)
    terms = {
        "name": {name.lower() for name in names | slugs}
        | {word if len(word) == 3 else word.lower() for word in name_words},
        "host": {host for host in hosts if host},
        "title": titles,
        "proper": runs | words,
    }
    protected = {term.lower() for kind in ("name", "host", "title") for term in terms[kind]}
    terms["proper"] = {term for term in terms["proper"] if term.lower() not in protected}
    return terms


def read_allowlist(root, terms):
    """Return (allowed terms, problems) from the allowlist file."""
    path = os.path.join(root, ALLOWLIST)
    if not os.path.isfile(path):
        return set(), []
    try:
        with open(path, encoding="utf-8") as handle:
            lines = fold(handle.read()).split("\n")
    except (OSError, UnicodeDecodeError):
        return set(), ["%s: cannot be read as UTF-8 text" % ALLOWLIST]
    protected = {term.lower() for kind in ("name", "host", "title") for term in terms[kind]}
    allowed = set()
    problems = []
    for number, line in enumerate(lines, 1):
        term = " ".join(line.split())
        if not term or term.startswith("#"):
            continue
        if term.lower() in protected:
            problems.append(
                "%s: line %d: a name, a host, or a title cannot be allowed"
                % (ALLOWLIST, number)
            )
        elif term not in terms["proper"]:
            problems.append(
                "%s: line %d: allows nothing this check looks for; remove it"
                % (ALLOWLIST, number)
            )
        elif term in allowed:
            problems.append("%s: line %d: repeats an earlier line" % (ALLOWLIST, number))
        else:
            allowed.add(term)
    return allowed, problems


def compile_terms(terms):
    """Return [(kind, pattern)] in the order the kinds are reported."""
    patterns = []
    for kind in KINDS:
        found = sorted(terms[kind], key=lambda term: (-len(term), term))
        if not found:
            continue
        if kind == "host":
            patterns.append((kind, re.compile("|".join(map(re.escape, found)), re.I)))
        elif kind == "name":
            short = [term for term in found if len(term) == 3 and term != term.lower()]
            rest = [term for term in found if term not in short]
            if rest:
                patterns.append((kind, re.compile(EDGE % "|".join(map(phrase, rest)), re.I)))
            if short:
                patterns.append((kind, re.compile(EDGE % "|".join(map(phrase, short)))))
        elif kind == "title":
            marked = [term for term in found if term.startswith("*")]
            plain = [term for term in found if term not in marked]
            if plain:
                patterns.append((kind, re.compile(EDGE % "|".join(map(phrase, plain)))))
            if marked:
                patterns.append(
                    (kind, re.compile(r"(?<!\*)(?:%s)(?!\*)" % "|".join(map(re.escape, marked))))
                )
        else:
            patterns.append((kind, re.compile(EDGE % "|".join(map(phrase, found)))))
    return patterns


def find(patterns, text):
    """Return [(start, end, kind)] for every match in folded text.

    A match that lies inside a longer match of the same kind is left out.
    """
    found = []
    for kind, pattern in patterns:
        found.extend((match.start(), -match.end(), kind) for match in pattern.finditer(text))
    hits = []
    reach = {}
    for start, end, kind in sorted(found):
        if -end > reach.get(kind, -1):
            hits.append((start, -end, kind))
            reach[kind] = -end
    return hits


def tracked_files(root):
    result = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if result.returncode != 0:
        raise CannotRun("could not list the files of %s" % root)
    return sorted(
        {path for path in result.stdout.decode("utf-8", "surrogateescape").split("\0") if path}
    )


def main(argv):
    usage = "usage: check-names.py [--show] [--base <commit>] [repository-root]"
    show_names = False
    base = BASE
    rest = []
    args = argv[1:]
    while args:
        arg = args.pop(0)
        if arg == "--show":
            show_names = True
        elif arg == "--base" and args:
            base = args.pop(0)
        elif arg.startswith("-"):
            print(usage, file=sys.stderr)
            return 2
        else:
            rest.append(arg)
    if len(rest) > 1 or not base:
        print(usage, file=sys.stderr)
        return 2
    root = rest[0] if rest else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        terms = derive(root, base)
        files = tracked_files(root)
    except CannotRun as error:
        print("check-names: %s" % error, file=sys.stderr)
        return 2
    allowed, problems = read_allowlist(root, terms)
    terms["proper"] -= allowed
    patterns = compile_terms(terms)

    lines = list(problems)
    count = 0
    for path in files:
        full = os.path.join(root, path)
        if not os.path.isfile(full) and not os.path.islink(full):
            continue
        count += 1
        shown = path.encode("utf-8", "replace").decode("utf-8")
        for kind in sorted({hit[2] for hit in find(patterns, fold(shown))}, key=KINDS.index):
            lines.append("%s: %s in the path" % (shown, kind))
        if os.path.islink(full):
            continue
        try:
            with open(full, encoding="utf-8") as handle:
                text = fold(handle.read())
        except (OSError, UnicodeDecodeError):
            continue
        seen = set()
        for start, end, kind in find(patterns, text):
            number = text.count("\n", 0, start) + 1
            key = (number, kind) if not show_names else (number, kind, text[start:end])
            if key in seen:
                continue
            seen.add(key)
            line = "%s:%d: %s" % (shown, number, kind)
            if show_names:
                line += ": %s" % " ".join(text[start:end].split())
            lines.append(line)

    if lines:
        for line in lines:
            print(line)
        print("names check: %d hit(s)" % len(lines))
        return 1
    print("names checked: %d files, %d terms" % (count, sum(len(terms[kind]) for kind in KINDS)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
