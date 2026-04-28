"""
code_crew.py — Legacy flat stub (superseded by crews/code_crew.py).

Kept for backwards compatibility. The active implementation lives in
.github/skills/validate/scripts/crews/code_crew.py (Hierarchical · 4 agents).
"""

from crewai import Agent
from .schemas import CodeReport, Finding, Severity
from .tools import get_test_coverage, run_mypy, run_ruff


class CodeCrew:
    """
    Legacy stub — audits technical implementation quality (lint, types, tests).
    The real hierarchical crew lives in crews/code_crew.py.
    """

    def __init__(self, feature_path: str):
        self.feature_path = feature_path
        self.auditor = Agent(
            role="Code Reviewer",
            goal="Analyze implementation quality, security, and maintainability using automated tools",
            backstory=(
                "AgentSpec specialist (code-reviewer) focused on ensuring production-grade "
                "code quality and security standards."
            ),
            verbose=True,
        )

    def run(self) -> CodeReport:
        """
        Executes the technical audit.
        NOTE: This legacy stub runs ruff/mypy locally. Use crews/code_crew.py for LLM-augmented analysis.
        """
        ruff_res = run_ruff(self.feature_path)
        mypy_res = run_mypy(self.feature_path)
        coverage = get_test_coverage(self.feature_path)

        findings: list[Finding] = []
        if ruff_res["count"] > 0:
            findings.append(
                Finding(
                    title="Lint Issues Detected",
                    description=f"Ruff found {ruff_res['count']} issues.",
                    severity=Severity.MEDIUM,
                    category="Style",
                    file_path=None,
                    line_number=None,
                )
            )

        if mypy_res["count"] > 0:
            findings.append(
                Finding(
                    title="Type Errors Detected",
                    description=f"Mypy found {mypy_res['count']} errors.",
                    severity=Severity.HIGH,
                    category="Logic",
                    file_path=None,
                    line_number=None,
                )
            )

        lint_count: int = ruff_res["count"]
        type_count: int = mypy_res["count"]

        return CodeReport(
            feature=self.feature_path,
            quality_score=float(max(0, 100 - (lint_count * 5) - (type_count * 10))),
            devops_score=85.0,  # Default devops score for legacy stub (no CI introspection)
            test_coverage=coverage,
            lint_issues=lint_count,
            type_errors=type_count,
            findings=findings,
            status="PASSED" if type_count == 0 else "WARNING",
        )
