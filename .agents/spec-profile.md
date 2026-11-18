# Spec pipeline profile

## Identity

- Repository: `chef-council`, a fork-ready system for cooking with AI agents: a
  council of cooking lenses, plain-text recipe cards and cook logs, and an
  independent editor check that gates every recipe change. It is built private
  and made public only after the maintainer's review (map W001, decision T004).
- Default base branch: `main`.
- ADRs: none
- Branch protection: none is enforced on this private repository. The
  maintainer is the sole collaborator. Agents never push `main`. Every change
  lands through a pull request: the maintainer merges in the pipeline's manual
  mode, and the `spec-pipeline` driver merges through `gh pr merge` in
  autonomous mode under the kickoff grant `autonomous`, logging each merge.

## Verify

- Setup: run from the repository root with Git, Bash, Python 3 (standard
  library only), and an authenticated `gh`. There is no build step and nothing
  to install. Before the first commit of a session, require
  `git config user.email` to end in `@users.noreply.github.com`; anything else
  is a stop for the human.
- Deterministic checks:
  - Every check the repository's CI workflows under `.github/workflows/` run,
    run locally where it can be. Before review, `gh pr checks <PR>` must report
    every check passed; a red check is a kickback finding and a missing run is
    a question for the human. The spec that adds a check records its local
    command in this list.
  - The CI checks' local commands, run from the repository root:
    `python3 scripts/check-skills.py` (prints `skills checked: <N>` and exits
    0), `python3 scripts/check-council.py` (prints `council checked: <S>
    seated, <R> records` and exits 0), `python3 -m unittest discover -s tests
    -v` (its last line is `OK`), and
    `scripts/secret-scan.sh` (gitleaks over the full local history: exit 0
    with `no leaks found`, exit 1 on a leak, and exit 2 when the scan could
    not run, which never counts as clean). The scan downloads the pinned
    gitleaks release on Linux x86_64 on first use; elsewhere, set
    `GITLEAKS_BIN` to an installed gitleaks.
  - The wayfinder skill's `scripts/lint.py` over `docs/wayfinder/*/MAP.md`
    (the skill's directory is the one the harness prints when the skill
    loads). It prints one line per problem and exits 1 when it prints any.
  - `git diff --check` for unstaged changes and, with `BASE_SHA` read from the
    spec's `base_sha:` field, `git diff --check "$BASE_SHA"...HEAD -- .` for
    committed branch changes; stage every intended path explicitly, then run
    `git diff --cached --check` and inspect `git diff --cached` before the final
    green claim.
  - The privacy sweep, `"$(git rev-parse --git-common-dir)/info/privacy-sweep"`:
    a maintainer-local script that is never committed. It checks the working
    tree, the full local history (every ref, blob, commit message, and commit
    identity), and the repository's GitHub text (issues, pull requests,
    comments, reviews, review comments, labels, branch names) against a
    private denylist. It prints only a rule ID and a location for each hit,
    never the matched text, and ends with one summary line:
    `privacy sweep: clean [...]` with exit 0, or `privacy sweep: <N> hit(s) [...]`
    with exit 1. Exit 2 is a configuration error and never counts as clean.
    `--text <file>...` checks draft text before it is posted. Run
    `git fetch origin` first so remote branches are in the history it reads.
  - Every task-specific gate written in the approved spec; a task gate must
    cover its bounded touched paths.
- Real artifact: the repository as a stranger receives it from GitHub: the
  rendered `README.md` and docs, the skills an agent discovers in a fresh
  clone, the scripts and CI checks, the example cards with their editor
  reports, and the chat bundle a chat-app user pastes in.
- Observation method:
  - Markdown: render the changed file from the pushed branch with
    `gh api "repos/{owner}/{repo}/contents/<path>?ref=<branch>" -H 'Accept: application/vnd.github.html'`
    and inspect the result; confirm every relative link target exists with
    `git ls-files --error-unmatch`.
  - Skills: in a fresh clone of the pushed branch in a new temporary directory,
    confirm `.agents/skills/<name>/SKILL.md` has spec-valid frontmatter (`name`,
    `description`, and only the optional `license`, `compatibility`,
    `metadata`) and that `.claude/skills/<name>` resolves to it.
  - Scripts and CI: run the script on the spec's fixtures and read
    `gh pr checks <PR>`.
  - Agent behavior (an editor run, a behavior check, the stranger test): use a
    fresh subagent through the harness's agent tool, briefed only with what
    the spec names. A headless provider CLI call is a provider call, which
    needs the spec to require it and the maintainer to approve it.
- Artifact locator: record `git rev-parse HEAD` and, for each observed file,
  `git ls-files --error-unmatch <path>`; for a fresh clone, its
  `git rev-parse HEAD` must equal the PR's head commit.

## Ship tail

- Version policy: none for the repository: do not invent a version file,
  package version, or tag. Recipe cards carry their own `vX.Y` under the
  repository's status-and-versions rules.
- Sweeps: the three diff checks above, the Wayfinder lint, and the full privacy
  sweep printing `privacy sweep: clean`, run before every push and again before
  reporting a PR ready; `--text` on every draft PR body, issue body, and comment
  before it is posted.
- Test runner: Python standard-library `unittest`, tests under `tests/`, run as
  `python3 -m unittest discover -s tests -v`. A shell script is tested through
  `subprocess` from a `unittest` module. Do not add another framework or any
  third-party package. Documentation-only work has no tests task.
- Branch naming: `workstream/` plus the ticket's lowercase kebab-case slug for
  ticket work, `harvest/` plus the spec's slug for a harvest. A branch name
  never carries private detail.
- Commit subjects: imperative mood, no emoji; explain why when it is not
  obvious. No session links and no private detail in any commit message.
- PR base and body: target `main`. Open with ELI5 (what changed, what it
  means, and what the run did to get here, written for a non-developer in
  under 200 words by the leg that opens the PR), Summary (user outcome),
  Evidence (real before/after where applicable, the privacy sweep's summary
  line verbatim, or an explicit limitation), and Merge Danger (reversibility,
  blast radius, rollback limits). Every PR the pipeline opens, the harvest PR
  included, carries the ELI5 before it is merged. Draft every PR body, issue
  body, and comment into a temporary file outside the repository, run the
  sweep's `--text` on it, then post it with `--body-file`.
- Release/deploy: none. CI is a check, never a release. The repository stays
  private: making it public and linking it from the maintainer's website are
  the maintainer's separate steps after review, and no leg changes repository
  visibility or settings.

## Pipeline constraints

- **Public by default.** Everything that enters this repository becomes public
  when the maintainer publishes it: files, history, commit messages, branch
  names, specs, map tickets, learnings, issues, PR bodies, and review
  comments. Leave out the names of household members and any household
  detail, health details, location, notes-app IDs, private URLs or hosts,
  machine paths, the maintainer's self-hosted assistant, session links, and
  the names of the maintainer's private repositories; refer to the private
  predecessor only as "my private cooking repo" (decisions T005 and T006).
- **Private sources.** The material this repository is sanitized from is
  read-only under `"$(git rev-parse --git-common-dir)/info/private-sources/"`:
  `cooking/` (the private cooking repository), `home-design/` (the private
  home-design council), `council-skills/` (the earlier council skills), and
  `design/design-report.md` (this repository's design report; §4 is the
  sanitization ledger). Never write to them. Cite them in committed or posted
  text only as `private-sources/<path>`, and never quote them in GitHub text.
  Never copy a passage verbatim except what a ticket's evidence names as kept,
  and then only after the ledger's scrub. Never put a private-source file into
  a cross-examination dossier.
- **Third-party recipes.** Copy no third-party recipe text: no ingredient
  lists, methods, or headnotes from any publisher. Credit a source by title
  and link only when it was actually read.
- **Real people (decision T002).** Each named lens is seated only with a
  vetting record of the chef's published work and argues only from that
  record's tendencies. Never invent a quote, and never say a chef approved,
  reviewed, endorsed, or contributed to anything. Attribute advice as
  "Kenji-style lens" (the chef's name, then `-style lens`). Write no
  "weaknesses" about a real person; describe where the lens can mislead. A
  vetting record cites only pages actually read in the session, with the date
  checked, and describes published work, never personal life.
- **Privacy sweep hits.** Fix a hit at its location; never quote the matched
  text in any committed or posted text. A hit that would need rewriting pushed
  history, or editing GitHub text the leg cannot edit, is a `Question:` for the
  maintainer.
- **Not for any leg:** changing repository visibility or settings, touching
  the maintainer's website, writing to the private sources or to any other
  repository, and pushing `main`.

## Independent review

The invocation mechanics (route choice by session family, the commands, the
sandbox, the pinned binary, and the local failure checks) live in the
maintainer's routes document, `docs/reference/provider-routes.md` in the
private agent-system repository that the maintainer's global agent rules name,
and the tier table in those global rules decides the provider. This section
records only what is specific to this repository. Never copy an invocation
command into this file or into any committed text.

- Current session provider family: read from the running harness, never
  inferred from this profile. Claude Code states its model ID in the system
  prompt; a Pi session reads `PI_PROVIDER` and `PI_MODEL`. Map it to a tier
  table column as the routes document says; a family in no column, or an
  absent or ambiguous identity, is a stop to ask.
- Required outside provider family: the route the routes document selects for
  the session's family at the tier of the work, which is architect for the
  spec cross-examination and the PR cross-examination. Record the exact
  provider, model, effort, and CLI version in the artifact.
- Read-only invocation: the routes document's command for the selected route,
  with `REPO` set to this checkout's `git rev-parse --show-toplevel`. The
  dossier holds this repository's bounded evidence and nothing else: the full
  draft spec or reviewed diff, `AGENTS.md` once it exists, this profile, and
  every file in the spec's touch set. It never holds a private-source file.
  Run the privacy sweep's `--text` on the dossier before sending it; a hit is
  fixed in the dossier's source, never waved through. A dossier that cannot
  hold the complete bounded evidence is a stop for a maintainer-approved
  route, never a wider sandbox.
- Local failure checks: the routes document's checks, then one retry; a
  waiver is the maintainer's alone and is recorded as the routes document
  says.
