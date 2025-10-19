#!/usr/bin/env python3
"""Rename MOK HOUSE project files to match their project name field."""

import os
import re
from pathlib import Path

archive_dir = Path("/Users/harrysayers/Developer/claudelife/02-projects/mokhouse/archive")

renames = []

for md_file in archive_dir.glob("*.md"):
    content = md_file.read_text()

    # Extract project name from frontmatter
    match = re.search(r'^project name:\s*(.+)$', content, re.MULTILINE)

    if match:
        project_name = match.group(1).strip().strip('"')
        new_filename = f"{project_name}.md"
        new_path = archive_dir / new_filename

        if md_file.name != new_filename:
            renames.append((md_file, new_path, project_name))
            print(f"Will rename: {md_file.name} -> {new_filename}")

print(f"\nTotal files to rename: {len(renames)}\n")

# Perform renames
for old_path, new_path, project_name in renames:
    try:
        old_path.rename(new_path)
        print(f"✓ Renamed: {old_path.name} -> {new_path.name}")
    except Exception as e:
        print(f"✗ Error renaming {old_path.name}: {e}")

print(f"\n✅ Completed {len(renames)} renames")
