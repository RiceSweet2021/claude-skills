"""流式输出完整示例

展示流式输出的高级用法，包括多轮对话和中断处理。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.memory import InMemoryMemory
import time
import threading

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 创建支持流式和多轮对话的 Agent ============

agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    stream=True,
    memory=InMemoryMemory(),
    system_prompt="""你是一位资深 AI 架构师。

回答问题时请：
1. 结构清晰，分点论述
2. 包含代码示例
3. 给出实践建议"""
)

# ============ 流式输出处理器 ============

class StreamingPrinter:
    """流式输出处理器"""

    def __init__(self, show_progress=True):
        self.char_count = 0
        self.start_time = None
        self.show_progress = show_progress

    def start(self):
        """开始处理"""
        self.start_time = time.time()
        self.char_count = 0
        print("回复: ", end="", flush=True)

    def process(self, chunk):
        """处理每个文本块"""
        print(chunk, end="", flush=True)
        self.char_count += len(chunk)

        # 每 100 个字符显示一次进度
        if self.show_progress and self.char_count % 100 == 0:
            elapsed = time.time() - self.start_time
            speed = self.char_count / elapsed if elapsed > 0 else 0
            print(f"\n[进度: {self.char_count} 字, {speed:.0f} 字/秒] ", end="", flush=True)

    def finish(self):
        """结束处理"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        speed = self.char_count / elapsed if elapsed > 0 else 0
        print(f"\n\n统计: {self.char_count} 字, {elapsed:.2f} 秒, {speed:.0f} 字/秒")

# ============ 多轮流式对话演示 ============

print("=" * 70)
print("AgentScope 流式输出完整演示")
print("=" * 70)

questions = [
    "请介绍 AgentScope 的核心组件",
    "如何创建一个支持工具调用的 Agent？",
    "AgentScope 有哪些优势？"
]

for i, question in enumerate(questions, 1):
    print(f"\n{'='*70}")
    print(f"[第 {i} 轮对话]")
    print(f"问题: {question}")
    print(f"{'-'*70}")

    # 创建处理器
    printer = StreamingPrinter(show_progress=True)
    printer.start()

    # 流式输出
    for chunk in agent.stream(question):
        printer.process(chunk)

    printer.finish()

# ============ 流式输出对比演示 ============

print(f"\n{'='*70}")
print("[对比演示] 流式 vs 非流式")
print(f"{'='*70}")

# 非流式 Agent
normal_agent = ChatAgent(
    name="normal_assistant",
    model_config_name="qwen-max",
    stream=False
)

print("\n非流式输出:")
start = time.time()
response = normal_agent("说一句你好")
elapsed = time.time() - start
print(f"{response}")
print(f"(等待 {elapsed:.2f} 秒后一次性显示)")

print("\n流式输出:")
start = time.time()
for chunk in agent.stream("说一句你好"):
    if time.time() - start > 0.1:  # 首字延迟
        print(chunk, end="", flush=True)
print()
print("(逐字显示，用户无需等待完整生成)")

print(f"\n{'='*70}")
print("演示结束")
print("=" * 70)
