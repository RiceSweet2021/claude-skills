"""长期记忆极简示例

展示如何使用 AgentScope 的长期记忆功能。
"""

import agentscope
from agentscope.memory import LongTermMemory
from agentscope.agents import DialogAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建长期记忆
memory = LongTermMemory()

# 创建带记忆的 Agent
agent = DialogAgent(
    name="assistant",
    model_config_name="qwen-max",
    memory=memory
)

# 第一次对话
agent("我叫张三，住在北京")
agent("我喜欢吃苹果")

# 第二次对话（会记住之前的信息）
response = agent("我叫什么名字？")
print(response)  # 应该能回答"你叫张三"
