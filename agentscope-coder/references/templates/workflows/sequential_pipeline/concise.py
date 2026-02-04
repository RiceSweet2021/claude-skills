"""顺序流水线示例

展示文章创作的三阶段流水线：写作 → 审阅 → 发布。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.pipelines import SequentialPipeline

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 创建不同角色的 Agent ============

writer = ChatAgent(
    name="writer",
    model_config_name="qwen-max",
    system_prompt="你是一位专业作家，负责撰写文章初稿。"
)

reviewer = ChatAgent(
    name="reviewer",
    model_config_name="qwen-max",
    system_prompt="你是一位编辑，负责审阅文章并提出修改意见。"
)

publisher = ChatAgent(
    name="publisher",
    model_config_name="qwen-max",
    system_prompt="你是发布员，负责生成最终发布的文章格式。"
)

# ============ 创建流水线 ============

pipeline = SequentialPipeline(agents=[writer, reviewer, publisher])

# ============ 运行流水线 ============

print("=" * 60)
print("文章创作流水线")
print("=" * 60)

topic = "人工智能的未来发展"
print(f"\n主题: {topic}\n")

result = pipeline(topic)

print("\n" + "=" * 60)
print("最终结果:")
print("=" * 60)
print(result)
