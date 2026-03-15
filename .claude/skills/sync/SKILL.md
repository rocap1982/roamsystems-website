---
name: sync
description: Sync the local repo with remote. Checks for uncommitted work, pulls latest changes, prunes stale branches, and reports a summary. Quick daily driver for getting in sync.
---

# Sync

Quick skill to get the local repo in sync with remote. Handles dirty state safely.

> **See also**: `/pre-flight-git` for a more thorough pre-work preparation that includes branch cleanup.

## Steps (execute all in order)

### 1. Check working tree status

```bash
git status --porcelain
```

- If **clean**: proceed to step 2.
- If **dirty**: show the user what's uncommitted and ask:
  - "You have uncommitted changes. Should I stash them, or do you want to commit first?"
  - If user says stash: `git stash push -m "sync-auto-stash"` and set a flag to pop later.
  - If user says commit: stop and let them handle it.

### 2. Check current branch

```bash
git branch --show-current
```

- If not on `main`, warn the user and ask if they want to switch to main first.
- If they say no, sync the current branch instead (fetch + pull with its upstream).

### 3. Fetch from remote

```bash
git fetch origin
```

### 4. Show what's new

```bash
git log --oneline origin/main ^HEAD
```

- If no new commits: report "Already up to date."
- If new commits: list them.

### 5. Pull latest

```bash
git pull origin main
```

- If fast-forward succeeds: continue.
- If pull would require a merge or has conflicts: **stop and report** to the user. Do not auto-merge.

### 6. Check for unpushed local commits

```bash
git log --oneline HEAD ^origin/main
```

- If there are local commits not on remote: report them and ask if the user wants to push.

### 7. Prune stale remote refs

```bash
git remote prune origin
```

### 8. Restore stash (if stashed in step 1)

```bash
git stash pop
```

If pop fails due to conflicts, warn the user.

### 9. Report

Print a summary:

```
Sync complete:
- Branch: <branch-name>
- Status before sync: clean | stashed <n> files
- Pulled: <count> new commits (or "already up to date")
- Local unpushed: <count> commits (or "none")
- Stale refs pruned: yes/no
- Working tree: clean | restored from stash
```
