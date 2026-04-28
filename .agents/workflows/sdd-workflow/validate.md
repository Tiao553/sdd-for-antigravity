---
name: validate
description: Multi-agent quality gate for architectural and code validation (Phase 3.5)
---

# /validate — Quality Gate (Phase 3.5)

> Reads the `validate` skill and executes the multi-crew validation pipeline.

## Usage

```bash
/validate <FEATURE_NAME>
```

## Skill

Delegates all execution to: `.agents/skills/validate/skill.md`

## Execution

### Environment setup
```bash
export OPENAI_API_KEY='your-key-here'
export OPENAI_API_BASE='https://openrouter.ai/api/v1'  # OpenRouter
```

### Run
```bash
cd <project-root>
python3 .agents/skills/validate/scripts/main.py <FEATURE_NAME>
```

## Output Artifacts

| Score | CRITICAL Issues | Artifact |
|-------|----------------|----------|
| ≥ 90  | None | `RUNBOOK_{FEATURE}.md` |
| 70–89 | None | `ROADMAP_{FEATURE}.md` |
| < 70  | Any  | None, exit code 1 |

## References

- Skill: `.agents/skills/validate/skill.md`
- Design: `.agents/sdd/features/DESIGN_VALIDATE_WORKFLOW.md`
- Architecture: `docs/validate-crew-architecture.html`
- Next: `.agents/workflows/sdd-workflow/ship.md`
