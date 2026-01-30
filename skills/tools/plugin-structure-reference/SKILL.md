---
name: plugin-structure-reference
description: Reference guide for Claude Code plugin directory structure and organization. Use when creating new Claude Code plugins, debugging plugin installation issues, or understanding how plugins should be structured.
---

# Claude Code Plugin Structure Reference

Complete reference for creating properly structured Claude Code plugins that follow official patterns.

## Core Rule: The One Critical Principle

**ONLY `plugin.json` goes inside `.claude-plugin/`. Everything else goes at the plugin root.**

## Correct Directory Structure

```
my-plugin/                          ← Plugin root
├── .claude-plugin/                 ← ONLY manifests here
│   ├── plugin.json                 ← Plugin metadata (REQUIRED)
│   └── marketplace.json            ← Marketplace entry (OPTIONAL)
│
├── skills/                         ← Skills at plugin ROOT
│   ├── skill-one/
│   │   ├── SKILL.md                ← Main skill file
│   │   ├── references/             ← Optional reference docs
│   │   │   ├── patterns.md
│   │   │   └── examples.md
│   │   ├── examples/               ← Optional working code
│   │   │   └── sample.py
│   │   └── scripts/                ← Optional utility scripts
│   │       └── validate.sh
│   └── skill-two/
│       └── SKILL.md
│
├── commands/                       ← Commands at plugin root (OPTIONAL)
│   └── my-command.md
│
├── agents/                         ← Agents at plugin root (OPTIONAL)
│   └── my-agent.md
│
├── hooks/                          ← Hooks at plugin root (OPTIONAL)
│   └── hooks.json
│
├── .mcp.json                       ← MCP config at plugin root (OPTIONAL)
├── .lsp.json                       ← LSP config at plugin root (OPTIONAL)
│
├── README.md                       ← Plugin documentation
├── LICENSE                         ← License file
└── CHANGELOG.md                    ← Version history
```

## Minimal Required Structure

The absolute minimum to create a working plugin:

```
minimal-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

## plugin.json - Minimal Required Format

```json
{
  "name": "unique-plugin-name",
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

### Valid plugin.json Fields

| Field | Required | Type | Purpose |
|-------|----------|------|---------|
| `name` | YES | string | Unique identifier (kebab-case) |
| `description` | YES | string | Brief description |
| `version` | YES | string | Semantic version (1.0.0) |
| `author.name` | NO | string | Creator attribution |
| `author.email` | NO | string | Contact email |
| `homepage` | NO | string | Documentation URL |
| `repository` | NO | string | GitHub/Git URL |
| `license` | NO | string | License (Apache-2.0, MIT, etc.) |
| `keywords` | NO | array | Search tags |

### INVALID Fields (Will Cause Errors)

❌ DON'T include these in plugin.json:
- `category` - Invalid field
- `templates` - Invalid field
- `skills` - Auto-discovered, don't list
- `commands` - Auto-discovered, don't list
- `agents` - Auto-discovered, don't list

## SKILL.md Format

Every skill MUST have a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-identifier-kebab-case
description: When to use this skill. Clear, specific trigger phrases.
disable-model-invocation: true  # OPTIONAL: Prevent auto-invocation
---

# Skill Title

[Skill instructions and guidance...]
```

### Required Frontmatter Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | YES | Skill identifier (kebab-case) |
| `description` | YES | When/why to use skill (1-2 sentences) |
| `disable-model-invocation` | NO | Set `true` to prevent Claude auto-invocation |

## Organizing Skills by Category

For clarity with many skills, use category folders:

```
skills/
├── foundations/              ← Category
│   ├── python-testing/
│   │   └── SKILL.md
│   ├── python-coding/
│   │   └── SKILL.md
│   └── python-layout/
│       └── SKILL.md
├── roles/                    ← Category
│   ├── manager/
│   │   └── SKILL.md
│   ├── developer/
│   │   └── SKILL.md
│   └── reviewer/
│       └── SKILL.md
└── philosophy/               ← Category
    ├── unix-philosophy/
    │   └── SKILL.md
    └── package-research/
        └── SKILL.md
```

Claude Code auto-discovers all SKILL.md files regardless of nesting depth.

## Common Mistakes to Avoid

### ❌ Mistake 1: Putting components inside .claude-plugin/

**WRONG:**
```
.claude-plugin/
├── plugin.json       ✓
├── skills/           ✗ DON'T!
├── commands/         ✗ DON'T!
└── agents/           ✗ DON'T!
```

**RIGHT:**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json   ✓
├── skills/           ✓ At plugin root
├── commands/         ✓ At plugin root
└── agents/           ✓ At plugin root
```

### ❌ Mistake 2: Missing SKILL.md frontmatter

**WRONG:**
```markdown
# My Skill
Instructions without frontmatter...
```

**RIGHT:**
```yaml
---
name: my-skill
description: Use when...
---

# My Skill
Instructions with frontmatter...
```

### ❌ Mistake 3: Using skills directory as a lone file

**WRONG:**
```
skills/
└── my-skill.md       ← Won't work
```

**RIGHT:**
```
skills/
└── my-skill/
    └── SKILL.md      ← Proper structure
```

### ❌ Mistake 4: Invalid fields in plugin.json

**WRONG:**
```json
{
  "name": "plugin",
  "skills": ["python-testing"],    ← Auto-discovered, don't list
  "category": "development"        ← Invalid field
}
```

**RIGHT:**
```json
{
  "name": "plugin",
  "description": "...",
  "version": "1.0.0"
}
```

### ❌ Mistake 5: Using camelCase or underscores for identifiers

**WRONG:**
- `pythonTesting` (camelCase)
- `python_testing` (snake_case)

**RIGHT:**
- `python-testing` (kebab-case)

## Skill Invocation

### How users invoke skills

Skills are accessed with the plugin namespace:

```
/plugin-name:skill-identifier
```

**Example:**
```
/jaymd96:python-testing
/jaymd96:workflow-manager
/jaymd96:package-research
```

### Auto-discovery behavior

Claude Code automatically discovers:
- All folders in `skills/` containing `SKILL.md` → become skills
- All `.md` files in `commands/` → become commands
- All `.md` files in `agents/` → become agents
- `hooks/hooks.json` → hook configuration
- `plugin.json` in `.claude-plugin/` → plugin metadata

**You don't need to list them in plugin.json** - they're auto-discovered!

## Real Working Examples

### From anthropics/claude-code repository:

**plugin-dev plugin:**
- Skills: 7 (hook-development, mcp-integration, plugin-structure, etc.)
- Each skill has: SKILL.md, references/, examples/, scripts/
- Auto-discovered from `skills/` at plugin root

**code-review plugin:**
- Commands: `/code-review` with 4 parallel review agents
- Minimal structure: `.claude-plugin/plugin.json`, `commands/`

## marketplace.json for Distribution

When publishing to a marketplace:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "my-plugin-marketplace",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./",
      "description": "Plugin description",
      "version": "1.0.0",
      "author": { "name": "Your Name" }
    }
  ]
}
```

**Required fields:**
- `name` - Marketplace plugin identifier
- `source` - Where to fetch the plugin from
- `description` - Brief plugin description

## Summary: The 7 Essential Rules

1. **Only `plugin.json` in `.claude-plugin/`** - Everything else at plugin root
2. **Skills in `skills/SKILL-NAME/SKILL.md`** - One folder per skill
3. **Use kebab-case for identifiers** - `python-testing`, not `pythonTesting`
4. **Include frontmatter in SKILL.md** - `name` and `description` required
5. **No invalid fields in plugin.json** - No `skills`, `commands`, `category` fields
6. **Organize skills logically** - Use category folders for clarity (optional)
7. **Let auto-discovery work** - Don't manually list components

See [references/](references/) for detailed documentation and working examples.
