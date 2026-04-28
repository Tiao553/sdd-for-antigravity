"""
council_crew.py — CouncilCrew: Final Scoring and Artifact Eligibility.

Crew topology (per docs/validate-crew-architecture.html):
  JDG  The Judge           — Computes final 5-dimension weighted score
  RPT  Report Writer       — Synthesizes findings into an executive summary
  PRD  Readiness Officer   — Determines eligibility for RUNBOOK/ROADMAP artifacts

Process: CrewAI Process.sequential
Input:   ValidateContext + SpecReport + CodeReport + DeliveryDelta
Output:  ValidationReport (Pydantic-validated)

AgentSpec persona mapping:
  JDG → genai-architect   (master orchestrator and mathematical judge)
  RPT → code-documenter   (expert documentation and summary synthesis)
  PRD → the-planner       (strategic readiness assessment)
"""

from __future__ import annotations

from crewai import Agent, Crew, Process, Task
from ..schemas import ValidationReport, ValidateContext, SpecReport, CodeReport, DeliveryDelta


def _build_council_crew(
    ctx: ValidateContext,
    spec_report: SpecReport,
    code_report: CodeReport,
    delivery_delta: DeliveryDelta
) -> tuple[list[Agent], list[Task]]:
    """
    Construct the 3 CouncilCrew agents and the final verdict tasks.
    """
    # ── JDG: The Judge (genai-architect persona) ───────────────────────────
    judge = Agent(
        role="The Judge",
        goal=(
            "Apply the weighted scoring formula from DESIGN v2.0 to calculate the final score. "
            "Dimension weights: SpecAlignment(30%), CodeQuality(25%), ArchFidelity(20%), "
            "Security/DevOps(15%), ProdReadiness(10%)."
        ),
        backstory=(
            "You are the AgentSpec genai-architect — a mathematical judge focused on "
            "system-level correctness. You aggregate data from all previous crews and "
            "compute the definitive feature score."
        ),
        verbose=True,
        allow_delegation=False
    )

    # ── RPT: Report Writer (code-documenter persona) ───────────────────────
    writer = Agent(
        role="Report Writer",
        goal=(
            "Synthesize all findings from Spec, Code, and Delivery crews into a single, "
            "concise Executive Summary. Highlight the most critical risks."
        ),
        backstory=(
            "You are the AgentSpec code-documenter — a master of technical clarity. "
            "You turn complex audit logs into readable, actionable summaries for stakeholders."
        ),
        verbose=True,
        allow_delegation=False
    )

    # ── PRD: Readiness Officer (the-planner persona) ────────────────────────
    officer = Agent(
        role="Readiness Officer",
        goal=(
            "Assess production readiness. Determine if the feature is eligible for a RUNBOOK "
            "(score >= 90, zero CRITICAL) or a ROADMAP (score 70-89, zero CRITICAL)."
        ),
        backstory=(
            "You are the AgentSpec the-planner — a strategic analyst who determines when "
            "a feature is truly ready for deployment versus when it needs more iteration."
        ),
        verbose=True,
        allow_delegation=False
    )

    # ── Task 1: Scoring and Synthesis ──────────────────────────────────────
    verdict_task = Task(
        description=(
            f"Produce the final ValidationReport for feature '{ctx.feature_name}'.\n\n"
            "INPUT DATA:\n"
            f"- Spec Report: {spec_report.model_dump_json()}\n"
            f"- Code Report: {code_report.model_dump_json()}\n"
            f"- Delivery Delta: {delivery_delta.model_dump_json()}\n\n"
            "SCORING FORMULA (apply these weights exactly):\n"
            "  score = (alignment_score * 0.30)\n"
            "        + (quality_score   * 0.25)\n"
            "        + (architecture_score * 0.20)\n"
            "        + (devops_score    * 0.15)\n"
            "        + (delta_score     * 0.10)\n\n"
            "ARTIFACT ELIGIBILITY:\n"
            "  runbook_eligible = score >= 90 AND zero CRITICAL findings\n"
            "  roadmap_eligible = 70 <= score < 90 AND zero CRITICAL findings\n\n"
            "CRITICAL: You MUST produce ONLY the following JSON fields. Do NOT add any other fields.\n"
            "Produce a JSON object with EXACTLY these fields:\n"
            "{\n"
            f'  "feature": "{ctx.feature_name}",\n'
            '  "score": <computed weighted score 0-100 as a number>,\n'
            '  "status": "PASSED" | "WARNING" | "FAILED",\n'
            '  "dimensions": {\n'
            '    "Spec Alignment": <alignment_score value>,\n'
            '    "Code Quality": <quality_score value>,\n'
            '    "Architecture Fidelity": <architecture_score value>,\n'
            '    "Security & DevOps": <devops_score value>,\n'
            '    "Production Readiness": <delta_score value>\n'
            '  },\n'
            '  "critical_issues": [<list of Finding objects with severity CRITICAL>],\n'
            '  "findings": [<list of all non-CRITICAL Finding objects>],\n'
            '  "runbook_eligible": <true or false>,\n'
            '  "roadmap_eligible": <true or false>,\n'
            '  "summary": "<one paragraph executive summary>"\n'
            "}\n\n"
            "IMPORTANT: Each Finding object must have: title, description, severity (LOW|MEDIUM|HIGH|CRITICAL), category.\n"
            "Do NOT include fields like requirement_coverage, artifacts, or any other custom fields."
        ),
        expected_output=(
            "A valid JSON object with exactly these fields: feature, score, status, dimensions, "
            "critical_issues, findings, runbook_eligible, roadmap_eligible, summary. "
            "No other fields allowed."
        ),
        agent=judge
    )

    return [judge, writer, officer], [verdict_task]


class CouncilCrew:
    """
    Sequential CrewAI crew for final verdict and scoring.
    """

    def __init__(
        self,
        ctx: ValidateContext,
        spec_report: SpecReport,
        code_report: CodeReport,
        delivery_delta: DeliveryDelta
    ) -> None:
        self.ctx = ctx
        self.spec_report = spec_report
        self.code_report = code_report
        self.delivery_delta = delivery_delta

    def run(self) -> ValidationReport:
        agents, tasks = _build_council_crew(
            self.ctx, self.spec_report, self.code_report, self.delivery_delta
        )

        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        try:
            raw = result.raw if hasattr(result, "raw") else str(result)
            # Strip markdown fences if present
            raw = raw.strip().removeprefix("```json").removeprefix("```").strip()
            if raw.endswith("```"):
                raw = raw[:-3].strip()
            # Remove LLM abbreviation placeholders like `...` inside arrays
            # e.g. ["real item", ..., "real item"] → ["real item", "real item"]
            import re as _re
            raw = _re.sub(r",\s*\.\.\.\s*(?=[,\]])", "", raw)
            raw = _re.sub(r"\[\s*\.\.\.\s*\]", "[]", raw)
            return ValidationReport.model_validate_json(raw)
        except Exception as exc:
            return ValidationReport(
                feature=self.ctx.feature_name,
                score=0.0,
                status="FAILED",
                dimensions={
                    "Spec Alignment": 0.0,
                    "Code Quality": 0.0,
                    "Architecture Fidelity": 0.0,
                    "Security & DevOps": 0.0,
                    "Production Readiness": 0.0,
                },
                critical_issues=[],
                findings=[],
                runbook_eligible=False,
                roadmap_eligible=False,
                summary=f"Parse error in CouncilCrew: {exc}",
            )
