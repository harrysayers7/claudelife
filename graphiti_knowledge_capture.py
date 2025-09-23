"""
Graphiti Knowledge Capture System

Captures knowledge from tasks, projects, and interactions into the Graphiti knowledge graph.
Integrates with Task Master and personal assistant workflows.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path

from graphiti_config import get_graphiti, GraphitiManager
from graphiti_core.nodes import EpisodeType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntity:
    """Represents an entity extracted from content."""
    name: str
    type: str  # 'person', 'project', 'technology', 'concept', etc.
    description: str
    confidence: float
    source: str
    metadata: Dict[str, Any]


@dataclass
class KnowledgeRelationship:
    """Represents a relationship between entities."""
    from_entity: str
    to_entity: str
    relationship_type: str
    description: str
    confidence: float
    source: str
    metadata: Dict[str, Any]


@dataclass
class KnowledgeEpisode:
    """Represents a knowledge episode to be added to Graphiti."""
    name: str
    content: str
    source_type: EpisodeType
    source_description: str
    entities: List[KnowledgeEntity]
    relationships: List[KnowledgeRelationship]
    metadata: Dict[str, Any]
    timestamp: datetime


class KnowledgeExtractor:
    """Extracts entities and relationships from text content."""

    def __init__(self):
        self.entity_patterns = {
            'project': ['MOKAI', 'Mok Music', 'Brain', 'Mac projects', 'Task Master', 'Graphiti'],
            'technology': ['Claude Code', 'Neo4j', 'Python', 'JavaScript', 'API', 'database'],
            'person': ['Harry', 'Harrison', 'user', 'client', 'team member'],
            'tool': ['Linear', 'GitHub', 'Trigger.dev', 'MCP', 'git'],
            'concept': ['authentication', 'security', 'performance', 'automation']
        }

    async def extract_entities(self, content: str, source: str) -> List[KnowledgeEntity]:
        """Extract entities from content using pattern matching and LLM enhancement."""
        entities = []

        # Pattern-based extraction (fast)
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                if pattern.lower() in content.lower():
                    entities.append(KnowledgeEntity(
                        name=pattern,
                        type=entity_type,
                        description=f"{entity_type.title()} mentioned in {source}",
                        confidence=0.8,
                        source=source,
                        metadata={'extraction_method': 'pattern_matching'}
                    ))

        # TODO: Add LLM-based entity extraction for more sophisticated detection
        # This would use the Graphiti LLM to identify additional entities

        return entities

    async def extract_relationships(self, content: str, entities: List[KnowledgeEntity], source: str) -> List[KnowledgeRelationship]:
        """Extract relationships between entities."""
        relationships = []

        # Simple relationship detection based on co-occurrence and context
        entity_names = [e.name for e in entities]

        for i, entity1 in enumerate(entity_names):
            for entity2 in entity_names[i+1:]:
                if entity1 != entity2:
                    # Check if entities appear together in context
                    if entity1.lower() in content.lower() and entity2.lower() in content.lower():
                        relationship_type = self._infer_relationship_type(entity1, entity2, content)
                        if relationship_type:
                            relationships.append(KnowledgeRelationship(
                                from_entity=entity1,
                                to_entity=entity2,
                                relationship_type=relationship_type,
                                description=f"{entity1} {relationship_type} {entity2} (from {source})",
                                confidence=0.7,
                                source=source,
                                metadata={'extraction_method': 'co_occurrence'}
                            ))

        return relationships

    def _infer_relationship_type(self, entity1: str, entity2: str, content: str) -> Optional[str]:
        """Infer relationship type between entities based on context."""
        content_lower = content.lower()

        # Project relationships
        if any(proj in entity1.lower() for proj in ['mokai', 'mok music', 'brain', 'mac']):
            if any(tech in entity2.lower() for tech in ['python', 'neo4j', 'claude', 'api']):
                return 'uses_technology'
            if 'task' in content_lower:
                return 'contains_task'

        # Technology relationships
        if 'implement' in content_lower or 'setup' in content_lower:
            return 'implements'
        if 'integrate' in content_lower:
            return 'integrates_with'
        if 'configure' in content_lower:
            return 'configures'

        # Generic relationships
        if 'work' in content_lower:
            return 'works_with'
        if 'connect' in content_lower:
            return 'connects_to'

        return 'related_to'


class KnowledgeCapture:
    """Main knowledge capture system."""

    def __init__(self):
        self.extractor = KnowledgeExtractor()
        self.graphiti_manager: Optional[GraphitiManager] = None

    async def initialize(self):
        """Initialize the knowledge capture system."""
        self.graphiti = await get_graphiti()
        logger.info("Knowledge capture system initialized")

    async def capture_task_knowledge(self, task_data: Dict[str, Any]) -> str:
        """Capture knowledge from Task Master task data."""
        try:
            # Extract content from task
            task_id = task_data.get('id', 'unknown')
            title = task_data.get('title', '')
            description = task_data.get('description', '')
            details = task_data.get('details', '')
            status = task_data.get('status', '')

            content = f"""
            Task {task_id}: {title}
            Description: {description}
            Details: {details}
            Status: {status}
            """

            # Create episode
            episode = await self._create_episode(
                name=f"Task {task_id}: {title}",
                content=content,
                source_type=EpisodeType.text,
                source_description=f"Task Master task {task_id}",
                metadata={
                    'task_id': task_id,
                    'task_status': status,
                    'source_system': 'task_master',
                    'capture_time': datetime.now(timezone.utc).isoformat()
                }
            )

            # Add to Graphiti
            await self.graphiti.add_episode(
                name=episode.name,
                episode_body=episode.content,
                source=episode.source_type,
                source_description=episode.source_description,
                reference_time=episode.timestamp
            )

            logger.info(f"Captured knowledge for task {task_id}")
            return f"task_{task_id}_episode"

        except Exception as e:
            logger.error(f"Failed to capture task knowledge: {e}")
            raise

    async def capture_interaction_knowledge(self, interaction_content: str, interaction_type: str = "conversation") -> str:
        """Capture knowledge from user interactions or conversations."""
        try:
            episode = await self._create_episode(
                name=f"Interaction: {interaction_type} at {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                content=interaction_content,
                source_type=EpisodeType.text,
                source_description=f"User interaction: {interaction_type}",
                metadata={
                    'interaction_type': interaction_type,
                    'source_system': 'personal_assistant',
                    'capture_time': datetime.now(timezone.utc).isoformat()
                }
            )

            await self.graphiti.add_episode(
                name=episode.name,
                episode_body=episode.content,
                source=episode.source_type,
                source_description=episode.source_description,
                reference_time=episode.timestamp
            )

            logger.info(f"Captured interaction knowledge: {interaction_type}")
            return f"interaction_{interaction_type}_{int(episode.timestamp.timestamp())}"

        except Exception as e:
            logger.error(f"Failed to capture interaction knowledge: {e}")
            raise

    async def capture_project_knowledge(self, project_name: str, project_data: Dict[str, Any]) -> str:
        """Capture knowledge about projects and their context."""
        try:
            content = f"""
            Project: {project_name}
            Description: {project_data.get('description', '')}
            Context: {project_data.get('context', '')}
            Technologies: {', '.join(project_data.get('technologies', []))}
            Status: {project_data.get('status', '')}
            Team: {', '.join(project_data.get('team', []))}
            """

            episode = await self._create_episode(
                name=f"Project: {project_name}",
                content=content,
                source_type=EpisodeType.text,
                source_description=f"Project information for {project_name}",
                metadata={
                    'project_name': project_name,
                    'source_system': 'project_management',
                    'capture_time': datetime.now(timezone.utc).isoformat(),
                    **project_data
                }
            )

            await self.graphiti.add_episode(
                name=episode.name,
                episode_body=episode.content,
                source=episode.source_type,
                source_description=episode.source_description,
                reference_time=episode.timestamp
            )

            logger.info(f"Captured project knowledge: {project_name}")
            return f"project_{project_name.lower().replace(' ', '_')}_episode"

        except Exception as e:
            logger.error(f"Failed to capture project knowledge: {e}")
            raise

    async def _create_episode(self, name: str, content: str, source_type: EpisodeType,
                            source_description: str, metadata: Dict[str, Any]) -> KnowledgeEpisode:
        """Create a knowledge episode with extracted entities and relationships."""

        # Extract entities and relationships
        entities = await self.extractor.extract_entities(content, source_description)
        relationships = await self.extractor.extract_relationships(content, entities, source_description)

        return KnowledgeEpisode(
            name=name,
            content=content,
            source_type=source_type,
            source_description=source_description,
            entities=entities,
            relationships=relationships,
            metadata=metadata,
            timestamp=datetime.now(timezone.utc)
        )

    async def search_knowledge(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search the knowledge graph for relevant information."""
        try:
            results = await self.graphiti.search(query)
            return results[:limit]
        except Exception as e:
            logger.error(f"Knowledge search failed: {e}")
            return []

    async def get_related_knowledge(self, entity_name: str) -> List[Dict[str, Any]]:
        """Get knowledge related to a specific entity."""
        try:
            # Search for the entity and related information
            results = await self.graphiti.search(f"entity:{entity_name}")
            return results
        except Exception as e:
            logger.error(f"Failed to get related knowledge for {entity_name}: {e}")
            return []


class TaskMasterIntegration:
    """Integration hooks for Task Master."""

    def __init__(self, knowledge_capture: KnowledgeCapture):
        self.knowledge_capture = knowledge_capture

    async def on_task_created(self, task_data: Dict[str, Any]):
        """Hook called when a new task is created."""
        await self.knowledge_capture.capture_task_knowledge(task_data)

    async def on_task_completed(self, task_data: Dict[str, Any]):
        """Hook called when a task is completed."""
        # Add completion information to the task
        completion_data = task_data.copy()
        completion_data['completion_time'] = datetime.now(timezone.utc).isoformat()
        completion_data['status'] = 'completed'

        await self.knowledge_capture.capture_task_knowledge(completion_data)

    async def on_task_updated(self, task_data: Dict[str, Any], update_info: str):
        """Hook called when a task is updated."""
        # Capture the update as an interaction
        update_content = f"""
        Task {task_data.get('id')} Update:
        {update_info}

        Current Task State:
        Title: {task_data.get('title')}
        Status: {task_data.get('status')}
        """

        await self.knowledge_capture.capture_interaction_knowledge(
            update_content,
            "task_update"
        )


# Global knowledge capture instance
_knowledge_capture: Optional[KnowledgeCapture] = None
_task_master_integration: Optional[TaskMasterIntegration] = None


async def get_knowledge_capture() -> KnowledgeCapture:
    """Get the global knowledge capture instance."""
    global _knowledge_capture

    if not _knowledge_capture:
        _knowledge_capture = KnowledgeCapture()
        await _knowledge_capture.initialize()

    return _knowledge_capture


async def get_task_master_integration() -> TaskMasterIntegration:
    """Get the Task Master integration."""
    global _task_master_integration

    if not _task_master_integration:
        knowledge_capture = await get_knowledge_capture()
        _task_master_integration = TaskMasterIntegration(knowledge_capture)

    return _task_master_integration


# Example usage and testing
async def test_knowledge_capture():
    """Test the knowledge capture system."""
    try:
        # Initialize
        kc = await get_knowledge_capture()

        # Test task knowledge capture
        sample_task = {
            'id': '15.3',
            'title': 'Develop Knowledge Capture System',
            'description': 'Build system for capturing knowledge from tasks into Graphiti',
            'details': 'Implement entity extraction, relationship mapping, and automatic updates',
            'status': 'in-progress'
        }

        task_episode_id = await kc.capture_task_knowledge(sample_task)
        logger.info(f"Task knowledge captured: {task_episode_id}")

        # Test interaction knowledge capture
        interaction_content = """
        Working on integrating Graphiti with Task Master.
        Need to extract entities like projects (MOKAI), technologies (Neo4j, Python),
        and create relationships between them.
        """

        interaction_episode_id = await kc.capture_interaction_knowledge(
            interaction_content,
            "development_session"
        )
        logger.info(f"Interaction knowledge captured: {interaction_episode_id}")

        # Test project knowledge capture
        project_data = {
            'description': 'Indigenous-owned technology consultancy',
            'technologies': ['Python', 'Neo4j', 'Claude Code', 'Cybersecurity'],
            'status': 'active',
            'team': ['Harrison', 'Team members']
        }

        project_episode_id = await kc.capture_project_knowledge('MOKAI', project_data)
        logger.info(f"Project knowledge captured: {project_episode_id}")

        # Test knowledge search
        search_results = await kc.search_knowledge("Graphiti Task Master integration")
        logger.info(f"Search returned {len(search_results)} results")

        logger.info("✅ Knowledge capture system test completed successfully!")

    except Exception as e:
        logger.error(f"❌ Knowledge capture test failed: {e}")
        raise


if __name__ == "__main__":
    # Run test if script is executed directly
    asyncio.run(test_knowledge_capture())
