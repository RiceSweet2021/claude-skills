"""SubAgent 子智能体极简示例

展示如何在 Agent 中嵌套使用其他 Agent。
"""

import agentscope
from agentscope.agents import ChatAgent, ReActAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建一个简单的工具函数
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {e}"

# 创建子 Agent
tool_agent = ReActAgent(
    name="tool_user",
    model_config_name="qwen-max",
    tools={"calculator": calculator}
)

# 创建主 Agent，使用子 Agent
main_agent = ChatAgent(
    name="main",
    model_config_name="qwen-max",
    system_prompt="你有一个助手可以帮你进行数学计算。"
)

# 使用子 Agent
response = tool_agent("帮我计算 123 * 456")
print(response)
