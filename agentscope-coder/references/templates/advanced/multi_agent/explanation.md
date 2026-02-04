# 多智能体协作教程

## 核心概念

多智能体协作（Multi-Agent Collaboration）是指多个 Agent 共同完成一个任务的模式。通过合理设计 Agent 之间的关系，可以实现：

1. **观点多样性**：不同 Agent 有不同视角，产生更全面的回答
2. **任务分工**：每个 Agent 专注于自己的专业领域
3. **互相补充**：Agent 之间可以互相纠正、补充信息
4. **协作智能**：群体智慧超越单个 Agent 的能力

多 Agent 协作适合复杂问题分析、辩论讨论、创意生成等场景。

---

## 代码解析

### 知识点 1：创建多 Agent 系统

**核心代码：**
```python
# 创建多个角色不同的 Agent
agent_a = ChatAgent(
    name="Expert_A",
    model_config_name="qwen-max",
    system_prompt="你是技术专家，从技术角度分析。"
)

agent_b = ChatAgent(
    name="Expert_B",
    model_config_name="qwen-max",
    system_prompt="你是产品专家，从用户角度分析。"
)
```

**解析：**

多 Agent 系统的设计要点：

| 要点 | 说明 |
|------|------|
| 角色定义 | 每个 Agent 有明确的专业领域或立场 |
| 系统提示词 | 通过 prompt 赋予 Agent 不同的视角 |
| 记忆管理 | 每个 Agent 可以有独立的记忆 |

### 知识点 2：对话流程设计

**核心代码：**
```python
# 主持人开场
opening = moderator("请开始讨论")

# 专家 A 发言
response_a = expert_a(opening)

# 专家 B 回应 A
response_b = expert_b(response_a)

# 主持人总结
summary = moderator(f"总结: A={response_a}, B={response_b}")
```

**解析：**

对话流程的设计模式：

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| 顺序发言 | Agent 按顺序依次发言 | 简单讨论 |
| 辩论对立 | Agent 互相反驳 | 观点对立分析 |
| 协作补充 | 后续 Agent 补充前面的内容 | 创意生成 |

### 知识点 3：上下文传递

**核心代码：**
```python
# 将 Agent A 的回答传递给 Agent B
context = f"专家 A 说: {response_a}"
response_b = expert_b(context)

# 或包含更多历史
full_context = f"""
A 的观点: {response_a}
B 的观点: {response_b}
请总结: """
summary = moderator(full_context)
```

**解析：**

上下文传递的最佳实践：

1. **简洁引用**：只引用关键内容，避免上下文过长
2. **结构化格式**：使用清晰的格式标记发言者
3. **明确指令**：告诉后续 Agent 如何使用前面的信息

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| 角色设计 | 每个 Agent 有不同的专业领域或立场 |
| 流程设计 | 选择合适的对话模式（顺序/辩论/协作） |
| 上下文传递 | 将前面的观点传递给后续 Agent |
| 记忆管理 | 可为每个 Agent 配置独立记忆 |

---

## 典型应用场景

| 场景 | Agent 配置 |
|------|-----------|
| 观点分析 | 不同立场的专家 |
| 创意风暴 | 不同风格的创作者 |
| 问题诊断 | 不同专长的诊断员 |
| 决策讨论 | 不同利益的代表 |

---

## 练习题

1. 创建一个三人创业团队：CEO、CTO、CMO 讨论新产品发布
2. 实现"投票机制"，让多个 Agent 投票决定最终方案
3. 设计一个"轮流发言"的多 Agent 创意写作系统
