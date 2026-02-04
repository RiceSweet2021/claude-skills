"""消息中心极简示例

展示 MsgHub 实现多 Agent 广播通信。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.msghub import MsgHub

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建多个 Agent
agent1 = ChatAgent(name="agent1", model_config_name="qwen-max")
agent2 = ChatAgent(name="agent2", model_config_name="qwen-max")
agent3 = ChatAgent(name="agent3", model_config_name="qwen-max")

# 创建消息中心
hub = MsgHub()

# 广播消息给所有 Agent
hub.broadcast("大家好，欢迎使用 AgentScope！")
