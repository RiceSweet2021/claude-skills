"""短期记忆极简示例

展示 InMemoryMemory 的基本用法。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.memory import InMemoryMemory

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建带记忆的 Agent
memory = InMemoryMemory()
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    memory=memory
)

# 多轮对话
agent("我的名字是小明")
response = agent("我叫什么名字？")
print(response)
