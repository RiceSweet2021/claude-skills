---
name: agentscope-bridge
description: "AgentScope development workflow coordinator. Implements Commander + Advisor architecture: superpowers (commander) decides WHAT/WHY, agentscope-coder and skill-creator (advisors) provide domain knowledge. For any AgentScope framework development tasks. Triggers: agentscope + implement/create/feature/fix/debug, ReActAgent, ChatAgent, MsgHub, MsgDispatcher, Pipeline, agent + memory/tool/workflow, multi-agent, skill + create/modify"
---

# AgentScope Bridge

Workflow coordinator implementing **"Commander + Advisor"** architecture.

## Architecture

```
superpowers (Commander)     → Decides WHAT/WHY/WHEN
    ├── agentscope-coder    → AgentScope code knowledge
    └── skill-creator       → Skill development guidance
```

## Workflow Patterns

| Task Type | Commander | Advisor |
|-----------|-----------|---------|
| New feature | brainstorming → writing-plans → execution | agentscope-coder |
| Bug fix | systematic-debugging → execution → verification | agentscope-coder |
| Create skill | brainstorming → writing-plans → execution | skill-creator |
| Multi-agent | brainstorming → writing-plans → execution | agentscope-coder |

## Component Mapping

| Keywords | Template Path |
|----------|---------------|
| ReActAgent, react | templates/agents/react_agent/ |
| ChatAgent, chat | templates/agents/basic_chat_agent/ |
| SubAgent, nested | templates/agents/subagent/ |
| memory | templates/memory/ |
| tool, decorator | templates/tools/ |
| Pipeline | templates/workflows/sequential_pipeline/ |
| MsgHub, msghub | templates/workflows/msg_hub/ |
| streaming | templates/advanced/streaming/ |
| multi-agent | templates/advanced/multi_agent/ |
| RAG | templates/advanced/rag/ |

## Resource Usage

### coordinator.py
Use for workflow analysis and skill coordination. Can run demo: `python3 coordinator.py`

### Do NOT preload
All referenced skills should be invoked on-demand via Skill tool, not preloaded.
