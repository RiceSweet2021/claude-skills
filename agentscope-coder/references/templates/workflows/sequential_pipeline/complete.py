"""顺序流水线完整示例

展示多阶段数据处理流水线，包含中间结果监控。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.pipelines import SequentialPipeline

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 阶段 1: 数据提取 ============

extractor = ChatAgent(
    name="extractor",
    model_config_name="qwen-max",
    system_prompt="""你是数据提取专家。

从用户输入中提取结构化信息，包括：
1. 关键实体（人名、地名、组织名等）
2. 重要事件
3. 时间信息

请以 JSON 格式返回提取结果。"""
)

# ============ 阶段 2: 数据分析 ============

analyzer = ChatAgent(
    name="analyzer",
    model_config_name="qwen-max",
    system_prompt="""你是数据分析专家。

根据提取的信息，分析：
1. 事件之间的关联性
2. 潜在的影响和趋势
3. 可能的后续发展

请给出简洁的分析结论。"""
)

# ============ 阶段 3: 报告生成 ============

reporter = ChatAgent(
    name="reporter",
    model_config_name="qwen-max",
    system_prompt="""你是报告生成专家。

根据数据提取和分析结果，生成一份结构化报告，包括：
1. 执行摘要
2. 详细分析
3. 结论和建议

报告应该专业、清晰、易读。"""
)

# ============ 创建流水线 ============

pipeline = SequentialPipeline(
    agents=[extractor, analyzer, reporter],
    show_progress=True  # 显示中间结果
)

# ============ 测试数据 ============

test_data = """
2024年1月，科技巨头ABC公司宣布推出新一代AI助手产品。
该产品由张三领导的团队开发，历时两年完成。
产品发布后，股价上涨15%，市场反应积极。
专家预测，这将对整个AI行业产生深远影响。
"""

# ============ 运行流水线 ============

print("=" * 70)
print("智能信息处理流水线")
print("=" * 70)

print("\n[输入数据]")
print(test_data)

print("\n" + "=" * 70)
print("[开始处理]")
print("=" * 70)

result = pipeline(test_data)

print("\n" + "=" * 70)
print("[最终报告]")
print("=" * 70)
print(result)

# ============ 流水线统计 ============

print("\n" + "=" * 70)
print("流水线统计:")
print(f"处理阶段数: {len(pipeline.agents)}")
print(f"各阶段名称: {[agent.name for agent in pipeline.agents]}")
print("=" * 70)
