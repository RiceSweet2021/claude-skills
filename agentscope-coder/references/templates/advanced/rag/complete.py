"""RAG 检索增强完整示例

展示 RAG 的完整工作流程，包括文档管理、向量检索和答案生成。
"""

import agentscope
from agentscope.agents import ChatAgent
from agentscope.memory import InMemoryMemory

# 初始化 AgentScope
agentscope.init(model_configs="./model_config.json")

# ============ 知识库文档 ============

DOCUMENTS = {
    "agent_intro": "AgentScope 是一个多智能体框架，由清华大学知识工程实验室开发。它提供了完整的 Agent 开发、部署和调度能力，支持多种大语言模型 API。",
    "chat_agent": "ChatAgent 是 AgentScope 中最基础的 Agent 类型，专注于对话交互。它支持自定义系统提示词、记忆管理，适合构建聊天机器人、客服助手等应用。",
    "react_agent": "ReActAgent 是支持推理和行动的 Agent 类型。ReAct 代表 Reasoning（推理）和 Acting（行动），Agent 可以根据任务需要自主决定调用哪些工具函数。",
    "memory": "AgentScope 提供了灵活的记忆管理机制。InMemoryMemory 用于短期对话记忆，长期记忆支持 Mem0 和 Reme 等后端，实现跨会话的信息持久化。",
    "workflow": "AgentScope 提供了丰富的工作流组件。SequentialPipeline 实现顺序流水线，MsgHub 支持多 Agent 广播通信，这些组件可以灵活组合构建复杂的多 Agent 系统。",
    "tools": "AgentScope 支持工具调用机制。通过 @tool_decorator 装饰器可以快速定义工具函数，Agent 可以根据语义理解自动选择合适的工具进行调用。"
}

# ============ 简化的 RAG 实现 ============

class SimpleRAG:
    """简化的 RAG 系统"""

    def __init__(self, documents):
        """初始化 RAG 系统

        Args:
            documents: 文档字典 {标题: 内容}
        """
        self.documents = documents
        self.doc_keys = list(documents.keys())
        self.doc_texts = list(documents.values())

    def retrieve(self, query: str, top_k: int = 2):
        """检索相关文档

        Args:
            query: 查询文本
            top_k: 返回前 k 个最相关的文档

        Returns:
            相关文档内容列表
        """
        # 简化的关键词匹配检索
        query_lower = query.lower()
        scores = []

        for title, content in self.documents.items():
            score = 0
            content_lower = content.lower()

            # 关键词匹配
            for word in query_lower.split():
                if word in content_lower:
                    score += content_lower.count(word)

            scores.append((score, title, content))

        # 按得分排序，返回 top_k
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc[2] for doc in scores[:top_k] if doc[0] > 0]

    def add_document(self, title: str, content: str):
        """添加新文档"""
        self.documents[title] = content
        self.doc_keys.append(title)
        self.doc_texts.append(content)

# ============ 创建 RAG 和 Agent ============

rag = SimpleRAG(DOCUMENTS)

qa_agent = ChatAgent(
    name="qa_assistant",
    model_config_name="qwen-max",
    memory=InMemoryMemory(),
    system_prompt="""你是一个 AgentScope 技术顾问。

你的任务是根据提供的参考文档回答用户问题。
请遵循以下规则：
1. 只使用参考文档中的信息
2. 如果参考文档中没有相关信息，诚实告知
3. 回答时引用具体的文档内容
4. 保持回答简洁准确"""
)

# ============ 交互式问答演示 ============

print("=" * 70)
print("AgentScope RAG 问答系统")
print("=" * 70)
print("\n知识库包含以下文档:")
for i, title in enumerate(rag.doc_keys, 1):
    print(f"  {i}. {title}")
print(f"\n共 {len(DOCUMENTS)} 篇文档")
print("=" * 70)

# ============ 测试查询 ============

test_queries = [
    "AgentScope 是什么？",
    "ReActAgent 和 ChatAgent 有什么区别？",
    "如何使用工具调用功能？",
    "AgentScope 支持哪些工作流组件？"
]

for i, query in enumerate(test_queries, 1):
    print(f"\n[查询 {i}]")
    print(f"问题: {query}")
    print("-" * 70)

    # 检索相关文档
    retrieved = rag.retrieve(query, top_k=3)

    if retrieved:
        print("检索到相关文档:")
        for j, doc in enumerate(retrieved, 1):
            preview = doc[:80] + "..." if len(doc) > 80 else doc
            print(f"  文档{j}: {preview}")
    else:
        print("未找到相关文档")

    # 生成回答
    if retrieved:
        context = "\n\n".join([f"参考文档{j+1}: {doc}" for j, doc in enumerate(retrieved)])
        prompt = f"参考信息：\n{context}\n\n问题：{query}"
    else:
        prompt = query

    response = qa_agent(prompt)
    print(f"\n回答: {response}")

    print("=" * 70)
