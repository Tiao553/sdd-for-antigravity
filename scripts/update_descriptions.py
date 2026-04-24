import json
import os
import re

def optimize_description(desc):
    desc = desc.strip()
    if desc.startswith("Apply this rule"):
        return desc

    # Get the first sentence to keep it short and punchy
    first_sentence = desc.split('. ')[0]

    if first_sentence:
        # Avoid double 'a(n)' if it already starts with one, but let's just use a simple prefix
        first_letter = first_sentence[0].lower()
        rest = first_sentence[1:]

        # Determine prefix
        prefix = "Apply this rule when you need a(n)"
        if first_sentence.lower().startswith("expert") or first_sentence.lower().startswith("elite") or first_sentence.lower().startswith("apache"):
            prefix = "Apply this rule when you need an"
        elif first_sentence.lower().startswith("specialist"):
            prefix = "Apply this rule when you need a"

        transformed = f"Apply this rule when you need a {first_letter}{rest}"

        # Clean up some grammar
        transformed = transformed.replace("a a ", "a ").replace("a an ", "an ").replace("a e", "an e").replace("a a", "an a")

        if not transformed.endswith('.'):
            transformed += '.'

        # truncate to 240 chars safely
        if len(transformed) > 240:
            transformed = transformed[:237] + "..."

        return transformed
    return desc

def update_yaml_description(content, new_desc):
    # Escape quotes
    safe_desc = new_desc.replace('"', '\\"')

    # Match multiline description
    multiline_pattern = re.compile(r'^(description:\s*[|>]\s*\n(?:[ \t]+.*\n)+)', re.MULTILINE)
    if multiline_pattern.search(content):
        return multiline_pattern.sub(f'description: "{safe_desc}"\n', content)

    # Match single line description
    single_line_pattern = re.compile(r'^(description:.*)$', re.MULTILINE)
    if single_line_pattern.search(content):
        return single_line_pattern.sub(f'description: "{safe_desc}"', content)

    return content

def process_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    routing_path = os.path.join(project_root, ".agents", "rules", "routing.json")
    print(f"Loading {routing_path}...")

    try:
        with open(routing_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {routing_path}: {e}")
        return

    updated_count = 0
    for agent in data.get("agents", []):
        old_desc = agent.get("description", "")
        new_desc = optimize_description(old_desc)
        agent["description"] = new_desc

        md_path = agent.get("path")
        if md_path:
            # Handle mixed slashes and join safely
            md_path_normalized = md_path.replace("/", os.sep)
            abs_md_path = os.path.join(project_root, md_path_normalized)
            if os.path.exists(abs_md_path):
                try:
                    with open(abs_md_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    new_content = update_yaml_description(content, new_desc)

                    if new_content != content:
                        with open(abs_md_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        updated_count += 1
                        print(f"Updated: {abs_md_path}")
                except Exception as e:
                    print(f"Error updating {abs_md_path}: {e}")
            else:
                print(f"Warning: File not found {abs_md_path}")

    try:
        with open(routing_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {routing_path}")
    except Exception as e:
        print(f"Error saving {routing_path}: {e}")

    print(f"Successfully updated {updated_count} markdown files and the routing.json.")

if __name__ == "__main__":
    process_all()
