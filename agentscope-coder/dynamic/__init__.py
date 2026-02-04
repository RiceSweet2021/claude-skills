"""agentscope-coder dynamic module

Provides LLM-based code generation for AgentScope framework.
Designed for Claude Code usage - returns code only, no tutorial fluff.
"""

from .core import GeneratedCode, ComplexityLevel
from .generator import CodeGenerator

__all__ = ['GeneratedCode', 'ComplexityLevel', 'CodeGenerator']
__version__ = '1.0.0'
