"""
code_crew.py — CodeCrew: Hierarchical technical implementation audit.

Crew topology (per docs/validate-crew-architecture.html):
  MGR  Code Manager LLM   — Runs ruff/mypy/pytest; classifies findings by domain
  SWE  Software Engineer   — Code quality, linting, type safety, anti-patterns
  ENG  Data Engineer       — Pipeline impl, transformation correctness, data test coverage
  OPS  DevOps Specialist   — CI/CD config, Dockerfile, deps, secrets hygiene

Process: CrewAI Process.hierarchical
Input:   ValidateContext (immutable) + tool outputs (ruff, mypy, pytest)
Output:  CodeReport (Pydantic-validated)

AgentSpec persona mapping:
  MGR → code-reviewer      (classifies findings, routes to specialist)
  SWE → python-developer   (code quality, type hints, clean patterns)
  ENG → ai-data-engineer   (pipeline implementation, data logic coverage)
  OPS → ci-cd-specialist   (DevOps hygiene, CI/CD, infra-as-code)
"""

from __future__ import annotations

import json

from crewai import Agent, Crew, Process, Task

from ..llm import get_llm
from ..schemas import CodeReport, Finding, Severity, ValidateContext
from ..tools import run_mypy, run_ruff


def _compute_quality_score(lint_issues: int, type_errors: int) -> float:
    """
    Compute a code quality score from lint and type error counts.

    Scoring logic:
      - Start at 100
      - Each lint issue deducts 3 points (capped at -40)
      - Each type error deducts 8 points (capped at -60)
    """
    lint_penalty = min(lint_issues * 3, 40)
    type_penalty = min(type_errors * 8, 60)
    return max(0.0, float(100 - lint_penalty - type_penalty))


def _compute_devops_score(ctx: ValidateContext) -> float:
    """
    Compute a basic DevOps hygiene score from the code tree.

    Checks for presence of common DevOps artifacts.
    """
    tree_lower = [f.lower() for f in ctx.code_tree]
    checks = {
        "ci_config": any("github" in f or ".gitlab" in f or "ci.yml" in f for f in tree_lower),
        "dockerfile": any("dockerfile" in f for f in tree_lower),
        "requirements": any("requirements" in f or "pyproject" in f for f in tree_lower),
        "no_secrets": not any(".env" in f and "example" not in f for f in tree_lower),
    }
    passed = sum(checks.values())
    return float(passed / len(checks) * 100)


def _build_code_crew(
    ctx: ValidateContext,
    ruff_result: dict,
    mypy_result: dict,
) -> tuple[Agent, list[Agent], Task]:
    """
    Construct the 4 CodeCrew agents and the audit task.

    Returns: (manager_agent, specialist_list, task)
    """
    # ── MGR: Code Manager LLM (code-reviewer persona) ─────────────────────
    manager = Agent(
        role="Code Manager",
        goal=(
            "Coordinate the technical audit of the implementation. "
            "Analyse ruff, mypy and pytest results, classify findings by "
            "severity and domain, then route each finding to the correct specialist."
        ),
        backstory=(
            "You are the AgentSpec code-reviewer — a senior engineer expert "
            "in code quality, security, and maintainability. You receive the "
            "raw output from ruff, mypy, and pytest, triage the findings, "
            "and dispatch them to the appropriate domain specialist."
        ),
        verbose=True,
        allow_delegation=True,
    )

    # ── SWE: Software Engineer (python-developer persona) ──────────────────
    swe = Agent(
        role="Software Engineer",
        goal=(
            "Review code quality, linting results, type safety, complexity "
            "metrics, and anti-patterns. Produce severity-scored findings for "
            "each issue identified in the ruff and mypy output."
        ),
        backstory=(
            "You are the AgentSpec python-developer — a code architect for "
            "data engineering systems specializing in clean patterns, type hints, "
            "dataclasses, and generators. You translate tool output into "
            "actionable, severity-scored code quality findings."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── ENG: Data Engineer (ai-data-engineer persona) ──────────────────────
    engineer = Agent(
        role="Data Engineer",
        goal=(
            "Review pipeline implementation correctness, transformation logic, "
            "and test coverage of data-specific logic. Flag missing tests for "
            "data transformations, schema validation, and edge cases."
        ),
        backstory=(
            "You are the AgentSpec ai-data-engineer — a specialist in RAG "
            "pipelines, feature stores, and data quality patterns. You assess "
            "whether the data logic has adequate test coverage and whether "
            "transformation correctness can be verified."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── OPS: DevOps Specialist (ci-cd-specialist persona) ──────────────────
    ops = Agent(
        role="DevOps Specialist",
        goal=(
            "Check CI/CD configuration, Dockerfile, dependency manifests, "
            "infra-as-code, and secrets hygiene. Flag missing or misconfigured "
            "DevOps artifacts with severity scores."
        ),
        backstory=(
            "You are the AgentSpec ci-cd-specialist — a DevOps expert for "
            "Azure DevOps, Terraform, and Databricks Asset Bundles. You audit "
            "the code tree for CI/CD maturity: pipeline config, containerization, "
            "dependency pinning, and secret management hygiene."
        ),
        verbose=True,
        allow_delegation=False,
    )

    # ── Task definition ────────────────────────────────────────────────────
    task = Task(
        description=(
            f"Perform a technical audit of the implementation of feature "
            f"'{ctx.feature_name}'.\n\n"
            f"Implemented files:\n{json.dumps(ctx.code_tree, indent=2)}\n\n"
            f"ruff check results ({ruff_result['count']} issues):\n"
            f"{json.dumps(ruff_result['issues'][:20], indent=2)}\n\n"
            f"mypy results ({mypy_result['count']} errors):\n"
            f"{mypy_result['raw'][:2000]}\n\n"
            "Produce a JSON object matching the CodeReport schema:\n"
            "{\n"
            '  "feature": "<feature_name>",\n'
            '  "quality_score": <0-100>,\n'
            '  "devops_score": <0-100>,\n'
            '  "test_coverage": <0-100 or null>,\n'
            '  "lint_issues": <int>,\n'
            '  "type_errors": <int>,\n'
            '  "findings": [{"title": ..., "description": ..., "severity": "LOW|MEDIUM|HIGH|CRITICAL", "category": ...}],\n'
            '  "status": "PASSED|WARNING|FAILED"\n'
            "}"
        ),
        expected_output=(
            "A valid JSON object matching the CodeReport schema. "
            "quality_score reflects Code Quality dimension (25% weight). "
            "devops_score reflects Security & DevOps dimension (15% weight). "
            "Severity CRITICAL blocks runbook generation."
        ),
        agent=manager,
    )

    return manager, [swe, engineer, ops], task


class CodeCrew:
    """
    Hierarchical CrewAI crew for technical implementation auditing.

    Agents (4 total):
      MGR  Code Manager LLM   (code-reviewer persona)
      SWE  Software Engineer   (python-developer persona)
      ENG  Data Engineer       (ai-data-engineer persona)
      OPS  DevOps Specialist   (ci-cd-specialist persona)
    """

    def __init__(self, ctx: ValidateContext) -> None:
        self.ctx = ctx

    def run(self) -> CodeReport:
        """
        Execute the technical audit and return a CodeReport.

        Step 1: Run ruff and mypy via tools.py (deterministic, no LLM).
        Step 2: Pass results to hierarchical crew for severity classification.
        Step 3: Parse crew output into a validated CodeReport Pydantic model.
        """
        # Step 1 — Run deterministic tools (whitelisted, no arbitrary shell)
        skill_path = ".agents/skills/validate"
        ruff_result = run_ruff(skill_path)
        mypy_result = run_mypy(skill_path)

        # Pre-compute scores for graceful degradation
        quality_score = _compute_quality_score(ruff_result["count"], mypy_result["count"])
        devops_score = _compute_devops_score(self.ctx)

        # Step 2 — Crew analysis
        manager, specialists, task = _build_code_crew(self.ctx, ruff_result, mypy_result)

        crew = Crew(
            agents=specialists,
            tasks=[task],
            process=Process.hierarchical,
            manager_agent=manager,
            manager_llm=get_llm(),
            verbose=True,
        )

        result = crew.kickoff()

        # Step 3 — Parse output
        try:
            raw = result.raw if hasattr(result, "raw") else str(result)
            raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return CodeReport.model_validate_json(raw)
        except Exception as exc:
            # Graceful degradation: build report from tool outputs directly
            findings = []
            if ruff_result["count"] > 0:
                findings.append(
                    Finding(
                        title="Lint Issues Detected",
                        description=f"ruff found {ruff_result['count']} issues.",
                        severity=Severity.MEDIUM,
                        category="Style",
                        file_path=None,
                        line_number=None,
                    )
                )
            if mypy_result["count"] > 0:
                findings.append(
                    Finding(
                        title="Type Errors Detected",
                        description=f"mypy found {mypy_result['count']} errors.",
                        severity=Severity.HIGH,
                        category="Logic",
                        file_path=None,
                        line_number=None,
                    )
                )
            findings.append(
                Finding(
                    title="CodeCrew Output Parse Error",
                    description=f"Could not parse crew output as CodeReport: {exc}",
                    severity=Severity.MEDIUM,
                    category="Logic",
                    file_path=None,
                    line_number=None,
                )
            )
            return CodeReport(
                feature=self.ctx.feature_name,
                quality_score=quality_score,
                devops_score=devops_score,
                test_coverage=None,
                lint_issues=ruff_result["count"],
                type_errors=mypy_result["count"],
                findings=findings,
                status="WARNING" if ruff_result["count"] + mypy_result["count"] == 0 else "FAILED",
            )
