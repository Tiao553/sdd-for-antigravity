"""
schemas.py — Pydantic contracts for the /validate multi-crew workflow.

ALL inter-crew communication passes through these models. They are the single
source of truth for data shape across Orchestrator → SpecCrew → CodeCrew →
DeliveryCrew → CouncilCrew.

Design: DESIGN_VALIDATE_WORKFLOW.md v2.0
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ─── Severity ────────────────────────────────────────────────────────────────


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ─── Finding (shared across all crews) ───────────────────────────────────────


class Finding(BaseModel):
    """A single issue or observation surfaced by any crew agent."""

    title: str = Field(..., description="Short title for the finding")
    description: str = Field(..., description="Detailed explanation of the issue")
    severity: Severity
    category: str = Field(
        ...,
        description="Domain: Architecture | Logic | Style | DevOps | Security | Coverage",
    )
    file_path: Optional[str] = Field(None, description="Affected file path, if applicable")
    line_number: Optional[int] = Field(None, description="Affected line number, if applicable")


# ─── ValidateContext — built ONCE by Orchestrator, immutable ─────────────────


class ValidateContext(BaseModel):
    """
    Immutable shared context built once by the Orchestrator and passed to ALL crews.

    No crew modifies this object. Each crew produces its own separate output model.
    Prevents context drift and hallucination across the multi-crew pipeline.
    """

    feature_name: str = Field(..., description="Feature name (e.g. VALIDATE_WORKFLOW)")
    brainstorm_content: str = Field(
        default="", description="Raw text of BRAINSTORM_{FEATURE}.md (optional)"
    )
    define_content: str = Field(..., description="Raw text of DEFINE_{FEATURE}.md")
    design_content: str = Field(..., description="Raw text of DESIGN_{FEATURE}.md")
    build_report_content: str = Field(..., description="Raw text of BUILD_REPORT_{FEATURE}.md")
    code_tree: List[str] = Field(
        default_factory=list,
        description="List of all implemented file paths discovered under the feature directory",
    )


# ─── SpecReport — output of SpecCrew (flow 1.1) ──────────────────────────────


class SpecReport(BaseModel):
    """
    Output of SpecCrew (Hierarchical · 4 agents: MGR, ARC, ENG, SWE).
    Validates the implementation against DEFINE requirements and DESIGN intent.
    """

    feature: str
    alignment_score: float = Field(
        ..., ge=0, le=100, description="Spec alignment score (Spec Alignment dimension)"
    )
    architecture_score: float = Field(
        ..., ge=0, le=100, description="Architecture fidelity score (Architecture Fidelity dimension)"
    )
    requirement_coverage: float = Field(
        ..., ge=0, le=100, description="% of DEFINE requirements with implementation evidence"
    )
    findings: List[Finding] = Field(default_factory=list)
    status: str = Field(..., description="PASSED | WARNING | FAILED")


# ─── CodeReport — output of CodeCrew (flow 1.2) ──────────────────────────────


class CodeReport(BaseModel):
    """
    Output of CodeCrew (Hierarchical · 4 agents: MGR, SWE, ENG, OPS).
    Performs technical audit: lint, type safety, tests, and DevOps hygiene.
    """

    feature: str
    quality_score: float = Field(
        ..., ge=0, le=100, description="Code quality score (Code Quality dimension)"
    )
    devops_score: float = Field(
        ..., ge=0, le=100, description="DevOps/Security score (Security & DevOps dimension)"
    )
    test_coverage: Optional[float] = Field(
        None, ge=0, le=100, description="Test coverage % from pytest-cov (if available)"
    )
    lint_issues: int = Field(..., ge=0, description="Number of ruff issues found")
    type_errors: int = Field(..., ge=0, description="Number of mypy type errors found")
    findings: List[Finding] = Field(default_factory=list)
    status: str = Field(..., description="PASSED | WARNING | FAILED")


# ─── DeliveryDelta — output of DeliveryCrew ──────────────────────────────────


class RequirementStatus(str, Enum):
    DELIVERED = "DELIVERED"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"


class DeliveryDelta(BaseModel):
    """
    Output of DeliveryCrew (Sequential · 2 agents: CMP, GAP).
    Compares the 'As-Designed' intent against the 'As-Built' state.
    """

    feature: str
    missing_files: List[str] = Field(
        default_factory=list,
        description="Files in DESIGN manifest that were not found in code_tree",
    )
    unexpected_files: List[str] = Field(
        default_factory=list,
        description="Files in code_tree not mentioned in DESIGN manifest",
    )
    logic_gaps: List[str] = Field(
        default_factory=list,
        description="Functional gaps identified by CMP agent: features planned but not implemented",
    )
    requirement_map: Dict[str, RequirementStatus] = Field(
        default_factory=dict,
        description="Mapping of DEFINE requirement IDs to their delivery status",
    )
    delta_score: float = Field(
        ..., ge=0, le=100, description="Delivery completeness score (0=nothing delivered, 100=all delivered)"
    )
    status: str = Field(..., description="PASSED | WARNING | FAILED")


# ─── ValidationReport — output of CouncilCrew (final verdict) ────────────────


class ValidationReport(BaseModel):
    """
    Final output of CouncilCrew (Sequential · 3 agents: JDG, RPT, PRD).
    Computes the weighted 5-dimension score and determines artifact eligibility.

    Scoring formula (from DESIGN v2.0):
        score = spec_report.alignment_score * 0.30
              + code_report.quality_score   * 0.25
              + spec_report.architecture_score * 0.20
              + code_report.devops_score    * 0.15
              + prd_score                   * 0.10
    """

    feature: str
    score: float = Field(..., ge=0, le=100, description="Final weighted validation score")
    status: str = Field(..., description="PASSED | WARNING | FAILED")
    dimensions: Dict[str, float] = Field(
        default_factory=lambda: {
            "Spec Alignment": 0.0,
            "Code Quality": 0.0,
            "Architecture Fidelity": 0.0,
            "Security & DevOps": 0.0,
            "Production Readiness": 0.0,
        },
        description="Per-dimension scores (each 0-100)",
    )
    critical_issues: List[Finding] = Field(
        default_factory=list,
        description="All findings with severity=CRITICAL that block runbook generation",
    )
    findings: List[Finding] = Field(default_factory=list, description="All non-critical findings")
    runbook_eligible: bool = Field(
        ..., description="True if score >= 90 AND zero CRITICAL issues"
    )
    roadmap_eligible: bool = Field(
        ..., description="True if score in [70, 89] AND zero CRITICAL issues"
    )
    summary: Optional[str] = Field(None, description="Executive summary from RPT agent")
