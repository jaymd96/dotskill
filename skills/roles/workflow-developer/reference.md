# Developer Reference

Quick reference for anti-patterns, checklists, and success criteria.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | What to Do |
|--------------|---------|-----------|
| Skip steps | Miss issues | Do all 6 steps, every iteration |
| Manual reviews | Reinvent wheel | Use skills provided |
| Defer issues | They come back later | Fix immediately |
| Hide blockers | Surprise escalations | Report early |
| Expand scope | Never ends | Ask Manager first |
| Vague reports | Can't decide | Be specific and detailed |
| Claim perfect | Dishonest | Be honest about issues |
| Reinvent wheel | Waste time | Research packages first |
| Skip llmtxt | Forget patterns | Document adopted packages |

---

## Success Checklist (After Each Iteration)

- [ ] Steps 1-6 done in order (not skipped)
- [ ] Code follows layout conventions (Step 2)
- [ ] All findings from steps 3-4 addressed
- [ ] Playground runs without errors (Step 5)
- [ ] >= 5 scenarios tested in playground
- [ ] Discoveries documented with actions
- [ ] Tests written in step 6
- [ ] Zero runtime errors
- [ ] Report uses standard format
- [ ] Honest assessment (not sugarcoating)
- [ ] Clear recommendation (ACCEPT/ITERATE/ESCALATE)

---

## Quality Gate Targets

### Code Quality
- ✅ Zero critical issues
- ✅ >= 85% zen-of-python compliance
- ✅ 100% of public APIs documented
- ✅ Type hints on all public APIs

### Testing
- ✅ >= 5 distinct test scenarios
- ✅ Zero runtime errors
- ✅ Edge cases handled
- ✅ All tests pass

### Integration
- ✅ No breaking changes
- ✅ Follows existing patterns
- ✅ Integrates with existing code smoothly

### Documentation
- ✅ All public APIs documented
- ✅ >= 1 usage example provided
- ✅ Integration points clear
- ✅ Complex logic explained

---

## Iteration Metrics

| Iteration | Typical Feedback | Issues Count | Expectation |
|-----------|------------------|--------------|------------|
| 1 | Architecture, overall design | 5-15 | Initial implementation |
| 2 | Quality improvements, edge cases | 2-8 | Quality focus |
| 3 | Polishing, minor fixes | 0-3 | Final touches |
| 4+ | ESCALATE | — | Architectural issue |

---

## Communication Templates

### When Unsure

```
I've completed Steps 1-4 but I'm unsure about [aspect].

Issue: [Describe uncertainty clearly]
Question: [What exactly do you need?]

Should I proceed to Step 5, or wait for clarification?
```

### When Blocked

```
BLOCKER

Issue: [What's blocking progress]
Details: [Why it's blocking and what I've tried]
Options: [What could fix it]

Awaiting guidance before proceeding.
```

### Submitting Report

```
# Iteration [N] Report: [Module Name]

## Status Summary
- Implementation: [X]% complete
- Zen-Python: [Y]% compliance
- Code-Review: [C] critical, [M] major
- Test Scenarios: [N] tested

## Quality Gates
| Gate | Status | Details |
|------|--------|---------|
| Code Quality | PASS/FAIL | ... |
| Testing | PASS/FAIL | ... |
| Integration | PASS/FAIL | ... |
| Documentation | PASS/FAIL | ... |

## Summary
[What went well, what was fixed, what remains]

## Recommendation
[ ] ACCEPT / [ ] ITERATE / [ ] ESCALATE
```

---

## Decision Points

### When to Ask for Help

🤔 **Before** you spend > 15 minutes:
- Unclear requirements
- Unsure about approach
- Confused by feedback
- Missing context

### When to Report Immediately

🚨 **Without delay:**
- Blocker (cannot proceed)
- Major design problem
- Security issue
- Test framework failure

### When to Continue Silently

✅ **Keep working:**
- Normal implementation work
- Expected issues (fix them)
- Step completion
- Test writing

---

## Tips for Success

1. **Read feedback carefully** - Manager feedback is specific and actionable
2. **Fix immediately** - Don't let issues pile up
3. **Test as you go** - Verify changes work
4. **Document discoveries** - Write them down as you find them
5. **Be honest** - Report accurately, not optimistically
6. **Follow the process** - All 6 steps catch different issues
7. **Use the skills** - They're designed for this workflow
8. **Commit early and often** - Small, logical commits
9. **Playground first** - Test your code before formal tests
10. **Ask questions** - Better to clarify than guess

---

## Velocity Indicators

### Green Flags 🟢
- Iteration 1 covers ~70% of functionality
- Manager decisions come within 1 hour
- Issues get fixed next iteration
- Gate compliance improves iteration-to-iteration
- Team confidence increasing

### Red Flags 🔴
- Iteration 1 only 20% done (scope too big)
- Decisions take days (bottleneck)
- Same issues appear multiple iterations (not reading feedback)
- Gate compliance declining (wrong approach)
- Developer morale dropping

If you see red flags, raise them immediately.

---

## Remember

**"Procedures > Capability."**

The process works. Follow the steps, use the skills, report transparently. Quality follows naturally.

Your job: Execute well, report accurately, iterate based on feedback.

Manager's job: Decide what to accept or improve.

Together: Build quality code.
