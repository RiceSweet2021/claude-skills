"""多智能体协作示例

展示三个 Agent 进行讨论式对话。
"""

import agentscope
from agentscope.agents import ChatAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 创建讨论小组 ============

moderator = ChatAgent(
    name="Moderator",
    model_config_name="qwen-max",
    system_prompt="你是讨论主持人，负责引导讨论、总结观点。"
)

expert_a = ChatAgent(
    name="Expert_A",
    model_config_name="qwen-max",
    system_prompt="你是技术专家 A，支持技术方案，请从技术角度发言。"
)

expert_b = ChatAgent(
    name="Expert_B",
    model_config_name="qwen-max",
    system_prompt="你是产品专家 B，关注用户体验，请从产品角度发言。"
)

# ============ 讨论流程 ============

print("=" * 60)
print("多 Agent 讨论示例")
print("=" * 60)

topic = "是否应该在聊天应用中引入 AI 助手"
print(f"\n讨论主题: {topic}\n")

# 主持人开场
opening = moderator(f"请开始讨论：{topic}")
print(f"主持人: {opening}\n")

# 专家 A 发言
response_a = expert_a(opening)
print(f"专家 A: {response_a}\n")

# 专家 B 发言
response_b = expert_b(f"{response_a}\n请发表你的看法")
print(f"专家 B: {response_b}\n")

# 主持人总结
summary = moderator(f"请总结两位专家的观点：\nA: {response_a}\nB: {response_b}")
print(f"主持人总结: {summary}")
