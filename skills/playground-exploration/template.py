#!/usr/bin/env python3
"""Exploration of {MODULE_NAME} functionality.

This playground demonstrates and tests the {MODULE_NAME} module's capabilities
through interactive exploration. It serves multiple purposes:

1. **Discovery**: Find missing features and API friction through real usage
2. **Documentation**: Show how the API is meant to be used
3. **Testing**: Validate behavior before formal test creation
4. **Dogfooding**: Be the first user of your own code

Demonstrates:
1. Core API usage patterns
2. Edge cases and error handling
3. Integration with related modules

Run directly:
    python playground/{module_name}_exploration.py

Each section can be run independently by calling the specific function.

Discoveries (update as you explore):
- [ ] TODO: Document discoveries as you find them
- [ ] TODO: Note API friction points
- [ ] TODO: Identify missing features
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# =============================================================================
# SETUP: Import the module under exploration
# =============================================================================

# Adjust path if needed for direct execution
# project_root = Path(__file__).parent.parent
# sys.path.insert(0, str(project_root))

# Import the module under exploration
# from mypackage.{module_name} import (
#     MainClass,
#     Config,
#     ModuleError,
# )


# =============================================================================
# UTILITIES: Helper functions for exploration output
# =============================================================================


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subsection(title: str) -> None:
    """Print a subsection header."""
    print(f"\n--- {title} ---")


def print_result(success: bool, message: str) -> None:
    """Print a test result with status indicator."""
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {message}")


def print_discovery(category: str, description: str) -> None:
    """Print a discovery for later action.

    Categories:
    - DISCOVERY: General finding about behavior
    - FRICTION: API awkwardness that should be improved
    - MISSING: Feature that should exist but doesn't
    - UNDOCUMENTED: Behavior that needs documentation
    - PERFORMANCE: Performance concern to investigate
    """
    print(f"\n  >> {category}: {description}")


# =============================================================================
# Section 1: Basic Usage
# =============================================================================


def explore_basic_usage() -> bool:
    """Explore the primary use case.

    This section tests the most common, expected usage pattern.
    The "happy path" that most users will follow.
    """
    print_section("1. Basic Usage")

    # Example structure - replace with actual exploration:
    #
    # config = Config(setting="value")
    # instance = MainClass(config)
    #
    # # Test basic operation
    # result = instance.do_thing(valid_input)
    # print_result(result.success, "Basic operation completed")
    #
    # # Verify result
    # assert result.value == expected_value, "Result should match expected"
    # print_result(True, "Result matches expected value")

    print("TODO: Implement basic usage exploration")
    print_result(True, "Basic usage placeholder")

    return True


# =============================================================================
# Section 2: Edge Cases
# =============================================================================


def explore_edge_cases() -> bool:
    """Explore edge cases and boundary conditions.

    Test unusual but valid inputs:
    - Empty inputs
    - Single items
    - Maximum sizes
    - Boundary values
    """
    print_section("2. Edge Cases")

    print_subsection("2.1 Empty Input")
    # instance = MainClass(config)
    # result = instance.do_thing([])
    # print_result(len(result.items) == 0, "Empty input handled correctly")
    print("TODO: Test empty input behavior")

    print_subsection("2.2 Single Item")
    # result = instance.do_thing(["one"])
    # print_result(len(result.items) == 1, "Single item handled correctly")
    print("TODO: Test single item behavior")

    print_subsection("2.3 Large Input")
    # large_input = ["item"] * 10000
    # result = instance.do_thing(large_input)
    # print_result(result.success, "Large input processed successfully")
    print("TODO: Test large input behavior")

    print_subsection("2.4 Boundary Values")
    # Test at limits (0, 1, max-1, max, max+1)
    print("TODO: Test boundary values")

    print_result(True, "Edge cases placeholder")
    return True


# =============================================================================
# Section 3: Error Handling
# =============================================================================


def explore_error_handling() -> bool:
    """Explore error handling and failure modes.

    Test how the module responds to invalid inputs and error conditions:
    - Invalid input types
    - Invalid values
    - Invalid state
    - Resource exhaustion
    """
    print_section("3. Error Handling")

    print_subsection("3.1 Invalid Input Type")
    # try:
    #     instance.do_thing(None)
    #     print_result(False, "Should have rejected None input")
    #     return False
    # except TypeError as e:
    #     print_result(True, f"None rejected: {e}")
    print("TODO: Test invalid input type handling")

    print_subsection("3.2 Invalid Value")
    # try:
    #     instance.do_thing(invalid_value)
    #     print_result(False, "Should have rejected invalid value")
    #     return False
    # except ValueError as e:
    #     print_result(True, f"Invalid value rejected: {e}")
    print("TODO: Test invalid value handling")

    print_subsection("3.3 Invalid State")
    # try:
    #     instance.close()
    #     instance.do_thing(valid_input)  # After close
    #     print_result(False, "Should have rejected operation after close")
    #     return False
    # except ModuleError as e:
    #     print_result(True, f"Post-close operation rejected: {e}")
    print("TODO: Test invalid state handling")

    print_subsection("3.4 Error Message Quality")
    # Verify error messages include helpful context
    # try:
    #     instance.do_thing(bad_input)
    # except ModuleError as e:
    #     has_context = "expected" in str(e).lower() or "got" in str(e).lower()
    #     print_result(has_context, f"Error message includes context: {e}")
    #     if not has_context:
    #         print_discovery("FRICTION", "Error message lacks context - should explain what's wrong")
    print("TODO: Verify error message quality")

    print_result(True, "Error handling placeholder")
    return True


# =============================================================================
# Section 4: Configuration
# =============================================================================


def explore_configuration() -> bool:
    """Explore configuration options and defaults.

    Test:
    - Default configuration works
    - Custom configuration works
    - Invalid configuration rejected
    - Configuration immutability (if applicable)
    """
    print_section("4. Configuration")

    print_subsection("4.1 Default Configuration")
    # instance = MainClass()  # No config = defaults
    # print_result(instance is not None, "Default config works")
    print("TODO: Test default configuration")

    print_subsection("4.2 Custom Configuration")
    # config = Config(custom_setting=True)
    # instance = MainClass(config)
    # print_result(instance.config.custom_setting, "Custom config applied")
    print("TODO: Test custom configuration")

    print_subsection("4.3 Invalid Configuration")
    # try:
    #     Config(invalid_setting="bad")
    # except ValueError as e:
    #     print_result(True, f"Invalid config rejected: {e}")
    print("TODO: Test invalid configuration rejection")

    print_result(True, "Configuration placeholder")
    return True


# =============================================================================
# Section 5: Integration
# =============================================================================


def explore_integration() -> bool:
    """Explore integration with related modules.

    Test how this module works with:
    - Other modules in the package
    - External dependencies
    - Common usage patterns
    """
    print_section("5. Integration")

    print_subsection("5.1 Module Interoperability")
    # from mypackage.other_module import OtherClass
    # other = OtherClass()
    # result = instance.do_thing_with(other)
    # print_result(result.success, "Integration with OtherClass works")
    print("TODO: Test integration with related modules")

    print_subsection("5.2 Composition Pattern")
    # Show how modules compose together
    # pipeline = Pipeline([
    #     MainClass(config1),
    #     OtherClass(config2),
    # ])
    # result = pipeline.run(input_data)
    print("TODO: Demonstrate composition patterns")

    print_result(True, "Integration placeholder")
    return True


# =============================================================================
# Section 6: Discovery Documentation
# =============================================================================


def document_discoveries() -> None:
    """Document all discoveries found during exploration.

    Update this section as you explore. Each discovery should have:
    - Category (DISCOVERY, FRICTION, MISSING, UNDOCUMENTED, PERFORMANCE)
    - Description of what you found
    - Proposed action (fix, document, discuss)
    """
    print_section("6. Discoveries Summary")

    # Example discoveries - replace with actual findings:
    discoveries = [
        # ("DISCOVERY", "Empty input returns empty result (not error)", "Document in docstring"),
        # ("FRICTION", "Must call prepare() before every operation", "Auto-prepare on first use"),
        # ("MISSING", "No batch operation support", "Add batch_do_thing() method"),
        # ("UNDOCUMENTED", "Config defaults vary by environment", "Document environment handling"),
        # ("PERFORMANCE", "Large input causes O(n^2) behavior", "Investigate and optimize"),
    ]

    if not discoveries:
        print("\nNo discoveries documented yet.")
        print("Add discoveries as you explore the module.")
        print("\nExample format:")
        print('  ("FRICTION", "Description of issue", "Proposed fix")')
        return

    print("\nDiscoveries to address:")
    for category, description, action in discoveries:
        print(f"\n  [{category}]")
        print(f"    Issue: {description}")
        print(f"    Action: {action}")

    print(f"\nTotal: {len(discoveries)} discoveries")


# =============================================================================
# Main Entry Point
# =============================================================================


def run_all_explorations() -> bool:
    """Run all exploration sections and summarize results."""
    print("\n" + "=" * 70)
    print("  {MODULE_NAME} EXPLORATION")
    print("  Interactive demonstration and discovery")
    print("=" * 70)
    print(f"  Started: {datetime.now().isoformat()}")

    explorations = [
        ("Basic Usage", explore_basic_usage),
        ("Edge Cases", explore_edge_cases),
        ("Error Handling", explore_error_handling),
        ("Configuration", explore_configuration),
        ("Integration", explore_integration),
    ]

    results: list[tuple[str, bool]] = []

    for name, func in explorations:
        try:
            success = func()
            results.append((name, success))
        except Exception as e:
            print(f"\n[ERROR] {name} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("  EXPLORATION SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "[OK]  " if success else "[FAIL]"
        print(f"  {status} {name}")

    print(f"\n  Results: {passed}/{total} sections passed")

    # Document discoveries
    document_discoveries()

    print("\n" + "=" * 70)
    if passed == total:
        print("  ALL EXPLORATIONS PASSED")
    else:
        print(f"  {total - passed} EXPLORATION(S) FAILED")
    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    success = run_all_explorations()
    sys.exit(0 if success else 1)
