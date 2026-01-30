# Phase 0: Discovery

**Duration:** 30-60 minutes
**Purpose:** Understand the problem before building

Prepare thoroughly before development begins. Discovery prevents wasted effort on wrong approaches.

## Step 0.0: Branch Setup (GitOps)

```bash
# Ensure main is current
git checkout main && git pull origin main

# Create feature branch
git checkout -b feature/module-name

# Push and track
git push -u origin feature/module-name
```

---

## Step 0.1: Playground Setup (Dogfooding)

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

You'll update this throughout Phase 1 as you develop the module.

---

## Step 0.2: Context Gathering

Review the existing codebase:
- What already exists (don't reimplement)
- Architectural patterns (follow them)
- Integration points (where you connect)
- Constraints or gotchas (what to respect)

Document key findings in your discovery report.

---

## Step 0.3: Package Research (Unix Philosophy)

**Skill**: package-research

Before implementing anything, ask: **Does a well-maintained package already solve this?**

### Decision Process

1. **Define the problem** - What exactly is needed?
2. **Search packages** - PyPI, GitHub, awesome-lists
3. **Evaluate candidates** - Maintenance, API, docs, adoption
4. **Make decision** - COMPOSE, EXTEND, or BUILD
5. **Document choice** - Rationale and llmtxt for adopted packages

### Decision Checkpoint

```markdown
## Build vs Compose Decision

[ ] Searched PyPI, GitHub, awesome-lists
[ ] Evaluated at least 3 candidates (if available)
[ ] Documented decision with rationale
[ ] Created llmtxt for chosen packages (if COMPOSE/EXTEND)

Decision: [COMPOSE / EXTEND / BUILD]
Packages: [list if applicable]
Rationale: [why this choice]
```

> "Use tools in preference to unskilled help to lighten a programming task."

### If COMPOSE or EXTEND
- Add package to dependencies with pinned version
- Create llmtxt documentation (see: llmtxt-generation skill)
- Plan integration in technical approach

### If BUILD
- Document why packages were rejected
- Apply unix-philosophy principles to design

---

## Step 0.4: Gap Analysis

Document what's needed:

```markdown
## Gap Analysis: [Module Name]

### Existing Code
- [What already exists that we'll use]
- [Patterns we'll follow]

### What's Missing
- [Classes/functions to create]
- [Functionality to implement]

### Integration Points
- [Where new code connects to existing]
- [APIs we'll call or implement]

### Dependencies
- [External packages (from package research)]
- [Internal modules to import]

### Risks & Unknowns
- [What could go wrong]
- [What we don't know yet]
```

---

## Step 0.5: Technical Approach

Plan implementation:

```markdown
## Technical Approach: [Module Name]

### Architecture Overview
[ASCII diagram or description]

### Key Components
1. [Class/Function]: [Purpose]
2. [Class/Function]: [Purpose]

### Package Integration (if applicable)
- [Package]: [How we'll use it]
- [Package]: [Wrapper approach if EXTEND]

### Implementation Sequence
1. [What to build first]
2. [What depends on #1]
3. [Final integration]

### Public API
- [function(args) -> return]: [what it does]
- [function(args) -> return]: [what it does]
```

---

## Step 0.6: Initial Commit

```bash
git add -A
git commit -m "chore(module-name): initialize development

- Discovery report complete
- Package research complete
- Playground file created
- Technical approach documented"
```

---

## Step 0.7: Manager Approval

Submit discovery report to Manager:
- Include gap analysis
- Include build vs compose decision with rationale
- Include technical approach
- Wait for approval before Phase 1

Manager will evaluate and respond with:
- ACCEPT - Proceed to Phase 1
- ITERATE - Clarify/improve discovery
- ESCALATE - Fundamental concerns

Once approved, you're ready for Phase 1: Development.
