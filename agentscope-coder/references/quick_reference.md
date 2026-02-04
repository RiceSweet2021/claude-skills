# AgentScope Quick Reference

## Essential Imports

```python
import agentscope
from agentscope.agents import ChatAgent, ReActAgent
from agentscope.memory import InMemoryMemory
from agentscope.pipelines import SequentialPipeline
from agentscope.msghub import MsgHub
```

## Initialization

```python
agentscope.init(model_configs="./model_config.json")
```

## Agent Types

| Agent | Use Case |
|-------|----------|
| `ChatAgent` | Basic dialogue, Q&A |
| `ReActAgent` | Tool calling, reasoning |
| `DialogAgent` | Multi-turn dialogue |

## Memory Types

| Memory | Use Case |
|--------|----------|
| `InMemoryMemory` | Session-based, volatile |
| `LongTermMemory` | Persistent, requires backend |

## Common Patterns

### Create Agent with Memory

```python
memory = InMemoryMemory()
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    memory=memory
)
```

### Create Agent with Tools

```python
def tool_func(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

agent = ReActAgent(
    name="agent",
    tools={"tool_func": tool_func}
)
```

### Create Pipeline

```python
pipeline = SequentialPipeline(agents=[agent1, agent2])
result = pipeline("Input")
```

## Model Configuration

Models are configured in `model_config.json`:

```json
{
  "qwen-max": {
    "type": "dashscope",
    "model": "qwen-max",
    "api_key": "YOUR_API_KEY"
  }
}
```
