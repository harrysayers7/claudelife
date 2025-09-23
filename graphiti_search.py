"""
Graphiti Search and Retrieval System

Provides intelligent search capabilities leveraging the graph structure
for context-aware information retrieval and relationship-based queries.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import re

from graphiti_config import get_graphiti
from graphiti_knowledge_capture import get_knowledge_capture, KnowledgeEntity, KnowledgeRelationship

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Represents a search result with relevance scoring."""
    content: str
    source: str
    relevance_score: float
    entities: List[str]
    relationships: List[str]
    metadata: Dict[str, Any]
    timestamp: datetime


@dataclass
class SearchQuery:
    """Represents a structured search query."""
    text: str
    entities: Optional[List[str]] = None
    relationship_types: Optional[List[str]] = None
    source_types: Optional[List[str]] = None
    time_range: Optional[Tuple[datetime, datetime]] = None
    limit: int = 10
    include_related: bool = True


class QueryTemplates:
    """Pre-built query templates for common search patterns."""

    @staticmethod
    def find_project_tasks(project_name: str) -> SearchQuery:
        """Find all tasks related to a specific project."""
        return SearchQuery(
            text=f"tasks project {project_name}",
            entities=[project_name],
            relationship_types=["contains_task", "uses_technology", "implements"],
            source_types=["task_master"],
            include_related=True
        )

    @staticmethod
    def find_technology_usage(technology: str) -> SearchQuery:
        """Find how a technology is being used across projects."""
        return SearchQuery(
            text=f"{technology} implementation usage",
            entities=[technology],
            relationship_types=["uses_technology", "implements", "integrates_with"],
            include_related=True
        )

    @staticmethod
    def find_recent_work(days: int = 7) -> SearchQuery:
        """Find recent work within the specified days."""
        end_date = datetime.now(timezone.utc)
        start_date = end_date.replace(day=end_date.day - days)

        return SearchQuery(
            text="recent work progress tasks",
            time_range=(start_date, end_date),
            source_types=["task_master", "personal_assistant"],
            include_related=True
        )

    @staticmethod
    def find_related_concepts(concept: str) -> SearchQuery:
        """Find concepts related to a given concept."""
        return SearchQuery(
            text=f"{concept} related concepts connections",
            entities=[concept],
            relationship_types=["related_to", "connects_to", "works_with"],
            include_related=True
        )

    @staticmethod
    def find_implementation_details(feature: str) -> SearchQuery:
        """Find implementation details for a specific feature."""
        return SearchQuery(
            text=f"{feature} implementation details code",
            entities=[feature],
            relationship_types=["implements", "configures", "uses_technology"],
            source_types=["task_master"],
            include_related=True
        )


class RelevanceScorer:
    """Calculates relevance scores for search results."""

    def __init__(self):
        self.weights = {
            'text_match': 0.4,
            'entity_match': 0.3,
            'relationship_match': 0.2,
            'recency': 0.1
        }

    def calculate_score(self, result: Dict[str, Any], query: SearchQuery) -> float:
        """Calculate relevance score for a search result."""
        scores = {}

        # Text similarity score (simplified - could use embeddings)
        scores['text_match'] = self._text_similarity(
            result.get('content', ''),
            query.text
        )

        # Entity matching score
        scores['entity_match'] = self._entity_similarity(
            result.get('entities', []),
            query.entities or []
        )

        # Relationship matching score
        scores['relationship_match'] = self._relationship_similarity(
            result.get('relationships', []),
            query.relationship_types or []
        )

        # Recency score
        scores['recency'] = self._recency_score(
            result.get('timestamp', datetime.now(timezone.utc))
        )

        # Weighted total
        total_score = sum(
            scores[key] * self.weights[key]
            for key in scores
        )

        return min(total_score, 1.0)  # Cap at 1.0

    def _text_similarity(self, text: str, query: str) -> float:
        """Calculate text similarity score (simplified)."""
        text_lower = text.lower()
        query_lower = query.lower()

        # Simple keyword matching
        query_words = set(query_lower.split())
        text_words = set(text_lower.split())

        if not query_words:
            return 0.0

        matches = len(query_words.intersection(text_words))
        return matches / len(query_words)

    def _entity_similarity(self, result_entities: List[str], query_entities: List[str]) -> float:
        """Calculate entity matching score."""
        if not query_entities or not result_entities:
            return 0.0

        result_set = set(e.lower() for e in result_entities)
        query_set = set(e.lower() for e in query_entities)

        matches = len(result_set.intersection(query_set))
        return matches / len(query_set)

    def _relationship_similarity(self, result_rels: List[str], query_rels: List[str]) -> float:
        """Calculate relationship matching score."""
        if not query_rels or not result_rels:
            return 0.0

        result_set = set(r.lower() for r in result_rels)
        query_set = set(r.lower() for r in query_rels)

        matches = len(result_set.intersection(query_set))
        return matches / len(query_set)

    def _recency_score(self, timestamp: datetime) -> float:
        """Calculate recency score (more recent = higher score)."""
        now = datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        days_old = (now - timestamp).days

        # Exponential decay: full score for today, half score after 30 days
        return max(0.0, pow(0.5, days_old / 30))


class GraphSearchEngine:
    """Main search engine that leverages Graphiti's graph structure."""

    def __init__(self):
        self.graphiti = None
        self.knowledge_capture = None
        self.scorer = RelevanceScorer()
        self.query_cache = {}
        self.cache_ttl = 300  # 5 minutes

    async def initialize(self):
        """Initialize the search engine."""
        self.graphiti = await get_graphiti()
        self.knowledge_capture = await get_knowledge_capture()
        logger.info("Graph search engine initialized")

    async def search(self, query: Union[str, SearchQuery], use_cache: bool = True) -> List[SearchResult]:
        """Perform a graph-aware search."""
        try:
            # Convert string to SearchQuery if needed
            if isinstance(query, str):
                query = SearchQuery(text=query)

            # Check cache
            cache_key = self._get_cache_key(query)
            if use_cache and cache_key in self.query_cache:
                cached_result, timestamp = self.query_cache[cache_key]
                if (datetime.now().timestamp() - timestamp) < self.cache_ttl:
                    logger.info(f"Returning cached results for query: {query.text}")
                    return cached_result

            # Perform search
            results = await self._perform_search(query)

            # Score and rank results
            scored_results = []
            for result in results:
                score = self.scorer.calculate_score(result, query)

                search_result = SearchResult(
                    content=result.get('content', ''),
                    source=result.get('source', ''),
                    relevance_score=score,
                    entities=result.get('entities', []),
                    relationships=result.get('relationships', []),
                    metadata=result.get('metadata', {}),
                    timestamp=result.get('timestamp', datetime.now(timezone.utc))
                )
                scored_results.append(search_result)

            # Sort by relevance score
            scored_results.sort(key=lambda x: x.relevance_score, reverse=True)

            # Limit results
            final_results = scored_results[:query.limit]

            # Cache results
            if use_cache:
                self.query_cache[cache_key] = (final_results, datetime.now().timestamp())

            logger.info(f"Search returned {len(final_results)} results for: {query.text}")
            return final_results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def _perform_search(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """Perform the actual search using Graphiti."""
        # Use Graphiti's search functionality
        raw_results = await self.graphiti.search(query.text)

        # Process and enrich results
        processed_results = []
        for result in raw_results:
            # Handle different result types from Graphiti
            if hasattr(result, '__dict__'):
                # Convert object to dict
                result_dict = result.__dict__ if hasattr(result, '__dict__') else {}
            else:
                result_dict = result if isinstance(result, dict) else {}

            # Extract content from various possible fields
            content_parts = []

            # Try different content field names
            for field in ['content', 'name', 'summary', 'fact', 'episode_name', 'source_description']:
                if hasattr(result, field):
                    value = getattr(result, field, '')
                    if value:
                        content_parts.append(str(value))
                elif field in result_dict:
                    value = result_dict.get(field, '')
                    if value:
                        content_parts.append(str(value))

            content = ' '.join(content_parts) if content_parts else str(result)

            # Extract source information
            source = ''
            for field in ['source', 'source_description', 'episode_type']:
                if hasattr(result, field):
                    value = getattr(result, field, '')
                    if value:
                        source = str(value)
                        break
                elif field in result_dict:
                    value = result_dict.get(field, '')
                    if value:
                        source = str(value)
                        break

            # Extract timestamp
            timestamp = None
            for field in ['created_at', 'createdAt', 'timestamp', 'valid_at']:
                if hasattr(result, field):
                    timestamp = getattr(result, field, None)
                    break
                elif field in result_dict:
                    timestamp = result_dict.get(field, None)
                    break

            processed_result = {
                'content': content,
                'source': source,
                'entities': self._extract_entities_from_content(content),
                'relationships': self._extract_relationships_from_content(content),
                'metadata': {'raw_result_type': type(result).__name__},
                'timestamp': self._parse_timestamp(str(timestamp) if timestamp else '')
            }
            processed_results.append(processed_result)

        # If include_related is True, fetch related information
        if query.include_related and processed_results:
            related_results = await self._get_related_information(processed_results, query)
            processed_results.extend(related_results)

        return processed_results

    def _extract_entities_from_content(self, content: str) -> List[str]:
        """Extract entities from content text."""
        entities = []

        # Simple entity extraction (could be enhanced with NLP)
        entity_patterns = [
            r'\b(MOKAI|Mok Music|Brain|Mac projects|Task Master|Graphiti)\b',
            r'\b(Claude Code|Neo4j|Python|JavaScript|API|database)\b',
            r'\b(Linear|GitHub|Trigger\.dev|MCP|git)\b',
            r'\b(authentication|security|performance|automation)\b'
        ]

        for pattern in entity_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            entities.extend(matches)

        return list(set(entities))  # Remove duplicates

    def _extract_relationships_from_content(self, content: str) -> List[str]:
        """Extract relationship types from content text."""
        relationships = []
        content_lower = content.lower()

        # Identify relationship patterns
        if 'implement' in content_lower or 'setup' in content_lower:
            relationships.append('implements')
        if 'integrate' in content_lower:
            relationships.append('integrates_with')
        if 'configure' in content_lower:
            relationships.append('configures')
        if 'uses' in content_lower:
            relationships.append('uses_technology')
        if 'work' in content_lower:
            relationships.append('works_with')
        if 'connect' in content_lower:
            relationships.append('connects_to')
        if 'task' in content_lower:
            relationships.append('contains_task')

        return relationships

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp from various formats."""
        if not timestamp_str:
            return datetime.now(timezone.utc)

        try:
            # Try ISO format first
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            # Fallback to current time
            return datetime.now(timezone.utc)

    async def _get_related_information(self, results: List[Dict[str, Any]], query: SearchQuery) -> List[Dict[str, Any]]:
        """Get related information based on entities in the results."""
        related_results = []

        # Extract all entities from current results
        all_entities = set()
        for result in results:
            all_entities.update(result.get('entities', []))

        # Search for related information
        for entity in list(all_entities)[:5]:  # Limit to prevent explosion
            try:
                related_search = await self.graphiti.search(f"entity:{entity}")
                for related in related_search[:3]:  # Limit related results
                    processed = {
                        'content': related.get('content', ''),
                        'source': f"related_to_{entity}",
                        'entities': [entity],
                        'relationships': ['related_to'],
                        'metadata': {'related_entity': entity},
                        'timestamp': self._parse_timestamp(related.get('createdAt', ''))
                    }
                    related_results.append(processed)
            except Exception as e:
                logger.warning(f"Failed to get related info for {entity}: {e}")
                continue

        return related_results

    def _get_cache_key(self, query: SearchQuery) -> str:
        """Generate cache key for a query."""
        key_parts = [
            query.text,
            str(query.entities or []),
            str(query.relationship_types or []),
            str(query.source_types or []),
            str(query.time_range),
            str(query.limit),
            str(query.include_related)
        ]
        return hash(tuple(key_parts))

    async def faceted_search(self, base_query: str, facets: Dict[str, List[str]]) -> Dict[str, List[SearchResult]]:
        """Perform faceted search with multiple categories."""
        results = {}

        for facet_name, facet_values in facets.items():
            facet_results = []

            for value in facet_values:
                query = SearchQuery(
                    text=f"{base_query} {value}",
                    entities=[value] if facet_name == 'entities' else None,
                    relationship_types=[value] if facet_name == 'relationships' else None,
                    source_types=[value] if facet_name == 'sources' else None,
                    limit=5
                )

                search_results = await self.search(query)
                facet_results.extend(search_results)

            # Remove duplicates and sort by score
            unique_results = []
            seen_content = set()
            for result in sorted(facet_results, key=lambda x: x.relevance_score, reverse=True):
                if result.content not in seen_content:
                    unique_results.append(result)
                    seen_content.add(result.content)

            results[facet_name] = unique_results[:10]  # Top 10 per facet

        return results

    async def get_context_for_task(self, task_id: str) -> List[SearchResult]:
        """Get relevant context for a specific task."""
        query = SearchQuery(
            text=f"task {task_id} context implementation",
            entities=[f"task_{task_id}"],
            source_types=["task_master"],
            include_related=True,
            limit=20
        )

        return await self.search(query)

    async def get_project_overview(self, project_name: str) -> Dict[str, Any]:
        """Get comprehensive overview of a project."""
        # Search for project information
        project_query = QueryTemplates.find_project_tasks(project_name)
        tasks = await self.search(project_query)

        # Search for technology usage
        tech_query = SearchQuery(
            text=f"{project_name} technology stack",
            entities=[project_name],
            relationship_types=["uses_technology"],
            include_related=True
        )
        technologies = await self.search(tech_query)

        # Get recent activity
        recent_query = SearchQuery(
            text=f"{project_name} recent activity",
            entities=[project_name],
            time_range=(
                datetime.now(timezone.utc).replace(day=datetime.now().day - 14),
                datetime.now(timezone.utc)
            ),
            include_related=True
        )
        recent_activity = await self.search(recent_query)

        return {
            'project_name': project_name,
            'tasks': tasks,
            'technologies': technologies,
            'recent_activity': recent_activity,
            'summary': {
                'total_tasks': len(tasks),
                'active_technologies': len(set(
                    entity for result in technologies
                    for entity in result.entities
                )),
                'recent_updates': len(recent_activity)
            }
        }


# Global search engine instance
_search_engine: Optional[GraphSearchEngine] = None


async def get_search_engine() -> GraphSearchEngine:
    """Get the global search engine instance."""
    global _search_engine

    if not _search_engine:
        _search_engine = GraphSearchEngine()
        await _search_engine.initialize()

    return _search_engine


# Convenience functions for common searches
async def search_knowledge(query: str, limit: int = 10) -> List[SearchResult]:
    """Simple knowledge search."""
    engine = await get_search_engine()
    return await engine.search(SearchQuery(text=query, limit=limit))


async def find_project_info(project_name: str) -> Dict[str, Any]:
    """Find comprehensive information about a project."""
    engine = await get_search_engine()
    return await engine.get_project_overview(project_name)


async def find_task_context(task_id: str) -> List[SearchResult]:
    """Find context for a specific task."""
    engine = await get_search_engine()
    return await engine.get_context_for_task(task_id)


async def find_related_work(concept: str) -> List[SearchResult]:
    """Find work related to a concept."""
    engine = await get_search_engine()
    query = QueryTemplates.find_related_concepts(concept)
    return await engine.search(query)


# Example usage and testing
async def test_search_system():
    """Test the search and retrieval system."""
    try:
        engine = await get_search_engine()

        # Test basic search
        logger.info("Testing basic search...")
        basic_results = await search_knowledge("Graphiti Task Master integration")
        logger.info(f"Basic search returned {len(basic_results)} results")

        for i, result in enumerate(basic_results[:3]):
            logger.info(f"Result {i+1}: Score={result.relevance_score:.3f}, Content preview: {result.content[:100]}...")

        # Test project overview
        logger.info("\nTesting project overview...")
        project_info = await find_project_info("MOKAI")
        logger.info(f"Project overview: {project_info['summary']}")

        # Test faceted search
        logger.info("\nTesting faceted search...")
        facets = {
            'technologies': ['Graphiti', 'Neo4j', 'Python'],
            'concepts': ['task', 'project', 'knowledge']
        }
        faceted_results = await engine.faceted_search("implementation", facets)
        for facet, results in faceted_results.items():
            logger.info(f"Facet '{facet}': {len(results)} results")

        # Test query templates
        logger.info("\nTesting query templates...")
        template_query = QueryTemplates.find_recent_work(7)
        recent_results = await engine.search(template_query)
        logger.info(f"Recent work search returned {len(recent_results)} results")

        logger.info("✅ Search system test completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Search system test failed: {e}")
        raise


if __name__ == "__main__":
    # Run test if script is executed directly
    asyncio.run(test_search_system())
