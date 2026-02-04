"""RAG 检索增强示例

展示完整的 RAG 流程：文档加载 → 向量化 → 检索 → 生成。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.rag import SimpleRAG

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 准备知识库 ============

knowledge_base = [
    "AgentScope 是一个由清华大学开发的多智能体协作框架",
    "AgentScope 支持多种 Agent 类型，包括 ChatAgent、ReActAgent 等",
    "ReActAgent 结合了推理（Reasoning）和行动（Acting）能力",
    "ChatAgent 是最基础的对话 Agent，适合问答和聊天场景",
    "AgentScope 提供了记忆管理功能，支持长期和短期记忆",
    "AgentScope 支持工具调用，Agent 可以使用外部工具",
    "AgentScope 提供了工作流组件，如 Pipeline 和 MsgHub",
    "AgentScope 的模型配置支持多种大模型 API"
]

# ============ 创建 RAG 系统 ============

print("=" * 60)
print("RAG 检索增强演示")
print("=" * 60)

# 初始化 RAG
rag = SimpleRAG(knowledge_base)

# ============ 查询演示 ============

queries = [
    "AgentScope 是什么？",
    "有哪些类型的 Agent？",
    "ReActAgent 有什么特点？"
]

# ============ 创建回答 Agent ============

agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    system_prompt="你是一个技术助手，根据提供的文档信息回答用户问题。"
)

# ============ 处理每个查询 ============

for query in queries:
    print(f"\n{'='*60}")
    print(f"问题: {query}")
    print(f"{'-'*60}")

    # 检索相关文档
    retrieved = rag.retrieve(query, top_k=3)

    print("检索到的文档:")
    for i, doc in enumerate(retrieved, 1):
        print(f"  {i}. {doc}")

    # 基于检索内容生成回答
    context = "\n".join(retrieved)
    response = agent(f"根据以下参考信息回答问题：\n\n参考信息：\n{context}\n\n问题：{query}")

    print(f"\n回答: {response}")
