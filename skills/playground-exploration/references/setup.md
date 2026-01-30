# Playground Setup and Patterns

Directory structure, module organization, and templates for playground exploration.

---

## Directory Structure

Playground files live alongside your project, not hidden:

```
project/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── _core.py
│       └── ...
├── tests/
│   ├── test_core.py
│   └── conftest.py
├── playground/                 # Exploration code (part of project!)
│   ├── __init__.py
│   ├── core_exploration.py     # Exploration of mypackage._core
│   ├── api_exploration.py      # Exploration of public API
│   └── integration_exploration.py
└── README.md
```

**Why playground is part of the project:**
- It's not throwaway code
- It documents real usage patterns
- It stays in version control
- It gets updated as module evolves
- It's run by CI/CD as part of quality check

---

## Module Naming Pattern

**Convention:**
```
playground/{module_or_feature}_exploration.py
```

**Examples:**
```
playground/core_exploration.py          # Explores _core module
playground/validators_exploration.py    # Explores validation functions
playground/api_integration.py           # Explores public API
playground/performance_exploration.py   # Performance testing
```

---

## Module Structure

Each playground file should have:

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

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Import the module under exploration
from mypackage._core import MainClass, SupportingClass, ModuleError


def print_section(title: str) -> None:
    """Print a section header for readability."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(success: bool, message: str) -> None:
    """Print a test result with [OK] or [FAIL] status."""
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {message}")


# Section functions (one per exploration area)

def explore_section() -> bool:
    """Explore a specific capability."""
    print_section("Section Name")
    # Implementation
    return True


if __name__ == "__main__":
    success = explore_section()
    sys.exit(0 if success else 1)
```

---

## Helper Functions

### Print Utilities

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


def print_discovery(discovery_type: str, description: str) -> None:
    """Record a discovery."""
    print(f"  [{discovery_type}] {description}")
```

### Testing Utilities

```python
def assert_equal(actual: Any, expected: Any, message: str = "") -> bool:
    """Check equality and print result."""
    if actual == expected:
        print_result(True, message or f"Assert {actual} == {expected}")
        return True
    else:
        print_result(False, message or f"Assert failed: {actual} != {expected}")
        return False


def assert_raises(func: callable, exception_type: type, message: str = "") -> bool:
    """Check that function raises expected exception."""
    try:
        func()
        print_result(False, message or f"Should raise {exception_type.__name__}")
        return False
    except exception_type:
        print_result(True, message or f"Correctly raised {exception_type.__name__}")
        return True
    except Exception as e:
        print_result(False, message or f"Wrong exception: {type(e).__name__}")
        return False
```

---

## Complete Template

```python
#!/usr/bin/env python3
"""Exploration of {module_name} functionality.

Demonstrates:
1. {Primary capability}
2. {Secondary capability}
3. Edge cases and error handling

Run directly:
    python playground/{filename}.py

Discoveries recorded below are converted to:
- Formal tests in tests/
- Documentation updates
- Feature requests if needed
"""

from __future__ import annotations

import sys
import time
from typing import Any

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


def print_discovery(discovery_type: str, description: str) -> None:
    """Record a discovery."""
    print(f"  [{discovery_type}] {description}")


# =============================================================================
# Section 1: Basic Usage
# =============================================================================


def explore_basic_usage() -> bool:
    """Explore the primary use case."""
    print_section("1. Basic Usage")

    try:
        # Create instance
        instance = MainClass(config={"timeout": 30})
        print_result(True, "Instance created successfully")

        # Test primary operation
        result = instance.do_thing({"data": "test"})
        print_result(result.success, "Primary operation works")

        # Verify expected behavior
        print_result(
            result.value == "expected",
            f"Result matches expectation: {result.value}",
        )

        return True
    except Exception as e:
        print_result(False, f"Basic usage failed: {e}")
        return False


# =============================================================================
# Section 2: Edge Cases
# =============================================================================


def explore_edge_cases() -> bool:
    """Explore edge cases and boundaries."""
    print_section("2. Edge Cases")

    instance = MainClass()

    # Empty input
    result = instance.do_thing({})
    print_result(len(result.items) == 0, "Empty input handled")

    # Single item
    result = instance.do_thing({"key": "value"})
    print_result(len(result.items) == 1, "Single item handled")

    # Large input
    large_input = {f"key_{i}": f"value_{i}" for i in range(1000)}
    result = instance.do_thing(large_input)
    print_result(result.success, f"Large input handled ({len(result.items)} items)")

    return True


# =============================================================================
# Section 3: Error Handling
# =============================================================================


def explore_error_handling() -> bool:
    """Explore error handling and failure modes."""
    print_section("3. Error Handling")

    instance = MainClass()

    # Invalid input type
    try:
        instance.do_thing(None)
        print_result(False, "Should reject None input")
        return False
    except (ValueError, TypeError) as e:
        print_result(True, f"None rejected: {e}")

    # Invalid state (if applicable)
    try:
        instance.close()
        instance.do_thing({"data": "test"})  # After close
        print_result(False, "Should reject after close")
        return False
    except ModuleError as e:
        print_result(True, f"Post-close rejected: {e}")

    return True


# =============================================================================
# Section 4: Integration
# =============================================================================


def explore_integration() -> bool:
    """Explore integration with related modules."""
    print_section("4. Integration")

    instance = MainClass()

    # Test with supporting class
    helper = SupportingClass()
    result = instance.process(helper.prepare_data({"test": "data"}))
    print_result(result.success, "Integration with SupportingClass works")

    return True


# =============================================================================
# Section 5: Performance (Optional)
# =============================================================================


def explore_performance() -> bool:
    """Explore performance characteristics."""
    print_section("5. Performance")

    instance = MainClass()
    data = {f"key_{i}": f"value_{i}" for i in range(1000)}

    start = time.time()
    result = instance.do_thing(data)
    elapsed = time.time() - start

    print_result(
        elapsed < 1.0,
        f"Processed 1000 items in {elapsed:.3f}s",
    )

    return True


# =============================================================================
# Main Execution
# =============================================================================


def run_all() -> bool:
    """Run all explorations and collect results."""
    print("\n" + "=" * 60)
    print("  {MODULE_NAME} EXPLORATION")
    print("=" * 60)

    explorations = [
        ("Basic Usage", explore_basic_usage),
        ("Edge Cases", explore_edge_cases),
        ("Error Handling", explore_error_handling),
        ("Integration", explore_integration),
        ("Performance", explore_performance),
    ]

    results = []
    for name, func in explorations:
        try:
            success = func()
            results.append((name, success))
        except Exception as e:
            print(f"\n[ERROR] {name} failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("  EXPLORATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, s in results if s)
    total = len(results)

    for name, success in results:
        status = "[OK] " if success else "[FAIL]"
        print(f"{status} {name}")

    print(f"\nResults: {passed}/{total} sections passed")

    # Discoveries section
    print("\n" + "=" * 60)
    print("  DISCOVERIES & ACTION ITEMS")
    print("=" * 60)
    print("\nEdit this section with findings:")
    print("# DISCOVERY: What did you find?")
    print("# ACTION: What should we do about it?")

    return passed == total


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
```

---

## Quick Checklist for New Playground File

- [ ] Create file in `playground/{module}_exploration.py`
- [ ] Add file docstring explaining what it explores
- [ ] Import module under exploration
- [ ] Add `print_section()` and `print_result()` helpers
- [ ] Implement 3-5 exploration functions (basic, edge, errors, integration, etc.)
- [ ] Add main execution block that runs all functions
- [ ] Make file directly runnable: `python playground/foo.py`
- [ ] Print clear results: `[OK]` and `[FAIL]`
- [ ] Return exit code 0 on success, 1 on failure

---

## Running Playground Files

From project root:

```bash
# Run single exploration
python playground/core_exploration.py

# Run all playground files
for f in playground/*_exploration.py; do python "$f" || exit 1; done

# Capture output for review
python playground/core_exploration.py > /tmp/exploration.log 2>&1

# With verbose error output
python -u playground/core_exploration.py 2>&1 | tee exploration-output.txt
```

---

## Adding to CI/CD

In GitHub Actions or equivalent:

```yaml
- name: Run playground explorations
  run: |
    for file in playground/*_exploration.py; do
      echo "Running $file..."
      python "$file" || exit 1
    done
```

This ensures playground code stays runnable and passes every commit.

---

## Evolution Over Time

### Phase 0: Initial Setup
- Create minimal exploration file
- Placeholder functions for future expansion

### Phase 1: Active Exploration
- Add real implementations
- Document discoveries
- Record friction points

### Phase 2: Refinement
- Update explorations based on feedback
- Add new scenarios for fixed issues
- Remove obsolete sections

### Phase 3: Maintenance
- Keep exploration code clean and current
- Update when module API changes
- Use as reference for new developers

---

## Summary

Good playground files:
- ✅ Import the module under exploration
- ✅ Test 5+ scenarios (happy path, edge cases, errors, integration, performance)
- ✅ Print clear, understandable results
- ✅ Are directly runnable with no setup
- ✅ Document discoveries inline
- ✅ Return proper exit codes
- ✅ Use helper functions for consistency
- ✅ Stay updated with module changes
- ✅ Become the first documentation of real usage
