# 顺序流水线教程

## 核心概念

SequentialPipeline（顺序流水线）是 AgentScope 中用于组织多个 Agent 依次处理同一任务的工作流模式。它的特点是：

1. **顺序执行**：Agent 按预定顺序依次处理
2. **结果传递**：前一个 Agent 的输出作为后一个 Agent 的输入
3. **职责分离**：每个 Agent 专注于处理任务的特定阶段
4. **易于扩展**：可以灵活添加或移除处理阶段

SequentialPipeline 适合多步骤任务场景，如文章创作、数据处理、内容审核等。

---

## 代码解析

### 知识点 1：创建流水线

**核心代码：**
```python
from agentscope.pipelines import SequentialPipeline

agent1 = ChatAgent(name="stage1", model_config_name="qwen-max")
agent2 = ChatAgent(name="stage2", model_config_name="qwen-max")

pipeline = SequentialPipeline(agents=[agent1, agent2])
```

**解析：**

创建流水线的关键：

1. **Agent 列表**：按处理顺序传入 Agent 对象列表
2. **顺序保证**：列表中的顺序即为执行顺序
3. **类型一致**：通常使用相同类型的 Agent（如都是 ChatAgent）

### 知识点 2：运行流水线

**核心代码：**
```python
result = pipeline("处理这个任务")
```

**解析：**

流水线执行过程：

```
输入 → Agent1 → 中间结果1 → Agent2 → 中间结果2 → ... → 最终输出
```

1. 第一个 Agent 接收原始输入
2. 后续 Agent 接收前一个 Agent 的输出
3. 最后一个 Agent 的输出作为流水线结果

### 知识点 3：各阶段职责划分

**核心代码：**
```python
writer = ChatAgent(
    name="writer",
    system_prompt="负责撰写初稿"
)

reviewer = ChatAgent(
    name="reviewer",
    system_prompt="负责审阅和修改"
)

publisher = ChatAgent(
    name="publisher",
    system_prompt="负责格式化发布"
)

pipeline = SequentialPipeline(agents=[writer, reviewer, publisher])
```

**解析：**

合理的阶段划分原则：

| 原则 | 说明 |
|------|------|
| 单一职责 | 每个 Agent 只负责一个明确的子任务 |
| 顺序合理 | 前一阶段的输出是后一阶段的输入 |
| 独立可测 | 每个 Agent 可以独立测试验证 |

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| SequentialPipeline | 多个 Agent 顺序执行的工作流 |
| 结果传递 | 前一 Agent 输出 → 后一 Agent 输入 |
| 职责分离 | 每个 Agent 专注任务的特定阶段 |
| 适用场景 | 多步骤任务，如写作、数据处理 |

---

## 练习题

1. 创建一个四阶段翻译流水线：原文 → 翻译 → 校对 → 格式化
2. 实现一个带条件分支的流水线（根据内容选择不同处理路径）
3. 添加中间结果日志，观察每个阶段的输出
