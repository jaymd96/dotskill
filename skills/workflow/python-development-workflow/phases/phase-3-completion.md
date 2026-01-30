# Phase 3: Completion

**Trigger:** Manager says ACCEPT
**Duration:** ~30 minutes

Finalize code and prepare for production integration.

---

## Step 3.1: Final Cleanup

Prepare code for production:

- [ ] Remove all debug code
- [ ] Remove console.log or print statements (except logging)
- [ ] Remove commented-out code
- [ ] Complete all docstrings
- [ ] Remove TODOs without context
- [ ] Clean up test fixtures
- [ ] Verify production-ready

---

## Step 3.2: Final Documentation

Ensure complete documentation:

- [ ] All public APIs documented
- [ ] Type hints complete on public APIs
- [ ] Usage examples provided
- [ ] Complex logic explained
- [ ] README updated (if applicable)
- [ ] Edge cases documented
- [ ] Performance notes added (if relevant)

---

## Step 3.3: Final Testing

Run comprehensive tests:

```bash
# Run full test suite
pytest

# Check coverage
pytest --cov=src

# Type check
mypy src

# Lint check
ruff check src
```

Verify:
- [ ] All tests pass
- [ ] No type errors
- [ ] No lint issues
- [ ] Integration verified

---

## Step 3.4: Final Commit

```bash
git add -A
git commit -m "docs(module-name): complete documentation

- All public APIs documented
- Usage examples added
- README updated (if applicable)
- Final cleanup complete"

git push
```

---

## Step 3.5: Create Pull Request

Use GitHub CLI to create PR:

```bash
gh pr create \
  --title "feat(module-name): Brief description" \
  --body "$(cat <<'EOF'
## Summary
Brief description of what this module accomplishes.

## Changes
- Change 1
- Change 2
- Change 3

## Quality Gates
- [x] Code Quality: 0 critical, >= 85% zen-python
- [x] Testing: >= 5 scenarios, 0 errors
- [x] Integration: No breaking changes
- [x] Documentation: Public APIs documented

## Test Plan
How to verify these changes work:
1. Step 1
2. Step 2
3. Expected result

## Iterations
- Iteration 1: Initial implementation
- Iteration 2: [if applicable]

Closes #[issue-number]
EOF
)"
```

### PR Checklist

- [ ] Title follows conventional commit format
- [ ] Description is clear and concise
- [ ] Quality gate checkboxes all marked
- [ ] Test plan is clear
- [ ] Related issue is referenced

---

## Step 3.6: Code Review

Share PR with reviewers:

- Get approval from at least one other person
- Address any final concerns
- Make sure reviewers understand the changes

Reviewers should verify:
- [ ] Code quality gates pass
- [ ] Tests are comprehensive
- [ ] Documentation is complete
- [ ] No breaking changes
- [ ] Follows project conventions

---

## Step 3.7: Merge and Cleanup

After PR approval:

```bash
# Merge with squash (recommended for clean history)
gh pr merge --squash --delete-branch

# Or merge without squash if preserving commit history is important
# gh pr merge --create-commit --delete-branch

# Verify local
git checkout main
git pull origin main

# Check latest commits
git log --oneline -5
```

### Merge Checklist

- [ ] PR approved
- [ ] All CI checks passing
- [ ] Branch merged to main
- [ ] Remote branch deleted
- [ ] Local merged branch deleted
- [ ] Main branch pulled and verified
- [ ] Latest commit visible in `git log`

---

## Success Criteria

Phase 3 is complete when:
- ✅ Code is production-ready
- ✅ Documentation is complete
- ✅ All tests pass
- ✅ PR is approved and merged
- ✅ Changes are on main branch
- ✅ No outstanding issues

---

## Common Issues

### PR Merge Conflicts
1. Update local main: `git checkout main && git pull`
2. Rebase feature branch: `git rebase main`
3. Resolve conflicts
4. Force push: `git push --force-with-lease`
4. Retry merge

### Test Failures in PR
1. Check CI error logs
2. Reproduce locally: `pytest`
3. Fix issues on feature branch
4. Push: `git push`
5. CI re-runs automatically

### Approval Delays
- Check if reviewers need clarification
- Add comments explaining complex parts
- Offer to walk through changes live
- Set deadline if needed

---

## After Completion

Once merged:

1. **Verify on main**
   - Pull latest: `git pull origin main`
   - Verify your changes are there
   - Update local branches: `git branch -a`

2. **Clean up**
   - Delete old feature branches locally and remotely
   - Archive any temporary files
   - Update tracking board (if using)

3. **Document lessons learned**
   - What went well?
   - What would you do differently?
   - What did you learn?

4. **Celebrate!**
   - You shipped it! 🎉

---

## Module Complete Checklist

- [ ] Code merged to main
- [ ] Tests all pass on main
- [ ] Documentation complete and accessible
- [ ] No outstanding issues or TODOs
- [ ] Integration verified
- [ ] Ready for production use

Your module is now complete and ready for use by the rest of the project.
