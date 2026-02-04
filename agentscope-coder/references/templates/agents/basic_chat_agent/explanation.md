# ChatAgent 基础对话教程

## 核心概念

ChatAgent 是 AgentScope 中最基础的 Agent 类型，专注于对话交互。它具有以下特点：

1. **简单易用**：只需提供名称和模型配置即可创建
2. **系统提示词**：可以设置角色和行为准则
3. **记忆管理**：可选地保存对话历史，支持多轮对话
4. **参数可调**：支持温度、top-p 等生成参数

ChatAgent 适合用于问答、聊天机器人、客服等场景。

---

## 代码解析

### 知识点 1：创建基础 ChatAgent

**核心代码：**
```python
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max"
)
```

**解析：**

ChatAgent 的最小化创建只需要两个参数：

| 参数 | 说明 | 必填 |
|------|------|------|
| `name` | Agent 的唯一标识名称 | 是 |
| `model_config_name` | 模型配置名称（在 model_config.json 中定义） | 是 |

创建后，可以直接像函数一样调用：`agent("你的问题")`

### 知识点 2：设置系统提示词

**核心代码：**
```python
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    system_prompt="你是一个友好的 AI 助手，专门回答技术问题。"
)
```

**解析：**

`system_prompt` 参数定义了 Agent 的角色和行为：

1. **角色定位**：告诉 Agent 它是什么（如助手、顾问、客服）
2. **行为准则**：规定 Agent 应该如何回答
3. **专业领域**：指定 Agent 擅长的领域

好的系统提示词应该：
- 明确具体，避免模糊
- 说明应该做什么和不应该做什么
- 定义回答的风格和长度

### 知识点 3：添加记忆功能

**核心代码：**
```python
from agentscope.memory import InMemoryMemory

memory = InMemoryMemory()

agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    memory=memory
)
```

**解析：**

记忆功能使 Agent 能够记住之前的对话内容：

1. **InMemoryMemory**：将对话保存在内存中，程序重启后清空
2. **自动管理**：每次对话自动保存到记忆中
3. **上下文感知**：Agent 可以引用之前对话的内容

对于需要长期持久化的场景，可以使用 AgentScope 的长期记忆功能。

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| ChatAgent 创建 | 最少需要 name 和 model_config_name 两个参数 |
| 系统提示词 | 定义 Agent 的角色、行为和回答风格 |
| 记忆功能 | 通过 memory 参数添加，支持多轮对话 |
| Agent 调用 | 直接将 Agent 对象当作函数调用 |

---

## 练习题

1. 创建一个专门翻译文本的 ChatAgent
2. 添加系统提示词，让 Agent 以 JSON 格式返回回答
3. 尝试调整 temperature 参数，观察回答风格的变化
