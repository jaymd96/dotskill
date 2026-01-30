---
name: literate-python
description: Write Python code using literate programming style with Litterate-compatible annotations. Use when writing Python code that should include meaningful documentation annotations, creating code intended for human understanding, or when the user requests literate programming style. Annotations start with hash-greater-than and explain WHY and provide context—never repeat WHAT the code does.
---

# Literate Python Programming

Write Python code with `#>` annotation blocks for Litterate documentation generation.

## Annotation Syntax

```python
#> Annotation starts with #> marker
#  Continuation lines use plain # (with space)
#  Supports **Markdown**: *emphasis*, `code`, links
```

## Core Principle: Add Value, Not Noise

Annotations explain **why** and provide **context**—they never repeat what code already says.

**Never annotate:**
- What a variable does when the name is self-explanatory
- Loop mechanics (`iterating over items`)
- Basic operations (`adding x to y`)
- Standard patterns (`initializing empty list`)

**Always annotate:**
- Domain knowledge not obvious from code
- Design decisions and tradeoffs
- Edge cases and their rationale
- Performance considerations
- Business logic context
- Mathematical/algorithmic insights

## Examples

### Bad: Redundant Annotation

```python
#> Loop through each user and check if they are active
for user in users:
    if user.is_active:
        active_users.append(user)
```

### Good: Contextual Annotation

```python
#> Active users include those with activity in the last 90 days,
#  excluding accounts flagged for review—per GDPR compliance
#  requirements documented in SEC-2024-01.
for user in users:
    if user.is_active:
        active_users.append(user)
```

### Bad: Explaining Obvious Code

```python
#> Calculate the average by summing all values and dividing by count
average = sum(values) / len(values)
```

### Good: Explaining Why This Approach

```python
#> Using arithmetic mean rather than median here because outliers
#  represent valid high-value transactions we want to weight.
average = sum(values) / len(values)
```

## Annotation Placement

Place annotations **before** the code block they describe:

```python
#> Retry logic uses exponential backoff to avoid thundering herd
#  when the payment gateway recovers from downtime.
for attempt in range(max_retries):
    delay = base_delay * (2 ** attempt)
    try:
        return process_payment(order)
    except GatewayTimeout:
        time.sleep(delay)
```

## When to Use Annotations

| Scenario | Annotate? | Reason |
|----------|-----------|--------|
| Complex algorithm | Yes | Explain the approach |
| Business rule | Yes | Document the requirement |
| Performance optimization | Yes | Explain the tradeoff |
| Standard library call | No | Well-documented elsewhere |
| Variable assignment | No | Name should be clear |
| Import statements | No | Obvious purpose |

## Multi-Block Annotations

For complex sections, use annotations to narrate the flow:

```python
#> **Phase 1: Data Validation**
#  Incoming records may have missing fields from legacy systems
#  migrated before 2019. We default missing values rather than
#  rejecting records to preserve historical data continuity.
validated = [normalize_record(r) for r in raw_records]

#> **Phase 2: Deduplication**
#  Records are keyed by (customer_id, transaction_date) because
#  the same customer can have multiple transactions per day,
#  but duplicate submissions from retry logic are common.
unique_records = deduplicate(validated, key=dedup_key)
```

## Configuration Reference

For Python files, configure Litterate with:

```javascript
// litterate.config.js
module.exports = {
    annotationStartMark: '#>',
    annotationContinueMark: '#',
    files: ['src/**/*.py'],
}
```

## Quick Reference

- Start annotation: `#>` (with space after)
- Continue annotation: `#` followed by space
- Markdown supported: **bold**, *italic*, `code`, [links]()
- Empty `#` line creates paragraph break in annotation
- Regular `# comments` without `>` are ignored by Litterate
