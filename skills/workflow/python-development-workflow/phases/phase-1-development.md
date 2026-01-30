# Phase 1: Development Loop

**Duration:** 1-2 hours per iteration
**Repeat:** Until Manager approves (typically 2-4 iterations)

Execute 6 steps in order, each iteration. The sequence is important - each step catches different issues.

---

## Step 1: Implementation

**Skill**: python-coding

Write production code following standards:

- Type hints on public APIs
- Docstrings on public functions
- Clear, explicit names
- Follow existing patterns
- Handle edge cases

**How to know you're done:**
- Code imports without error
- Public APIs documented
- Another developer could understand it

**Output:** Updated code files

---

## Step 2: Layout & Organization

**Skill**: python-layout

Review and organize:

- Right things in right files?
- Related functions grouped?
- Imports clean and logical?
- Naming consistent?

Check against layout standards:
- `__init__.py` exports public API only
- Types in `_types.py`, exceptions in `_exceptions.py`
- Private modules prefixed with `_`
- Files under 300 lines
- Imports ordered: stdlib → third-party → local

**How to know you're done:**
- Code organized like a senior developer would
- Imports make sense
- Clear structure

**Output:** Refactored code + change notes

---

## Step 3: Standards

**Skill**: zen-of-python

Evaluate and fix Python Zen violations:

- Run zen-of-python critique
- Fix violations immediately
- Target >= 85% compliance

**Common fixes:**
- Names not explicit → Rename
- Nested logic → Guard clauses
- Implicit behavior → Make explicit
- Complex when simple works → Simplify

**How to know you're done:**
- >= 85% compliance
- All reported issues fixed
- Code reads naturally

**Output:** Compliance report + updated code

---

## Step 4: Review

**Skill**: code-review

Deep structural review:

- **CRITICAL**: Fix immediately (bugs, security, crashes)
- **MAJOR**: Fix before done (maintainability, edge cases)
- **MINOR**: Fix if time (style, optimizations)

**How to know you're done:**
- Zero critical issues
- All major issues fixed
- Code would pass peer review

**Output:** Review report + updated code

---

## Step 5: Experimentation (Dogfooding)

**Skill**: playground-exploration

Use your own code interactively:

1. Update playground file with real scenarios
2. Run `python playground/{module}_exploration.py`
3. Test happy paths, edge cases, error paths
4. Document discoveries (missing features, API friction)
5. Target >= 5 test scenarios

**Dogfooding Checklist:**
```
[ ] Playground file runs without errors
[ ] At least 5 scenarios tested
[ ] Discoveries documented with action items
[ ] API friction points noted
[ ] Missing features identified
```

This is where you find issues that formal testing misses. Your own usage reveals:
- Awkward APIs that need simplification
- Missing features you didn't anticipate
- Performance issues
- Confusing error messages

**How to know you're done:**
- >= 5 test scenarios pass
- API is usable and intuitive
- Discoveries documented

**Output:** Test scenarios + findings

---

## Step 6: Testing

**Skill**: python-testing

Write formal tests:

- Use pytest
- Cover key behaviors
- Include edge cases
- All tests pass
- No flaky tests

Convert key playground discoveries into permanent tests.

**How to know you're done:**
- Tests exist and pass
- Key behaviors covered
- No flaky tests

**Output:** Test files

---

## Commit & Report

After completing Steps 1-6:

### Step 7: Commit Changes

```bash
# Stage all changes
git add -A

# Commit with conventional message
git commit -m "feat(module-name): iteration N implementation

- [Summary of what was built/changed]
- Zen-python compliance: X%
- Test scenarios: N passed"

# Push to remote
git push
```

### Step 8: Submit Iteration Report

Submit to Manager:

```markdown
# Iteration [N] Report: [Module Name]

## Status Summary
- Implementation: [X]% complete
- Zen-Python: [Y]% compliance
- Code-Review: [C] critical, [M] major, [m] minor
- Test Scenarios: [N] tested, [N] passed

## Quality Gate Self-Evaluation
- [ ] Code Quality: [PASS/FAIL] - [details]
- [ ] Testing: [PASS/FAIL] - [details]
- [ ] Integration: [PASS/FAIL] - [details]
- [ ] Documentation: [PASS/FAIL] - [details]

## Iteration Details

### Step 1 - Implementation
[What was built]

### Step 2 - Organization
[What was reorganized]

### Step 3 - Standards
[Findings and fixes, compliance %]

### Step 4 - Review
[Critical/major issues found and fixed]

### Step 5 - Experimentation
[Test scenarios and results]

### Step 6 - Testing
[Tests written, coverage]

## Summary

### What Went Well
- [Positive 1]
- [Positive 2]

### Issues Fixed This Iteration
- [Fixed 1]
- [Fixed 2]

### Remaining Issues (if any)
- [Remaining 1]

### Blockers or Unknowns
- [Any blockers?]

## Recommendation
[ ] ACCEPT - All gates passing, ready for production
[ ] ITERATE - Specific improvements identified
[ ] ESCALATE - Fundamental issue found

If ITERATE, focus on:
1. [Item 1]
2. [Item 2]
```

---

## Manager Response

Await Manager decision:

- **ACCEPT** → Proceed to Phase 3 (Completion)
- **ITERATE** → Phase 2 (Refinement) with specific feedback
- **ESCALATE** → Stop and reassess approach

---

## Key Rules

1. **Do all 6 steps in order, every iteration**
   - Even if Step 3 seems sufficient, complete all steps
   - Each step catches different issues

2. **Fix issues immediately**
   - Don't defer to "later"
   - Action every finding

3. **Report honestly**
   - Don't hide problems
   - Be specific about issues

4. **Don't expand scope**
   - Only implement what Manager approved
   - Ask before adding features
