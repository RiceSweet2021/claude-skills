"""AgentSkill 机制极简示例

展示如何创建和使用 Agent 技能。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.skill import Skill
from agentscope.models import read_model_config

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 定义一个技能类
class GreeterSkill(Skill):
    """问候技能"""

    def __call__(self, user_name: str) -> str:
        return f"你好，{user_name}！欢迎使用 AgentScope！"

# 创建 Agent 并注册技能
agent = ChatAgent(
    name="greeter",
    model_config_name="qwen-max"
)

# 使用技能
greeter = GreeterSkill()
print(greeter("小明"))
