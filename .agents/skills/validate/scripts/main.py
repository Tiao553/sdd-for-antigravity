"""
main.py — CLI entry point for the /validate quality gate.

Usage:
  python .github/skills/validate/scripts/main.py <FEATURE_NAME>

Orchestrates the multi-crew pipeline:
  1. SpecCrew & CodeCrew (Parallel)
  2. DeliveryCrew (Sequential)
  3. CouncilCrew (Sequential)

Design: DESIGN_VALIDATE_WORKFLOW.md v2.0
"""

import sys
from datetime import date
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# main.py lives in scripts/, so:
#   __file__ → .github/skills/validate/scripts/main.py
#   .parent  → .github/skills/validate/scripts/
#   .parent.parent → .github/skills/validate/  (the validate package root)
#   .parent.parent.parent → .github/skills/      (on sys.path so `from scripts...` works)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # skills/
sys.path.insert(0, str(Path(__file__).parent.parent))         # validate/

# Import from the scripts sub-package (where all code actually lives)
from scripts import ValidateSkill
from scripts.schemas import Finding, ValidationReport
from scripts.tools import find_feature_dir

app = typer.Typer(help="AgentSpec /validate quality gate.")
console = Console()

SDD_TEMPLATES_DIR = Path(".github/sdd/templates")


def _load_template(name: str) -> str:
    """Read an SDD template from .github/sdd/templates."""
    return (SDD_TEMPLATES_DIR / name).read_text(encoding="utf-8")


def _finding_rows(findings: list[Finding], prefix: str) -> str:
    if not findings:
        return "| - | None | - | - |"
    rows = []
    for index, finding in enumerate(findings, start=1):
        rows.append(
            "| {id} | {issue} | {domain} | {recommendation} |".format(
                id=f"{prefix}-{index:02d}",
                issue=finding.title.replace("|", "/"),
                domain=finding.category.replace("|", "/"),
                recommendation=finding.description.replace("|", "/"),
            )
        )
    return "\n".join(rows)


def _gate(score: float, warning_threshold: float = 70.0, pass_threshold: float = 90.0) -> str:
    if score >= pass_threshold:
        return "PASS"
    if score >= warning_threshold:
        return "WARNING"
    return "FAIL"


def _gap_rows(report: ValidationReport) -> str:
    gaps = report.findings or report.critical_issues
    if not gaps:
        return "| - | None | - |"
    return "\n".join(
        "| GAP-{index:02d} | {description} | {severity} |".format(
            index=index,
            description=finding.description.replace("|", "/"),
            severity=finding.severity.value,
        )
        for index, finding in enumerate(gaps, start=1)
    )


def _scoring_rows(report: ValidationReport) -> str:
    rows = [
        ("Spec Alignment", "30%", "DEFINE coverage and requirement traceability"),
        ("Code Quality", "25%", "Lint, type checks, tests, and maintainability"),
        ("Architecture Fidelity", "20%", "Conformance to DESIGN decisions and boundaries"),
        ("Security & DevOps", "15%", "Secrets, CI/CD, dependency, and operational controls"),
        ("Production Readiness", "10%", "Delivery completeness, rollback, and observability"),
    ]
    return "\n".join(
        "| {dimension} | {weight} | {score:.1f}/100 | {gate} | {notes} |".format(
            dimension=dimension,
            weight=weight,
            score=report.dimensions.get(dimension, 0.0),
            gate=_gate(report.dimensions.get(dimension, 0.0)),
            notes=notes,
        )
        for dimension, weight, notes in rows
    )


def _roadmap_rows(report: ValidationReport) -> str:
    items = report.artifact_plan.get("roadmap_items", [])
    if not isinstance(items, list) or not items:
        items = [finding.description for finding in report.findings[:5]]
    if not items:
        items = ["Re-run /validate after implementation changes and review the validation report."]
    return "\n".join(
        "| P{priority} | GAP-{index:02d} | {task} | TBD | DataEng / SWE |".format(
            priority=min(index, 3),
            index=index,
            task=str(item).replace("|", "/"),
        )
        for index, item in enumerate(items, start=1)
    )


def _render_validation_report(feature_name: str, report: ValidationReport) -> str:
    template = _load_template("VALIDATION_REPORT_TEMPLATE.md")
    verdict = "Approved for Prod" if report.runbook_eligible else "Remediation Required"
    production_decision = (
        "Approved for production runbook generation"
        if report.runbook_eligible
        else "Requires remediation before production approval"
    )
    replacements = {
        "{FEATURE_NAME}": feature_name,
        "{YYYY-MM-DD}": date.today().isoformat(),
        "{SCORE}": f"{report.score:.1f}",
        "{VERDICT}": verdict,
        "{RECOMMENDED_ARTIFACT}": str(report.artifact_plan.get("recommended_artifact", "VALIDATION_REPORT")),
        "{GATE_OWNER}": "Validation owner",
        "{DELIVERY_OWNER}": "Delivery owner",
        "{EXECUTIVE_SUMMARY}": report.summary or "Validation completed. Review scoring, gaps, and evidence before promotion.",
        "{PRODUCTION_READINESS_DECISION}": production_decision,
        "{RUNBOOK_ELIGIBILITY}": "Eligible" if report.runbook_eligible else "Not eligible",
        "{ROADMAP_ELIGIBILITY}": "Eligible" if report.roadmap_eligible else "Not eligible",
        "{BLOCKING_ISSUE_COUNT}": str(len(report.critical_issues)),
        "{SPEC_GATE_RESULT}": _gate(report.dimensions.get("Spec Alignment", 0.0)),
        "{ARCH_GATE_RESULT}": _gate(report.dimensions.get("Architecture Fidelity", 0.0)),
        "{CODE_GATE_RESULT}": _gate(report.dimensions.get("Code Quality", 0.0)),
        "{DEVOPS_GATE_RESULT}": _gate(report.dimensions.get("Security & DevOps", 0.0)),
        "{READINESS_GATE_RESULT}": _gate(report.dimensions.get("Production Readiness", 0.0)),
        "{SCORING_ROWS}": _scoring_rows(report),
        "{CRITICAL_ISSUE_ROWS}": _finding_rows(report.critical_issues, "CRIT"),
        "{GAP_ROWS}": _gap_rows(report),
        "{DEFINE_EVIDENCE_STATUS}": "Required",
        "{DESIGN_EVIDENCE_STATUS}": "Required",
        "{BUILD_EVIDENCE_STATUS}": "Required",
        "{CODE_TREE_STATUS}": "Reviewed",
    }
    content = template
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content


def _render_runbook(feature_name: str, report: ValidationReport) -> str:
    template = _load_template("RUNBOOK_TEMPLATE.md")
    notes = report.artifact_plan.get("runbook_notes", [])
    note_text = "; ".join(str(note) for note in notes) if isinstance(notes, list) else str(notes)
    replacements = {
        "{FEATURE_NAME}": feature_name,
        "{YYYY-MM-DD}": date.today().isoformat(),
        "{STATUS}": "Approved",
        "{RELEASE_OWNER}": "Release owner",
        "{OPERATIONS_OWNER}": "Operations owner",
        "{GATE_OWNER}": "Validation owner",
        "{DELIVERY_OWNER}": "Delivery owner",
        "{RELEASE_SUMMARY}": report.summary or "Feature passed validation and is eligible for production runbook generation.",
        "{VALIDATION_SCORE}": f"{report.score:.1f}",
        "{CRITICAL_ISSUE_COUNT}": str(len(report.critical_issues)),
        "{RELEASE_VERIFICATION_COMMAND}": "git rev-parse HEAD",
        "{DEPLOY_COMMAND}": "TBD",
        "{SMOKE_TEST_COMMAND}": "TBD",
        "{HEALTH_CHECK_COMMAND}": "TBD",
        "{COMMUNICATION_CHANNEL}": "TBD",
        "{RUNTIME_ENVIRONMENT}": "TBD",
        "{ENV_CHECK_COMMAND}": "TBD",
        "{SECRET_REFERENCES}": "TBD",
        "{EXTERNAL_DEPENDENCIES}": "TBD",
        "{DATA_DEPENDENCIES}": "TBD",
        "{FEATURE_FLAGS}": "TBD",
        "{AVAILABILITY_SOURCE}": "Monitoring dashboard",
        "{AVAILABILITY_THRESHOLD}": "Project-defined SLA",
        "{ALERT_OWNER}": "On-call owner",
        "{ERROR_RATE_SOURCE}": "Runtime logs or metrics",
        "{ERROR_RATE_THRESHOLD}": "Project-defined threshold",
        "{LATENCY_SOURCE}": "Runtime metrics",
        "{LATENCY_THRESHOLD}": "Project-defined threshold",
        "{DATA_QUALITY_SOURCE}": "Quality checks or validation suite",
        "{DATA_QUALITY_THRESHOLD}": "No critical regressions",
        "{OPERATIONAL_NOTES}": note_text or "No additional operational notes were provided by validation guidance.",
        "{ROLLBACK_TRIGGER}": "Critical smoke test failure, elevated error rate, or data quality regression",
        "{FREEZE_COMMAND}": "TBD",
        "{ROLLBACK_COMMAND}": "TBD",
        "{POST_ROLLBACK_CHECK}": "TBD",
        "{INCIDENT_DOC_LINK}": "TBD",
        "{MONITORING_DASHBOARD}": "TBD",
    }
    content = template
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content


def _render_roadmap(feature_name: str, report: ValidationReport) -> str:
    template = _load_template("ROADMAP_TEMPLATE.md")
    replacements = {
        "{FEATURE_NAME}": feature_name,
        "{YYYY-MM-DD}": date.today().isoformat(),
        "{CURRENT_SCORE}": f"{report.score:.1f}",
        "{CURRENT_VERDICT}": report.status,
        "{REMEDIATION_OWNER}": "Remediation owner",
        "{ARCHITECTURE_OWNER}": "Architecture owner",
        "{DELIVERY_OWNER}": "Delivery owner",
        "{OPERATIONS_OWNER}": "Operations owner",
        "{REMEDIATION_SUMMARY}": report.summary or "Validation found gaps that must be remediated before production approval.",
        "{ROADMAP_ROWS}": _roadmap_rows(report),
    }
    content = template
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content


def _write_artifacts(feature_name: str, report: ValidationReport) -> None:
    """Render markdown artifacts from templates using the crew's JSON guidance."""
    feature_dir = find_feature_dir(feature_name)
    feature_dir.mkdir(parents=True, exist_ok=True)

    artifacts = {
        f"VALIDATION_REPORT_{feature_name}.md": _render_validation_report(feature_name, report),
    }
    if report.runbook_eligible:
        artifacts[f"RUNBOOK_{feature_name}.md"] = _render_runbook(feature_name, report)
    elif report.roadmap_eligible:
        artifacts[f"ROADMAP_{feature_name}.md"] = _render_roadmap(feature_name, report)

    for filename, content in artifacts.items():
        target_path = feature_dir / filename
        target_path.write_text(content, encoding="utf-8")
        console.print(f"[bold green]✅ Artifact generated:[/bold green] {target_path}")


@app.command()
def validate(
    feature_name: str = typer.Argument(..., help="Feature name to validate (e.g. VALIDATE_WORKFLOW)")
):
    """Execute the full multi-agent validation pipeline."""
    console.print(Panel(f"[bold blue]🚀 Starting Validation for: {feature_name}[/bold blue]"))

    try:
        skill = ValidateSkill(feature_name)
        report: ValidationReport = skill.run()
    except FileNotFoundError as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]❌ Pipeline Failed:[/bold red] {e}")
        raise typer.Exit(code=1)

    # ── Summary Display ────────────────────────────────────────────────────
    console.print("\n[bold]Validation Summary[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Dimension", style="dim")
    table.add_column("Score", justify="right")

    for dim, score in report.dimensions.items():
        color = "green" if score >= 85 else "yellow" if score >= 70 else "red"
        table.add_row(dim, f"[{color}]{score:.1f}%[/{color}]")

    table.add_section()
    final_color = "green" if report.score >= 90 else "yellow" if report.score >= 70 else "red"
    table.add_row("[bold]TOTAL SCORE[/bold]", f"[{final_color}][bold]{report.score:.1f}%[/bold][/{final_color}]")
    console.print(table)

    # ── Verdict ────────────────────────────────────────────────────────────
    console.print(f"\n[bold]Status:[/bold] {report.status}")
    if report.summary:
        console.print(Panel(report.summary, title="Executive Summary"))

    # ── Critical Issues ────────────────────────────────────────────────────
    if report.critical_issues:
        console.print("\n[bold red]🚫 CRITICAL ISSUES (Blocking Artifacts):[/bold red]")
        for issue in report.critical_issues:
            console.print(f"- [red]{issue.title}:[/red] {issue.description}")

    # ── Artifact Generation ────────────────────────────────────────────────
    _write_artifacts(feature_name, report)
    if not report.runbook_eligible and not report.roadmap_eligible:
        console.print("\n[bold yellow]⚠️ Only VALIDATION_REPORT was generated.[/bold yellow]")

    if report.status == "FAILED" or report.score < 70:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
