#!/usr/bin/env python3
"""test_integration.py - Integration test for agentscope-coder"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from dynamic.generator import CodeGenerator
from dynamic.core import ComplexityLevel


def test_template_retrieval():
    """Test static template retrieval"""
    generator = CodeGenerator()

    result = generator.generate("react agent with tools", ComplexityLevel.CONCISE)

    assert result.source == "template", f"Expected template source, got {result.source}"
    assert len(result.code) > 0, "Code should not be empty"
    assert "ReActAgent" in result.code or "react" in result.code.lower(), "Code should mention ReActAgent"

    print("✓ Template retrieval works")
    return True


def test_llm_fallback():
    """Test LLM fallback when no template matches"""
    generator = CodeGenerator()

    # Use a query that won't match any template
    result = generator.generate("xyzabc123 nonexistent template", ComplexityLevel.MINIMAL)

    if generator.has_llm():
        assert result.source == "llm", f"Expected llm source, got {result.source}"
        print("✓ LLM generation works")
    else:
        assert result.source == "none", f"Expected none source, got {result.source}"
        print("✓ Graceful fallback without API key")

    return True


def test_list_templates():
    """Test template listing"""
    generator = CodeGenerator()
    templates = generator.list_templates()

    assert len(templates) == 12, f"Expected 12 templates, got {len(templates)}"

    print(f"✓ Found {len(templates)} templates")
    return True


def main():
    tests = [
        ("Template Retrieval", test_template_retrieval),
        ("LLM Fallback", test_llm_fallback),
        ("List Templates", test_list_templates),
    ]

    print("Running agentscope-coder integration tests...\n")

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"✗ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
