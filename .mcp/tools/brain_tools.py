# Brain Tools for FastMCP Server
# Additional tool implementations for brain dump and morning review functionality

import asyncio
from datetime import datetime
import json
import os

class BrainTools:
    """Brain-related tools for the FastMCP server"""

    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.brain_dump_dir = os.path.join(data_dir, "brain_dumps")
        self.morning_review_dir = os.path.join(data_dir, "morning_reviews")

        # Create directories if they don't exist
        os.makedirs(self.brain_dump_dir, exist_ok=True)
        os.makedirs(self.morning_review_dir, exist_ok=True)

    async def save_brain_dump(self, thoughts: str) -> str:
        """Save brain dump thoughts to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"brain_dump_{timestamp}.txt"
        filepath = os.path.join(self.brain_dump_dir, filename)

        with open(filepath, 'w') as f:
            f.write(f"Brain Dump - {datetime.now().isoformat()}\n")
            f.write("=" * 50 + "\n\n")
            f.write(thoughts)

        return f"Brain dump saved to: {filepath}"

    async def get_recent_brain_dumps(self, limit: int = 5) -> list:
        """Retrieve recent brain dumps"""
        files = []
        if os.path.exists(self.brain_dump_dir):
            files = [f for f in os.listdir(self.brain_dump_dir) if f.endswith('.txt')]
            files.sort(reverse=True)  # Most recent first

        recent_dumps = []
        for file in files[:limit]:
            filepath = os.path.join(self.brain_dump_dir, file)
            with open(filepath, 'r') as f:
                content = f.read()
                recent_dumps.append({
                    'filename': file,
                    'content': content[:200] + "..." if len(content) > 200 else content
                })

        return recent_dumps

    async def generate_morning_review(self) -> dict:
        """Generate morning review based on recent brain dumps and tasks"""
        # Get recent brain dumps
        recent_dumps = await self.get_recent_brain_dumps(3)

        # Create morning review structure
        review = {
            'date': datetime.now().isoformat(),
            'recent_thoughts': recent_dumps,
            'priorities': [],  # TODO: Integrate with task system
            'schedule': [],    # TODO: Integrate with calendar
            'reminders': []    # TODO: Integrate with reminder system
        }

        # Save morning review
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"morning_review_{timestamp}.json"
        filepath = os.path.join(self.morning_review_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(review, f, indent=2)

        return review