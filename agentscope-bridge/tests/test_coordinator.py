#!/usr/bin/env python3
"""Unit tests for coordinator.py"""

import sys
import os
import unittest

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from coordinator import (
    SkillCoordinator,
    Domain,
    CommanderSkill,
    WorkflowPhase,
    WorkflowContext,
    quick_analyze,
    recommend_workflow
)


class TestSkillCoordinator(unittest.TestCase):
    """Test cases for SkillCoordinator"""

    def setUp(self):
        """Set up test fixtures"""
        self.coordinator = SkillCoordinator()

    def test_identify_domain_agentscope(self):
        """Test domain identification for AgentScope queries"""
        queries = [
            "Create a ReActAgent",
            "How do I use ChatAgent?",
            "Build a multi-agent system",
            "Add memory to my agent",
            "Create a pipeline workflow",
        ]
        for query in queries:
            domain = self.coordinator.identify_domain(query)
            self.assertEqual(domain, Domain.AGENTSCOPE, f"Failed for: {query}")

    def test_identify_domain_skill_creation(self):
        """Test domain identification for skill creation queries"""
        queries = [
            "Create a new skill for code generation",
            "Make a skill that generates documentation",
            "Build a tutorial creator skill",
        ]
        for query in queries:
            domain = self.coordinator.identify_domain(query)
            self.assertEqual(domain, Domain.SKILL_CREATION, f"Failed for: {query}")

    def test_identify_domain_general(self):
        """Test domain identification for general queries"""
        queries = [
            "How do I write a for loop?",
            "Explain what a function is",
            "Help me debug this error",
        ]
        for query in queries:
            domain = self.coordinator.identify_domain(query)
            self.assertEqual(domain, Domain.GENERAL, f"Failed for: {query}")

    def test_classify_task_type_bug_fix(self):
        """Test task type classification for bug fixes"""
        queries = [
            "Fix the agent initialization error",
            "Debug this memory issue",
            "The code doesn't work",
        ]
        for query in queries:
            task_type = self.coordinator.classify_task_type(query)
            self.assertEqual(task_type, "bug_fix", f"Failed for: {query}")

    def test_classify_task_type_new_feature(self):
        """Test task type classification for new features"""
        queries = [
            "Implement a ReActAgent",
            "Add memory to the agent",
            "Create a multi-agent system",
        ]
        for query in queries:
            task_type = self.coordinator.classify_task_type(query)
            self.assertEqual(task_type, "new_feature", f"Failed for: {query}")

    def test_classify_task_type_exploration(self):
        """Test task type classification for exploration"""
        queries = [
            "How do I add tools?",
            "Explain how MsgHub works",
            "Where do I configure the model?",
        ]
        for query in queries:
            task_type = self.coordinator.classify_task_type(query)
            self.assertEqual(task_type, "exploration", f"Failed for: {query}")

    def test_select_workflow_new_feature(self):
        """Test workflow selection for new features"""
        workflow = self.coordinator.select_workflow(Domain.AGENTSCOPE, "new_feature")
        self.assertEqual(workflow["name"], "New Feature Development")
        self.assertEqual(len(workflow["phases"]), 4)
        self.assertIn(CommanderSkill.BRAINSTORMING, workflow["phases"])
        self.assertIn(CommanderSkill.PLANNING, workflow["phases"])

    def test_select_workflow_bug_fix(self):
        """Test workflow selection for bug fixes"""
        workflow = self.coordinator.select_workflow(Domain.AGENTSCOPE, "bug_fix")
        self.assertEqual(workflow["name"], "Bug Fix")
        self.assertEqual(len(workflow["phases"]), 3)
        self.assertIn(CommanderSkill.DEBUGGING, workflow["phases"])

    def test_create_context(self):
        """Test complete workflow context creation"""
        query = "Implement a ReActAgent with memory"
        ctx = self.coordinator.create_context(query)

        self.assertIsInstance(ctx, WorkflowContext)
        self.assertEqual(ctx.domain, Domain.AGENTSCOPE)
        self.assertEqual(ctx.user_query, query)
        self.assertIn("agentscope-coder", ctx.advisor_skills)

    def test_component_hints_extraction(self):
        """Test component hint extraction"""
        test_cases = [
            ("Create a ReActAgent", {"agent_type": "ReActAgent"}),
            ("Build a ChatAgent", {"agent_type": "ChatAgent"}),
            ("Agent with memory", {"has_memory": True}),
            ("Agent with tools", {"has_tools": True}),
            ("Multi-agent system", {"is_multi_agent": True}),
        ]

        for query, expected_hints in test_cases:
            hints = self.coordinator._extract_component_hints(query)
            for key, value in expected_hints.items():
                self.assertEqual(hints.get(key), value, f"Failed for {query}: {key}")

    def test_template_mapping(self):
        """Test template path mapping"""
        test_cases = [
            ({"agent_type": "ReActAgent"}, "templates/agents/react_agent/"),
            ({"agent_type": "ChatAgent"}, "templates/agents/basic_chat_agent/"),
            ({"has_memory": True, "agent_type": None}, "templates/memory/short_term_memory/"),
            ({"is_multi_agent": True}, "templates/advanced/multi_agent/"),
        ]

        for hints, expected_path in test_cases:
            path = self.coordinator._map_to_template(hints)
            self.assertEqual(path, expected_path)

    def test_advisor_guidance_agentscope(self):
        """Test advisor guidance for AgentScope domain"""
        guidance = self.coordinator.get_advisor_guidance(
            Domain.AGENTSCOPE,
            {"agent_type": "ReActAgent"}
        )
        self.assertEqual(guidance["skill"], "agentscope-coder")
        self.assertIn("react_agent", guidance["template_path"])

    def test_advisor_guidance_skill_creation(self):
        """Test advisor guidance for skill creation domain"""
        guidance = self.coordinator.get_advisor_guidance(
            Domain.SKILL_CREATION,
            {}
        )
        self.assertEqual(guidance["skill"], "skill-creator")

    def test_export_context_json(self):
        """Test context export as JSON"""
        ctx = self.coordinator.create_context("Create a ReActAgent")
        json_str = self.coordinator.export_context("Create a ReActAgent", format="json")
        self.assertIn("ReActAgent", json_str)
        self.assertIn("agentscope", json_str)

    def test_export_context_markdown(self):
        """Test context export as Markdown"""
        md_str = self.coordinator.export_context("Create a ReActAgent", format="markdown")
        self.assertIn("ReActAgent", md_str)
        self.assertIn("Workflow Recommendation", md_str)

    def test_quick_analyze(self):
        """Test quick analyze convenience function"""
        ctx = quick_analyze("Implement a ReActAgent with memory")
        self.assertIsInstance(ctx, WorkflowContext)
        self.assertEqual(ctx.domain, Domain.AGENTSCOPE)

    def test_recommend_workflow(self):
        """Test recommend workflow convenience function"""
        recommendation = recommend_workflow("Fix the bug")
        self.assertIn("Workflow Recommendation", recommendation)
        self.assertIn("Bug Fix", recommendation)


class TestWorkflowContext(unittest.TestCase):
    """Test cases for WorkflowContext"""

    def test_to_dict(self):
        """Test WorkflowContext serialization"""
        ctx = WorkflowContext(
            user_query="Create a ReActAgent",
            domain=Domain.AGENTSCOPE,
            workflow_name="New Feature Development",
            phases=[CommanderSkill.BRAINSTORMING, CommanderSkill.PLANNING],
            advisor_skills=["agentscope-coder"],
            metadata={"agent_type": "ReActAgent"}
        )

        result = ctx.to_dict()
        self.assertEqual(result["user_query"], "Create a ReActAgent")
        self.assertEqual(result["domain"], "agentscope")
        self.assertEqual(result["workflow"], "New Feature Development")
        self.assertIn("brainstorming", result["phases"])
        self.assertIn("agentscope-coder", result["advisors"])


if __name__ == '__main__':
    unittest.main()
