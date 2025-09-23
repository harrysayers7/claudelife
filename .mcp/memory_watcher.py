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
import asyncio
import fnmatch

class MemoryCapture(FileSystemEventHandler):
    def __init__(self, project_root):
        self.project_root = Path(project_root)

        # Smart trigger configuration
        self.context_triggers = {
            '.mcp.json': 'mcp-config',
            'CLAUDE.md': 'instructions',
            'context/**/*.md': 'context-docs',
            '.taskmaster/tasks/tasks.json': 'tasks',
            'trigger.config.ts': 'trigger-config',
            '.mcp/*.py': 'mcp-server',
            '*.config.json': 'config'
        }

        # High-impact changes that should always be captured
        self.high_impact_changes = {
            'mcp-config': True,
            'instructions': True,
            'trigger-config': True,
            'mcp-server': True
        }

        self.last_capture = time.time()
        self.pending_changes = []

    def get_change_type(self, file_path):
        """Determine the type of change and its significance"""
        rel_path = os.path.relpath(file_path, self.project_root)

        # Check against trigger patterns
        for pattern, change_type in self.context_triggers.items():
            if fnmatch.fnmatch(rel_path, pattern):
                return change_type, self.should_auto_capture(rel_path, change_type)

        return None, False

    def should_auto_capture(self, file_path, change_type):
        """Determine if change should trigger auto-capture"""
        # Always capture high-impact changes
        if self.high_impact_changes.get(change_type, False):
            return True

        # Conditional captures
        if change_type == 'context-docs':
            # Only capture business context changes
            return any(keyword in file_path.lower() for keyword in ['business', 'mokai', 'profile'])

        if change_type == 'tasks':
            # Only capture significant task structure changes
            return self.has_significant_task_changes(file_path)

        return False

    def has_significant_task_changes(self, file_path):
        """Check if task changes are structurally significant"""
        try:
            with open(os.path.join(self.project_root, file_path), 'r') as f:
                data = json.load(f)
                # Capture if tasks array length changed significantly or new top-level tasks
                return len(data.get('tasks', [])) > 10  # Simple heuristic
        except:
            return False

    def on_modified(self, event):
        if event.is_directory:
            return

        change_type, should_capture = self.get_change_type(event.src_path)
        if should_capture:
            self.pending_changes.append({
                'path': event.src_path,
                'event': 'modified',
                'change_type': change_type,
                'timestamp': datetime.now().isoformat()
            })

            # Batch changes - capture after 30 seconds of inactivity
            if time.time() - self.last_capture > 30:
                self.capture_changes()

    def on_created(self, event):
        if event.is_directory:
            return

        change_type, should_capture = self.get_change_type(event.src_path)
        if should_capture:
            self.pending_changes.append({
                'path': event.src_path,
                'event': 'created',
                'change_type': change_type,
                'timestamp': datetime.now().isoformat()
            })

    def capture_changes(self):
        """Auto-capture changes to Graphiti memory"""
        if not self.pending_changes:
            return

        try:
            # Group changes by type for better organization
            changes_by_type = {}
            for change in self.pending_changes:
                change_type = change.get('change_type', 'unknown')
                if change_type not in changes_by_type:
                    changes_by_type[change_type] = []
                changes_by_type[change_type].append(change)

            # Create structured memory for each change type
            for change_type, changes in changes_by_type.items():
                self.capture_to_graphiti(change_type, changes)

            print(f"📝 Auto-captured {len(self.pending_changes)} changes to Graphiti memory")
            self.pending_changes = []
            self.last_capture = time.time()

        except Exception as e:
            print(f"❌ Failed to auto-capture changes: {e}")

    def capture_to_graphiti(self, change_type, changes):
        """Capture specific change type to Graphiti"""
        try:
            # Generate context-aware summary
            summary = self.generate_change_summary(change_type, changes)

            if summary:
                # Use Graphiti MCP to capture memory
                cmd = [
                    'python', '-c', f'''
import asyncio
import sys
sys.path.append("{self.project_root}/.mcp")
from tools.brain_tools import capture_memory

async def main():
    await capture_memory(
        name="Auto: {change_type.title()} Changes",
        content="""{summary}""",
        source="auto-detection",
        group_id="claudelife"
    )

asyncio.run(main())
'''
                ]
                subprocess.run(cmd, cwd=self.project_root, capture_output=True)

        except Exception as e:
            print(f"❌ Failed to capture {change_type}: {e}")

    def generate_change_summary(self, change_type, changes):
        """Generate contextual summary based on change type"""
        if change_type == 'mcp-config':
            return self.summarize_mcp_changes(changes)
        elif change_type == 'instructions':
            return self.summarize_instruction_changes(changes)
        elif change_type == 'context-docs':
            return self.summarize_context_changes(changes)
        elif change_type == 'tasks':
            return self.summarize_task_changes(changes)
        else:
            return self.summarize_generic_changes(change_type, changes)

    def summarize_mcp_changes(self, changes):
        """Create summary for MCP configuration changes"""
        return f"""## Context
MCP server configuration updated

## Implementation Details
- Configuration file: .mcp.json modified
- Timestamp: {changes[0]['timestamp']}
- Impact: New integration capabilities added

## Future Considerations
- Verify MCP server connectivity
- Update Claude Code permissions if needed
- Test new integration functionality"""

    def summarize_instruction_changes(self, changes):
        """Create summary for CLAUDE.md changes"""
        return f"""## Context
Core Claude Code instructions updated

## Implementation Details
- Instructions file: CLAUDE.md modified
- Timestamp: {changes[0]['timestamp']}
- Impact: Assistant behavior or capabilities changed

## Future Considerations
- Instructions affect all future Claude Code sessions
- May require testing to verify new behaviors
- Consider documenting significant changes"""

    def summarize_context_changes(self, changes):
        """Create summary for context documentation changes"""
        file_names = [os.path.basename(c['path']) for c in changes]
        return f"""## Context
Business/project context documentation updated

## Implementation Details
- Files modified: {', '.join(file_names)}
- Timestamp: {changes[0]['timestamp']}
- Impact: Business logic or project understanding updated

## Future Considerations
- Context changes affect project decision-making
- May impact automation rules or workflows
- Consider updating related documentation"""

    def summarize_task_changes(self, changes):
        """Create summary for Task Master changes"""
        return f"""## Context
Task Master project structure updated

## Implementation Details
- Tasks file: .taskmaster/tasks/tasks.json modified
- Timestamp: {changes[0]['timestamp']}
- Impact: Project workflow or task dependencies changed

## Future Considerations
- Task changes affect development priorities
- May require dependency validation
- Consider updating project timeline"""

    def summarize_generic_changes(self, change_type, changes):
        """Create summary for other significant changes"""
        file_paths = [os.path.relpath(c['path'], self.project_root) for c in changes]
        return f"""## Context
{change_type.title()} configuration updated

## Implementation Details
- Files: {', '.join(file_paths)}
- Timestamp: {changes[0]['timestamp']}
- Change type: {change_type}

## Future Considerations
- Configuration changes may affect system behavior
- Consider testing affected functionality
- Document if changes are significant"""

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
