# Eyeball Command Reference

Complete reference for all eyeball commands.

---

## Global Options

```bash
eyeball [--pretty/-p] <command> [options]
```

| Option | Description |
|--------|-------------|
| `--pretty`, `-p` | Pretty-print JSON output (use when reading manually) |

---

## Discovery Commands

### `discover`

List all public classes and functions in a module.

```bash
eyeball discover <module>
```

**Examples:**
```bash
eyeball discover mypackage.models
eyeball discover requests
eyeball -p discover pandas.core.frame
```

**Output:**
```json
{
  "status": "success",
  "module_name": "mypackage.models",
  "items": [
    {"path": "mypackage.models:User", "name": "User", "type": "class", "local": true},
    {"path": "mypackage.models:validate", "name": "validate", "type": "function", "local": true}
  ],
  "total": 5,
  "local": 3
}
```

### `inspect`

Get detailed information about a module, class, or function.

```bash
eyeball inspect <target>
```

**Target formats:**
- Module: `mypackage.models`
- Class: `mypackage.models:User`
- Method: `mypackage.models:User.validate`
- Function: `mypackage.utils:process`

**Examples:**
```bash
eyeball -p inspect mypackage.models:User
eyeball inspect requests:Session.get
```

**Output (class):**
```json
{
  "status": "success",
  "type": "class",
  "class_name": "User",
  "init_signature": "(name: str, email: str, age: int = 0)",
  "attributes": [
    {"name": "name", "type": "str", "required": true},
    {"name": "email", "type": "str", "required": true}
  ],
  "methods": [
    {"name": "validate", "signature": "()", "defined_in": "User"}
  ],
  "docstring": "A user in the system."
}
```

### `source`

Show source code of a target.

```bash
eyeball source <target>
```

**Examples:**
```bash
eyeball source mypackage.models:User
eyeball source mypackage.utils:process
```

**Output:**
```json
{
  "status": "success",
  "file_path": "/path/to/models.py",
  "start_line": 10,
  "end_line": 45,
  "source": "class User:\n    ..."
}
```

---

## API Documentation Commands

### `api`

Get comprehensive API documentation for any target. Works on third-party libraries.

```bash
eyeball api <target> [--source/--no-source] [--source-lines N]
```

**Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `--source/--no-source` | `--source` | Include source code preview |
| `--source-lines`, `-n` | 50 | Number of source lines |

**Examples:**
```bash
eyeball -p api requests:get
eyeball api pandas:DataFrame.merge --source-lines 30
eyeball api pydantic:BaseModel --no-source
```

**Output:**
```json
{
  "status": "success",
  "type": "function",
  "name": "get",
  "signature": "(url, params=None, **kwargs)",
  "parameters": [
    {"name": "url", "required": true, "description": "URL for the request."},
    {"name": "params", "required": false, "default": "None", "description": "Query parameters."}
  ],
  "return_type": "Response",
  "summary": "Sends a GET request.",
  "examples": [
    {"code": "requests.get('https://api.example.com')"}
  ],
  "source_available": true,
  "source_preview": "def get(url, params=None, **kwargs):..."
}
```

### `search-api`

Search for items in a module by name.

```bash
eyeball search-api <module> <query>
```

**Examples:**
```bash
eyeball search-api requests get
eyeball search-api pandas merge
eyeball search-api sqlalchemy session
```

**Output:**
```json
{
  "status": "success",
  "module": "requests",
  "query": "get",
  "results": [
    {"name": "get", "type": "function", "signature": "(url, params=None, **kwargs)", "summary": "Sends a GET request."}
  ],
  "total": 1
}
```

---

## Execution Commands

### `run`

Execute a function or instantiate a class.

```bash
eyeball run <target> [--args JSON] [--kwargs JSON]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--args`, `-a` | JSON array of positional arguments |
| `--kwargs`, `-k` | JSON object of keyword arguments |

**Examples:**
```bash
eyeball run mypackage.utils:add --args '[1, 2]'
eyeball run mypackage.models:User --kwargs '{"name": "Alice", "email": "alice@example.com"}'
eyeball -p run mypackage.services:process --kwargs '{"data": [1,2,3]}'
```

**Output:**
```json
{
  "status": "success",
  "result": {"name": "Alice", "email": "alice@example.com"},
  "result_type": "User",
  "stdout": null
}
```

### `exec`

Execute arbitrary Python code.

```bash
eyeball exec '<code>'
```

**Examples:**
```bash
eyeball exec 'print(1 + 1)'
eyeball exec 'from mypackage import VERSION; print(VERSION)'
eyeball exec 'import sys; print(sys.version)'
```

**Output:**
```json
{
  "status": "success",
  "result": null,
  "stdout": "2\n"
}
```

### `probe`

Run quick verification probes with assertions.

```bash
eyeball probe '<code>' [--setup CODE] [--fixture NAME] [--patch SPEC] [--timeout SEC]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--setup`, `-s` | Setup code to run before probe |
| `--fixture`, `-f` | Fixture to load (repeatable) |
| `--patch`, `-P` | Patch spec: `module.attr=value` (repeatable) |
| `--timeout`, `-t` | Execution timeout in seconds (default: 30) |

**Examples:**
```bash
# Simple assertion
eyeball probe "assert 1 + 1 == 2"

# Test implementation
eyeball probe "from mypackage import func; assert func(5) == 25"

# With setup
eyeball probe --setup "from mypackage import db; db.connect()" "assert db.is_connected()"

# With fixture
eyeball probe --fixture mocks "assert Mock is not None"

# With patch
eyeball probe --patch "mypackage.config.DEBUG=True" "from mypackage.config import DEBUG; assert DEBUG"

# Multiple checks with labels
eyeball probe "
# @check: addition works
assert 1 + 1 == 2
# @check: subtraction works
assert 5 - 3 == 2
"
```

**Output (success):**
```json
{
  "status": "success",
  "checks": [
    {"name": "probe", "passed": true, "line": 1}
  ],
  "summary": {"total": 1, "passed": 1, "failed": 0}
}
```

**Output (failure):**
```json
{
  "status": "failed",
  "checks": [
    {"name": "probe", "passed": false, "error": "assert 20 == 25", "error_type": "AssertionError", "line": 1}
  ],
  "summary": {"total": 1, "passed": 0, "failed": 1}
}
```

---

## Dependency Analysis Commands

### `deps`

Analyze dependencies of a function, method, or class.

```bash
eyeball deps <target>
```

**Examples:**
```bash
eyeball -p deps mypackage.models:User
eyeball deps mypackage.services:OrderProcessor.process
```

**Output:**
```json
{
  "status": "success",
  "target": "mypackage.models:User",
  "target_type": "class",
  "imports": [
    {"module": "dataclasses", "name": "dataclass"},
    {"module": "typing", "name": "Optional"}
  ],
  "calls": [
    {"name": "field", "is_method": false, "args_count": 0, "kwargs_count": 1}
  ],
  "instantiations": [
    {"name": "ValidationError", "is_method": false}
  ],
  "summary": {
    "imports": 3,
    "calls": 5,
    "instantiations": 2
  }
}
```

### `callers`

Find all references to a target (reverse dependency analysis).

```bash
eyeball callers <target>
```

**Examples:**
```bash
eyeball -p callers mypackage.models:User
eyeball callers mypackage.utils:validate
```

**Output:**
```json
{
  "status": "success",
  "target": "mypackage.models:User",
  "callers": [
    {
      "file": "mypackage/services/user_service.py",
      "references": [
        {"type": "import_from", "line": 3, "text": "from mypackage.models import User"},
        {"type": "name", "line": 15, "context": "load"}
      ]
    }
  ],
  "total_files": 3,
  "total_references": 8
}
```

### `module-deps`

Analyze all imports in a module.

```bash
eyeball module-deps <module>
```

**Examples:**
```bash
eyeball -p module-deps mypackage.models
eyeball module-deps mypackage.services
```

**Output:**
```json
{
  "status": "success",
  "target": "mypackage.models",
  "imports": {
    "stdlib": [
      {"type": "from", "module": "dataclasses", "name": "dataclass"}
    ],
    "third_party": [
      {"type": "from", "module": "pydantic", "name": "BaseModel"}
    ],
    "local": [
      {"type": "from", "module": "mypackage.utils", "name": "validate"}
    ]
  },
  "summary": {
    "total": 5,
    "stdlib": 2,
    "third_party": 1,
    "local": 2
  }
}
```

---

## Testing Commands

### `test`

Run pytest for a target with structured output.

```bash
eyeball test <target> [options]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--discover`, `-d` | List tests without running |
| `--verbose`, `-v` | Include full stdout/stderr |
| `--filter`, `-k` | Pytest -k filter expression |
| `--markers`, `-m` | Pytest markers to filter |
| `--coverage` | Include coverage report |
| `--failed`, `-f` | Run only previously failed |
| `--timeout`, `-t` | Timeout in seconds (default: 300) |

**Examples:**
```bash
# Run all tests for a module
eyeball test mypackage.models

# Discover tests
eyeball test mypackage.models --discover

# Filtered tests
eyeball test mypackage.models -k "validation"

# With coverage
eyeball test mypackage.models --coverage

# Verbose output
eyeball test mypackage.models -v
```

**Output:**
```json
{
  "status": "success",
  "target": "mypackage.models",
  "test_files": ["tests/test_models.py"],
  "summary": {
    "total": 15,
    "passed": 15,
    "failed": 0,
    "skipped": 0,
    "duration_seconds": 1.23
  },
  "passed": [...],
  "failed": []
}
```

### `list-tests`

List all test files in the project.

```bash
eyeball list-tests [--pattern PATTERN]
```

**Examples:**
```bash
eyeball list-tests
eyeball list-tests --pattern auth
```

---

## Utility Commands

### `reload`

Reload a module after making changes (hot-reload).

```bash
eyeball reload <module>
```

**Examples:**
```bash
eyeball reload mypackage.models
```

### `fixtures`

List available fixtures for probes.

```bash
eyeball fixtures
```

**Output:**
```json
{
  "status": "success",
  "fixtures": [
    {"name": "mocks", "description": "Common mocking utilities.", "provides": ["Mock", "MagicMock", "patch"]},
    {"name": "async_helpers", "description": "Async testing utilities.", "provides": ["asyncio", "run_async"]},
    {"name": "temp_files", "description": "Temporary file utilities.", "provides": ["temp_dir", "temp_file", "Path"]}
  ],
  "total": 3
}
```

### `help-json`

Output help information as JSON.

```bash
eyeball help-json
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Failure (test failed, assertion failed, error) |
| 2 | Error (could not execute) |
