# Discovery Categories and Patterns

What to look for during exploration and how to identify each type.

---

## Overview

Discoveries fall into five categories. Learn to recognize each type and what it means for your API.

| Category | Question | Example | Action |
|----------|----------|---------|--------|
| **Missing** | What would make this easier? | No batch API | Add feature |
| **Friction** | What feels awkward? | Repetitive calls | Simplify API |
| **Undocumented** | What's unclear? | Behavior not explained | Update docs |
| **Error Messages** | Are they helpful? | Generic "Error" | Improve clarity |
| **Performance** | Is it acceptable? | Slow operation | Optimize or document |

---

## 1. Missing Features

### Definition
Features that would be useful but don't exist. Things you wish you could do.

### How to Spot Them

**You find yourself doing something repetitive:**
```python
# MISSING: Batch operation support
for item in items:
    result = processor.do_thing(item)  # Called N times
    # Would prefer:
    # results = processor.do_things(items)  # Single call
```

**You work around a limitation:**
```python
# MISSING: Timeout configuration
# Have to restructure code to work around fixed timeout
result = processor.process(data)  # No way to set timeout
```

**You implement something the library should do:**
```python
# MISSING: Retry logic
for attempt in range(3):
    try:
        result = processor.do_thing(data)
        break
    except TransientError:
        continue
# Should be: result = processor.do_thing(data)  # with auto-retry
```

### Examples

```python
# MISSING: State inspection
# Can't check if ready before operating
if instance.is_ready():  # This doesn't exist
    instance.do_thing()

# MISSING: Bulk operations
# Must handle items one by one
for item in items:
    instance.process(item)
# vs single bulk call

# MISSING: Custom handlers
# Can't hook into lifecycle events
instance.on_error = my_handler  # This doesn't work

# MISSING: Configuration options
# Can't customize behavior
instance = Processor()  # No parameters
# vs instance = Processor(cache_size=1000, timeout=60)
```

### What to Do

1. **Document clearly:**
   ```python
   # MISSING: Batch processing
   # Use case: Process many items efficiently
   # Current: for item in items: processor.process(item)
   # Desired: processor.process_batch(items)
   ```

2. **Ask: Is this in scope?**
   - Does it fit the library's purpose?
   - Is it a core feature or edge case?

3. **Create feature request:**
   - Describe the use case
   - Show current workaround
   - Suggest API design

---

## 2. API Friction

### Definition
Awkward or repetitive usage patterns that work but feel wrong.

### How to Spot Them

**You notice boilerplate:**
```python
# FRICTION: Repetitive setup
for item in items:
    instance.reset()          # Reset needed each time
    instance.configure(cfg)   # Config needed each time
    instance.do_thing(item)

# Better: Setup once, use multiple times
instance = Processor(cfg)
for item in items:
    instance.do_thing(item)
```

**You find yourself wrapping the API:**
```python
# FRICTION: Parameters in wrong order (hard to remember)
result = processor.process(
    data,
    timeout,
    retries,
    batch_size,
    callback,
    verbose,
)

# Better: Named parameters or sensible defaults
result = processor.process(
    data,
    timeout=30,
    retries=3,
)
```

**You prefer a different API style:**
```python
# FRICTION: Awkward chaining
result = processor.do_a(data)
result = processor.do_b(result)
result = processor.do_c(result)

# Better: Fluent/chainable
result = processor.do_a(data).do_b().do_c()
```

### Examples

```python
# FRICTION: Must initialize before every operation
processor = Processor(config)
processor.initialize()
processor.do_thing(data)

# vs better design:
processor = Processor(config)  # Initialize once
processor.do_thing(data)       # Ready immediately

# FRICTION: Deeply nested imports
from mypackage.subpackage.submodule.core import Processor
# vs simpler:
from mypackage import Processor

# FRICTION: Complex configuration
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "credentials": {"user": "admin", "pass": "xxx"},
    },
    "cache": {"type": "redis", ...},
    # ... 20 more options
}
processor = Processor(config)
# vs simpler:
processor = Processor(db_host="localhost")

# FRICTION: Inconsistent API
instance.process(data)      # Returns Result
instance.validate(data)     # Returns bool
instance.transform(data)    # Returns dict
# Should all return same type or consistently documented
```

### What to Do

1. **Document the friction:**
   ```python
   # FRICTION: Must call prepare() before each operation
   # Causes: Repetitive boilerplate in loops
   # Improvement: Auto-prepare on first use
   ```

2. **Suggest simplification:**
   - Remove unnecessary steps
   - Provide sensible defaults
   - Improve naming/ordering
   - Support method chaining

3. **Consider API redesign:**
   - This is valuable feedback for next version
   - Often indicates conceptual issue

---

## 3. Undocumented Behavior

### Definition
Code works but its behavior isn't explained in docstrings or documentation.

### How to Spot Them

**You test something and behavior is unclear:**
```python
# UNDOCUMENTED: What happens with None config?
processor = Processor(config=None)  # Allowed, but what happens?

# Docstring should say:
"""
Args:
    config: Configuration dict. If None, uses default settings.
"""
```

**You discover behavior not in the docstring:**
```python
# UNDOCUMENTED: Timeout units
processor.process(data, timeout=30)  # Is this seconds? milliseconds?

# Docstring should specify:
"""
Args:
    timeout: Maximum time in seconds (default: 30). If exceeded, raises TimeoutError.
"""
```

**Edge cases aren't documented:**
```python
# UNDOCUMENTED: What if items is empty?
result = processor.process([])  # Returns empty result? Or error?

# Should be documented:
"""
Args:
    items: List of items to process. Can be empty.

Returns:
    Result with empty items list if input was empty.
"""
```

### Examples

```python
# UNDOCUMENTED: Retry behavior
# Code retries on failure, but docstring doesn't mention it
result = processor.do_thing(data)

# Should document:
"""
Automatically retries up to 3 times on transient failures.
Raises PermanentError if all retries fail.
"""

# UNDOCUMENTED: Side effects
# Function modifies input in place - not mentioned
processor.transform(data)  # data was modified!

# Should document:
"""
Modifies input dict in place. To preserve original:
    import copy
    result = processor.transform(copy.deepcopy(data))
"""

# UNDOCUMENTED: Performance characteristics
# This is O(n²) but not documented
result = processor.process(large_list)

# Should document:
"""
Time complexity: O(n²) where n is number of items.
For large datasets (>1000 items), use process_fast() for O(n log n).
"""

# UNDOCUMENTED: State requirements
# Must be in specific state before calling
processor.process(data)  # Fails silently if not initialized

# Should document:
"""
Requires initialization via __init__() or reset().
Raises RuntimeError if called before initialization.
"""
```

### What to Do

1. **Identify the behavior:**
   - What does it actually do?
   - What should users expect?

2. **Update docstring:**
   ```python
   def process(self, data: list, timeout: int = 30) -> Result:
       """Process data with automatic retry.

       Args:
           data: List of items to process (can be empty)
           timeout: Max time in seconds (default: 30)

       Returns:
           Result with processed items

       Raises:
           TypeError: If data is not a list
           TimeoutError: If timeout exceeded

       Note:
           Automatically retries up to 3 times on transient errors.
       """
   ```

3. **Add examples if complex:**
   ```python
   def process(self, data: list) -> Result:
       """Process data.

       Example:
           processor = Processor()
           result = processor.process([1, 2, 3])
           if result.success:
               print(result.items)
       """
   ```

---

## 4. Poor Error Messages

### Definition
Errors that occur but don't help you fix the problem.

### How to Spot Them

**You get a vague error:**
```python
# POOR: Generic message
try:
    processor.process(data)
except ValueError as e:
    print(e)  # Output: "Invalid input"
    # What's invalid? Which field? What's expected?
```

**You don't know which item failed:**
```python
# POOR: No context
try:
    result = processor.process([...huge list...])
except ProcessingError as e:
    print(e)  # "Processing failed"
    # Which item? Index? Content?
```

**The error doesn't match the real issue:**
```python
# POOR: Misleading error message
processor.process(None)
# Error: "Attribute error: 'NoneType' has no attribute 'length'"
# Better: "data parameter cannot be None"
```

### Examples

```python
# POOR ERROR MESSAGES

# ❌ Too generic
raise ValueError("Invalid input")

# ✅ Better - specific and actionable
raise ValueError("Expected list for 'items', got str")

# ❌ No context
raise ProcessingError("Failed to process")

# ✅ Better - includes context
raise ProcessingError(f"Failed to process item {i}: {item_data}")

# ❌ Doesn't explain the fix
raise ValueError("Invalid range")

# ✅ Better - explains valid range
raise ValueError(f"timeout must be 1-300 seconds, got {timeout}")

# ❌ Stack trace instead of explanation
raise RuntimeError("unsupported operand type(s)")

# ✅ Better - explains what went wrong
raise TypeError("config must be dict, not {type(config).__name__}")

# ❌ Vague about requirements
raise AssertionError("Configuration error")

# ✅ Better - specific requirements
raise ValueError(f"config['cache'] must have 'size' key, got {config.get('cache')}")
```

### What to Do

1. **Test error messages:**
   ```python
   # Good test
   with pytest.raises(ValueError) as exc_info:
       processor.process(None)

   assert "Expected list" in str(exc_info.value)
   assert "got" in str(exc_info.value)
   ```

2. **Improve error messages in code:**
   ```python
   # Before
   if not data:
       raise ValueError("Invalid data")

   # After
   if not data:
       raise ValueError("data must be a non-empty list")

   # Even better
   if data is None:
       raise TypeError("data cannot be None")
   elif not isinstance(data, list):
       raise TypeError(f"data must be list, got {type(data).__name__}")
   elif len(data) == 0:
       raise ValueError("data cannot be empty list")
   ```

3. **Include helpful context:**
   ```python
   try:
       result = processor.process_item(item)
   except SomeError:
       raise ProcessingError(
           f"Failed to process item at index {i}: {item}\n"
           f"Original error: {e}"
       )
   ```

---

## 5. Performance Issues

### Definition
Operations that are too slow, use too much memory, or have unacceptable characteristics.

### How to Spot Them

**It's slower than expected:**
```python
import time

start = time.time()
result = processor.process(large_data)
elapsed = time.time() - start

print(f"Took {elapsed:.2f}s for {len(large_data)} items")
# PERFORMANCE: Takes 10s for 1000 items = 10ms per item (too slow)
```

**Memory usage grows unexpectedly:**
```python
import tracemalloc

tracemalloc.start()
result = processor.process(large_data)
current, peak = tracemalloc.get_traced_memory()

print(f"Peak memory: {peak / 1024 / 1024:.1f} MB")
# PERFORMANCE: Uses 1GB for 1M items = 1byte per item × 1000? (too much)
```

**Behavior gets worse with size:**
```python
# PERFORMANCE: O(n²) behavior
# 100 items: 0.1s
# 1000 items: 10s
# 10000 items: 1000s
# Pattern suggests quadratic behavior
```

### Examples

```python
# PERFORMANCE: N² algorithm
# Comparing each item to every other item
for i in range(len(items)):
    for j in range(len(items)):
        if items[i] == items[j]:  # Naive
            ...

# Better: O(n log n) with sorting or O(n) with set
seen = set(items)
for item in items:
    if item in seen:  # Fast lookup
        ...

# PERFORMANCE: No caching
def expensive_calculation(x):
    time.sleep(1)  # Simulate expensive work
    return x * 2

result = expensive_calculation(5)  # 1s
result = expensive_calculation(5)  # 1s again - no caching!

# Better: Cache results
@functools.lru_cache(maxsize=128)
def expensive_calculation(x):
    time.sleep(1)
    return x * 2

# PERFORMANCE: Loading everything into memory
def process_file(filename):
    with open(filename) as f:
        all_lines = f.readlines()  # All 1GB at once
    for line in all_lines:
        process(line)

# Better: Stream processing
def process_file(filename):
    with open(filename) as f:
        for line in f:  # One at a time
            process(line)
```

### What to Do

1. **Measure and document:**
   ```python
   # PERFORMANCE: Quadratic behavior
   # 100 items: 0.1s, 1000 items: 10s, 10000: 1000s
   # Caused by nested loops comparing items
   # ACTION: Replace with hash-based approach (O(n))
   ```

2. **Add performance warning:**
   ```python
   def process(self, items: list) -> Result:
       """Process items.

       Warning:
           For >10000 items, consider using process_fast() which
           sacrifices accuracy for speed: O(n) vs O(n²)
       """
   ```

3. **Profile and optimize:**
   ```python
   import cProfile
   cProfile.run('processor.process(large_data)')

   # Identify hot spots
   # Optimize bottlenecks
   # Measure improvement
   ```

---

## Summary Matrix

| Discovery | Indicator | Action |
|-----------|-----------|--------|
| **Missing** | You work around a limitation | Request feature |
| **Friction** | Repetitive or awkward code | Simplify API |
| **Undocumented** | Behavior isn't explained | Update docstring |
| **Poor Error** | Error doesn't help fix | Improve message |
| **Performance** | Too slow or memory-heavy | Optimize or document |

All five categories are valuable feedback. Record them all.
