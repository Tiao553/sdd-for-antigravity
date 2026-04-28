"""
ValidateSkill — Multi-agent quality gate for the AgentSpec SDD workflow.

Entry point for the /validate skill. Exposes ValidateSkill as the primary
orchestration class. Internally coordinates four specialized CrewAI crews:

    SpecCrew (Hierarchical · 4 agents)  ─── parallel ───┐
    CodeCrew (Hierarchical · 4 agents)  ─────────────────┤
                                                         ▼
                                            DeliveryCrew (Sequential · 2 agents)
                                                         │
                                                         ▼
                                            CouncilCrew  (Sequential · 3 agents)
                                                         │
                                                         ▼
                                            ValidationReport → RUNBOOK | ROADMAP

Design: DESIGN_VALIDATE_WORKFLOW.md v2.0
"""

from __future__ import annotations

from .schemas import (
    CodeReport,
    DeliveryDelta,
    Finding,
    RequirementStatus,
    Severity,
    SpecReport,
    ValidateContext,
    ValidationReport,
)
from .tools import read_sdd_context

__all__ = [
    # Primary entry point
    "ValidateSkill",
    # Schemas (re-exported for external use)
    "ValidateContext",
    "SpecReport",
    "CodeReport",
    "DeliveryDelta",
    "ValidationReport",
    "Finding",
    "Severity",
    "RequirementStatus",
    # Tools
    "read_sdd_context",
]


class ValidateSkill:
    """
    Orchestrates the full multi-crew validation pipeline for a given feature.

    Usage:
        skill = ValidateSkill("VALIDATE_WORKFLOW")
        report = skill.run()

    The run() method:
      1. Builds ValidateContext from disk (immutable)
      2. Executes SpecCrew and CodeCrew in parallel (ThreadPoolExecutor)
      3. Passes results to DeliveryCrew for delta analysis
      4. Passes all results to CouncilCrew for final scoring and verdict
      5. Returns a ValidationReport with runbook_eligible / roadmap_eligible flags
    """

    def __init__(self, feature_name: str) -> None:
        self.feature_name = feature_name
        self._context: ValidateContext | None = None

    def build_context(self) -> ValidateContext:
        """Build and cache the ValidateContext from SDD files on disk."""
        if self._context is None:
            self._context = read_sdd_context(self.feature_name)
        return self._context

    def run(self) -> ValidationReport:
        """
        Execute the full validation pipeline.

        Crews are imported lazily to avoid circular imports and to allow
        the skill to be used without crewai installed (e.g. in testing).
        """
        ctx = self.build_context()

        # Lazy imports to prevent circular dependency issues and avoid CrewAI
        # side effects before local SDD pre-flight checks pass.
        import concurrent.futures

        from .crews.code_crew import CodeCrew
        from .crews.council_crew import CouncilCrew
        from .crews.delivery_crew import DeliveryCrew
        from .crews.spec_crew import SpecCrew

        # Phase 1 — Parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            spec_future = executor.submit(SpecCrew(ctx).run)
            code_future = executor.submit(CodeCrew(ctx).run)
            spec_report: SpecReport = spec_future.result()
            code_report: CodeReport = code_future.result()

        # Phase 2 — Sequential convergence
        delivery_delta: DeliveryDelta = DeliveryCrew(ctx, spec_report, code_report).run()
        validation_report: ValidationReport = CouncilCrew(
            ctx, spec_report, code_report, delivery_delta
        ).run()

        return validation_report
