"""SubAgent 子智能体完整示例

展示多层 Agent 架构，包含任务分发和结果聚合。
"""

import agentscope
from agentscope.agents import ChatAgent, ReActAgent
from agentscope.memory import InMemoryMemory

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 工具函数定义 ============

def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        result = eval(expression)
        return f"{result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

def get_weather(city: str) -> str:
    """获取天气信息"""
    weather_db = {
        "北京": "晴天，25°C",
        "上海": "多云，28°C",
        "深圳": "小雨，30°C"
    }
    return weather_db.get(city, f"{city} 暂无数据")

def get_news(category: str) -> str:
    """获取新闻"""
    news = {
        "科技": "AI 技术最新突破：大模型效率提升50%",
        "体育": "奥运会备战工作全面展开",
        "财经": "股市今日收盘上涨2.5%"
    }
    return news.get(category, f"{category}版块暂无新闻")

# ============ 子 Agent 创建 ============

# 数学专家 Agent
math_expert = ReActAgent(
    name="math_expert",
    model_config_name="qwen-max",
    tools={"calculate": calculate},
    system_prompt="你是数学计算专家，专门处理各种数学运算问题。"
)

# 天气查询 Agent
weather_agent = ReActAgent(
    name="weather_agent",
    model_config_name="qwen-max",
    tools={"get_weather": get_weather},
    system_prompt="你是天气查询助手，负责提供城市天气信息。"
)

# 新闻查询 Agent
news_agent = ReActAgent(
    name="news_agent",
    model_config_name="qwen-max",
    tools={"get_news": get_news},
    system_prompt="你是新闻助手，负责提供各类新闻资讯。"
)

# ============ 主协调 Agent ============

coordinator = ChatAgent(
    name="coordinator",
    model_config_name="qwen-max",
    memory=InMemoryMemory(),
    system_prompt="""你是任务协调中心，管理三个专业助手：

1. math_expert - 处理数学计算问题
2. weather_agent - 处理天气查询
3. news_agent - 处理新闻资讯

当用户提问时，判断应该由哪个助手处理，然后模拟调用该助手。
对于普通对话，你可以直接回答。

请用友好专业的语气回复用户。"""
)

# ============ 测试场景 ============

print("=" * 60)
print("多 Agent 协作系统 - 任务协调示例")
print("=" * 60)

scenarios = [
    ("数学问题", "帮我计算 1234 * 5678 + 999"),
    ("天气查询", "北京今天天气怎么样？"),
    ("新闻资讯", "有什么科技新闻吗？"),
    ("普通对话", "请介绍一下你的团队"),
]

for title, query in scenarios:
    print(f"\n{'='*60}")
    print(f"场景: {title}")
    print(f"用户: {query}")
    print(f"协调中心: {coordinator(query)}")

print(f"\n{'='*60}")
print(f"对话历史记录: {len(coordinator.memory)} 条")
print("=" * 60)
