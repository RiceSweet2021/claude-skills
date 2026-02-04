"""generator.py - Main code generator with progressive enhancement

Level 1: Static templates (no API needed)
Level 2: LLM generation (requires DASHSCOPE_API_KEY)
"""

import os
from typing import Optional
from .core import GeneratedCode, ComplexityLevel, ValidationResult, ValidationStatus
from .retriever import TemplateRetriever
from .parser import CodeParser
from .validator import CodeValidator


class CodeGenerator:
    """Progressive code generator for AgentScope"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize generator

        Args:
            api_key: DashScope API key (optional, for LLM generation)
        """
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        self.retriever = TemplateRetriever()
        self.parser = CodeParser()
        self.validator = CodeValidator()

    def has_llm(self) -> bool:
        """Check if LLM generation is available"""
        return bool(self.api_key)

    def generate(
        self,
        query: str,
        complexity: ComplexityLevel = ComplexityLevel.CONCISE
    ) -> GeneratedCode:
        """Generate code with progressive strategy

        Level 1: Try static template first
        Level 2: Fallback to LLM if configured
        """
        # Level 1: Static template
        template = self.retriever.match(query)
        if template:
            code = self.retriever.get_template_code(template.id, complexity.value)
            if code:
                return GeneratedCode(
                    code=code,
                    title=template.title,
                    complexity=complexity,
                    source="template",
                    validation=None  # Templates are pre-validated
                )

        # Level 2: LLM generation
        if self.has_llm():
            return self._generate_llm(query, complexity)

        # No template and no API
        return GeneratedCode(
            code="",
            title="Not Available",
            complexity=complexity,
            source="none",
            validation=ValidationResult(
                status=ValidationStatus.FAILED,
                message="No matching template and DASHSCOPE_API_KEY not configured",
                error="Configure API key or use different query"
            )
        )

    def _generate_llm(
        self,
        query: str,
        complexity: ComplexityLevel
    ) -> GeneratedCode:
        """Generate code using LLM"""
        try:
            from dashscope import Generation
        except ImportError:
            return GeneratedCode(
                code="",
                title="Not Available",
                complexity=complexity,
                source="llm",
                validation=ValidationResult(
                    status=ValidationStatus.FAILED,
                    message="DashScope not installed",
                    error="Run: pip install dashscope"
                )
            )

        # Build prompt
        prompt = self._build_prompt(query, complexity)

        # Call LLM
        try:
            response = Generation.call(
                model="qwen-max",
                api_key=self.api_key,
                prompt=prompt,
                temperature=0.7,
                result_format='text',
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.message}")

            # Parse response
            parsed, error = self.parser.parse(response.output.text)
            if not parsed:
                return GeneratedCode(
                    code="",
                    title="Generation Failed",
                    complexity=complexity,
                    source="llm",
                    validation=ValidationResult(
                        status=ValidationStatus.FAILED,
                        message="Failed to parse LLM response",
                        error=error
                    )
                )

            # Validate code
            validation = self.validator.validate(parsed.code)

            return GeneratedCode(
                code=parsed.code,
                title=parsed.title,
                complexity=complexity,
                source="llm",
                validation=validation
            )

        except Exception as e:
            return GeneratedCode(
                code="",
                title="Generation Failed",
                complexity=complexity,
                source="llm",
                validation=ValidationResult(
                    status=ValidationStatus.FAILED,
                    message=f"LLM generation failed",
                    error=str(e)
                )
            )

    def _build_prompt(self, query: str, complexity: ComplexityLevel) -> str:
        """Build LLM prompt for code generation"""
        complexity_guide = {
            ComplexityLevel.MINIMAL: "15-30 lines, core concept only",
            ComplexityLevel.CONCISE: "50-100 lines, complete runnable example",
            ComplexityLevel.COMPLETE: "100-200 lines, production-ready with error handling",
        }

        return f"""You are an AgentScope framework code generator.

Generate Python code for: {query}

Requirements:
- Use AgentScope standard API
- Code length: {complexity_guide[complexity]}
- Include necessary imports
- Add brief comments for key steps
- NO markdown formatting in code
- Use simple, clear naming

Return ONLY JSON format:
{{
  "title": "Code title",
  "code": "Complete Python code here"
}}

Do not include any explanation outside the JSON."""

    def list_templates(self) -> list:
        """List all available templates"""
        return list(self.retriever.templates.values())
