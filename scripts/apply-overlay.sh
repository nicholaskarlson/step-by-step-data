#!/usr/bin/env bash
# apply-overlay.sh: apply a drop-in overlay ZIP and open a PR.
#   (In a guide repository the same script is scripts/apply-overlay.sh.)
#
#   bash tools/apply-overlay.sh ~/Downloads/<overlay>.zip [--no-pr] [--no-checks] [--base main]
#   bash tools/apply-overlay.sh ~/Downloads/<fix>.zip --here [--no-checks]
#
# The ZIP holds files at their paths in this repository (optionally inside one
# top-level folder) plus an OVERLAY.md manifest at its root:
#
#   Branch: feat/short-name
#   Title: One-line commit subject and PR title
#   Delete: path/to/remove            (optional, one per line)
#
#   Everything after the first blank line is the PR description (Markdown).
#
# Default: refuse if the working tree is dirty; update the base branch; create
# the branch; copy the files; apply deletions; mark the overlay's scripts executable; run the
# repo's quick checks; commit; push; open the PR.
# --here: add the overlay as one more commit on the branch you are on, which
# must be the manifest's Branch: (a fix-up for an open PR). It pushes, CI reruns
# on that PR, and no new PR is opened.
# It never merges: wait for CI, read the diff, then `bash tools/pr.sh merge`.
set -euo pipefail
# The whole script is one { ... } block, so bash reads all of it before running
# any of it. An overlay or a merge may rewrite this very file while it runs.
{

say()  { printf '==> %s\n' "$*"; }
die()  { printf 'error: %s\n' "$*" >&2; exit 1; }

# Git on Windows (core.filemode=false) records new files as 100644, so Linux
# will not run them directly. Record the executable bit for each file the overlay
# brought (given as arguments) that starts with "#!". Files the overlay did not
# touch keep their modes: a companion's frozen scripts must not change mode.
mark_executables() {
  local meta path first
  local -a todo=()
  for path in "$@"; do
    [ -f "$path" ] || continue
    meta=$(git ls-files -s -- "$path")
    [ "${meta%% *}" = 100644 ] || continue
    first=""; IFS= read -r -n 2 first < "$path" 2>/dev/null || true
    [ "$first" = '#!' ] && todo+=("$path")
  done
  [ ${#todo[@]} -gt 0 ] || return 0
  chmod +x -- "${todo[@]}" 2>/dev/null || true
  git update-index --chmod=+x -- "${todo[@]}"
  say "Marked ${#todo[@]} script(s) executable in git"
}

script_dir=$(cd "$(dirname "$0")" && pwd)   # where this script lives (its pr.sh sits beside it)
zip=""; PR=1; CHECKS=1; BASE=main; HERE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --no-pr) PR=0 ;;
    --no-checks) CHECKS=0 ;;
    --here) HERE=1 ;;
    --base) shift; BASE="$1" ;;
    -h|--help) sed -n '2,23p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) die "unknown option $1" ;;
    *) zip="$1" ;;
  esac; shift
done
[ -n "$zip" ] || die "usage: bash tools/apply-overlay.sh <overlay.zip> [--here] [--no-pr] [--no-checks]"
[ -f "$zip" ] || die "no such file: $zip"
zip_abs="$(cd "$(dirname "$zip")" && pwd)/$(basename "$zip")"

top=$(git rev-parse --show-toplevel 2>/dev/null) || die "run this inside the repository the overlay is for"
cd "$top"
[ -z "$(git status --porcelain)" ] || { git status --short >&2; die "the working tree has changes; commit or stash them first"; }

# extract with unzip, or Python if unzip is missing
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
if command -v unzip >/dev/null 2>&1; then
  unzip -q "$zip_abs" -d "$tmp/x"
else
  py=""
  for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys' >/dev/null 2>&1; then py="$c"; break; fi
  done
  [ -n "$py" ] || die "need unzip or Python to read the ZIP"
  "$py" -c 'import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])' "$zip_abs" "$tmp/x"
fi
root="$tmp/x"
if [ ! -f "$root/OVERLAY.md" ]; then
  entries=("$root"/*)
  if [ ${#entries[@]} -eq 1 ] && [ -d "${entries[0]}" ] && [ -f "${entries[0]}/OVERLAY.md" ]; then root="${entries[0]}"; fi
fi
[ -f "$root/OVERLAY.md" ] || die "the ZIP has no OVERLAY.md manifest at its root"

# parse the manifest (tolerate CRLF)
tr -d '\r' < "$root/OVERLAY.md" > "$tmp/manifest"
BRANCH=$(sed -n 's/^Branch:[[:space:]]*//p;T;q' "$tmp/manifest")   # first match only
TITLE=$(sed -n 's/^Title:[[:space:]]*//p;T;q' "$tmp/manifest")
mapfile -t DELETES < <(sed -n 's/^Delete:[[:space:]]*//p' "$tmp/manifest")
awk 'body{print} /^$/ && !body{body=1}' "$tmp/manifest" > "$tmp/body.md"
[ -n "$BRANCH" ] && [ -n "$TITLE" ] || die "OVERLAY.md needs Branch: and Title: lines"
git check-ref-format --branch "$BRANCH" >/dev/null || die "bad branch name: $BRANCH"

has_origin=0; git remote get-url origin >/dev/null 2>&1 && has_origin=1
current=$(git branch --show-current)

say "Overlay: $(basename "$zip")"
if [ "$HERE" = 1 ]; then
  [ "$current" != "$BASE" ] || die "--here adds a commit to a PR branch, and you are on $BASE"
  [ "$current" = "$BRANCH" ] || die "this overlay is for branch $BRANCH, but you are on ${current:-a detached HEAD}; run: git switch $BRANCH"
  say "Branch:  $BRANCH (adding a commit to the branch you are on)"
  if [ "$has_origin" = 1 ]; then
    git fetch -q origin
    if git rev-parse --verify -q "origin/$BRANCH" >/dev/null; then
      git merge -q --ff-only "origin/$BRANCH" 2>/dev/null \
        || die "local $BRANCH and origin/$BRANCH have diverged; sort that out first"
    fi
  fi
else
  git show-ref --verify --quiet "refs/heads/$BRANCH" \
    && die "branch $BRANCH already exists locally (for a fix-up to its open PR, switch to it and add --here)"
  say "Branch:  $BRANCH (from $BASE)"
  git switch -q "$BASE"
  if [ "$has_origin" = 1 ]; then
    git fetch -q origin
    git rev-parse --verify -q "origin/$BASE" >/dev/null && git merge -q --ff-only "origin/$BASE"
  fi
  git switch -q -c "$BRANCH"
fi
say "Title:   $TITLE"

# copy every file except the manifest
count=0; copied=()
while IFS= read -r -d '' f; do
  rel="${f#"$root"/}"
  [ "$rel" = OVERLAY.md ] && continue
  mkdir -p "$(dirname "$rel")"
  cp "$f" "$rel"
  copied+=("$rel")
  count=$((count + 1))
done < <(find "$root" -type f -print0)
for d in "${DELETES[@]}"; do
  [ -n "$d" ] && git rm -rq --ignore-unmatch -- "$d" && say "deleted $d"
done
git add -A
mark_executables "${copied[@]}"
say "Copied $count files. Changes:"
git status --short
if git diff --cached --quiet; then
  if [ "$HERE" = 0 ]; then git switch -q "$BASE"; git branch -q -D "$BRANCH"; die "the overlay changes nothing; branch removed"; fi
  die "the overlay changes nothing"
fi

if [ "$CHECKS" = 1 ]; then
  if [ -f tests/quick.sh ]; then say "Running tests/quick.sh"; bash tests/quick.sh
  elif [ -f scripts/check.sh ]; then say "Running scripts/check.sh"; bash scripts/check.sh
  fi || die "checks failed; the overlay's changes are staged on $BRANCH. Fix them, then commit and push."
fi

# commit message: the title, the overlay's name, then the manifest's description
{ printf '%s\n\nApplied overlay %s.\n' "$TITLE" "$(basename "$zip")"
  if [ -s "$tmp/body.md" ]; then printf '\n'; cat "$tmp/body.md"; fi; } > "$tmp/message"
git commit -q -F "$tmp/message"
say "Committed $(git rev-parse --short HEAD) on $BRANCH"

if [ "$PR" = 0 ] || [ "$has_origin" = 0 ]; then
  if [ "$HERE" = 1 ]; then say "Not pushed. When ready: git push"
  else say "Not pushed. When ready: git push -u origin $BRANCH && gh pr create --fill"; fi
  exit 0
fi
git push -q -u origin "$BRANCH"
# name the pr.sh to use next: the one beside this script, else the repository's own
prsh=""
if [ -f "$script_dir/pr.sh" ]; then
  prsh="$script_dir/pr.sh"
  case "$prsh" in "$top"/*) prsh="${prsh#"$top"/}" ;; "$HOME"/*) prsh="~/${prsh#"$HOME"/}" ;; esac
elif [ -f tools/pr.sh ]; then prsh="tools/pr.sh"
elif [ -f scripts/pr.sh ]; then prsh="scripts/pr.sh"; fi
if [ "$HERE" = 1 ]; then
  url=$(gh pr view "$BRANCH" --json url -q .url 2>/dev/null || true)
  if [ -n "$url" ]; then say "Pushed to the open PR, so its checks run again: $url"
  else say "Pushed. There is no open PR for $BRANCH yet: bash $prsh open"; fi
else
  gh pr create --base "$BASE" --head "$BRANCH" --title "$TITLE" --body-file "$tmp/body.md"
fi
say "Next: wait for the checks, read the diff on GitHub, then merge:"
if [ -n "$prsh" ]; then
  echo "    bash $prsh watch"
  echo "    bash $prsh merge"
else
  echo "    gh pr checks --watch"
  echo "    gh pr merge --squash --delete-branch"
fi
exit
}
