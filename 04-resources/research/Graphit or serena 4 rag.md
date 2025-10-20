---
Done: false
today: false
follow up: false
this week: false
back burner: false
ASAP: false
type:
  - research 
status:
relation:
description:
effort:
ai-assigned: false
ai-ignore: false
ai-ask: false
priority:
agent:
---
# Graphiti vs Serena: Knowledge Architecture Analysis

You're asking the **right question** — Serena and Graphiti solve different problems, and understanding the distinction is critical before migrating your knowledge layer.

---

## 🎯 Core Difference: Storage Philosophy

### **Serena MCP**
- **Static memory persistence** — stores conversation context as flat JSON/text
- **Retrieval = keyword/semantic search** over stored conversations
- **Best for:** Continuity across sessions, "remember what I said last week"
- **Limitation:** No relational understanding — treats memories as isolated artifacts

### **Graphiti**
- **Dynamic knowledge graph** — stores entities, relationships, and temporal context
- **Retrieval = graph traversal** — "find all projects connected to React that involve authentication"
- **Best for:** Complex reasoning, multi-hop queries, evolving knowledge structures
- **Limitation:** Requires structured ingestion — can't just dump raw conversation text

---

## 🔬 When Graphiti Actually Wins

Graphiti becomes **meaningfully better** when you need:

### 1. **Multi-Dimensional Context**
```
Serena: "User discussed authentication on 2024-10-15"
Graphiti:
  - User → works_on → Project_X
  - Project_X → uses → NextAuth
  - NextAuth → requires → PostgreSQL
  - User → previously_struggled_with → PostgreSQL_connection_pooling
```

### 2. **Temporal Reasoning**
```
Query: "What was I building before I started this current project?"
Serena: Full-text search through chronological memories (slow, imprecise)
Graphiti: Traverse (User)-[:WORKED_ON {start_date, end_date}]->(Project) edges
```

### 3. **Automatic Knowledge Evolution**
```
Session 1: "I'm building a React app"
Session 2: "The app needs authentication"
Session 3: "Using Supabase for auth"

Graphiti automatically merges:
  (React_App)-[:USES]->(Supabase_Auth)

Serena stores 3 separate memories with no connection
```

---

## ⚖️ Decision Framework

| Use Case | Serena | Graphiti |
|----------|--------|----------|
| "Remember conversation from last week" | ✅ Better | ❌ Overkill |
| "What tools do I use for music production?" | ✅ Sufficient | ✅ Better structure |
| "Find all unfinished projects related to crypto automation" | ❌ Poor | ✅ Ideal |
| "What did I learn about Wim Hof breathing?" | ✅ Perfect | ❌ Unnecessary |
| "Connect my Obsidian vault knowledge to Claude sessions" | ❌ Manual | ✅ Automated |
| Low-friction setup | ✅ Plug-and-play | ❌ Requires architecture |

---

## 🧬 Intelligent Storage Strategy for Graphiti

The key to making Graphiti **intelligently** store/retrieve is **structured ingestion pipelines** — not just dumping conversation text.

### Architecture Pattern

```
┌─────────────────────────────────────────────────────────┐
│         Claude Code Session                              │
│  ↓                                                       │
│  Event Detector (identifies storage-worthy moments)     │
│  ↓                                                       │
│  Entity Extractor (NLP → structured data)               │
│  ↓                                                       │
│  Graphiti Ingestion Layer                               │
│  ↓                                                       │
│  Knowledge Graph (nodes + relationships)                │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Implementation: Intelligent Storage Pipeline

### 1. **Event Detection Layer** (`detect_storage_event.py`)

```python
#!/usr/bin/env python3
import json
import re

STORAGE_TRIGGERS = {
    "project_creation": r"(?i)(created?|start(ed|ing)|new) (project|repo|app)",
    "tool_adoption": r"(?i)(using|switched to|adopted) ([A-Z]\w+)",
    "problem_solved": r"(?i)(fixed|solved|resolved|working now)",
    "learning_moment": r"(?i)(learned|discovered|realized|found out)",
    "goal_setting": r"(?i)(want to|planning to|goal|objective)",
    "connection": r"(?i)(related to|part of|connects to|depends on)"
}

def should_store(tool_output):
    """Determine if tool output warrants Graphiti storage"""
    for event_type, pattern in STORAGE_TRIGGERS.items():
        if re.search(pattern, tool_output):
            return event_type
    return None

def extract_context(tool_output, event_type):
    """Pull relevant entities from the text"""
    # This is where you'd use Claude or an NLP model
    # For now, simple regex extraction

    if event_type == "project_creation":
        project_name = re.search(r"project[:\s]+(\w+)", tool_output, re.I)
        return {"entity_type": "project", "name": project_name.group(1) if project_name else "unknown"}

    elif event_type == "tool_adoption":
        tool_name = re.search(r"(?:using|switched to|adopted)\s+([A-Z]\w+)", tool_output, re.I)
        return {"entity_type": "tool", "name": tool_name.group(1) if tool_name else "unknown"}

    # Add more extraction logic per event type
    return {}
```

---

### 2. **Entity Extraction via Claude** (`extract_entities.py`)

```python
#!/usr/bin/env python3
import anthropic
import json
import os

def extract_structured_knowledge(raw_text):
    """Use Claude to convert conversation text into graph entities"""

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Extract structured knowledge from this coding session output:

{raw_text}

Return JSON with this schema:
{{
  "entities": [
    {{
      "name": "entity name",
      "type": "project|tool|concept|file|problem",
      "properties": {{"key": "value"}}
    }}
  ],
  "relationships": [
    {{
      "from": "entity1",
      "to": "entity2",
      "type": "uses|part_of|depends_on|solves|created_for",
      "properties": {{"context": "why this connection exists"}}
    }}
  ]
}}

Focus on extracting:
- Tools/technologies mentioned
- Projects or codebases referenced
- Problems solved
- Concepts learned
- Files created/modified

Only extract meaningful, persistent knowledge — not transient debugging steps."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(message.content[0].text)
```

---

### 3. **Intelligent Graphiti Ingestion** (`store_to_graphiti.py`)

```python
#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime

GRAPHITI_URL = "http://localhost:8080/graphiti/api/v1"
AUTH_TOKEN = os.getenv("GRAPHITI_TOKEN")

def store_knowledge(structured_data):
    """Store extracted entities and relationships in Graphiti"""

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    # First, create/update entities
    entity_ids = {}
    for entity in structured_data.get("entities", []):
        payload = {
            "name": entity["name"],
            "entity_type": entity["type"],
            "properties": {
                **entity.get("properties", {}),
                "last_updated": datetime.now().isoformat(),
                "source": "claude_code"
            }
        }

        # Check if entity exists first (merge instead of duplicate)
        search_response = requests.post(
            f"{GRAPHITI_URL}/search",
            headers=headers,
            json={"query": entity["name"], "entity_type": entity["type"], "limit": 1}
        )

        if search_response.ok and search_response.json().get("nodes"):
            # Update existing entity
            entity_id = search_response.json()["nodes"][0]["id"]
            requests.put(
                f"{GRAPHITI_URL}/entities/{entity_id}",
                headers=headers,
                json=payload
            )
        else:
            # Create new entity
            response = requests.post(
                f"{GRAPHITI_URL}/entities",
                headers=headers,
                json=payload
            )
            entity_id = response.json().get("id")

        entity_ids[entity["name"]] = entity_id

    # Then create relationships
    for rel in structured_data.get("relationships", []):
        if rel["from"] in entity_ids and rel["to"] in entity_ids:
            edge_payload = {
                "from_entity_id": entity_ids[rel["from"]],
                "to_entity_id": entity_ids[rel["to"]],
                "edge_type": rel["type"],
                "properties": {
                    **rel.get("properties", {}),
                    "created_at": datetime.now().isoformat()
                }
            }

            requests.post(
                f"{GRAPHITI_URL}/edges",
                headers=headers,
                json=edge_payload
            )

    print(f"✓ Stored {len(structured_data['entities'])} entities, {len(structured_data['relationships'])} relationships")
```

---

### 4. **Intelligent Retrieval** (`retrieve_context.py`)

```python
#!/usr/bin/env python3
import requests
import json
import os

GRAPHITI_URL = "http://localhost:8080/graphiti/api/v1"
AUTH_TOKEN = os.getenv("GRAPHITI_TOKEN")

def retrieve_relevant_context(current_activity_description):
    """Query Graphiti for contextually relevant knowledge"""

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    # Step 1: Extract key terms from current activity
    # (In production, use Claude for this)
    key_terms = extract_key_terms(current_activity_description)

    # Step 2: Multi-hop graph query
    query = {
        "start_nodes": key_terms,
        "max_depth": 2,  # Traverse up to 2 relationships away
        "edge_types": ["uses", "part_of", "related_to", "depends_on"],
        "entity_types": ["project", "tool", "concept", "problem"]
    }

    response = requests.post(
        f"{GRAPHITI_URL}/traverse",
        headers=headers,
        json=query
    )

    if response.ok:
        graph_data = response.json()

        # Format as context for Claude
        context_summary = format_graph_context(graph_data)
        return context_summary

    return None

def extract_key_terms(text):
    """Extract entities from current activity description"""
    # Placeholder — use Claude or NLP model
    words = text.lower().split()
    # Filter for capitalized words, tech terms, etc.
    return [w for w in words if w[0].isupper() or w in TECH_KEYWORDS]

def format_graph_context(graph_data):
    """Convert graph response into readable context"""
    context = "## Relevant Knowledge\n\n"

    for node in graph_data.get("nodes", []):
        context += f"**{node['name']}** ({node['entity_type']})\n"
        if node.get("properties"):
            context += f"  - {json.dumps(node['properties'], indent=2)}\n"

    context += "\n## Relationships\n"
    for edge in graph_data.get("edges", []):
        context += f"- {edge['from']} → {edge['type']} → {edge['to']}\n"

    return context

TECH_KEYWORDS = {
    "react", "python", "obsidian", "supabase", "claude",
    "graphiti", "api", "database", "authentication", "ableton"
}
```

---

## 🔗 Updated Hook Configuration

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "python3 ~/.claude/scripts/retrieve_context.py '${PROJECT_DIR}' > ~/.claude/active_context.md"
      }
    ],
    "PostToolUse": [
      {
        "type": "command",
        "command": "python3 ~/.claude/scripts/detect_storage_event.py '${TOOL_OUTPUT}' && python3 ~/.claude/scripts/extract_entities.py '${TOOL_OUTPUT}' | python3 ~/.claude/scripts/store_to_graphiti.py"
      }
    ]
  }
}
```

---

## 🎯 Hybrid Strategy: Serena + Graphiti

**Best approach for your workflow:**

| Layer | Tool | Purpose |
|-------|------|---------|
| **Conversational Memory** | Serena | "What did we discuss about cold exposure?" |
| **Structured Knowledge** | Graphiti | "All projects using Supabase with auth issues" |
| **Human Archive** | Obsidian | Daily notes, manual insights, long-form thinking |

### Workflow Example:
1. **Claude Code session starts** → Retrieve from Graphiti (structured context) + Serena (recent conversation)
2. **During session** → Serena logs everything, Graphiti ingests only structured knowledge
3. **Session ends** → Create Obsidian daily note linking to both

---

## 🚨 Critical Consideration

**Graphiti requires more engineering investment** than Serena:
- Need entity extraction pipeline (Claude API costs)
- Schema design for your domain (music production, crypto, business)
- Merge logic to avoid duplicate entities
- Query optimization for fast retrieval

**My recommendation:**
1. **Keep Serena** for conversational continuity (it's working fine)
2. **Add Graphiti** as a **secondary layer** for structured knowledge
3. **Use Obsidian** as the human-readable archive that links both

This gives you:
- **Speed** (Serena is faster for simple recall)
- **Intelligence** (Graphiti for complex queries)
- **Control** (Obsidian for manual curation)

Want me to build you a complete bridge system that syncs Serena → Graphiti → Obsidian automatically?
