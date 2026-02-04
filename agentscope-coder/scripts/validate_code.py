#!/usr/bin/env python3
"""Validate AgentScope code syntax and structure."""

import ast
import sys
from pathlib import Path


def validate_python_file(filepath: str) -> tuple[bool, str]:
    """Validate a Python file for syntax errors.

    Args:
        filepath: Path to the Python file

    Returns:
        (is_valid, error_message)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()

        ast.parse(code)
        return True, "Syntax valid"

    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def check_agentscope_imports(filepath: str) -> list[str]:
    """Check if file uses proper AgentScope imports.

    Args:
        filepath: Path to the Python file

    Returns:
        List of found AgentScope imports
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    imports = []
    agentscope_imports = [
        "agentscope",
        "agentscope.agents",
        "agentscope.memory",
        "agentscope.tools",
        "agentscope.pipelines",
        "agentscope.msghub",
    ]

    for imp in agentscope_imports:
        if imp in content:
            imports.append(imp)

    return imports


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_code.py <file.py>")
        sys.exit(1)

    filepath = sys.argv[1]

    # Syntax validation
    is_valid, msg = validate_python_file(filepath)
    print(f"Syntax: {msg}")

    # AgentScope imports
    imports = check_agentscope_imports(filepath)
    if imports:
        print(f"AgentScope imports: {', '.join(imports)}")
    else:
        print("Warning: No AgentScope imports found")

    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
