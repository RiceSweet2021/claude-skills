"""基础对话 Agent 极简示例

展示最简单的对话 Agent 创建方法。
"""

import agentscope
from agentscope.agents import ChatAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建对话 Agent
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max"
)

# 进行对话
response = agent("你好，请介绍一下你自己")
print(response)
