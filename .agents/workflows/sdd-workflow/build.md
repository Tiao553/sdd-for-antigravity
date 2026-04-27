---
name: build
description: Execute implementation with on-the-fly task generation (Phase 3)
---

# Build Command

> Execute implementation with on-the-fly task generation (Phase 3)

## Usage

```bash
/build <design-file>
```

## Examples

```bash
/build .agents/sdd/features/DESIGN_NOTIFICATION_SYSTEM.md
/build DESIGN_USER_AUTH.md
```

---

## Overview

This is **Phase 3** of the 5-phase AgentSpec workflow:

```text
Phase 0: /brainstorm → .agents/sdd/features/BRAINSTORM_{FEATURE}.md (optional)
Phase 1: /define     → .agents/sdd/features/DEFINE_{FEATURE}.md
Phase 2: /design   → .agents/sdd/features/DESIGN_{FEATURE}.md
Phase 3: /build    → Code + .agents/sdd/reports/BUILD_REPORT_{FEATURE}.md (THIS COMMAND)
Phase 4: /ship     → .agents/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md
```

The `/build` command executes the implementation, generating tasks on-the-fly from the file manifest.

---

## What This Command Does

1. **Parse** - Extract Implementation Chunks from DESIGN
2. **Plan & Task** - ALWAYS create/update `implementation_plan.md` and `task.md` with extreme depth
3. **Isolate** - Identify the next `⏳ Pending` chunk
4. **Execute** - Create files for that specific chunk with verification
5. **Persist State** - ALWAYS update `.agents/sdd/reports/BUILD_REPORT_{FEATURE}.md` after every file/interaction
6. **Report** - Finalize chunk status in the report and STOP

---

## Process

### Step 1: Load Context

```markdown
Read(.agents/sdd/features/DESIGN_{FEATURE}.md)
Read(.agents/sdd/features/DEFINE_{FEATURE}.md)
Read(GEMINI.md)
```

### Step 2: Planning & Task Extraction (Mandatory)

Before writing any code, you MUST generate or update two critical artifacts in the conversation's artifact directory:

1. **`implementation_plan.md`**:
   - **Extreme Depth**: Detail every technical decision, edge case, and architectural pattern.
   - **Agent Assignments**: A table mapping every file to a specialist agent found in `routing.json`.
   - **Workflow Reference**: Explicitly link to `.agents/workflows/sdd-workflow/build.md`.
   - **Agent References**: Link to each specialist's `.md` file in `.agents/rules/`.

2. **`task.md`**:
   - **Granularity**: Break down chunks into tiny, verifiable sub-tasks.
   - **Allocation**: State which agent is responsible for each sub-task.

```markdown
Target: Chunk 1 - Foundation & State
```

```markdown
From DESIGN file manifest:
| File | Action | Agent Allocation (from routing.json) |
|------|--------|------------------------------------|

Generate:
- [ ] Sub-task 1.1: [Agent] Description
- [ ] Sub-task 1.2: [Agent] Description
- [ ] ...
```

### Step 3: Order by Dependencies

Analyze imports and dependencies to determine execution order.

### Step 4: Execute Chunk Files

**First Action:**
Create an isolated directory for the feature:
```bash
mkdir -p {FEATURE}
```

**For each file:**

1. **Delegate (JIT Persona)** - Check the `implementation_plan.md` for the assigned agent.
2. **Reference Check (MANDATORY)** - You MUST read the specialist's rule file (from `routing.json`) AND the `routing.json` itself before execution.
3. **Banner Protocol** - Print `> [!IMPORTANT] Invoking Specialist: [Agent Name] (Path: [Agent Path])`.
4. **Write** - Create the file inside the isolated directory applying the exact rules, constraints, and code patterns from the invoked specialist and the `DESIGN` doc.
5. **Verify** - Run verification command (lint, type check, import test).
6. **Mark Complete** - Update progress in `task.md`.
7. **Persist (MANDATORY)** - Immediately update `.agents/sdd/reports/BUILD_REPORT_{FEATURE}.md`. This is the **System of Record (SoR)** that allows you to resume work on any computer via Git.

### Step 5: Run Full Validation (For the Chunk)

After the chunk files are created:

```bash
# Lint check
ruff check .

# Type check (if applicable)
mypy .

# Run tests
pytest
```

### Step 6: Update Living Report

Update the `Chunk Execution Log` in the `BUILD_REPORT_{FEATURE}.md`:
- If all checks pass: Mark as ✅ Passed
- If checks fail (and auto-retries exhausted): Mark as ❌ Failed, log the error.

---

## Output

| Artifact | Location |
|----------|----------|
| **Code** | As specified in DESIGN file manifest |
| **Build Report** | `.agents/sdd/reports/BUILD_REPORT_{FEATURE}.md` |

**Next Step:** `/ship .agents/sdd/features/DEFINE_{FEATURE}.md` (when ready)

---

## Execution Loop

The build agent follows this loop for each `/build` invocation:

```text
┌─────────────────────────────────────────────────────┐
│                 CHUNK EXECUTION                      │
├─────────────────────────────────────────────────────┤
│  1. Identify next Pending chunk from BUILD_REPORT   │
│  2. Write code for files in this chunk              │
│  3. Run verification command (ruff, mypy, pytest)   │
│     └─ If FAIL → Fix and retry (max 3)             │
│  4. Update BUILD_REPORT chunk status (✅ or ❌)       │
│  5. STOP. Ask user to proceed to next chunk.        │
└─────────────────────────────────────────────────────┘
```

---

## Quality Gate

Before marking complete, verify:

```text
[ ] All files from manifest created
[ ] All verification commands pass
[ ] Lint check passes
[ ] Tests pass (if applicable)
[ ] No TODO comments left in code
[ ] Build report generated
```

---

## Tips

1. **Follow the DESIGN** - Don't improvise, use the code patterns
2. **Chunk Execution** - Execute ONLY the next pending chunk. Do NOT build the whole project at once.
3. **Verify Incrementally** - Use the `run_command` tool to test after the chunk is built (`ruff check`, `mypy`, `pytest`).
4. **Fix Forward** - If a test fails, read the output using `command_status`, fix the code, and retry up to 3 times.
5. **Living Artifact** - Keep the `BUILD_REPORT` updated. It is the source of truth for execution state.

---

## Handling Issues During Build

If you encounter issues:

| Issue | Action |
|-------|--------|
| Missing requirement | Use `/iterate` to update DEFINE |
| Architecture problem | Use `/iterate` to update DESIGN |
| Simple bug | Fix immediately and continue |
| Major blocker | Stop and report in build report |

---

## References

- Agent: `.agents/rules/workflow/build-agent.md`
- Template: `.agents/sdd/templates/BUILD_REPORT_TEMPLATE.md`
- Contracts: `.agents/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- Next Phase: `.agents/workflows/workflow/ship.md`
