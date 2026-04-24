import os

rules_dir = r'.\sdd-for-antigravity\.agents\rules'

for root, dirs, files in os.walk(rules_dir):
    for file in files:
        if file.endswith('.md') and file != 'default.md':
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if len(lines) > 1 and 'trigger:' not in lines[1]:
                # Insert trigger: model_decision at line 2
                lines.insert(1, 'trigger: model_decision\n')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"Updated {filepath}")
