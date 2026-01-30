---
name: python-repl
description: REPL-driven development playground for Python packages. Use when exploring APIs interactively, prototyping new features, debugging behavior, or discovering the right abstractions through experimentation. Triggers on requests to explore a package interactively, set up a playground, prototype in REPL, or do exploratory programming.
---

# Playground Exploration: Box-Based Discovery

> "Be the designer, implementor, first user, AND documentation writer."
> -- Donald Knuth, "The Errors of TeX" (1989)

Use **Boxes** to define bounded exploration contexts, then systematically discover what's missing, awkward, or undocumented.

---

## Core Concept: The Box

A **Box** is a bounded context for exploration:

```
┌─────────────────────────────────────────────────────────────┐
│  BOX: user_operations                                       │
│  Target: mypackage.models:User                              │
│                                                             │
│  FIXTURES (what's available):                               │
│    db         → test database instance                      │
│    sample_users → [Alice, Bob]                              │
│    User       → the class under exploration                 │
│                                                             │
│  ASSUMPTIONS (what we're NOT testing):                      │
│    - Database starts empty                                  │
│    - No network calls                                       │
│    - Single-threaded access                                 │
│                                                             │
│  QUESTIONS (what we want to discover):                      │
│    □ USABILITY: How easy is it to create a user?            │
│    □ FEATURE: Is there bulk creation?                       │
│    □ ERROR: What happens with duplicate names?              │
│    □ EDGE: How does it handle empty strings?                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## LLM Workflow

### 1. Define the Box

Create a box definition for the module you're exploring:

```python
# playground/user_operations.box.py
"""
Box: user_operations
Target: mypackage.models:User
Description: Exploring User model CRUD and validation

Fixtures:
  db: |
    from mypackage.db import create_test_db
    db = create_test_db()

  sample_users: |
    from mypackage.models import User
    users = [User(name="Alice"), User(name="Bob")]

Assumptions:
  - Database is empty at session start
  - No external API calls
  - Validation is synchronous

Questions:
  - USABILITY: How many steps to create a user?
  - USABILITY: Are required fields obvious?
  - FEATURE: Is there a bulk_create method?
  - FEATURE: Can I update a user in place?
  - ERROR: What happens with duplicate names?
  - ERROR: What's the error message for invalid email?
  - EDGE: Empty string for name?
  - EDGE: Very long name (1000+ chars)?
  - PERFORMANCE: Creating 1000 users - acceptable speed?
"""
```

### 2. Explore with Eyeball

Use eyeball to answer each question:

```bash
# Understand what's available
eyeball discover mypackage.models
eyeball -p inspect mypackage.models:User

# Answer: USABILITY - How many steps to create a user?
eyeball probe "from mypackage.models import User; u = User(name='test'); print(u)"
# Observation: Just one step - good!

# Answer: FEATURE - Is there bulk_create?
eyeball probe "from mypackage.models import User; print(dir(User))"
# Observation: No bulk_create - MISSING feature

# Answer: ERROR - Duplicate names?
eyeball probe "
from mypackage.models import User
from mypackage.db import create_test_db
db = create_test_db()
db.add(User(name='Alice'))
db.add(User(name='Alice'))  # Duplicate
db.commit()
"
# Observation: No error! Silent duplicate - needs validation

# Answer: EDGE - Empty string?
eyeball probe "from mypackage.models import User; User(name='')"
# Observation: Allowed but shouldn't be - MISSING validation
```

### 3. Log Discoveries

Track what you find in structured format:

```yaml
# playground/user_operations.discoveries.yaml
box: user_operations
explored: 2024-01-15
status: in_progress

discoveries:
  - type: USABILITY
    rating: good
    finding: "Single-step user creation"
    detail: "User(name='x') works directly, no factory needed"
    action: none

  - type: MISSING
    finding: "No bulk_create method"
    detail: "Must create users one at a time in a loop"
    action: "Consider adding User.bulk_create(items)"
    priority: medium

  - type: MISSING
    finding: "No duplicate name validation"
    detail: "Can create multiple users with same name"
    action: "Add unique constraint or validation"
    priority: high

  - type: MISSING
    finding: "Empty name allowed"
    detail: "User(name='') succeeds but shouldn't"
    action: "Add name validation: non-empty, reasonable length"
    priority: high

  - type: FRICTION
    finding: "Error messages lack context"
    detail: "'Invalid input' doesn't say which field"
    action: "Include field name in validation errors"
    priority: medium

unanswered_questions:
  - "PERFORMANCE: Creating 1000 users - acceptable speed?"
  - "EDGE: Very long name (1000+ chars)?"
```

### 4. Convert to Actions

Discoveries become:
- **Tests** → Formal pytest tests
- **Issues** → GitHub issues for missing features
- **Docs** → Docstring updates for undocumented behavior
- **Fixes** → Immediate code changes for critical issues

---

## Question Categories

When defining a Box, pose questions across these categories:

### USABILITY
*How easy is it to use correctly?*

- How many steps to accomplish the primary task?
- Are required parameters obvious?
- Do defaults make sense?
- Is the API self-documenting?

```bash
# Probe usability
eyeball probe "from mypackage import Thing; t = Thing(); print(t)"
# How hard was that? What did I need to know?
```

### FEATURE
*What capabilities exist or are missing?*

- Does it support batch operations?
- Can I customize behavior?
- Are there convenience methods?
- What's the API surface area?

```bash
# Check available features
eyeball -p inspect mypackage.models:User
eyeball probe "print([m for m in dir(User) if not m.startswith('_')])"
```

### ERROR
*How does it fail? Are errors helpful?*

- What happens with invalid input?
- Are error messages specific?
- Can I recover from errors?
- Are exceptions typed appropriately?

```bash
# Test error handling
eyeball probe "from mypackage import Thing; Thing(invalid=True)"
# Is the error message helpful?
```

### EDGE
*What happens at boundaries?*

- Empty input ([], "", None)
- Single item
- Maximum size
- Special characters (unicode, null bytes)
- Concurrent access

```bash
# Test edges
eyeball probe "from mypackage import process; process([])"
eyeball probe "from mypackage import process; process(['x' * 10000])"
```

### PERFORMANCE
*Is it fast enough?*

- Acceptable speed for typical input?
- How does it scale?
- Memory usage reasonable?

```bash
# Quick performance check
eyeball probe "
import time
from mypackage import process
start = time.time()
process(list(range(10000)))
print(f'10K items: {time.time() - start:.2f}s')
"
```

---

## Discovery Types

| Type | Meaning | Action |
|------|---------|--------|
| **MISSING** | Feature that should exist | File issue or implement |
| **FRICTION** | Works but awkward | Simplify API |
| **UNDOCUMENTED** | Behavior not explained | Update docstring |
| **ERROR_MESSAGE** | Unhelpful error text | Improve message |
| **PERFORMANCE** | Too slow | Optimize or document limitation |
| **BUG** | Incorrect behavior | Fix immediately |

---

## Box File Format

Boxes can be defined as Python files with structured docstrings:

```python
# playground/boxes/user_crud.box.py
"""
Box: user_crud
Target: mypackage.models:User
Description: CRUD operations on User model

Fixtures:
  db: |
    from mypackage.db import Database
    db = Database(":memory:")
    db.initialize()

  User: |
    from mypackage.models import User

Assumptions:
  - Fresh database each exploration
  - No authentication required
  - Single-threaded

Questions:
  USABILITY:
    - How do I create a user?
    - How do I find a user by ID?
    - How do I update a user's email?
    - How do I delete a user?

  FEATURE:
    - Can I query users by name?
    - Is there pagination for list operations?
    - Can I bulk create users?

  ERROR:
    - What happens if I delete a non-existent user?
    - What's the error for invalid email format?

  EDGE:
    - Maximum name length?
    - Unicode in names?
"""

# Optional: Pre-configured eyeball fixtures
def get_fixtures():
    """Return fixtures for eyeball probes."""
    from mypackage.db import Database
    from mypackage.models import User

    db = Database(":memory:")
    db.initialize()

    return {
        "db": db,
        "User": User,
        "sample_user": User(name="Alice", email="alice@example.com"),
    }
```

---

## Integration with Eyeball

Register box fixtures with eyeball for use in probes:

```python
# mypackage/fixtures.py
from eyeball.harness import Fixtures

@Fixtures.register("user_crud_box")
def user_crud_box():
    """Fixtures for user_crud box exploration."""
    from mypackage.db import Database
    from mypackage.models import User

    db = Database(":memory:")
    db.initialize()

    return {
        "db": db,
        "User": User,
        "create_user": lambda name: db.add(User(name=name)),
    }
```

Then explore:
```bash
eyeball probe --fixture user_crud_box "u = create_user('Alice'); print(db.get(u.id))"
```

---

## Complete Example

### 1. Define Box

```python
# playground/boxes/data_processor.box.py
"""
Box: data_processor
Target: mypackage.processing:DataProcessor
Description: Exploring the data processing pipeline

Fixtures:
  processor: |
    from mypackage.processing import DataProcessor
    processor = DataProcessor()

  sample_data: |
    data = [{"id": i, "value": i * 10} for i in range(100)]

Assumptions:
  - Data fits in memory
  - No external services
  - Synchronous processing

Questions:
  USABILITY:
    - How do I process a single item?
    - How do I process a batch?
    - Can I stream results?

  FEATURE:
    - Is there filtering support?
    - Can I transform during processing?
    - Is there progress reporting?

  ERROR:
    - What if an item fails mid-batch?
    - Can I retry failed items?

  EDGE:
    - Empty input?
    - Single item?
    - 1 million items?

  PERFORMANCE:
    - Items per second?
    - Memory usage for large batches?
"""
```

### 2. Explore

```bash
# Understand the API
eyeball -p inspect mypackage.processing:DataProcessor

# USABILITY: Single item processing
eyeball probe "
from mypackage.processing import DataProcessor
p = DataProcessor()
result = p.process({'id': 1, 'value': 10})
print(f'Result: {result}')
"
# Finding: Works! Returns transformed dict

# FEATURE: Filtering
eyeball probe "
from mypackage.processing import DataProcessor
p = DataProcessor()
print([m for m in dir(p) if 'filter' in m.lower()])
"
# Finding: No filter method - MISSING

# ERROR: Mid-batch failure
eyeball probe "
from mypackage.processing import DataProcessor
p = DataProcessor()
data = [{'id': 1}, {'id': 'invalid'}, {'id': 3}]
try:
    p.process_batch(data)
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
"
# Finding: Fails on first error, no partial results - FRICTION

# EDGE: Empty input
eyeball probe "
from mypackage.processing import DataProcessor
p = DataProcessor()
result = p.process_batch([])
print(f'Empty result: {result}')
"
# Finding: Returns [] - good!
```

### 3. Record Discoveries

```yaml
# playground/data_processor.discoveries.yaml
box: data_processor
explored: 2024-01-15

discoveries:
  - type: USABILITY
    rating: good
    finding: "Simple single-item API"
    detail: "processor.process(item) just works"

  - type: MISSING
    finding: "No filtering support"
    action: "Add processor.filter(predicate) method"
    priority: medium

  - type: FRICTION
    finding: "Batch fails on first error"
    detail: "No way to get partial results or skip bad items"
    action: "Add on_error='skip'|'raise'|'collect' parameter"
    priority: high

  - type: USABILITY
    rating: good
    finding: "Empty input handled gracefully"
    detail: "Returns empty list, no error"
```

### 4. Convert to Tests

```python
# tests/test_data_processor.py
"""Tests derived from playground exploration."""

def test_single_item_processing():
    """USABILITY: Single item works."""
    processor = DataProcessor()
    result = processor.process({"id": 1, "value": 10})
    assert result is not None

def test_empty_batch_returns_empty_list():
    """EDGE: Empty input handled."""
    processor = DataProcessor()
    assert processor.process_batch([]) == []

def test_batch_error_handling():
    """ERROR: Mid-batch failure behavior.

    Currently fails on first error (discovered friction).
    This test documents current behavior.
    """
    processor = DataProcessor()
    with pytest.raises(ValueError):
        processor.process_batch([{"id": 1}, {"id": "invalid"}])
```

---

## Quick Reference

```bash
# Define box → explore → discover → convert

# 1. Understand target
eyeball discover mypackage.module
eyeball -p inspect mypackage.module:Class

# 2. Pose questions (USABILITY, FEATURE, ERROR, EDGE, PERFORMANCE)

# 3. Answer with probes
eyeball probe "from mypackage import X; ..."
eyeball probe --fixture my_box "..."

# 4. Log discoveries (MISSING, FRICTION, UNDOCUMENTED, BUG)

# 5. Convert to tests/issues/docs
```

---

## Related Skills

- **eyeball-introspection** - Full eyeball command reference
- **python-testing** - Converting discoveries to formal tests
- **python-coding-standards** - Code quality standards
