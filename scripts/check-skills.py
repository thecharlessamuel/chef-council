#!/usr/bin/env python3
"""Check that every skill is linked for Claude Code and named in AGENTS.md.

Usage: python3 scripts/check-skills.py [repository-root]

A skill is a directory under .agents/skills/. Each one needs a SKILL.md, a
symbolic link .claude/skills/<name> -> ../../.agents/skills/<name>, and its
path .agents/skills/<name>/SKILL.md written in AGENTS.md. Prints one line per
problem and exits 1, or prints "skills checked: <N>" and exits 0.
"""

import os
import sys


def main(argv):
    if len(argv) > 2:
        print("usage: check-skills.py [repository-root]", file=sys.stderr)
        return 2
    if len(argv) == 2:
        root = argv[1]
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    skills_dir = os.path.join(root, ".agents", "skills")
    links_dir = os.path.join(root, ".claude", "skills")
    if not os.path.isdir(skills_dir):
        print(".agents/skills is missing")
        return 1

    skills = sorted(
        name
        for name in os.listdir(skills_dir)
        if not name.startswith(".")
        and os.path.isdir(os.path.join(skills_dir, name))
    )
    links = []
    if os.path.isdir(links_dir):
        links = sorted(
            name for name in os.listdir(links_dir) if not name.startswith(".")
        )
    try:
        with open(os.path.join(root, "AGENTS.md"), encoding="utf-8") as handle:
            index = handle.read()
    except FileNotFoundError:
        index = ""

    problems = []
    for name in skills:
        skill_path = ".agents/skills/%s/SKILL.md" % name
        link_path = ".claude/skills/%s" % name
        expected = "../../.agents/skills/%s" % name
        link = os.path.join(links_dir, name)
        if not os.path.isfile(os.path.join(skills_dir, name, "SKILL.md")):
            problems.append((name, "%s is missing" % skill_path))
        if os.path.islink(link):
            target = os.readlink(link)
            if target != expected:
                problems.append(
                    (name, "%s points to %s, expected %s" % (link_path, target, expected))
                )
        elif os.path.lexists(link):
            problems.append((name, "%s is not a symbolic link" % link_path))
        else:
            problems.append((name, "%s is missing" % link_path))
        if skill_path not in index:
            problems.append((name, "AGENTS.md does not name %s" % skill_path))
    for name in links:
        if name not in skills:
            problems.append(
                (name, ".claude/skills/%s has no skill at .agents/skills/%s" % (name, name))
            )

    if problems:
        for name, text in sorted(problems, key=lambda problem: problem[0]):
            print("%s: %s" % (name, text))
        return 1
    print("skills checked: %d" % len(skills))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
