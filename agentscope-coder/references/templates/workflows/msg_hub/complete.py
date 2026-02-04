"""消息中心完整示例

展示 MsgHub 实现复杂的多 Agent 协作网络。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.msghub import MsgHub

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 创建协作团队 ============

# 项目经理
manager = ChatAgent(
    name="manager",
    model_config_name="qwen-max",
    system_prompt="""你是项目经理。

你的职责：
1. 分配任务给团队成员
2. 收集工作成果
3. 整合最终报告

团队成员：
- developer: 负责技术实现
- designer: 负责设计工作
- tester: 负责质量测试"""
)

# 开发工程师
developer = ChatAgent(
    name="developer",
    model_config_name="qwen-max",
    system_prompt="你是开发工程师，负责技术实现和代码编写。"
)

# 设计师
designer = ChatAgent(
    name="designer",
    model_config_name="qwen-max",
    system_prompt="你是设计师，负责界面设计和用户体验。"
)

# 测试工程师
tester = ChatAgent(
    name="tester",
    model_config_name="qwen-max",
    system_prompt="你是测试工程师，负责质量保证和问题发现。"
)

# ============ 创建消息中心 ============

hub = MsgHub()

# ============ 建立通信网络 ============

# 项目经理可以向所有人广播
hub.connect(manager, [developer, designer, tester])

# 团队成员可以向项目经理汇报
hub.connect(developer, manager)
hub.connect(designer, manager)
hub.connect(tester, manager)

# 开发和设计师之间可以协作
hub.connect(developer, designer)
hub.connect(designer, developer)

# ============ 项目执行流程 ============

print("=" * 70)
print("敏捷开发团队协作模拟")
print("=" * 70)

# 阶段 1: 项目启动
print("\n[阶段 1: 项目启动]")
print("-" * 50)

project_task = "开发一个待办事项管理应用"
manager_msg = manager(f"请团队开始执行项目：{project_task}")
print(f"经理: {manager_msg}")

# 模拟任务分配
print("\n任务分配:")
hub.send(manager, "请开始设计和开发工作", broadcast=True)

# 阶段 2: 设计阶段
print("\n[阶段 2: 设计阶段]")
print("-" * 50)

design_work = designer("请设计待办事项应用的界面")
print(f"设计师: {design_work}")

# 开发评审设计
dev_feedback = developer(f"请评审这个设计：{design_work}")
print(f"开发评审: {dev_feedback}")

# 阶段 3: 开发阶段
print("\n[阶段 3: 开发阶段]")
print("-" * 50)

dev_work = developer("请实现待办事项的核心功能")
print(f"开发: {dev_work[:100]}...")

# 阶段 4: 测试阶段
print("\n[阶段 4: 测试阶段]")
print("-" * 50)

test_report = tester(f"请测试这个应用：{dev_work[:200]}...")
print(f"测试报告: {test_report[:150]}...")

# 阶段 5: 项目总结
print("\n[阶段 5: 项目总结]")
print("-" * 50)

summary = manager(f"""
请整合以下信息生成项目总结：
- 设计方案: {design_work[:100]}...
- 开发成果: {dev_work[:100]}...
- 测试报告: {test_report[:100]}...
""")
print(f"项目总结: {summary[:200]}...")

# ============ 通信统计 ============

print("\n" + "=" * 70)
print("通信网络统计")
print("=" * 70)
print(f"参与 Agent 数: 4")
print(f"通信连接数: {len(hub.connections) if hasattr(hub, 'connections') else '已建立'}")
print("=" * 70)
