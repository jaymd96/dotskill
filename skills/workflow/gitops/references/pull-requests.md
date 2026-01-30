# Pull Requests: Creation, Reviews, and Merging

Creating effective pull requests and managing the review process.

---

## Creating a Pull Request

### Using GitHub CLI (gh)

```bash
gh pr create \
  --title "feat(module-name): Brief description" \
  --body "## Summary\n- What this PR does\n- Key changes"
```

### Full PR Creation Example

```bash
gh pr create \
  --title "feat(catalog): add dependency resolution with semver support" \
  --body "$(cat <<'EOF'
## Summary
Implements semver-aware version resolution for dependencies.
Handles pre-release versions and version ranges correctly.

## Changes
- Added SemVer parser and resolver
- Integrated with existing dependency graph
- Added caching for performance

## Quality Gates
- [x] Code Quality: 0 critical issues, >= 85% zen-python compliance
- [x] Testing: 5 test scenarios, 0 runtime errors
- [x] Integration: No breaking changes to public API
- [x] Documentation: All public APIs documented with examples

## Test Plan
1. Run unit tests: `pytest tests/test_catalog.py`
2. Run integration tests: `pytest tests/integration/`
3. Run playground: `python playground/catalog_exploration.py`
4. Check specific behavior:
   - Semver ranges parsed correctly
   - Pre-release versions handled
   - Circular dependencies detected
   - Performance acceptable (< 1s for 1000 items)

## Iteration Summary
| Iteration | Focus | Changes |
|-----------|-------|---------|
| 1 | Core resolver + tests | 450 lines, 12 tests |
| 2 | Add caching + benchmarks | 100 lines, 3 performance tests |
| 3 | Documentation + examples | 80 lines, 5 usage examples |

## Related Issues
Closes #123
Fixes #456

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
EOF
)"
```

### Web Interface Alternative

```bash
# Push branch and follow link
git push origin feature/module-name

# Visit GitHub and create PR via web UI
# Provides better UI for large descriptions
```

---

## Pull Request Template

Save in `.github/PULL_REQUEST_TEMPLATE.md`:

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
Fixes #

## Checklist
- [ ] Tests pass locally
- [ ] Code follows project conventions
- [ ] Documentation updated
- [ ] No debug code remaining
```

---

## Quality Gates in PR Description

Always confirm these before creating PR:

### Code Quality
```
- [ ] Code Quality: 0 critical issues, >= 85% zen-python compliance
```

Verify with:
```bash
# Style checking
pylint module/
flake8 module/

# Type hints
mypy module/
```

### Testing
```
- [ ] Testing: >= 5 scenarios tested, 0 runtime errors
```

Verify with:
```bash
# Run tests
pytest tests/

# Coverage
coverage run -m pytest
coverage report

# Manual testing
python playground/module_exploration.py
```

### Integration
```
- [ ] Integration: No breaking changes
```

Verify with:
```bash
# Check if existing tests still pass
pytest tests/

# Manual test with dependent code
# If API changed, verify backward compatibility
```

### Documentation
```
- [ ] Documentation: All public APIs documented
```

Verify with:
```bash
# Check docstrings
python -m pydoc module

# Verify examples work
python -c "from module import X; help(X)"
```

---

## Review Process

### Requesting Review

```bash
# Add reviewers
gh pr edit <number> --add-reviewer @username

# Or when creating
gh pr create --reviewer @username
```

### Responding to Feedback

When reviewer suggests changes:

1. **Understand the feedback** - Ask clarifying questions
2. **Make changes** - Update code as needed
3. **Commit** - Add new commit(s) with changes
4. **Push** - `git push origin feature/module-name`
5. **Respond** - Reply in PR thread explaining changes

```bash
# Don't amend/rebase after review started
# New commits appear in PR and reviewers see what changed

git add fixed_file.py
git commit -m "fix(module): address review feedback on validation

- Added bounds checking
- Improved error message clarity"

git push origin feature/module-name
```

### Re-requesting Review

After making changes:
```bash
# Re-request review from reviewer
gh pr review --request-review @username
```

---

## Merge Strategies

### Squash Merge (Recommended)

Best for feature branches with lots of commits:

```bash
# All commits become one clean commit
gh pr merge --squash

# Deletes remote branch
gh pr merge --squash --delete-branch
```

**Use when:**
- Feature branch has 5+ commits
- Commit history is mainly incremental fixes
- Want clean main branch history

**Example:**
```
Before merge:
  main: [A] [B] [C]
  feature: [A] [feat] [fix] [docs] [polish]

After squash merge:
  main: [A] [B] [C] [feature_complete]
```

### Rebase Merge

Keep individual commits clean:

```bash
# Replays commits on main
gh pr merge --rebase

# Delete branch
gh pr merge --rebase --delete-branch
```

**Use when:**
- Individual commits are meaningful
- Want to preserve commit history
- Commits are already clean

**Example:**
```
Before merge:
  main: [A] [B] [C]
  feature: [A] [feat] [fix] [docs]

After rebase merge:
  main: [A] [B] [C] [feat] [fix] [docs]
```

### Merge Commit

Creates explicit merge commit:

```bash
# Creates merge commit
gh pr merge --merge

# Delete branch
gh pr merge --merge --delete-branch
```

**Use when:**
- Long-running feature branches
- Want to preserve merge history
- Branch represents major work

**Example:**
```
Before merge:
  main: [A] [B] [C]
  feature: [A] [feat] [fix] [docs]

After merge:
  main: [A] [B] [C] [merge: feature]
               └─[feat] [fix] [docs]
```

### Recommendation

**Default: Squash merge**

Reasons:
- Clean main branch history
- PR itself serves as historical record
- Easier to find bugs with git bisect
- Simpler for CI/CD

---

## Handling Review Conflicts

### When Reviewer Asks for Major Changes

If feedback is substantial:

```bash
# Discuss with reviewer first
# Make changes in new commits (don't amend)

git add changed_files.py
git commit -m "refactor(module): major restructuring per review feedback"

# Let reviewer see the evolution
# They understand why changes were made
```

### When PR Gets Out of Sync with Main

If main has new changes:

```bash
# Rebase onto main to update PR
git fetch origin
git rebase origin/main

# Force push (safe on feature branches)
git push --force-with-lease origin feature/module-name

# PR automatically updates, shows new changes in main
```

### When Multiple People Working on Same Module

Not recommended, but if necessary:

```bash
# Coordinate commits
# Use atomic, non-overlapping changes
# Communicate frequently

# Rebase frequently to stay in sync
git fetch origin
git rebase origin/main
git push --force-with-lease
```

---

## After Merge

### Local Cleanup

```bash
# Switch to main
git checkout main

# Pull latest (includes merged PR)
git pull origin main

# Delete local feature branch
git branch -d feature/module-name

# Verify
git branch -a | grep feature/module-name  # Should be empty
```

### Verify Merge

```bash
# Check that main includes your changes
git log main --oneline | head -5

# Verify merged PR
gh pr list --state merged | head -5
```

### Deploy or Continue

After successful merge:

1. **Update main locally** - `git pull origin main`
2. **Next module** - Create new feature branch for next work
3. **Monitor** - Check that CI/CD passes
4. **Announce** - Let team know feature is merged

---

## Best Practices

### Before Creating PR
- [ ] All tests pass locally
- [ ] Code follows style guide
- [ ] Documentation complete
- [ ] No debug code or commented-out sections
- [ ] Branch is up-to-date with main

### In PR Description
- [ ] Clear, descriptive title
- [ ] Comprehensive summary
- [ ] Quality gates confirmed
- [ ] Test plan provided
- [ ] Related issues linked

### During Review
- [ ] Respond to feedback promptly
- [ ] Make changes in new commits (don't amend)
- [ ] Ask clarifying questions
- [ ] Update based on feedback quickly

### After Approval
- [ ] Use consistent merge strategy
- [ ] Delete remote branch
- [ ] Delete local branch
- [ ] Update main
- [ ] Verify merge successful

---

## Summary

**Creating PR:**
```bash
gh pr create --title "feat(module): description" --body "## Summary\n..."
```

**Quality Gates:** Code quality, Testing, Integration, Documentation

**Responding to Feedback:** Make changes, commit, push - don't amend

**Merge Strategy:** Squash merge by default for clean history

**After Merge:** Update main, delete branches, cleanup

Effective PRs make code review easier and maintain clean history.
