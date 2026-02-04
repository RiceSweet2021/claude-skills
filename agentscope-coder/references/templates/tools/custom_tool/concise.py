"""自定义工具精简示例

展示多个工具函数的定义和使用。
"""

import agentscope
from agentscope.agents import ReActAgent

agentscope.init(model_configs="./model_config.json")

# 定义多个工具函数
def add(a: float, b: float) -> str:
    """计算两个数的和

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        计算结果的字符串描述
    """
    return f"{a} + {b} = {a + b}"

def multiply(a: float, b: float) -> str:
    """计算两个数的积

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        计算结果的字符串描述
    """
    return f"{a} × {b} = {a * b}"

def power(base: float, exponent: float) -> str:
    """计算幂运算

    Args:
        base: 底数
        exponent: 指数

    Returns:
        计算结果的字符串描述
    """
    result = base ** exponent
    return f"{base}^{exponent} = {result}"

def celsius_to_fahrenheit(celsius: float) -> str:
    """摄氏度转华氏度

    Args:
        celsius: 摄氏温度

    Returns:
        华氏温度字符串
    """
    fahrenheit = celsius * 9 / 5 + 32
    return f"{celsius}°C = {fahrenheit:.1f}°F"

# 创建 Agent，注册所有工具
agent = ReActAgent(
    name="multi_tool_assistant",
    model_config_name="qwen-max",
    tools={
        "add": add,
        "multiply": multiply,
        "power": power,
        "celsius_to_fahrenheit": celsius_to_fahrenheit,
    }
)

print("=" * 60)
print("多功能工具 Agent 演示")
print("=" * 60)

# 测试各种工具
test_cases = [
    "帮我计算 25 加 38",
    "100 乘以 4.5 等于多少",
    "2 的 10 次方是多少",
    "把 25 摄氏度转换成华氏度",
    "先算 10 加 20，再把结果乘以 3",
]

for query in test_cases:
    print(f"\n用户: {query}")
    print("-" * 40)
    response = agent(query)
    print(f"助手: {response}")
