#!/Users/harrysayers/Developer/claudelife/.mcp/fastmcp-env/bin/python
"""
Memory Watcher - Auto-capture significant file changes to Graphiti memory
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MemoryCapture(FileSystemEventHandler):
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.significant_patterns = [
            "context/**/*.md",
            ".mcp.json",
            ".mcp/*.py",
            "trigger.config.ts",
            "CLAUDE.md",
            "*.config.json"
        ]
        self.last_capture = time.time()
        self.pending_changes = []

    def is_significant(self, file_path):
        """Check if file change should trigger memory capture"""
        rel_path = os.path.relpath(file_path, self.project_root)

        significant_dirs = ['context/', '.mcp/', 'trigger/']
        significant_files = ['.mcp.json', 'CLAUDE.md', 'trigger.config.ts']

        return (
            any(rel_path.startswith(d) for d in significant_dirs) or
            any(rel_path.endswith(f) for f in significant_files)
        )

    def on_modified(self, event):
        if event.is_directory:
            return

        if self.is_significant(event.src_path):
            self.pending_changes.append({
                'path': event.src_path,
                'event': 'modified',
                'timestamp': datetime.now().isoformat()
            })

            # Batch changes - capture after 30 seconds of inactivity
            if time.time() - self.last_capture > 30:
                self.capture_changes()

    def on_created(self, event):
        if event.is_directory:
            return

        if self.is_significant(event.src_path):
            self.pending_changes.append({
                'path': event.src_path,
                'event': 'created',
                'timestamp': datetime.now().isoformat()
            })

    def capture_changes(self):
        """Trigger memory capture via Claude Code"""
        if not self.pending_changes:
            return

        try:
            # Create summary of changes
            summary = f"Auto-detected {len(self.pending_changes)} significant changes:\n"
            for change in self.pending_changes:
                rel_path = os.path.relpath(change['path'], self.project_root)
                summary += f"- {change['event']}: {rel_path}\n"

            # Trigger Claude Code memory capture
            cmd = ['claude', '-p', f'/remember {summary}']
            subprocess.run(cmd, cwd=self.project_root, capture_output=True)

            print(f"📝 Captured {len(self.pending_changes)} changes to memory")
            self.pending_changes = []
            self.last_capture = time.time()

        except Exception as e:
            print(f"❌ Failed to capture changes: {e}")

def main():
    project_root = os.path.dirname(os.path.abspath(__file__ + "/../"))

    print(f"🔍 Starting memory watcher for {project_root}")

    event_handler = MemoryCapture(project_root)
    observer = Observer()
    observer.schedule(event_handler, project_root, recursive=True)

    print(f"🔍 Watching {project_root} for significant changes...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Memory watcher stopped")

    observer.join()

if __name__ == "__main__":
    main()