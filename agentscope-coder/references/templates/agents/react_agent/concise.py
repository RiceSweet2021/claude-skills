"""ReActAgent 精简示例

完整可运行的 ReActAgent 示例，展示工具调用能力。
"""

import agentscope
from agentscope.agents import ReActAgent
from agentscope.models import read_model_config

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 定义工具函数
def get_weather(city: str) -> str:
    """获取指定城市的天气信息

    Args:
        city: 城市名称

    Returns:
        天气描述字符串
    """
    # 模拟天气数据
    weather_data = {
        "北京": "晴朗，温度25°C",
        "上海": "多云，温度28°C",
        "深圳": "小雨，温度30°C",
    }
    return weather_data.get(city, f"{city}的天气信息暂无")

def get_time(city: str) -> str:
    """获取指定城市的时间

    Args:
        city: 城市名称

    Returns:
        时间字符串
    """
    from datetime import datetime
    now = datetime.now()
    return f"{city}当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"

# 创建 ReActAgent，注册工具
agent = ReActAgent(
    name="weather_assistant",
    model_config_name="qwen-max",
    tools={
        "get_weather": get_weather,
        "get_time": get_time,
    }
)

# 测试工具调用
print("=" * 50)
print("测试 1: 查询天气")
print("=" * 50)
response = agent("北京今天天气怎么样？")
print(f"Agent 回复: {response}\n")

print("=" * 50)
print("测试 2: 查询时间")
print("=" * 50)
response = agent("现在上海几点了？")
print(f"Agent 回复: {response}\n")

print("=" * 50)
print("测试 3: 组合查询")
print("=" * 50)
response = agent("帮我查一下深圳的天气和时间")
print(f"Agent 回复: {response}\n")
