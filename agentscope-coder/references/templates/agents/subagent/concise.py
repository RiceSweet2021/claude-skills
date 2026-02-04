"""SubAgent 子智能体示例

展示主 Agent 和子 Agent 的协作模式。
"""

import agentscope
from agentscope.agents import ChatAgent, ReActAgent

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 定义工具函数
def get_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_web(query: str) -> str:
    """模拟网络搜索"""
    return f"关于 '{query}' 的搜索结果：这是模拟的搜索内容。"

# 创建专门的工具子 Agent
specialist = ReActAgent(
    name="specialist",
    model_config_name="qwen-max",
    tools={
        "get_time": get_time,
        "search_web": search_web
    },
    system_prompt="你是一个信息查询专家，可以帮助获取时间和搜索信息。"
)

# 创建主 Agent
manager = ChatAgent(
    name="manager",
    model_config_name="qwen-max",
    system_prompt="""你是一个任务协调者。

当用户需要查询信息或使用工具时，请通知你的助手 specialist 来处理。
对于普通对话，你可以直接回答。"""
)

print("=" * 50)
print("任务协调示例")
print("=" * 50)

# 测试场景
test_cases = [
    "你好，请问 AgentScope 是什么？",  # 主 Agent 处理
    "现在几点了？",                      # 需要 specialist
    "帮我搜索一下 Python 教程"           # 需要 specialist
]

for query in test_cases:
    print(f"\n用户: {query}")
    print(f"协调者: {manager(query)}")
