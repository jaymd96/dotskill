# Common Operations and Troubleshooting

Useful commands and solutions for everyday git tasks.

---

## Syncing with Main

### Keep Feature Branch Current

```bash
# Fetch latest from remote
git fetch origin

# Rebase onto main (preferred - clean history)
git rebase origin/main

# Or merge if rebase causes issues
git merge origin/main
```

### Handling Rebase Conflicts

```bash
# Start rebase
git rebase origin/main

# [conflict occurs]
# Edit files to resolve conflicts

# Add resolved files
git add resolved_file.py

# Continue rebase
git rebase --continue

# If something goes wrong, abort
git rebase --abort
```

### View Status During Rebase

```bash
# See what's happening
git status

# See commits being replayed
git log origin/main..HEAD --oneline

# See changes in current rebase step
git diff HEAD
```

---

## Viewing Branch Status

### Commits Ahead/Behind Main

```bash
# See commits ahead of main
git log main..HEAD --oneline

# See commits behind main
git log HEAD..main --oneline

# See both
git log --graph --oneline --all --decorate
```

### Files Changed

```bash
# List changed files
git diff --stat main

# See actual changes
git diff main

# See only additions/deletions
git diff --stat --summary main
```

### Branch Tracking

```bash
# Show upstream branch
git branch -vv

# Update tracking (if necessary)
git branch -u origin/feature/module-name
```

---

## Stashing Work

### Save Work in Progress

```bash
# Stash with message
git stash push -m "WIP: auth implementation"

# Or simpler
git stash

# List all stashes
git stash list
```

### Apply Stashed Work

```bash
# Apply latest stash
git stash pop

# Apply specific stash
git stash pop stash@{0}

# Apply without removing from stash
git stash apply stash@{0}
```

### Manage Stashes

```bash
# Drop a stash
git stash drop stash@{0}

# Clear all stashes
git stash clear

# Create branch from stash
git stash branch feature/from-stash
```

---

## Editing Commits

### Amend Last Commit

```bash
# Fix commit message
git commit --amend -m "new message"

# Add forgotten files
git add forgotten_file.py
git commit --amend --no-edit

# Change commit content but keep message
git add changes.py
git commit --amend --no-edit
```

### Reset Last Commit

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1

# Move changes to staging
git reset --mixed HEAD~1
```

### Rebase to Edit Multiple Commits

```bash
# Interactive rebase on last N commits
git rebase -i HEAD~3

# Edit appears as:
# pick aaa1111 Commit message 1
# pick bbb2222 Commit message 2
# pick ccc3333 Commit message 3

# Change 'pick' to:
# - 'reword' to change message
# - 'edit' to modify commit
# - 'squash' to combine with previous
# - 'drop' to delete

# Then save file and follow prompts
```

---

## Undoing Changes

### Undo Unstaged Changes

```bash
# Discard changes to file
git checkout -- path/to/file.py

# Or modern syntax
git restore path/to/file.py

# Discard all changes
git checkout -- .
```

### Unstage Files

```bash
# Unstage file from staging
git reset HEAD path/to/file.py

# Or modern syntax
git restore --staged path/to/file.py

# Unstage all
git reset HEAD
```

### Remove Commits from History

```bash
# Remove last commit (keep changes)
git reset --soft HEAD~1

# Remove last 3 commits (keep changes)
git reset --soft HEAD~3

# Remove commit and discard changes
git reset --hard HEAD~1

# Remove specific commit from middle
git rebase -i HEAD~3  # Mark as 'drop'
```

---

## Viewing History

### Browse Commits

```bash
# View last N commits
git log --oneline -10

# View commits on current branch not on main
git log main..HEAD --oneline

# View with graph
git log --graph --oneline --all --decorate

# View specific file history
git log --oneline -- path/to/file.py
```

### Search History

```bash
# Find commits with message
git log --grep="fix.*cache" --oneline

# Find commits by author
git log --author="Claude" --oneline

# Find commits that changed specific function
git log -S "function_name" --oneline

# Find when line was added/removed
git log -p --follow -- path/to/file.py | grep -A2 -B2 "search term"
```

### View Specific Commit

```bash
# Show commit details
git show aaa1111

# Show only statistics
git show aaa1111 --stat

# Show only changes to file
git show aaa1111 -- path/to/file.py
```

---

## Comparing Branches

### Diff Against Main

```bash
# See all changes
git diff main

# See statistics
git diff --stat main

# See specific file
git diff main -- path/to/file.py
```

### Find Divergence Point

```bash
# Find where branches split
git merge-base main HEAD

# Show commits unique to each branch
git log --oneline main...HEAD
```

---

## Error Recovery

### Lost Commits

```bash
# Find lost commits
git reflog

# Shows: aaa1111 HEAD@{0}: commit: message
#        bbb2222 HEAD@{1}: checkout: branch

# Recover specific commit
git cherry-pick aaa1111

# Or create branch from it
git branch recovery aaa1111
```

### Accidental Commits to Main

```bash
# Save the work
git branch feature/accidental-work

# Reset main to origin state
git reset --hard origin/main

# Continue work on feature branch
git checkout feature/accidental-work
```

### Reverted Too Much

```bash
# See what was deleted
git reflog

# Recover
git reset --hard <commit-hash>
```

### Merge Conflict Resolution

```bash
# Start problematic merge/rebase
git rebase origin/main

# [conflict occurs]
# See conflicted files
git status

# Edit files (look for >>>>> and <<<<<)
# Keep what you need, remove conflict markers

# Mark as resolved
git add resolved_file.py
git rebase --continue

# Abort if needed
git rebase --abort
```

---

## Worktree Operations

### Create Worktree

```bash
# Create with new branch
git worktree add ../project-auth-work -b feature/auth

# Create with existing branch
git worktree add ../project-cache-work feature/cache

# Navigate to it
cd ../project-auth-work
```

### Manage Worktrees

```bash
# List all worktrees
git worktree list

# Remove worktree after merge
git worktree remove ../project-auth-work

# Prune stale worktree references
git worktree prune
```

### Switch Between Worktrees

```bash
# Work in one worktree
cd ~/project
git checkout feature/auth
# ... work ...

# Switch to parallel work
cd ~/project-cache
# ... work ...

# Back to first
cd ~/project
```

---

## Performance and Cleanup

### Clean Up Local Branches

```bash
# Delete merged branches
git branch --merged | grep -v main | xargs git branch -d

# Delete all local tracking branches for deleted remotes
git fetch origin --prune

# Show what would be cleaned
git branch -a | grep deleted
```

### Compact Repository

```bash
# Optimize git database
git gc

# Aggressive optimization (slower)
git gc --aggressive
```

### Large File Handling

```bash
# Find large files
git rev-list --all --objects | \
  sort -k2 | \
  tail -10

# Remove file from history
git filter-branch --tree-filter 'rm -f large_file.bin' HEAD

# Alternative: BFG (faster)
bfg --delete-files large_file.bin
```

---

## Useful Configuration

### Global Aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'
```

### User Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Default editor
git config --global core.editor "vim"

# Default merge strategy
git config --global pull.rebase true
```

### Colors and Output

```bash
# Enable colors
git config --global color.ui true

# Set pager
git config --global core.pager "less -R"
```

---

## Quick Command Reference

| Task | Command |
|------|---------|
| **Status** | `git status` |
| **View changes** | `git diff` |
| **Sync main** | `git fetch origin && git rebase origin/main` |
| **View commits** | `git log --oneline` |
| **Stash work** | `git stash push -m "message"` |
| **Unstage file** | `git reset HEAD file.py` |
| **Undo file changes** | `git checkout -- file.py` |
| **Create worktree** | `git worktree add ../project-name -b feature/name` |
| **View branch status** | `git log main..HEAD --oneline` |
| **Amend commit** | `git commit --amend -m "new message"` |

---

## Summary

**Key Commands:**
- `git fetch origin` - Get latest
- `git rebase origin/main` - Update feature branch
- `git stash` - Save work temporarily
- `git reset --soft HEAD~1` - Undo last commit
- `git log --oneline` - View history
- `git reflog` - Find lost commits

**Most Common Issues:**
- Out of sync with main → `git rebase origin/main`
- Accidental commit → `git reset --soft HEAD~1`
- Conflicted merge → Resolve files, `git add`, `git rebase --continue`
- Need to switch quickly → `git stash` then `git checkout`
- Lost commits → `git reflog`, then recover

Practice these commands and they become second nature.
