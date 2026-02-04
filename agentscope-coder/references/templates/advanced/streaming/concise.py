"""流式输出示例

展示流式输出的进度显示和用户体验优化。
"""

import agentscope
from agentscope.agents import ChatAgent
import time

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建支持流式输出的 Agent
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    stream=True,
    system_prompt="你是一位技术专家，请详细回答问题。"
)

# 流式对话演示
print("=" * 60)
print("流式输出演示")
print("=" * 60)

question = "什么是 AgentScope 框架？"
print(f"\n问题: {question}\n")
print("回答:")

start_time = time.time()
char_count = 0

for chunk in agent.stream(question):
    print(chunk, end="", flush=True)
    char_count += 1

    # 每 50 个字符显示一次进度
    if char_count % 50 == 0:
        elapsed = time.time() - start_time
        speed = char_count / elapsed if elapsed > 0 else 0
        print(f"\n[已生成 {char_count} 字, 速度 {speed:.1f} 字/秒]", end="")

elapsed = time.time() - start_time
print(f"\n\n统计:")
print(f"总字数: {char_count}")
print(f"总耗时: {elapsed:.2f} 秒")
print(f"平均速度: {char_count / elapsed:.1f} 字/秒")
