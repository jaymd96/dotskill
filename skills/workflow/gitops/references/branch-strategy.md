# Branch Strategy and Management

Naming conventions, creation, and lifecycle for feature branches.

---

## Branch Naming Convention

Use prefixes to categorize branches by purpose:

```
feature/{module-name}      # New feature development
fix/{issue-description}    # Bug fixes
refactor/{component}       # Code improvements
docs/{topic}               # Documentation updates
```

### Examples

```bash
feature/dependency-graph
feature/auth-token-refresh
feature/api-rate-limiting

fix/auth-token-expiry
fix/null-pointer-exception
fix/race-condition-in-cache

refactor/catalog-resolver
refactor/simplify-api-routes
refactor/extract-validation-logic

docs/api-reference
docs/quickstart-guide
docs/troubleshooting
```

### Rules

1. **Use lowercase with hyphens** - `feature/my-module`, not `feature/MyModule` or `feature/my_module`
2. **Be descriptive but concise** - `feature/user-authentication` (good), `feature/fix-the-thing-on-line-42` (bad)
3. **Match the module or issue** - If working on the `catalog` module, use `feature/catalog-resolver`
4. **Delete after merge** - Keep repository clean, delete merged branches

---

## Branch Lifecycle

### Creating a Branch

```bash
# Update main first
git checkout main
git pull origin main

# Create new feature branch from main
git checkout -b feature/module-name

# Push to create tracking branch
git push -u origin feature/module-name
```

### Naming for Worktrees

When using worktrees for parallel development:

```bash
# Create worktree with same name as module
git worktree add ../project-module-name -b feature/module-name

# Directory names match branch names
../project-auth-system
../project-cache-layer
../project-api-versioning
```

### Keeping Branch Updated

```bash
# Rebase onto main (preferred - clean history)
git fetch origin
git rebase origin/main

# Or merge if rebasing causes issues
git merge origin/main
```

### Deleting a Branch

After merge is complete:

```bash
# Delete local branch
git branch -d feature/module-name

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/module-name

# Or use gh CLI
gh pr merge --delete-branch
```

---

## Branch Protection Rules

Recommended GitHub settings for `main` branch:

1. **Require pull request reviews** - At least 1 approval before merge
2. **Require status checks to pass** - Tests must pass
3. **Require branches to be up to date** - Rebase/merge with main before merging
4. **Require code quality checks** - Linting, coverage, etc.

Example `.github/settings.yml`:

```yaml
repository:
  name: python-quality-loop
  description: Manager-Doer workflow with quality gates
  private: false
  has_issues: true
  has_projects: true
  has_downloads: true
  has_wiki: false

  # Branch protection for main
  branch_protection_rules:
    - pattern: main
      required_approving_review_count: 1
      require_code_owner_reviews: false
      require_status_checks_to_pass: true
      require_branches_to_be_up_to_date: true
      allow_force_pushes: false
      allow_deletions: false
```

---

## Best Practices

### 1. Use Focused Branches

```bash
# Good: One module per branch
feature/auth-system      # All auth work in one branch
feature/cache-layer      # All caching work in another

# Bad: Multiple unrelated changes
feature/auth-and-caching-and-logging  # Too much scope
```

### 2. Branch per Iteration (Optional)

Some projects prefer one branch per module iteration:

```bash
feature/auth-system-v1   # Iteration 1
feature/auth-system-v2   # Iteration 2 (if major changes)

# But usually: Commits on same branch as iterations progress
# feature/auth-system
#   commit 1: Initial implementation
#   commit 2: Address feedback
#   commit 3: Final polish
```

### 3. Don't Commit to Main

```bash
# Always use feature branches
git checkout main
git pull origin main
git checkout -b feature/new-work

# Never work directly on main
# Bad: git checkout main && git commit -m "..."
```

### 4. Sync Regularly

When main receives updates:

```bash
# Don't let branch drift
git fetch origin
git rebase origin/main

# Resolve conflicts immediately, don't wait
```

### 5. Clean Up After Merge

```bash
# After PR is merged
git checkout main
git pull origin main

# Remove worktree (if used)
git worktree remove ../project-module-name

# Delete local branch
git branch -d feature/module-name

# Verify it's gone
git branch -a | grep feature/module-name  # Should be empty
```

---

## Branch Status Commands

### View Local Branches

```bash
# List local branches
git branch

# List all branches (local + remote)
git branch -a

# Show which branch is tracking
git branch -vv
```

### Compare with Main

```bash
# See commits ahead of main
git log main..HEAD --oneline

# See commits behind main
git log HEAD..main --oneline

# See files changed
git diff --stat main

# See detailed changes
git diff main
```

### Prune Stale Branches

```bash
# Clean up deleted remote branches
git fetch origin --prune

# Remove local tracking branches for deleted remote branches
git branch --merged main | grep -v main | xargs git branch -d
```

---

## Common Branch Scenarios

### Scenario 1: Fresh Start (Phase 0)

```bash
# Pull latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/new-module

# Push to create tracking
git push -u origin feature/new-module
```

### Scenario 2: Long-Running Development (Phase 1-2)

```bash
# Work on feature for several iterations
git add implementation.py
git commit -m "feat(module): implement core"

git add tests.py
git commit -m "test(module): add test coverage"

git add fixes.py
git commit -m "fix(module): address feedback"

# Keep synced with main
git fetch origin
git rebase origin/main

# Continue work
git add polish.py
git commit -m "refactor(module): polish implementation"
```

### Scenario 3: Multiple Modules (Worktrees)

```bash
# Main worktree - stays on main
cd ~/project

# Create first feature worktree
git worktree add ../project-auth -b feature/auth
cd ../project-auth
# Work on auth

# Switch to main worktree, create another
cd ~/project
git worktree add ../project-cache -b feature/cache
cd ../project-cache
# Work on cache (parallel to auth!)

# When auth done
cd ~/project
git worktree remove ../project-auth
# Continue cache work
```

---

## Troubleshooting Branches

### Accidentally Committed to Main

```bash
# Save the work
git branch feature/accidental-work

# Reset main to origin
git reset --hard origin/main

# Continue work on feature branch
git checkout feature/accidental-work
```

### Need to Switch Context Quickly

```bash
# Stash current work
git stash push -m "WIP: auth implementation"

# Switch branches
git checkout feature/cache-layer
# Do other work

# Return to auth
git checkout feature/auth
git stash pop
```

### Branch Diverged from Main

```bash
# Rebase to get clean history
git fetch origin
git rebase origin/main

# If conflicts occur
# [resolve conflicts in editor]
git add resolved-file.py
git rebase --continue

# If something goes wrong
git rebase --abort  # Start over
```

---

## Summary

**Branch Naming:**
- Prefix: `feature/`, `fix/`, `refactor/`, `docs/`
- Format: lowercase with hyphens
- Be descriptive: `feature/auth-token-refresh`

**Lifecycle:**
1. Create from main
2. Push with `-u` to set upstream
3. Keep synced with rebase
4. Delete after merge

**Best Practices:**
- One module per branch
- Sync regularly with main
- Never commit to main
- Clean up after merge
- Use worktrees for parallel work

Clean branches = clean history = easier reviews and merges.
