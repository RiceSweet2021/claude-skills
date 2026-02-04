# AgentSkill 机制教程

## 核心概念

AgentSkill 是 AgentScope 中用于封装可复用功能的机制。与简单工具函数不同，Skill 是一个类，可以包含多个相关方法：

1. **面向对象**：以类的形式组织代码，支持状态管理
2. **可复用**：Skill 可以在不同 Agent 之间共享
3. **可发现**：Agent 可以自动发现 Skill 中的可用方法
4. **模块化**：相关功能组织在同一个 Skill 类中

AgentSkill 适合构建复杂的功能模块，如数据分析、文本处理等。

---

## 代码解析

### 知识点 1：定义 Skill 类

**核心代码：**
```python
from agentscope.skill import Skill

class CalculatorSkill(Skill):
    """计算器技能"""

    def add(self, a: float, b: float) -> float:
        """加法运算"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        return a - b
```

**解析：**

定义 Skill 的关键要点：

1. **继承 Skill**：必须继承 `agentscope.skill.Skill` 基类
2. **方法定义**：每个方法代表一个具体功能
3. **类型注解**：参数和返回值的类型注解帮助 Agent 理解用法
4. **文档字符串**：`"""..."""` 中的描述会被 Agent 读取

### 知识点 2：Skill 与工具函数的区别

| 特性 | 工具函数 | AgentSkill |
|------|---------|-----------|
| 形式 | 函数 | 类 |
| 状态管理 | ❌ 无状态 | ✅ 可有状态 |
| 方法数量 | 单一功能 | 多个相关方法 |
| 可发现性 | 需要手动注册 | 可自动发现方法 |
| 适用场景 | 简单操作 | 复杂功能模块 |

### 知识点 3：使用 Skill

**核心代码：**
```python
# 创建 Skill 实例
calc_skill = CalculatorSkill()

# 直接调用 Skill 方法
result = calc_skill.add(10, 5)

# 或通过 Agent 调用
agent = ChatAgent(
    name="assistant",
    model_config_name="qwen-max",
    skills=[calc_skill]  # 注册技能
)
```

**解析：**

Skill 的使用方式：

1. **独立使用**：直接实例化并调用方法
2. **Agent 集成**：通过 `skills` 参数注册到 Agent
3. **动态调用**：Agent 可以根据需要动态选择调用哪个方法

---

## 关键知识点总结

| 知识点 | 要点 |
|--------|------|
| Skill 定义 | 继承 Skill 基类，定义多个方法 |
| 与工具函数区别 | Skill 是类，支持状态和多方法 |
| 方法发现 | Agent 可以自动发现 Skill 中的方法 |
| 适用场景 | 复杂功能模块、需要状态管理 |

---

## 练习题

1. 创建一个 `DateTimeSkill`，包含格式化时间、计算时间差等方法
2. 实现一个带状态的 `CounterSkill`，记录调用次数
3. 尝试将一个自定义工具函数改造为 Skill
