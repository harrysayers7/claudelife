"""
Notion Client - Interface to Tasks-AI database
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from notion_client import AsyncClient
from datetime import datetime

class NotionClient:
    """Async Notion client for Tasks-AI integration"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = AsyncClient(auth=config['api_key'])
        self.logger = logging.getLogger(__name__)

        # Database IDs
        self.tasks_db_id = config['database_ids']['tasks_ai']

    async def initialize(self):
        """Initialize the Notion client"""
        try:
            # Test connection
            await self.client.users.me()
            self.logger.info("Notion client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Notion client: {e}")
            raise

    async def close(self):
        """Close the Notion client"""
        if hasattr(self.client, 'close'):
            await self.client.close()

    async def create_task(self, task_data: Dict[str, Any]) -> str:
        """Create a new task in Tasks-AI database"""
        try:
            # Format task properties according to Tasks-AI schema
            properties = {
                "Task": {"title": [{"text": {"content": task_data['title']}}]},
                "Status": {"select": {"name": task_data.get('status', 'Not Started')}},
                "Assigner": {"select": {"name": "AI"}},
                "Category": {"select": {"name": task_data.get('category', 'Development')}},
                "Priority": {"select": {"name": task_data.get('priority', 'P2 - Medium')}},
                "Notes": {"rich_text": [{"text": {"content": task_data.get('notes', '')}}]}
            }

            # Add optional fields
            if 'tags' in task_data:
                properties["Tags"] = {"multi_select": [{"name": tag} for tag in task_data['tags']]}

            if 'area' in task_data:
                properties["Area"] = {"multi_select": [{"name": area} for area in task_data['area']]}

            if 'due_date' in task_data:
                properties["date:Due Date:start"] = {"date": {"start": task_data['due_date']}}

            response = await self.client.pages.create(
                parent={"database_id": self.tasks_db_id},
                properties=properties
            )

            task_id = response['id']
            self.logger.info(f"Created task: {task_id}")
            return task_id

        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            raise

    async def get_tasks(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get tasks from Tasks-AI database"""
        try:
            query = {"database_id": self.tasks_db_id}

            if filters:
                query["filter"] = self._build_filter(filters)

            response = await self.client.databases.query(**query)

            tasks = []
            for page in response['results']:
                task = self._parse_task_page(page)
                tasks.append(task)

            return tasks

        except Exception as e:
            self.logger.error(f"Failed to get tasks: {e}")
            raise

    async def update_task_status(self, task_id: str, status: str) -> None:
        """Update task status"""
        try:
            await self.client.pages.update(
                page_id=task_id,
                properties={
                    "Status": {"select": {"name": status}}
                }
            )
            self.logger.info(f"Updated task {task_id} status to {status}")

        except Exception as e:
            self.logger.error(f"Failed to update task status: {e}")
            raise

    def _build_filter(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Build Notion API filter from simple filters"""
        notion_filters = []

        if 'status' in filters:
            notion_filters.append({
                "property": "Status",
                "select": {"equals": filters['status']}
            })

        if 'priority' in filters:
            notion_filters.append({
                "property": "Priority",
                "select": {"equals": filters['priority']}
            })

        if 'area' in filters:
            notion_filters.append({
                "property": "Area",
                "multi_select": {"contains": filters['area']}
            })

        if 'due_today' in filters and filters['due_today']:
            today = datetime.now().strftime('%Y-%m-%d')
            notion_filters.append({
                "property": "date:Due Date:start",
                "date": {"equals": today}
            })

        if len(notion_filters) == 1:
            return notion_filters[0]
        elif len(notion_filters) > 1:
            return {"and": notion_filters}
        else:
            return {}

    def _parse_task_page(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a Notion page into a task dict"""
        properties = page['properties']

        task = {
            'id': page['id'],
            'title': self._get_title(properties.get('Task', {})),
            'status': self._get_select(properties.get('Status', {})),
            'priority': self._get_select(properties.get('Priority', {})),
            'category': self._get_select(properties.get('Category', {})),
            'notes': self._get_rich_text(properties.get('Notes', {})),
            'tags': self._get_multi_select(properties.get('Tags', {})),
            'area': self._get_multi_select(properties.get('Area', {})),
            'created_time': page['created_time'],
            'last_edited_time': page['last_edited_time']
        }

        return task

    def _get_title(self, prop: Dict[str, Any]) -> str:
        """Extract title from Notion property"""
        if 'title' in prop and prop['title']:
            return ''.join([t['plain_text'] for t in prop['title']])
        return ''

    def _get_select(self, prop: Dict[str, Any]) -> str:
        """Extract select value from Notion property"""
        if 'select' in prop and prop['select']:
            return prop['select']['name']
        return ''

    def _get_multi_select(self, prop: Dict[str, Any]) -> List[str]:
        """Extract multi-select values from Notion property"""
        if 'multi_select' in prop:
            return [option['name'] for option in prop['multi_select']]
        return []

    def _get_rich_text(self, prop: Dict[str, Any]) -> str:
        """Extract rich text from Notion property"""
        if 'rich_text' in prop and prop['rich_text']:
            return ''.join([t['plain_text'] for t in prop['rich_text']])
        return ''