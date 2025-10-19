---
created: "2025-10-17 12:38"
description: |
  Updates the Graphiti knowledge graph structure visualization at 04-resources/guides/graphiti-tree.md with current state.
  Regenerates the entire file with:
    - Current entity hierarchy and statistics
    - Relationship mappings and network analysis
    - Domain coverage breakdown
    - Growth recommendations highlighting gaps
    - Changelog showing recent additions since last update
  Use this whenever you want a visual snapshot of the knowledge graph structure without exposing actual knowledge content.
examples:
  - /update-graphiti-tree
---

# Update Graphiti Tree

This command regenerates the Graphiti knowledge graph structure visualization with current state, providing a visual representation of entities, relationships, and highlighting areas for growth.

## Usage

```bash
/update-graphiti-tree
```

## Process

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

I'll silently update the knowledge graph structure file by:

1. **Query Current State**: Fetch all entities and relationships from Graphiti using `mcp__memory__read_graph`

2. **Read Previous State**: Read the existing `/04-resources/guides/graphiti-tree.md` to extract:
   - Previous entity counts by type
   - Previous relationship counts
   - Last update timestamp

3. **Analyze Structure**: Process the current graph data to:
   - Group entities by type (Person, Business, Client, etc.)
   - Count relationships by type
   - Identify isolated entities (no relationships)
   - Calculate network density and hub entities
   - Calculate domain coverage percentages

4. **Identify Changes**: Compare current vs previous state to generate changelog:
   - New entities added (by type and name)
   - New relationships created
   - Entities removed (if any)
   - Relationships removed (if any)

5. **Highlight Gaps**: Analyze the structure for growth opportunities:
   - Isolated entities that need connections
   - Under-represented domains (e.g., "MOKAI has no contractors/clients")
   - Missing relationship types
   - Imbalanced entity distributions

6. **Regenerate File**: Write the complete new version of `graphiti-tree.md` with:
   - Updated frontmatter with current date
   - Complete entity type hierarchy with current counts
   - All relationship structures
   - Current statistics tables
   - Network density analysis
   - Domain coverage breakdown
   - Growth recommendations based on current gaps
   - Changelog section at the bottom showing changes since last update

7. **Update Timestamp**: Set "Last synchronized" to current timestamp

## Output Format

The regenerated file includes:

### Main Sections
- **Entity Type Hierarchy**: Visual tree showing all entity types and counts
- **Relationship Structure**: Diagrams showing how entities connect
- **Entity Statistics**: Tables with counts and percentages
- **Relationship Statistics**: Breakdown of relationship types
- **Network Density Analysis**: Most connected entities, hubs, isolated nodes
- **Domain Coverage**: Business, personal, financial domain percentages
- **Growth Recommendations**: Specific suggestions based on current gaps
- **Usage Notes**: How to query and work with the graph
- **Query Patterns**: Example code for common operations

### Changelog Section (New)
```markdown
## Changelog

### 2025-10-17 12:38
**Added Entities**:
- Person: New Person Name
- Client: New Client Name

**Added Relationships**:
- Harrison Robert Sayers → works_with → New Client Name

**Statistics**:
- Total entities: 15 → 17 (+2)
- Total relationships: 9 → 10 (+1)
- Isolated entities: 6 → 5 (-1)
```

## Gap Analysis

The command automatically highlights:

1. **Isolated Entities**: Entities with no relationships that should be connected
   - Example: "CRYPTO, SMSF have no connections - consider adding investment details"

2. **Under-Represented Domains**:
   - Example: "MOKAI has minimal relationships - add clients, contractors, services"
   - Example: "Only 1 client tracked - add more MOK Music client entities"

3. **Missing Relationship Types**:
   - Example: "No contractor relationships defined yet"
   - Example: "No project or campaign entities linked to clients"

4. **Domain Imbalances**:
   - Example: "60% business entities but only 13% financial - expand investment tracking"

## Evaluation Criteria

A successful update should:
1. ✅ Query Graphiti without errors
2. ✅ Preserve all existing file formatting and structure
3. ✅ Update all statistics accurately (entity counts, relationships, percentages)
4. ✅ Generate meaningful changelog entries showing what changed
5. ✅ Highlight specific, actionable gaps in the knowledge graph
6. ✅ Update timestamp to current date/time
7. ✅ Maintain visual tree formatting with proper indentation

## Technical Notes

### Data Sources
- **Primary**: `mcp__memory__read_graph` - Returns complete graph structure
- **Previous state**: Extracted from existing `graphiti-tree.md` frontmatter and statistics

### Change Detection
- Compare entity counts by type between previous and current
- Identify new entity names not in previous list
- Compare relationship counts and types
- Calculate net changes (additions/removals)

### Performance
- Single Graphiti query: ~1 second
- File parsing and generation: <1 second
- Total execution time: ~2-3 seconds

No caching or companion scripts needed due to fast execution and simple data structure.

## Related Resources

- Graphiti MCP Documentation: `mcp__memory__*` tools
- Example usage: See `/mokai-master` command for Graphiti integration patterns
- Knowledge graph file: `/04-resources/guides/graphiti-tree.md`
