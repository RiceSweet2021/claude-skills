"""parser.py - LLM response parser for code extraction

Simplified version - extracts code only, no tutorial fields.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class ParsedCode:
    """Parsed code from LLM response"""
    code: str
    title: str
    parse_strategy: str


class CodeParser:
    """Parse LLM response to extract code"""

    def parse(self, response: str) -> Tuple[Optional[ParsedCode], Optional[str]]:
        """Parse response, return (code, error)"""
        # Strategy 1: JSON in markdown
        result, error = self._parse_json_markdown(response)
        if result:
            return result, None

        # Strategy 2: Direct JSON
        result, error = self._parse_direct_json(response)
        if result:
            return result, None

        # Strategy 3: Python code block
        result, error = self._parse_python_block(response)
        if result:
            return result, None

        return None, "Failed to extract code from response"

    def _parse_json_markdown(self, response: str) -> Tuple[Optional[ParsedCode], Optional[str]]:
        """Parse ```json...``` blocks"""
        pattern = r'```json\s*([\s\S]*?)\s*```'
        matches = re.findall(pattern, response)

        for match in matches:
            try:
                data = json.loads(match.strip())
                if 'code' in data:
                    return ParsedCode(
                        code=data['code'],
                        title=data.get('title', 'Generated Code'),
                        parse_strategy='json_markdown'
                    ), None
            except json.JSONDecodeError:
                continue
        return None, None

    def _parse_direct_json(self, response: str) -> Tuple[Optional[ParsedCode], Optional[str]]:
        """Parse direct JSON response"""
        try:
            data = json.loads(response.strip())
            if 'code' in data:
                return ParsedCode(
                    code=data['code'],
                    title=data.get('title', 'Generated Code'),
                    parse_strategy='direct_json'
                ), None
        except json.JSONDecodeError:
            pass

        # Find JSON boundaries
        first, last = response.find('{'), response.rfind('}')
        if first != -1 and last > first:
            try:
                data = json.loads(response[first:last+1])
                if 'code' in data:
                    return ParsedCode(
                        code=data['code'],
                        title=data.get('title', 'Generated Code'),
                        parse_strategy='json_extracted'
                    ), None
            except json.JSONDecodeError:
                pass
        return None, None

    def _parse_python_block(self, response: str) -> Tuple[Optional[ParsedCode], Optional[str]]:
        """Parse ```python...``` blocks"""
        pattern = r'```python\s*([\s\S]*?)\s*```'
        matches = re.findall(pattern, response)

        if not matches:
            pattern = r'```\s*([\s\S]*?)\s*```'
            matches = re.findall(pattern, response)

        for match in matches:
            code = match.strip()
            if code and len(code) > 10:
                title = self._extract_title(response)
                return ParsedCode(
                    code=code,
                    title=title,
                    parse_strategy='python_block'
                ), None
        return None, None

    def _extract_title(self, response: str) -> str:
        """Extract title from response"""
        # Try markdown heading
        m = re.search(r'^#\s+(.+)$', response, re.MULTILINE)
        if m:
            return m.group(1).strip()

        # Try title field
        m = re.search(r'title[：:]\s*(.+)', response, re.IGNORECASE)
        if m:
            return m.group(1).strip()

        return 'Generated Code'
