#!/usr/bin/env python3
"""Unit tests for validator.py"""

import sys
import os
import unittest

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

from dynamic.validator import CodeValidator
from dynamic.errors import (
    SyntaxValidationError,
    SafetyValidationError,
    AgentScopeSyntaxError
)


class TestCodeValidator(unittest.TestCase):
    """Test cases for CodeValidator"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = CodeValidator()

    def test_syntax_valid_code(self):
        """Test validation of valid Python code"""
        code = """
import agentscope
from agentscope.agents import ChatAgent

agentscope.init(model_configs="./model_config.json")
agent = ChatAgent(name="assistant")
"""
        result = self.validator.validate_syntax(code)
        self.assertTrue(result)

    def test_syntax_invalid_code(self):
        """Test validation of invalid Python code"""
        code = "def foo(\n"  # Invalid syntax
        with self.assertRaises(SyntaxValidationError):
            self.validator.validate_syntax(code)

    def test_safety_safe_code(self):
        """Test safety check passes for safe code"""
        code = """
import agentscope
from agentscope.agents import ChatAgent

agent = ChatAgent(name="assistant")
response = agent("Hello")
"""
        is_safe, patterns = self.validator.validate_safety(code)
        self.assertTrue(is_safe)
        self.assertEqual(len(patterns), 0)

    def test_safety_unsafe_code(self):
        """Test safety check fails for unsafe code"""
        code = "import os; os.system('rm -rf /')"
        with self.assertRaises(SafetyValidationError):
            self.validator.validate_safety(code)

    def test_safety_detects_eval(self):
        """Test safety check detects eval"""
        code = "result = eval(user_input)"
        with self.assertRaises(SafetyValidationError):
            self.validator.validate_safety(code)

    def test_agentscope_conventions_valid(self):
        """Test AgentScope conventions pass"""
        code = """
import agentscope
from agentscope.agents import ChatAgent

agentscope.init(model_configs="./model_config.json")
agent = ChatAgent(name="assistant")
"""
        result = self.validator.validate_agentscope_conventions(code)
        self.assertTrue(result)

    def test_agentscope_missing_import(self):
        """Test AgentScope conventions fail without import"""
        code = """
from agentscope.agents import ChatAgent

agentscope.init(model_configs="./model_config.json")
agent = ChatAgent(name="assistant")
"""
        with self.assertRaises(AgentScopeSyntaxError) as context:
            self.validator.validate_agentscope_conventions(code)
        self.assertIn("import agentscope", str(context.exception))

    def test_agentscope_missing_init(self):
        """Test AgentScope conventions fail without init"""
        code = """
import agentscope
from agentscope.agents import ChatAgent

agent = ChatAgent(name="assistant")
"""
        with self.assertRaises(AgentScopeSyntaxError) as context:
            self.validator.validate_agentscope_conventions(code)
        self.assertIn("agentscope.init", str(context.exception))

    def test_validate_complete_all_pass(self):
        """Test complete validation with all checks passing"""
        code = """
import agentscope
from agentscope.agents import ChatAgent

agentscope.init(model_configs="./model_config.json")
agent = ChatAgent(name="assistant")
"""
        result = self.validator.validate_complete(code)
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['checks']['syntax'], 'pass')
        self.assertEqual(result['checks']['safety'], 'pass')
        self.assertEqual(result['checks']['agentscope'], 'pass')
        self.assertEqual(len(result['errors']), 0)

    def test_validate_complete_syntax_fail(self):
        """Test complete validation fails on syntax error"""
        code = "def foo(\n"
        result = self.validator.validate_complete(code)
        self.assertFalse(result['is_valid'])
        self.assertEqual(result['checks']['syntax'], 'fail')
        # Safety and agentscope should not be checked if syntax fails
        self.assertNotIn('safety', result['checks'])

    def test_validate_complete_safety_fail(self):
        """Test complete validation fails on safety error"""
        code = """
import agentscope
from agentscope.agents import ChatAgent
import os
os.system('ls')
"""
        result = self.validator.validate_complete(code)
        self.assertFalse(result['is_valid'])
        self.assertEqual(result['checks']['syntax'], 'pass')
        self.assertEqual(result['checks']['safety'], 'fail')

    def test_validate_backward_compatibility(self):
        """Test backward compatible validate method"""
        code = """
import agentscope
from agentscope.agents import ChatAgent

agentscope.init(model_configs="./model_config.json")
agent = ChatAgent(name="assistant")
"""
        result = self.validator.validate(code)
        self.assertTrue(hasattr(result, 'status'))
        self.assertEqual(str(result.status), 'ValidationStatus.PASSED')


if __name__ == '__main__':
    unittest.main()
