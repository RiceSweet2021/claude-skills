"""基础对话 Agent 示例

展示 ChatAgent 的基本用法和系统提示词设置。
"""

import agentscope
from agentscope.agents import ChatAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建对话 Agent，带有系统提示词
agent = ChatAgent(
    name="helpful_assistant",
    model_config_name="qwen-max",
    system_prompt="你是一个友好的 AI 助手，专门帮助用户解答关于 AgentScope 框架的问题。"
)

# 进行多轮对话
print("=" * 50)
print("对话示例")
print("=" * 50)

queries = [
    "什么是 AgentScope？",
    "AgentScope 有哪些主要组件？",
    "如何创建一个简单的 Agent？"
]

for query in queries:
    print(f"\n用户: {query}")
    response = agent(query)
    print(f"助手: {response}")

print("\n" + "=" * 50)
print("对话结束")
print("=" * 50)
