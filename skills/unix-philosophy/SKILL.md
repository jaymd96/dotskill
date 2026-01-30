---
name: unix-philosophy
description: Unix philosophy principles applied to Python development. Use when designing modules, structuring code, making build-vs-compose decisions, or reviewing architecture. Guides composition, single responsibility, and tool reuse patterns.
---

# Unix Philosophy for Python Development

Core Unix principles adapted for modern Python development: composition over reimplementation, small focused modules, and leveraging existing tools.

## The Core Principles

From Doug McIlroy and Unix pioneers:

1. **Do one thing well** - Write programs that do one thing and do it well
2. **Compose via pipes** - Write programs to work together
3. **Text streams** - Expect output to become input to another program
4. **Reuse existing tools** - Use tools rather than unskilled help

> "The power of Unix comes not from individual programs, but from how they combine."

---

## When to Use This Skill

- Designing new modules or packages
- Making build-vs-compose (build vs reuse) decisions
- Reviewing code architecture
- Refactoring monolithic code
- Evaluating third-party package usage

---

## Quick Reference

```
Single Responsibility  → One module, one purpose
Composable Interfaces  → Functions accept and return standard types
Leverage stdlib        → os, pathlib, subprocess, shutil first
Use Existing Packages  → Don't reinvent solved problems
Text as Interface      → JSON, CSV, or line-based for interop
Stay Small             → < 400 lines per module, < 7 parameters
```

---

## The Six Principles

### 1. Do One Thing Well

Each module has a single, clear purpose. Functions do one job. This makes code testable, reusable, and maintainable.

See [references/design-patterns.md](references/design-patterns.md) for module and function design.

### 2. Compose Via Clear Interfaces

Write functions that accept standard types and return standard types. This enables composition: output of one becomes input to another.

See [references/design-patterns.md](references/design-patterns.md) for composable function design.

### 3. Leverage Standard Library

Before writing or importing, check stdlib. `pathlib`, `subprocess`, `dataclasses`, `asyncio` solve many problems already.

See [references/tools-and-packages.md](references/tools-and-packages.md) for stdlib patterns.

### 4. Reuse Existing Tools

Package research first. Well-maintained packages save time, handle edge cases, and have community support. Only build when no suitable package exists.

See [references/tools-and-packages.md](references/tools-and-packages.md) for build vs compose decisions.

### 5. Text Streams as Interface

Design for pipes and text interoperability. JSON Lines for streaming, stdin/stdout for CLIs, structured formats for composability.

See [references/interfaces-and-structure.md](references/interfaces-and-structure.md) for text interface patterns.

### 6. Small, Focused Programs

Keep modules under 400 lines. Functions under 50 lines. This maintains clarity and composability.

See [references/interfaces-and-structure.md](references/interfaces-and-structure.md) for module organization guidelines.

---

## Key Patterns

**Single Responsibility:** One module, one purpose. Don't mix validation, formatting, and I/O.

**Composable Design:** Functions accept `Iterable`, return `list`. Makes them chainable.

**Generator Pipelines:** Memory-efficient composition for large data streams.

**Context Managers:** Encapsulate resource management, enable composition.

**Decorators:** Separate cross-cutting concerns (retry, logging, caching) from business logic.

**Protocols:** Accept interfaces, not concrete types. Enables flexibility and testing.

---

## Applied to Your Workflow

**Phase 0: Discovery** - Evaluate build-vs-compose decisions, research packages

**Phase 1: Implementation** - Design with single responsibility, use stdlib first, keep modules small

**Code Review** - Check module size, parameter count, composability, package consideration

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| God module | 1000+ lines, does everything | Split by responsibility |
| NIH syndrome | Rewriting solved problems | Research packages first |
| Deep inheritance | Tight coupling | Composition + protocols |
| Global state | Non-composable, hard to test | Explicit dependencies |
| Mixed I/O and logic | Can't compose, hard to test | Separate pure and impure |
| Custom formats | Not interoperable | JSON, CSV, or line-based |

---

## Related Resources

- **[references/design-patterns.md](references/design-patterns.md)** - Single responsibility, composable functions, generator pipelines
- **[references/tools-and-packages.md](references/tools-and-packages.md)** - stdlib patterns, package research, build vs compose
- **[references/interfaces-and-structure.md](references/interfaces-and-structure.md)** - Text interfaces, module organization, size guidelines
- **[references/python-patterns.md](references/python-patterns.md)** - Context managers, decorators, protocols, anti-patterns, workflow integration
