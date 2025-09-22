Store information in the memory graph:

## Pre-Steps:
1. **Check for git reminder**: Look for `.memory-capture-needed` file
2. **If reminder exists**: Include its contents in the memory capture context

## Main Process:
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

## Post-Steps:
1. **Confirm what was remembered**
2. **Check if `.memory-capture-needed` exists**
3. **If reminder file exists**: Ask user if they want to delete it
4. **Suggest**: `rm .memory-capture-needed` to clear the reminder