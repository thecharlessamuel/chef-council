#!/usr/bin/env bash
# The editor gate: every recipe card that changed needs a current, passing
# editor report.
#
# Usage: scripts/check-qc.sh [--staged | --working-tree | --stop-hook] [--base <revision>]
#        scripts/check-qc.sh --hash <file>
#
# A card is recipes/<category>/<slug>.md. A card that was added or changed
# since the base passes only when a report qc/<category>/<slug>/<name>.md was
# added or changed too, holds exactly one line that starts with "VERDICT:",
# reading "VERDICT: PASS" or "VERDICT: PASS WITH NOTES", and holds exactly one
# line that starts with "Card-SHA256:", giving the SHA-256 of the card's bytes.
# Any later edit to the card changes its hash, so an old PASS stops counting.
#
# What is compared with the base:
#   (default)        the last commit, which is what CI sees
#   --staged         what is staged, for a pre-commit hook
#   --working-tree   the files as they are now, untracked ones included
#   --stop-hook      --working-tree, as a Claude Code Stop hook (see below)
#
# The base is --base, else $QC_BASE, else origin/main. Changes are counted
# from the commit where the branch left the base. A base of forty zeros,
# which is what a first push reports, means every card is checked.
#
# --hash prints the "Card-SHA256:" line for a file, for a report.
#
# Exit status: 0 every changed card has a current passing report; 1 one does
# not; 2 the check could not run, which never counts as a pass. A missing
# base is one such case: the check never passes without a base to compare.
# With --stop-hook the script prints nothing on success, exits 2 with the
# problems on standard error when a card lacks its report (which keeps the
# session open), and exits 1 when the check could not run (2 when CI=true).
# See method/recipe-qc.md.
set -uo pipefail

USAGE="usage: scripts/check-qc.sh [--staged | --working-tree | --stop-hook] [--base <revision>] | --hash <file>"
ZERO=0000000000000000000000000000000000000000

usage() {
  echo "$USAGE" >&2
  exit 2
}

mode=""
hook=0
base=${QC_BASE:-origin/main}

# The check could not run. Never exits 0.
fail() {
  echo "check-qc: $1" >&2
  if [ "$hook" = 1 ] && [ "${CI:-}" != "true" ]; then
    exit 1
  fi
  exit 2
}

sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum | cut -d ' ' -f 1
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 | cut -d ' ' -f 1
  else
    return 1
  fi
}

if [ "${1:-}" = "--hash" ]; then
  [ "$#" -eq 2 ] || usage
  [ -f "$2" ] || fail "$2 is not a file"
  digest=$(sha256 < "$2") && [ -n "$digest" ] || fail "needs sha256sum or shasum"
  echo "Card-SHA256: $digest"
  exit 0
fi

while [ "$#" -gt 0 ]; do
  case "$1" in
    --staged | --working-tree | --stop-hook)
      [ -z "$mode" ] || usage
      mode=$1
      ;;
    --base)
      [ "$#" -ge 2 ] || usage
      base=$2
      shift
      ;;
    *) usage ;;
  esac
  shift
done
[ -n "$mode" ] || mode=--head
if [ "$mode" = "--stop-hook" ]; then
  hook=1
  mode=--working-tree
  # Claude Code sends the hook a JSON object. When this hook has already kept
  # the session open once, let it stop, so the session cannot loop forever.
  if [ ! -t 0 ]; then
    input=$(cat || true)
    if printf '%s' "$input" | tr '\n' ' ' | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
      exit 0
    fi
  fi
fi

root=$(git rev-parse --show-toplevel 2>/dev/null) || fail "not inside a git repository"
cd "$root" || fail "cannot enter $root"
git rev-parse --verify -q "HEAD^{commit}" >/dev/null || fail "this repository has no commit yet"

if [ "$base" = "$ZERO" ]; then
  from=$(git hash-object -t tree /dev/null) || fail "cannot name the empty tree"
else
  git rev-parse --verify -q "$base^{commit}" >/dev/null ||
    fail "base $base not found: fetch it, or name another with --base or QC_BASE"
  from=$(git merge-base "$base" HEAD 2>/dev/null) || fail "no merge base between $base and HEAD"
fi

list=$(mktemp) || fail "cannot create a temporary file"
trap 'rm -f "$list" "$list.sorted"' EXIT
case "$mode" in
  --head)
    git diff --no-renames --name-only -z --diff-filter=d "$from" HEAD > "$list" ||
      fail "git diff failed"
    ;;
  --staged)
    git diff --cached --no-renames --name-only -z --diff-filter=d "$from" > "$list" ||
      fail "git diff failed"
    ;;
  --working-tree)
    git diff --no-renames --name-only -z --diff-filter=d "$from" > "$list" ||
      fail "git diff failed"
    git ls-files --others --exclude-standard -z >> "$list" || fail "git ls-files failed"
    ;;
esac
# Sort the NUL-separated list with a plain sort, by swapping NUL and newline.
tr '\0\n' '\n\0' < "$list" | LC_ALL=C sort -u | tr '\0\n' '\n\0' > "$list.sorted" || fail "sort failed"

changed=()
while IFS= read -r -d '' path; do
  changed+=("$path")
done < "$list.sorted"

# Print the candidate content of one path.
show() {
  case "$mode" in
    --head) git show "HEAD:$1" ;;
    --staged) git show ":$1" ;;
    --working-tree) cat -- "$1" ;;
  esac
}

# Print why the report $1 does not pass for a card whose hash is $2, or nothing.
judge() {
  local text verdict stated
  text=$(show "$1" | sed 's/[[:space:]]*$//') || { echo "cannot be read"; return; }
  if [ "$(printf '%s\n' "$text" | grep -c '^VERDICT:')" != 1 ]; then
    echo "must hold exactly one line that starts with VERDICT:"
    return
  fi
  verdict=$(printf '%s\n' "$text" | grep '^VERDICT:')
  case "$verdict" in
    "VERDICT: PASS" | "VERDICT: PASS WITH NOTES") ;;
    "VERDICT: FAIL")
      echo "the verdict is FAIL"
      return
      ;;
    *)
      echo "the VERDICT line is not PASS, PASS WITH NOTES, or FAIL"
      return
      ;;
  esac
  if [ "$(printf '%s\n' "$text" | grep -c '^Card-SHA256:')" != 1 ]; then
    echo "must hold exactly one line that starts with Card-SHA256:"
    return
  fi
  stated=$(printf '%s\n' "$text" | grep '^Card-SHA256:')
  if ! printf '%s\n' "$stated" | grep -Eq '^Card-SHA256: [0-9a-f]{64}$'; then
    echo "the Card-SHA256 line does not hold 64 lowercase hexadecimal digits"
    return
  fi
  if [ "$stated" != "Card-SHA256: $2" ]; then
    echo "Card-SHA256 is not the hash of the card, so the card changed after this check"
  fi
}

cards=0
lacking=0
problems=()
for path in ${changed[@]+"${changed[@]}"}; do
  [[ "$path" =~ ^recipes/([^/]+)/([^/]+)\.md$ ]] || continue
  category=${BASH_REMATCH[1]}
  slug=${BASH_REMATCH[2]}
  case "$category" in .*) continue ;; esac
  case "$slug" in .*) continue ;; esac
  cards=$((cards + 1))
  digest=$(show "$path" | sha256) && [ -n "$digest" ] || fail "cannot hash $path: needs sha256sum or shasum"
  prefix="qc/$category/$slug/"
  passed=0
  found=()
  for report in "${changed[@]}"; do
    name=${report#"$prefix"}
    [ "$name" != "$report" ] || continue
    case "$name" in
      */* | .*) continue ;;
      *.md) ;;
      *) continue ;;
    esac
    reason=$(judge "$report" "$digest")
    if [ -z "$reason" ]; then
      passed=1
      break
    fi
    found+=("$path: $report: $reason")
  done
  [ "$passed" = 0 ] || continue
  lacking=$((lacking + 1))
  if [ "${#found[@]}" -eq 0 ]; then
    problems+=("$path: no editor report was added or changed under $prefix")
  else
    problems+=("${found[@]}")
  fi
done

if [ "$lacking" -gt 0 ]; then
  if [ "$hook" = 1 ]; then
    printf '%s\n' "${problems[@]}" >&2
  else
    printf '%s\n' "${problems[@]}"
  fi
  echo "check-qc: $lacking of $cards changed recipe cards lack a current passing editor report; method/recipe-qc.md says how to get one" >&2
  if [ "$hook" = 1 ]; then
    exit 2
  fi
  exit 1
fi
[ "$hook" = 1 ] || echo "qc checked: $cards"
exit 0
