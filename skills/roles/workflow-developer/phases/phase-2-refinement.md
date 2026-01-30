# Phase 2: Refinement (Developer Perspective)

**Trigger:** Manager says ITERATE with specific feedback
**Duration:** 1-2 hours
**Key Rule:** Do ONLY what Manager flagged. Don't expand scope.

---

## What You'll Receive from Manager

```
ITERATE

Specific Improvements Needed:
1. [Issue] - [location] - [fix approach]
2. [Issue] - [location] - [fix approach]
3. [Issue] - [location] - [fix approach]

Scope: Do NOT expand beyond these items.
Iteration: [N] of [MAX]
```

---

## Your Process

### 1. Read Feedback Carefully

Understand each issue:
- What exactly is wrong?
- Where in the code?
- How should you fix it?

### 2. Make Focused Improvements

**For each issue:**
1. Change ONLY what Manager flagged
2. Don't refactor entire module
3. Don't add features
4. One change at a time

### 3. Re-Run Affected Steps

For each change:

1. **Step 1** - Adjust implementation if needed
2. **Step 2** - Check organization isn't broken
3. **Step 3** - Re-run standards on changed code
4. **Step 4** - Verify issues actually fixed
5. **Step 5** - Re-run affected playground scenarios
6. **Step 6** - Update tests if needed

### 4. Commit Fixes

```bash
git add -A
git commit -m "fix(module-name): address iteration N feedback

- [Specific fix 1]
- [Specific fix 2]
- [Specific fix 3]"

git push
```

### 5. Submit New Iteration Report

Same format as Phase 1, but focus on improvements made:

```markdown
# Iteration [N+1] Report: [Module Name]

## Improvements Made

### Issue 1: [Description]
**Location:** [File and line/function]
**Fix Applied:** [What changed and why]
**Verified:** [How tested]

### Issue 2: [Description]
**Location:** [File and line/function]
**Fix Applied:** [What changed and why]
**Verified:** [How tested]

## Updated Status

| Gate | Status | Details |
|------|--------|---------|
| Code Quality | PASS / FAIL | [Updated metrics] |
| Testing | PASS / FAIL | [Updated metrics] |
| Integration | PASS / FAIL | [Updated metrics] |
| Documentation | PASS / FAIL | [Updated metrics] |

## Recommendation
[ ] ACCEPT - All feedback addressed, gates passing
[ ] ITERATE - Additional improvements needed
```

---

## Key Points

✅ **DO:**
- Address only what Manager flagged
- Be focused and efficient
- Update tests if behavior changes
- Commit with clear messages
- Re-verify fixes work

❌ **DON'T:**
- Add new features
- Refactor unrelated code
- Skip the 6 steps for affected areas
- Hide problems
- Let scope creep happen

---

## If Confused

If Manager's feedback is unclear:

```
I'm working on the Phase 2 improvements but need clarification:

Issue: [Which feedback item?]
Confusion: [What specifically is unclear?]
My understanding: [What I think you mean]

Should I proceed this way, or did you mean something else?
```

Don't guess—ask for clarity before proceeding.

---

## Manager Response (Next Cycle)

Manager will evaluate your improvements:

**ACCEPT** → All feedback addressed, proceed to Phase 3
**ITERATE** → More improvements needed (typically rare in Phase 2)
**ESCALATE** → Fundamental issue discovered

If ITERATE again, you have limited iterations left (typically 3-4 total max).
