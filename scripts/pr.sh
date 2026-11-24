#!/usr/bin/env bash
# pr.sh: the feature-branch and pull-request loop, from the terminal.
#   (In a guide repository the same script is scripts/pr.sh.)
#
#   bash tools/pr.sh start <name>    update main, then create branch feat/<name>
#   bash tools/pr.sh open [title]    push the branch and open a PR (title from the last commit)
#   bash tools/pr.sh status          the PR for this branch and its checks
#   bash tools/pr.sh watch           wait for the checks to finish
#   bash tools/pr.sh merge           wait for checks; squash-merge only if all pass;
#                                    delete the branch; return to an updated main
#   bash tools/pr.sh tidy            delete local branches whose remote branch is gone
#
# On a private repository with GitHub Free, branch protection is not available,
# so this script is the guard: `merge` refuses unless every check passed.
set -euo pipefail
# The whole script is one { ... } block, so bash reads all of it before running
# any of it. An overlay or a merge may rewrite this very file while it runs.
{

say() { printf '==> %s\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

top=$(git rev-parse --show-toplevel 2>/dev/null) || die "run this inside a git repository"
cd "$top"
main=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || true)
main=${main:-main}
branch=$(git branch --show-current)

wait_for_checks() {
  # checks can take a few seconds to register after a push
  local i out
  for i in $(seq 1 18); do
    out=$(gh pr checks 2>&1) && return 0
    case "$out" in *"no checks reported"*) sleep 10 ;; *) break ;; esac
  done
  gh pr checks --watch
}

update_main() {
  git switch -q "$main"
  git fetch -q --prune origin
  git merge -q --ff-only "origin/$main"
}

case "${1:-help}" in
  start)
    [ -n "${2:-}" ] || die "usage: pr.sh start <name>"
    [ -z "$(git status --porcelain)" ] || die "commit or stash your changes first"
    update_main
    git switch -c "feat/$2"
    say "On feat/$2. Commit your work, then: bash ${0#"$top"/} open"
    ;;
  open)
    [ "$branch" != "$main" ] || die "you are on $main; start a branch first"
    [ -z "$(git status --porcelain)" ] || die "commit your changes first"
    git push -q -u origin "$branch"
    if [ -n "${2:-}" ]; then
      gh pr create --base "$main" --title "$2" --body "$(git log --format='- %s' "origin/$main..HEAD")"
    else
      gh pr create --base "$main" --fill
    fi
    ;;
  status)
    gh pr view --json number,title,state,url -q '"#\(.number) \(.title) [\(.state)] \(.url)"'
    gh pr checks || true
    ;;
  watch)
    wait_for_checks
    ;;
  merge)
    [ "$branch" != "$main" ] || die "you are on $main; switch to the PR's branch"
    [ -z "$(git status --porcelain)" ] || die "commit or stash your changes first"
    [ "$(git rev-parse HEAD)" = "$(git rev-parse "origin/$branch" 2>/dev/null)" ] \
      || die "local $branch differs from origin/$branch; push first"
    say "Waiting for checks on $branch"
    wait_for_checks || die "checks did not all pass; nothing merged"
    gh pr merge --squash --delete-branch --match-head-commit "$(git rev-parse HEAD)"
    update_main
    git branch -D "$branch" >/dev/null 2>&1 || true
    say "Merged. On $main at $(git rev-parse --short HEAD)."
    ;;
  tidy)
    git fetch -q --prune origin
    git for-each-ref --format '%(refname:short) %(upstream:track)' refs/heads |
      awk '$2 == "[gone]" {print $1}' | while read -r b; do
        [ "$b" = "$branch" ] && continue
        git branch -D "$b" && say "deleted $b"
      done
    ;;
  help|-h|--help) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//' ;;
  *) die "unknown command $1 (try: bash tools/pr.sh help)" ;;
esac
exit
}
