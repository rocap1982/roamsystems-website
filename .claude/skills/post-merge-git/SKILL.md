---
name: post-merge-git
description: Clean up after a PR merge. Switches to main, pulls latest, deletes the merged branch, and prunes stale remotes.
argument-hint: "[optional: branch name to clean up]"
---

# /post-merge-git — Clean up after PR merge

## Goal

After a PR has been merged on the remote, clean up the local repo: switch to main, pull the merge, delete the feature branch, and prune stale remote references.

## Inputs

$ARGUMENTS

If no branch name is provided, use the current branch (if it's not main).

## Steps

### 1) Identify the merged branch

- If on a feature branch, note its name.
- If on main already, check `$ARGUMENTS` for the branch to clean up.
- Verify the branch was actually merged (check if remote tracking branch is gone or PR is merged).

### 2) Switch to main and pull

- Stash any uncommitted changes if present (warn the user).
- Switch to main: `git checkout main`
- Pull latest: `git pull`

### 3) Delete the merged branch

- Delete the local branch: `git branch -d <branch>`
  - If `-d` fails (not fully merged), inform the user and ask before using `-D`.
- If the remote branch still exists, delete it: `git push origin --delete <branch>`

### 4) Prune and verify

- Prune stale remote references: `git fetch --prune`
- Verify the branch is gone: `git branch -a | grep <branch>`
- Report current state.

## Output

1. Branch cleaned up: `<name>`
2. Current branch: main (at commit `<sha>`)
3. Remote pruned: yes/no
4. Any stashed changes to restore
