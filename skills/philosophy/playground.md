---
name: playground-exploration
description: Playground-driven development using Knuth's dogfooding philosophy. Use when exploring APIs interactively, discovering features through usage, finding missing functionality, prototyping new features, or converting experiments to tests. Essential for feature discovery and quality improvement through real usage.
---

# Playground-Driven Development

> "...the designer of a new system must not only be the implementor and the first large-scale user; the designer should also write the first user manual. ... If I had not participated fully in all these activities, literally hundreds of improvements would never have been made, because I would never have thought of them or perceived why they were important."
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

## Contents

- [When to Use Playground Exploration](#when-to-use-playground-exploration)
- [Playground Setup](#playground-setup) - Directory structure
- [Exploration Workflow](#exploration-workflow) - Step-by-step process
- [Discovery Patterns](#discovery-patterns) - What to look for
- [Converting to Tests](#converting-to-tests) - From exploration to validation
- [Documentation from Discoveries](#documentation-from-discoveries) - Using learnings
- [Playground Checklist](#playground-checklist) - Verification
- [Anti-Patterns](#anti-patterns) - What not to do

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

## Playground Setup

### Directory Structure

```
project/
├── playground/                 # Exploration code (part of project!)
│   ├── __init__.py
│   ├── {module}_exploration.py # Per-module exploration
│   ├── {module}_experiments.py # Experimental scenarios
│   └── test_{feature}.py       # Playground-to-test conversion
├── src/                        # Production code
└── tests/                      # Formal tests
```

### Module Pattern

Each playground file should:
1. Document what it explores
2. Be runnable directly (`python playground/foo_exploration.py`)
3. Print clear results
4. Return success/failure status

```python
#!/usr/bin/env python3
"""Exploration of {module} functionality.

Demonstrates:
1. Core API usage patterns
2. Edge cases and error handling
3. Integration with related modules

Run directly:
    python playground/{module}_exploration.py

Discoveries feed into:
- tests/test_{module}.py
- Documentation improvements
- API refinements
"""
```

---

## Exploration Process

### Step 1: Setup Playground File

Create `playground/{module}_exploration.py`:

```python
#!/usr/bin/env python3
"""Exploration of {module} functionality."""

import asyncio
from typing import Any

# Import the module under exploration
from mypackage.{module} import (
    MainClass,
    SupportingClass,
    ModuleError,
)


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(success: bool, message: str) -> None:
    """Print a test result."""
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {message}")
```

### Step 2: Explore Happy Path

Test the primary use case:

```python
def explore_basic_usage() -> bool:
    """Explore the primary use case."""
    print_section("1. Basic Usage")

    # Setup
    instance = MainClass(config)

    # The happy path
    result = instance.do_thing(valid_input)
    print_result(result.success, "Basic operation works")

    # Verify expected behavior
    assert result.value == expected_value
    print_result(True, "Result matches expected value")

    return True
```

### Step 3: Explore Edge Cases

Test boundaries and unusual inputs:

```python
def explore_edge_cases() -> bool:
    """Explore edge cases and boundaries."""
    print_section("2. Edge Cases")

    instance = MainClass(config)

    # Empty input
    result = instance.do_thing([])
    print_result(len(result.items) == 0, "Empty input handled")

    # Single item
    result = instance.do_thing(["one"])
    print_result(len(result.items) == 1, "Single item handled")

    # Maximum size
    large_input = ["item"] * 1000
    result = instance.do_thing(large_input)
    print_result(result.success, "Large input handled")

    return True
```

### Step 4: Explore Error Handling

Test failure modes and error messages:

```python
def explore_error_handling() -> bool:
    """Explore error handling and failure modes."""
    print_section("3. Error Handling")

    instance = MainClass(config)

    # Invalid input type
    try:
        instance.do_thing(None)
        print_result(False, "Should reject None input")
        return False
    except ValueError as e:
        print_result(True, f"None rejected: {e}")

    # Invalid state
    try:
        instance.close()
        instance.do_thing(valid_input)  # After close
        print_result(False, "Should reject after close")
        return False
    except ModuleError as e:
        print_result(True, f"Post-close rejected: {e}")

    return True
```

### Step 5: Document Discoveries

Add discovery comments:

```python
def explore_with_discovery() -> bool:
    """Explore and document discoveries."""
    print_section("4. API Discovery")

    # DISCOVERY: The API doesn't support batch operations
    # This would be useful for processing multiple items
    # TODO: Add batch_do_thing() method?
    for item in items:
        instance.do_thing(item)

    # DISCOVERY: Error messages don't include context
    # When do_thing fails, we don't know which item caused it
    # IMPROVEMENT: Include item info in error message

    # DISCOVERY: No way to check if ready before calling
    # Would be helpful to have instance.is_ready() method
    # IMPROVEMENT: Add state checking method

    return True
```

---

## Discovery Categories

When exploring, look for:

### Missing Features
```python
# MISSING: No way to cancel in-progress operations
# Use case: User wants to abort long-running task
# Proposed API: instance.cancel() -> bool
```

### API Friction
```python
# FRICTION: Must call prepare() before every operation
# This is repetitive and error-prone
# Proposed fix: Auto-prepare on first operation
```

### Documentation Gaps
```python
# UNDOCUMENTED: Behavior when config is None
# Actual: Uses default config (sensible)
# Should document: "If config is None, uses default settings"
```

### Error Improvements
```python
# POOR_ERROR: "Invalid input" doesn't say what's invalid
# Better: "Invalid input: expected string, got int for 'name'"
```

### Performance Issues
```python
# PERFORMANCE: This operation is O(n^2) due to nested loops
# Should document performance characteristics
# Consider: Add caching for repeated lookups
```

---

## Converting Discoveries to Actions

### Discovery to Test

```python
# Playground discovery:
# DISCOVERY: Empty input returns empty result (not error)

# Converts to test:
def test_empty_input_returns_empty_result():
    """Empty input should return empty result, not raise error."""
    instance = MainClass(config)
    result = instance.do_thing([])
    assert result.items == []
    assert result.success is True
```

### Discovery to Documentation

```python
# Playground discovery:
# DISCOVERY: Config can be None, uses defaults

# Converts to docstring update:
def __init__(self, config: Config | None = None):
    """Initialize the processor.

    Args:
        config: Configuration options. If None, uses sensible defaults
                suitable for most use cases.
    """
```

### Discovery to Feature Request

```python
# Playground discovery:
# MISSING: No batch operation support

# Converts to issue/task:
"""
Feature Request: Add batch processing support

Use Case:
When processing multiple items, the current API requires:
    for item in items:
        instance.do_thing(item)  # Separate call each time

This is inefficient for large batches. Proposed API:
    results = instance.do_things(items)  # Single call

Benefits:
- Reduced overhead (single call vs N calls)
- Better error handling (partial success possible)
- More intuitive for batch operations
"""
```

---

## Playground File Template

```python
#!/usr/bin/env python3
"""Exploration of {module_name} functionality.

Demonstrates:
1. {Primary capability}
2. {Secondary capability}
3. Edge cases and error handling

Run directly:
    python playground/{filename}.py

Each section can be run independently by calling the specific function.

Discoveries:
- [List discoveries as you find them]
- [Update this list during exploration]
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Import module under exploration
from mypackage.{module} import (
    MainClass,
    RelatedClass,
    ModuleError,
)


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(success: bool, message: str) -> None:
    """Print a test result."""
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {message}")


# =============================================================================
# Section 1: Basic Usage
# =============================================================================


def explore_basic_usage() -> bool:
    """Explore the primary use case."""
    print_section("1. Basic Usage")

    # Your exploration code here

    print_result(True, "Basic usage works")
    return True


# =============================================================================
# Section 2: Edge Cases
# =============================================================================


def explore_edge_cases() -> bool:
    """Explore edge cases and boundaries."""
    print_section("2. Edge Cases")

    # Your edge case exploration here

    return True


# =============================================================================
# Section 3: Error Handling
# =============================================================================


def explore_error_handling() -> bool:
    """Explore error handling and failure modes."""
    print_section("3. Error Handling")

    # Your error handling exploration here

    return True


# =============================================================================
# Section 4: Integration
# =============================================================================


def explore_integration() -> bool:
    """Explore integration with related modules."""
    print_section("4. Integration")

    # Your integration exploration here

    return True


# =============================================================================
# Main Entry Point
# =============================================================================


def run_all_explorations() -> bool:
    """Run all exploration sections."""
    print("\n" + "=" * 60)
    print("  {MODULE_NAME} EXPLORATION")
    print("=" * 60)

    explorations = [
        ("Basic Usage", explore_basic_usage),
        ("Edge Cases", explore_edge_cases),
        ("Error Handling", explore_error_handling),
        ("Integration", explore_integration),
    ]

    results = []
    for name, func in explorations:
        try:
            success = func()
            results.append((name, success))
        except Exception as e:
            print(f"\n[ERROR] {name} failed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("  EXPLORATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, s in results if s)
    total = len(results)

    for name, success in results:
        status = "[OK]  " if success else "[FAIL]"
        print(f"{status} {name}")

    print(f"\nResults: {passed}/{total} sections passed")

    # Document discoveries
    print("\n--- DISCOVERIES ---")
    print("# TODO: List discoveries found during exploration")
    print("# - Missing features")
    print("# - API friction points")
    print("# - Documentation gaps")
    print("# - Error message improvements")

    return passed == total


if __name__ == "__main__":
    success = run_all_explorations()
    sys.exit(0 if success else 1)
```

---

## Iterative Exploration

Playground exploration is **not a one-time step**. It's continuous:

```
Implement -> Playground Explore -> Find Issues -> Update Requirements
     ^                                                    |
     |                                                    |
     +----------------------------------------------------+
```

### When to Re-explore

- After implementing new features
- After fixing bugs (verify the fix)
- After refactoring (verify behavior unchanged)
- When adding new use cases
- When integrating with new modules

### Evolving Playground Code

Playground code should evolve with the module:

1. **Add new sections** for new features
2. **Update existing sections** when API changes
3. **Remove obsolete sections** when features removed
4. **Promote stable patterns** to formal tests

---

## Integration with Workflow

### Phase 0: Discovery
- Create initial `playground/{module}_exploration.py`
- Explore existing related code
- Document initial understanding

### Phase 1: Development (Step 5)
- Run playground after implementation
- Document at least 5 scenarios
- Record discoveries
- Update exploration code

### Phase 2: Refinement
- Re-run playground to verify fixes
- Add scenarios for fixed issues
- Update discovery list

### Phase 3: Completion
- Finalize playground code (it stays!)
- Convert key discoveries to tests
- Document findings in module docstrings

---

## Best Practices

### Do
- Run playground code frequently during development
- Document every discovery, even small ones
- Keep playground code clean and runnable
- Convert stable patterns to formal tests
- Update playground when module changes

### Don't
- Delete playground code after testing
- Skip exploration because "tests are enough"
- Ignore friction points ("it's fine")
- Write exploration code you can't run
- Treat playground as throwaway

---

## Success Criteria

Playground exploration is successful when:

1. **Runnable**: `python playground/{module}.py` works
2. **Documented**: Clear comments explain what each section explores
3. **Discoverable**: Findings are recorded with action items
4. **Convertible**: Key scenarios become formal tests
5. **Maintained**: Updated when module changes

---

## Summary

> "Eat your own dog food."

The playground is how you become the first user of your own code. Every friction point you feel is a bug report. Every missing feature you want is a feature request. Every confusing behavior is a documentation gap.

By using your own code extensively before others do, you find and fix issues that would otherwise escape to users.
