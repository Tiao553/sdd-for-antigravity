"""
llm.py — Shared LLM factory for all crews in the /validate skill.

Loads credentials from .env at project root via python-dotenv.
Compatible with crewai 0.28.x (uses langchain_openai.ChatOpenAI directly).
Supports OpenRouter (set OPENAI_API_BASE=https://openrouter.ai/api/v1 in .env).
"""

from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv() -> None:
    """Load .env from the project root (two levels up from scripts/)."""
    try:
        from dotenv import load_dotenv

        # scripts/ → validate/ → skills/ → .agents/ → project root
        project_root = Path(__file__).parent.parent.parent.parent.parent
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=False)
    except ImportError:
        pass  # python-dotenv not installed; rely on environment variables


def get_llm(model: str = "openai/gpt-5.5"):
    """
    Build a LangChain ChatOpenAI instance from .env or environment variables.

    Resolution order (first wins):
      1. Already-set environment variables (export in shell)
      2. Values in .env at project root

    Required (.env or env var):
      OPENAI_API_KEY  — API key (OpenRouter or OpenAI)

    Optional:
      OPENAI_API_BASE — Base URL override (e.g. https://openrouter.ai/api/v1)
      CREWAI_MODEL    — Model name (e.g. openai/gpt-4o-mini)
    """
    _load_dotenv()

    from langchain_openai import ChatOpenAI

    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_API_BASE", None)
    model_name = os.environ.get("CREWAI_MODEL", model)

    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. "
            "Add it to your .env file or export it in the shell."
        )

    kwargs: dict = {"model": model_name, "api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)
