#!/usr/bin/env python3
"""
Ensures all specialist rules in rules/specialists/ declare trigger: model_decision.
"""
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT_DIR / "rules" / "specialists"

def update_triggers():
    updated = 0
    for root, _, files in os.walk(RULES_DIR):
        for file in files:
            if file.endswith('.md') and file not in ('default.md', '_template.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                if len(lines) > 1 and 'trigger:' not in lines[1]:
                    lines.insert(1, 'trigger: model_decision\n')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    updated += 1
                    print(f"Updated trigger in: {filepath}")

    print(f"Completed trigger verification. Updated {updated} files.")

if __name__ == "__main__":
    update_triggers()
