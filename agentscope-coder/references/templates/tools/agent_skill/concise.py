"""AgentSkill 机制示例

展示如何定义技能并集成到 Agent 中。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.skill import Skill

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 技能定义 ============

class CalculatorSkill(Skill):
    """计算器技能"""

    def add(self, a: float, b: float) -> float:
        """加法运算"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        return a - b

class FormatterSkill(Skill):
    """格式化技能"""

    def format_list(self, items: list) -> str:
        """格式化列表为字符串"""
        return ", ".join(str(item) for item in items)

    def format_dict(self, data: dict) -> str:
        """格式化字典为字符串"""
        return "\n".join(f"{k}: {v}" for k, v in data.items())

# ============ Agent 创建 ============

agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    system_prompt="你是一个助手，可以帮助用户进行计算和格式化操作。"
)

# ============ 技能使用 ============

print("=" * 50)
print("AgentSkill 使用示例")
print("=" * 50)

# 创建技能实例
calc = CalculatorSkill()
formatter = FormatterSkill()

# 测试计算器技能
print("\n[计算器技能]")
print(f"10 + 5 = {calc.add(10, 5)}")
print(f"10 - 5 = {calc.subtract(10, 5)}")

# 测试格式化技能
print("\n[格式化技能]")
items = ["苹果", "香蕉", "橙子"]
print(f"列表格式化: {formatter.format_list(items)}")

data = {"name": "张三", "age": 25, "city": "北京"}
print("字典格式化:")
print(formatter.format_dict(data))
