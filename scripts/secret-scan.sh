#!/usr/bin/env bash
# Scan the full git history of a repository for secrets with a pinned gitleaks.
#
# Usage: scripts/secret-scan.sh [repository-directory]   (default: this repository)
#
# Exit status: 0 no leaks, 1 leaks found, 2 the scan could not run.
# Set GITLEAKS_BIN to use a gitleaks of the pinned version that you installed
# yourself. Otherwise the pinned release is downloaded once, checked against
# its SHA-256, and kept in GITLEAKS_CACHE (default: the runner's temporary
# directory in CI, else ~/.cache/chef-council). Only Linux x86_64 is pinned.
set -euo pipefail

GITLEAKS_VERSION=8.30.1
GITLEAKS_SHA256_LINUX_X64=551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb

fail() {
  echo "secret-scan: $1" >&2
  exit 2
}

[ "$#" -le 1 ] || fail "usage: scripts/secret-scan.sh [repository-directory]"
repo=${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 || fail "$repo is not a git repository"

bin=${GITLEAKS_BIN:-}
if [ -z "$bin" ]; then
  cache=${GITLEAKS_CACHE:-${RUNNER_TEMP:-${XDG_CACHE_HOME:-$HOME/.cache}/chef-council}/gitleaks-$GITLEAKS_VERSION}
  bin=$cache/gitleaks
  if [ ! -x "$bin" ]; then
    [ "$(uname -s)-$(uname -m)" = "Linux-x86_64" ] ||
      fail "only Linux x86_64 is pinned; install gitleaks $GITLEAKS_VERSION and set GITLEAKS_BIN"
    archive=gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz
    mkdir -p "$cache"
    work=$(mktemp -d "$cache/download.XXXXXX")
    trap 'rm -rf "$work"' EXIT
    curl -sSfL --retry 3 -o "$work/$archive" \
      "https://github.com/gitleaks/gitleaks/releases/download/v$GITLEAKS_VERSION/$archive" ||
      fail "could not download $archive"
    echo "$GITLEAKS_SHA256_LINUX_X64  $work/$archive" | sha256sum -c - >/dev/null ||
      fail "$archive does not match its pinned SHA-256"
    tar -xzf "$work/$archive" -C "$work" gitleaks || fail "could not unpack $archive"
    mv "$work/gitleaks" "$bin"
  fi
fi
[ -x "$bin" ] || fail "$bin is not an executable gitleaks"
version=$("$bin" version 2>/dev/null) || fail "$bin did not report a version"
[ "$version" = "$GITLEAKS_VERSION" ] ||
  fail "$bin is gitleaks $version, expected $GITLEAKS_VERSION"

status=0
"$bin" git --log-opts=--all --redact --no-banner --verbose "$repo" || status=$?
case "$status" in
  0 | 1) exit "$status" ;;
  *) fail "gitleaks exited with status $status" ;;
esac
