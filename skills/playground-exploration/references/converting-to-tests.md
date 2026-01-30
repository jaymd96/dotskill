# Converting Discoveries to Tests, Docs, and Features

How to turn playground findings into actionable improvements.

---

## Overview

Discoveries are just observations until you act on them:

```
Playground Discovery
        ↓
   (Categorize)
        ↓
    (Analyze)
        ↓
   (Convert)
        ↓
    (Action)
    ├─ Missing → Feature Request
    ├─ Friction → API Redesign
    ├─ Undocumented → Documentation Update
    ├─ Poor Error → Error Message Improvement
    └─ Performance → Optimization or Warning
```

---

## Discovery to Test

### Pattern: Behavior Test

Discoveries reveal what actually happens vs. what should happen.

```python
# Playground discovery:
# DISCOVERY: Empty input returns empty result (not error)

# Becomes test:
def test_empty_input_returns_empty_result():
    """Empty input should return empty result, not raise error."""
    processor = Processor(config)
    result = processor.process([])
    assert result.items == []
    assert result.success is True
    assert result.count == 0
```

### Pattern: Edge Case Test

```python
# Playground discovery:
# EDGE_CASE: Single item works correctly

# Becomes test:
def test_single_item_processing():
    """Single item should process correctly."""
    processor = Processor()
    result = processor.process([42])
    assert len(result.items) == 1
    assert result.items[0] == 42
```

### Pattern: Error Handling Test

```python
# Playground discovery:
# DISCOVERY: None input raises TypeError

# Becomes test:
def test_none_input_raises_type_error():
    """None input should raise TypeError."""
    processor = Processor()
    with pytest.raises(TypeError) as exc_info:
        processor.process(None)
    assert "Cannot be None" in str(exc_info.value)
```

### Pattern: Integration Test

```python
# Playground discovery:
# INTEGRATION: Works with related module

# Becomes test:
def test_integration_with_validator():
    """Processor should work with Validator output."""
    validator = Validator()
    processor = Processor()

    data = {"items": [1, 2, 3]}
    validated = validator.validate(data)
    result = processor.process(validated)

    assert result.success is True
    assert len(result.items) == 3
```

### Pattern: Performance Test

```python
# Playground discovery:
# PERFORMANCE: Processes 10K items in 0.5s

# Becomes test:
def test_performance_threshold():
    """Performance should remain O(n)."""
    processor = Processor()
    large_data = list(range(10000))

    import time
    start = time.time()
    result = processor.process(large_data)
    elapsed = time.time() - start

    # Should be fast (< 1s for 10K items)
    assert elapsed < 1.0, f"Too slow: {elapsed:.2f}s"
```

### Test Conversion Checklist

- [ ] Identify what the discovery revealed
- [ ] Determine if it should always be true (test candidate)
- [ ] Extract minimal reproducible example
- [ ] Write test that verifies the behavior
- [ ] Run test to confirm it passes
- [ ] Add test to test suite

---

## Discovery to Documentation

### Pattern: Docstring Update

```python
# Playground discovery:
# UNDOCUMENTED: What happens with None config?

# Update docstring:
def __init__(self, config: dict | None = None):
    """Initialize processor.

    Args:
        config: Configuration dict with keys:
            - timeout: Max seconds (default: 30)
            - retries: Max retry attempts (default: 3)

            If config is None, uses default settings equivalent to:
            {"timeout": 30, "retries": 3}

    Raises:
        ValueError: If config contains invalid values
    """
```

### Pattern: Behavior Documentation

```python
# Playground discovery:
# UNDOCUMENTED: Empty list handling

# Add to docstring:
def process(self, items: list) -> Result:
    """Process items.

    Args:
        items: List of items to process. Can be empty.

    Returns:
        Result with:
            - items: Processed items (empty if input was empty)
            - count: Number of items processed
            - success: True if all items processed successfully
    """
```

### Pattern: Error Documentation

```python
# Playground discovery:
# UNDOCUMENTED: When errors occur

# Add to docstring:
def process(self, items: list) -> Result:
    """Process items.

    Raises:
        TypeError: If items is not a list
        ValueError: If items contains invalid types
        TimeoutError: If processing exceeds timeout seconds
    """
```

### Pattern: Example Documentation

```python
# Playground discovery:
# FRICTION: Hard to remember parameter order

# Add example to docstring:
def process(self, data: dict, timeout: int = 30, retries: int = 3) -> Result:
    """Process data with options.

    Args:
        data: Data to process
        timeout: Max seconds (default: 30)
        retries: Max attempts (default: 3)

    Example:
        processor = Processor()

        # Basic usage
        result = processor.process({"items": [1, 2, 3]})

        # With custom options
        result = processor.process(
            {"items": [1, 2, 3]},
            timeout=60,
            retries=5,
        )

        # Handle errors
        try:
            result = processor.process(data)
            if result.success:
                print(f"Processed {result.count} items")
        except TimeoutError:
            print("Operation took too long")
    """
```

### Pattern: Performance Documentation

```python
# Playground discovery:
# PERFORMANCE: Quadratic behavior for large inputs

# Add to docstring:
def process(self, items: list) -> Result:
    """Process items.

    Performance:
        - Time: O(n²) where n is number of items
        - Memory: O(n) for internal structures
        - Typical: 100 items in 0.01s, 1000 items in 1s

        For large datasets (>10,000 items), consider:
        - Using process_fast() for O(n log n) performance
        - Batching with process_batch() for memory efficiency

    Warning:
        Processing >100,000 items may exceed memory limits.
        Use streaming approach for large files.
    """
```

### Documentation Checklist

- [ ] Identify what behavior isn't documented
- [ ] Determine which section needs update (Args, Returns, Raises, etc.)
- [ ] Write clear, specific documentation
- [ ] Add examples if behavior is complex
- [ ] Review for clarity and completeness

---

## Discovery to Feature Request

### Pattern: Missing Feature

```python
# Playground discovery:
# MISSING: No batch operation support

# Becomes feature request:
"""
# Feature Request: Batch Processing

## Use Case
Processing multiple items requires looping:

    for item in items:
        result = processor.do_thing(item)

This is inefficient because:
- Each call has overhead
- No ability to parallelize
- Can't optimize across batch

## Proposed Solution
Add batch method:

    results = processor.do_things(items)

Benefits:
- Single call overhead
- Internal parallelization
- Cross-item optimization
- 10-100x faster for large batches

## API Design
```python
def do_things(
    self,
    items: list,
    parallel: bool = True,
    chunk_size: int = 100,
) -> list[Result]:
    '''Process multiple items.

    Args:
        items: List of items to process
        parallel: Use multiprocessing (default: True)
        chunk_size: Items per chunk (default: 100)

    Returns:
        List of Result objects
    '''
```

## Example
```python
processor = Processor()
items = [data1, data2, data3, ...]

# Old way
results = [processor.do_thing(item) for item in items]

# New way
results = processor.do_things(items)
```
"""
```

### Pattern: API Redesign

```python
# Playground discovery:
# FRICTION: Repetitive setup in loops

# Becomes redesign proposal:
"""
# API Redesign: Simplify Initialization

## Problem
Current design requires repeated setup:

    config = load_config()
    for item in items:
        processor = Processor(config)
        processor.initialize()
        result = processor.do_thing(item)

## Proposed Solution
Make initialization optional:

    processor = Processor(config)
    for item in items:
        result = processor.do_thing(item)

## Changes Required
1. Auto-initialize on first use
2. Provide reset() method for clean state
3. Document initialization behavior

## Migration Path
- Old code continues to work
- New code can skip initialize()
- Version 2.0: Make initialize() optional by default
"""
```

### Feature Request Checklist

- [ ] Identify the limitation or missing feature
- [ ] Describe the use case clearly
- [ ] Show current workaround
- [ ] Propose API design
- [ ] Include examples
- [ ] Consider impact and alternatives
- [ ] Decide: In scope? Priority?

---

## Discovery to Improvement

### Pattern: Error Message Improvement

```python
# Playground discovery:
# POOR_ERROR: "Invalid input" doesn't say what's wrong

# Becomes code fix:

# Before
if not data:
    raise ValueError("Invalid input")

# After
if data is None:
    raise TypeError("data cannot be None (required)")
elif not isinstance(data, list):
    raise TypeError(f"data must be list, got {type(data).__name__}")
elif len(data) == 0:
    raise ValueError("data cannot be empty list")
else:
    raise ValueError(f"data contains invalid items: {invalid_items}")
```

### Pattern: Performance Optimization

```python
# Playground discovery:
# PERFORMANCE: O(n²) comparison is slow for large lists

# Becomes code improvement:

# Before (O(n²))
def has_duplicates(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

# After (O(n))
def has_duplicates(items):
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False
```

### Pattern: API Simplification

```python
# Playground discovery:
# FRICTION: Too many required parameters

# Becomes design improvement:

# Before
processor = Processor(
    config={...},
    timeout=30,
    retries=3,
    batch_size=100,
    verbose=False,
)

# After (sensible defaults)
processor = Processor(config={...})

# And if needed:
processor = Processor(
    config={...},
    timeout=60,  # Override just what's needed
)
```

### Improvement Checklist

- [ ] Identify the root cause
- [ ] Propose clear improvement
- [ ] Verify it solves the problem
- [ ] Check for side effects
- [ ] Update tests/docs
- [ ] Get review if team change

---

## Complete Conversion Example

```python
# Playground discovery
discovery = """
DISCOVERY: API requires calling prepare() before every use

Example:
    processor = Processor(config)
    processor.prepare()
    result = processor.do_thing(data1)

    processor.prepare()
    result = processor.do_thing(data2)

This is repetitive and error-prone (forget prepare() → mysterious failures)

FRICTION: Users need to remember prepare() every time

IMPROVEMENT: Auto-prepare on first use or lazy initialization
"""

# Converted to test
def test_auto_prepare_on_first_use():
    """Processor should auto-prepare on first use."""
    processor = Processor(config)
    # No explicit prepare() call!
    result = processor.do_thing(data)
    assert result.success is True

# Converted to documentation
def do_thing(self, data):
    """Process data.

    Note:
        Processor automatically initializes on first call.
        No need to call prepare() explicitly.

    Args:
        data: Data to process

    Returns:
        Result object

    Example:
        processor = Processor(config)
        result = processor.do_thing(data)  # Works immediately
    """

# Converted to feature request
feature_request = """
## Feature: Auto-Preparation

Current behavior requires:
    processor.prepare()
    result = processor.do_thing(data)

Proposed: Auto-prepare on first use:
    result = processor.do_thing(data)  # prepare() called automatically

This simplifies usage and reduces error-prone patterns.
"""
```

---

## Workflow Integration

### Phase 1: After Implementation
- Write playground code
- Run exploration
- Record 10-20 discoveries

### Phase 2: Analysis
- Categorize discoveries (missing, friction, undocumented, etc.)
- Prioritize by impact

### Phase 3: Conversion
- **Tests** - Convert must-have behaviors
- **Docs** - Update docstrings for clarity
- **Features** - Create requests for missing functionality
- **Improvements** - Fix errors, simplify APIs

### Phase 4: Implementation
- Fix urgent issues (errors, docs)
- Create issues for deferred improvements
- Track feature requests

### Phase 5: Verification
- Re-run playground
- Verify fixes
- Update discoveries

---

## Summary

| Discovery Type | Converts To | Priority |
|---|---|---|
| **Undocumented** | Docstring update | High - easy win |
| **Poor Error** | Error message improvement | High - helps users |
| **Edge case found** | Test case | High - prevents regression |
| **Friction** | API simplification | Medium - improves UX |
| **Missing feature** | Feature request | Medium - nice to have |
| **Performance issue** | Optimization or warning | Low - optimize later |

Convert as many discoveries as possible. They represent real user experience.
