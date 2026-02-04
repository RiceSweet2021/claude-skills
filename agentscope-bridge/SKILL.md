---
name: agentscope-bridge
description: "AgentScope development workflow coordinator. Implements Commander + Advisor architecture: superpowers (commander) decides WHAT/WHY, agentscope-coder and skill-creator (advisors) provide domain knowledge. For any AgentScope framework development tasks. Triggers: agentscope + implement/create/feature/fix/debug, ReActAgent, ChatAgent, MsgHub, MsgDispatcher, Pipeline, agent + memory/tool/workflow, multi-agent, skill + create/modify"
---

# AgentScope Bridge

Workflow coordinator for AgentScope development, implementing the **"Commander + Advisor"** architecture.

## Skill Ecosystem: "Commander + Advisor"

```
┌──────────────────────────────────────────────────────────────────┐
│                    superpowers (Commander)                       │
│  - Decides WHEN/WHY: what to do, why to do it                   │
│  - Controls full development lifecycle                           │
│  - Coordinates skill invocation timing                           │
└──────────────────────────────────────────────────────────────────┘
                          │
                          ▼ Skill reference
        ┌─────────────────┴─────────────────┬─────────────────┐
        │                                    │                 │
┌───────▼────────┐                  ┌───────▼────────┐  ┌──────▼──────┐
│ agentscope-    │                  │ skill-creator  │  │  Other       │
│ coder (Advisor)│                  │   (Advisor)    │  │  Domain      │
│ - Provides HOW │                  │ - Provides HOW │  │  Skills...   │
│   code         │                  │   skill dev    │  │              │
│   templates    │                  │   guidance     │  │              │
│   AgentScope   │                  │                │  │              │
│   knowledge    │                  │                │  │              │
└────────────────┘                  └────────────────┘  └─────────────┘
     ~/.claude/skills/                  ~/.claude/skills/
```

### Role Definitions

| Level | Skill | Role | Responsibility |
|-------|-------|------|----------------|
| **Commander** | superpowers | Commander | Decides what/why/when, which advisor to call |
| **Advisor** | agentscope-coder | Domain Expert | Provides AgentScope code knowledge and templates |
| **Advisor** | skill-creator | Domain Expert | Provides skill development workflow guidance |
| **Bridge** | agentscope-bridge | Coordinator | Defines when to call which advisor skill |

## Coordinated Skills

### Commander Skills (superpowers)

| Sub-skill | Purpose |
|-----------|---------|
| brainstorming | Design exploration, think before building |
| test-driven-development | TDD workflow |
| subagent-driven-development | Plan execution |
| systematic-debugging | Bug investigation |
| writing-plans | Plan writing |
| verification-before-completion | Pre-completion verification |

### Advisor Skills

| Skill | Domain | When to Call |
|-------|--------|--------------|
| **agentscope-coder** | AgentScope code | User request involves AgentScope component development |
| **skill-creator** | Skill development | User request involves creating/modifying skills |

## Development Workflows

### Invocation Decision Flow

```
User Request → Identify Domain → Select Commander → Call Advisor Reference
                          ↓
                    superpowers (Commander)
                          ↓
            Need domain knowledge reference?
                    ↙        ↘
                  Yes         No
                  ↓           ↓
            Call Advisor    Execute
            skill           directly
                  ↓           ↓
            Get domain     Execute
            knowledge       workflow
                  ↓           ↓
            └───────┬───────┘
                    ↓
              Execute + Verify
```

### Pattern 1: Add AgentScope Feature

```
User: "Implement a ReActAgent with memory"

1. superpowers:brainstorming (Commander) → Identify this is AgentScope feature development
2. agentscope-coder (Advisor)        → Get ReActAgent + Memory code template reference
3. superpowers:writing-plans          → Create implementation plan based on template
4. superpowers:subagent-driven-development → Execute development
5. superpowers:verification-before-completion → Verify completion
```

### Pattern 2: Fix AgentScope Code Bug

```
User: "Fix agent initialization error"

1. superpowers:systematic-debugging (Commander) → Investigate root cause
2. agentscope-coder (Advisor)                  → Get correct pattern reference
3. superpowers:test-driven-development          → TDD fix
4. superpowers:verification-before-completion → Verify fix
```

### Pattern 3: Create/Modify New Skill

```
User: "Create a xxx-generator skill"

1. superpowers:brainstorming (Commander) → Understand skill requirements
2. skill-creator (Advisor)               → Get skill development workflow guidance
3. superpowers:writing-plans              → Create implementation plan
4. superpowers:subagent-driven-development → Execute development
5. superpowers:verification-before-completion → Verify skill
```

### Pattern 4: Multi-Agent System Development

```
User: "Create a multi-agent discussion system"

1. superpowers:brainstorming (Commander) → Design system architecture
2. agentscope-coder (Advisor)            → Get MsgHub/multi-agent template
3. superpowers:writing-plans              → Create implementation plan
4. superpowers:subagent-driven-development → Execute development
5. superpowers:verification-before-completion → Verify completion
```

## Invocation Principles

1. **superpowers is always Commander** - All development tasks should be led by superpowers skills
2. **Advisor skills on-demand** - Only call agentscope-coder or skill-creator when domain knowledge is needed
3. **Commander first, then Advisor** - Let superpowers identify task type, then decide which advisor to call

## Invocation Timing

| User Request Type | Commander Skill | Advisor Skill |
|-------------------|-----------------|---------------|
| "Implement a ReActAgent with memory" | brainstorming → writing-plans | agentscope-coder |
| "Create a multi-agent discussion" | brainstorming → writing-plans | agentscope-coder |
| "Create a xxx-generator skill" | brainstorming → writing-plans | skill-creator |
| "Fix agent initialization error" | systematic-debugging | agentscope-coder |
| "Add tools to Agent project" | brainstorming → writing-plans | agentscope-coder |

## Command Reference

### agentscope-coder

```bash
# Generate code
cd ~/.claude/skills/agentscope-coder
PYTHONPATH=. python dynamic/scripts/generate.py "react agent"

# Check dependencies
python dynamic/scripts/check_deps.py

# Run tests
PYTHONPATH=. python dynamic/scripts/test_integration.py
```

### skill-creator

```bash
# Initialize new skill
cd ~/.claude/skills/skill-creator
python scripts/init_skill.py <skill-name> --path <output-directory>

# Package skill
python scripts/package_skill.py <path/to/skill-folder>
```

### superpowers

```bash
# Invoke via Claude Code SlashCommand
/superpowers:brainstorming
/superpowers:test-driven-development
/superpowers:systematic-debugging
/superpowers:writing-plans
/superpowers:subagent-driven-development
/superpowers:verification-before-completion
```

## AgentScope Component Mapping

When user mentions these keywords, reference the corresponding agentscope-coder template:

| Keywords | Component | Template Path |
|----------|-----------|---------------|
| ReActAgent, react, tool calling | ReActAgent | templates/agents/react_agent/ |
| ChatAgent, chat, dialogue | ChatAgent | templates/agents/basic_chat_agent/ |
| SubAgent, nested, sub agent | SubAgent | templates/agents/subagent/ |
| memory | Memory module | templates/memory/ |
| tool, decorator | Tool definition | templates/tools/ |
| Pipeline | Sequential workflow | templates/workflows/sequential_pipeline/ |
| MsgHub, msghub, broadcast | Message hub | templates/workflows/msg_hub/ |
| streaming | Streaming output | templates/advanced/streaming/ |
| multi-agent | Multi-agent system | templates/advanced/multi_agent/ |
| RAG, retrieval augmented | RAG system | templates/advanced/rag/ |

## Design Philosophy

The core idea of this architecture is the **"Commander + Advisor"** pattern:

1. **superpowers is the brain** - Decides what/why/when
2. **Domain skills are encyclopedias** - Provide specific domain knowledge and templates
3. **agentscope-bridge is the coordination protocol** - Defines how to combine them

Advantages of this design:
- **Clear separation of concerns** - Process control decoupled from domain knowledge
- **Easy to extend** - Adding domain skills doesn't affect commander logic
- **Reusable** - Same skill can be reused across different projects
- **Intuitive** - Mimics human team collaboration patterns
