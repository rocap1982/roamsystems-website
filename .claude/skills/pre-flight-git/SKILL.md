---
name: pre-flight-git
description: Prepare the repo for new work. Syncs with remote, cleans up stale branches, and verifies a clean working state.
---

# /pre-flight-git — Prepare repo for new work

## Goal

Get the local repo into a clean, up-to-date state before starting new work. Sync with remote, clean up stale branches, and verify there's no leftover uncommitted work.

> **See also**: `/sync` for a lighter daily sync without branch cleanup.

## Steps

### 1) Check working state

- Run `git status` to check for uncommitted changes.
- If there are uncommitted changes:
  - Ask the user whether to commit, stash, or discard them.
  - Do not proceed until the working tree is clean.

### 2) Sync with remote

- Fetch all remotes: `git fetch --all --prune`
- Check if the current branch is behind the remote:
  - If behind: pull (rebase preferred) to get up to date.
  - If diverged: inform the user and ask how to proceed.
  - If ahead: note there are unpushed commits.

### 3) Clean up stale branches

- List local branches that have been merged into the main branch:
  ```
  git branch --merged main
  ```
- List local branches whose remote tracking branch is gone:
  ```
  git branch -vv | grep ': gone]'
  ```
- Present the list to the user and ask which to delete.
- Do not delete the current branch or the main branch.

### 4) Verify clean state

- Confirm working tree is clean.
- Confirm branch is up to date with remote.
- Report the current branch and latest commit.

## Output

1. Current branch and commit
2. Sync status (up to date / pulled N commits / unpushed commits)
3. Branches cleaned up (if any)
4. Ready to start work: Yes / No (with reason)
