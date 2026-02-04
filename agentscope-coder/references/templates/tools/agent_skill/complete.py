"""AgentSkill 机制完整示例

展示技能的定义、注册和动态调用。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.skill import Skill

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 技能定义 ============

class DataAnalysisSkill(Skill):
    """数据分析技能"""

    name = "data_analysis"

    def calculate_average(self, numbers: list) -> float:
        """计算平均值

        Args:
            numbers: 数字列表

        Returns:
            平均值
        """
        if not numbers:
            return 0.0
        return sum(numbers) / len(numbers)

    def find_max(self, numbers: list) -> float:
        """找出最大值

        Args:
            numbers: 数字列表

        Returns:
            最大值
        """
        if not numbers:
            return 0.0
        return max(numbers)

    def find_min(self, numbers: list) -> float:
        """找出最小值"""
        if not numbers:
            return 0.0
        return min(numbers)

class TextProcessingSkill(Skill):
    """文本处理技能"""

    name = "text_processing"

    def word_count(self, text: str) -> int:
        """统计字数"""
        return len(text.replace(" ", ""))

    def to_uppercase(self, text: str) -> str:
        """转为大写"""
        return text.upper()

    def to_lowercase(self, text: str) -> str:
        """转为小写"""
        return text.lower()

    def reverse_text(self, text: str) -> str:
        """反转文本"""
        return text[::-1]

# ============ 技能管理器 ============

class SkillManager:
    """技能管理器"""

    def __init__(self):
        self.skills = {}

    def register_skill(self, skill: Skill):
        """注册技能"""
        self.skills[skill.name] = skill
        print(f"✓ 技能 '{skill.name}' 已注册")

    def get_skill(self, skill_name: str):
        """获取技能"""
        return self.skills.get(skill_name)

    def list_skills(self):
        """列出所有技能"""
        return list(self.skills.keys())

# ============ 演示使用 ============

print("=" * 60)
print("AgentSkill 完整功能演示")
print("=" * 60)

# 创建技能管理器
manager = SkillManager()

# 注册技能
data_skill = DataAnalysisSkill()
text_skill = TextProcessingSkill()

manager.register_skill(data_skill)
manager.register_skill(text_skill)

print(f"\n已注册技能: {manager.list_skills()}")

# ============ 技能调用演示 ============

print("\n" + "=" * 60)
print("[数据分析技能演示]")
print("=" * 60)

numbers = [23, 45, 67, 89, 12, 34]
print(f"数据: {numbers}")
print(f"平均值: {data_skill.calculate_average(numbers)}")
print(f"最大值: {data_skill.find_max(numbers)}")
print(f"最小值: {data_skill.find_min(numbers)}")

print("\n" + "=" * 60)
print("[文本处理技能演示]")
print("=" * 60)

text = "Hello AgentScope"
print(f"原文: {text}")
print(f"大写: {text_skill.to_uppercase(text)}")
print(f"小写: {text_skill.to_lowercase(text)}")
print(f"反转: {text_skill.reverse_text(text)}")
print(f"字数: {text_skill.word_count(text)}")

# ============ 技能发现机制 ============

print("\n" + "=" * 60)
print("[技能发现]")
print("=" * 60)

print("\nDataAnalysisSkill 可用方法:")
for method in dir(data_skill):
    if not method.startswith('_'):
        print(f"  - {method}")

print("\nTextProcessingSkill 可用方法:")
for method in dir(text_skill):
    if not method.startswith('_'):
        print(f"  - {method}")
