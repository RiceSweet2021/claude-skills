---
name: agentscope-coder
description: AgentScope code generator. 12 pre-built templates + LLM fallback. Supports: ReActAgent, ChatAgent, MsgHub, Pipeline, memory, tools, streaming, RAG, multi-agent. Triggers: agentscope, agent, react, chat, memory, tool, workflow, pipeline, msghub, streaming, rag
---

# AgentScope Coder

## Overview

This skill provides instant access to AgentScope framework code examples. It contains 12 pre-built templates covering all major AgentScope components: ChatAgent, ReActAgent, SubAgent, memory management, tools, workflows, streaming, RAG, and multi-agent collaboration.

Each template comes in 3 complexity levels:
- **Minimal** (15-30 lines) - Quick concept understanding
- **Concise** (50-100 lines) - Complete runnable examples (recommended)
- **Complete** (100-200 lines) - Production-grade code

## Quick Start

When user asks about AgentScope, use the matching template directly:

```
User: "How to use ReActAgent?"
→ Use templates/agents/react_agent/

User: "How do I add memory to my agent?"
→ Use templates/memory/short_term_memory/

User: "Create a multi-agent system"
→ Use templates/advanced/multi_agent/
```

### Template Categories

| Category | Templates | Keywords |
|----------|-----------|----------|
| **Agents** | react_agent, basic_chat_agent, subagent | react, chat, subagent |
| **Memory** | long_term_memory, short_term_memory | memory, longterm, short |
| **Tools** | custom_tool, agent_skill | tool, skill, decorator |
| **Workflows** | sequential_pipeline, msg_hub | pipeline, workflow, msghub |
| **Advanced** | streaming, multi_agent, rag | streaming, multi, rag |

## Template Selection Guide

Match user query to template:

1. **Agent creation**
   - Basic dialogue: `basic_chat_agent`
   - Tool calling: `react_agent`
   - Nested agents: `subagent`

2. **Memory**
   - Session history: `short_term_memory`
   - Persistent storage: `long_term_memory`

3. **Tools**
   - Simple functions: `custom_tool`
   - Class-based skills: `agent_skill`

4. **Workflows**
   - Sequential processing: `sequential_pipeline`
   - Broadcast communication: `msg_hub`

5. **Advanced**
   - Real-time output: `streaming`
   - Multiple agents discussion: `multi_agent`
   - Knowledge-augmented QA: `rag`

## Template Structure

Each template directory contains:
- `minimal.py` - 15-30 lines, core concept only
- `concise.py` - 50-100 lines, complete runnable (default)
- `complete.py` - 100-200 lines, production-ready
- `explanation.md` - Detailed tutorial with knowledge points

## Using Templates

Read the appropriate template file based on requested complexity:

```python
# Default: concise level
from references/templates/agents/react_agent/concise.py

# User wants simpler example
from references/templates/agents/react_agent/minimal.py

# User wants full-featured example
from references/templates/agents/react_agent/complete.py
```

## Common Patterns

### Agent Creation

```python
import agentscope
from agentscope.agents import ChatAgent

agentscope.init(model_configs="./model_config.json")

agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    system_prompt="You are a helpful assistant."
)

response = agent("Your question here")
```

### Tool Definition

```python
def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

agent = ReActAgent(
    name="agent",
    tools={"my_tool": my_tool}
)
```

### Memory

```python
from agentscope.memory import InMemoryMemory

memory = InMemoryMemory()
agent = ChatAgent(name="agent", memory=memory)
```

### Workflow

```python
from agentscope.pipelines import SequentialPipeline

pipeline = SequentialPipeline(agents=[agent1, agent2])
result = pipeline("Input")
```

## Code Quality

All templates follow AgentScope best practices:
- Proper import statements
- Type annotations
- Docstrings
- Error handling
- Clean, readable code
- Ready to run (with model config)

## Progressive Enhancement

This skill uses a two-tier strategy:

### Level 1: Static Templates (Default)

- 12 pre-built templates, 3 complexity levels each
- No API key required
- Instant response
- Covers common AgentScope patterns

### Level 2: LLM Generation (Opt-in)

When no template matches:
- Checks if `DASHSCOPE_API_KEY` is configured
- Uses LLM to generate custom code
- Validates syntax and safety
- Falls back to error message if unavailable

### For Claude Code:

When user asks for AgentScope code:

1. **Check static templates first**
   - Run: `PYTHONPATH=. python dynamic/scripts/generate.py "<query>" -c concise`
   - If successful, return code directly

2. **If template fails and API available**
   - LLM generates custom code
   - Validate before returning

3. **If both unavailable**
   - Inform user about available templates
   - Suggest installing/configuring dependencies

## Resources

### references/templates/

The complete template library organized by category. Each template contains working code examples and explanations.

**When to read:** Load specific template file when user asks about that component. Do not preload all templates.

### dynamic/

Python module for LLM-based code generation:
- `core.py` - Data models (GeneratedCode, ComplexityLevel)
- `retriever.py` - Template matching
- `parser.py` - LLM response parsing
- `validator.py` - Code validation
- `generator.py` - Main CodeGenerator class
- `scripts/` - CLI tools

**When to use:** For dynamic code generation when templates don't match.

### scripts/

Utility scripts:
- `generate.py` - CLI for code generation
- `check_deps.py` - Check dependencies for LLM generation
- `test_integration.py` - Run integration tests

**When to use:** Run directly without loading into context for validation tasks.
