"""消息中心示例

展示 MsgHub 实现 Agent 之间的点对点通信。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.msghub import MsgHub

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 创建不同角色的 Agent ============

coordinator = ChatAgent(
    name="coordinator",
    model_config_name="qwen-max",
    system_prompt="你是任务协调者，负责分配任务给其他 Agent。"
)

worker1 = ChatAgent(
    name="worker1",
    model_config_name="qwen-max",
    system_prompt="你是数据处理专员，负责处理数据分析任务。"
)

worker2 = ChatAgent(
    name="worker2",
    model_config_name="qwen-max",
    system_prompt="你是内容生成专员，负责撰写文档内容。"
)

# ============ 创建消息中心 ============

hub = MsgHub()

# ============ 定义通信规则 ============

# 协调者可以向所有工人发送消息
hub.connect(coordinator, [worker1, worker2])

# 工人可以向协调者报告结果
hub.connect(worker1, coordinator)
hub.connect(worker2, coordinator)

# ============ 模拟通信 ============

print("=" * 50)
print("多 Agent 通信示例")
print("=" * 50)

# 协调者广播任务
task = "请处理一个数据分析任务"
print(f"\n协调者广播: {task}")
hub.send(coordinator, task, broadcast=True)

# 工人1响应
response1 = worker1(f"我收到任务: {task}")
print(f"工人1: {response1}")

# 工人2响应
response2 = worker2(f"我收到任务: {task}")
print(f"工人2: {response2}")
