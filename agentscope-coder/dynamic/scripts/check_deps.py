#!/usr/bin/env python3
"""check_deps.py - Check dependencies for dynamic generation

Returns exit code 0 if all dependencies are available.
"""

import sys
import os


def check_dashscope():
    """Check if dashscope is installed"""
    try:
        import dashscope
        return True
    except ImportError:
        return False


def check_api_key():
    """Check if API key is configured"""
    return bool(os.getenv('DASHSCOPE_API_KEY'))


def main():
    all_ok = True

    # Check dashscope
    if check_dashscope():
        print("✓ dashscope installed")
    else:
        print("✗ dashscope not installed (run: pip install dashscope)")
        all_ok = False

    # Check API key
    if check_api_key():
        print("✓ DASHSCOPE_API_KEY configured")
    else:
        print("✗ DASHSCOPE_API_KEY not set (LLM generation unavailable)")
        all_ok = False

    if all_ok:
        print("\nDynamic generation: ENABLED")
        return 0
    else:
        print("\nDynamic generation: DISABLED (static templates only)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
