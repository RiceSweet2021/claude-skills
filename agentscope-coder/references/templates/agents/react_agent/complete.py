"""ReActAgent 完整示例

生产级代码示例，包含完整的错误处理、类型注解和文档字符串。
"""

import agentscope
from agentscope.agents import ReActAgent
from agentscope.models import read_model_config
from typing import Callable, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_agent_scope(model_config_path: str = "./model_config.json") -> bool:
    """初始化 AgentScope

    Args:
        model_config_path: 模型配置文件路径

    Returns:
        初始化是否成功
    """
    try:
        agentscope.init(model_configs=model_config_path)
        logger.info("AgentScope 初始化成功")
        return True
    except Exception as e:
        logger.error(f"AgentScope 初始化失败: {e}")
        return False


def get_weather(city: str) -> str:
    """获取指定城市的天气信息

    Args:
        city: 城市名称

    Returns:
        天气描述字符串

    Raises:
        ValueError: 当城市名称为空时
    """
    if not city or not city.strip():
        raise ValueError("城市名称不能为空")

    # 模拟天气数据
    weather_data: Dict[str, Dict[str, Any]] = {
        "北京": {
            "condition": "晴朗",
            "temperature": 25,
            "humidity": 45,
            "wind": "东北风 3级"
        },
        "上海": {
            "condition": "多云",
            "temperature": 28,
            "humidity": 65,
            "wind": "东南风 2级"
        },
        "深圳": {
            "condition": "小雨",
            "temperature": 30,
            "humidity": 80,
            "wind": "无风"
        },
    }

    data = weather_data.get(city.strip())
    if data:
        return (f"{city}天气：{data['condition']}，"
                f"温度{data['temperature']}°C，"
                f"湿度{data['humidity']}%，"
                f"{data['wind']}")
    else:
        return f"抱歉，没有{city}的天气信息"


def get_time(city: str) -> str:
    """获取指定城市的当前时间

    Args:
        city: 城市名称

    Returns:
        时间字符串
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo

    # 城市时区映射
    timezones: Dict[str, str] = {
        "北京": "Asia/Shanghai",
        "上海": "Asia/Shanghai",
        "深圳": "Asia/Shanghai",
        "纽约": "America/New_York",
        "伦敦": "Europe/London",
        "东京": "Asia/Tokyo",
    }

    tz_name = timezones.get(city.strip(), "Asia/Shanghai")
    try:
        tz = ZoneInfo(tz_name)
        now = datetime.now(tz)
        return f"{city}当前时间：{now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        logger.warning(f"获取{city}时间失败: {e}")
        return f"{city}时间获取失败"


def calculate(expression: str) -> str:
    """计算数学表达式

    Args:
        expression: 数学表达式字符串

    Returns:
        计算结果字符串

    Raises:
        ValueError: 当表达式无效时
    """
    try:
        # 仅允许安全的数学运算
        allowed_names = {}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        raise ValueError(f"无效的表达式: {expression}")


def create_react_agent() -> ReActAgent:
    """创建配置好的 ReActAgent

    Returns:
        ReActAgent 实例
    """
    tools: Dict[str, Callable] = {
        "get_weather": get_weather,
        "get_time": get_time,
        "calculate": calculate,
    }

    agent = ReActAgent(
        name="intelligent_assistant",
        model_config_name="qwen-max",
        tools=tools,
    )

    logger.info(f"ReActAgent '{agent.name}' 创建成功，注册了 {len(tools)} 个工具")
    return agent


def run_interactive_demo(agent: ReActAgent) -> None:
    """运行交互式演示

    Args:
        agent: ReActAgent 实例
    """
    test_queries = [
        "北京今天天气怎么样？",
        "现在伦敦几点了？",
        "帮我计算 25 * 4 + 10",
        "我想知道深圳的天气，还有现在几点",
    ]

    print("=" * 70)
    print("ReActAgent 交互式演示")
    print("=" * 70)

    for i, query in enumerate(test_queries, 1):
        print(f"\n[查询 {i}] {query}")
        print("-" * 70)
        try:
            response = agent(query)
            print(f"[回复] {response}")
        except Exception as e:
            print(f"[错误] {e}")

    print("\n" + "=" * 70)
    print("演示完成")
    print("=" * 70)


def main() -> None:
    """主函数"""
    # 初始化
    if not initialize_agent_scope():
        return

    # 创建 Agent
    try:
        agent = create_react_agent()
    except Exception as e:
        logger.error(f"创建 Agent 失败: {e}")
        return

    # 运行演示
    run_interactive_demo(agent)


if __name__ == "__main__":
    main()
