# Claude Skills

Collection of custom skills for [Claude Code](https://claude.ai/code).

## Overview

This repository contains reusable skills that extend Claude's capabilities for specific domains and workflows. Each skill is a self-contained package with specialized knowledge, tools, and workflows.

## Skills

### [agentscope-coder](./agentscope-coder/)

AgentScope framework code generator. Provides 12 pre-built templates + LLM fallback for generating multi-agent system code.

- **Templates**: ChatAgent, ReActAgent, SubAgent, memory, tools, workflows, streaming, RAG, multi-agent
- **3 complexity levels**: Minimal (15-30 lines), Concise (50-100), Complete (100-200)
- **Progressive enhancement**: Static templates → LLM generation

**Triggers**: `agentscope`, `agent`, `react`, `chat`, `memory`, `tool`, `workflow`, `pipeline`, `msghub`, `streaming`, `rag`

### [agentscope-bridge](./agentscope-bridge/)

Workflow coordinator implementing "Commander + Advisor" architecture for AgentScope development.

- **Commander**: superpowers (decides WHAT/WHY)
- **Advisors**: agentscope-coder (code), skill-creator (skill development)

**Triggers**: `agentscope + implement/create/feature/fix/debug`, `ReActAgent`, `ChatAgent`, `MsgHub`, `Pipeline`, `multi-agent`

## Installation

### Option 1: Clone and Copy

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/claude-skills.git ~/claude-skills

# Copy skills to Claude's skills directory
cp -r ~/claude-skills/agentscope-coder ~/.claude/skills/
cp -r ~/claude-skills/agentscope-bridge ~/.claude/skills/
```

### Option 2: Symlink (Development)

```bash
# Create symlinks for easy updates
ln -s ~/claude-skills/agentscope-coder ~/.claude/skills/agentscope-coder
ln -s ~/claude-skills/agentscope-bridge ~/.claude/skills/agentscope-bridge
```

## Skill Structure

```
skill-name/
├── SKILL.md           # Required: Metadata (name, description) + instructions
├── scripts/           # Optional: Executable scripts
├── references/        # Optional: Documentation loaded as needed
└── assets/            # Optional: Templates, icons, etc.
```

## Architecture

### "Commander + Advisor" Pattern

```
┌─────────────────────────────────────────────┐
│         superpowers (Commander)              │
│  - Decides WHAT/WHY to do                    │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐      ┌───────▼────────┐
│ agentscope-    │      │ skill-creator  │
│ coder (Advisor)│      │   (Advisor)    │
│ - Provides HOW │      │ - Provides HOW │
└────────────────┘      └────────────────┘
```

- **Commander skills**: Control workflow, decide when/how to act
- **Advisor skills**: Provide domain knowledge and templates
- **Bridge skills**: Coordinate multiple skills

## Development

Skills follow [Claude's skill creation guidelines](https://github.com/anthropics/claude-code/tree/main/skills/skill-creator).

Key principles:
- **Concise is key** - Context window is a shared resource
- **Progressive disclosure** - Metadata → Body → Resources
- **No extra files** - No README.md inside skill directories

## License

MIT

## Contributing

Contributions welcome! Please ensure:
1. SKILL.md follows skill-creator guidelines
2. Description is concise and clear
3. No extra files (README.md, CHANGELOG.md) inside skill directories
4. Test skills before submitting
