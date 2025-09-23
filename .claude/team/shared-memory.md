# Shared Team Memory

## Entity Namespaces

### Personal Entities (Private)
personal/[user]/entities/
- Only visible to owner
- Can reference shared entities
- Can be selectively shared

### Team Entities (Shared)
team/entities/
- Visible to all team members
- Collectively maintained
- Version controlled
- Audit logged

### Public Entities (Organization)
org/entities/
- Organization-wide knowledge
- Read-only for most users
- Maintained by admins

## Relationship Visibility

### Private Relationships
- Both entities private → Relationship private
- One entity private → Relationship private

### Shared Relationships
- Both entities shared → Relationship shared
- Can be marked sensitive

## Knowledge Merge System

When team members contribute knowledge:
1. Check for duplicate entities
2. Merge attributes (union)
3. Preserve attribution
4. Update confidence scores
5. Log contribution

Format:
{
  "entity": "Project Apollo",
  "contributors": [
    {"user": "alice", "timestamp": "...", "attributes": {}},
    {"user": "bob", "timestamp": "...", "attributes": {}}
  ],
  "merged_attributes": {},
  "confidence": 0.95
}
