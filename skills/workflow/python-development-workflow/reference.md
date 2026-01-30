# Workflow Reference

Quick reference for commands, patterns, anti-patterns, and metrics.

---

## Quick Commands

| Task | Command |
|------|---------|
| Create branch | `git checkout -b feature/module-name` |
| Create playground | `touch playground/{module}_exploration.py` |
| Commit progress | `git commit -m "feat(mod): iteration N"` |
| Run tests | `pytest` |
| Check zen | Run zen-of-python skill |
| Run playground | `python playground/{module}_exploration.py` |
| Create PR | `gh pr create --title "..." --body "..."` |
| Merge and cleanup | `gh pr merge --squash --delete-branch` |

---

## Phase Overview

```
┌─────────────────────────┐
│    Phase 0: Discovery   │ ← Understand the problem (30-60 min)
│  - Branch setup         │
│  - Playground creation  │
│  - Package research     │
│  - Gap analysis         │
│  - Technical approach   │
│  - Manager approval     │
└────────────┬────────────┘
             │
    ┌────────▼────────┐
    │                 │
    │ Phase 1 Loop    │ ← Implement and iterate (1-2 hrs/iteration)
    │ (iterate 2-4x)  │
    │                 │ ← Step 1: Implementation
    │                 │ ← Step 2: Layout & Organization
    │  Manager ◄──────┤ ← Step 3: Standards (Zen)
    │ Evaluates       │ ← Step 4: Review
    │                 │ ← Step 5: Experimentation
    │                 │ ← Step 6: Testing
    └────────┬────────┘
             │
    ┌────────▼────────────┐
    │ ACCEPT / ITERATE /  │
    │ ESCALATE            │
    └────────┬────────────┘
             │
    ┌────────▼──────────────┐
    │ Phase 3: Completion   │ ← Finalize for production (30 min)
    │  - Final cleanup      │
    │  - Documentation      │
    │  - Create PR          │
    │  - Merge & cleanup    │
    └───────────────────────┘
```

---

## Iteration Decision Tree

### After Phase 1 Iteration

```
All gates pass?
├─ YES → ACCEPT
│        └─ Go to Phase 3: Completion
│
├─ FIXABLE ISSUES + Under limit?
│  └─ YES → ITERATE
│           └─ Go to Phase 2: Refinement
│           └─ Return to Phase 1 after fixes
│
└─ FUNDAMENTAL ISSUE or Limit reached?
   └─ YES → ESCALATE
            └─ Stop and reassess approach
```

### Iteration Limits

| Iteration | Expectation | Typical Feedback |
|-----------|------------|-----------------|
| 1 | Initial implementation | Broad feedback on architecture, patterns |
| 2 | Quality improvements | Focused improvements, missing edge cases |
| 3 | Polishing, minor fixes | Polish and refinement only |
| 4+ | → ESCALATE | If still issues, architectural problem |

---

## Best Practices Checklist

### For Manager

- [ ] Define gates clearly before Phase 1 starts
- [ ] Be specific in feedback (not vague)
- [ ] Evaluate against gates, not personal preference
- [ ] Enforce iteration limits consistently
- [ ] Escalate when pattern indicates fundamental issue
- [ ] Provide actionable feedback (not just criticism)
- [ ] Acknowledge what went well
- [ ] Make decisions quickly (don't leave developer waiting)

### For Developer

- [ ] Do all 6 steps in order (don't skip)
- [ ] Use the skills provided (don't improvise)
- [ ] Fix issues immediately (don't defer)
- [ ] Report honestly (don't hide problems)
- [ ] Don't expand scope without approval
- [ ] Ask for clarification if confused
- [ ] Report blockers immediately
- [ ] Follow phase sequences

### For Reviewer (if applicable)

- [ ] Evaluate independently (read the code yourself)
- [ ] Verify fixes were actually made
- [ ] Catch issues Developer might have missed
- [ ] Provide objective, specific feedback
- [ ] Report concerns to Manager
- [ ] Look for patterns across iterations
- [ ] Recommend decision to Manager

---

## Anti-Patterns and Solutions

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Skipping steps | Miss issues, lower quality | Do all 6 steps, every iteration |
| Vague feedback | Developer can't improve | Be specific: location, issue, fix |
| Lazy gate evaluation | Standards slip | Evaluate objectively against metrics |
| No iteration limit | Never-ending cycle | Set limit at start, enforce it |
| Scope creep | Takes forever | Require approval for changes |
| Silent blockers | Late surprises | Report problems immediately |
| Delayed decisions | Developer stalled | Make decision promptly |
| Perfectionism | Analysis paralysis | "Good enough" per gates is acceptable |
| Too many review cycles | Burnout risk | 2-4 iterations is healthy |
| Blame game | Team conflict | Focus on gates, not personalities |

---

## Success Metrics

### Workflow Succeeds When:

- ✅ Modules complete in 2-4 iterations
- ✅ Quality gates consistently applied
- ✅ Decisions are fast and objective
- ✅ Blockers surface early
- ✅ Time is predictable (4-10 hours per module)

### Velocity Indicators:

**Good signs:**
- Iteration 1 covers ~70% of functionality
- Manager decisions take < 1 hour
- Issues get fixed in next iteration
- Gate compliance improves per iteration
- Team confidence increases

**Red flags:**
- Iteration 1 only 20% done (scope too big)
- Decisions take days (bottleneck)
- Same issues appear multiple iterations
- Gate compliance declining
- Developer morale dropping

---

## Common Scenarios

### Scenario: Manager finds 8 issues in iteration 1

**Good response:**
ITERATE with specific feedback:
1. [Issue 1] - [location] - [fix approach]
2. [Issue 2] - [location] - [fix approach]
3. [Issue 3] - [location] - [fix approach]

Focus developer's next iteration.

**Bad response:**
ESCALATE or let them fix everything at once.

---

### Scenario: Same issue appears twice

**First time:** Fix in Phase 2 refinement.

**Second time:**
- Might indicate developer isn't reading feedback
- Consider more specific feedback
- If repeats again → investigate root cause

---

### Scenario: 3 iterations in, still failing gates

**Analysis:**
- Is scope too large?
- Are gates unrealistic?
- Is approach fundamentally wrong?

**Decision:**
- Iteration 4 → ESCALATE per policy
- Reassess scope or approach
- Consider splitting into smaller tasks

---

### Scenario: Developer requests scope change

**Process:**
1. Developer proposes change (don't implement yet)
2. Manager evaluates impact
3. Manager approves or rejects
4. If approved, add to Phase 1 tasks
5. If rejected, document and continue

**Don't:** Let developer expand scope without approval.

---

## Quality Gate Standards

### Code Quality Gates

```
✅ PASS: 0 critical issues
✅ PASS: >= 85% zen-python compliance
✅ PASS: 100% of public APIs documented
✅ PASS: Type hints on all public APIs
```

### Testing Gates

```
✅ PASS: >= 5 distinct test scenarios
✅ PASS: 0 runtime errors
✅ PASS: Edge cases identified and handled
✅ PASS: All tests pass
```

### Integration Gates

```
✅ PASS: 0 breaking changes
✅ PASS: Follows existing patterns
✅ PASS: Integrates with existing code
✅ PASS: No conflicts with other modules
```

### Documentation Gates

```
✅ PASS: All public APIs documented
✅ PASS: >= 1 usage example provided
✅ PASS: Integration points clear
✅ PASS: Edge cases explained
```

---

## Troubleshooting

### "Developer isn't making progress"

Check:
- Is the problem clear?
- Are they following all 6 steps?
- Do they need help with specific skill?
- Is scope too large?

### "Same issues keep appearing"

Check:
- Is feedback specific enough?
- Are gates clearly defined?
- Is developer following steps?
- Should we escalate?

### "Manager feedback is vague"

Request:
- Specific location in code
- What exactly needs to change
- Why it matters
- How you'd fix it

### "Phase 1 is taking forever"

Analyze:
- Is scope reasonable?
- Are iterations productive?
- Are decisions timely?
- Is developer following workflow?

---

## When to Escalate

ESCALATE (stop development) when:

1. **Architectural mismatch** - Proposed approach conflicts with system design
2. **Technology blocked** - External dependency or tool issue prevents progress
3. **Scope fundamentally wrong** - Requirements misunderstood at discovery
4. **Iteration limit reached** - 4+ iterations with continued gate failures
5. **Blocker unresolvable** - Issue that developer and manager can't solve

ESCALATE output:
- Stop active development
- Document the issue clearly
- Escalate to broader team
- Reassess approach
- Resume when unblocked

---

## More Information

- **Phase details:** See `phases/` directory
- **Templates:** See `templates.md`
- **Main workflow:** See `SKILL.md`
