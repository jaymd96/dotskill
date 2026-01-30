# Phase 1: Development (Developer Perspective)

**Duration:** 1-2 hours per iteration
**Repeat:** Until Manager approves (typically 2-4 iterations)

Execute 6 steps in order, every iteration. Each step catches different issues.

For detailed workflow steps, see [python-development-workflow Phase 1](../../workflow/python-development-workflow/phases/phase-1-development.md).

---

## The 6 Steps

### Step 1: Implementation
**Skill:** python-coding

Write production code:
- Type hints on public APIs
- Docstrings on public functions
- Clear, explicit names
- Follow existing patterns
- Handle edge cases

**Done when:** Code imports, public APIs documented, readable.

### Step 2: Organization
**Skill:** python-layout

Review structure:
- Right things in right files?
- Related functions grouped?
- Imports clean and logical?
- Naming consistent?

Check layout standards:
- `__init__.py` exports public API only
- Types in `_types.py`, exceptions in `_exceptions.py`
- Private modules prefixed with `_`
- Files under 300 lines
- Imports: stdlib → third-party → local

**Done when:** Code organized like a senior dev would.

### Step 3: Standards
**Skill:** zen-of-python

Evaluate and fix:
- Run zen-of-python critique
- Fix violations immediately
- Target >= 85% compliance

Common fixes:
- Non-explicit names → Rename
- Nested logic → Guard clauses
- Implicit behavior → Make explicit
- Complex → Simplify

**Done when:** >= 85% compliance, all violations fixed.

### Step 4: Review
**Skill:** code-review

Deep structural review:
- **CRITICAL:** Fix immediately (bugs, security, crashes)
- **MAJOR:** Fix before done (maintainability, edge cases)
- **MINOR:** Fix if time (style, optimizations)

**Done when:** Zero critical, all major fixed.

### Step 5: Experimentation
**Skill:** playground-exploration

Use your own code:
1. Update playground with real scenarios
2. Run `python playground/{module}_exploration.py`
3. Test >= 5 scenarios: happy path, edge cases, errors
4. Document discoveries (missing features, API friction)

**Dogfooding Checklist:**
```
[ ] Runs without errors
[ ] At least 5 scenarios tested
[ ] Discoveries documented with actions
[ ] API friction points noted
[ ] Missing features identified
```

**Done when:** >= 5 pass, API usable.

### Step 6: Testing
**Skill:** python-testing

Write formal tests:
- Use pytest
- Cover key behaviors
- Include edge cases
- All tests pass

Convert playground discoveries into permanent tests.

**Done when:** Tests exist and pass, key behaviors covered.

---

## Commit and Report

### Commit Progress

```bash
git add -A
git commit -m "feat(module-name): iteration N implementation

- [Summary of changes]
- Zen-python: X%
- Test scenarios: N passed"

git push
```

### Submit Iteration Report

```markdown
# Iteration [N] Report: [Module Name]

## Status Summary
- Implementation: [X]% complete
- Zen-Python: [Y]% compliance
- Code-Review: [C] critical, [M] major
- Test Scenarios: [N] tested, [N] passed

## Quality Gate Self-Evaluation
- Code Quality: [PASS/FAIL] - [details]
- Testing: [PASS/FAIL] - [details]
- Integration: [PASS/FAIL] - [details]
- Documentation: [PASS/FAIL] - [details]

## What Went Well
- [Positive 1]
- [Positive 2]

## Issues Fixed
- [Fixed 1]
- [Fixed 2]

## Remaining Issues (if any)
- [Issue 1]

## Recommendation
[ ] ACCEPT - Ready for Phase 3
[ ] ITERATE - Specific improvements needed
[ ] ESCALATE - Fundamental issue
```

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
   - Be realistic about progress

4. **Don't expand scope**
   - Only implement what Manager approved
   - Ask before adding features
   - Protect the iteration limit

---

## Manager Response

Await Manager decision:

**ACCEPT** → Proceed to Phase 3: Completion
**ITERATE** → Phase 2: Refinement with specific feedback
**ESCALATE** → Stop and reassess approach

Ready to iterate? Re-read your findings and proceed to the next cycle.
