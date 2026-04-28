"""
delivery_crew.py — DeliveryCrew: Intent vs. Delivery Gap Analysis.

Crew topology (per docs/validate-crew-architecture.html):
  CMP  Delivery Comparator — Diffs SpecReport + CodeReport vs original intents
  GAP  Gap Mapper          — Maps DEFINE requirements to implementation evidence

Process: CrewAI Process.sequential
Input:   ValidateContext + SpecReport + CodeReport
Output:  DeliveryDelta (Pydantic-validated)

AgentSpec persona mapping:
  CMP → the-planner           (strategic comparison of planned vs built)
  GAP → data-quality-analyst  (detailed mapping and gap identification)
"""

from __future__ import annotations

from crewai import Agent, Crew, Process, Task
from ..schemas import DeliveryDelta, ValidateContext, SpecReport, CodeReport


def _build_delivery_crew(
    ctx: ValidateContext,
    spec_report: SpecReport,
    code_report: CodeReport
) -> tuple[list[Agent], list[Task]]:
    """
    Construct the 2 DeliveryCrew agents and the comparison tasks.
    """
    # ── CMP: Delivery Comparator (the-planner persona) ─────────────────────
    comparator = Agent(
        role="Delivery Comparator",
        goal=(
            "Compare the original architectural intent (DESIGN) and requirements (DEFINE) "
            "against the actual implementation artifacts (SpecReport and CodeReport). "
            "Identify what was planned vs. what was actually delivered."
        ),
        backstory=(
            "You are the AgentSpec the-planner — a strategic AI architect focused on "
            "implementation traceability. You excel at detecting when a codebase has "
            "drifted from its design or when planned features are missing."
        ),
        verbose=True,
        allow_delegation=False
    )

    # ── GAP: Gap Mapper (data-quality-analyst persona) ──────────────────────
    gap_mapper = Agent(
        role="Gap Mapper",
        goal=(
            "Map every specific requirement from the DEFINE document to its evidence "
            "in the codebase. Flag missing, partial, or misaligned deliverables."
        ),
        backstory=(
            "You are the AgentSpec data-quality-analyst — a specialist in ensuring "
            "that every data contract and requirement is met with high fidelity. "
            "You identify 'ghost' requirements that exist in docs but not in code."
        ),
        verbose=True,
        allow_delegation=False
    )

    # ── Task 1: Comparison Analysis ────────────────────────────────────────
    compare_task = Task(
        description=(
            f"Perform a detailed comparison for feature '{ctx.feature_name}'.\n\n"
            f"Original Intent (DEFINE):\n{ctx.define_content[:2000]}\n\n"
            f"Original Design (DESIGN):\n{ctx.design_content[:2000]}\n\n"
            f"Spec Validation Findings:\n{spec_report.model_dump_json(indent=2)}\n\n"
            f"Code Audit Findings:\n{code_report.model_dump_json(indent=2)}\n\n"
            "Identify missing files from the DESIGN manifest and functional logic gaps."
        ),
        expected_output="A structured list of missing files and identified functional logic gaps.",
        agent=comparator
    )

    # ── Task 2: Requirement Mapping ─────────────────────────────────────────
    map_task = Task(
        description=(
            "Based on the comparison, map each requirement in the DEFINE doc to its delivery status.\n"
            "Produce a JSON object matching the DeliveryDelta schema:\n"
            "{\n"
            '  "feature": "<feature_name>",\n'
            '  "missing_files": [...],\n'
            '  "unexpected_files": [...],\n'
            '  "logic_gaps": [...],\n'
            '  "requirement_map": {"REQ-001": "DELIVERED|PARTIAL|MISSING", ...},\n'
            '  "delta_score": <0-100>,\n'
            '  "status": "PASSED|WARNING|FAILED"\n'
            "}"
        ),
        expected_output="A valid JSON object matching the DeliveryDelta schema.",
        agent=gap_mapper,
        context=[compare_task]
    )

    return [comparator, gap_mapper], [compare_task, map_task]


class DeliveryCrew:
    """
    Sequential CrewAI crew for delivery gap analysis.
    """

    def __init__(
        self,
        ctx: ValidateContext,
        spec_report: SpecReport,
        code_report: CodeReport
    ) -> None:
        self.ctx = ctx
        self.spec_report = spec_report
        self.code_report = code_report

    def run(self) -> DeliveryDelta:
        agents, tasks = _build_delivery_crew(self.ctx, self.spec_report, self.code_report)

        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        try:
            raw = result.raw if hasattr(result, "raw") else str(result)
            raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return DeliveryDelta.model_validate_json(raw)
        except Exception as exc:
            return DeliveryDelta(
                feature=self.ctx.feature_name,
                missing_files=[],
                unexpected_files=[],
                logic_gaps=[f"Parse error in DeliveryCrew: {exc}"],
                requirement_map={},
                delta_score=0.0,
                status="FAILED"
            )
