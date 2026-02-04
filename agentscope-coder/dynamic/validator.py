"""Code validation module for agentscope-coder

Provides syntax check, safety scanning, and AgentScope convention validation.
"""

import ast
import re
import logging
from typing import Tuple, List, Optional, Dict

from .core import ValidationResult, ValidationStatus
from .errors import (
    SyntaxValidationError,
    SafetyValidationError,
    AgentScopeSyntaxError
)

logger = logging.getLogger(__name__)


class CodeValidator:
    """Validates generated AgentScope code with multiple checks"""

    # Unsafe operation patterns
    UNSAFE_PATTERNS = [
        (r'os\.system\s*\(', 'os.system'),
        (r'subprocess\.', 'subprocess'),
        (r'__import__\s*\(', '__import__'),
        (r'\beval\s*\(', 'eval'),
        (r'\bexec\s*\(', 'exec'),
        (r'compile\s*\(', 'compile'),
    ]

    # AgentScope required imports
    REQUIRED_AGENTSCOPE_IMPORTS = {
        'agentscope': 'import agentscope',
        'ChatAgent|ReActAgent|SubAgent': 'from agentscope.agents import ...',
    }

    def validate_syntax(self, code: str) -> bool:
        """
        Validate Python syntax

        Args:
            code: Python code string

        Returns:
            bool: True if syntax is correct

        Raises:
            SyntaxValidationError: When syntax error is found
        """
        try:
            ast.parse(code)
            logger.info("✅ Syntax validation passed")
            return True
        except SyntaxError as e:
            logger.error(f"❌ Syntax error: {e}")
            raise SyntaxValidationError(code, e)

    def validate_safety(self, code: str) -> Tuple[bool, List[str]]:
        """
        Check code for unsafe operations

        Args:
            code: Python code string

        Returns:
            Tuple[bool, List[str]]: (is_safe, list of unsafe patterns found)

        Raises:
            SafetyValidationError: When unsafe patterns are detected
        """
        unsafe_found = []

        for pattern, name in self.UNSAFE_PATTERNS:
            if re.search(pattern, code):
                unsafe_found.append(name)
                logger.warning(f"⚠️ Unsafe pattern detected: {name}")

        if unsafe_found:
            raise SafetyValidationError(code, unsafe_found)

        logger.info("✅ Safety validation passed")
        return True, []

    def validate_agentscope_conventions(self, code: str) -> bool:
        """
        Check if code follows AgentScope conventions

        Args:
            code: Python code string

        Returns:
            bool: True if conventions are followed

        Raises:
            AgentScopeSyntaxError: When conventions are violated
        """
        checks = [
            self._check_agentscope_import(code),
            self._check_initialization(code),
            self._check_type_hints(code),
        ]

        for is_valid, error_msg in checks:
            if not is_valid:
                raise AgentScopeSyntaxError(error_msg[0], error_msg[1])

        logger.info("✅ AgentScope conventions validation passed")
        return True

    def _check_agentscope_import(self, code: str) -> Tuple[bool, Optional[Tuple[str, str]]]:
        """Check if agentscope is properly imported"""
        if 'import agentscope' not in code:
            return False, (
                "Missing 'import agentscope'",
                "Add 'import agentscope' at the beginning"
            )
        return True, None

    def _check_initialization(self, code: str) -> Tuple[bool, Optional[Tuple[str, str]]]:
        """Check if agentscope.init() is called"""
        if 'agentscope.init' not in code:
            return False, (
                "Missing 'agentscope.init()' call",
                "Call agentscope.init() with proper model_configs"
            )
        return True, None

    def _check_type_hints(self, code: str) -> Tuple[bool, Optional[Tuple[str, str]]]:
        """Check if code includes type hints (warning only)"""
        # Simple check: at least one function should have type hints
        if re.search(r'def \w+\([^)]*:\s*\w+\)', code) or 'def main' in code:
            return True, None

        # Warning but not failure (many simple examples may not have type hints)
        logger.warning("⚠️ Recommend adding type hints for better code quality")
        return True, None

    def validate_complete(self, code: str) -> Dict:
        """
        Execute complete validation (three-tier validation)

        Args:
            code: Python code string

        Returns:
            dict: Validation result with all check statuses

        Example:
            >>> result = validator.validate_complete(code)
            >>> if result['is_valid']:
            >>>     print("Code is ready to use!")
        """
        result = {
            'is_valid': True,
            'checks': {},
            'errors': [],
            'warnings': []
        }

        # Check 1: Syntax
        try:
            self.validate_syntax(code)
            result['checks']['syntax'] = 'pass'
        except SyntaxValidationError as e:
            result['checks']['syntax'] = 'fail'
            result['errors'].append(str(e))
            result['is_valid'] = False
            return result  # Syntax error: return early, skip other checks

        # Check 2: Safety
        try:
            self.validate_safety(code)
            result['checks']['safety'] = 'pass'
        except SafetyValidationError as e:
            result['checks']['safety'] = 'fail'
            result['errors'].append(str(e))
            result['is_valid'] = False

        # Check 3: AgentScope conventions
        try:
            self.validate_agentscope_conventions(code)
            result['checks']['agentscope'] = 'pass'
        except AgentScopeSyntaxError as e:
            result['checks']['agentscope'] = 'fail'
            result['errors'].append(str(e))
            result['is_valid'] = False

        return result

    # Backward compatibility: keep old validate method
    def validate(self, code: str) -> ValidationResult:
        """
        Validate code syntax and safety (backward compatible method)

        Args:
            code: Python code string

        Returns:
            ValidationResult: Validation result
        """
        result = self.validate_complete(code)

        if result['is_valid']:
            return ValidationResult(
                status=ValidationStatus.PASSED,
                message="Code validated successfully"
            )

        return ValidationResult(
            status=ValidationStatus.FAILED,
            message="; ".join(result['errors']),
            error="; ".join(result['errors'])
        )
