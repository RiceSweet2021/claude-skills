# 长期记忆使用教程

## 核心概念

长期记忆（LongTermMemory）是 AgentScope 中用于持久化存储对话历史的组件。与短期记忆不同，长期记忆具有以下特点：

1. **持久化存储**：对话内容可以保存到文件或数据库
2. **向量检索**：通过语义相似度快速查找相关记忆
3. **跨会话使用**：Agent 重启后仍然可以访问之前的记忆
4. **智能过滤**：可以按重要性或相关性筛选记忆

长期记忆适用于需要记住用户偏好、历史记录等信息的场景。

---

## 代码解析

### 知识点 1：创建长期记忆

**核心代码：**
```python
from agentscope.memory import LongTermMemory

memory = LongTermMemory(
    name="long_memory",
    embedding_model="text-embedding-ada-002"
)
```

**解析：**

创建 LongTermMemory 时的关键参数：

- `name`：记忆实例的唯一标识符
- `embedding_model`：用于生成向量嵌入的模型，用于语义检索

记忆系统使用向量嵌入来存储和检索对话内容，使得 Agent 可以根据语义相似度找到相关的历史记忆。

### 知识点 2：绑定记忆到 Agent

**核心代码：**
```python
agent = DialogAgent(
    name="assistant",
    model_config_name="qwen-max",
    memory=memory  # 绑定记忆对象
)
```

**解析：**

将记忆对象传递给 Agent 后，Agent 会自动：

1. 在每次对话后保存内容到记忆
2. 在生成回复前检索相关记忆
3. 将记忆作为上下文传递给模型

这样 Agent 就能够"记住"之前的对话内容。

### 知识点 3：记忆持久化

**核心代码：**
```python
import json
from pathlib import Path

# 保存记忆到文件
memory_data = {
    'fragments': [
        {'content': frag.content, 'embedding': frag.embedding}
        for frag in memory.memory
    ]
}

with open('memory.json', 'w') as f:
    json.dump(memory_data, f)

# 从文件加载记忆
with open('memory.json', 'r') as f:
    data = json.load(f)
    for fragment in data['fragments']:
        memory.add(fragment['content'], fragment['embedding'])
```

**解析：**

将记忆序列化为 JSON 格式保存到文件，可以实现：

1. **跨会话记忆**：程序重启后仍然可以访问
2. **记忆备份**：防止重要信息丢失
3. **记忆迁移**：在不同环境间共享记忆

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| LongTermMemory | 使用向量嵌入实现语义检索 |
| Agent 绑定 | 通过 `memory` 参数传递记忆对象 |
| 持久化 | 序列化为 JSON 保存到文件 |
| 记忆检索 | 基于语义相似度自动查找相关内容 |

---

## 练习题

1. 创建一个能够记住用户生日并在当天提醒的 Agent
2. 实现记忆的增量保存，每次对话后自动保存
3. 添加记忆过期机制，自动清理旧记忆
