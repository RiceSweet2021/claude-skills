"""自定义工具极简示例

展示如何定义一个简单的工具函数。
"""

import agentscope
from agentscope.agents import ReActAgent

agentscope.init(model_configs="./model_config.json")

# 定义工具函数
def add(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b

# 创建 Agent 并注册工具
agent = ReActAgent(
    name="calculator",
    model_config_name="qwen-max",
    tools={"add": add}
)

# 使用工具
response = agent("请计算 123 加 456 等于多少")
print(response)
