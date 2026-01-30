---
name: playground-exploration
description: Playground-driven development using Knuth's dogfooding philosophy. Use when exploring APIs interactively, discovering features through usage, finding missing functionality, prototyping new features, or converting experiments to tests. Essential for feature discovery and quality improvement through real usage.
---

# Playground-Driven Development

> "...the designer of a new system must not only be the implementor and the first large-scale user; the designer should also write the first user manual."
> -- Donald Knuth, "The Errors of TeX" (1989)

## Core Philosophy: Dogfooding

**Be the designer, implementor, first user, AND documentation writer.**

The playground is not throwaway code -- it's a discovery tool that:
1. Reveals missing features you didn't anticipate
2. Exposes awkward APIs that need improvement
3. Documents real usage patterns for others
4. Converts directly into tests and documentation
5. Creates a feedback loop that improves quality

Every friction point you personally feel should be addressed.

---

## When to Use Playground Exploration

Use this skill:
- After implementing new functionality (Phase 1, Step 5)
- When exploring unfamiliar APIs in existing code
- To prototype features before formal implementation
- To discover edge cases and missing functionality
- When preparing test scenarios
- To validate API ergonomics

---

## Quick Start

1. **Create** `playground/{module}_exploration.py` before implementation
2. **Implement** module functionality
3. **Explore** the API: basic usage, edge cases, error handling
4. **Document** discoveries with action items
5. **Convert** key scenarios to formal tests

---

## Discovery Types

Look for these while exploring:

- **Missing Features** - What would make usage easier?
- **API Friction** - What feels awkward or repetitive?
- **Documentation Gaps** - What behaviors aren't clear?
- **Error Improvements** - Are error messages helpful?
- **Performance Issues** - Is performance acceptable?

See [references/discovery-categories.md](references/discovery-categories.md) for detailed examples.

---

## Setting Up Playground

### Directory Structure

```
project/
├── playground/
│   ├── __init__.py
│   ├── {module}_exploration.py
│   └── {module}_experiments.py
├── src/
└── tests/
```

### Module Pattern

Each playground file:
1. Documents what it explores
2. Is runnable directly
3. Prints clear results
4. Returns success/failure status

See [template.py](template.py) for a starting template and [references/setup.md](references/setup.md) for detailed setup patterns.

---

## Exploration Process

The 5-step process for discovering API qualities:

1. **Setup** - Create exploration file with helper functions
2. **Happy Path** - Test primary use case
3. **Edge Cases** - Explore boundaries and unusual inputs
4. **Error Handling** - Test failure modes and error messages
5. **Document Discoveries** - Record findings and action items

See [references/exploration-process.md](references/exploration-process.md) for detailed steps and code examples.

---

## Converting Discoveries to Actions

Playground findings become:

- **Tests** - Scenarios become `test_*.py`
- **Documentation** - Gaps become docstring updates
- **Features** - Missing functionality becomes requests
- **Improvements** - Friction becomes API refinements

See [references/converting-to-tests.md](references/converting-to-tests.md) for conversion patterns.

---

## Integration with Workflow

**Phase 0**: Create initial playground file, explore related code

**Phase 1 (Step 5)**: Run playground after implementation, document 5+ scenarios, record discoveries

**Phase 2**: Re-run playground to verify fixes, update discovery list

**Phase 3**: Finalize playground, convert key scenarios to tests

See [references/best-practices.md](references/best-practices.md) for full integration details.

---

## Best Practices

### Do
- Run playground frequently during development
- Document every discovery
- Keep playground code clean and runnable
- Convert stable patterns to formal tests
- Update playground when module changes

### Don't
- Delete playground code after testing (it stays!)
- Skip exploration because "tests are enough"
- Ignore friction points
- Write code you can't run
- Treat playground as throwaway

---

## Success Criteria

Playground exploration succeeds when:

1. **Runnable** - `python playground/{module}.py` works without errors
2. **Documented** - Clear comments explain each section
3. **Discoverable** - Findings recorded with action items
4. **Convertible** - Key scenarios become formal tests
5. **Maintained** - Updated when module changes

---

## Quick Reference

```
Exploration phases:
  1. Setup         → Import module, helper functions
  2. Happy Path    → Primary use case
  3. Edge Cases    → Boundaries, empty, maximum
  4. Errors        → Invalid input, failures
  5. Discoveries   → Record findings & actions

Discovery types:
  - MISSING: Features that would be useful
  - FRICTION: Awkward or repetitive patterns
  - UNDOCUMENTED: Behavior that's unclear
  - POOR_ERROR: Messages that don't help
  - PERFORMANCE: Speed or memory issues

Conversion:
  Discovery → Test scenario → Formal test
  Discovery → API gap → Documentation update
  Discovery → Friction → Feature request
```

---

## Related Resources

- **[references/setup.md](references/setup.md)** - Directory structure, module pattern, template
- **[references/exploration-process.md](references/exploration-process.md)** - Step-by-step exploration with code examples
- **[references/discovery-categories.md](references/discovery-categories.md)** - Types of discoveries and how to identify them
- **[references/converting-to-tests.md](references/converting-to-tests.md)** - How to convert discoveries to tests, docs, and features
- **[references/best-practices.md](references/best-practices.md)** - Do's/don'ts, success criteria, workflow integration
