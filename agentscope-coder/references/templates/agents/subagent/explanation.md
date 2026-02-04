# SubAgent 子智能体教程

## 核心概念

SubAgent（子智能体）是指在 Agent 中嵌套使用其他 Agent 的设计模式。这种架构带来以下优势：

1. **专业分工**：每个子 Agent 专注于特定领域（如计算、搜索、天气）
2. **模块化设计**：便于独立开发和测试各个功能模块
3. **灵活组合**：可以根据需要动态添加或移除子 Agent
4. **责任分离**：主 Agent 负责协调，子 Agent 负责执行

SubAgent 模式适合构建复杂的多功能 AI 系统。

---

## 代码解析

### 知识点 1：创建子 Agent

**核心代码：**
```python
# 创建专门功能的子 Agent
specialist = ReActAgent(
    name="specialist",
    model_config_name="qwen-max",
    tools={"calculate": calculator},
    system_prompt="你是计算专家，专门处理数学问题。"
)

# 创建主 Agent
manager = ChatAgent(
    name="manager",
    model_config_name="qwen-max",
    system_prompt="你有一个助手可以帮你进行计算。"
)
```

**解析：**

子 Agent 和主 Agent 的创建方式相同，关键在于：

1. **功能定位**：子 Agent 通常具备特定能力（如工具调用）
2. **提示词设计**：子 Agent 的系统提示词更聚焦于专业领域
3. **层级关系**：主 Agent 负责任务分发，子 Agent 负责具体执行

### 知识点 2：任务协调模式

**核心代码：**
```python
coordinator = ChatAgent(
    name="coordinator",
    system_prompt="""你管理三个专业助手：
1. math_expert - 处理数学计算
2. weather_agent - 处理天气查询
3. news_agent - 处理新闻资讯

根据用户问题，分发给合适的助手处理。"""
)
```

**解析：**

任务协调的核心在于主 Agent 的系统提示词设计：

| 要素 | 说明 |
|------|------|
| 能力声明 | 明确列出有哪些子 Agent 可用 |
| 职责划分 | 说明每个子 Agent 负责什么类型的问题 |
| 分发逻辑 | 指导如何判断应该由哪个子 Agent 处理 |

### 知识点 3：子 Agent 通信

**核心代码：**
```python
# 主 Agent 可以"调用"子 Agent
math_result = math_expert("计算 100 + 200")
weather_result = weather_agent("北京天气")

# 主 Agent 整合子 Agent 的结果
final_response = f"根据计算结果{math_result}，同时{weather_result}"
```

**解析：**

子 Agent 之间的通信有两种方式：

1. **直接调用**：在代码层面直接调用子 Agent 并获取结果
2. **提示词引导**：通过系统提示词让 LLM "模拟"调用子 Agent

在 AgentScope 中，推荐使用 MsgHub 等工作流组件实现更规范的 Agent 间通信。

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| SubAgent 定义 | 在 Agent 中嵌套使用其他 Agent 的模式 |
| 专业分工 | 每个 Agent 专注于特定领域 |
| 任务协调 | 主 Agent 负责任务分发和结果整合 |
| 系统提示词 | 明确声明可用子 Agent 及其职责 |

---

## 练习题

1. 创建一个包含"翻译专家"和"写作专家"的 SubAgent 系统
2. 设计一个三层架构：协调层 → 专业层 → 工具层
3. 尝试让主 Agent 根据问题复杂度动态选择使用子 Agent
