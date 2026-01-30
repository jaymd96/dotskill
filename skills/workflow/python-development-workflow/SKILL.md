---
name: python-development-workflow
description: Manager-Doer orchestrator for iterative Python development with GitOps integration. Use when developing new modules, managing quality gates, or implementing features that require structured iteration. Coordinates Manager, Developer, and Reviewer roles with quality gates, decision frameworks, and Git branch management.
---

# Python Development Workflow Orchestrator

Orchestrates iterative Python module development using the Manager-Doer pattern with quality gates, structured decision frameworks, and integrated GitOps for version control.

## Core Philosophy: Dogfooding

> "...the designer of a new system must not only be the implementor and the first large-scale user; the designer should also write the first user manual."
> -- Donald Knuth

**Be the designer, implementor, first user, AND documentation writer.**

The playground creates a continuous feedback loop:
```
Implement -> Playground Explore -> Find Issues -> Update Requirements -> Implement
```

This is NOT a one-time step -- it's continuous throughout development.

## Quick Start

Starting a new module:
1. Define the requirement clearly
2. Set quality gates (or use defaults)
3. Set iteration limit (typically 3-4)
4. Create feature branch (GitOps)
5. Create playground file (dogfooding)
6. Begin Phase 0: Discovery

### Workflow Overview

**Phase 0: Discovery** (30-60 min) - Understand the problem
**Phase 1: Development** (1-2 hrs/iteration) - Implement and iterate
**Phase 2: Refinement** (if ITERATE) - Address manager feedback
**Phase 3: Completion** (30 min) - Finalize and ship

See [phases/](phases/) for detailed phase workflows.

---

## Roles

### Manager
- Defines requirements and quality gates
- Evaluates iteration reports
- Makes ACCEPT/ITERATE/ESCALATE decisions
- Provides specific feedback

### Developer
- Investigates codebase (Phase 0)
- Implements using structured steps (Phase 1)
- Reports findings transparently
- Makes focused improvements (Phase 2)

### Reviewer
- Provides independent quality evaluation
- Verifies fixes were made
- Catches issues Developer missed
- Reports to Manager

---

## Quality Gates (Defaults)

```yaml
Code Quality:
  critical_issues: 0
  zen_compliance: ">= 85%"
  docstrings: "100% public APIs"
  type_hints: "100% public APIs"

Testing:
  scenarios_tested: ">= 5"
  runtime_errors: 0
  edge_cases: "handled"

Integration:
  breaking_changes: 0
  patterns_followed: true

Documentation:
  public_apis: "documented"
  examples: ">= 1"
```

---

## Decision Framework

### ACCEPT
**All gates pass** → Proceed to Phase 3 (Completion)

### ITERATE
**Fixable issues, under limit** → Return specific feedback for improvements

### ESCALATE
**Fundamental issues or limit reached** → Stop and reassess approach

---

## Iteration Limits

| Iteration | Expectation |
|-----------|------------|
| 1 | Initial implementation, broad feedback |
| 2 | Quality improvements, focused feedback |
| 3 | Polishing, minor fixes |
| 4+ | Escalate instead |

---

## Integration with Skills

Core skills used throughout workflow:

| Skill | Purpose | Phase |
|-------|---------|-------|
| gitops-workflow | Branch, commit, PR, merge | 0, 1, 2, 3 |
| playground-exploration | Dogfooding, discovery | 0, 1, 2, 3 |
| python-coding | Write production code | 1, 2, 3 |
| python-layout | Organize structure | 1, 2, 3 |
| python-testing | Formal tests | 1, 2, 3 |
| code-review | Quality review | 0, 1, 2 |
| package-research | Build vs compose | 0 |
| llmtxt-generation | Document packages | 0, 1 |
| unix-philosophy | Design principles | 0, 1 |

---

## Best Practices

### For Manager
- Be specific in feedback
- Evaluate against gates, not feelings
- Enforce iteration limits
- Escalate when appropriate

### For Developer
- Follow all steps in order
- Use the skills (don't improvise)
- Fix issues immediately
- Report honestly

### For Reviewer
- Evaluate independently
- Verify fixes were made
- Catch what Developer missed
- Provide actionable feedback

---

## Success Metrics

The workflow succeeds when:
- Modules complete in 2-4 iterations
- Quality gates consistently applied
- Decisions are fast and objective
- Blockers surface early
- Time is predictable (4-10 hours/module)

---

## Related Resources

- **[phases/phase-0-discovery.md](phases/phase-0-discovery.md)** - Discovery phase detailed steps
- **[phases/phase-1-development.md](phases/phase-1-development.md)** - Development loop with 6 steps
- **[phases/phase-3-completion.md](phases/phase-3-completion.md)** - Completion phase walkthrough
- **[templates.md](templates.md)** - Discovery, iteration, and gate evaluation templates
- **[reference.md](reference.md)** - Commands, anti-patterns, and detailed examples

---

## Anti-Patterns to Avoid

| Pattern | Problem | Solution |
|---------|---------|----------|
| Skipping steps | Miss issues | Do all 6 steps |
| Vague feedback | Can't improve | Be specific |
| No iteration limit | Endless loop | Set limit upfront |
| Scope creep | Never done | Approve changes |
| Silent blockers | Late surprises | Report immediately |
