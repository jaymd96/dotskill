# Best Practices, Checklists, and Workflow Integration

Proven patterns for successful playground-driven development.

---

## Best Practices

### Do ✓

#### Run Playground Frequently
```python
# Good workflow:
# 1. Implement feature
# 2. Run playground
# 3. Find issues
# 4. Fix issues
# 5. Re-run playground
# Repeat until solid

# Not: Save all testing for the end
```

**Why:** Early feedback catches issues before they compound.

#### Document Every Discovery
```python
# Good: Record everything
print("[DISCOVERY] Empty list returns None (not empty result)")
print("[FRICTION] Config required for every call")
print("[MISSING] No batch processing support")

# Not: Only record "important" findings
# You can't act on what you forgot!
```

**Why:** Discoveries fade from memory. Writing them down preserves the insight.

#### Keep Playground Code Clean and Runnable
```python
# Good
def explore_basic_usage() -> bool:
    """Clear, documented function."""
    processor = Processor()
    result = processor.process([1, 2, 3])
    assert result.count == 3
    return True

if __name__ == "__main__":
    success = explore_basic_usage()
    sys.exit(0 if success else 1)

# Not
def test():  # Vague name
    # Do stuff
    x = get_processor()
    y = x.do_stuff([1,2,3])  # Unclear
    # Maybe it works? Hard to tell
```

**Why:** Code you can't run isn't useful. Code you can't understand is a time sink.

#### Convert Stable Patterns to Formal Tests
```python
# Good: Playground discovers behavior → becomes test

# Playground:
result = processor.process([])
print(f"Empty: {result}")  # Record observation

# Later, convert to test:
def test_empty_input():
    result = processor.process([])
    assert result.items == []

# Not: Keep using playground for same things forever
# Playground is for discovery, tests are for verification
```

**Why:** Tests ensure behaviors don't regress. Playground discovers them.

#### Update Playground When Module Changes
```python
# Good: Playground evolves with code
# When API changes:
# 1. Update playground to reflect new API
# 2. Re-run to verify behavior
# 3. Record new discoveries

# Not: Leave playground outdated
# Outdated code is misleading and becomes dead weight
```

**Why:** Playground is documentation. Docs must be accurate.

---

### Don't ✗

#### Don't Delete Playground Code After Testing
```python
# Bad: Deleting playgrounds
rm playground/processor_exploration.py  # ❌ Deletes valuable discovery tool

# Good: Keep it in version control
git add playground/processor_exploration.py
git commit -m "Add playground exploration for processor module"
```

**Why:** Playground isn't throwaway. It's the first documentation and lives with the code.

#### Don't Skip Exploration Because "Tests Are Enough"
```python
# Bad: Assuming tests cover everything
# Tests verify known requirements
# Playground discovers unknown requirements!

def test_existing_behavior():
    # Tests what you already know should happen
    pass

# Good: Use both
# Tests verify behavior
# Playground discovers behavior you didn't think to test
```

**Why:** Playground finds things tests don't (missing features, friction, docs gaps).

#### Don't Ignore Friction Points
```python
# Bad: Dismissing usability issues
print("[FRICTION] API is awkward, but it works")
# → Nothing changes, users suffer forever

# Good: Act on friction
print("[FRICTION] API is awkward")
# → Create issue, consider redesign, improve UX
```

**Why:** Friction compounds. Fix it early or pay for it forever.

#### Don't Write Exploration Code You Can't Run
```python
# Bad: Exploration that doesn't work
def explore():
    # Import that doesn't exist
    from foo import bar  # ❌ Crashes

    # Using undefined variables
    processor.process(nonexistent_data)  # ❌ NameError

# Good: Exploration that works
def explore():
    processor = Processor()
    data = [1, 2, 3]
    result = processor.process(data)  # ✓ Runs
```

**Why:** Non-runnable code is useless. It's not exploration, it's fiction.

#### Don't Treat Playground as Throwaway
```python
# Bad: Temporary exploration code
# Not in version control
# No cleanup
# Forgotten immediately

# Good: Permanent discovery tool
# In version control
# Maintained with project
# Referenced by developers
```

**Why:** Playground is an asset. It documents real usage patterns.

---

## Checklists

### Playground Setup Checklist

Before exploring:

- [ ] Created `playground/{module}_exploration.py` file
- [ ] File is executable: `python playground/{module}.py`
- [ ] Module under exploration is imported correctly
- [ ] Helper functions defined: `print_section()`, `print_result()`
- [ ] File has docstring explaining what it explores
- [ ] At least 4 exploration functions planned:
  - [ ] Basic usage (happy path)
  - [ ] Edge cases (boundaries)
  - [ ] Error handling (failures)
  - [ ] Discoveries (findings)
- [ ] Main execution block collects and reports results
- [ ] Returns proper exit code (0=success, 1=failure)

### Exploration Completeness Checklist

After exploring:

- [ ] Tested 5+ distinct scenarios (happy path, edge cases, errors, integration, performance)
- [ ] Each scenario documented with clear assertions
- [ ] Discoveries recorded with category tags (MISSING, FRICTION, etc.)
- [ ] Error messages reviewed for clarity and helpfulness
- [ ] Edge cases identified and tested:
  - [ ] Empty input
  - [ ] Single item
  - [ ] Maximum size
  - [ ] Invalid types
  - [ ] Special characters/unicode
  - [ ] Concurrent access (if applicable)
- [ ] Integration with related modules tested
- [ ] Performance measured (optional but recommended)
- [ ] All discoveries have action items assigned
- [ ] Playground code is clean and well-organized
- [ ] Code is committed to version control

### Discovery Processing Checklist

After exploring:

- [ ] All discoveries categorized:
  - [ ] Missing features
  - [ ] API friction
  - [ ] Undocumented behavior
  - [ ] Poor error messages
  - [ ] Performance issues
- [ ] Discoveries prioritized by impact
- [ ] Urgent items (errors, docs) scheduled for immediate fix
- [ ] Nice-to-haves (features, friction) created as issues
- [ ] Key behavioral discoveries converted to tests
- [ ] Docstring gaps identified and scheduled for update

---

## Success Criteria

Playground exploration succeeds when:

### 1. Runnable ✓
```python
# Can you run it without errors?
$ python playground/processor_exploration.py
[OK] Basic usage works
[OK] Edge cases handled
[OK] Error handling works
[OK] Discoveries recorded
```

### 2. Documented ✓
```python
# Clear comments explain each section
def explore_edge_cases() -> bool:
    """Explore edge cases and boundaries."""
    print_section("2. Edge Cases")

    # Test 1: Empty input
    result = processor.process([])
    print_result(len(result) == 0, "Empty input returns empty")

    # Test 2: Single item
    result = processor.process([1])
    print_result(len(result) == 1, "Single item works")
```

### 3. Discoverable ✓
```python
# Findings are recorded with action items
print("[MISSING] No batch processing API")
print("  Use case: Process 1000 items efficiently")
print("  Current: Loop with do_thing() 1000 times")
print("  Proposed: do_things(items) for batch")
```

### 4. Convertible ✓
```python
# Key scenarios become formal tests
# Playground:
result = processor.process([])
print_result(len(result) == 0, "Empty input works")

# Becomes test:
def test_empty_input():
    assert len(processor.process([])) == 0
```

### 5. Maintained ✓
```python
# Updated when module changes
# Not left to rot

# When API changes:
# - Update playground to match new API
# - Re-run to verify
# - Record changes
```

---

## Workflow Integration

### Phase 0: Discovery (Prepare)

**Before implementing the module:**

1. Create playground file structure:
   ```bash
   mkdir -p playground
   touch playground/{module}_exploration.py
   ```

2. Skeleton exploration file:
   ```python
   #!/usr/bin/env python3
   """Exploration of {module} functionality."""

   def explore_basic_usage() -> bool:
       """Explore primary use case."""
       # TODO: Implement as module develops
       return True

   if __name__ == "__main__":
       sys.exit(0 if explore_basic_usage() else 1)
   ```

3. Research similar modules and existing patterns

---

### Phase 1: Development (Step 5)

**After implementing the module:**

1. Run playground exploration:
   ```bash
   python playground/{module}_exploration.py
   ```

2. Update exploration file with real scenarios (5+ scenarios)

3. Document at least:
   - Basic usage (happy path)
   - Edge cases (boundaries)
   - Error handling (failures)
   - Integration (if applicable)

4. Record discoveries:
   ```python
   # DISCOVERY: Feature X would make usage easier
   # FRICTION: API requires repetitive setup
   # MISSING: No batch processing support
   # UNDOCUMENTED: Behavior when input is None
   ```

5. Convert key findings to action items:
   - Update docstrings (high priority)
   - Fix error messages (high priority)
   - Create feature requests (medium)
   - Plan API improvements (medium)

---

### Phase 2: Refinement (Iteration)

**If feedback suggests improvements:**

1. Re-run playground with new API:
   ```bash
   python playground/{module}_exploration.py
   ```

2. Update exploration file for any API changes

3. Verify fixes work correctly

4. Record new discoveries from refined implementation

5. Update action items based on feedback

---

### Phase 3: Completion (Final)

**When module is ready to release:**

1. Finalize playground code:
   - Clean up any TODOs
   - Ensure all scenarios work
   - Update documentation

2. Convert stable patterns to formal tests:
   ```bash
   # Discoveries → test cases
   # playground/{module}_exploration.py → tests/test_{module}.py
   ```

3. Document findings in module docstrings:
   - Performance characteristics
   - Known limitations
   - Usage examples
   - Error conditions

4. Commit playground code:
   ```bash
   git add playground/{module}_exploration.py
   git commit -m "Add playground exploration for {module}"
   ```

---

## Common Pitfalls

### Pitfall 1: Not Recording Discoveries

```python
# ❌ Bad: Discoveries vanish
# Run playground, think "Oh, that's awkward"
# Don't write it down
# Next day, forgotten

# ✓ Good: Write everything down
print("[FRICTION] API requires X every time")
print("ACTION: Make X automatic with sensible default")
```

**Fix:** Add discovery comments to playground code immediately.

---

### Pitfall 2: Playground Code Drifts from Reality

```python
# ❌ Bad: Outdated playground
# Module API changes
# Playground never updated
# Old exploration no longer runs
# Becomes dead weight

# ✓ Good: Keep playground current
# When API changes:
# 1. Update playground
# 2. Run to verify
# 3. Commit changes
```

**Fix:** When updating module, update playground first.

---

### Pitfall 3: Not Converting to Tests

```python
# ❌ Bad: Discoveries never become tests
# Playground reveals edge cases
# But no test prevents regression
# Same issue appears later

# ✓ Good: Convert key behaviors to tests
# Playground reveals: "Empty input returns empty result"
# Becomes: def test_empty_input(): assert...
```

**Fix:** After each playground session, convert 3-5 behaviors to tests.

---

### Pitfall 4: Waiting Too Long to Explore

```python
# ❌ Bad: Explore only after "complete"
# Implement entire module
# Run playground once
# Already committed to API design
# Hard to fix issues found

# ✓ Good: Explore iteratively
# Implement feature
# Run playground
# Fix issues found
# Iterate until solid
```

**Fix:** Run playground after each feature, not just once at the end.

---

## Tips for Success

1. **Embrace friction** - Every awkward moment is valuable feedback
2. **Document discoveries immediately** - Don't rely on memory
3. **Test edge cases** - Boundaries reveal design issues
4. **Include examples** - Playground is your first documentation
5. **Keep it clean** - Runnable code is an asset
6. **Iterate quickly** - Fix issues while fresh
7. **Share findings** - Other developers learn from discoveries
8. **Maintain playground** - Update when module changes
9. **Convert to tests** - Make discoveries permanent
10. **Enjoy the insights** - You're discovering your own API!

---

## Key Principle

> "Eat your own dog food."

The playground is how you become the **first user** of your own code. Every friction point you feel is a bug report. Every missing feature you want is a feature request. Every confusing behavior is a documentation gap.

By using your own code extensively before others do, you find and fix issues that would otherwise escape to users. This is invaluable quality improvement work.

---

## Summary

| Aspect | Do ✓ | Don't ✗ |
|--------|------|---------|
| **Running** | Run frequently | Skip because "tests exist" |
| **Recording** | Document all discoveries | Ignore friction points |
| **Cleaning** | Keep code runnable | Write non-executable code |
| **Converting** | Make tests from behaviors | Treat as throwaway |
| **Maintaining** | Update with changes | Leave outdated |
| **Sharing** | Document usage examples | Keep findings private |

Playground-driven development is how you become your own best user.
