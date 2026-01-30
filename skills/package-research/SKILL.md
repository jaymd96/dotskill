---
name: package-research
description: Research existing packages before implementing from scratch. Use when starting new features, adding dependencies, or evaluating build vs compose decisions. Guides systematic package discovery, evaluation, and documentation.
---

# Package Research Skill

Research existing packages before implementing from scratch. Embodies the Unix philosophy: "Use tools in preference to unskilled help."

## Core Philosophy

> "Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them."

Before writing code, ask: **Does a well-maintained package already solve this?**

---

## When to Use This Skill

- Starting work on a new feature or module
- Phase 0: Discovery (before implementation planning)
- Adding new functionality to existing code
- Evaluating "build vs buy" decisions
- Encountering a problem domain you haven't worked in before

---

## Quick Reference

```
1. Define the Problem     -> What exactly do you need?
2. Search for Packages    -> PyPI, GitHub, awesome-lists
3. Create Shortlist       -> 3-5 candidates max
4. Evaluate Candidates    -> Maintenance, API, docs, adoption
5. Make Decision          -> Build, compose, or extend
6. Document Choice        -> Create llmtxt for chosen packages
```

---

## Step 1: Define the Problem

Before searching, clearly articulate what you need:

```markdown
## Problem Definition

### Need
[One sentence: what functionality is required]

### Constraints
- Python version: [e.g., 3.11+]
- License: [e.g., permissive only]
- Dependencies: [e.g., minimal, no heavy frameworks]
- Performance: [e.g., must handle 10k items/sec]

### Scope
- Must have: [essential features]
- Nice to have: [optional features]
- Out of scope: [explicitly exclude]
```

**Key Question**: Is this a well-known problem domain (e.g., HTTP, JSON, dates) or novel?

- **Well-known**: Almost certainly use a package
- **Novel**: May need to implement, but still search first

---

## Step 2: Search for Packages

### Primary Sources

1. **PyPI** - Python Package Index
   ```
   Search: https://pypi.org/search/?q=<term>
   API: https://pypi.org/pypi/<package>/json
   ```

2. **GitHub**
   - Search repositories by language:python
   - Look at Stars, Issues, Last commit
   - Check the `Insights > Contributors` tab

3. **Awesome Lists**
   - `awesome-python` - Curated Python libraries
   - Domain-specific awesome lists (awesome-fastapi, etc.)

4. **Documentation Sites**
   - Read the Docs - Often has related packages
   - Official library docs often recommend alternatives

### Search Strategies

```markdown
## Search Terms Used

### Direct Terms
- [exact functionality, e.g., "rate limiting"]

### Alternative Terms
- [synonyms, e.g., "throttling", "backpressure"]

### Domain Terms
- [industry terms, e.g., "token bucket", "leaky bucket"]

### Combined Terms
- [python + functionality, e.g., "python async rate limiter"]
```

### What to Look For

| Signal | Good | Bad |
|--------|------|-----|
| Last commit | < 6 months | > 2 years |
| Open issues | Actively triaged | 100s ignored |
| Contributors | Multiple | Single, inactive |
| Documentation | Comprehensive | None or outdated |
| Test coverage | Visible CI/CD | No tests mentioned |
| License | Clear, permissive | Unclear or restrictive |

---

## Step 3: Create Shortlist

Narrow to 3-5 candidates maximum:

```markdown
## Package Shortlist

### 1. [package-name]
- **PyPI**: https://pypi.org/project/package-name/
- **GitHub**: https://github.com/org/package-name
- **Stars**: X,XXX | **Last Commit**: YYYY-MM-DD
- **License**: MIT/Apache/etc.
- **One-liner**: [What it does]

### 2. [package-name-2]
...

### 3. [package-name-3]
...
```

### Elimination Criteria

Immediately eliminate packages that:
- Have no commits in 2+ years (unless stable/complete)
- Have unclear or incompatible licenses
- Have no documentation
- Have unresolved critical security issues
- Don't support your Python version

---

## Step 4: Evaluate Candidates

### Evaluation Matrix

| Criteria | Weight | Package A | Package B | Package C |
|----------|--------|-----------|-----------|-----------|
| Maintenance | 25% | | | |
| API Design | 25% | | | |
| Documentation | 20% | | | |
| Adoption | 15% | | | |
| Dependencies | 15% | | | |
| **Total** | 100% | | | |

### Scoring Guide

**Maintenance (25%)**
- 5: Active development, responsive maintainers
- 3: Stable, occasional updates
- 1: Abandoned or single maintainer, no response

**API Design (25%)**
- 5: Pythonic, intuitive, well-typed
- 3: Functional but verbose or inconsistent
- 1: Awkward, undocumented, or unsafe

**Documentation (20%)**
- 5: Complete API docs + tutorials + examples
- 3: API docs exist, basic examples
- 1: README only or outdated docs

**Adoption (15%)**
- 5: Industry standard, many dependents
- 3: Moderate usage, known in community
- 1: Minimal adoption, few dependents

**Dependencies (15%)**
- 5: Minimal, well-maintained deps
- 3: Reasonable deps, no conflicts
- 1: Heavy deps or known conflicts

### Hands-On Evaluation

For top 1-2 candidates, actually try them:

```python
# Quick evaluation script
# Install: pip install <package>

from package import main_feature

# Test 1: Basic usage
result = main_feature.do_thing()

# Test 2: Error handling
try:
    main_feature.do_bad_thing()
except ExpectedException:
    pass  # Good: Clear exception

# Test 3: Edge case
result = main_feature.do_thing(edge_case_input)
```

---

## Step 5: Make Decision

### Decision Options

#### COMPOSE: Use existing package(s)
Choose when:
- Package scores >= 4.0 overall
- Active maintenance
- API fits your needs (80%+ coverage)
- Documentation is adequate

**Action**: Add to dependencies, create llmtxt documentation

#### EXTEND: Use package with wrapper
Choose when:
- Package core is solid but API needs adaptation
- Missing features are easily added
- Wrapper is thin (< 100 lines)

**Action**: Add to dependencies, create thin wrapper, document why

#### BUILD: Implement from scratch
Choose when:
- No suitable packages exist
- All candidates score < 3.0
- Unique requirements not met by any package
- Package would be heavier than custom solution

**Action**: Implement, document why packages were rejected

### Decision Document

```markdown
## Package Research Decision

### Requirement
[What was needed]

### Decision: [COMPOSE / EXTEND / BUILD]

### Rationale
[Why this decision was made]

### If COMPOSE/EXTEND:
- Package: [name]
- Version: [pinned version]
- Why this package: [key reasons]
- Alternatives rejected: [with reasons]

### If BUILD:
- Packages evaluated: [list]
- Why all rejected: [reasons]
- Estimated effort: [hours/days]

### Risk Assessment
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]
```

---

## Step 6: Document Choice

### For COMPOSE/EXTEND Decisions

Create llmtxt documentation for chosen packages. See: `llmtxt` skill.

```markdown
## llmtxt Files Created

- docs/llmtxt/[package-name].md
  - Core API reference
  - Common patterns for our use case
  - Gotchas discovered during evaluation
```

### For BUILD Decisions

Document the design approach:
- Architecture overview
- Key components
- Why this design (vs package approaches)

---

## Integration with Workflow

### Phase 0: Discovery

Package research is **Step 0.2** in the Discovery phase:

```
Phase 0: Discovery
├── Step 0.0: Branch Setup (GitOps)
├── Step 0.1: Context Gathering
├── Step 0.2: Package Research    <-- THIS SKILL
│   ├── Define problem
│   ├── Search packages
│   ├── Evaluate candidates
│   ├── Make decision
│   └── Document choice
├── Step 0.3: Gap Analysis
├── Step 0.4: Technical Approach
└── Step 0.5: Manager Approval
```

### Decision Checkpoint

Before proceeding to Technical Approach:

```markdown
## Build vs Compose Checkpoint

[ ] Searched PyPI, GitHub, awesome-lists
[ ] Evaluated at least 3 candidates (if available)
[ ] Documented decision with rationale
[ ] Created llmtxt for chosen packages
[ ] Manager aware of external dependencies

Decision: [COMPOSE / EXTEND / BUILD]
Ready to proceed: [YES / NO - needs discussion]
```

---

## Common Domains and Packages

### Quick Reference for Common Needs

| Domain | First-Choice Package | Alternatives |
|--------|---------------------|--------------|
| HTTP Client | `httpx` | `requests`, `aiohttp` |
| CLI | `click` | `typer`, `argparse` |
| Config | `pydantic-settings` | `dynaconf`, `python-decouple` |
| Dates | `pendulum` | `arrow`, `dateutil` |
| Validation | `pydantic` | `attrs`, `marshmallow` |
| Testing | `pytest` | (standard) |
| Mocking | `pytest-mock` | `unittest.mock` |
| Async | `anyio` | `asyncio` (stdlib) |
| Retries | `tenacity` | `backoff`, `retry` |
| Rate Limiting | `limits` | `ratelimit`, `slowapi` |
| Caching | `cachetools` | `diskcache`, `redis` |
| Logging | `structlog` | `loguru`, stdlib |
| Serialization | `msgspec` | `orjson`, `ujson` |

**Note**: This table is a starting point. Always verify current status before committing.

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| NIH Syndrome | Reimplementing solved problems | Search first, build second |
| Dependency Bloat | Adding packages for trivial needs | stdlib for simple cases |
| Evaluation Paralysis | Endless comparison | Time-box to 1-2 hours |
| Ignoring Maintenance | Using abandoned packages | Check commit history |
| Skipping Docs | Not reading before adopting | Read docs, try examples |
| Version Pinning Avoidance | Using `*` or no pins | Pin with `~=` or `>=,<` |

---

## Output Artifacts

After completing package research:

1. **Decision Document** - Rationale and choice
2. **llmtxt Files** - For each adopted package
3. **Updated Requirements** - Pinned versions
4. **Wrapper Code** - If EXTEND decision (optional)

---

## References

- `llmtxt` skill - Creating package documentation
- `unix-philosophy` skill - Composition principles
- `workflow` skill - Phase 0 integration
