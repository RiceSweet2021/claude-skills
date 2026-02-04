"""自定义工具完整示例

生产级工具定义，包含错误处理、类型验证和文档规范。
"""

import agentscope
from agentscope.agents import ReActAgent
from typing import Callable, Dict, Any, List, Optional, Union
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ToolRegistry:
    """工具注册表类

    管理所有工具函数的注册和验证。
    """

    def __init__(self):
        """初始化工具注册表"""
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> bool:
        """注册工具函数

        Args:
            name: 工具名称
            func: 工具函数

        Returns:
            是否注册成功
        """
        if name in self._tools:
            logger.warning(f"工具 '{name}' 已存在，将被覆盖")

        # 验证函数是否有文档字符串
        if not func.__doc__:
            logger.warning(f"工具 '{name}' 缺少文档字符串")

        self._tools[name] = func
        logger.info(f"工具 '{name}' 注册成功")
        return True

    def get_tools(self) -> Dict[str, Callable]:
        """获取所有已注册工具

        Returns:
            工具字典
        """
        return self._tools.copy()

    def list_tools(self) -> List[str]:
        """列出所有工具名称

        Returns:
            工具名称列表
        """
        return list(self._tools.keys())


# === 工具函数定义 ===

def safe_calculate(expression: str) -> str:
    """安全计算数学表达式

    Args:
        expression: 待计算的数学表达式字符串

    Returns:
        计算结果字符串

    Raises:
        ValueError: 当表达式非法时
    """
    # 只允许数字和基本运算符
    if not re.match(r'^[\d+\-*/().\s]+$', expression):
        raise ValueError(f"表达式包含非法字符: {expression}")

    try:
        # 使用安全的 eval 环境
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except ZeroDivisionError:
        raise ValueError("除数不能为零")
    except Exception as e:
        raise ValueError(f"计算失败: {str(e)}")


def format_currency(amount: float, currency: str = "CNY") -> str:
    """格式化货币金额

    Args:
        amount: 金额数值
        currency: 货币代码（CNY, USD, EUR, JPY）

    Returns:
        格式化后的货币字符串
    """
    currency_symbols = {
        "CNY": "¥",
        "USD": "$",
        "EUR": "€",
        "JPY": "¥",
    }

    symbol = currency_symbols.get(currency, currency)

    # 根据货币类型格式化
    if currency == "JPY":
        # 日元不显示小数
        return f"{symbol}{int(amount):,}"
    else:
        # 其他货币显示两位小数
        return f"{symbol}{amount:,.2f}"


def calculate_tip(bill_amount: float, tip_percentage: float = 15) -> str:
    """计算小费和总金额

    Args:
        bill_amount: 账单金额
        tip_percentage: 小费百分比（默认15%）

    Returns:
        包含小费和总额的字符串
    """
    if bill_amount < 0:
        raise ValueError("账单金额不能为负数")
    if tip_percentage < 0 or tip_percentage > 100:
        raise ValueError("小费百分比必须在 0-100 之间")

    tip = bill_amount * tip_percentage / 100
    total = bill_amount + tip

    return (
        f"账单: ¥{bill_amount:.2f}\n"
        f"小费 ({tip_percentage}%): ¥{tip:.2f}\n"
        f"总计: ¥{total:.2f}"
    )


def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """单位转换

    支持长度（米、千米、厘米、毫米）和重量（千克、克、吨）转换。

    Args:
        value: 待转换的数值
        from_unit: 原单位
        to_unit: 目标单位

    Returns:
        转换结果字符串
    """
    # 长度单位转换基准（米）
    length_units = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
    }

    # 重量单位转换基准（千克）
    weight_units = {
        "g": 0.001,
        "kg": 1.0,
        "t": 1000.0,
    }

    # 检查单位类型
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit in length_units and to_unit in length_units:
        # 长度转换
        base_value = value * length_units[from_unit]
        result = base_value / length_units[to_unit]
        return f"{value} {from_unit} = {result} {to_unit}"

    elif from_unit in weight_units and to_unit in weight_units:
        # 重量转换
        base_value = value * weight_units[from_unit]
        result = base_value / weight_units[to_unit]
        return f"{value} {from_unit} = {result} {to_unit}"

    else:
        return f"不支持 {from_unit} 到 {to_unit} 的转换"


def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取指定时区的当前时间

    Args:
        timezone: 时区名称（如 Asia/Shanghai, America/New_York）

    Returns:
        当前时间字符串
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo

    try:
        tz = ZoneInfo(timezone)
        now = datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        return f"获取时间失败: {str(e)}"


# === 主程序 ===

def create_tool_agent() -> ReActAgent:
    """创建带工具注册的 Agent

    Returns:
        配置好的 ReactAgent
    """
    # 创建工具注册表
    registry = ToolRegistry()

    # 注册所有工具
    tools_to_register = {
        "safe_calculate": safe_calculate,
        "format_currency": format_currency,
        "calculate_tip": calculate_tip,
        "unit_convert": unit_convert,
        "get_current_time": get_current_time,
    }

    for name, func in tools_to_register.items():
        registry.register(name, func)

    # 创建 Agent
    agent = ReActAgent(
        name="utility_assistant",
        model_config_name="qwen-max",
        tools=registry.get_tools()
    )

    logger.info(f"Agent 创建完成，注册了 {len(registry.list_tools())} 个工具")
    return agent


def demo():
    """运行工具演示"""
    # 初始化
    agentscope.init(model_configs="./model_config.json")

    # 创建 Agent
    agent = create_tool_agent()

    # 演示查询
    demos = [
        "帮我计算 150 * 8 + 200",
        "把 5000 元格式化成货币显示",
        "账单是 280 元，给 18% 的小费，总共多少钱",
        "把 2.5 千米转换成米",
        "现在纽约时间是几点",
    ]

    print("=" * 70)
    print("实用工具 Agent 演示")
    print("=" * 70)

    for query in demos:
        print(f"\n用户: {query}")
        print("-" * 70)
        try:
            response = agent(query)
            print(f"助手: {response}")
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    demo()
