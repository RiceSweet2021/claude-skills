"""RAG 检索增强极简示例

展示使用向量存储和检索增强生成。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.rag import SimpleRAG

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# 准备文档知识
documents = [
    "AgentScope 是一个多智能体框架",
    "ReActAgent 支持工具调用功能",
    "ChatAgent 是最基础的对话 Agent"
]

# 创建 RAG 系统
rag = SimpleRAG(documents)

# 创建带 RAG 的 Agent
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max"
)

# 查询并检索相关文档
query = "ReActAgent 有什么功能？"
retrieved_docs = rag.retrieve(query)

# 结合检索内容回答
context = "\n".join(retrieved_docs)
response = agent(f"根据以下信息回答问题：\n{context}\n\n问题：{query}")
print(response)
