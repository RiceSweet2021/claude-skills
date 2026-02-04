"""AgentScope Bridge Coordinator

Implements the "Commander + Advisor" architecture for coordinating
AgentScope development workflows.

Usage:
    from coordinator import SkillCoordinator, Domain, CommanderSkill

    coordinator = SkillCoordinator()
    domain = coordinator.identify_domain("Create a ReActAgent")
    workflow = coordinator.select_workflow(domain, is_new_feature=True)
"""

import re
import logging
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class Domain(Enum):
    """Domain types for skill routing"""
    AGENTSCOPE = "agentscope"
    SKILL_CREATION = "skill_creation"
    GENERAL = "general"


class CommanderSkill(Enum):
    """Superpowers sub-skills (Commander level)"""
    BRAINSTORMING = "brainstorming"
    TDD = "test-driven-development"
    DEBUGGING = "systematic-debugging"
    PLANNING = "writing-plans"
    EXECUTION = "subagent-driven-development"
    VERIFICATION = "verification-before-completion"
    DISPATCHING = "dispatching-parallel-agents"
    FINISHING = "finishing-a-development-branch"


class WorkflowPhase(Enum):
    """Development workflow phases"""
    DISCOVERY = "discovery"      # Understand requirements
    PLANNING = "planning"        # Create implementation plan
    EXECUTION = "execution"      # Implement
    VERIFICATION = "verification"  # Test and verify


@dataclass
class WorkflowContext:
    """Context for workflow coordination"""
    user_query: str
    domain: Domain
    workflow_name: str
    phases: List[CommanderSkill]
    advisor_skills: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for logging/debugging"""
        return {
            "user_query": self.user_query,
            "domain": self.domain.value,
            "workflow": self.workflow_name,
            "phases": [p.value for p in self.phases],
            "advisors": self.advisor_skills,
            "metadata": self.metadata
        }


class SkillCoordinator:
    """Coordinates skill invocation following Commander + Advisor architecture"""

    # Domain keyword patterns
    DOMAIN_PATTERNS = {
        Domain.AGENTSCOPE: [
            r'\bReActAgent\b',
            r'\bChatAgent\b',
            r'\bSubAgent\b',
            r'\bMsgHub\b',
            r'\bPipeline\b',
            r'\bmsghub\b',
            r'\bagent\b.*\bmemory\b',
            r'\bmemory\b.*\bagent\b',
            r'\bagent\b.*\btool\b',
            r'\btool\b.*\bagent\b',
            r'\bagent\b.*\bworkflow\b',
            r'\bworkflow\b.*\bagent\b',
            r'\bmulti[-\s]?agent\b',
            r'\bstreaming\b',
            r'\bRAG\b',
            r'\bretrieval.*augmented\b',
            r'\bAgentScope\b',
            r'\bagscope\b',
        ],
        Domain.SKILL_CREATION: [
            r'\bskill\b.*\b(create|make|build|generate)\b',
            r'\b(create|make|build|generate)\b.*\bskill\b',
            r'\bnew skill\b',
            r'\bskill[-\s]?creator\b',
        ]
    }

    # Workflow templates
    WORKFLOWS = {
        "new_feature": {
            "name": "New Feature Development",
            "phases": [
                CommanderSkill.BRAINSTORMING,
                CommanderSkill.PLANNING,
                CommanderSkill.EXECUTION,
                CommanderSkill.VERIFICATION,
            ],
            "advisor_map": {
                Domain.AGENTSCOPE: ["agentscope-coder"],
                Domain.SKILL_CREATION: ["skill-creator"],
            }
        },
        "bug_fix": {
            "name": "Bug Fix",
            "phases": [
                CommanderSkill.DEBUGGING,
                CommanderSkill.EXECUTION,
                CommanderSkill.VERIFICATION,
            ],
            "advisor_map": {
                Domain.AGENTSCOPE: ["agentscope-coder"],
                Domain.SKILL_CREATION: ["skill-creator"],
            }
        },
        "refactor": {
            "name": "Refactoring",
            "phases": [
                CommanderSkill.BRAINSTORMING,
                CommanderSkill.PLANNING,
                CommanderSkill.EXECUTION,
                CommanderSkill.VERIFICATION,
            ],
            "advisor_map": {
                Domain.AGENTSCOPE: ["agentscope-coder"],
            }
        },
        "exploration": {
            "name": "Code Exploration",
            "phases": [
                CommanderSkill.BRAINSTORMING,
            ],
            "advisor_map": {
                Domain.AGENTSCOPE: ["agentscope-coder"],
            }
        },
        "test_dev": {
            "name": "Test-Driven Development",
            "phases": [
                CommanderSkill.TDD,
                CommanderSkill.VERIFICATION,
            ],
            "advisor_map": {
                Domain.AGENTSCOPE: ["agentscope-coder"],
            }
        }
    }

    def __init__(self, log_level: int = logging.INFO):
        """Initialize the coordinator

        Args:
            log_level: Logging level (default: INFO)
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def identify_domain(self, query: str) -> Domain:
        """Identify the domain based on user query

        Args:
            query: User's request text

        Returns:
            Domain: Identified domain (AGENTSCOPE, SKILL_CREATION, or GENERAL)
        """
        query_lower = query.lower()

        # Check AgentScope patterns
        if any(re.search(pattern, query, re.IGNORECASE)
               for pattern in self.DOMAIN_PATTERNS[Domain.AGENTSCOPE]):
            logger.info(f"Identified domain: AGENTSCOPE")
            return Domain.AGENTSCOPE

        # Check Skill Creation patterns
        if any(re.search(pattern, query, re.IGNORECASE)
               for pattern in self.DOMAIN_PATTERNS[Domain.SKILL_CREATION]):
            logger.info(f"Identified domain: SKILL_CREATION")
            return Domain.SKILL_CREATION

        logger.info(f"Identified domain: GENERAL")
        return Domain.GENERAL

    def classify_task_type(self, query: str) -> str:
        """Classify the type of task (new_feature, bug_fix, refactor, etc.)

        Args:
            query: User's request text

        Returns:
            str: Task type key (maps to WORKFLOWS)
        """
        query_lower = query.lower()

        # Bug fix indicators
        bug_patterns = [r'\bfix\b', r'\bbug\b', r'\berror\b', r'\bissue\b',
                       r'\bdebug\b', r'\bnot work\b', r'\bdoesn\'t work\b',
                       r'\bfailed\b', r'\bexception\b', r'\bproblem\b']
        if any(re.search(p, query, re.IGNORECASE) for p in bug_patterns):
            return "bug_fix"

        # Test/verification indicators
        test_patterns = [r'\btest\b', r'\btdd\b', r'\bverify\b', r'\bcheck\b']
        if any(re.search(p, query, re.IGNORECASE) for p in test_patterns):
            return "test_dev"

        # Refactoring indicators
        refactor_patterns = [r'\brefactor\b', r'\brestructure\b', r'\bclean\b',
                            r'\breorganize\b', r'\boptimize\b']
        if any(re.search(p, query, re.IGNORECASE) for p in refactor_patterns):
            return "refactor"

        # Exploration/understanding indicators
        explore_patterns = [r'\bexplain\b', r'\bunderstand\b', r'\bhow (do|to|can)\b',
                           r'\bwhat (is|are|does)\b', r'\bwhere\b', r'\bfind\b',
                           r'\blocate\b', r'\bshow\b', r'\bdemonstrate\b']
        if any(re.search(p, query, re.IGNORECASE) for p in explore_patterns):
            return "exploration"

        # Default: new feature
        return "new_feature"

    def select_workflow(self, domain: Domain, task_type: str = None,
                       query: str = None) -> Dict[str, Any]:
        """Select the appropriate workflow

        Args:
            domain: Identified domain
            task_type: Task type (if already classified)
            query: User query (for auto-classification if task_type not provided)

        Returns:
            dict: Workflow configuration with phases and advisor skills
        """
        if task_type is None and query:
            task_type = self.classify_task_type(query)

        workflow = self.WORKFLOWS.get(task_type, self.WORKFLOWS["new_feature"])

        # Get advisor skills for this domain
        advisor_skills = workflow["advisor_map"].get(domain, [])

        return {
            "name": workflow["name"],
            "task_type": task_type,
            "phases": workflow["phases"],
            "advisor_skills": advisor_skills,
        }

    def create_context(self, query: str) -> WorkflowContext:
        """Create a complete workflow context for a user query

        Args:
            query: User's request text

        Returns:
            WorkflowContext: Complete context with domain, workflow, and skills

        Example:
            >>> ctx = coordinator.create_context("Implement a ReActAgent with memory")
            >>> print(ctx.domain)
            Domain.AGENTSCOPE
            >>> print(ctx.workflow_name)
            'New Feature Development'
            >>> print(ctx.advisor_skills)
            ['agentscope-coder']
        """
        domain = self.identify_domain(query)
        task_type = self.classify_task_type(query)
        workflow = self.select_workflow(domain, task_type)

        # Extract component hints from query
        component_hints = self._extract_component_hints(query)

        return WorkflowContext(
            user_query=query,
            domain=domain,
            workflow_name=workflow["name"],
            phases=workflow["phases"],
            advisor_skills=workflow["advisor_skills"],
            metadata={
                "task_type": task_type,
                "component_hints": component_hints,
            }
        )

    def _extract_component_hints(self, query: str) -> Dict[str, str]:
        """Extract AgentScope component hints from query

        Args:
            query: User's request text

        Returns:
            dict: Component type hints (agent_type, has_memory, etc.)
        """
        hints = {
            "agent_type": None,
            "has_memory": False,
            "has_tools": False,
            "is_multi_agent": False,
            "has_workflow": False,
        }

        query_lower = query.lower()

        # Agent type
        if "react" in query_lower:
            hints["agent_type"] = "ReActAgent"
        elif "chat" in query_lower:
            hints["agent_type"] = "ChatAgent"
        elif "subagent" in query_lower or "sub agent" in query_lower:
            hints["agent_type"] = "SubAgent"

        # Features
        hints["has_memory"] = bool(re.search(r'\bmemory\b', query_lower))
        hints["has_tools"] = bool(re.search(r'\btools?\b', query_lower))
        hints["is_multi_agent"] = bool(re.search(r'\bmulti[-\s]?agent\b', query_lower))
        hints["has_workflow"] = bool(
            re.search(r'\bworkflow\b|\bpipeline\b|\bmsghub\b', query_lower)
        )

        return hints

    def get_advisor_guidance(self, domain: Domain,
                            component_hints: Dict[str, str]) -> Dict[str, str]:
        """Get guidance on which advisor to call and with what parameters

        Args:
            domain: Identified domain
            component_hints: Component type hints from query

        Returns:
            dict: Advisor guidance with skill name and suggested parameters
        """
        if domain == Domain.AGENTSCOPE:
            advisor = "agentscope-coder"
            # Map to template path
            template_path = self._map_to_template(component_hints)
            return {
                "skill": advisor,
                "template_path": template_path,
                "reason": f"AgentScope component development: {component_hints.get('agent_type', 'general')}"
            }

        elif domain == Domain.SKILL_CREATION:
            return {
                "skill": "skill-creator",
                "reason": "New skill creation or modification"
            }

        else:
            return {
                "skill": None,
                "reason": "General task, no specific advisor needed"
            }

    def _map_to_template(self, hints: Dict[str, str]) -> Optional[str]:
        """Map component hints to agentscope-coder template path

        Args:
            hints: Component type hints

        Returns:
            str: Template path (e.g., "templates/agents/react_agent/")
        """
        agent_type = hints.get("agent_type")

        if agent_type == "ReActAgent":
            return "templates/agents/react_agent/"
        elif agent_type == "ChatAgent":
            return "templates/agents/basic_chat_agent/"
        elif agent_type == "SubAgent":
            return "templates/agents/subagent/"
        elif hints.get("has_memory"):
            return "templates/memory/short_term_memory/"
        elif hints.get("has_tools"):
            return "templates/tools/custom_tool/"
        elif hints.get("is_multi_agent"):
            return "templates/advanced/multi_agent/"
        elif hints.get("has_workflow"):
            if "msghub" in str(hints).lower():
                return "templates/workflows/msg_hub/"
            else:
                return "templates/workflows/sequential_pipeline/"

        return None

    def generate_recommendation(self, query: str) -> str:
        """Generate a human-readable workflow recommendation

        Args:
            query: User's request text

        Returns:
            str: Formatted recommendation
        """
        ctx = self.create_context(query)

        lines = [
            "## Workflow Recommendation",
            "",
            f"**Domain:** {ctx.domain.value}",
            f"**Workflow:** {ctx.workflow_name}",
            "",
            "### Phases:",
        ]

        for i, phase in enumerate(ctx.phases, 1):
            lines.append(f"{i}. `superpowers:{phase.value}`")

        if ctx.advisor_skills:
            lines.append("")
            lines.append("### Advisor Skills:")
            for skill in ctx.advisor_skills:
                guidance = self.get_advisor_guidance(ctx.domain, ctx.metadata.get("component_hints", {}))
                lines.append(f"- `{skill}`: {guidance.get('reason', 'Domain knowledge')}")

        if ctx.metadata.get("component_hints"):
            hints = ctx.metadata["component_hints"]
            lines.append("")
            lines.append("### Detected Components:")
            for key, value in hints.items():
                if value:
                    lines.append(f"- {key}: {value}")

        return "\n".join(lines)

    def export_context(self, query: str, format: str = "json") -> str:
        """Export workflow context for debugging or external use

        Args:
            query: User's request text
            format: Export format ("json" or "markdown")

        Returns:
            str: Serialized context
        """
        ctx = self.create_context(query)

        if format == "json":
            return json.dumps(ctx.to_dict(), indent=2)

        elif format == "markdown":
            return self.generate_recommendation(query)

        else:
            raise ValueError(f"Unsupported format: {format}")


# CLI convenience functions
def quick_analyze(query: str) -> WorkflowContext:
    """Quick analysis of a query

    Args:
        query: User's request text

    Returns:
        WorkflowContext: Analysis result
    """
    coordinator = SkillCoordinator()
    return coordinator.create_context(query)


def recommend_workflow(query: str) -> str:
    """Get workflow recommendation for a query

    Args:
        query: User's request text

    Returns:
        str: Formatted recommendation
    """
    coordinator = SkillCoordinator()
    return coordinator.generate_recommendation(query)


if __name__ == "__main__":
    # Demo: analyze sample queries
    sample_queries = [
        "Implement a ReActAgent with memory",
        "Fix the agent initialization error",
        "Create a new skill for code generation",
        "How do I add tools to my agent?",
        "Build a multi-agent discussion system",
    ]

    coordinator = SkillCoordinator()

    print("=" * 60)
    print("AgentScope Bridge Coordinator - Demo")
    print("=" * 60)

    for query in sample_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("=" * 60)
        print(coordinator.generate_recommendation(query))
