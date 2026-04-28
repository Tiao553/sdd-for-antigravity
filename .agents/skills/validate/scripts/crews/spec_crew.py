"""
spec_crew.py — SpecCrew: Hierarchical validation of architectural intent.

Crew topology (per docs/validate-crew-architecture.html):
  MGR  Spec Manager LLM   — Routes each section to the right specialist
  ARC  Data Architect      — Schema/medallion layer alignment vs DESIGN
  ENG  Data Engineer       — Pipeline spec, DAG logic, DEFINE requirements
  SWE  Software Engineer   — Code structure, patterns, API contracts

Process: CrewAI Process.hierarchical
Input:   ValidateContext (immutable, built by Orchestrator)
Output:  SpecReport (Pydantic-validated)

AgentSpec persona mapping:
  MGR → design-agent       (routes and classifies artifacts)
  ARC → medallion-architect (schema design, Bronze/Silver/Gold alignment)
  ENG → ai-data-engineer   (pipeline spec, DAG logic, data quality)
  SWE → code-reviewer      (code structure, patterns, maintainability)
"""

from __future__ import annotations

import json

from crewai import Agent, Crew, Process, Task

from ..llm import get_llm
from ..schemas import Finding, Severity, SpecReport, ValidateContext


def _build_spec_crew(ctx: ValidateContext) -> tuple[Agent, list[Agent], Task]:
    """
    Construct the 4 SpecCrew agents and the validation task.

    Returns: (manager_agent, specialist_list, task)
    """
    # ── MGR: Spec Manager LLM (design-agent persona) ──────────────────────
    manager = Agent(
        role="Spec Manager",
        goal=(
            "Coordinate the validation of implementation artifacts against "
            "the DEFINE requirements and DESIGN intent. Classify each artifact "
            "section and route it to the appropriate domain specialist."
        ),
        backstory=(
            "You are the AgentSpec design-agent — a strategic architect "
            "responsible for ensuring SDD phase consistency. You read the "
            "BRAINSTORM, DEFINE, and DESIGN documents and decide which sections "
            "need architectural review, pipeline review, or code review."
        ),
        verbose=True,
        allow_delegation=True,
    )

    # ── ARC: Data Architect (medallion-architect persona) ──────────────────
    architect = Agent(
        role="Data Architect",
        goal=(
            "Review schema design, data modeling choices, and medallion layer "
            "alignment against the DESIGN document. Score architecture fidelity."
        ),
        backstory=(
            "You are the AgentSpec medallion-architect — an expert in "
            "Bronze/Silver/Gold layer design, Iceberg/Delta table formats, and "
            "data quality progression. You validate that the implementation "
            "matches the architectural decisions documented in DESIGN."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── ENG: Data Engineer (ai-data-engineer persona) ──────────────────────
    engineer = Agent(
        role="Data Engineer",
        goal=(
            "Validate pipeline spec, DAG logic, and transformation logic "
            "against the DEFINE requirements. Map each requirement to its "
            "implementation evidence and flag gaps."
        ),
        backstory=(
            "You are the AgentSpec ai-data-engineer — a specialist in RAG "
            "pipelines, data quality, streaming patterns, and feature stores. "
            "You read DEFINE and check whether each stated requirement has a "
            "corresponding implementation in the code tree."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── SWE: Software Engineer (code-reviewer persona) ─────────────────────
    swe = Agent(
        role="Software Engineer",
        goal=(
            "Review code structure, design patterns, and API contracts as "
            "documented in the DESIGN. Identify deviations, anti-patterns, "
            "and missing quality gates."
        ),
        backstory=(
            "You are the AgentSpec code-reviewer — a senior engineer focused "
            "on code quality, security, and maintainability. You compare the "
            "implemented code structure against the patterns specified in DESIGN "
            "and flag deviations with severity scores."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── Task definition ────────────────────────────────────────────────────
    task = Task(
        description=(
            f"Validate the implementation of feature '{ctx.feature_name}' "
            "against its DEFINE requirements and DESIGN intent.\n\n"
            f"DEFINE document (requirements source):\n{ctx.define_content[:3000]}\n\n"
            f"DESIGN document (architecture source):\n{ctx.design_content[:3000]}\n\n"
            f"Implemented files (code tree):\n{json.dumps(ctx.code_tree, indent=2)}\n\n"
            "Produce a JSON object matching the SpecReport schema:\n"
            "{\n"
            '  "feature": "<feature_name>",\n'
            '  "alignment_score": <0-100>,\n'
            '  "architecture_score": <0-100>,\n'
            '  "requirement_coverage": <0-100>,\n'
            '  "findings": [{"title": ..., "description": ..., "severity": "LOW|MEDIUM|HIGH|CRITICAL", "category": ...}],\n'
            '  "status": "PASSED|WARNING|FAILED"\n'
            "}"
        ),
        expected_output=(
            "A valid JSON object matching the SpecReport schema. "
            "alignment_score reflects Spec Alignment (30% weight). "
            "architecture_score reflects Architecture Fidelity (20% weight). "
            "Severity CRITICAL blocks runbook generation."
        ),
        agent=manager,
    )

    return manager, [architect, engineer, swe], task


class SpecCrew:
    """
    Hierarchical CrewAI crew for spec and architectural validation.

    Agents (4 total):
      MGR  Spec Manager LLM   (design-agent persona)
      ARC  Data Architect      (medallion-architect persona)
      ENG  Data Engineer       (ai-data-engineer persona)
      SWE  Software Engineer   (code-reviewer persona)
    """

    def __init__(self, ctx: ValidateContext) -> None:
        self.ctx = ctx

    def run(self) -> SpecReport:
        """
        Execute the hierarchical spec validation and return a SpecReport.

        The Manager LLM routes sections of the DEFINE/DESIGN to the
        appropriate specialist. Results are merged into a single SpecReport.
        """
        manager, specialists, task = _build_spec_crew(self.ctx)

        crew = Crew(
            agents=specialists,
            tasks=[task],
            process=Process.hierarchical,
            manager_agent=manager,
            manager_llm=get_llm(),
            verbose=True,
        )

        result = crew.kickoff()

        # Parse the LLM output into a validated Pydantic model
        try:
            raw = result.raw if hasattr(result, "raw") else str(result)
            # Strip markdown fences if present
            raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return SpecReport.model_validate_json(raw)
        except Exception as exc:
            # Graceful degradation: return a WARNING report with the parse error
            return SpecReport(
                feature=self.ctx.feature_name,
                alignment_score=0.0,
                architecture_score=0.0,
                requirement_coverage=0.0,
                findings=[
                    Finding(
                        title="SpecCrew Output Parse Error",
                        description=f"Could not parse crew output as SpecReport: {exc}",
                        severity=Severity.HIGH,
                        category="Architecture",
                        file_path=None,
                        line_number=None,
                    )
                ],
                status="FAILED",
            )
