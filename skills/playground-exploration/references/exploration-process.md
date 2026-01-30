# Step-by-Step Exploration Process

The five-phase process for discovering API qualities and design issues.

---

## Overview

Exploration follows a logical progression that uncovers increasingly subtle issues:

```
Setup         → Basic Usage    → Edge Cases    → Errors    → Discoveries
Prepare       → Happy Path     → Boundaries    → Failures  → Record Issues
scaffolding   → Success case   → Unusual input → Handling  → Action Items
```

Each phase builds on the previous, revealing more about the API.

---

## Phase 1: Setup

### Goal
Create the infrastructure for exploration - imports, helpers, and structure.

### Steps

1. **Create file with proper header:**

```python
#!/usr/bin/env python3
"""Exploration of {module} functionality.

Demonstrates:
1. Core API usage patterns
2. Edge cases and error handling
3. Integration with related modules

Run directly:
    python playground/{module}_exploration.py
"""

from __future__ import annotations

import sys
from typing import Any

# Import the module under exploration
from mypackage._core import MainClass, SupportingClass, ModuleError
```

2. **Add helper functions:**

```python
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

3. **Create main execution block:**

```python
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  MODULE_NAME EXPLORATION")
    print("=" * 60)
    # More to come...
```

---

## Phase 2: Happy Path

### Goal
Document the primary use case. The "everything works perfectly" scenario.

### Questions to Answer
- What is the main thing this module is supposed to do?
- What's the simplest successful operation?
- What inputs does it expect?
- What output should I get?

### Implementation

```python
def explore_basic_usage() -> bool:
    """Explore the primary use case."""
    print_section("1. Basic Usage")

    # Setup: Create minimal valid instance
    try:
        config = {"timeout": 30, "retries": 3}
        instance = MainClass(config)
        print_result(True, "Instance created successfully")
    except Exception as e:
        print_result(False, f"Failed to create instance: {e}")
        return False

    # Happy path: Primary operation with typical input
    try:
        valid_input = {
            "name": "test",
            "data": [1, 2, 3, 4, 5],
        }
        result = instance.do_thing(valid_input)
        print_result(result.success, "Primary operation completed")
    except Exception as e:
        print_result(False, f"Primary operation failed: {e}")
        return False

    # Verify expected behavior
    try:
        assert result.count == 5, f"Expected 5 items, got {result.count}"
        print_result(True, f"Output as expected: {result.count} items processed")
    except AssertionError as e:
        print_result(False, str(e))
        return False

    return True
```

### What This Reveals
- Can you create the object?
- Does the API match what the documentation promises?
- Does it produce sensible output?
- Are docstrings accurate?

---

## Phase 3: Edge Cases

### Goal
Test boundaries and unusual (but valid) inputs.

### What to Test

```python
def explore_edge_cases() -> bool:
    """Explore edge cases and boundaries."""
    print_section("2. Edge Cases")

    instance = MainClass()

    # EMPTY INPUT: What happens with minimal data?
    try:
        result = instance.do_thing({})
        print_result(
            result.count == 0,
            f"Empty input: {result.count} items (expected 0)"
        )
    except Exception as e:
        print_result(False, f"Empty input failed: {e}")
        return False

    # SINGLE ITEM: Does it work with one item?
    try:
        result = instance.do_thing({"data": [1]})
        print_result(
            result.count == 1,
            f"Single item: {result.count} items (expected 1)"
        )
    except Exception as e:
        print_result(False, f"Single item failed: {e}")
        return False

    # MAXIMUM SIZE: How much can it handle?
    try:
        large_input = {"data": list(range(10000))}
        result = instance.do_thing(large_input)
        print_result(
            result.success and result.count == 10000,
            f"Large input: {result.count} items processed"
        )
    except Exception as e:
        print_result(False, f"Large input failed: {e}")
        return False

    # UNICODE/SPECIAL CHARS: Does it handle them?
    try:
        special_input = {
            "data": ["café", "日本語", "🎉", "NULL\x00BYTE"]
        }
        result = instance.do_thing(special_input)
        print_result(
            result.count == 4,
            f"Special characters: {result.count} items handled"
        )
    except Exception as e:
        print_result(False, f"Special characters failed: {e}")
        return False

    # REPEATED VALUES: Duplicates?
    try:
        repeated = {"data": [1, 1, 1, 2, 2, 2]}
        result = instance.do_thing(repeated)
        print_result(
            result.count == 6 or result.unique == 2,
            f"Duplicates: {result.count} total, {result.unique} unique"
        )
    except Exception as e:
        print_result(False, f"Duplicates failed: {e}")
        return False

    return True
```

### Common Edge Cases to Test

| Edge Case | Example | What to Check |
|-----------|---------|---------------|
| **Empty** | Empty list, empty string | Does it return empty or fail? |
| **Single item** | List with 1 element | Same code path as multi-item? |
| **Maximum** | Largest valid input | Performance/memory issues? |
| **Zero/None** | 0 value, None input | Special case handling? |
| **Duplicates** | Repeated values | Uniqueness enforced? |
| **Mixed types** | Numbers and strings | Type validation? |
| **Unicode** | 日本語, emoji | Encoding handling? |
| **Whitespace** | Leading/trailing spaces | Trimming behavior? |

---

## Phase 4: Error Handling

### Goal
Test failure modes and error messages. Make sure errors are clear and recoverable.

### Implementation

```python
def explore_error_handling() -> bool:
    """Explore error handling and failure modes."""
    print_section("3. Error Handling")

    instance = MainClass()

    # INVALID TYPE: Wrong input type
    try:
        instance.do_thing(None)
        print_result(False, "Should reject None input")
        return False
    except (ValueError, TypeError) as e:
        print_result(True, f"None rejected with: {type(e).__name__}: {e}")

    # MISSING REQUIRED FIELD: Incomplete input
    try:
        instance.do_thing({"missing_required": True})
        print_result(False, "Should reject incomplete input")
        return False
    except ValueError as e:
        print_result(True, f"Incomplete input rejected: {e}")

    # INVALID STATE: Operation after close
    try:
        instance.close()
        instance.do_thing({"data": [1, 2, 3]})
        print_result(False, "Should reject after close")
        return False
    except ModuleError as e:
        print_result(True, f"Post-close rejected: {e}")

    # INVALID VALUE RANGE: Out of bounds
    try:
        instance.do_thing({"timeout": 99999})  # Too large?
        print_result(False, "Should reject invalid timeout")
        return False
    except ValueError as e:
        print_result(True, f"Invalid range rejected: {e}")

    # RESOURCE EXHAUSTION: Too much data
    try:
        huge_input = {"data": list(range(1_000_000))}
        instance.do_thing(huge_input)
        print_result(False, "Should reject excessive data")
        return False
    except (MemoryError, ValueError) as e:
        print_result(True, f"Excessive data rejected: {e}")

    return True
```

### Questions to Ask

1. **Are errors clear?**
   - "Invalid input" vs "Expected string for 'name' field"
   - Which one helps you fix the problem?

2. **Are they recoverable?**
   - Can you catch specific error types?
   - Can you continue after an error?

3. **Do they have context?**
   - Which item caused the failure?
   - What was the actual vs expected value?

### Common Error Scenarios

```python
# Bad: Generic error messages
# "Error" - What error? Where? Why?

# Good: Specific, helpful messages
# "Invalid timeout: expected int ≤ 300, got 9999"
# "Field 'name' is required but was None"
# "Item at index 42 has invalid type: str (expected int)"
```

---

## Phase 5: Document Discoveries

### Goal
Record what you learned. Observations become action items.

### Implementation

```python
def explore_with_discoveries() -> bool:
    """Explore and document findings."""
    print_section("4. Discoveries")

    instance = MainClass()

    # DISCOVERY: API limitation
    print("\n[DISCOVERY] No batch operation support")
    print("  Currently must call do_thing() N times for N items")
    print("  Would be more efficient with do_things(items)")
    print("  ACTION: Consider adding batch API for performance")

    # FRICTION: Awkward usage pattern
    print("\n[FRICTION] Config required on every creation")
    print("  Must pass config: MainClass(config)")
    print("  Would prefer defaults: MainClass() with optional override")
    print("  ACTION: Make config optional with sensible defaults")

    # UNDOCUMENTED: Behavior not in docstring
    print("\n[UNDOCUMENTED] Behavior when retries exhausted")
    print("  Raises TimeoutError but max_retries not mentioned")
    print("  ACTION: Add retry behavior to docstring")

    # IMPROVEMENT: Error messages could be clearer
    print("\n[ERROR_MESSAGE] Index out of range error lacks context")
    print("  'Index out of range' doesn't say which index")
    print("  Better: 'Index 42 out of range [0, 41]'")
    print("  ACTION: Improve error message format")

    return True
```

### Discovery Categories

| Category | Example | Action |
|----------|---------|--------|
| **MISSING** | No batch API | Request feature |
| **FRICTION** | Repetitive setup | Simplify API |
| **UNDOCUMENTED** | Behavior unclear | Update docs |
| **ERROR_MESSAGE** | Generic error | Improve message |
| **PERFORMANCE** | Slow operation | Optimize or document |

---

## Complete 5-Phase Example

```python
#!/usr/bin/env python3
"""Complete exploration example."""

from mypackage import DataProcessor


def print_section(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(success: bool, message: str) -> None:
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {message}")


def explore_basic_usage() -> bool:
    """Phase 2: Happy path."""
    print_section("1. Basic Usage (Happy Path)")

    processor = DataProcessor()
    result = processor.process([1, 2, 3, 4, 5])

    print_result(result is not None, "Returns a result")
    print_result(len(result) == 5, f"Processed {len(result)} items")
    print_result(result[0] == 2, f"First item doubled: {result[0]}")

    return True


def explore_edge_cases() -> bool:
    """Phase 3: Boundaries."""
    print_section("2. Edge Cases (Boundaries)")

    processor = DataProcessor()

    # Empty
    print_result(len(processor.process([])) == 0, "Empty input works")

    # Single
    print_result(len(processor.process([42])) == 1, "Single item works")

    # Large
    large = list(range(10000))
    print_result(len(processor.process(large)) == 10000, "10K items works")

    return True


def explore_errors() -> bool:
    """Phase 4: Failures."""
    print_section("3. Error Handling (Failures)")

    processor = DataProcessor()

    # None input
    try:
        processor.process(None)
        print_result(False, "Should reject None")
        return False
    except TypeError:
        print_result(True, "None rejected correctly")

    # String (not list)
    try:
        processor.process("not a list")
        print_result(False, "Should reject string")
        return False
    except TypeError:
        print_result(True, "String rejected correctly")

    return True


def explore_discoveries() -> bool:
    """Phase 5: Observations."""
    print_section("4. Discoveries")

    print("  [MISSING] No in-place processing option")
    print("  [FRICTION] Always copies result (could use parameter)")
    print("  [UNDOCUMENTED] Behavior with NaN/Inf values")
    print("  [IMPROVEMENT] Error: 'invalid input' (too vague)")

    return True


if __name__ == "__main__":
    results = []
    for explore_func in [
        explore_basic_usage,
        explore_edge_cases,
        explore_errors,
        explore_discoveries,
    ]:
        try:
            success = explore_func()
            results.append((explore_func.__name__, success))
        except Exception as e:
            print(f"ERROR: {explore_func.__name__} failed: {e}")
            results.append((explore_func.__name__, False))

    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)

    for name, success in results:
        status = "[OK]" if success else "[FAIL]"
        print(f"{status} {name}")

    import sys
    sys.exit(0 if all(s for _, s in results) else 1)
```

---

## Tips for Each Phase

**Phase 1: Setup**
- Organize imports clearly
- Create reusable helper functions
- Plan for 5-6 exploration sections

**Phase 2: Happy Path**
- Focus on what should work
- Use typical, realistic inputs
- Verify expected outputs

**Phase 3: Edge Cases**
- Test boundaries: empty, single, maximum
- Test unusual but valid inputs
- Discover assumptions you made

**Phase 4: Error Handling**
- Try to break it intentionally
- Check error messages for clarity
- Verify recovery is possible

**Phase 5: Discoveries**
- Write down everything you notice
- Be honest about friction
- Convert findings to test cases

---

## Summary

The five phases progress from happy path → boundaries → failures → observations:

1. **Setup** - Infrastructure and helpers
2. **Basic Usage** - Happy path with typical input
3. **Edge Cases** - Boundaries, unusual inputs
4. **Errors** - Invalid input, failure modes
5. **Discoveries** - Observations, action items

Each phase is complete in itself but builds on previous phases.
