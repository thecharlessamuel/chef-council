# Skills

Each skill is one folder here, `.agents/skills/<name>/`, holding a `SKILL.md` in the Agent Skills format. An agent that follows the Agent Skills format finds skills in this folder on its own. Claude Code looks in `.claude/skills/`, so every skill also has a symbolic link there.

## Adding a skill

1. Create `.agents/skills/<name>/SKILL.md`. Use a lowercase, hyphenated name that matches the folder. Keep the front matter to `name` and `description`, plus the optional `license`, `compatibility`, and `metadata`.
2. Link it for Claude Code, from the repository root:

   ```bash
   ln -s ../../.agents/skills/<name> .claude/skills/<name>
   ```

3. Add one line for it under "Skills" in [`AGENTS.md`](../../AGENTS.md), so an agent that discovers nothing can still find it. The line gives the path and says when to use the skill:

   ```markdown
   - `<name>`: [`.agents/skills/<name>/SKILL.md`](.agents/skills/<name>/SKILL.md). <When to use it.>
   ```
4. Run the check, which CI also runs:

   ```bash
   python3 scripts/check-skills.py
   ```

The check fails when a skill has no `SKILL.md`, no link, a link that is not a symbolic link to `../../.agents/skills/<name>`, or no line in `AGENTS.md`, and when a link has no skill behind it.

## Windows

Git on Windows checks symbolic links out as small text files unless `core.symlinks` is enabled. If the check reports "is not a symbolic link" on a fresh clone, run `git config core.symlinks true` and check the files out again, or read the skills from `.agents/skills/` directly.
