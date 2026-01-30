# Conventional Commits

Structured commit message format for searchable, meaningful history.

---

## Format

```
type(scope): description

[optional body]

[optional footer]
```

### Example

```
feat(catalog): add dependency resolution with semver support

Implements semver-aware version resolution for dependencies.
Handles pre-release versions and version ranges.

Closes #123
Fixes #456
```

---

## Commit Types

| Type | Description | When to Use |
|------|-------------|------------|
| `feat` | New feature | Adding new functionality |
| `fix` | Bug fix | Fixing a bug or issue |
| `refactor` | Code change (no new feature) | Restructuring without changing behavior |
| `test` | Adding/updating tests | Adding test coverage |
| `docs` | Documentation | Docstrings, READMEs, guides |
| `chore` | Maintenance | Dependencies, build config |
| `style` | Formatting (no code change) | Whitespace, formatting, linting |
| `perf` | Performance improvement | Optimization, caching, efficiency |

### Examples by Type

**Feature:**
```bash
git commit -m "feat(catalog): add version resolution with semver support"
git commit -m "feat(api): add /health endpoint for monitoring"
git commit -m "feat(cli): add --verbose flag for detailed output"
```

**Bug Fix:**
```bash
git commit -m "fix(auth): prevent token refresh race condition"
git commit -m "fix(cache): handle null values correctly"
git commit -m "fix(parser): handle edge case in date parsing"
```

**Refactor:**
```bash
git commit -m "refactor(catalog): extract dependency graph to separate module"
git commit -m "refactor(api): simplify route handlers"
git commit -m "refactor(core): rename Config to AppConfig for clarity"
```

**Test:**
```bash
git commit -m "test(catalog): add tests for circular dependency detection"
git commit -m "test(auth): add edge case coverage for token expiry"
git commit -m "test(cache): verify concurrent access handling"
```

**Documentation:**
```bash
git commit -m "docs(api): document new /versions endpoint"
git commit -m "docs(readme): add installation guide"
git commit -m "docs(module): add usage examples"
```

**Maintenance:**
```bash
git commit -m "chore(deps): update pytest to 7.0"
git commit -m "chore(build): configure github actions"
git commit -m "chore(docs): update contributing guide"
```

**Style:**
```bash
git commit -m "style(lint): fix whitespace in core.py"
git commit -m "style(format): run black on all modules"
```

**Performance:**
```bash
git commit -m "perf(query): optimize batch loading with caching"
git commit -m "perf(parser): use compiled regex for validation"
```

---

## Scope

Scope identifies which module or component changed:

```bash
feat(catalog)      # Catalog module
feat(auth)         # Authentication module
feat(api)          # API routes
feat(cli)          # Command-line interface
feat(core)         # Core functionality
feat(db)           # Database layer
feat(utils)        # Utility functions
```

**Rules:**
- Match the actual module/component
- Keep concise (1-2 words)
- Use lowercase
- Match folder or file names

### Multi-Component Changes

If a change affects multiple components, use the most significant one:

```bash
# If both models and API changed, but API is primary
feat(api): update user endpoints to use new model

# Include affected areas in body
feat(core): restructure initialization

Models: User, Post
API: Routes /users, /posts
Migration: Add version field
```

---

## Description (Subject)

Keep it concise and clear:

```bash
# Good: Specific and actionable
feat(auth): add token refresh with exponential backoff

# Bad: Vague
feat(auth): improve authentication

# Good: Clear what was done
fix(cache): handle expired entries on access

# Bad: Unclear
fix(cache): stuff doesn't work
```

**Rules:**
- Imperative mood: "add", not "added" or "adds"
- No period at end
- First letter lowercase (after type/scope)
- Under 72 characters is ideal
- Describe WHAT, not WHY (that goes in body)

---

## Message Body (Optional)

Use when more context is needed:

```bash
git commit -m "feat(catalog): add module promotion workflow

Implements the promotion workflow for moving modules between
release channels. Includes validation gates and rollback support.

Key features:
- Pre-promotion validation
- Atomic promotion operations
- Rollback capability if validation fails
- Audit logging of all promotions"
```

**Guidelines:**
- Explain WHY this change was made
- List key features or changes
- Reference issues/PRs
- Wrap at 72 characters
- Blank line between subject and body

---

## Footer (Optional)

Use footers to reference issues and breaking changes:

```bash
git commit -m "feat(api): redesign user endpoint

Closes #123
Fixes #456
Related to #789"
```

### Footer Keywords

**Closes/Fixes:**
```bash
Closes #123        # Closes an issue
Fixes #456         # Fixes a bug
Resolves #789      # Resolves an issue
```

**Breaking Change:**
```bash
BREAKING CHANGE: Removed /v1/users endpoint

Migration: Use /v2/users with new schema
```

---

## AI Co-Authored Commits

When working with AI assistance:

```bash
git commit -m "feat(module): description of changes

Co-Authored-By: Claude <noreply@anthropic.com>"
```

Or with full context:

```bash
git commit -m "feat(module): add core functionality

Implemented using iterative feedback from code review.
Includes comprehensive test coverage and documentation.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Real-World Examples

### Simple Feature

```
feat(auth): add password reset workflow
```

### Feature with Details

```
feat(catalog): add dependency resolution with semver support

Implements semver-aware version resolution for dependencies.
Handles pre-release versions and version ranges properly.

Features:
- SemVer range parsing
- Pre-release version handling
- Caching for performance

Closes #123
```

### Bug Fix

```
fix(cache): prevent stale data when TTL expires

Stale entries were being returned instead of refreshed.
Added expiry check on access and background cleanup.

Fixes #456
```

### Refactoring

```
refactor(api): extract common validation logic

Reduces duplication across route handlers.
Improves maintainability and consistency.

Related to #789
```

### Multi-line with Breaking Change

```
feat(api): redesign user endpoints for consistency

BREAKING CHANGE: Old /v1/users endpoints removed

Migration guide:
- /v1/users/list → /v2/users
- /v1/users/{id} → /v2/users/{id}
- /v1/users/create → POST /v2/users

New endpoints include better filtering and pagination.

Closes #999
```

---

## Commit Message Checklist

Before committing:

- [ ] Type is correct (feat, fix, refactor, etc.)
- [ ] Scope matches actual component
- [ ] Description is clear and concise
- [ ] Imperative mood (add, not added)
- [ ] No period at end of subject
- [ ] Body explains WHY, not WHAT
- [ ] Related issues referenced in footer
- [ ] Co-authored by if AI assisted

---

## Tools and Automation

### Pre-commit Hook

Validate commit messages:

```bash
# Create .git/hooks/commit-msg
#!/bin/bash
# Validate conventional commit format

MSG=$(cat "$1")
if ! echo "$MSG" | grep -E '^(feat|fix|refactor|test|docs|chore|style|perf)(\(.+\))?:.{1,}' > /dev/null; then
    echo "Commit message must follow conventional commit format"
    echo "Example: feat(scope): description"
    exit 1
fi
```

### commitizen (Python)

Install and use:

```bash
pip install commitizen
cz commit  # Interactive commit dialog
```

### Commitlint

JavaScript tool that works with any project:

```bash
npm install commitlint
echo "conventional" > commitlint.config.js
```

---

## Summary

**Format:**
```
type(scope): description

[body]

[footer]
```

**Types:** feat, fix, refactor, test, docs, chore, style, perf

**Scope:** Module or component (catalog, auth, api, etc.)

**Description:** Clear, concise, imperative mood

**Body:** Explain WHY, list key changes

**Footer:** Reference issues, breaking changes

Conventional commits make history searchable and meaningful for developers and tooling.
