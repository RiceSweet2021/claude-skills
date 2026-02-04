"""长期记忆精简示例

完整的长期记忆使用示例，展示记忆的持久化能力。
"""

import agentscope
from agentscope.memory import LongTermMemory
from agentscope.agents import DialogAgent
from agentscope.models import read_model_config

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建长期记忆实例
memory = LongTermMemory(
    name="long_memory",
    embedding_model="text-embedding-ada-002"  # 使用 OpenAI 或其他向量模型
)

# 创建 Agent，绑定长期记忆
agent = DialogAgent(
    name="personal_assistant",
    model_config_name="qwen-max",
    memory=memory,
    system_prompt="你是一个贴心的个人助理，请记住用户的个人信息和偏好。"
)

print("=" * 60)
print("第一阶段：信息录入")
print("=" * 60)

# 用户分享个人信息
queries = [
    "你好，我叫李明，是一名软件工程师",
    "我住在上海，平时喜欢打篮球和看电影",
    "我对人工智能技术很感兴趣，特别是大语言模型",
]

for query in queries:
    print(f"\n用户: {query}")
    response = agent(query)
    print(f"助理: {response}")

print("\n" + "=" * 60)
print("第二阶段：记忆测试")
print("=" * 60)

# 测试 Agent 是否记住了信息
test_queries = [
    "我叫什么名字？",
    "我住在哪里？",
    "我有什么爱好？",
    "我的职业是什么？",
]

for query in test_queries:
    print(f"\n用户: {query}")
    response = agent(query)
    print(f"助理: {response}")

print("\n" + "=" * 60)
print("记忆状态")
print("=" * 60)
print(f"记忆片段数量: {len(memory.memory)}")
for i, fragment in enumerate(memory.memory[-5:], 1):  # 显示最近5条
    print(f"{i}. {fragment}")
