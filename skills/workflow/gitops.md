---
name: gitops-workflow
description: Git operations and branch management for iterative development. Use when creating feature branches, managing worktrees, making commits, creating pull requests, or cleaning up after merges. Integrates with Manager-Doer workflow phases.
compatibility: Requires git. GitHub CLI (gh) recommended for PR operations.
---

# GitOps Workflow

Structured Git operations integrated with the Manager-Doer development workflow. Ensures clean history, isolated development, and proper code review.

## Contents

- [Quick Reference](#quick-reference) - Common commands
- [When to Use This Skill](#when-to-use-this-skill)
- [Branch Strategy](#branch-strategy) - Naming and organization
- [Worktree Management](#worktree-management) - Parallel development
- [Conventional Commits](#conventional-commits) - Commit message format
- [Commit Strategy by Phase](#commit-strategy-by-phase)
- [Pull Requests](#pull-requests) - Creating and managing PRs
- [Phase Integration](#phase-integration) - When to commit and push

## Quick Reference

### Branch Creation
```bash
git checkout -b feature/module-name main
```

### Conventional Commit
```bash
git commit -m "feat(module): add core functionality"
```

### Create PR
```bash
gh pr create --title "feat(module): description" --body "## Summary\n..."
```

---

## When to Use This Skill

Use GitOps workflow when:
- Starting a new module development (Phase 0)
- Making progress commits during development (Phase 1)
- Cleaning up history before review (Phase 2)
- Creating pull requests for merge (Phase 3)
- Cleaning up after successful merge

---

## Branch Strategy

### Branch Naming Convention

```
feature/{module-name}      # New feature development
fix/{issue-description}    # Bug fixes
refactor/{component}       # Code improvements
docs/{topic}               # Documentation updates
```

### Examples

```bash
feature/dependency-graph
fix/auth-token-expiry
refactor/catalog-resolver
docs/api-reference
```

### Rules

1. Use lowercase with hyphens
2. Be descriptive but concise
3. Match the module or issue being worked on
4. Delete after merge

---

## Worktree Management

### When to Use Worktrees

- Parallel development of multiple modules
- Keeping main branch accessible while working
- Context switching without stashing

### Create Worktree

```bash
# Create branch and worktree together
git worktree add ../project-module-name -b feature/module-name

# Or for existing branch
git worktree add ../project-module-name feature/module-name
```

### List Worktrees

```bash
git worktree list
```

### Remove Worktree

After merge:
```bash
git worktree remove ../project-module-name
```

### Best Practices

1. **Naming**: Use `project-module-name` format for worktree directories
2. **Location**: Place worktrees adjacent to main repo (`../`)
3. **Cleanup**: Always remove worktrees after merge
4. **Branch deletion**: Delete branch after worktree removal

---

## Conventional Commits

### Format

```
type(scope): description

[optional body]

[optional footer]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(catalog): add dependency resolver` |
| `fix` | Bug fix | `fix(auth): handle expired tokens` |
| `refactor` | Code change (no new feature) | `refactor(api): simplify route handlers` |
| `test` | Adding/updating tests | `test(catalog): add edge case coverage` |
| `docs` | Documentation | `docs(readme): add installation guide` |
| `chore` | Maintenance | `chore(deps): update dependencies` |
| `style` | Formatting (no code change) | `style(lint): fix whitespace` |
| `perf` | Performance improvement | `perf(query): optimize batch loading` |

### Scope

The scope should match the module or component being changed:
- `(catalog)` - Catalog module
- `(auth)` - Authentication
- `(api)` - API routes
- `(cli)` - Command line interface

### Examples

```bash
# Feature
git commit -m "feat(catalog): add version resolution with semver support"

# Bug fix
git commit -m "fix(auth): prevent token refresh race condition"

# Refactor
git commit -m "refactor(catalog): extract dependency graph to separate module"

# Test
git commit -m "test(catalog): add tests for circular dependency detection"

# Documentation
git commit -m "docs(api): document new /versions endpoint"

# With body
git commit -m "feat(catalog): add module promotion workflow

Implements the promotion workflow for moving modules between
release channels. Includes validation gates and rollback support.

Closes #123"
```

### Co-Authored Commits

When working with AI assistance:
```bash
git commit -m "feat(module): description

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Phase Integration

### Phase 0: Discovery

**Setup branch and tracking**

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/module-name

# Initial commit
git commit --allow-empty -m "chore(module-name): initialize development"

# Push branch
git push -u origin feature/module-name
```

**If using worktree**:
```bash
git worktree add ../project-module-name -b feature/module-name
cd ../project-module-name
git push -u origin feature/module-name
```

### Phase 1: Development

**Commit per development step**

```bash
# After Step 1 (Implementation)
git add -A
git commit -m "feat(module): implement core functionality"

# After Step 3 (Standards)
git add -A
git commit -m "refactor(module): apply zen-of-python improvements"

# After Step 4 (Review)
git add -A
git commit -m "fix(module): address code review findings"

# After Step 6 (Testing)
git add -A
git commit -m "test(module): add pytest coverage"
```

**Commit frequency options**:

| Strategy | When | Example |
|----------|------|---------|
| Per step | Long iterations | 6 commits per iteration |
| Per iteration | Short iterations | 1 commit with all changes |
| Logical units | Normal | 2-3 commits per iteration |

### Phase 2: Refinement

**After ITERATE feedback**

```bash
# Fix specific issues
git add -A
git commit -m "fix(module): address iteration N feedback

- Fixed edge case in validate_input()
- Added missing error handling
- Improved docstring clarity"
```

**Optional: Squash commits**

```bash
# Interactive rebase to squash (if history is messy)
git rebase -i main

# Or squash last N commits
git reset --soft HEAD~N
git commit -m "feat(module): consolidated implementation"
```

### Phase 3: Completion

**Final documentation commit**

```bash
git add -A
git commit -m "docs(module): complete documentation and examples"
```

**Create pull request**

```bash
gh pr create \
  --title "feat(module-name): Brief description" \
  --body "$(cat <<'EOF'
## Summary
- What this PR accomplishes
- Key changes made

## Quality Gates
- [x] Code Quality: 0 critical, >= 85% zen-python
- [x] Testing: >= 5 scenarios, 0 errors
- [x] Integration: No breaking changes
- [x] Documentation: Public APIs documented

## Test Plan
How to verify these changes work.

## Iteration Summary
- Iteration 1: Initial implementation
- Iteration 2: Addressed feedback on X
- Iteration 3: Final polish

## Related Issues
Closes #123
EOF
)"
```

**After PR approval**

```bash
# Merge (squash by default)
gh pr merge --squash --delete-branch

# Or via web interface for review
```

**Cleanup**

```bash
# Switch back to main
git checkout main
git pull origin main

# If worktree was used
git worktree remove ../project-module-name

# Delete local branch (if not auto-deleted)
git branch -d feature/module-name
```

---

## Pull Request Template

Save as `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Summary
<!-- Brief description of what this PR accomplishes -->

## Changes
<!-- List of key changes -->
-

## Quality Gates
- [ ] Code Quality: 0 critical issues, >= 85% zen-python compliance
- [ ] Testing: >= 5 scenarios tested, 0 runtime errors
- [ ] Integration: No breaking changes
- [ ] Documentation: All public APIs documented

## Test Plan
<!-- How to verify these changes work -->

## Iteration Summary
<!-- Summary of development iterations -->
| Iteration | Focus | Outcome |
|-----------|-------|---------|
| 1 | Initial implementation | ... |
| 2 | ... | ... |

## Related Issues
<!-- Link to related issues -->
Closes #

## Checklist
- [ ] Tests pass locally
- [ ] Code follows project conventions
- [ ] Documentation updated
- [ ] No debug code remaining
```

---

## Common Operations

### Sync with Main

```bash
# Rebase onto main (preferred)
git fetch origin
git rebase origin/main

# Or merge (if rebasing causes issues)
git merge origin/main
```

### Fix Last Commit

```bash
# Amend message
git commit --amend -m "new message"

# Add forgotten files
git add forgotten-file.py
git commit --amend --no-edit
```

### Undo Last Commit (keep changes)

```bash
git reset --soft HEAD~1
```

### View Branch Status

```bash
# See commits ahead of main
git log main..HEAD --oneline

# See files changed
git diff --stat main
```

### Stash Work in Progress

```bash
# Stash with message
git stash push -m "WIP: description"

# List stashes
git stash list

# Apply and remove
git stash pop
```

---

## Merge Strategies

### Squash Merge (Default)

All commits combined into one. Best for:
- Feature branches with messy history
- Small features
- Standard workflow

```bash
gh pr merge --squash
```

### Rebase Merge

Commits replayed on main. Best for:
- Clean, logical commit history
- When individual commits are meaningful

```bash
gh pr merge --rebase
```

### Merge Commit

Creates merge commit. Best for:
- Long-running branches
- When branch history matters

```bash
gh pr merge --merge
```

### Recommendation

Use **squash merge** by default. The PR itself serves as the historical record.

---

## Error Recovery

### Accidental Commit to Main

```bash
# Create branch with the commit
git branch feature/accidental-work

# Reset main
git reset --hard origin/main
```

### Merge Conflict

```bash
# During rebase
git rebase origin/main
# [resolve conflicts]
git add resolved-file.py
git rebase --continue

# Abort if needed
git rebase --abort
```

### Lost Commits

```bash
# Find lost commits
git reflog

# Recover specific commit
git cherry-pick <commit-hash>
```

---

## Checklist

### Starting Development
- [ ] Main is up to date
- [ ] Feature branch created with proper naming
- [ ] Branch pushed to origin
- [ ] Worktree set up (if parallel development)

### During Development
- [ ] Commits follow conventional format
- [ ] Branch synced with main regularly
- [ ] Changes are atomic and logical

### Before PR
- [ ] All tests pass
- [ ] History is clean (squash if needed)
- [ ] Documentation complete
- [ ] Branch is rebased on current main

### After Merge
- [ ] Remote branch deleted
- [ ] Local branch deleted
- [ ] Worktree removed (if used)
- [ ] Main pulled and verified

---

## Summary

GitOps integrates with the Manager-Doer workflow:

| Phase | GitOps Actions |
|-------|---------------|
| Phase 0 | Create branch, optional worktree |
| Phase 1 | Atomic commits per step/iteration |
| Phase 2 | Fix commits, optional squash |
| Phase 3 | Create PR, merge, cleanup |

**Key Principles**:
1. One branch per module
2. Conventional commits
3. Squash merge by default
4. Clean up after merge
5. Keep history meaningful
