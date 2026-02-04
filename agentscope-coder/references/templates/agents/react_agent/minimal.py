"""ReActAgent 极简示例

展示 ReActAgent 的核心概念：推理+行动。
"""

import agentscope
from agentscope.agents import ReActAgent
from agentscope.models import read_model_config

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 定义一个简单的工具
def get_weather(city: str) -> str:
    """获取指定城市的天气"""
    return f"{city}今天晴朗，温度25度"

# 创建 ReActAgent
agent = ReActAgent(
    name="assistant",
    model_config_name="qwen-max",
    tools={"get_weather": get_weather}
)

# 运行 Agent
response = agent("北京今天天气怎么样？")
print(response)
