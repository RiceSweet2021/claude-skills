"""多智能体协作极简示例

展示两个 Agent 讨论一个问题。
"""

import agentscope
from agentscope.agents import ChatAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建两个 Agent
agent_a = ChatAgent(
    name="Alice",
    model_config_name="qwen-max",
    system_prompt="你叫 Alice，请与 Bob 讨论问题。"
)

agent_b = ChatAgent(
    name="Bob",
    model_config_name="qwen-max",
    system_prompt="你叫 Bob，请与 Alice 讨论问题。"
)

# 简单对话
topic = "人工智能的未来"
msg = f"请讨论：{topic}"

print(f"Alice: {agent_a(msg)}")
print(f"Bob: {agent_b(msg)}")
