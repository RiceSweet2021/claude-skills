"""基础对话 Agent 完整示例

展示 ChatAgent 的完整功能，包括系统提示词、温度参数设置和对话历史管理。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.memory import InMemoryMemory

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建带记忆的对话 Agent
memory = InMemoryMemory()

agent = ChatAgent(
    name="advanced_assistant",
    model_config_name="qwen-max",
    system_prompt="""你是一个专业的 AI 框架技术顾问。

你的职责是：
1. 准确回答用户关于 AgentScope 的问题
2. 提供清晰易懂的代码示例
3. 当不确定时，诚实告知用户
4. 保持回答简洁但完整""",
    memory=memory,
    temperature=0.7  # 控制输出的随机性
)

# 模拟多轮对话场景
print("=" * 60)
print("AgentScope 技术顾问 - 对话示例")
print("=" * 60)

conversation = [
    "你好，我想学习 AgentScope",
    "从哪里开始比较好？",
    "能给我一个简单的示例吗？",
    "谢谢你的帮助！"
]

for i, user_msg in enumerate(conversation, 1):
    print(f"\n[第 {i} 轮]")
    print(f"用户: {user_msg}")

    response = agent(user_msg)

    print(f"顾问: {response}")

    # 显示当前对话记忆
    if i < len(conversation):
        print(f"  (当前记忆中保存了 {len(memory)} 条消息)")

print("\n" + "=" * 60)
print("对话历史摘要:")
print(f"总轮数: {len(memory)}")
print("=" * 60)
