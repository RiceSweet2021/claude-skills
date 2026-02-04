# 自定义工具函数教程

## 核心概念

工具函数是 Agent 与外部世界交互的桥梁。通过定义工具，Agent 可以：

1. **访问外部数据**：获取天气、时间、股票等信息
2. **执行计算**：进行数学运算、数据处理
3. **操作服务**：发送请求、调用 API
4. **扩展能力**：实现模型无法直接完成的功能

工具函数本质上是普通的 Python 函数，但需要遵循特定的规范才能被 Agent 正确调用。

---

## 代码解析

### 知识点 1：工具函数规范

**核心代码：**
```python
def add(a: float, b: float) -> str:
    """计算两个数的和

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        计算结果的字符串描述
    """
    return f"{a} + {b} = {a + b}"
```

**解析：**

一个规范的工具函数应该包含：

| 要素 | 说明 | 示例 |
|------|------|------|
| **类型注解** | 参数和返回值的类型 | `a: float` `-> str` |
| **文档字符串** | 描述函数功能 | `"""计算两个数的和"""` |
| **参数说明** | 解释每个参数的含义 | `Args: a: 第一个数` |
| **返回说明** | 解释返回值的含义 | `Returns: 计算结果` |
| **字符串返回** | 返回便于 Agent 理解的文本 | `f"{a} + {b} = {a + b}"` |

### 知识点 2：工具注册

**核心代码：**
```python
agent = ReActAgent(
    name="assistant",
    model_config_name="qwen-max",
    tools={
        "add": add,
        "multiply": multiply,
        "calculate": calculate,
    }
)
```

**解析：**

工具通过 `tools` 字典参数注册：

1. **键（Key）**：工具的调用名称，Agent 会使用这个名称调用工具
2. **值（Value）**：工具函数对象（不是字符串，是函数本身）

建议使用清晰、描述性的工具名称，如 `get_weather` 而不是 `tool1`。

### 知识点 3：错误处理

**核心代码：**
```python
def safe_calculate(expression: str) -> str:
    """安全计算数学表达式"""
    # 验证输入
    if not re.match(r'^[\d+\-*/().\s]+$', expression):
        raise ValueError(f"表达式包含非法字符: {expression}")

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except ZeroDivisionError:
        raise ValueError("除数不能为零")
```

**解析：**

工具函数中的错误处理很重要：

1. **输入验证**：检查参数是否合法
2. **异常捕获**：处理可能的运行时错误
3. **明确错误信息**：返回 Agent 能理解的错误描述

这样 Agent 可以在出错时给用户友好的反馈。

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| 函数规范 | 类型注解 + 文档字符串 + 字符串返回 |
| 工具注册 | 通过 `tools` 字典参数，键为调用名 |
| 错误处理 | 验证输入 + 捕获异常 + 明确错误信息 |
| 工具命名 | 使用描述性名称，便于 Agent 理解 |

---

## 练习题

1. 创建一个 `get_stock_price` 工具，查询股票价格
2. 实现一个 `send_email` 工具，发送邮件通知
3. 编写一个支持多种单位转换的工具函数
