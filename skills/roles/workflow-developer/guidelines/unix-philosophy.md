# Unix Philosophy for Developers

Apply these principles throughout your development work.

See also: [unix-philosophy skill](../../workflow/python-philosophy/unix-philosophy.md) for comprehensive guide.

---

## 1. Always Check for Existing Packages First

Before writing any significant functionality:

**Search:**
- PyPI (https://pypi.org/)
- GitHub (awesome-lists, popular repositories)
- Your internal package repository

**Evaluate:**
- Maintenance (recent commits, active issues)
- API design (intuitive, well-named)
- Documentation (complete, clear)
- Adoption (popular, production-ready)

**Make Decision:**
- **COMPOSE** - Use package as-is
- **EXTEND** - Wrap or extend package
- **BUILD** - Write your own

**Document:**
- Why you chose this approach
- Why other approaches were rejected
- Key trade-offs

---

## 2. Create llmtxt Documentation for Adopted Packages

When you adopt an external package:

**Create llmtxt file** with:
- What the package does
- Key APIs and usage patterns
- Common gotchas discovered
- Code examples

Store in `docs/llmtxt/` or `.claude/llmtxt/`

This helps others (and future you) quickly understand adopted packages.

---

## 3. Design with Composition in Mind

When implementing (BUILD decision):

**Principles:**
- **Single responsibility** - Each module does one thing well
- **Composable functions** - Accept and return standard types (str, list, dict, etc.)
- **Leverage stdlib** - Use Python standard library before external packages
- **Keep modules small** - Under 400 lines per file
- **Limit parameters** - Functions with < 7 parameters
- **Reuse patterns** - Use existing patterns from codebase

**Example:**
```python
# Good: Focused, reusable
def parse_config(path: Path) -> Config:
    """Parse config from file."""
    data = json.load(path.open())
    return Config.from_dict(data)

# Bad: Mixed concerns
def load_config_and_apply_and_run():
    """Does everything."""
    ...
```

---

## 4. Code Design Checklist

- [ ] Did I search for existing packages?
- [ ] Did I document the build vs compose decision?
- [ ] Did I create llmtxt for adopted packages?
- [ ] Does each module do one thing?
- [ ] Are functions composable (accept/return standard types)?
- [ ] Did I use stdlib where appropriate?
- [ ] Is code following existing patterns?

---

## When Composing Packages

If combining multiple packages:

1. **Plan integration** - How do they work together?
2. **Create wrapper** - If needed, wrap them for consistency
3. **Document interfaces** - How other code will use them
4. **Test composition** - Verify they work well together
5. **Document gotchas** - What to watch for when using together

---

## Remember

> "Use tools in preference to unskilled help to lighten a programming task."

Tools (packages) should make your job easier, not harder. If integration is painful, reconsider the choice.
