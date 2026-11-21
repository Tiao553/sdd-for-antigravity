"""
tools.py — File readers and CLI tool wrappers for the /validate skill.

Responsibilities:
  1. SDD File Readers — read BRAINSTORM, DEFINE, DESIGN, BUILD_REPORT from disk
     and assemble them into an immutable ValidateContext Pydantic object.
  2. Code Tree Scanner — discover all implemented file paths under the feature directory.
  3. CLI Tool Wrappers — run ruff, mypy, pytest via subprocess and return structured results.

Design: DESIGN_VALIDATE_WORKFLOW.md v2.0
Security: Only whitelisted commands are executed (ruff check, mypy, pytest).
          No eval(), exec(), or arbitrary shell expansion.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from .schemas import ValidateContext

# ─── Constants ────────────────────────────────────────────────────────────────

SDD_FEATURES_DIR = Path(".github/sdd/features")
SDD_REPORTS_DIR = Path(".github/sdd/reports")
SKILLS_DIR = Path(".github/skills")

# Whitelisted commands — DO NOT add arbitrary commands here.
_ALLOWED_COMMANDS: set[str] = {"ruff", "mypy", "pytest"}


def _safe_run(command: List[str]) -> Dict[str, Any]:
    """
    Execute a whitelisted shell command safely via subprocess.

    Args:
        command: List of command parts (e.g. ["ruff", "check", "."]).

    Returns:
        Dict with stdout, stderr, and exit_code.

    Raises:
        ValueError: If the base command is not in the whitelist.
    """
    base = command[0] if command else ""
    if base not in _ALLOWED_COMMANDS:
        raise ValueError(
            f"Command '{base}' is not whitelisted. Allowed: {_ALLOWED_COMMANDS}"
        )

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
        }
    except FileNotFoundError:
        return {
            "stdout": "",
            "stderr": f"Command not found: {base}. Is it installed?",
            "exit_code": 127,
        }


# ─── SDD File Readers ─────────────────────────────────────────────────────────


def _feature_slug(feature_name: str) -> str:
    """Convert FEATURE_NAME into the kebab-case directory convention."""
    return feature_name.lower().replace("_", "-")


def find_feature_dir(feature_name: str) -> Path:
    """Return the feature directory, preferring the standard kebab-case path."""
    preferred = SDD_FEATURES_DIR / _feature_slug(feature_name)
    if preferred.exists():
        return preferred

    matches = sorted(SDD_FEATURES_DIR.rglob(f"DEFINE_{feature_name}.md"))
    if matches:
        return matches[0].parent

    matches = sorted(SDD_FEATURES_DIR.rglob(f"DESIGN_{feature_name}.md"))
    if matches:
        return matches[0].parent

    return preferred


def _read_sdd_file(feature_name: str, prefix: str, directories: List[Path]) -> str:
    """
    Read a single SDD document from disk.

    Searches for `{PREFIX}_{FEATURE_NAME}.md` in the given directories.
    Returns empty string if not found (graceful degradation for optional files).
    """
    filename = f"{prefix}_{feature_name}.md"
    for directory in directories:
        path = directory / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
    return ""


def scan_code_tree(feature_path: str) -> List[str]:
    """
    Discover all Python and config files under the given feature directory.

    Args:
        feature_path: Relative or absolute path to the feature root directory.

    Returns:
        Sorted list of file paths relative to the feature root.
    """
    root = Path(feature_path)
    if not root.exists():
        return []

    extensions = {".py", ".yaml", ".yml", ".toml", ".json", ".md"}
    return sorted(
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and p.suffix in extensions
    )


def read_sdd_context(feature_name: str) -> ValidateContext:
    """
    Build an immutable ValidateContext from SDD documents on disk.

    Reads (in order):
      - BRAINSTORM_{feature_name}.md (optional)
      - DEFINE_{feature_name}.md (required)
      - DESIGN_{feature_name}.md (required)
      - BUILD_REPORT_{feature_name}.md (required)

    Args:
        feature_name: The feature identifier (e.g. "VALIDATE_WORKFLOW").

    Returns:
        A fully populated ValidateContext Pydantic object.

    Raises:
        FileNotFoundError: If DEFINE or DESIGN documents are missing.
    """
    feature_dir = find_feature_dir(feature_name)
    sdd_dirs = [feature_dir, SDD_FEATURES_DIR]
    report_dirs = [feature_dir, SDD_REPORTS_DIR]

    define_content = _read_sdd_file(feature_name, "DEFINE", sdd_dirs)
    design_content = _read_sdd_file(feature_name, "DESIGN", sdd_dirs)
    build_report_content = _read_sdd_file(feature_name, "BUILD_REPORT", report_dirs)

    missing: List[str] = []
    if not define_content:
        missing.append(f"DEFINE_{feature_name}.md")
    if not design_content:
        missing.append(f"DESIGN_{feature_name}.md")
    if not build_report_content:
        missing.append(f"BUILD_REPORT_{feature_name}.md")
    if missing:
        raise FileNotFoundError(
            f"Required SDD files not found: {', '.join(missing)}. "
            "Run /define, /design, and /build first."
        )

    brainstorm_content = _read_sdd_file(feature_name, "BRAINSTORM", sdd_dirs)

    # Infer code tree from skill directory.
    # Convention tries multiple candidates in order:
    #   1. .github/skills/{kebab-full}  (e.g. validate-workflow)
    #   2. .github/skills/{first-word}  (e.g. validate — actual dir for this feature)
    kebab_full = _feature_slug(feature_name)
    first_word = kebab_full.split("-")[0]
    candidates = [
        str(SKILLS_DIR / kebab_full),
        str(SKILLS_DIR / first_word),
    ]
    code_tree: List[str] = []
    for candidate in candidates:
        tree = scan_code_tree(candidate)
        if tree:
            code_tree = [f"{candidate}/{f}" for f in tree]
            break

    return ValidateContext(
        feature_name=feature_name,
        brainstorm_content=brainstorm_content,
        define_content=define_content,
        design_content=design_content,
        build_report_content=build_report_content,
        code_tree=code_tree,
    )


# ─── CLI Tool Wrappers ────────────────────────────────────────────────────────


def run_ruff(path: str) -> Dict[str, Any]:
    """
    Run `ruff check` on the given path and return structured output.

    Returns:
        Dict with `count` (int), `issues` (list of ruff JSON objects), `raw` (str).
    """
    res = _safe_run(["ruff", "check", path, "--output-format", "json"])

    issues: List[Dict[str, Any]] = []
    if res["stdout"]:
        try:
            issues = json.loads(res["stdout"])
        except json.JSONDecodeError:
            pass

    return {
        "count": len(issues),
        "issues": issues,
        "raw": res["stdout"] or res["stderr"],
        "exit_code": res["exit_code"],
    }


def run_mypy(path: str) -> Dict[str, Any]:
    """
    Run `mypy` on the given path and return structured output.

    Returns:
        Dict with `count` (int, number of type errors), `raw` (str).
    """
    res = _safe_run(["mypy", path, "--ignore-missing-imports", "--no-error-summary"])

    error_count = 0
    if res["exit_code"] != 0 and res["stdout"]:
        # Mypy format: "path/file.py:line: error: message  [error-code]"
        error_lines = [
            line for line in res["stdout"].splitlines() if ": error:" in line
        ]
        error_count = len(error_lines)

    return {
        "count": error_count,
        "raw": res["stdout"] or res["stderr"],
        "exit_code": res["exit_code"],
    }


def run_pytest(path: str) -> Dict[str, Any]:
    """
    Run `pytest` on the given path and return structured output.

    Returns:
        Dict with `exit_code`, `stdout`, `stderr`.
    """
    res = _safe_run(["pytest", path, "-v", "--tb=short"])
    return {
        "exit_code": res["exit_code"],
        "stdout": res["stdout"],
        "stderr": res["stderr"],
    }


def get_test_coverage(path: str) -> float:
    """
    Run `pytest --cov` and extract the total coverage percentage.

    Returns:
        Float coverage percentage (0.0 if not determinable).
    """
    res = _safe_run(["pytest", f"--cov={path}", path, "--cov-report=term-missing", "-q"])

    # Mypy format: "TOTAL    nnn    nnn    nn%"
    match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", res["stdout"])
    if match:
        return float(match.group(1))
    return 0.0
