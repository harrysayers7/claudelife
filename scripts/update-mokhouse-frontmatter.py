#!/usr/bin/env python3
"""Update MOK HOUSE project frontmatter with type: project and relation: mokhouse."""

import os
import re
from pathlib import Path

def update_frontmatter(file_path):
    """Update frontmatter in a markdown file."""
    content = file_path.read_text()

    # Check if it has project name field (indicates it's a project file)
    if 'project name:' not in content:
        print(f"⊘ Skipped (not a project): {file_path.name}")
        return False

    # Split frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"⊘ Skipped (no frontmatter): {file_path.name}")
        return False

    frontmatter = parts[1]
    body = parts[2]

    # Update relation
    if 'relation:' in frontmatter:
        # Replace mokhouse-projects with mokhouse
        frontmatter = re.sub(
            r'relation:\s*\n\s*-\s*"\[\[mokhouse-projects\]\]"',
            'relation:\n  - "[[mokhouse]]"',
            frontmatter
        )
    else:
        # Add relation if missing
        frontmatter = 'relation:\n  - "[[mokhouse]]"\n' + frontmatter

    # Add or update type
    if 'type:' in frontmatter:
        frontmatter = re.sub(r'type:\s*.*', 'type: project', frontmatter)
    else:
        # Add type after relation
        frontmatter = re.sub(
            r'(relation:\s*\n\s*-\s*"\[\[mokhouse\]\]")',
            r'\1\ntype: project',
            frontmatter
        )

    # Reconstruct file
    new_content = f"---{frontmatter}---{body}"

    file_path.write_text(new_content)
    return True

# Process active projects
active_dir = Path("/Users/harrysayers/Developer/claudelife/02-projects/mokhouse")
archive_dir = active_dir / "archive"

updated_count = 0

print("Processing active projects...")
for md_file in active_dir.glob("*.md"):
    if md_file.name != "CLAUDE.md":
        if update_frontmatter(md_file):
            print(f"✓ Updated: {md_file.name}")
            updated_count += 1

# Process subdirectories (like 036-nintendo)
for subdir in active_dir.iterdir():
    if subdir.is_dir() and subdir.name != "archive":
        for md_file in subdir.glob("*.md"):
            if update_frontmatter(md_file):
                print(f"✓ Updated: {subdir.name}/{md_file.name}")
                updated_count += 1

print("\nProcessing archive projects...")
for md_file in archive_dir.glob("*.md"):
    if update_frontmatter(md_file):
        print(f"✓ Updated: archive/{md_file.name}")
        updated_count += 1

print(f"\n✅ Updated {updated_count} project files")
