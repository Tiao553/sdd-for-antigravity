"""
AgentSpec Security Pre-Hook
Intercepts command execution to prevent accidental data loss or destructive operations.
"""
import sys
import re

DENIED_PATTERNS = [
    r"\brm\s+-rf\s+[/~]",
    r"\bdel\s+/s\s+/q\s+[C-Z]:\\",
    r"\bDROP\s+(DATABASE|SCHEMA|TABLESPACE)\b",
    r"\bgit\s+push\s+.*--force\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bTRUNCATE\s+TABLE\s+prod",
]

def check_command(cmd_string: str) -> bool:
    for pattern in DENIED_PATTERNS:
        if re.search(pattern, cmd_string, re.IGNORECASE):
            print(f"[SECURITY BLOCKED] Command blocked by AgentSpec Security Hook: Matches denied pattern '{pattern}'", file=sys.stderr)
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        if not check_command(cmd):
            sys.exit(1)
    sys.exit(0)
