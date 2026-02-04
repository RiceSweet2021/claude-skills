#!/usr/bin/env python3
"""generate.py - CLI for code generation

Usage:
    python generate.py "react agent with tools"
    python generate.py "memory management" --complexity minimal
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dynamic.generator import CodeGenerator
from dynamic.core import ComplexityLevel


def main():
    parser = argparse.ArgumentParser(description="Generate AgentScope code")
    parser.add_argument("query", help="Code generation query")
    parser.add_argument(
        "-c", "--complexity",
        choices=["minimal", "concise", "complete"],
        default="concise",
        help="Code complexity level"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path"
    )

    args = parser.parse_args()

    complexity = ComplexityLevel(args.complexity)
    generator = CodeGenerator()

    result = generator.generate(args.query, complexity)

    if result.validation and not result.is_valid():
        print(f"Error: {result.validation.message}", file=sys.stderr)
        if result.validation.error:
            print(f"  {result.validation.error}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result.code)
        print(f"Code written to {args.output}")
    else:
        print(result.code)


if __name__ == "__main__":
    main()
