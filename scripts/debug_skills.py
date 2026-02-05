import os
import re

def get_frontmatter(content):
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
    if not match:
        return ""
    return match.group(1)

def extract_field(content, field):
    frontmatter = get_frontmatter(content)
    if not frontmatter:
        return ""
    
    lines = frontmatter.split('\n')
    for i, line in enumerate(lines):
        if line.startswith(f"{field}:"):
            value = line[len(field)+1:].strip()
            if value == ">":
                multi_lines = []
                for next_line in lines[i+1:]:
                    if next_line.startswith('  ') or not next_line.strip():
                        multi_lines.append(next_line.strip())
                    else:
                        break
                return " ".join(multi_lines).strip()
            return value.strip('"\'')
    return ""

def extract_metadata(content, field):
    frontmatter = get_frontmatter(content)
    if not frontmatter:
        return []
    
    lines = frontmatter.split('\n')
    in_metadata = False
    metadata_indent = -1
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
            
        indent = len(line) - len(line.lstrip())
        
        if stripped.startswith("metadata:"):
            in_metadata = True
            metadata_indent = indent
            continue
            
        if in_metadata:
            if indent <= metadata_indent and stripped and not stripped.startswith('-'):
                # We left the metadata block
                if not stripped.startswith(f"{field}:"): # unless it was just the first field? No, metadata is a block
                    in_metadata = False
                    continue

            if stripped.startswith(f"{field}:"):
                value = stripped[len(field)+1:].strip()
                
                # Single line list [a, b]
                if value.startswith('[') and value.endswith(']'):
                    return [v.strip('"\' ') for v in value[1:-1].split(',')]
                
                # Single line scalar
                if value:
                    v = value.strip('"\'')
                    if v: return [v]
                    # if v is empty, it might be a multi-line list starting below
                
                # Multi-line list
                results = []
                for next_line in lines[i+1:]:
                    next_stripped = next_line.strip()
                    if not next_stripped:
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent > indent and next_stripped.startswith('-'):
                        results.append(next_stripped[1:].strip('"\' '))
                    elif next_indent > indent:
                        continue # continuation line or nested?
                    else:
                        break
                return results
    return []

repo_root = "/Users/arnoldobenitezvalero/Desktop/Proyectos Personales/Goals-Dashboard"
skills_dir = os.path.join(repo_root, ".agent", "skills")

for root, dirs, files in os.walk(skills_dir):
    if "SKILL.md" in files:
        skill_file = os.path.join(root, "SKILL.md")
        with open(skill_file, 'r') as f:
            content = f.read()
        name = extract_field(content, "name")
        scopes = extract_metadata(content, "scope")
        auto_invokes = extract_metadata(content, "auto_invoke")
        print(f"Skill: {name}")
        print(f"  Path: {os.path.relpath(skill_file, repo_root)}")
        print(f"  Scopes: {scopes}")
        print(f"  Auto-invokes: {auto_invokes}")
        print("-" * 20)
