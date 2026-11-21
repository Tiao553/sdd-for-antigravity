# Changelog

All notable changes to the AgentSpec framework are documented in this file.

## [3.1.0] - 2026-11-21

### Added
- **Official Antigravity Plugin Support:** Added `plugin.json` (schema v1), `mcp_config.json`, `hooks.json`, and `assets/logo.svg`.
- **First-Class Skills (`skills/`):** Migrated 34 legacy workflows into 38 native skills with slash command integration (`/pipeline`, `/define`, `/brainstorm`, `/validate`, `/sdd-init`, etc.).
- **Subagents (`agents/`):** Added 5 native subagents (`security-auditor`, `spec-crew`, `code-crew`, `delivery-crew`, `council-crew`) for parallel task delegation and security auditing.
- **SDD Workspace Initializer:** Added `/sdd-init` skill to scaffold `.agents/sdd/` in external user projects.
- **Automated Validation Suite:** Added `scripts/validate_plugin_manifest.py` verifying manifest compliance, skills frontmatter, specialist routing, and rule sizes.

### Changed
- **Router & JIT Specialist Layout:** Moved specialist agents to `rules/specialists/` with consolidated `rules/AGENTS.md` and updated `rules/routing.json`.
- **Global KB & SDD Migration:** Embedded 26 knowledge base domains in `kb/` and templates in `sdd/` at the root of the plugin.

### Removed
- Deprecated `.agents/workflows/` and `.agents/skills/` directories in compliance with modern Antigravity customization standards.
