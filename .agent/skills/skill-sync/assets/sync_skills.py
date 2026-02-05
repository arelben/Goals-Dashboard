import os
import re
import sys
import argparse
import tempfile
import shutil

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
                    return [value.strip('"\'')]
                
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
                        continue # continuation line?
                    else:
                        break
                return results
    return []

def main():
    parser = argparse.ArgumentParser(description="Sync skill metadata to AGENTS.md")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    parser.add_argument("--scope", help="Filter by scope")
    args = parser.parse_args()

    # Determine paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # assets -> skill-sync -> skills -> .agent -> root
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))
    skills_dir = os.path.join(repo_root, ".agent", "skills")

    print(f"Skill Sync - Updating AGENTS.md Auto-invoke sections")
    print("========================================================")
    print(f"Repo Root: {repo_root}")
    print(f"Skills Dir: {skills_dir}")
    print("")

    scope_skills = {} # scope -> {skill_name: [auto_invokes]}

    # Find all SKILL.md files
    for root, dirs, files in os.walk(skills_dir):
        if "SKILL.md" in files:
            skill_file = os.path.join(root, "SKILL.md")
            with open(skill_file, 'r') as f:
                content = f.read()
            
            name = extract_field(content, "name")
            scopes = extract_metadata(content, "scope")
            auto_invokes = extract_metadata(content, "auto_invoke")
            
            if not name or not scopes or not auto_invokes:
                continue
                
            for scope in scopes:
                if args.scope and scope != args.scope:
                    continue
                
                if scope not in scope_skills:
                    scope_skills[scope] = {}
                
                if name not in scope_skills[scope]:
                    scope_skills[scope][name] = []
                
                scope_skills[scope][name].extend(auto_invokes)

    # Scopes to update
    scope_to_path = {
        "root": os.path.join(repo_root, "AGENTS.md"),
        "ui": os.path.join(repo_root, "ui", "AGENTS.md"),
        "api": os.path.join(repo_root, "api", "AGENTS.md"),
        "sdk": os.path.join(repo_root, "prowler", "AGENTS.md"),
        "mcp_server": os.path.join(repo_root, "mcp_server", "AGENTS.md"),
    }

    for scope in sorted(scope_skills.keys()):
        agents_path = scope_to_path.get(scope)
        if not agents_path or not os.path.exists(agents_path):
            print(f"Warning: No AGENTS.md found for scope '{scope}' at {agents_path}")
            continue

        print(f"Processing: {scope} -> {os.path.relpath(agents_path, repo_root)}")

        # Build section content
        rows = []
        for skill_name, actions in scope_skills[scope].items():
            for action in actions:
                rows.append((action, skill_name))
        
        # Sort rows by action then skill_name
        rows.sort()
        
        table_lines = [
            "### Auto-invoke Skills",
            "",
            "When performing these actions, ALWAYS invoke the corresponding skill FIRST:",
            "",
            "| Action | Skill |",
            "|--------|-------|"
        ]
        for action, skill in rows:
            table_lines.append(f"| {action} | `{skill}` |")
        
        new_section = "\n".join(table_lines)

        if args.dry_run:
            print(f"[DRY RUN] Would update {agents_path} with:")
            print(new_section)
            print("")
            continue

        with open(agents_path, 'r') as f:
            lines = f.readlines()

        # Find the section to replace or insert
        output_lines = []
        skip = False
        inserted = False
        
        # Check if section exists (support ## and ###)
        section_pattern = r'^#+ Auto-invoke Skills'
        has_section = any(re.match(section_pattern, line) for line in lines)
        
        if has_section:
            for i, line in enumerate(lines):
                if re.match(section_pattern, line):
                    output_lines.append(new_section + "\n")
                    skip = True
                    inserted = True
                    continue
                
                if skip:
                    if line.startswith("---") or line.startswith("## ") or line.startswith("### "):
                        skip = False
                        # Avoid double spacing if the next line is a header
                        output_lines.append("\n" + line)
                    continue
                
                output_lines.append(line)
        else:
            # Insert after Skills Reference blockquote or after Critical Rules
            insertion_point = -1
            for i, line in enumerate(lines):
                if ")`" in line and "SKILL.md)" in line:
                    insertion_point = i
                elif "## Critical Rules" in line and insertion_point == -1:
                    # Fallback to after Critical Rules if Skills Reference not found
                    insertion_point = i
            
            if insertion_point != -1:
                for i, line in enumerate(lines):
                    output_lines.append(line)
                    if i == insertion_point:
                        output_lines.append("\n" + new_section + "\n")
                        inserted = True
            else:
                # Appending to end
                output_lines = lines + ["\n", new_section, "\n"]
                inserted = True

        with open(agents_path, 'w') as f:
            f.writelines(output_lines)
        
        print(f"  \u2713 {'Updated' if has_section else 'Inserted'} Auto-invoke section")

    print("\nDone!")

if __name__ == "__main__":
    main()
