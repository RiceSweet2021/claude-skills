"""流式输出极简示例

展示 Agent 的流式响应功能。
"""

import agentscope
from agentscope.agents import ChatAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建 Agent
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    stream=True  # 启用流式输出
)

# 流式生成响应
print("Agent 回复: ", end="", flush=True)

for chunk in agent.stream("请介绍一下 Python 编程语言"):
    print(chunk, end="", flush=True)

print()  # 换行
