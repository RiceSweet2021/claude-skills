"""短期记忆示例

展示 InMemoryMemory 在多轮对话中的应用。
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

# 模拟多轮对话
print("=" * 50)
print("多轮对话示例（带记忆）")
print("=" * 50)

conversations = [
    "我喜欢吃苹果和香蕉",
    "我还喜欢什么水果？",        # Agent 应该能回答之前提到的水果
    "给我推荐一些红色水果",       # 基于偏好推荐
    "谢谢你的推荐！",            # 礼貌结束
]

for msg in conversations:
    print(f"\n用户: {msg}")
    response = agent(msg)
    print(f"助手: {response}")
    print(f"[记忆中当前有 {len(memory)} 条消息]")
