"""长期记忆完整示例

生产级长期记忆实现，包含持久化存储和向量检索。
"""

import agentscope
from agentscope.memory import LongTermMemory
from agentscope.agents import DialogAgent
from agentscope.models import read_model_config
from typing import Optional, Dict, Any, List
import logging
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersistentLongTermMemory:
    """持久化长期记忆封装类

    提供记忆的保存和加载功能，支持跨会话记忆。
    """

    def __init__(
        self,
        name: str = "persistent_memory",
        storage_path: str = "./memory_storage",
        embedding_model: str = "text-embedding-ada-002"
    ):
        """初始化持久化记忆

        Args:
            name: 记忆名称
            storage_path: 存储路径
            embedding_model: 向量嵌入模型
        """
        self.name = name
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # 创建底层 LongTermMemory
        self.memory = LongTermMemory(
            name=name,
            embedding_model=embedding_model
        )

        # 尝试加载已保存的记忆
        self._load_memory()

    def _load_memory(self) -> bool:
        """从文件加载记忆

        Returns:
            是否成功加载
        """
        memory_file = self.storage_path / f"{self.name}.json"
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 恢复记忆片段
                    for fragment_data in data.get('fragments', []):
                        self.memory.add(
                            content=fragment_data['content'],
                            embedding=fragment_data.get('embedding')
                        )
                logger.info(f"成功从 {memory_file} 加载记忆")
                return True
            except Exception as e:
                logger.warning(f"加载记忆失败: {e}")
        return False

    def save_memory(self) -> bool:
        """保存记忆到文件

        Returns:
            是否成功保存
        """
        memory_file = self.storage_path / f"{self.name}.json"
        try:
            # 准备保存的数据
            data = {
                'name': self.name,
                'fragments': [
                    {
                        'content': frag.content,
                        'embedding': frag.embedding
                    }
                    for frag in self.memory.memory
                ]
            }

            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"记忆已保存到 {memory_file}")
            return True
        except Exception as e:
            logger.error(f"保存记忆失败: {e}")
            return False

    def get_memory(self) -> LongTermMemory:
        """获取底层记忆对象

        Returns:
            LongTermMemory 实例
        """
        return self.memory

    def get_summary(self) -> Dict[str, Any]:
        """获取记忆摘要信息

        Returns:
            记忆摘要字典
        """
        return {
            'name': self.name,
            'fragment_count': len(self.memory.memory),
            'storage_path': str(self.storage_path),
        }


def create_memory_agent(
    memory_name: str = "user_memory",
    system_prompt: Optional[str] = None
) -> DialogAgent:
    """创建带持久化记忆的 Agent

    Args:
        memory_name: 记忆名称
        system_prompt: 系统提示词

    Returns:
        配置好的 DialogAgent
    """
    # 创建持久化记忆
    persistent_memory = PersistentLongTermMemory(name=memory_name)

    # 默认系统提示词
    if system_prompt is None:
        system_prompt = (
            "你是一个专业的个人助理。"
            "请记住对话中的重要信息，"
            "包括用户的姓名、偏好、兴趣等。"
            "在后续对话中，主动运用这些记忆提供个性化服务。"
        )

    # 创建 Agent
    agent = DialogAgent(
        name="memory_assistant",
        model_config_name="qwen-max",
        memory=persistent_memory.get_memory(),
        system_prompt=system_prompt
    )

    return agent, persistent_memory


def demo_conversation(agent: DialogAgent, rounds: int = 3) -> List[Dict[str, str]]:
    """演示对话流程

    Args:
        agent: DialogAgent 实例
        rounds: 对话轮数

    Returns:
        对话历史列表
    """
    conversation_history = []

    # 示例对话脚本
    scripts = [
        "你好，我是王芳，是一名产品经理",
        "我最喜欢的运动是游泳，每周去三次",
        "我最近在学习数据分析，主要用 Python",
        "",  # 触发记忆测试
        "请帮我总结一下我的信息",
    ]

    print("=" * 70)
    print("对话演示")
    print("=" * 70)

    for i, query in enumerate(scripts, 1):
        if not query:
            # 测试记忆
            print(f"\n--- 记忆测试 ---")
            test_queries = [
                "我叫什么名字？",
                "我的职业是什么？",
                "我喜欢什么运动？",
            ]
            for test_q in test_queries:
                print(f"\n用户: {test_q}")
                response = agent(test_q)
                print(f"助理: {response}")
                conversation_history.append({
                    'user': test_q,
                    'assistant': response
                })
        else:
            print(f"\n[第 {i} 轮]")
            print(f"用户: {query}")
            response = agent(query)
            print(f"助理: {response}")
            conversation_history.append({
                'user': query,
                'assistant': response
            })

    return conversation_history


def main():
    """主函数"""
    # 初始化 AgentScope
    try:
        agentscope.init(model_configs="./model_config.json")
    except Exception as e:
        logger.error(f"初始化失败: {e}")
        logger.info("提示：请确保 model_config.json 文件存在且配置正确")
        return

    # 创建带记忆的 Agent
    agent, persistent_memory = create_memory_agent()

    # 显示记忆摘要
    summary = persistent_memory.get_summary()
    print(f"\n记忆摘要: {summary}")

    # 运行对话演示
    demo_conversation(agent)

    # 保存记忆
    print("\n" + "=" * 70)
    persistent_memory.save_memory()

    # 最终摘要
    final_summary = persistent_memory.get_summary()
    print(f"最终记忆状态: {final_summary}")


if __name__ == "__main__":
    main()
