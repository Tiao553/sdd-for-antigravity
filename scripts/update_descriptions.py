#!/usr/bin/env python3
"""
Optimizes description triggers in rules/specialists/ and rules/routing.json (< 250 chars).
"""
import json
import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT_DIR / "rules"
ROUTING_PATH = RULES_DIR / "routing.json"

def optimize_description(desc):
    desc = desc.strip()
    if desc.startswith("Apply this rule"):
        return desc

    first_sentence = desc.split('. ')[0]

    if first_sentence:
        first_letter = first_sentence[0].lower()
        rest = first_sentence[1:]

        prefix = "Apply this rule when you need a"
        if first_sentence.lower().startswith(("expert", "elite", "apache", "orchestration")):
            prefix = "Apply this rule when you need an"

        transformed = f"{prefix} {first_letter}{rest}"
        transformed = (
            transformed.replace("a a ", "a ")
            .replace("a an ", "an ")
            .replace("a e", "an e")
            .replace("a a", "an a")
        )

        if not transformed.endswith('.'):
            transformed += '.'

        if len(transformed) > 240:
            transformed = transformed[:237] + "..."

        return transformed
    return desc

def update_yaml_description(content, new_desc):
    safe_desc = new_desc.replace('"', '\\"')

    multiline_pattern = re.compile(r'^(description:\s*[|>]\s*\n(?:[ \t]+.*\n)+)', re.MULTILINE)
    if multiline_pattern.search(content):
        return multiline_pattern.sub(f'description: "{safe_desc}"\n', content)

    single_line_pattern = re.compile(r'^(description:.*)$', re.MULTILINE)
    if single_line_pattern.search(content):
        return single_line_pattern.sub(f'description: "{safe_desc}"', content)

    return content

def process_all():
    print(f"Loading {ROUTING_PATH}...")
    if not ROUTING_PATH.exists():
        print(f"Error: {ROUTING_PATH} does not exist.")
        return

    with open(ROUTING_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_count = 0
    for agent in data.get("agents", []):
        old_desc = agent.get("description", "")
        new_desc = optimize_description(old_desc)
        agent["description"] = new_desc

        md_path = agent.get("path")
        if md_path:
            abs_md_path = ROOT_DIR / md_path
            if abs_md_path.exists():
                content = abs_md_path.read_text(encoding="utf-8")
                new_content = update_yaml_description(content, new_desc)
                if new_content != content:
                    abs_md_path.write_text(new_content, encoding="utf-8")
                    updated_count += 1
            else:
                print(f"Warning: File not found {abs_md_path}")

    with open(ROUTING_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully verified/updated {updated_count} specialist markdown files and rules/routing.json.")

if __name__ == "__main__":
    process_all()
