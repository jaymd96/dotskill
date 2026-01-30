# Eyeball Workflow Integration

How eyeball integrates into each phase of the Python development workflow.

---

## Phase 0: Discovery

**Goal:** Understand the problem before building.

### Exploring Existing Code

Before modifying anything, understand what exists:

```bash
# What modules are in the package?
eyeball discover mypackage

# What's in the specific module I'll modify?
eyeball discover mypackage.models

# How does the key class work?
eyeball -p inspect mypackage.models:Entity
```

**Output tells you:**
- What classes and functions exist
- Their signatures and parameters
- Docstrings and type hints
- What's defined locally vs imported

### Understanding Dependencies

Before adding code, understand what it will affect:

```bash
# What does this module import?
eyeball -p module-deps mypackage.models

# What uses the class I might modify?
eyeball callers mypackage.models:Entity

# What does the function I'm extending depend on?
eyeball deps mypackage.services:process_order
```

**This prevents:**
- Breaking existing functionality
- Circular imports
- Unexpected side effects

### Evaluating Third-Party Libraries

When researching packages (per `package-research` skill):

```bash
# Search for functionality
eyeball search-api sqlalchemy session
eyeball search-api pydantic validator

# Verify API before committing to a library
eyeball -p api sqlalchemy.orm:Session
eyeball -p api pydantic:BaseModel
```

**Before adopting a library:**
1. `search-api` to find relevant functions
2. `api` to understand signatures and usage
3. Verify it matches your needs

### Discovery Checklist

- [ ] `eyeball discover` on modules I'll modify
- [ ] `eyeball inspect` on key classes/functions
- [ ] `eyeball callers` to understand impact
- [ ] `eyeball api` on third-party libraries I'll use
- [ ] Document findings for Manager report

---

## Phase 1: Development

### Step 1: Implementation

**Use `api` to verify correct library usage:**

```bash
# Before writing code that uses requests
eyeball -p api requests:Session.request

# Check the exact parameter names and types
# Output shows:
# - signature: (method, url, **kwargs)
# - parameters with descriptions
# - return type
```

**Pattern: Check → Write → Verify**

```bash
# 1. Check the API
eyeball api httpx:Client.get

# 2. Write code using it
# async with httpx.AsyncClient() as client:
#     response = await client.get(url, params=params)

# 3. Verify with probe
eyeball probe "import httpx; print(httpx.Client.get.__doc__[:100])"
```

### Step 2: Layout & Organization

After organizing files, verify structure:

```bash
# Check module is importable
eyeball discover mypackage.new_module

# Verify exports
eyeball exec "from mypackage.new_module import *; print(dir())"
```

### Step 3: Standards Check

Use probes to verify standards compliance:

```bash
# Check all public functions have docstrings
eyeball probe "
from mypackage.new_module import MyClass
for name in dir(MyClass):
    if not name.startswith('_'):
        method = getattr(MyClass, name)
        if callable(method):
            assert method.__doc__, f'{name} missing docstring'
"

# Check type hints exist
eyeball -p inspect mypackage.new_module:MyClass
# Verify parameters show type hints in output
```

### Step 4: Code Review

Before independent review, self-check with eyeball:

```bash
# Analyze what your new code depends on
eyeball -p deps mypackage.new_module:NewClass

# Check for unexpected dependencies
# Output shows imports, calls, instantiations
```

### Step 5: Experimentation (Playground)

**This is where eyeball shines.** Use probes as your playground:

```bash
# Happy path
eyeball probe "
from mypackage.models import User
user = User(name='test', email='test@example.com')
assert user.name == 'test'
assert user.email == 'test@example.com'
print('Happy path: PASS')
"

# Edge case: empty input
eyeball probe "
from mypackage.models import User
try:
    user = User(name='', email='test@example.com')
    assert False, 'Should have raised'
except ValueError as e:
    assert 'empty' in str(e).lower()
    print('Empty name rejected: PASS')
"

# Edge case: invalid email
eyeball probe "
from mypackage.models import User
try:
    user = User(name='test', email='not-an-email')
    assert False, 'Should have raised'
except ValueError as e:
    assert 'email' in str(e).lower()
    print('Invalid email rejected: PASS')
"

# Integration: works with database
eyeball probe --fixture test_db "
user = User(name='test', email='test@example.com')
db.save(user)
loaded = db.get_user(user.id)
assert loaded.name == user.name
print('Database integration: PASS')
"
```

**Minimum 5 scenarios required by quality gates.**

### Step 6: Testing

Run formal tests with structured output:

```bash
# Run tests for the module
eyeball test mypackage.new_module

# Verbose output for debugging failures
eyeball test mypackage.new_module -v

# Run specific test
eyeball test mypackage.new_module -k "test_validation"

# With coverage
eyeball test mypackage.new_module --coverage
```

**Interpret results:**
```json
{
  "status": "success",
  "summary": {"total": 15, "passed": 15, "failed": 0},
  "passed": [...],
  "failed": []
}
```

If failed:
```json
{
  "status": "failed",
  "summary": {"total": 15, "passed": 13, "failed": 2},
  "failed": [
    {"test": "test_validation_rejects_empty", "error_type": "AssertionError", "line": 42}
  ]
}
```

---

## Phase 2: Refinement

**Goal:** Fix specific issues Manager flagged.

### Verify Specific Fixes

Manager says: "Empty string validation is missing"

```bash
# 1. Write the fix
# 2. Probe to verify
eyeball probe "
from mypackage.models import User
try:
    User(name='')
    assert False, 'Should reject empty'
except ValueError:
    print('FIXED: Empty name rejected')
"

# 3. Run targeted test
eyeball test mypackage.models -k "empty"
```

### Regression Check

After fixing, verify nothing else broke:

```bash
# Run full test suite
eyeball test mypackage.models

# Check callers still work
eyeball callers mypackage.models:User
# Then probe each caller if concerned
```

### Quick Iteration Loop

```bash
# Fix → Probe → Fix → Probe until passing
while true; do
    eyeball probe "from mypackage import func; assert func(x) == expected"
    # If passes, break
    # If fails, fix and repeat
done
```

---

## Phase 3: Completion

### Full Test Suite

```bash
# Run everything
eyeball test mypackage --coverage

# Verify all pass
# Check coverage output
```

### Final Verification

```bash
# Verify all public APIs documented
eyeball -p inspect mypackage.new_module:NewClass
# Check docstrings exist

# Verify dependencies are clean
eyeball -p module-deps mypackage.new_module
# Should show expected imports only

# Verify nothing unexpected uses new code
eyeball callers mypackage.new_module:NewClass
# Should be empty or expected list
```

### Document for PR

Include in PR description:

```markdown
## Verification

```bash
eyeball test mypackage.new_module --coverage
# Result: 15 passed, 0 failed, 95% coverage

eyeball probe "from mypackage import NewClass; assert NewClass(x).process() == y"
# Result: success
```
```

---

## Integration Summary

| Phase | Step | Eyeball Command | Purpose |
|-------|------|-----------------|---------|
| 0 | Discovery | `discover`, `inspect` | Understand existing code |
| 0 | Discovery | `api`, `search-api` | Evaluate libraries |
| 0 | Discovery | `deps`, `callers` | Understand relationships |
| 1 | Step 1 | `api` | Verify API usage |
| 1 | Step 2 | `discover` | Verify structure |
| 1 | Step 3 | `inspect`, `probe` | Check standards |
| 1 | Step 4 | `deps` | Review dependencies |
| 1 | Step 5 | `probe` | Playground experiments |
| 1 | Step 6 | `test` | Formal testing |
| 2 | Refinement | `probe`, `test -k` | Verify fixes |
| 3 | Completion | `test --coverage` | Final verification |
