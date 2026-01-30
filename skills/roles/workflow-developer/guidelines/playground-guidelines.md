# Playground Guidelines: Dogfooding

The playground is how you become the first user of your own code.

See also: [playground-exploration skill](../../workflow/python-philosophy/playground.md) for comprehensive guide.

---

## 1. Create Playground Early (Phase 0)

Create exploration file before implementing:

```bash
mkdir -p playground
touch playground/{module}_exploration.py
```

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
    # TODO: Implement as module develops
    return True

if __name__ == "__main__":
    explore_basic_usage()
```

---

## 2. Update Playground During Phase 1, Step 5

After implementing code, use your code:

```python
def explore_basic_usage() -> bool:
    """Explore the primary use case."""
    from mypackage import MainClass

    instance = MainClass(config)
    result = instance.do_thing(test_input)

    # DISCOVERY: No way to check status before operation
    # FRICTION: Config requires manual setup
    # MISSING: Batch operation support

    return result.success

def explore_edge_cases() -> bool:
    """Test boundary conditions."""
    # Empty input
    # Max input
    # Invalid input
    # Concurrent operations
    return True

if __name__ == "__main__":
    print("Testing basic usage...")
    explore_basic_usage()

    print("Testing edge cases...")
    explore_edge_cases()
```

---

## 3. Document Discoveries

Every discovery should be actionable:

```python
# DISCOVERY: Empty input returns error instead of empty result
# Action: Change behavior OR document in docstring

# FRICTION: Must call prepare() before every operation
# Action: Auto-prepare on first use OR simplify API

# MISSING: No way to cancel in-progress operations
# Action: Add cancel() method OR document limitation

# EDGE CASE: Float comparison fails due to precision
# Action: Use tolerance-based comparison OR document
```

---

## 4. Target Scenarios

Test at least 5 distinct scenarios:

1. **Happy Path** - Normal, expected usage
   ```python
   result = process_data(valid_input)
   assert result.success
   ```

2. **Edge Cases** - Boundaries, empty, max values
   ```python
   assert process_data([]) == []
   assert process_data([1]) == [1]
   assert process_data(MAX_SIZE) doesn't crash
   ```

3. **Error Paths** - Invalid input, failures
   ```python
   with pytest.raises(ValueError):
       process_data(None)
   ```

4. **Integration** - Works with existing code
   ```python
   existing_instance.new_method()
   assert everything_still_works()
   ```

5. **Performance** - Acceptable speed/memory (if relevant)
   ```python
   start = time.time()
   process_large_dataset()
   assert time.time() - start < 1.0
   ```

---

## 5. Convert Discoveries to Tests

Discoveries become formal tests:

```python
# Playground discovery:
# "Empty input returns error instead of empty result"

# Becomes formal test:
def test_empty_input_returns_empty_result():
    instance = MainClass(config)
    result = instance.do_thing([])
    assert result.items == []
    assert result.success
```

Key test questions:
- What should happen?
- What currently happens?
- Is that correct?
- How do we ensure it stays correct?

---

## 6. Playground Checklist (Phase 1, Step 5)

- [ ] Playground file created in Phase 0
- [ ] Updated with real scenarios in Phase 1
- [ ] Runs without errors: `python playground/{module}_exploration.py`
- [ ] At least 5 scenarios tested
- [ ] Discoveries documented with action items
- [ ] API friction points noted
- [ ] Missing features identified
- [ ] Key discoveries converted to tests in Step 6

---

## 7. Your First User Experience

Remember: **You are the first user.**

When you find friction:
- **Too many setup steps?** Simplify the API
- **Hard to discover features?** Improve naming or docs
- **Surprising error messages?** Make them clearer
- **Performance too slow?** Optimize or document why
- **Missing features?** Consider adding them

Your first-user experience is valuable feedback. Act on it.

---

## Example: Full Playground

```python
#!/usr/bin/env python3
"""Exploration of data_pipeline functionality."""
import time
from mypackage import DataPipeline, ValidationError

def explore_basic_usage() -> bool:
    """Test core functionality."""
    print("\n=== Basic Usage ===")

    pipeline = DataPipeline()
    result = pipeline.process([1, 2, 3, 4, 5])

    print(f"Input: [1, 2, 3, 4, 5]")
    print(f"Output: {result}")

    # FRICTION: Requires manual initialization
    # MISSING: Chainable operations
    return result is not None

def explore_edge_cases() -> bool:
    """Test boundaries."""
    print("\n=== Edge Cases ===")

    pipeline = DataPipeline()

    # Empty
    assert pipeline.process([]) == []
    print("✓ Empty input works")

    # Single item
    assert len(pipeline.process([1])) == 1
    print("✓ Single item works")

    # Large input
    large = list(range(10000))
    result = pipeline.process(large)
    assert len(result) == 10000
    print("✓ Large input works")

    return True

def explore_error_paths() -> bool:
    """Test error handling."""
    print("\n=== Error Paths ===")

    pipeline = DataPipeline()

    try:
        pipeline.process(None)
        print("✗ None input should fail")
        return False
    except ValidationError:
        print("✓ None input raises ValidationError")

    try:
        pipeline.process("not a list")
        print("✗ String input should fail")
        return False
    except ValidationError:
        print("✓ String input raises ValidationError")

    return True

def explore_performance() -> bool:
    """Test performance."""
    print("\n=== Performance ===")

    pipeline = DataPipeline()
    data = list(range(10000))

    start = time.time()
    result = pipeline.process(data)
    elapsed = time.time() - start

    print(f"Processed {len(data)} items in {elapsed:.3f}s")
    assert elapsed < 1.0, "Too slow!"

    return True

if __name__ == "__main__":
    print("Exploring DataPipeline...")

    explore_basic_usage()
    explore_edge_cases()
    explore_error_paths()
    explore_performance()

    print("\n✓ All explorations complete")
```

---

## Key Principle

> "...the designer of a new system must not only be the implementor and the first large-scale user; the designer should also write the first user manual."

Your playground IS your first-user manual in action. Use it to discover what works and what doesn't.
