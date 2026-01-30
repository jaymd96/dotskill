# Complete Plugin Structure Blueprint

Detailed reference showing the complete, correct structure with all optional components.

## Full Plugin Structure with All Components

```
enterprise-plugin/
├── .claude-plugin/                           ← ONLY manifests
│   ├── plugin.json                           ← Plugin metadata (REQUIRED)
│   └── marketplace.json                      ← Marketplace entry (OPTIONAL)
│
├── skills/                                   ← Skills at plugin root
│   ├── README.md                             ← Overview of all skills
│   │
│   ├── foundations/                          ← Category (optional grouping)
│   │   ├── README.md
│   │   ├── python-coding/
│   │   │   ├── SKILL.md                      ← Main skill file
│   │   │   ├── references/                   ← Detailed reference docs
│   │   │   │   ├── patterns.md
│   │   │   │   ├── examples.md
│   │   │   │   └── best-practices.md
│   │   │   ├── examples/                     ← Working code examples
│   │   │   │   └── sample.py
│   │   │   └── scripts/                      ← Utility scripts
│   │   │       └── validate.py
│   │   │
│   │   ├── python-testing/
│   │   │   ├── SKILL.md
│   │   │   ├── references/
│   │   │   │   └── testing-patterns.md
│   │   │   └── examples/
│   │   │       └── test-examples.py
│   │   │
│   │   └── python-layout/
│   │       ├── SKILL.md
│   │       └── references/
│   │           ├── layouts.md
│   │           ├── patterns.md
│   │           └── imports.md
│   │
│   ├── workflow/                             ← Another category
│   │   ├── README.md
│   │   ├── gitops/
│   │   │   ├── SKILL.md
│   │   │   └── references/
│   │   │       ├── conventional-commits.md
│   │   │       ├── branch-strategy.md
│   │   │       └── pull-requests.md
│   │   │
│   │   └── orchestration/
│   │       ├── SKILL.md
│   │       ├── examples/
│   │       │   └── workflow-example.md
│   │       └── references/
│   │           └── patterns.md
│   │
│   └── roles/                                ← Manager-Doer pattern example
│       ├── README.md
│       ├── manager/
│       │   └── SKILL.md
│       ├── developer/
│       │   ├── SKILL.md
│       │   ├── references/
│       │   │   └── implementation-guide.md
│       │   └── examples/
│       │       └── phase-workflow.md
│       └── reviewer/
│           └── SKILL.md
│
├── commands/                                 ← Commands (OPTIONAL)
│   ├── deploy.md
│   ├── review.md
│   ├── test.md
│   └── README.md
│
├── agents/                                   ← Agents (OPTIONAL)
│   ├── code-reviewer.md
│   ├── architect.md
│   ├── tester.md
│   └── README.md
│
├── hooks/                                    ← Hooks (OPTIONAL)
│   └── hooks.json
│
├── .mcp.json                                 ← MCP servers (OPTIONAL)
│
├── .lsp.json                                 ← LSP servers (OPTIONAL)
│
├── README.md                                 ← Plugin documentation
│
├── LICENSE                                   ← License file
│
├── CHANGELOG.md                              ← Version history
│
└── docs/                                     ← Additional docs (OPTIONAL)
    ├── design.md
    ├── architecture.md
    └── troubleshooting.md
```

## Component Descriptions

### .claude-plugin/

**Location:** Plugin root
**Required:** YES
**Contents:**
- `plugin.json` - Plugin metadata (REQUIRED)
- `marketplace.json` - Marketplace entry (OPTIONAL)

**Rule:** ONLY manifest files go here. No skills, commands, agents, or other components.

### skills/

**Location:** Plugin root
**Required:** NO (but recommended if plugin provides knowledge/guidance)
**Structure:**
```
skills/
├── category-one/        ← Optional categorization
│   └── skill-name/
│       └── SKILL.md
└── category-two/
    └── skill-name/
        └── SKILL.md
```

**Auto-discovery:** All folders containing `SKILL.md` become accessible as `/plugin-name:skill-name`

### commands/

**Location:** Plugin root
**Required:** NO (only if plugin needs user-initiated commands)
**Structure:**
```
commands/
├── command-one.md       ← Creates /command-one
├── command-two.md       ← Creates /command-two
└── README.md
```

**Note:** Skills can also act as commands via frontmatter.

### agents/

**Location:** Plugin root
**Required:** NO (only if plugin needs autonomous agents)
**Structure:**
```
agents/
├── code-reviewer.md     ← Specialized code review agent
├── architect.md         ← Architecture planning agent
└── README.md
```

### hooks/

**Location:** Plugin root
**Required:** NO (only if plugin needs event handlers)
**Structure:**
```
hooks/
└── hooks.json          ← Hook configuration
```

**Events supported:**
- PreToolUse - Before Claude uses a tool
- PostToolUse - After successful tool use
- SessionStart - At session beginning
- UserPromptSubmit - When user submits prompt

### .mcp.json

**Location:** Plugin root
**Required:** NO (only for external tool integration)
**Purpose:** Configure Model Context Protocol servers

Example:
```json
{
  "mcpServers": {
    "database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

### .lsp.json

**Location:** Plugin root
**Required:** NO (only for language server integration)
**Purpose:** Configure Language Server Protocol servers

Example:
```json
{
  "python": {
    "command": "pyright",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python"
    }
  }
}
```

## SKILL.md File Format

Every skill MUST have this structure:

```yaml
---
name: skill-identifier-kebab-case
description: When to use this skill. For example: "Use when implementing Python functions, writing unit tests, or designing API endpoints."
disable-model-invocation: true  # OPTIONAL: true = Claude won't auto-invoke
---

# Skill Title

[Skill body content...]

## When to Use

[Clear use cases...]

## How to Use

[Step-by-step instructions...]

## Examples

[Concrete examples...]

## See Also

- [references/](references/) - Detailed reference material
- [examples/](examples/) - Working code examples
```

## Naming Conventions

### Plugin Name (in plugin.json)
- Format: kebab-case (lowercase with hyphens)
- Examples: `jaymd96`, `code-review`, `plugin-dev`
- Used in skill namespaces: `/jaymd96:skill-name`

### Skill Names (in SKILL.md frontmatter)
- Format: kebab-case
- Examples: `python-testing`, `workflow-manager`, `code-review`
- Full invocation: `/plugin-name:skill-name`

### Directory Names
- Format: kebab-case to match identifiers
- Match the name field in SKILL.md frontmatter

### File Names
- SKILL.md - Main skill file (exact name)
- *.md - Documentation files
- *.py, *.sh, etc. - Supporting scripts

## What Goes Where

### ✅ .claude-plugin/
- `plugin.json` - Plugin metadata only
- `marketplace.json` - Optional marketplace entry

### ✅ Plugin Root
- `skills/` - Skill directories with SKILL.md
- `commands/` - Command markdown files
- `agents/` - Agent markdown files
- `hooks/` - hooks.json configuration
- `.mcp.json` - MCP server configuration
- `.lsp.json` - LSP server configuration
- `README.md` - Plugin documentation
- `LICENSE` - License file
- `CHANGELOG.md` - Version history
- `docs/` - Additional documentation

### ❌ NOT in .claude-plugin/
- Don't put skills/ here - goes at plugin root
- Don't put commands/ here - goes at plugin root
- Don't put agents/ here - goes at plugin root
- Don't put other components here

## Real Example Structure (plugin-dev)

From anthropics/claude-code repository:

```
plugin-dev/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── 1-hook-development/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── patterns.md
│   │   │   ├── migration.md
│   │   │   └── advanced-techniques.md
│   │   ├── examples/
│   │   │   └── validate-write-hook.sh
│   │   └── scripts/
│   │       └── validate-hook-schema.sh
│   ├── 2-mcp-integration/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── server-types.md
│   │   │   └── authentication.md
│   │   └── examples/
│   │       ├── stdio-mcp-config.json
│   │       ├── sse-mcp-config.json
│   │       └── http-mcp-config.json
│   ├── 3-plugin-structure/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── manifest-reference.md
│   └── [4 more skills...]
├── commands/
│   └── create-plugin.md
├── agents/
│   └── validator.md
└── README.md
```

This is a working reference - use it as a template!

## Testing Your Plugin Structure

### Validate JSON
```bash
python3 -m json.tool .claude-plugin/plugin.json
```

### Check Skills
```bash
find skills/ -name "SKILL.md" | sort
```

### Verify No .claude-plugin/ Contents
```bash
ls -la .claude-plugin/
# Should show only: plugin.json, marketplace.json
```

### Install Locally
```bash
claude --plugin-dir /path/to/plugin
```

## Checklist for New Plugins

- [ ] `.claude-plugin/` directory created
- [ ] `plugin.json` in `.claude-plugin/` with required fields
- [ ] `skills/` directory at plugin root (if applicable)
- [ ] Each skill in `skills/SKILL-NAME/SKILL.md` format
- [ ] Each SKILL.md has frontmatter with `name` and `description`
- [ ] No skills, commands, or agents inside `.claude-plugin/`
- [ ] `plugin.json` has no `category`, `templates`, or `skills` fields
- [ ] Skill identifiers use kebab-case
- [ ] `README.md` at plugin root with documentation
- [ ] `LICENSE` file present
- [ ] Plugin can install: `claude --plugin-dir /path/to/plugin`
- [ ] Skills appear in `/jaymd96:skill-name` format (with plugin namespace)
