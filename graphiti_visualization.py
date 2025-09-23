"""
Graphiti Visualization and Integration System

Provides visualization endpoints, web interface integration, and system-wide
integration with Task Master and personal assistant workflows.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import os

from graphiti_config import get_graphiti
from graphiti_knowledge_capture import get_knowledge_capture
from graphiti_search import get_search_engine, SearchQuery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GraphNode:
    """Represents a node in the visualization graph."""
    id: str
    label: str
    type: str
    properties: Dict[str, Any]
    size: float = 1.0
    color: str = "#97C2FC"


@dataclass
class GraphEdge:
    """Represents an edge in the visualization graph."""
    from_id: str
    to_id: str
    label: str
    type: str
    properties: Dict[str, Any]
    weight: float = 1.0


@dataclass
class GraphVisualization:
    """Complete graph visualization data."""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    metadata: Dict[str, Any]


class Neo4jVisualizationQueries:
    """Neo4j queries for visualization data extraction."""

    @staticmethod
    def get_overview_graph(limit: int = 50) -> str:
        """Get an overview of the entire graph."""
        return f"""
        MATCH (n:Entity)-[r:RELATES_TO]->(m:Entity)
        RETURN n, r, m
        LIMIT {limit}
        """

    @staticmethod
    def get_project_subgraph(project_name: str, limit: int = 30) -> str:
        """Get a subgraph focused on a specific project."""
        return f"""
        MATCH (n:Entity)-[r:RELATES_TO]->(m:Entity)
        WHERE n.name CONTAINS '{project_name}' OR m.name CONTAINS '{project_name}'
        RETURN n, r, m
        LIMIT {limit}
        """

    @staticmethod
    def get_task_context_graph(task_id: str, depth: int = 2) -> str:
        """Get graph context around a specific task."""
        return f"""
        MATCH (n:Entity)-[r:RELATES_TO*1..{depth}]->(m:Entity)
        WHERE n.name CONTAINS 'task' OR n.name CONTAINS '{task_id}'
        RETURN n, r, m
        LIMIT 40
        """

    @staticmethod
    def get_technology_network(technology: str, limit: int = 25) -> str:
        """Get network of relationships around a technology."""
        return f"""
        MATCH (n:Entity)-[r:RELATES_TO]->(m:Entity)
        WHERE n.name CONTAINS '{technology}' OR m.name CONTAINS '{technology}'
           OR r.name CONTAINS 'uses_technology' OR r.name CONTAINS 'implements'
        RETURN n, r, m
        LIMIT {limit}
        """

    @staticmethod
    def get_recent_activity_graph(days: int = 7, limit: int = 30) -> str:
        """Get recent activity in the knowledge graph."""
        return f"""
        MATCH (n:Entity)-[r:RELATES_TO]->(m:Entity)
        WHERE r.created_at > datetime() - duration({{days: {days}}})
        RETURN n, r, m
        ORDER BY r.created_at DESC
        LIMIT {limit}
        """


class GraphVisualizationEngine:
    """Main visualization engine for Graphiti knowledge graph."""

    def __init__(self):
        self.graphiti = None
        self.knowledge_capture = None
        self.search_engine = None
        self.color_scheme = {
            'project': '#FF6B6B',      # Red for projects
            'technology': '#4ECDC4',   # Teal for technologies
            'task': '#45B7D1',         # Blue for tasks
            'concept': '#96CEB4',      # Green for concepts
            'person': '#FFEAA7',       # Yellow for people
            'tool': '#DDA0DD',         # Purple for tools
            'default': '#97C2FC'       # Light blue default
        }

    async def initialize(self):
        """Initialize the visualization engine."""
        self.graphiti = await get_graphiti()
        self.knowledge_capture = await get_knowledge_capture()
        self.search_engine = await get_search_engine()
        logger.info("Graph visualization engine initialized")

    async def get_graph_overview(self, limit: int = 50) -> GraphVisualization:
        """Get an overview visualization of the entire graph."""
        try:
            # Execute Neo4j query to get graph data
            driver = self.graphiti.driver
            nodes = []
            edges = []

            query = Neo4jVisualizationQueries.get_overview_graph(limit)

            # Create session directly (handle async properly)
            session = driver.session()
            try:
                result = session.run(query)
                records = list(result)

                node_ids = set()

                for record in records:
                    # Process nodes
                    for node_key in ['n', 'm']:
                        if node_key in record:
                            node_data = dict(record[node_key])
                            node_id = str(node_data.get('uuid', ''))

                            if node_id and node_id not in node_ids:
                                node_ids.add(node_id)

                                node_type = self._classify_node_type(node_data.get('name', ''))

                                nodes.append(GraphNode(
                                    id=node_id,
                                    label=node_data.get('name', 'Unknown')[:30],
                                    type=node_type,
                                    properties=dict(node_data),
                                    size=self._calculate_node_size(node_data),
                                    color=self.color_scheme.get(node_type, self.color_scheme['default'])
                                ))

                    # Process relationships
                    if 'r' in record:
                        rel_data = dict(record['r'])
                        from_node = dict(record.get('n', {}))
                        to_node = dict(record.get('m', {}))

                        if from_node and to_node:
                            edges.append(GraphEdge(
                                from_id=str(from_node.get('uuid', '')),
                                to_id=str(to_node.get('uuid', '')),
                                label=rel_data.get('name', 'relates_to'),
                                type=rel_data.get('name', 'relates_to'),
                                properties=dict(rel_data),
                                weight=self._calculate_edge_weight(rel_data)
                            ))
            finally:
                session.close()

            return GraphVisualization(
                nodes=nodes,
                edges=edges,
                metadata={
                    'total_nodes': len(nodes),
                    'total_edges': len(edges),
                    'query_type': 'overview',
                    'limit': limit,
                    'generated_at': datetime.now(timezone.utc).isoformat()
                }
            )

        except Exception as e:
            logger.error(f"Failed to generate graph overview: {e}")
            return GraphVisualization(
                nodes=[],
                edges=[],
                metadata={
                    'error': str(e),
                    'total_nodes': 0,
                    'total_edges': 0,
                    'query_type': 'overview',
                    'limit': limit,
                    'generated_at': datetime.now(timezone.utc).isoformat()
                }
            )

    async def get_project_visualization(self, project_name: str, limit: int = 30) -> GraphVisualization:
        """Get visualization focused on a specific project."""
        try:
            driver = self.graphiti.driver
            nodes = []
            edges = []

            query = Neo4jVisualizationQueries.get_project_subgraph(project_name, limit)

            # Create session directly
            session = driver.session()
            try:
                result = session.run(query)
                records = list(result)

                node_ids = set()

                for record in records:
                    # Process nodes (same logic as overview)
                    for node_key in ['n', 'm']:
                        if node_key in record:
                            node_data = dict(record[node_key])
                            node_id = str(node_data.get('uuid', ''))

                            if node_id and node_id not in node_ids:
                                node_ids.add(node_id)

                                node_type = self._classify_node_type(node_data.get('name', ''))

                                # Highlight project-related nodes
                                if project_name.lower() in node_data.get('name', '').lower():
                                    size_multiplier = 1.5
                                    color = '#FF4757'  # Bright red for project focus
                                else:
                                    size_multiplier = 1.0
                                    color = self.color_scheme.get(node_type, self.color_scheme['default'])

                                nodes.append(GraphNode(
                                    id=node_id,
                                    label=node_data.get('name', 'Unknown')[:30],
                                    type=node_type,
                                    properties=dict(node_data),
                                    size=self._calculate_node_size(node_data) * size_multiplier,
                                    color=color
                                ))

                    # Process relationships
                    if 'r' in record:
                        rel_data = dict(record['r'])
                        from_node = dict(record.get('n', {}))
                        to_node = dict(record.get('m', {}))

                        if from_node and to_node:
                            edges.append(GraphEdge(
                                from_id=str(from_node.get('uuid', '')),
                                to_id=str(to_node.get('uuid', '')),
                                label=rel_data.get('name', 'relates_to'),
                                type=rel_data.get('name', 'relates_to'),
                                properties=dict(rel_data),
                                weight=self._calculate_edge_weight(rel_data)
                            ))
            finally:
                session.close()

            return GraphVisualization(
                nodes=nodes,
                edges=edges,
                metadata={
                    'total_nodes': len(nodes),
                    'total_edges': len(edges),
                    'query_type': 'project',
                    'project_name': project_name,
                    'limit': limit,
                    'generated_at': datetime.now(timezone.utc).isoformat()
                }
            )

        except Exception as e:
            logger.error(f"Failed to generate project visualization for {project_name}: {e}")
            return GraphVisualization(
                nodes=[],
                edges=[],
                metadata={
                    'error': str(e),
                    'total_nodes': 0,
                    'total_edges': 0,
                    'query_type': 'project',
                    'project_name': project_name,
                    'limit': limit,
                    'generated_at': datetime.now(timezone.utc).isoformat()
                }
            )

    def _classify_node_type(self, node_name: str) -> str:
        """Classify node type based on name patterns."""
        name_lower = node_name.lower()

        if any(project in name_lower for project in ['mokai', 'mok music', 'brain', 'mac']):
            return 'project'
        elif any(tech in name_lower for tech in ['python', 'neo4j', 'graphiti', 'claude', 'api', 'database']):
            return 'technology'
        elif 'task' in name_lower:
            return 'task'
        elif any(tool in name_lower for tool in ['linear', 'github', 'trigger.dev', 'mcp', 'git']):
            return 'tool'
        elif any(person in name_lower for person in ['harry', 'harrison', 'user', 'team']):
            return 'person'
        else:
            return 'concept'

    def _calculate_node_size(self, node_data: Dict[str, Any]) -> float:
        """Calculate node size based on importance/connections."""
        # Simple heuristic - could be enhanced with actual degree calculation
        base_size = 1.0

        # Increase size for certain types
        name = node_data.get('name', '').lower()
        if any(important in name for important in ['mokai', 'graphiti', 'task master']):
            base_size *= 1.5

        return max(0.5, min(3.0, base_size))  # Clamp between 0.5 and 3.0

    def _calculate_edge_weight(self, edge_data: Dict[str, Any]) -> float:
        """Calculate edge weight based on relationship strength."""
        base_weight = 1.0

        # Increase weight for important relationships
        rel_name = edge_data.get('name', '').lower()
        if any(strong in rel_name for strong in ['implements', 'uses_technology', 'integrates_with']):
            base_weight *= 1.5

        return max(0.1, min(3.0, base_weight))

    async def export_for_neovis(self, visualization: GraphVisualization) -> Dict[str, Any]:
        """Export visualization data in neovis.js compatible format."""
        neovis_data = {
            'nodes': [],
            'edges': [],
            'config': {
                'container_id': 'graph-container',
                'server_url': 'bolt://localhost:7687',
                'server_user': 'neo4j',
                'server_password': 'neo4j',
                'labels': {},
                'relationships': {},
                'initial_cypher': 'MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 25'
            }
        }

        # Convert nodes to neovis format
        for node in visualization.nodes:
            neovis_data['nodes'].append({
                'id': node.id,
                'label': node.label,
                'group': node.type,
                'color': node.color,
                'size': node.size * 10,  # Scale for neovis
                'properties': node.properties
            })

        # Convert edges to neovis format
        for edge in visualization.edges:
            neovis_data['edges'].append({
                'from': edge.from_id,
                'to': edge.to_id,
                'label': edge.label,
                'width': edge.weight * 2,
                'properties': edge.properties
            })

        # Configure neovis labels and relationships
        node_types = set(node.type for node in visualization.nodes)
        for node_type in node_types:
            neovis_data['config']['labels'][node_type] = {
                'caption': 'name',
                'size': 'pagerank',
                'community': 'community'
            }

        edge_types = set(edge.type for edge in visualization.edges)
        for edge_type in edge_types:
            neovis_data['config']['relationships'][edge_type] = {
                'caption': 'name',
                'thickness': 'weight'
            }

        return neovis_data

    async def save_visualization_html(self, visualization: GraphVisualization, output_file: str = "graph_visualization.html"):
        """Save an interactive HTML visualization using vis.js."""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Graphiti Knowledge Graph Visualization</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        #graph-container {
            width: 100%;
            height: 800px;
            border: 1px solid #ddd;
            background-color: white;
        }
        .controls {
            margin-bottom: 20px;
            padding: 15px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            margin: 5px;
            padding: 10px 15px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .legend {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <h1>Graphiti Knowledge Graph Visualization</h1>

    <div class="controls">
        <button onclick="fitGraph()">Fit Graph</button>
        <button onclick="resetZoom()">Reset Zoom</button>
        <button onclick="togglePhysics()">Toggle Physics</button>
        <button onclick="exportGraph()">Export Data</button>
    </div>

    <div id="graph-container"></div>

    <div class="info">
        <h3>Graph Information</h3>
        <p><strong>Nodes:</strong> {total_nodes} | <strong>Edges:</strong> {total_edges}</p>
        <p><strong>Generated:</strong> {generated_at}</p>

        <h4>Legend</h4>
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background-color: #FF6B6B;"></div>
                <span>Projects</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #4ECDC4;"></div>
                <span>Technologies</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #45B7D1;"></div>
                <span>Tasks</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #96CEB4;"></div>
                <span>Concepts</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #FFEAA7;"></div>
                <span>People</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #DDA0DD;"></div>
                <span>Tools</span>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        // Graph data
        var nodes = new vis.DataSet({nodes_data});
        var edges = new vis.DataSet({edges_data});

        var data = {{
            nodes: nodes,
            edges: edges
        }};

        var options = {{
            layout: {{
                improvedLayout: true
            }},
            physics: {{
                enabled: true,
                stabilization: {{
                    iterations: 200
                }},
                barnesHut: {{
                    gravitationalConstant: -2000,
                    centralGravity: 0.3,
                    springLength: 200,
                    springConstant: 0.05,
                    damping: 0.09
                }}
            }},
            nodes: {{
                shape: 'dot',
                scaling: {{
                    min: 10,
                    max: 30
                }},
                font: {{
                    size: 12,
                    face: 'Arial'
                }}
            }},
            edges: {{
                width: 2,
                color: {{inherit: 'from'}},
                smooth: {{
                    type: 'continuous'
                }},
                arrows: {{
                    to: {{enabled: true, scaleFactor: 0.5}}
                }},
                font: {{
                    size: 10
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200
            }}
        }};

        var container = document.getElementById('graph-container');
        var network = new vis.Network(container, data, options);

        // Event handlers
        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodes.get(nodeId);
                alert('Node: ' + node.label + '\\nType: ' + node.group);
            }}
        }});

        // Control functions
        function fitGraph() {{
            network.fit();
        }}

        function resetZoom() {{
            network.moveTo({{scale: 1}});
        }}

        var physicsEnabled = true;
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{physics: {{enabled: physicsEnabled}}}});
        }}

        function exportGraph() {{
            var graphData = {{
                nodes: nodes.get(),
                edges: edges.get()
            }};
            var dataStr = JSON.stringify(graphData, null, 2);
            var dataBlob = new Blob([dataStr], {{type: 'application/json'}});
            var url = URL.createObjectURL(dataBlob);
            var link = document.createElement('a');
            link.href = url;
            link.download = 'graph-data.json';
            link.click();
        }}
    </script>
</body>
</html>
"""

        # Convert visualization data to vis.js format
        vis_nodes = []
        for node in visualization.nodes:
            vis_nodes.append({
                'id': node.id,
                'label': node.label,
                'group': node.type,
                'color': node.color,
                'size': node.size * 20,  # Scale for vis.js
                'title': f"Type: {node.type}\\nProperties: {len(node.properties)}"
            })

        vis_edges = []
        for edge in visualization.edges:
            vis_edges.append({
                'from': edge.from_id,
                'to': edge.to_id,
                'label': edge.label,
                'width': edge.weight * 3,
                'title': f"Relationship: {edge.type}"
            })

        # Format the HTML using string replacement instead of .format() to avoid brace conflicts
        html_content = html_template.replace('{nodes_data}', json.dumps(vis_nodes))
        html_content = html_content.replace('{edges_data}', json.dumps(vis_edges))
        html_content = html_content.replace('{total_nodes}', str(len(vis_nodes)))
        html_content = html_content.replace('{total_edges}', str(len(vis_edges)))
        html_content = html_content.replace('{generated_at}', visualization.metadata.get('generated_at', 'Unknown'))

        # Save to file
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"Saved interactive visualization to: {output_path.absolute()}")
        return str(output_path.absolute())


class PersonalAssistantIntegration:
    """Integration layer for connecting Graphiti with personal assistant systems."""

    def __init__(self):
        self.graphiti = None
        self.knowledge_capture = None
        self.search_engine = None
        self.visualization_engine = None

    async def initialize(self):
        """Initialize all integration components."""
        self.graphiti = await get_graphiti()
        self.knowledge_capture = await get_knowledge_capture()
        self.search_engine = await get_search_engine()
        self.visualization_engine = GraphVisualizationEngine()
        await self.visualization_engine.initialize()
        logger.info("Personal assistant integration initialized")

    async def capture_session_context(self, session_data: Dict[str, Any]) -> str:
        """Capture context from a Claude Code session."""
        session_content = f"""
        Claude Code Session:
        Duration: {session_data.get('duration', 'Unknown')}
        Commands Used: {', '.join(session_data.get('commands', []))}
        Files Modified: {', '.join(session_data.get('files_modified', []))}
        Tasks Completed: {', '.join(session_data.get('tasks_completed', []))}

        Session Summary:
        {session_data.get('summary', 'No summary available')}
        """

        episode_id = await self.knowledge_capture.capture_interaction_knowledge(
            session_content,
            "claude_code_session"
        )

        logger.info(f"Captured session context: {episode_id}")
        return episode_id

    async def get_project_dashboard_data(self, project_name: str) -> Dict[str, Any]:
        """Get comprehensive dashboard data for a project."""
        # Get project overview from search
        project_overview = await self.search_engine.get_project_overview(project_name)

        # Get visualization
        project_vis = await self.visualization_engine.get_project_visualization(project_name)

        # Get recent activity
        recent_query = SearchQuery(
            text=f"{project_name} recent activity",
            entities=[project_name],
            limit=5
        )
        recent_activity = await self.search_engine.search(recent_query)

        return {
            'project_name': project_name,
            'overview': project_overview,
            'visualization': asdict(project_vis),
            'recent_activity': [asdict(activity) for activity in recent_activity],
            'dashboard_generated_at': datetime.now(timezone.utc).isoformat()
        }

    async def auto_capture_task_context(self, task_id: str, context: str) -> None:
        """Automatically capture task context during execution."""
        task_data = {
            'id': task_id,
            'title': f"Auto-captured context for task {task_id}",
            'description': 'Automatically captured during task execution',
            'details': context,
            'status': 'auto-captured'
        }

        await self.knowledge_capture.capture_task_knowledge(task_data)
        logger.info(f"Auto-captured context for task {task_id}")


# Global integration instance
_integration: Optional[PersonalAssistantIntegration] = None


async def get_integration() -> PersonalAssistantIntegration:
    """Get the global integration instance."""
    global _integration

    if not _integration:
        _integration = PersonalAssistantIntegration()
        await _integration.initialize()

    return _integration


# Example usage and testing
async def test_visualization_system():
    """Test the visualization and integration system."""
    try:
        # Initialize
        integration = await get_integration()
        vis_engine = integration.visualization_engine

        # Test graph overview
        logger.info("Testing graph overview visualization...")
        overview = await vis_engine.get_graph_overview(limit=30)
        logger.info(f"Overview: {overview.metadata['total_nodes']} nodes, {overview.metadata['total_edges']} edges")

        # Test project visualization
        logger.info("Testing project visualization...")
        project_vis = await vis_engine.get_project_visualization("MOKAI", limit=20)
        logger.info(f"MOKAI visualization: {project_vis.metadata['total_nodes']} nodes, {project_vis.metadata['total_edges']} edges")

        # Test HTML export
        logger.info("Testing HTML visualization export...")
        html_file = await vis_engine.save_visualization_html(overview, "test_graph_viz.html")
        logger.info(f"Saved HTML visualization: {html_file}")

        # Test neovis export
        logger.info("Testing neovis export...")
        neovis_data = await vis_engine.export_for_neovis(project_vis)
        logger.info(f"Neovis export: {len(neovis_data['nodes'])} nodes, {len(neovis_data['edges'])} edges")

        # Test project dashboard
        logger.info("Testing project dashboard...")
        dashboard = await integration.get_project_dashboard_data("MOKAI")
        logger.info(f"Dashboard overview: {dashboard['overview']['summary']}")

        # Test session capture
        logger.info("Testing session context capture...")
        session_data = {
            'duration': '45 minutes',
            'commands': ['task-master next', 'claude search', 'git commit'],
            'files_modified': ['graphiti_visualization.py'],
            'tasks_completed': ['15.5'],
            'summary': 'Implemented visualization system for Graphiti knowledge graph'
        }
        session_id = await integration.capture_session_context(session_data)
        logger.info(f"Session captured: {session_id}")

        logger.info("✅ Visualization and integration test completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Visualization test failed: {e}")
        raise


if __name__ == "__main__":
    # Run test if script is executed directly
    asyncio.run(test_visualization_system())
