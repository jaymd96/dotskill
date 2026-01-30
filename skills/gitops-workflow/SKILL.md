---
name: gitops-workflow
description: Git operations and branch management for iterative development. Use when creating feature branches, managing worktrees, making commits, creating pull requests, or cleaning up after merges. Integrates with Manager-Doer workflow phases.
compatibility: Requires git. GitHub CLI (gh) recommended for PR operations.
---

# GitOps Workflow

Structured Git operations integrated with the Manager-Doer development workflow. Ensures clean history, isolated development, and proper code review.

---

## Quick Reference

**Branch Creation:**
```bash
git checkout -b feature/module-name main
```

**Conventional Commit:**
```bash
git commit -m "feat(module): add core functionality"
```

**Create PR:**
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
- Managing parallel development with worktrees

---

## Core Concepts

### Branch Strategy

- **feature/{name}** - New feature development
- **fix/{description}** - Bug fixes
- **refactor/{component}** - Code improvements
- **docs/{topic}** - Documentation updates

See [references/branch-strategy.md](references/branch-strategy.md) for detailed branch management.

### Conventional Commits

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `perf`

See [references/conventional-commits.md](references/conventional-commits.md) for detailed format and examples.

### Integration with Workflow

**Phase 0:** Create branch, optional worktree
**Phase 1:** Atomic commits per step/iteration
**Phase 2:** Fix commits, optional squash
**Phase 3:** Create PR, merge, cleanup

See [references/phase-integration.md](references/phase-integration.md) for detailed phase guidance.

### Pull Requests

Quality gates checked in PR description:
- Code Quality: 0 critical issues, >= 85% zen-python
- Testing: >= 5 scenarios, 0 runtime errors
- Integration: No breaking changes
- Documentation: All public APIs documented

See [references/pull-requests.md](references/pull-requests.md) for PR creation and merge strategies.

---

## Key Principles

1. **One branch per module** - Isolation and parallel development
2. **Conventional commits** - Structured, searchable history
3. **Squash merge by default** - Clean main branch history
4. **Clean up after merge** - Delete branches and worktrees
5. **Keep history meaningful** - Atomic, logical commits

---

## Common Tasks

**Sync with main:**
```bash
git fetch origin
git rebase origin/main
```

**View branch status:**
```bash
git log main..HEAD --oneline
git diff --stat main
```

**Worktree for parallel development:**
```bash
git worktree add ../project-module-name -b feature/module-name
git worktree remove ../project-module-name
```

See [references/common-operations.md](references/common-operations.md) for more operations and error recovery.

---

## Related Resources

- **[references/branch-strategy.md](references/branch-strategy.md)** - Branch naming, creation, deletion, best practices
- **[references/conventional-commits.md](references/conventional-commits.md)** - Commit format, types, scopes, examples
- **[references/phase-integration.md](references/phase-integration.md)** - Detailed git operations for each workflow phase
- **[references/pull-requests.md](references/pull-requests.md)** - Creating PRs, merge strategies, templates
- **[references/common-operations.md](references/common-operations.md)** - Sync, stash, error recovery, troubleshooting
