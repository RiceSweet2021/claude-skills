"""core.py - Simplified data models for code generation

Designed for Claude Code - returns code only, no tutorial content.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ComplexityLevel(Enum):
    """Code complexity levels"""
    MINIMAL = "minimal"      # 15-30 lines
    CONCISE = "concise"      # 50-100 lines
    COMPLETE = "complete"    # 100-200 lines


class ValidationStatus(Enum):
    """Code validation status"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ValidationResult:
    """Code validation result"""
    status: ValidationStatus
    message: str
    error: Optional[str] = None


@dataclass
class GeneratedCode:
    """Generated code result - simplified for Claude Code

    Attributes:
        code: Generated Python code
        title: Code title
        complexity: Complexity level used
        source: Source (template/llm)
        validation: Validation result
    """
    code: str
    title: str
    complexity: ComplexityLevel
    source: str  # "template" or "llm"
    validation: Optional[ValidationResult] = None

    def is_valid(self) -> bool:
        """Check if code is valid"""
        if self.validation is None:
            return True
        return self.validation.status == ValidationStatus.PASSED
