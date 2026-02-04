"""validator.py - Code validation for generated code

Provides syntax check and dangerous function scanning.
"""

import ast
import re
from typing import Optional
from .core import ValidationResult, ValidationStatus


class CodeValidator:
    """Validate generated code"""

    FORBIDDEN_PATTERNS = {
        'os.system',
        'subprocess.call',
        'subprocess.run',
        'subprocess.Popen',
        'eval(',
        'exec(',
        'os.remove',
        'os.unlink',
        'shutil.rmtree',
    }

    def validate(self, code: str) -> ValidationResult:
        """Validate code syntax and safety"""
        # Check syntax
        syntax_ok, syntax_error = self._check_syntax(code)
        if not syntax_ok:
            return ValidationResult(
                status=ValidationStatus.FAILED,
                message="Syntax error",
                error=syntax_error
            )

        # Check dangerous functions
        safety_ok, safety_error = self._check_safety(code)
        if not safety_ok:
            return ValidationResult(
                status=ValidationStatus.FAILED,
                message="Unsafe code detected",
                error=safety_error
            )

        return ValidationResult(
            status=ValidationStatus.PASSED,
            message="Code validated"
        )

    def _check_syntax(self, code: str) -> tuple[bool, Optional[str]]:
        """Check Python syntax"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"

    def _check_safety(self, code: str) -> tuple[bool, Optional[str]]:
        """Check for dangerous function calls"""
        found = []
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in code:
                found.append(pattern)

        if found:
            return False, f"Found: {', '.join(found)}"
        return True, None
