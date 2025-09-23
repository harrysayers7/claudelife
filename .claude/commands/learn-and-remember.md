Learn from recent interactions and store key information in memory:

## Pre-Steps:
1. **Check for git reminder**: Look for `.memory-capture-needed` file
2. **If reminder exists**: Include its contents in the learning and memory context

## Learning Phase:
1. Analyze memory/performance.json for patterns
2. Identify patterns in:
   - Successful task completions
   - Failed attempts
   - Time-saving workflows
   - User corrections

3. Update CLAUDE.md section "## Learned Patterns" with:
   - New successful patterns
   - Deprecated approaches
   - User preferences discovered

## Memory Phase:
Parse recent interactions to identify:
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

## Final Report:
Generate combined insight report:
# Learning & Memory Report - [Date]

## Success Patterns (Keep doing)
-

## Failure Patterns (Stop doing)
-

## Optimizations Discovered
-

## User Preferences Noted
-

## Entities Captured
-

## Relationships Mapped
-

Save to memory/learning-reports/

## Post-Steps:
1. **Confirm what was learned and remembered**
2. **Check if `.memory-capture-needed` exists**
3. **If reminder file exists**: Ask user if they want to delete it
4. **Suggest**: `rm .memory-capture-needed` to clear the reminder
