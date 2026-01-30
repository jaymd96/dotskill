# Workflow Templates

Standard templates for reports, evaluations, and decisions.

---

## Discovery Report Template

Use this when submitting Phase 0 discovery findings to Manager.

```markdown
# Discovery Report: [Module Name]

## Gap Analysis

### Existing Code
- [What already exists that we'll use]
- [Patterns we'll follow]
- [Integration points identified]

### What's Missing
- [Classes/functions to create]
- [Functionality to implement]
- [Features needed]

## Build vs Compose Decision

[ ] Searched PyPI, GitHub, awesome-lists
[ ] Evaluated at least 3 candidates (if available)
[ ] Documented decision with rationale
[ ] Created llmtxt for chosen packages (if COMPOSE/EXTEND)

**Decision:** [COMPOSE / EXTEND / BUILD]

**Packages:**
- [Package 1]: [version/rationale]
- [Package 2]: [version/rationale]

**Rationale:**
- Why this approach was chosen
- Why other approaches were rejected
- Key trade-offs

## Technical Approach

### Architecture Overview
[ASCII diagram or text description of overall structure]

### Key Components
1. **[Class/Module Name]** - [Purpose and responsibility]
2. **[Class/Module Name]** - [Purpose and responsibility]
3. **[Class/Module Name]** - [Purpose and responsibility]

### Package Integration (if applicable)
- **[Package]:** [How we'll use it] / [Wrapper approach if EXTEND]
- **[Package]:** [How we'll use it]

### Implementation Sequence
1. **[Build This First]** - Foundation that others depend on
2. **[Build Second]** - Depends on #1
3. **[Build Last]** - Final integration

### Public API
- **`[function_name](args) -> ReturnType`** - [What it does]
- **`[Class.__init__](args)`** - [Constructor purpose]
- **`[method_name](args) -> ReturnType`** - [What it does]

## Quality Gates (Proposed)

Confirm or customize for this module:
- Code Quality: Zero critical issues, >= 85% zen-python
- Testing: >= 5 scenarios, zero runtime errors
- Integration: No breaking changes
- Documentation: All public APIs documented

## Estimated Effort
- Phase 1 (Development): [X hours] / [N iterations]
- Phase 2 (Refinement, if needed): [X hours]
- Phase 3 (Completion): [1 hour]
- **Total:** [X hours]

## Questions for Manager
- [If any clarification needed]
- [Any concerns about approach]
- [Any domain constraints I missed]

---

## Recommendation
Proceed to Phase 1: Development
```

---

## Iteration Report Template

Submit after completing Phase 1 Steps 1-6.

```markdown
# Iteration [N] Report: [Module Name]

## Status Summary
- **Implementation:** [X]% complete
- **Zen-Python Compliance:** [Y]%
- **Code Review Issues:** [C] critical, [M] major, [m] minor
- **Test Scenarios:** [N] tested, [N] passed

## Quality Gate Self-Evaluation

| Gate | Status | Details |
|------|--------|---------|
| Code Quality | PASS / FAIL | [Details: critical issues, compliance %] |
| Testing | PASS / FAIL | [Details: scenarios, errors, edge cases] |
| Integration | PASS / FAIL | [Details: breaking changes, patterns] |
| Documentation | PASS / FAIL | [Details: APIs documented, examples] |

## Phase 1 Steps Completed

### Step 1 - Implementation
- [What was built or modified]
- [New classes/functions added]
- [Interfaces implemented]

### Step 2 - Organization
- [Files created/refactored]
- [Module structure improvements]
- [Import ordering fixed]

### Step 3 - Standards (Zen-Python)
Compliance: [Y]%
- [Issue 1 found and fixed]
- [Issue 2 found and fixed]
- [Remaining issues, if any]

### Step 4 - Review (Code Quality)
- **Critical issues found:** [N]
  - [Issue and fix]
- **Major issues found:** [N]
  - [Issue and fix]
- **Minor issues:** [N] (documented for future)

### Step 5 - Experimentation (Playground)
Scenarios tested: [N]
- [Scenario 1: Result]
- [Scenario 2: Result]
- [Scenario 3: Result]
- [Scenario 4: Result]
- [Scenario 5: Result]

Discoveries:
- **FRICTION:** [What's awkward or hard to use]
- **MISSING:** [What feature would help]
- **EDGE CASE:** [Boundary condition found]

### Step 6 - Testing (pytest)
- Test files: [tests/test_*.py]
- Test count: [N tests]
- Coverage: [X]%
- Results: All pass / [N failures]

## Summary

### What Went Well
- [Strong point 1]
- [Strong point 2]
- [Strong point 3]

### Issues Found and Fixed
- [Issue 1: How it was fixed]
- [Issue 2: How it was fixed]

### Remaining Issues (if any)
- [Issue]: [Severity and impact]
- [Issue]: [Severity and impact]

### Discoveries for Next Iteration
- [Learning 1]
- [Learning 2]
- [Learning 3]

### Blockers or Unknowns
- [Anything blocking progress?]
- [Anything unclear?]
- [Request for guidance?]

## Metrics
- Iterations completed: [N] of [max]
- Time spent: [X hours]
- Confidence level: [High / Medium / Low]
- Ready for next phase: [Yes / No]

## Recommendation

**Choose one:**

- [ ] **ACCEPT** - All quality gates passing. Code is production-ready. Ready for Phase 3: Completion.

- [ ] **ITERATE** - Fixable issues identified. Proceed to Phase 2: Refinement.
  - **Focus areas for next iteration:**
    1. [Specific improvement needed]
    2. [Specific improvement needed]
    3. [Specific improvement needed]

- [ ] **ESCALATE** - Fundamental issue found. Stop and reassess approach.
  - **Issue:** [What's fundamentally wrong]
  - **Impact:** [Why it matters]
  - **Required:** [What needs to change]
```

---

## Phase 2 Refinement Report Template

Submit after addressing Manager feedback in Phase 2.

```markdown
# Phase 2 Refinement Report: [Module Name]

## Manager Feedback (Iteration [N])

**Feedback received:**
1. [Item 1]
2. [Item 2]
3. [Item 3]

## Changes Made

### Issue 1: [Description]
**Location:** [File and line/function]
**Fix Applied:** [What was changed and why]
**Verified:** [How it was tested]

### Issue 2: [Description]
**Location:** [File and line/function]
**Fix Applied:** [What was changed and why]
**Verified:** [How it was tested]

## Verification

- [ ] All flagged issues addressed
- [ ] No new issues introduced
- [ ] Tests still pass
- [ ] Quality gates still met
- [ ] Changes committed

## Updated Status

| Gate | Status | Details |
|------|--------|---------|
| Code Quality | PASS / FAIL | [Updated details] |
| Testing | PASS / FAIL | [Updated details] |
| Integration | PASS / FAIL | [Updated details] |
| Documentation | PASS / FAIL | [Updated details] |

## Recommendation

- [ ] **ACCEPT** - All feedback addressed, gates passing. Ready for Phase 3.
- [ ] **ITERATE** - Additional improvements needed.
  - **Next focus:**
    1. [Item]
    2. [Item]
```

---

## Gate Evaluation Template

Manager uses this to evaluate iteration reports.

```markdown
# Quality Gate Evaluation: [Module Name]

## Iteration [N] Assessment

| Gate | Required | Actual | Status |
|------|----------|--------|--------|
| Code Quality - Critical Issues | 0 | [X] | [PASS/FAIL] |
| Code Quality - Zen Compliance | >= 85% | [Y]% | [PASS/FAIL] |
| Code Quality - Documentation | 100% public | [Z]% | [PASS/FAIL] |
| Testing - Scenarios | >= 5 | [N] | [PASS/FAIL] |
| Testing - Runtime Errors | 0 | [X] | [PASS/FAIL] |
| Testing - Edge Cases | Handled | [Y] | [PASS/FAIL] |
| Integration - Breaking Changes | 0 | [X] | [PASS/FAIL] |
| Integration - Patterns Followed | Yes | [Y] | [PASS/FAIL] |
| Documentation - APIs | Yes | [Y] | [PASS/FAIL] |
| Documentation - Examples | >= 1 | [N] | [PASS/FAIL] |

## Summary

**All gates pass:** [Yes / No]
**Iteration limit:** [N] of [max]

## Decision

**Choose one:**

### ACCEPT
All quality gates passing. Code is production-ready. Proceed to Phase 3: Completion.

### ITERATE
Fixable issues identified. Provide specific feedback:

1. **Issue:** [What needs to be fixed]
   **Location:** [Where in the code]
   **Approach:** [How to fix it]
   **Scope:** Do NOT expand beyond this.

2. **Issue:** [What needs to be fixed]
   **Location:** [Where in the code]
   **Approach:** [How to fix it]

**Iteration:** [N+1] of [max]

Return to Phase 2: Refinement.

### ESCALATE
Fundamental issues found. Stop and reassess.

**Issue:** [What's fundamentally wrong]
**Details:** [Why it matters]
**Action:** [What needs to happen]
```

---

## Using These Templates

1. **Copy and paste** - Take the template that matches your need
2. **Fill in sections** - Complete all bracketed sections
3. **Be specific** - Replace placeholders with actual details
4. **Include metrics** - Numbers and percentages support decisions
5. **Be honest** - Accurate reporting enables good decisions

Templates help maintain consistency and ensure all important information is communicated clearly.
