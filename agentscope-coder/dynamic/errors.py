"""Custom exceptions for agentscope-coder"""


class CodeValidationError(Exception):
    """Base exception for code validation failures"""
    pass


class SyntaxValidationError(CodeValidationError):
    """Raised when code has syntax errors"""

    def __init__(self, code: str, error: SyntaxError):
        self.code = code
        self.error = error
        super().__init__(
            f"Syntax error: {error.msg}\n"
            f"Line {error.lineno}: {error.text}"
        )


class SafetyValidationError(CodeValidationError):
    """Raised when code contains unsafe operations"""

    def __init__(self, code: str, unsafe_patterns: list):
        self.code = code
        self.unsafe_patterns = unsafe_patterns
        super().__init__(
            f"Safety check failed. Unsafe patterns found: {unsafe_patterns}"
        )


class AgentScopeSyntaxError(CodeValidationError):
    """Raised when code doesn't follow AgentScope conventions"""

    def __init__(self, issue: str, suggestion: str = None):
        self.issue = issue
        self.suggestion = suggestion
        msg = f"AgentScope syntax issue: {issue}"
        if suggestion:
            msg += f"\nSuggestion: {suggestion}"
        super().__init__(msg)


class TemplateNotFoundError(Exception):
    """Raised when a template file is not found"""
    pass


class LLMGenerationError(Exception):
    """Raised when LLM generation fails"""
    pass


class ValidationTimeoutError(CodeValidationError):
    """Raised when validation takes too long"""
    pass
