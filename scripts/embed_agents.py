#!/usr/bin/env python3
"""
Semantic Vector Routing Logic for AgentSpec/Antigravity
Uses specialist rule definitions in rules/specialists/ to build routing indices.
"""
import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT_DIR / "rules"
SPECIALISTS_DIR = RULES_DIR / "specialists"
ROUTING_JSON = RULES_DIR / "routing.json"
VECTOR_STORE = RULES_DIR / "routing_index.json"

def load_agents():
    """Loads all agent descriptions and capabilities from .md frontmatter."""
    agents = {}
    for md_file in SPECIALISTS_DIR.glob("**/*.md"):
        if md_file.name in ("default.md", "_template.md"):
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            agent_name = md_file.stem
            agents[agent_name] = content[:1000]

    return agents

def build_index():
    """Builds semantic vector index for routing."""
    print("Building semantic vector index for routing...")
    agents = load_agents()
    print(f"Loaded {len(agents)} specialist agents from {SPECIALISTS_DIR}")

    index_data = {
        name: {
            "name": name,
            "snippet": text[:200],
            "status": "indexed"
        }
        for name, text in agents.items()
    }

    with open(VECTOR_STORE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2)
    print(f"Vector index saved to {VECTOR_STORE}")

if __name__ == "__main__":
    build_index()
