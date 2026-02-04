"""多智能体协作完整示例

展示辩论式多 Agent 协作，包含立场对立和投票机制。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.memory import InMemoryMemory

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 创建辩论参与者 ============

pro_agent = ChatAgent(
    name="Pro_Speaker",
    model_config_name="qwen-max",
    memory=InMemoryMemory(),
    system_prompt="""你是正方辩手。

立场：支持人工智能技术快速发展。

你的论点：
1. AI 提高生产效率
2. AI 解决复杂问题
3. AI 创造新的就业机会

请用有力的论据支持你的立场。"""
)

con_agent = ChatAgent(
    name="Con_Speaker",
    model_config_name="qwen-max",
    memory=InMemoryMemory(),
    system_prompt="""你是反方辩手。

立场：担忧人工智能技术快速发展。

你的论点：
1. AI 可能导致失业
2. AI 存在安全风险
3. AI 缺乏伦理约束

请用有力的论据支持你的立场。"""
)

judge = ChatAgent(
    name="Judge",
    model_config_name="qwen-max",
    system_prompt="""你是辩论评委。

你的职责：
1. 分析双方论点的优劣
2. 指出逻辑漏洞
3. 给出公正评判

请客观、专业地进行点评。"""
)

# ============ 辩论流程 ============

print("=" * 70)
print("多 Agent 辩论赛")
print("=" * 70)

topic = "人工智能快速发展是否利大于弊"
print(f"\n辩题: {topic}")
print("-" * 70)

# 第一轮：立论
print("\n[第一轮：立论陈词]")
print("=" * 70)

pro_opening = pro_agent(f"请就'{topic}'进行正方立论陈词（100字左右）")
print(f"\n正方: {pro_opening}")

con_opening = con_agent(f"请就'{topic}'进行反方立论陈词（100字左右）")
print(f"\n反方: {con_opening}")

# 第二轮：反驳
print("\n[第二轮：互相反驳]")
print("=" * 70)

pro_rebuttal = pro_agent(f"反方说：{con_opening}\n请反驳（100字左右）")
print(f"\n正方反驳: {pro_rebuttal}")

con_rebuttal = con_agent(f"正方说：{pro_rebuttal}\n请反驳（100字左右）")
print(f"\n反方反驳: {con_rebuttal}")

# 第三轮：总结
print("\n[第三轮：总结陈词]")
print("=" * 70)

pro_summary = pro_agent("请做正方总结陈词（80字左右）")
print(f"\n正方总结: {pro_summary}")

con_summary = con_agent("请做反方总结陈词（80字左右）")
print(f"\n反方总结: {con_summary}")

# 评委点评
print("\n[评委点评]")
print("=" * 70)

verdict = judge(f"""
请对以下辩论进行点评：

辩题：{topic}

正方观点：
- 立论: {pro_opening[:80]}...
- 反驳: {pro_rebuttal[:80]}...
- 总结: {pro_summary[:80]}...

反方观点：
- 立论: {con_opening[:80]}...
- 反驳: {con_rebuttal[:80]}...
- 总结: {con_summary[:80]}...

请给出：
1. 双方表现评价
2. 优缺点分析
3. 最终判定""")
print(f"\n{verdict}")

print("\n" + "=" * 70)
print("辩论结束")
print("=" * 70)
