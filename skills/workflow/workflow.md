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

## Contents

- [Quick Start](#quick-start) - Getting started
- [Roles](#roles) - Manager, Developer, Reviewer
- [Quality Gates](#quality-gates-defaults) - Standards for success
- [Decision Framework](#decision-framework) - ACCEPT, ITERATE, ESCALATE
- [Phase 0: Discovery](#phase-0-discovery) - Understanding the problem
- [Phase 1: Development](#phase-1-development) - Implementation and iteration
- [Phase 2: Refinement](#phase-2-refinement) - Addressing feedback
- [Phase 3: Completion](#phase-3-completion) - Finalizing and shipping
- [GitOps Integration](#gitops-integration) - Branches, commits, PRs
- [Iteration Limits](#iteration-limits) - When to escalate
- [Examples](#examples) - Concrete workflows

---

## Quick Start

### Starting a New Module

```
1. Define the requirement clearly
2. Set quality gates (or use defaults)
3. Set iteration limit (typically 3-4)
4. Create feature branch (GitOps)
5. Create playground file (dogfooding)
6. Begin Phase 0: Discovery
```

### Workflow Overview

```
Phase 0: Discovery (30-60 min)
├── Create feature branch
├── Create playground file
├── Understand existing code
├── Package research (build vs compose)
├── Gap analysis
├── Technical approach
├── Initial commit
└── Manager approval

Phase 1: Development (1-2 hrs/iteration)
├── Step 1: Implementation
├── Step 2: Layout & Organization
├── Step 3: Standards
├── Step 4: Review
├── Step 5: Playground Exploration (dogfooding)
├── Step 6: Testing
├── Commit changes
└── Iteration report

Phase 2: Refinement (if ITERATE)
├── Focused improvements
├── Verification
├── Fix commits
└── New iteration report

Phase 3: Completion (30 min)
├── Final cleanup
├── Documentation
├── Create pull request
├── Merge and cleanup
└── Done
```

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

**All gates pass** -> Proceed to Phase 3

```
ACCEPT

All quality gates passing. Code is production-ready.

Gate Status:
  Code Quality: PASS
  Testing: PASS
  Integration: PASS
  Documentation: PASS

Proceed to Phase 3: Finalize and integrate.
```

### ITERATE

**Fixable issues, under limit** -> Return specific feedback

```
ITERATE

Gate Status:
  Code Quality: PASS
  Testing: FAIL (4 of 5 scenarios)
  Integration: PASS
  Documentation: PASS

Specific Improvements (prioritized):
1. Add error handling test scenario
   Location: tests/test_processor.py
   Approach: Test with invalid input

Scope: Do NOT expand beyond this.
Iteration: 2 of 4
```

### ESCALATE

**Fundamental issues or limit reached** -> Stop and reassess

```
ESCALATE

Issue: Architectural mismatch discovered

Details: Proposed sync approach conflicts with
         existing async architecture.

Iteration: 4 of 4 (limit reached)

Required Action: Review architecture decision
                 before continuing.
```

---

## Phase 0: Discovery

### Step 0.0: Branch Setup (GitOps)
```bash
# Ensure main is current
git checkout main && git pull origin main

# Create feature branch
git checkout -b feature/module-name

# Push and track
git push -u origin feature/module-name
```

### Step 0.1: Playground Setup (Dogfooding)
**Skill**: playground-exploration

Create initial playground file:
```bash
# Create playground directory if needed
mkdir -p playground

# Create exploration file
touch playground/{module}_exploration.py
```

Initial playground structure:
```python
#!/usr/bin/env python3
"""Exploration of {module} functionality.

Demonstrates:
1. Core API usage patterns
2. Edge cases and error handling

Run directly:
    python playground/{module}_exploration.py
"""

def explore_basic_usage() -> bool:
    """Explore the primary use case."""
    # TODO: Add exploration as implementation progresses
    return True

if __name__ == "__main__":
    explore_basic_usage()
```

### Step 0.2: Context Gathering
- Review existing codebase
- Identify patterns to follow
- Find integration points

### Step 0.3: Package Research (Unix Philosophy)
**Skill**: package-research

Before implementing, research existing solutions:

1. **Define the problem** - What exactly is needed?
2. **Search packages** - PyPI, GitHub, awesome-lists
3. **Evaluate candidates** - Maintenance, API, docs, adoption
4. **Make decision** - COMPOSE, EXTEND, or BUILD
5. **Document choice** - Rationale and llmtxt for adopted packages

**Decision Checkpoint**:
```markdown
## Build vs Compose Decision

[ ] Searched PyPI, GitHub, awesome-lists
[ ] Evaluated at least 3 candidates (if available)
[ ] Documented decision with rationale
[ ] Created llmtxt for chosen packages (if COMPOSE/EXTEND)

Decision: [COMPOSE / EXTEND / BUILD]
Packages: [list if applicable]
```

> "Use tools in preference to unskilled help to lighten a programming task."

### Step 0.4: Gap Analysis
- What exists vs. what's needed
- Dependencies (including packages from Step 0.3)
- Risks and unknowns

### Step 0.5: Technical Approach
- Architecture sketch
- Key components
- Implementation sequence
- Integration with chosen packages (if COMPOSE/EXTEND)

### Step 0.6: Initial Commit
```bash
git add -A
git commit -m "chore(module-name): initialize development

- Discovery report complete
- Package research complete
- Playground file created
- Technical approach documented"
```

### Step 0.7: Manager Approval
- Submit discovery report (including build vs compose decision)
- Wait for approval before Phase 1

---

## Phase 1: Development Loop

### Step 1: Implementation
**Skill**: python-coding

Write production code:
- Type hints on public APIs
- Docstrings on public functions
- Follow existing patterns

### Step 2: Layout & Organization
**Skill**: python-layout

Review structure against layout standards:
- `__init__.py` exports public API only
- Types in `_types.py`, exceptions in `_exceptions.py`
- Private modules prefixed with `_`
- Files under 300 lines
- Imports ordered: stdlib -> third-party -> local

### Step 3: Standards
**Skill**: zen-of-python

Check and fix:
- Evaluate against principles
- Fix violations immediately
- Target >= 85% compliance

### Step 4: Review
**Skill**: code-review

Deep review:
- Find bugs, edge cases
- Fix critical/major issues
- Document remaining minor

### Step 5: Playground Exploration (Dogfooding)
**Skill**: playground-exploration

Use your own code:
- Update playground file with real scenarios
- Run `python playground/{module}_exploration.py`
- Document discoveries (missing features, API friction)
- Test >= 5 scenarios: happy path, edge cases, errors

**Dogfooding Checklist**:
```
[ ] Playground file runs without errors
[ ] At least 5 scenarios tested
[ ] Discoveries documented with action items
[ ] API friction points noted
[ ] Missing features identified
```

This is where you find issues that formal testing misses.

### Step 6: Testing
**Skill**: python-testing

Formal tests:
- Write pytest tests
- Cover key behaviors
- All tests pass

### Step 7: Commit Iteration (GitOps)

After completing Steps 1-6:

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

### Iteration Report

Submit to Manager after Steps 1-7:

```markdown
# Iteration [N] Report

## Status
- Implementation: [X]%
- Zen-Python: [Y]%
- Issues: [C] critical, [M] major

## Gate Self-Evaluation
- Code Quality: [PASS/FAIL]
- Testing: [PASS/FAIL]
- Integration: [PASS/FAIL]
- Documentation: [PASS/FAIL]

## Summary
- What went well
- Issues fixed
- Remaining issues

## Recommendation
[ ] ACCEPT / [ ] ITERATE / [ ] ESCALATE
```

---

## Phase 2: Refinement

**Trigger**: Manager says ITERATE

### Process
1. Read Manager's specific feedback
2. Make ONLY those improvements
3. Re-run affected steps (1-6)
4. Commit fixes (GitOps)
5. Submit new iteration report

### Commit Fixes

```bash
git add -A
git commit -m "fix(module-name): address iteration N feedback

- [Specific fix 1]
- [Specific fix 2]"

git push
```

### Key Rule
Do NOT expand scope. Only fix what Manager flagged.

---

## Phase 3: Completion

**Trigger**: Manager says ACCEPT

### Step 3.1: Final Cleanup
- [ ] Remove debug code
- [ ] Complete documentation
- [ ] Run full test suite

### Step 3.2: Final Commit

```bash
git add -A
git commit -m "docs(module-name): complete documentation

- All public APIs documented
- Usage examples added
- README updated (if applicable)"

git push
```

### Step 3.3: Create Pull Request

```bash
gh pr create \
  --title "feat(module-name): Brief description" \
  --body "$(cat <<'EOF'
## Summary
Brief description of what this module accomplishes.

## Changes
- Change 1
- Change 2

## Quality Gates
- [x] Code Quality: 0 critical, >= 85% zen-python
- [x] Testing: >= 5 scenarios, 0 errors
- [x] Integration: No breaking changes
- [x] Documentation: Public APIs documented

## Test Plan
How to verify these changes work.

## Iterations
- Iteration 1: Initial implementation
- Iteration 2: [if applicable]

Closes #[issue-number]
EOF
)"
```

### Step 3.4: Merge and Cleanup

After PR approval:

```bash
# Merge with squash (recommended)
gh pr merge --squash --delete-branch

# Or via web interface

# Clean up local
git checkout main
git pull origin main

# Verify merge
git log --oneline -5
```

### Checklist
- [ ] PR created with proper description
- [ ] PR approved by reviewers
- [ ] Merged to main
- [ ] Remote branch deleted
- [ ] Local branch deleted
- [ ] Main branch pulled and verified

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

```
Phase 0:
├── gitops-workflow (Step 0.0 - branch setup)
├── playground-exploration (Step 0.1 - create playground file)
├── code-review (understand existing)
├── package-research (Step 0.3 - build vs compose)
├── llmtxt-generation (document chosen packages)
├── unix-philosophy (design principles)
└── gitops-workflow (Step 0.6 - initial commit)

Phase 1 (each iteration):
├── python-coding (Step 1 - implementation)
├── python-layout (Step 2 - organization)
├── zen-of-python (Step 3 - standards)
├── code-review (Step 4 - review)
├── playground-exploration (Step 5 - dogfooding)
├── python-testing (Step 6 - formal tests)
└── gitops-workflow (Step 7 - commit)

Phase 2:
├── [Same as Phase 1, focused]
├── playground-exploration (verify fixes)
└── gitops-workflow (fix commits)

Phase 3:
├── python-coding (finalize)
├── python-layout (final structure)
├── python-testing (verify)
├── playground-exploration (finalize, convert to tests)
└── gitops-workflow (PR, merge, cleanup)
```

### Skill Reference

| Skill | Purpose | Phase |
|-------|---------|-------|
| gitops-workflow | Branch, commit, PR, merge | 0, 1, 2, 3 |
| playground-exploration | Dogfooding, discovery, experimentation | 0, 1, 2, 3 |
| package-research | Evaluate build vs compose | 0 |
| llmtxt-generation | Document adopted packages | 0, 1 |
| unix-philosophy | Composition design principles | 0, 1 |
| python-coding | Write production code | 1, 2, 3 |
| python-layout | Organize structure, file conventions | 1, 2, 3 |
| zen-of-python | Check standards | 1, 2 |
| code-review | Quality review | 0, 1, 2 |
| python-testing | Formal tests | 1, 2, 3 |

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/start-project` | Initialize workflow |
| `/iterate` | Submit iteration report |
| `/check-status` | View all active modules |
| `/complete` | Finalize module |

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

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Skipping steps | Miss issues | Do all 6 steps |
| Vague feedback | Can't improve | Be specific |
| No iteration limit | Endless loop | Set limit upfront |
| Scope creep | Never done | Approve changes |
| Silent blockers | Late surprises | Report immediately |

---

## Templates

### Discovery Report

```markdown
# Discovery Report: [Module Name]

## Gap Analysis
- Existing: [what's there]
- Needed: [what to build]
- Dependencies: [what's required]

## Technical Approach
- Architecture: [overview]
- Components: [key parts]
- Sequence: [build order]

## Quality Gates (proposed)
- [Gate 1]
- [Gate 2]
```

### Iteration Report

```markdown
# Iteration [N] Report: [Module Name]

## Status
- Progress: [X]%
- Quality: [metrics]

## Gate Evaluation
- [Gate]: [PASS/FAIL] - [details]

## Summary
- Strengths: [what works]
- Fixed: [what improved]
- Remaining: [what's left]

## Recommendation
[ ] ACCEPT / [ ] ITERATE / [ ] ESCALATE
```

### Gate Evaluation

```markdown
# Gate Evaluation: [Module Name]

## Gates
| Gate | Status | Details |
|------|--------|---------|
| Code Quality | PASS/FAIL | [metrics] |
| Testing | PASS/FAIL | [metrics] |
| Integration | PASS/FAIL | [metrics] |
| Documentation | PASS/FAIL | [metrics] |

## Decision: [ACCEPT/ITERATE/ESCALATE]

## Feedback (if ITERATE)
1. [Item] - [location] - [fix]
```
