"""顺序流水线极简示例

展示多个 Agent 按顺序处理同一个任务。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.pipelines import SequentialPipeline

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 创建多个 Agent
writer = ChatAgent(name="writer", model_config_name="qwen-max")
reviewer = ChatAgent(name="reviewer", model_config_name="qwen-max")

# 创建顺序流水线
pipeline = SequentialPipeline(agents=[writer, reviewer])

# 运行流水线
result = pipeline("写一首关于春天的诗")
print(result)
