---
name: agentscope-coder
description: "AgentScope code generator. 12 pre-built templates + LLM fallback. Supports: ReActAgent, ChatAgent, MsgHub, Pipeline, memory, tools, streaming, RAG, multi-agent. Triggers: agentscope, agent, react, chat, memory, tool, workflow, pipeline, msghub, streaming, rag"
---

# AgentScope Coder

Instant access to AgentScope framework code examples. 12 pre-built templates covering all major components.

## Quick Start

When user asks about AgentScope, read the matching template:

| Category | Templates | Keywords |
|----------|-----------|----------|
| **Agents** | react_agent, basic_chat_agent, subagent | react, chat, subagent |
| **Memory** | long_term_memory, short_term_memory | memory, longterm, short |
| **Tools** | custom_tool, agent_skill | tool, skill, decorator |
| **Workflows** | sequential_pipeline, msg_hub | pipeline, workflow, msghub |
| **Advanced** | streaming, multi_agent, rag | streaming, multi, rag |

## Template Structure

Each template has 3 complexity levels:
- `minimal.py` - 15-30 lines, core concept only
- `concise.py` - 50-100 lines, complete runnable (default)
- `complete.py` - 100-200 lines, production-ready

## Resource Usage

### references/templates/
Load specific template file when user asks. Do NOT preload all templates.

### dynamic/
For LLM-based generation when templates don't match. Run scripts directly without loading into context.

### scripts/
Run directly for validation tasks. Do NOT load into context.
