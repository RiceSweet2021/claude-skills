# ReActAgent 工具调用教程

## 核心概念

ReActAgent 是 AgentScope 中支持推理和行动的 Agent 类型。它结合了 **推理（Reasoning）** 和 **行动（Acting）** 两种能力，能够：

1. **理解用户意图**：分析用户需要什么
2. **规划行动步骤**：决定使用哪些工具
3. **执行工具调用**：按步骤调用相应函数
4. **整合结果**：将工具返回的信息组织成自然语言回复

ReActAgent 的工作流程是：**观察 → 思考 → 行动 → 观察** 的循环。

---

## 代码解析

### 知识点 1：工具函数定义

**核心代码：**
```python
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    weather_data = {
        "北京": "晴朗，温度25°C",
        "上海": "多云，温度28°C",
    }
    return weather_data.get(city, f"{city}的天气信息暂无")
```

**解析：**

工具函数是 ReActAgent 执行任务的基本单元。定义工具函数时需要注意：

1. **类型注解**：使用 `str`、`int` 等类型注解，帮助 Agent 理解参数类型
2. **文档字符串**：`"""..."""` 中的描述会被 Agent 读取，理解工具功能
3. **简单返回**：返回字符串类型的结果，便于 Agent 处理
4. **错误处理**：使用 `.get()` 方法避免 KeyError

### 知识点 2：创建 ReActAgent

**核心代码：**
```python
agent = ReActAgent(
    name="weather_assistant",
    model_config_name="qwen-max",
    tools={
        "get_weather": get_weather,
        "get_time": get_time,
    }
)
```

**解析：**

创建 ReActAgent 的关键参数：

| 参数 | 说明 | 必填 |
|------|------|------|
| `name` | Agent 名称，用于标识 | 是 |
| `model_config_name` | 使用的模型配置名称 | 是 |
| `tools` | 工具函数字典 `{名称: 函数}` | 否 |

`tools` 参数是一个字典，键是工具名称（Agent 会用这个名称调用），值是函数对象。

### 知识点 3：Agent 调用

**核心代码：**
```python
response = agent("北京今天天气怎么样？")
print(f"Agent 回复: {response}")
```

**解析：**

直接将 Agent 对象当作函数调用，传入用户查询。Agent 会自动：

1. 分析查询，判断需要调用 `get_weather` 工具
2. 提取参数 `"北京"`
3. 调用工具函数获取结果
4. 将结果组织成自然语言回复

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| 工具函数定义 | 需要类型注解和详细的文档字符串 |
| 工具注册 | 通过 `tools` 字典参数注册，键为调用名称 |
| Agent 调用 | 直接像函数一样调用 Agent 对象 |
| ReAct 循环 | 观察→思考→行动的循环过程 |

---

## 练习题

1. 添加一个 `get_temperature` 工具，只返回温度信息
2. 创建一个支持货币换算的 ReactAgent
3. 尝试让 Agent 同时处理天气和时间查询
