# Phase Integration: GitOps for Each Workflow Phase

Detailed git operations for each phase of the Manager-Doer workflow.

---

## Phase 0: Discovery

**Goal:** Set up isolated development environment.

### Without Worktree

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/module-name

# Optional: Initial empty commit for tracking
git commit --allow-empty -m "chore(module-name): initialize development"

# Push branch with tracking
git push -u origin feature/module-name
```

### With Worktree (Parallel Development)

```bash
# Create new worktree with branch
git worktree add ../project-module-name -b feature/module-name

# Navigate to worktree
cd ../project-module-name

# Push branch from worktree
git push -u origin feature/module-name

# Now work in isolation while main branch accessible
```

### Worktree Operations

```bash
# List active worktrees
git worktree list

# Switch between worktrees
cd ../project-auth            # Auth module worktree
# ... work ...
cd ../project-cache           # Cache module worktree
# ... work ...
```

### Phase 0 Checklist

- [ ] Main is up to date
- [ ] Feature branch created with proper naming
- [ ] Branch pushed to origin with tracking (`-u`)
- [ ] Worktree set up (if using parallel development)

---

## Phase 1: Development

**Goal:** Implement features with atomic, meaningful commits.

### Commit Strategy Options

| Strategy | When | Commits per Iteration |
|----------|------|------|
| **Per step** | Long iterations with distinct tasks | ~6 commits |
| **Per iteration** | Quick iterations, few changes | 1 commit |
| **Logical units** | Normal development | 2-3 commits |

### Per-Step Commits (Detailed Tracking)

```bash
# After Step 1: Implementation
git add -A
git commit -m "feat(module): implement core functionality

Adds main classes and core business logic.
- Processor class
- Config dataclass
- Basic validation"

# After Step 2: Layout
git add -A
git commit -m "refactor(module): apply code layout standards

Reorganized into standard module structure:
- _types.py for dataclasses
- _exceptions.py for error hierarchy
- _core.py for main logic"

# After Step 3: Standards
git add -A
git commit -m "refactor(module): apply zen-of-python improvements

- Explicit is better than implicit
- Simple is better than complex
- Readability counts"

# After Step 4: Code Review
git add -A
git commit -m "fix(module): address code review findings

- Added missing type hints
- Improved error messages
- Simplified edge case handling"

# After Step 5: Exploration
git add -A
git commit -m "docs(module): document findings from exploration

Added docstrings and usage examples based on
playground discoveries."

# After Step 6: Testing
git add -A
git commit -m "test(module): add comprehensive test coverage

Added pytest tests covering:
- Happy path scenarios
- Edge cases
- Error handling
- Integration"
```

### Per-Iteration Commits (Clean History)

```bash
# After entire iteration (all 6 steps)
git add -A
git commit -m "feat(module): initial implementation with tests

Implements module with comprehensive test coverage
and full documentation. Ready for review."
```

### Logical Unit Commits (Balanced)

```bash
# Implementation + exploration
git add implementation.py _types.py _exceptions.py
git commit -m "feat(module): implement core functionality"

# Code review fixes
git add -A
git commit -m "fix(module): address review feedback"

# Testing
git add tests/
git commit -m "test(module): add test coverage"
```

### Phase 1 Guidelines

**Do:**
- [ ] Commit after logical units of work
- [ ] Write meaningful commit messages
- [ ] Keep commits atomic (one idea per commit)
- [ ] Sync with main regularly (`git rebase origin/main`)
- [ ] Test each commit is buildable

**Don't:**
- [ ] Commit broken code
- [ ] Mix unrelated changes
- [ ] Use vague messages ("update stuff")
- [ ] Wait too long between commits

---

## Phase 2: Refinement

**Goal:** Address feedback and polish implementation.

### After ITERATE Feedback

```bash
# Review manager's feedback
# Fix specific issues

git add specific_file.py
git commit -m "fix(module): address iteration 1 feedback

- Fixed edge case in validate_input()
- Added missing error handling
- Improved docstring clarity"

# Can make multiple fix commits for different issues
git add another_file.py
git commit -m "fix(module): improve error messages

Makes it clearer what went wrong when validation fails."
```

### Optional: Clean Up Commit History

If history is messy, squash before PR:

```bash
# Interactive rebase to squash commits
git rebase -i main

# Or reset and recommit everything
git reset --soft main
git add -A
git commit -m "feat(module): consolidated implementation

Implements module with comprehensive tests and documentation.
Addresses all quality gate requirements.
Ready for merge."
```

### Phase 2 Checklist

- [ ] All feedback from manager addressed
- [ ] Changes properly committed
- [ ] Branch synced with main
- [ ] History is clean (optional squash)
- [ ] All tests pass

---

## Phase 3: Completion

**Goal:** Finalize and prepare for merge.

### Final Documentation Commit (Optional)

```bash
# If documentation needs final updates
git add -A
git commit -m "docs(module): complete documentation and examples

- Add comprehensive module docstring
- Add usage examples
- Add troubleshooting guide
- Add performance notes"
```

### Create Pull Request

```bash
gh pr create \
  --title "feat(module-name): Brief description" \
  --body "$(cat <<'EOF'
## Summary
Module implements core functionality with:
- Feature X
- Feature Y
- Integration with Z

## Quality Gates
- [x] Code Quality: 0 critical, >= 85% zen-python
- [x] Testing: >= 5 scenarios, 0 errors
- [x] Integration: No breaking changes
- [x] Documentation: All public APIs documented

## Test Plan
1. Run unit tests: `pytest tests/`
2. Run playground: `python playground/module_exploration.py`
3. Check coverage: `coverage report`

## Iteration Summary
| Iteration | Focus | Outcome |
|-----------|-------|---------|
| 1 | Initial implementation | Complete core features |
| 2 | Address feedback | Improved error handling |
| 3 | Final polish | Documentation complete |

## Related Issues
Closes #123
Fixes #456

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
EOF
)"
```

### Merge Strategies

**Squash Merge (Default - Recommended)**
```bash
gh pr merge --squash --delete-branch
```

Combines all commits into one clean commit on main.

**Rebase Merge (Clean history)**
```bash
gh pr merge --rebase --delete-branch
```

Replays commits as-is on main.

**Merge Commit (Long-running branches)**
```bash
gh pr merge --merge --delete-branch
```

Creates explicit merge commit.

### After Merge Cleanup

```bash
# Switch back to main
git checkout main

# Pull latest (includes your merged changes)
git pull origin main

# If using worktree
git worktree remove ../project-module-name

# Delete local branch (if not auto-deleted by --delete-branch)
git branch -d feature/module-name

# Verify cleanup
git branch -a | grep feature/module-name  # Should be empty
git worktree list                         # Should not list removed worktree
```

### Phase 3 Checklist

- [ ] All tests pass
- [ ] History is clean
- [ ] Documentation complete
- [ ] PR created with quality gates confirmed
- [ ] PR approved and merged
- [ ] Remote branch deleted
- [ ] Local branch deleted
- [ ] Worktree removed (if used)
- [ ] Main branch pulled and verified

---

## Commit Frequency Guidelines

### When to Commit

**Good commit triggers:**
- Completed a step (implementation, testing, etc.)
- Fixed a specific issue
- Refactored a component
- Added documentation

**Bad commit triggers:**
- "I changed stuff" (too vague)
- Multiple unrelated changes
- Broken code
- Broken build

### Commit Message Quality

```bash
# Good: Specific and clear
git commit -m "feat(auth): add token refresh mechanism

Implements refresh token flow with proper expiry handling.
Prevents stale authentication state."

# Bad: Vague and unclear
git commit -m "feat(auth): stuff

Made some changes to auth"

# Bad: Implementation detail only
git commit -m "feat(auth): add method"

# Good: What changed and why
git commit -m "feat(auth): add automatic token refresh

Users stay authenticated longer without manual login.
Prevents session interruptions for long-running operations."
```

---

## Syncing with Main Branch

As main branch changes, keep your feature branch updated:

```bash
# Fetch latest changes
git fetch origin

# Rebase onto main (preferred)
git rebase origin/main

# If rebase causes issues, merge instead
git merge origin/main

# Force push if you rebased (only on feature branches!)
git push --force-with-lease origin feature/module-name
```

---

## Summary by Phase

| Phase | Key Actions | Commits |
|-------|-----------|---------|
| **Phase 0** | Create branch, optional worktree | 0-1 (setup) |
| **Phase 1** | Implement, test, document | 2-6 (per step/iteration) |
| **Phase 2** | Fix feedback, polish | 1-3 (focused fixes) |
| **Phase 3** | Create PR, merge, cleanup | 0-1 (docs), then PR merge |

Clean commits at each phase make history meaningful and PRs easier to review.
