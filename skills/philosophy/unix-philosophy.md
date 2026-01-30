---
name: unix-philosophy
description: Unix philosophy principles applied to Python development. Use when designing modules, structuring code, making build-vs-compose decisions, or reviewing architecture. Guides composition, single responsibility, and tool reuse patterns.
---

# Unix Philosophy for Python Development

Core Unix principles adapted for modern Python development: composition over reimplementation, small focused modules, and leveraging existing tools.

## Contents

- [The Original Principles](#the-original-principles)
- [When to Use This Skill](#when-to-use-this-skill)
- [Quick Reference](#quick-reference)
- [Principle 1: Do One Thing Well](#principle-1-do-one-thing-well)
- [Principle 2: Compose via Clear Interfaces](#principle-2-compose-via-clear-interfaces)
- [Principle 3: Expect Standard Types](#principle-3-expect-standard-types)
- [Principle 4: Reuse Existing Tools](#principle-4-reuse-existing-tools)
- [Build vs Compose Decision](#build-vs-compose-decision)
- [Composition Checklist](#composition-checklist)

## The Original Principles

From Doug McIlroy and the Unix pioneers:

1. **Do one thing well** - Write programs that do one thing and do it well
2. **Compose via pipes** - Write programs to work together
3. **Text streams** - Expect output to become input to another program
4. **Reuse existing tools** - Use tools rather than unskilled help

> "This is the Unix philosophy: Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface."

---

## When to Use This Skill

- Designing new modules or packages
- Making build-vs-compose decisions
- Reviewing code architecture
- Refactoring monolithic code
- Evaluating third-party package usage

---

## Quick Reference

```
1. Single Responsibility  -> One module, one purpose
2. Composable Interfaces  -> Functions accept and return standard types
3. Leverage stdlib        -> os, pathlib, subprocess, shutil first
4. Use Existing Packages  -> Don't reinvent solved problems
5. Pipeable Design        -> stdin/stdout patterns where appropriate
6. Text as Interface      -> JSON, CSV, or line-based for interop
```

---

## Principle 1: Do One Thing Well

### Module Design

Each module should have a single, clear purpose:

```python
# Good: Single responsibility
# _validation.py - only validation logic
def validate_email(email: str) -> bool: ...
def validate_phone(phone: str) -> bool: ...
def validate_address(address: Address) -> list[ValidationError]: ...

# _formatting.py - only formatting logic
def format_email(email: str) -> str: ...
def format_phone(phone: str, region: str) -> str: ...
def format_address(address: Address) -> str: ...
```

```python
# Bad: Mixed responsibilities
# utils.py - does everything
def validate_email(email: str) -> bool: ...
def format_email(email: str) -> str: ...
def send_email(to: str, body: str) -> None: ...  # I/O mixed with validation
def parse_email_config(path: str) -> dict: ...   # Config mixed with email
```

### Function Design

Each function should do one thing:

```python
# Good: Single operation
def load_config(path: Path) -> Config:
    """Load configuration from file."""
    ...

def validate_config(config: Config) -> list[ConfigError]:
    """Validate configuration values."""
    ...

def apply_config(config: Config) -> None:
    """Apply configuration to system."""
    ...

# Usage: Compose as needed
config = load_config(path)
errors = validate_config(config)
if not errors:
    apply_config(config)
```

```python
# Bad: Multiple operations bundled
def load_and_validate_and_apply_config(path: Path) -> None:
    """Load, validate, and apply config (all or nothing)."""
    # Can't load without validating
    # Can't validate without applying
    # Can't test pieces independently
    ...
```

---

## Principle 2: Compose via Interfaces

### Composable Function Design

Functions should accept and return standard types:

```python
# Good: Composable - accepts iterable, returns list
def filter_active(items: Iterable[Item]) -> list[Item]:
    return [item for item in items if item.is_active]

def sort_by_date(items: Iterable[Item]) -> list[Item]:
    return sorted(items, key=lambda x: x.created_at)

def take_recent(items: Iterable[Item], n: int) -> list[Item]:
    return list(items)[:n]

# Compose freely
result = take_recent(sort_by_date(filter_active(all_items)), 10)

# Or with pipe-style (Python 3.12+)
from functools import reduce
result = reduce(lambda x, f: f(x), [
    filter_active,
    sort_by_date,
    lambda x: take_recent(x, 10),
], all_items)
```

```python
# Bad: Non-composable - mutates, uses custom types everywhere
class ItemProcessor:
    def __init__(self, items: list[Item]):
        self.items = items  # Holds state

    def filter_active(self) -> "ItemProcessor":
        self.items = [i for i in self.items if i.is_active]
        return self  # Returns self, not data

    def get_items(self) -> list[Item]:
        return self.items
```

### Generator Pipelines

Use generators for memory-efficient composition:

```python
def read_lines(path: Path) -> Iterator[str]:
    """Yield lines from file."""
    with open(path) as f:
        for line in f:
            yield line.strip()

def parse_records(lines: Iterable[str]) -> Iterator[Record]:
    """Parse lines into records."""
    for line in lines:
        yield Record.from_line(line)

def filter_valid(records: Iterable[Record]) -> Iterator[Record]:
    """Yield only valid records."""
    for record in records:
        if record.is_valid:
            yield record

# Compose: Memory efficient, processes one at a time
valid_records = filter_valid(parse_records(read_lines(path)))
```

---

## Principle 3: Leverage the Standard Library

### Before Writing, Check stdlib

| Need | stdlib Module | Don't Reinvent |
|------|---------------|----------------|
| File paths | `pathlib` | String manipulation |
| File operations | `shutil` | Manual copy/move |
| JSON handling | `json` | Custom parsing |
| CSV handling | `csv` | Manual splitting |
| Dates/times | `datetime` | Custom parsing |
| Temp files | `tempfile` | Manual cleanup |
| Subprocesses | `subprocess` | os.system() |
| URL parsing | `urllib.parse` | Regex on URLs |
| Config files | `configparser` | Manual INI parsing |
| CLI args | `argparse` | Manual sys.argv |
| Async I/O | `asyncio` | Threading for I/O |
| Data classes | `dataclasses` | Manual __init__ |
| Enums | `enum` | String constants |
| Type hints | `typing` | Docstring types |

### stdlib Patterns

```python
# File operations with pathlib + shutil
from pathlib import Path
import shutil

def backup_config(src: Path, backup_dir: Path) -> Path:
    """Backup configuration file with timestamp."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = backup_dir / f"{src.stem}_{timestamp}{src.suffix}"
    shutil.copy2(src, dest)
    return dest
```

```python
# Subprocess with proper error handling
import subprocess

def run_git_command(args: list[str], cwd: Path) -> str:
    """Run git command and return output."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,  # Raises on non-zero exit
    )
    return result.stdout.strip()
```

```python
# Temporary files with automatic cleanup
import tempfile
from contextlib import contextmanager

@contextmanager
def temp_config(content: str) -> Iterator[Path]:
    """Create temporary config file, cleanup on exit."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".yaml",
        delete=False
    ) as f:
        f.write(content)
        temp_path = Path(f.name)
    try:
        yield temp_path
    finally:
        temp_path.unlink(missing_ok=True)
```

---

## Principle 4: Use Existing Tools

### Package Research First

Before implementing, always check:

1. **stdlib** - Is it in the standard library?
2. **PyPI** - Is there a well-maintained package?
3. **Awesome lists** - What do experts recommend?

See: `package-research` skill for systematic evaluation.

### Common Replacements

| Instead of Writing | Use Package |
|--------------------|-------------|
| HTTP client | `httpx` or `requests` |
| Rate limiting | `limits` or `tenacity` |
| Retries | `tenacity` |
| Validation | `pydantic` |
| CLI framework | `click` or `typer` |
| Config management | `pydantic-settings` |
| Date handling | `pendulum` |
| Async utilities | `anyio` |
| Testing utilities | `pytest` + plugins |
| Logging structure | `structlog` |

### When to Build vs Compose

**COMPOSE** when:
- Well-maintained package exists
- Saves significant implementation time
- Provides battle-tested edge case handling
- Has active community/support

**BUILD** when:
- No suitable package exists
- Package would be heavier than custom solution
- Unique requirements not met
- Security concerns with dependencies

---

## Principle 5: Text Streams as Interface

### CLI Input/Output Patterns

Design CLIs that work with pipes:

```python
import click
import sys

@click.command()
@click.argument("input", type=click.File("r"), default="-")
@click.argument("output", type=click.File("w"), default="-")
def process(input, output):
    """Process records from INPUT to OUTPUT.

    Use '-' for stdin/stdout (default).
    """
    for line in input:
        record = parse_record(line)
        if record.is_valid:
            output.write(format_record(record) + "\n")

# Works with pipes:
# cat data.txt | python process.py | grep "ERROR"
# python process.py input.txt output.txt
```

### JSON Lines for Streaming

Use JSON Lines (`.jsonl`) for streaming structured data:

```python
import json
from typing import Iterator

def read_jsonl(path: Path) -> Iterator[dict]:
    """Read JSON Lines file, yielding parsed objects."""
    with open(path) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def write_jsonl(records: Iterable[dict], path: Path) -> None:
    """Write records as JSON Lines."""
    with open(path, "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

# Composable with shell tools:
# cat records.jsonl | jq '.status' | sort | uniq -c
```

### Structured Output

For programmatic consumption, output structured data:

```python
@click.command()
@click.option("--format", type=click.Choice(["json", "table", "csv"]), default="table")
def list_items(format: str):
    """List items in specified format."""
    items = fetch_items()

    if format == "json":
        click.echo(json.dumps([asdict(i) for i in items], indent=2))
    elif format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=["id", "name", "status"])
        writer.writeheader()
        for item in items:
            writer.writerow(asdict(item))
    else:
        for item in items:
            click.echo(f"{item.id}\t{item.name}\t{item.status}")
```

---

## Principle 6: Small, Focused Programs

### Module Size Guidelines

| Metric | Target | Maximum |
|--------|--------|---------|
| Lines per module | < 200 | 400 |
| Functions per module | < 10 | 15 |
| Classes per module | < 3 | 5 |
| Parameters per function | < 5 | 7 |
| Cyclomatic complexity | < 5 | 10 |

### Splitting Large Modules

When a module grows too large, split by responsibility:

```
# Before: monolithic
scheduler.py (800 lines)
  - Task class
  - Queue class
  - Worker class
  - Scheduler class
  - CLI commands
  - Config handling

# After: focused modules
scheduler/
├── __init__.py      # Public API only
├── _types.py        # Task, ScheduledTask dataclasses
├── _queue.py        # Queue implementation
├── _worker.py       # Worker implementation
├── _scheduler.py    # Scheduler orchestration
├── _cli.py          # CLI commands
└── _config.py       # Configuration
```

---

## Python-Specific Patterns

### Context Managers for Resources

```python
from contextlib import contextmanager

@contextmanager
def database_transaction(conn: Connection) -> Iterator[Cursor]:
    """Execute operations in a transaction."""
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()

# Composable with other context managers
with database_transaction(conn) as cursor:
    with temp_config(config_content) as config_path:
        cursor.execute(...)
```

### Decorators for Cross-Cutting Concerns

```python
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator - separates retry logic from business logic."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except RetryableError as e:
                    last_error = e
                    time.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator

# Clean separation
@retry(max_attempts=3)
def fetch_data(url: str) -> dict:
    """Fetch data - no retry logic here."""
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()
```

### Protocols for Duck Typing

```python
from typing import Protocol

class Serializable(Protocol):
    """Any object that can be serialized to dict."""
    def to_dict(self) -> dict: ...

class Persistable(Protocol):
    """Any object that can be saved and loaded."""
    def save(self, path: Path) -> None: ...
    @classmethod
    def load(cls, path: Path) -> "Persistable": ...

# Functions accept protocols, not concrete types
def export_all(items: Iterable[Serializable], path: Path) -> None:
    """Export any serializable items - doesn't care about concrete type."""
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item.to_dict()) + "\n")
```

---

## Applying to the Workflow

### Phase 0: Discovery

- **Step 0.2: Package Research** - Search before building
- Evaluate build-vs-compose decision
- Document rationale

### Phase 1: Implementation

- Design modules with single responsibility
- Use composable interfaces
- Leverage stdlib and packages
- Keep modules small and focused

### Code Review Checklist

- [ ] Does each module do one thing?
- [ ] Are functions composable (standard input/output types)?
- [ ] Is stdlib used where appropriate?
- [ ] Were existing packages considered?
- [ ] Is the module under 400 lines?
- [ ] Do functions have < 7 parameters?

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| God module | 1000+ lines, does everything | Split by responsibility |
| NIH syndrome | Rewriting solved problems | Research packages first |
| Deep inheritance | Tight coupling, hard to compose | Composition + protocols |
| Global state | Non-composable, hard to test | Explicit dependencies |
| Mixed I/O and logic | Can't compose, hard to test | Separate pure and impure |
| Custom formats | Not interoperable | JSON, CSV, or line-based |

---

## Summary

1. **One thing well** - Small, focused modules and functions
2. **Compose** - Standard types in, standard types out
3. **stdlib first** - Know what's built-in before reaching for packages
4. **Reuse packages** - Research before reimplementing
5. **Text interface** - JSON/CSV/lines for interop
6. **Stay small** - Under 400 lines, under 7 parameters

> "The power of Unix comes not from individual programs, but from how they combine."

---

## References

- `package-research` skill - Systematic package evaluation
- `llmtxt` skill - Documenting packages for AI assistants
- `python-coding-standards` skill - Python code patterns
- "The Art of Unix Programming" by Eric S. Raymond
