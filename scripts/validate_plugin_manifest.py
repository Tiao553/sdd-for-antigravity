"""
Comprehensive Plugin Verification Script for AgentSpec
Validates manifest schema, mcp_config, hooks, skills, rules, agents, and kb.
"""
import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_plugin_manifest():
    manifest_path = ROOT / "plugin.json"
    assert manifest_path.exists(), "plugin.json not found"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert "$schema" in data, "plugin.json missing $schema"
    assert "name" in data, "plugin.json missing name"
    assert re.match(r"^[a-z0-9-_]+$", data["name"]), f"Invalid plugin name format: {data['name']}"
    assert "description" in data and len(data["description"]) > 10, "plugin.json missing valid description"
    
    if "suggestedPrompts" in data:
        assert len(data["suggestedPrompts"]) <= 3, "suggestedPrompts cannot exceed 3 items"
        
    if "logo" in data:
        logo_path = ROOT / data["logo"]
        assert logo_path.exists(), f"Logo file not found: {data['logo']}"
        
    print(f"[PASS] plugin.json is valid (name: {data['name']}, version: {data.get('version', 'N/A')})")

def test_mcp_config():
    mcp_path = ROOT / "mcp_config.json"
    assert mcp_path.exists(), "mcp_config.json not found"
    
    with open(mcp_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert "mcpServers" in data, "mcp_config.json missing mcpServers"
    servers = data["mcpServers"]
    assert "context7" in servers, "context7 missing in mcpServers"
    assert "sequential-thinking" in servers, "sequential-thinking missing in mcpServers"
    assert "github" in servers, "github missing in mcpServers"
    print(f"[PASS] mcp_config.json is valid ({len(servers)} servers declared)")

def test_hooks():
    hooks_path = ROOT / "hooks.json"
    assert hooks_path.exists(), "hooks.json not found"
    
    with open(hooks_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for hook_name, hook_def in data.items():
        if "PreToolUse" in hook_def:
            for item in hook_def["PreToolUse"]:
                for h in item.get("hooks", []):
                    cmd = h.get("command", "")
                    if cmd.startswith("python "):
                        script = cmd.split(" ")[1]
                        assert (ROOT / script).exists(), f"Hook script not found: {script}"
        if "SessionStart" in hook_def:
            for item in hook_def["SessionStart"]:
                cmd = item.get("command", "")
                if cmd.startswith("python "):
                    script = cmd.split(" ")[1]
                    assert (ROOT / script).exists(), f"Hook script not found: {script}"
                    
    print(f"[PASS] hooks.json is valid ({len(data)} hook groups)")

def test_skills():
    skills_dir = ROOT / "skills"
    assert skills_dir.exists(), "skills directory missing"
    
    skill_folders = [f for f in skills_dir.iterdir() if f.is_dir()]
    assert len(skill_folders) >= 35, f"Expected >= 35 skills, found {len(skill_folders)}"
    
    for folder in skill_folders:
        skill_file = folder / "SKILL.md"
        assert skill_file.exists(), f"SKILL.md missing in {folder.name}"
        
        content = skill_file.read_text(encoding="utf-8")
        assert content.startswith("---"), f"YAML frontmatter missing in {folder.name}/SKILL.md"
        
        # Check name and description in frontmatter
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        assert fm_match, f"Malformed frontmatter in {folder.name}/SKILL.md"
        fm_text = fm_match.group(1)
        
        assert re.search(r"^name:\s*.+", fm_text, re.MULTILINE), f"'name' missing in frontmatter of {folder.name}/SKILL.md"
        assert re.search(r"^description:\s*.+", fm_text, re.MULTILINE), f"'description' missing in frontmatter of {folder.name}/SKILL.md"
        
    print(f"[PASS] skills/ verified ({len(skill_folders)} skills with compliant SKILL.md)")

def test_rules_and_specialists():
    agents_rule = ROOT / "rules" / "AGENTS.md"
    assert agents_rule.exists(), "rules/AGENTS.md missing"
    rule_size = agents_rule.stat().st_size
    assert rule_size <= 24000, f"rules/AGENTS.md size ({rule_size} bytes) exceeds 24,000 bytes budget"
    
    routing_path = ROOT / "rules" / "routing.json"
    assert routing_path.exists(), "rules/routing.json missing"
    
    with open(routing_path, "r", encoding="utf-8") as f:
        routing = json.load(f)
        
    agents = routing.get("agents", [])
    assert len(agents) == 63, f"Expected 63 specialists, found {len(agents)}"
    
    for a in agents:
        agent_path = ROOT / a["path"]
        assert agent_path.exists(), f"Specialist rule file not found: {a['path']}"
        
    print(f"[PASS] rules/ verified: AGENTS.md ({rule_size} bytes) and 63 specialists in routing.json")

def test_subagents():
    agents_dir = ROOT / "agents"
    assert agents_dir.exists(), "agents directory missing"
    
    agent_files = list(agents_dir.glob("*.md"))
    assert len(agent_files) >= 5, f"Expected >= 5 subagents, found {len(agent_files)}"
    
    for af in agent_files:
        content = af.read_text(encoding="utf-8")
        assert "subagent: true" in content, f"subagent: true missing in {af.name}"
        assert "mainAgent: false" in content, f"mainAgent: false missing in {af.name}"
        
    print(f"[PASS] agents/ verified ({len(agent_files)} native subagents)")

def test_kb_and_sdd():
    kb_dir = ROOT / "kb"
    assert kb_dir.exists(), "kb directory missing"
    domains = [d for d in kb_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]
    assert len(domains) >= 25, f"Expected >= 25 KB domains, found {len(domains)}"
    
    sdd_dir = ROOT / "sdd"
    assert sdd_dir.exists(), "sdd directory missing"
    assert (sdd_dir / "templates").exists(), "sdd/templates missing"
    assert (sdd_dir / "architecture").exists(), "sdd/architecture missing"
    print(f"[PASS] kb/ and sdd/ verified ({len(domains)} KB domains and core SDD templates)")

if __name__ == "__main__":
    print("=== RUNNING AGENTSPEC PLUGIN VALIDATION SUITE ===")
    try:
        test_plugin_manifest()
        test_mcp_config()
        test_hooks()
        test_skills()
        test_rules_and_specialists()
        test_subagents()
        test_kb_and_sdd()
        print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY (100% COMPLIANT)!")
    except AssertionError as e:
        print(f"\n[VALIDATION FAILED] {e}", file=sys.stderr)
        sys.exit(1)
