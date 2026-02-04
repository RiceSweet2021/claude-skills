"""短期记忆完整示例

展示 InMemoryMemory 的高级用法，包括记忆管理、清理和查询。
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
    memory=memory,
    system_prompt="你是一个有记忆的对话助手，能够记住用户之前说过的话。"
)

print("=" * 60)
print("InMemoryMemory 完整功能演示")
print("=" * 60)

# ============ 第一阶段：正常对话 ============
print("\n[阶段 1: 建立记忆]")
print("-" * 40)

user_inputs = [
    "我叫张三，是一名软件工程师",
    "我最喜欢的编程语言是 Python",
    "我正在学习 AgentScope 框架",
]

for msg in user_inputs:
    response = agent(msg)
    print(f"用户: {msg}")
    print(f"助手: {response}\n")

# ============ 第二阶段：记忆检索 ============
print("[阶段 2: 记忆检索]")
print("-" * 40)
print(f"当前记忆条数: {len(memory)}")

# 查看记忆内容
print("\n记忆内容:")
for i, msg in enumerate(memory.get_memory()):
    print(f"  {i+1}. [{msg.role}] {msg.content[:50]}...")

# ============ 第三阶段：基于记忆的对话 ============
print("\n[阶段 3: 基于记忆的对话]")
print("-" * 40)

test_questions = [
    "我叫什么名字？",
    "我是什么职业？",
    "我喜欢什么编程语言？",
    "我在学习什么框架？",
]

for question in test_questions:
    response = agent(question)
    print(f"用户: {question}")
    print(f"助手: {response}\n")

# ============ 第四阶段：记忆管理 ============
print("[阶段 4: 记忆管理]")
print("-" * 40)

# 清空记忆
print(f"清空前记忆数: {len(memory)}")
memory.clear()
print(f"清空后记忆数: {len(memory)}")

# 清空后测试
response = agent("你还记得我叫什么吗？")
print(f"用户: 你还记得我叫什么吗？")
print(f"助手: {response}")

print("\n" + "=" * 60)
print("演示结束")
print("=" * 60)
