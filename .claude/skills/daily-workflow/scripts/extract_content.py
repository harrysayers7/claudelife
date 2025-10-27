#!/usr/bin/env python3
"""
Daily Content Extraction Script

Deterministic operations for extracting and processing daily note entries.
This script handles file I/O, pattern matching, and data structure operations.
AI classification and routing decisions are handled by Claude/MCP.

Usage:
    python extract_content.py <date>
    python extract_content.py 2025-10-21
    python extract_content.py --scan-unprocessed
"""

import os
import re
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher

# Constants
DAILY_NOTES_DIR = Path("00 - Daily")
TRACKER_PATH = Path(".claude/commands/.extract-daily-content-tracker.json")
NOTES_SECTION_PATTERN = r"### 🧠 Notes\n\n(.*?)(?=\n###|\Z)"


class DailyNoteExtractor:
    """Handles extraction of content from daily notes."""

    def __init__(self, vault_root: Path = Path(".")):
        self.vault_root = vault_root.resolve()
        self.tracker_path = self.vault_root / TRACKER_PATH
        self.daily_dir = self.vault_root / DAILY_NOTES_DIR

    def load_tracker(self) -> Dict:
        """Load the extraction tracker JSON."""
        if not self.tracker_path.exists():
            return {
                "last_scan": None,
                "processed_files": {},
                "entries_processed": 0,
                "routing_decisions": []
            }

        with open(self.tracker_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_tracker(self, tracker: Dict) -> None:
        """Save the extraction tracker JSON."""
        self.tracker_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.tracker_path, 'w', encoding='utf-8') as f:
            json.dump(tracker, f, indent=2, ensure_ascii=False)

    def find_daily_note(self, date_str: str) -> Optional[Path]:
        """
        Find daily note file for given date.

        Args:
            date_str: Date in YYYY-MM-DD format

        Returns:
            Path to daily note file or None if not found
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD.")
            return None

        # Daily note filename pattern: 🌤️ Day - DDth MMM YY.md
        day_name = date.strftime("%a")  # Mon, Tue, etc.
        day_num = date.strftime("%d").lstrip("0")  # 1, 2, ..., 21

        # Determine ordinal suffix
        if 10 <= int(day_num) % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(int(day_num) % 10, "th")

        month_abbr = date.strftime("%b")  # Jan, Feb, etc.
        year_short = date.strftime("%y")  # 25, 26, etc.

        filename = f"🌤️ {day_name} - {day_num}{suffix} {month_abbr} {year_short}.md"
        filepath = self.daily_dir / filename

        if filepath.exists():
            return filepath

        print(f"Daily note not found: {filename}")
        return None

    def scan_unprocessed_notes(self) -> List[Tuple[Path, datetime]]:
        """
        Scan for unprocessed daily notes (excluding today).

        Returns:
            List of (filepath, modification_time) tuples
        """
        tracker = self.load_tracker()
        processed_files = tracker.get("processed_files", {})
        today = datetime.now().date()

        unprocessed = []

        if not self.daily_dir.exists():
            print(f"Daily notes directory not found: {self.daily_dir}")
            return unprocessed

        for filepath in self.daily_dir.glob("🌤️ *.md"):
            # Skip today's note (allow re-processing)
            file_date = self._extract_date_from_filename(filepath.name)
            if file_date and file_date.date() == today:
                continue

            # Check if processed
            file_key = str(filepath.relative_to(self.vault_root))
            mod_time = datetime.fromtimestamp(filepath.stat().st_mtime)

            if file_key in processed_files:
                # Check if modified since last processing
                last_processed = datetime.fromisoformat(processed_files[file_key]["processed_at"])
                if mod_time <= last_processed:
                    continue  # Already processed, no changes

            unprocessed.append((filepath, mod_time))

        # Sort by date (oldest first)
        unprocessed.sort(key=lambda x: x[1])

        return unprocessed

    def extract_notes_section(self, filepath: Path) -> Optional[str]:
        """
        Extract content from ### 🧠 Notes section.

        Args:
            filepath: Path to daily note file

        Returns:
            Content string or None if section not found
        """
        if not filepath.exists():
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match ### 🧠 Notes section (case-insensitive, flexible whitespace)
        match = re.search(NOTES_SECTION_PATTERN, content, re.DOTALL | re.IGNORECASE)

        if not match:
            return None

        notes_content = match.group(1).strip()

        # Also scan nested H4/H5/H6 subsections within Notes
        # Pattern: capture all content until next H3 or EOF
        full_pattern = r"### 🧠 Notes(.*?)(?=\n###|\Z)"
        full_match = re.search(full_pattern, content, re.DOTALL | re.IGNORECASE)

        if full_match:
            return full_match.group(1).strip()

        return notes_content if notes_content else None

    def split_entries(self, notes_content: str) -> List[str]:
        """
        Split notes content into individual entries.

        Entries are separated by blank lines (2+ newlines).

        Args:
            notes_content: Raw notes section content

        Returns:
            List of entry strings
        """
        # Split by 2+ newlines
        entries = re.split(r'\n\s*\n', notes_content)

        # Filter out empty entries and strip whitespace
        entries = [e.strip() for e in entries if e.strip()]

        return entries

    def check_duplicate(self, entry: str, existing_entries: List[str], threshold: float = 0.80) -> bool:
        """
        Check if entry is a duplicate using fuzzy matching.

        Args:
            entry: New entry to check
            existing_entries: List of existing entries
            threshold: Similarity threshold (0.0-1.0)

        Returns:
            True if duplicate found, False otherwise
        """
        for existing in existing_entries:
            similarity = SequenceMatcher(None, entry.lower(), existing.lower()).ratio()
            if similarity >= threshold:
                return True

        return False

    def format_cross_link(self, daily_note_path: Path, section: str = "🧠 Notes") -> str:
        """
        Format cross-link to daily note.

        Args:
            daily_note_path: Path to daily note file
            section: Section anchor (default: "🧠 Notes")

        Returns:
            Formatted link string
        """
        # Get relative path from vault root
        rel_path = daily_note_path.relative_to(self.vault_root)

        # Remove .md extension for wikilink
        link_path = str(rel_path.with_suffix(''))

        # Format: [[00 - Daily/🌤️ Mon - 21st Oct 25#🧠 Notes]]
        if section:
            return f"[[{link_path}#{section}]]"
        else:
            return f"[[{link_path}]]"

    def read_destination_file(self, filepath: Path) -> List[str]:
        """
        Read existing entries from a destination file.

        Returns list of existing entries for duplicate checking.
        """
        if not filepath.exists():
            return []

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract entries (simple split by ## headers or bullet points)
        # This is a basic implementation - may need refinement
        entries = re.split(r'\n(?=##|\- )', content)

        return [e.strip() for e in entries if e.strip()]

    def append_to_file(self, filepath: Path, content: str, create_if_missing: bool = True) -> bool:
        """
        Append content to a file atomically.

        Args:
            filepath: Destination file path
            content: Content to append
            create_if_missing: Create file with frontmatter if missing

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Create file if missing
            if not filepath.exists() and create_if_missing:
                self._create_file_with_frontmatter(filepath)

            # Append content
            with open(filepath, 'a', encoding='utf-8') as f:
                # Ensure newline before appending
                f.write("\n\n" + content)

            return True

        except Exception as e:
            print(f"Error appending to {filepath}: {e}")
            return False

    def _create_file_with_frontmatter(self, filepath: Path) -> None:
        """Create a new file with proper frontmatter."""
        now = datetime.now()
        frontmatter = f"""---
date created: {now.strftime("%a, %m %dth %y, %I:%M:%S %p").lower()}
date modified: {now.strftime("%a, %m %dth %y, %I:%M:%S %p").lower()}
---

# {filepath.stem.replace('-', ' ').title()}

"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)

    def _extract_date_from_filename(self, filename: str) -> Optional[datetime]:
        """
        Extract date from daily note filename.

        Example: "🌤️ Mon - 21st Oct 25.md" → datetime(2025, 10, 21)
        """
        # Pattern: 🌤️ Day - DDth MMM YY.md
        pattern = r"🌤️ (\w+) - (\d+)(?:st|nd|rd|th) (\w+) (\d+)\.md"
        match = re.match(pattern, filename)

        if not match:
            return None

        day_name, day_num, month_abbr, year_short = match.groups()

        # Construct date string for parsing
        date_str = f"{day_num} {month_abbr} {year_short}"

        try:
            # Parse with 2-digit year
            date = datetime.strptime(date_str, "%d %b %y")
            return date
        except ValueError:
            return None

    def mark_as_processed(self, filepath: Path, entries_count: int, routing_decisions: List[Dict]) -> None:
        """
        Mark a daily note as processed in the tracker.

        Only mark as processed if date is in the past (not today).
        """
        file_date = self._extract_date_from_filename(filepath.name)
        if file_date and file_date.date() == datetime.now().date():
            print(f"Skipping tracker update for today's note: {filepath.name}")
            return

        tracker = self.load_tracker()

        file_key = str(filepath.relative_to(self.vault_root))

        tracker["processed_files"][file_key] = {
            "processed_at": datetime.now().isoformat(),
            "entries_count": entries_count,
            "routing_decisions": routing_decisions
        }

        tracker["last_scan"] = datetime.now().isoformat()
        tracker["entries_processed"] = tracker.get("entries_processed", 0) + entries_count

        self.save_tracker(tracker)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python extract_content.py <YYYY-MM-DD>")
        print("  python extract_content.py --scan-unprocessed")
        sys.exit(1)

    extractor = DailyNoteExtractor()

    if sys.argv[1] == "--scan-unprocessed":
        # Scan for unprocessed notes
        unprocessed = extractor.scan_unprocessed_notes()

        if not unprocessed:
            print("No unprocessed daily notes found.")
            sys.exit(0)

        print(f"Found {len(unprocessed)} unprocessed daily notes:")
        for filepath, mod_time in unprocessed:
            print(f"  - {filepath.name} (modified: {mod_time.strftime('%Y-%m-%d %H:%M')})")

        sys.exit(0)

    # Extract specific date
    date_str = sys.argv[1]
    filepath = extractor.find_daily_note(date_str)

    if not filepath:
        sys.exit(1)

    # Extract notes section
    notes_content = extractor.extract_notes_section(filepath)

    if not notes_content:
        print(f"No '### 🧠 Notes' section found in {filepath.name}")
        sys.exit(1)

    # Split into entries
    entries = extractor.split_entries(notes_content)

    print(f"Extracted {len(entries)} entries from {filepath.name}:")
    print()

    for i, entry in enumerate(entries, 1):
        print(f"Entry {i}:")
        print(f"  {entry[:100]}..." if len(entry) > 100 else f"  {entry}")
        print()

    # Output JSON for AI classification
    output = {
        "date": date_str,
        "filename": filepath.name,
        "entries_count": len(entries),
        "entries": [
            {
                "index": i,
                "content": entry,
                "cross_link": extractor.format_cross_link(filepath)
            }
            for i, entry in enumerate(entries, 1)
        ]
    }

    print("\nJSON Output for AI Classification:")
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
