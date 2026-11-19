#!/usr/bin/env bash
# Install an optional git pre-commit hook that runs the editor gate and the
# card linter before every commit in this repository.
#
# Usage: scripts/install-git-hooks.sh
#
# The hook runs scripts/check-qc.sh --staged and python3 scripts/lint-cards.py
# and stops the commit when either fails. CI runs the same two checks on every
# pull request, so the hook is a convenience and not the gate. An existing
# pre-commit hook that this script did not write is never replaced. To remove
# the hook, delete the file this script names when it finishes.
#
# Exit status: 0 the hook is installed; 1 another pre-commit hook is in the
# way; 2 the script could not run.
set -euo pipefail

MARK="# chef-council pre-commit hook"

fail() {
  echo "install-git-hooks: $1" >&2
  exit 2
}

[ "$#" -eq 0 ] || fail "usage: scripts/install-git-hooks.sh"
repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo"
git rev-parse --git-dir >/dev/null 2>&1 || fail "$repo is not a git repository"
hook=$(git rev-parse --git-path hooks/pre-commit)

if [ -e "$hook" ] || [ -L "$hook" ]; then
  if ! grep -qxF "$MARK" "$hook" 2>/dev/null; then
    echo "install-git-hooks: $hook already exists and was not written by this script; it was left as it is" >&2
    exit 1
  fi
fi

mkdir -p "$(dirname "$hook")"
cat > "$hook" <<'HOOK'
#!/bin/sh
# chef-council pre-commit hook
# Installed by scripts/install-git-hooks.sh. Delete this file to remove it.
root=$(git rev-parse --show-toplevel) || exit 1
"$root/scripts/check-qc.sh" --staged || exit 1
python3 "$root/scripts/lint-cards.py" || exit 1
HOOK
chmod +x "$hook"
echo "pre-commit hook installed: $hook"
