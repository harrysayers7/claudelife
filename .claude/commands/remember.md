Store information in the memory graph:

Parse the user's input to identify:
1. **Entities** (people, projects, tools, concepts)
2. **Relationships** (who knows who, what connects to what)
3. **Temporal markers** (when things happened)

Update the files:
- memory/graph/entities.json with new entities
- memory/graph/relationships.json with connections
- memory/graph/timeline.json with time-based events

Format entities as:
{
  "id": "entity_[timestamp]",
  "name": "[name]",
  "type": "[person|project|tool|concept]",
  "attributes": {},
  "created": "[timestamp]",
  "lastUpdated": "[timestamp]"
}

Format relationships as:
{
  "from": "[entity_id]",
  "to": "[entity_id]",
  "type": "[knows|manages|uses|blocks|depends_on]",
  "strength": [1-10],
  "created": "[timestamp]"
}

After storing, confirm what was remembered.