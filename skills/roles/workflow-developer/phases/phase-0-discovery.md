# Phase 0: Discovery (Developer Perspective)

**Duration:** 30-60 minutes
**Purpose:** Understand the problem before building

For detailed workflow steps, see the [python-development-workflow skill's Phase 0](../../workflow/python-development-workflow/phases/phase-0-discovery.md).

This file focuses on developer-specific guidance.

---

## Your Discovery Tasks

### 1. Review the Codebase

Understand what already exists:
- What patterns are used? (follow them)
- Where will you integrate? (identify connection points)
- What existing code will you reuse?
- What constraints or gotchas exist?

Document findings in your discovery report.

### 2. Research Existing Packages

**Use skill:** package-research

Ask: **Does a well-maintained package already solve this?**

- Search PyPI, GitHub, awesome-lists
- Evaluate top 3-5 candidates
- Make decision: COMPOSE, EXTEND, or BUILD
- Document rationale

**Decision Checkpoint:**
```
[ ] Searched PyPI/GitHub
[ ] Evaluated candidates
[ ] Documented decision with rationale
[ ] Created llmtxt for adopted packages
```

If COMPOSE/EXTEND: Add to dependencies with pinned version.
If BUILD: Document why packages were rejected.

### 3. Document Gaps

What's missing in existing code?
- Classes/functions to create
- Functionality to implement
- Features needed
- Risks and unknowns

### 4. Create Technical Approach

Plan your implementation:
- Architecture overview
- Key components
- Implementation sequence
- Package integration (if applicable)
- Public API

### 5. Create Playground File

Create initial exploration:

```bash
mkdir -p playground
touch playground/{module}_exploration.py
```

```python
#!/usr/bin/env python3
"""Exploration of {module} functionality."""

def explore_basic_usage() -> bool:
    """Explore the primary use case."""
    # TODO: Add exploration as implementation progresses
    return True

if __name__ == "__main__":
    explore_basic_usage()
```

You'll update this throughout Phase 1.

### 6. Submit for Manager Approval

Get Manager sign-off before Phase 1:
- Share discovery report
- Include build vs compose decision
- Include technical approach
- Wait for ACCEPT before proceeding

---

## Discovery Report Template

```markdown
# Discovery Report: [Module Name]

## Gap Analysis
- Existing: [what's there]
- Needed: [what to build]
- Integration: [connection points]

## Build vs Compose Decision
Decision: [COMPOSE / EXTEND / BUILD]
Packages: [list if applicable]
Rationale: [why this choice]

## Technical Approach
- Architecture: [overview]
- Components: [key parts]
- Sequence: [build order]

## Quality Gates (Proposed)
- Code Quality: Zero critical, >= 85% zen
- Testing: >= 5 scenarios, zero errors
- Integration: No breaking changes
- Documentation: All APIs documented
```

---

## Key Points

- ✅ Don't skip package research
- ✅ Document your decisions clearly
- ✅ Get Manager approval before proceeding
- ✅ Create playground file for later exploration
- ✅ Identify integration points early

Once Manager approves, proceed to Phase 1: Development.
