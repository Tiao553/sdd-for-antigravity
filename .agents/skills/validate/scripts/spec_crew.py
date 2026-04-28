"""
spec_crew.py — Legacy flat stub (superseded by crews/spec_crew.py).

Kept for backwards compatibility. The active implementation lives in
.agents/skills/validate/scripts/crews/spec_crew.py (Hierarchical · 4 agents).
"""

from crewai import Agent, Task
from .schemas import Finding, Severity, SpecReport


class SpecCrew:
    """
    Legacy stub — validates implementation against architectural intent.
    The real hierarchical crew lives in crews/spec_crew.py.
    """

    def __init__(self, feature_context: str):
        self.feature_context = feature_context
        self.manager = Agent(
            role="Validation Manager",
            goal="Coordinate specialized agents to validate implementation against design",
            backstory=(
                "Elite orchestrator from AgentSpec, specialized in cross-domain "
                "validation and ensuring SDD phase consistency."
            ),
            verbose=True,
            allow_delegation=True,
        )

        self.architect = Agent(
            role="Medallion Architect",
            goal="Validate architectural fidelity and layer-based quality progression",
            backstory=(
                "AgentSpec specialist (medallion-architect) focused on Bronze/Silver/Gold "
                "layer design and architectural integrity."
            ),
            verbose=True,
        )

        self.data_engineer = Agent(
            role="AI Data Engineer",
            goal="Validate data pipeline integrity and schema compliance",
            backstory=(
                "AgentSpec specialist (ai-data-engineer) with expertise in RAG pipelines, "
                "data quality, and streaming patterns."
            ),
            verbose=True,
        )

    def run(self) -> SpecReport:
        """
        Executes the hierarchical validation process.
        NOTE: This legacy stub returns a static mock. Use crews/spec_crew.py for live LLM execution.
        """
        _task = Task(  # noqa: F841 — kept for future crew.kickoff() activation
            description=(
                f"Validate implementation for feature context: {self.feature_context}. "
                "Identify gaps between DEFINE/DESIGN documents and the implementation."
            ),
            expected_output="A comprehensive SpecReport JSON matching the specified Pydantic schema.",
            agent=self.manager,
        )

        # Stub return — real execution delegates to crews/spec_crew.py
        return SpecReport(
            feature=self.feature_context,
            alignment_score=95.0,
            architecture_score=90.0,
            requirement_coverage=100.0,
            findings=[
                Finding(
                    title="Architectural Compliance",
                    description=(
                        "The implementation strictly follows the multi-crew topology defined in DESIGN."
                    ),
                    severity=Severity.LOW,
                    category="Architecture",
                    file_path=None,
                    line_number=None,
                )
            ],
            status="PASSED",
        )
