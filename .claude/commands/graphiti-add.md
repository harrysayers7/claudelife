---
version: 1.0
date: 2025-10-20
---

# /graphiti-add - Intelligent Graphiti Memory Addition

Add context-aware memories to the Graphiti knowledge graph with automatic categorization and routing.

## Usage

```bash
/graphiti-add [memory content or context description]
```

## Arguments

- **No arguments**: Analyze recent conversation context and extract memorable information
- **With content**: Add specific memory from user-provided information

## Examples

```bash
# Add person from conversation context
/graphiti-add I just had a great meeting with Sarah Chen, the CTO at TechCorp. She's interested in our IRAP services.

# Add from recent conversation
/graphiti-add
# → Analyzes last 10 messages for memorable content

# Add technical learning
/graphiti-add Just discovered that Prisma's connection pooling works better with PgBouncer in transaction mode

# Add business decision
/graphiti-add Decided to pivot MOKAI's positioning from pure cybersecurity to full technology consultancy
```

## How It Works

### 1. Context Analysis

The command analyzes input to determine:
- **Memory type**: Person, conversation, event, insight, decision, learning
- **Domain**: Business (MOKAI/MOK HOUSE), Finance, Personal, Technical
- **Entities**: People, organizations, concepts, technologies
- **Relationships**: How entities connect

### 2. Automatic Routing

**Graphiti Instance Selection**:
- `graphiti-mokai` → Business content (MOKAI, MOK HOUSE, clients, partnerships)
- `graphiti-finance` → Financial content (accounting, crypto, SMSF, investments)
- `graphiti-personal` → Personal life (relationships, health, hobbies, general learnings)

**Group IDs**:
- `mokai-business` (for graphiti-mokai)
- `financial-tracking` (for graphiti-finance)
- `personal-life` (for graphiti-personal)

### 3. Source Type Detection

**Text** (default):
- General notes, insights, learnings
- Unstructured observations

**Message**:
- Conversations, meetings, discussions
- Exchange of ideas with attribution

**JSON**:
- Structured data about people, organizations
- Complex relationships with multiple properties

### 4. Entity Extraction Patterns

**Person Memory**:
```json
{
  "person": {
    "name": "Sarah Chen",
    "role": "CTO",
    "company": "TechCorp",
    "interests": ["IRAP services", "cybersecurity"],
    "relationship": "potential client",
    "context": "Met at industry conference"
  },
  "interaction": {
    "date": "2025-10-20",
    "type": "meeting",
    "outcome": "interested in IRAP assessment"
  }
}
```

**Conversation Memory**:
```
user: What do you think about the new partnership model?
assistant: I think it has potential, but we need to validate the margin structure first.
user: Agreed. Let's schedule a financial review.
```

**Event/Decision Memory**:
```
Strategic Decision - MOKAI Pivot (2025-10-20)

Context: After reviewing Q3 performance and market feedback, decided to expand MOKAI's positioning from pure cybersecurity to full technology consultancy.

Rationale:
- Cybersecurity alone limits growth potential
- Clients requesting broader technology services
- Leverage Indigenous procurement advantage across tech stack

Next Steps:
- Update website messaging
- Retrain sales materials
- Identify technology partnerships
```

## Implementation

### Step 1: Analyze Input

```javascript
async function analyzeMemoryContext(userInput, conversationHistory) {
  const signals = {
    // Person indicators
    isPerson: /met with|meeting with|spoke to|talked to|introduced to|conversation with|call with/i.test(userInput),

    // Conversation indicators
    isConversation: conversationHistory.length > 3 && userInput.toLowerCase().includes('remember this conversation'),

    // Decision indicators
    isDecision: /decided|choosing to|going with|strategy|direction|pivot/i.test(userInput),

    // Learning indicators
    isLearning: /discovered|learned|realized|found out|insight|understanding/i.test(userInput),

    // Event indicators
    isEvent: /happened|occurred|event|milestone|launch/i.test(userInput)
  };

  // Determine primary type
  if (signals.isPerson) return 'person';
  if (signals.isConversation) return 'conversation';
  if (signals.isDecision) return 'decision';
  if (signals.isLearning) return 'learning';
  if (signals.isEvent) return 'event';
  return 'insight'; // default
}
```

### Step 2: Route to Graphiti Instance

```javascript
function routeToGraphitiInstance(content) {
  const keywords = {
    mokai: /mokai|mok house|mokhouse|client|irap|cybersecurity|penetration test|grc|safia|music production|esm/i,
    finance: /accounting|crypto|smsf|investment|tax|deduction|dividend|capital gains|invoice|bas/i,
  };

  if (keywords.mokai.test(content)) return 'graphiti-mokai';
  if (keywords.finance.test(content)) return 'graphiti-finance';
  return 'graphiti-personal';
}
```

### Step 3: Determine Source Type

```javascript
function determineSourceType(memoryType, content) {
  // Use JSON for structured person/organization data
  if (memoryType === 'person' && content.includes('company') || content.includes('role')) {
    return 'json';
  }

  // Use message for conversations
  if (memoryType === 'conversation' && content.includes('user:') || content.includes('assistant:')) {
    return 'message';
  }

  // Default to text
  return 'text';
}
```

### Step 4: Format Episode

```javascript
function formatEpisode(memoryType, content, sourceType) {
  const timestamp = new Date().toISOString();

  switch (memoryType) {
    case 'person':
      if (sourceType === 'json') {
        // Extract structured data
        return JSON.stringify(extractPersonData(content));
      }
      return content;

    case 'conversation':
      // Format as message exchange
      return formatConversation(content);

    case 'decision':
      return `Strategic Decision (${timestamp})\n\n${content}`;

    case 'learning':
      return `Technical Learning (${timestamp})\n\n${content}`;

    default:
      return content;
  }
}
```

### Step 5: Execute Memory Addition

```javascript
async function addGraphitiMemory(memoryType, instance, content, sourceType) {
  const groupIds = {
    'graphiti-mokai': 'mokai-business',
    'graphiti-finance': 'financial-tracking',
    'graphiti-personal': 'personal-life'
  };

  const episode = formatEpisode(memoryType, content, sourceType);

  await mcp__graphiti__add_memory({
    name: `${memoryType} - ${new Date().toISOString().split('T')[0]}`,
    episode_body: episode,
    group_id: groupIds[instance],
    source: sourceType,
    source_description: `User-added ${memoryType} memory`
  });

  return {
    success: true,
    instance,
    memoryType,
    sourceType
  };
}
```

## Complete Workflow

```javascript
async function executeGraphMemory(args) {
  // 1. Get input (from args or conversation context)
  const userInput = args || await extractFromConversation();

  // 2. Analyze context
  const memoryType = await analyzeMemoryContext(userInput, conversationHistory);

  // 3. Route to instance
  const instance = routeToGraphitiInstance(userInput);

  // 4. Determine source type
  const sourceType = determineSourceType(memoryType, userInput);

  // 5. Show preview to user
  console.log(`
📊 Memory Analysis:
- Type: ${memoryType}
- Instance: ${instance}
- Source: ${sourceType}

Preview:
${userInput.substring(0, 200)}...

Add to Graphiti? (yes/no)
  `);

  // 6. If confirmed, add memory
  const result = await addGraphitiMemory(memoryType, instance, userInput, sourceType);

  // 7. Confirm success
  console.log(`✅ Added ${memoryType} to ${instance} (${sourceType} format)`);
}
```

## Output Format

### Success
```
📊 Memory Analysis:
- Type: person
- Instance: graphiti-mokai
- Source: json

Preview:
Sarah Chen, CTO at TechCorp, interested in IRAP services...

✅ Added person to graphiti-mokai (json format)

Entity created: Sarah Chen
Relationships: TechCorp (works_at), IRAP services (interested_in)
```

### From Conversation Context
```
📊 Analyzing recent conversation...

Found 3 memorable items:
1. [Decision] Pivot MOKAI positioning → graphiti-mokai
2. [Person] Chris Paget mentioned → graphiti-personal
3. [Learning] Prisma connection pooling → graphiti-personal

Add all? (yes/no/select)
```

## Entity Extraction Examples

### Person Memory (JSON)
```json
{
  "person": {
    "name": "Chris Paget",
    "relationship": "friend, former colleague",
    "context": "SAFIA's tour manager",
    "role": "Production Management, Technical Director",
    "skills": ["Tour Management", "Event Management", "Logistics"]
  }
}
```

Graphiti will automatically create:
- Entity: "Chris Paget"
- Entity: "SAFIA"
- Relationship: Chris Paget → worked_with → SAFIA
- Relationship: Chris Paget → skills → Tour Management

### Business Decision (Text)
```
Strategic Decision - MOKAI Technology Expansion (2025-10-20)

Decided to expand MOKAI's service offering from cybersecurity to full technology consultancy.

Drivers:
- Client demand for broader services
- Leverage Indigenous procurement advantage
- Higher margin potential

Implementation:
- Update positioning and messaging
- Identify technology partnerships
- Retrain sales team
```

Graphiti extracts:
- Entity: "MOKAI"
- Entity: "technology consultancy"
- Relationship: MOKAI → expanding_to → technology consultancy
- Temporal marker: 2025-10-20

### Technical Learning (Text)
```
Discovered that Prisma's connection pooling works better with PgBouncer in transaction mode rather than session mode. This reduces connection overhead and improves performance under high load.
```

Graphiti extracts:
- Entity: "Prisma"
- Entity: "PgBouncer"
- Relationship: Prisma → works_with → PgBouncer
- Relationship: transaction mode → improves → performance

## Verification

After adding memory, verify with:

```javascript
// Search for the added entity
mcp__graphiti__search_memory_nodes({
  query: "Sarah Chen",
  max_nodes: 5
})

// Search for related facts
mcp__graphiti__search_memory_facts({
  query: "TechCorp IRAP services",
  max_facts: 10
})
```

## Integration with Existing Commands

### Complement `/extract-daily-content`
- `/extract-daily-content` → Automatic extraction from daily notes
- `/graphiti-add` → Manual addition of specific memories

### Complement `/remember` (Serena)
- `/remember` → Code/technical patterns for Serena memory
- `/graphiti-add` → People, events, decisions for Graphiti

### Use with `/graphiti-tree`
After adding memories, update visualization:
```bash
/graphiti-add [content]
/graphiti-tree
```

## Advanced Features

### Batch Addition
```javascript
// Add multiple related memories
const batch = [
  { type: 'person', content: '...' },
  { type: 'decision', content: '...' },
  { type: 'event', content: '...' }
];

for (const item of batch) {
  await addGraphitiMemory(item.type, instance, item.content, sourceType);
}
```

### Smart Deduplication
```javascript
// Before adding, check if entity exists
const existing = await mcp__graphiti__search_memory_nodes({
  query: personName,
  max_nodes: 1
});

if (existing.nodes.length > 0) {
  console.log(`⚠️ Entity "${personName}" already exists. Update instead? (yes/no)`);
}
```

### Relationship Suggestions
```javascript
// After adding entity, suggest connections
const relatedEntities = await findRelatedEntities(newEntityName);
console.log(`
💡 Suggested connections:
${relatedEntities.map(e => `- Connect to: ${e.name}`).join('\n')}
`);
```

## Error Handling

```javascript
try {
  await addGraphitiMemory(...);
} catch (error) {
  if (error.message.includes('Neo4j')) {
    console.error('❌ Graphiti database connection failed. Is Neo4j running?');
  } else if (error.message.includes('group_id')) {
    console.error('❌ Invalid instance selected. Use: graphiti-mokai, graphiti-finance, or graphiti-personal');
  } else {
    console.error(`❌ Failed to add memory: ${error.message}`);
  }
}
```

## Best Practices

1. **Be specific**: Include context (who, what, when, why)
2. **Use structured format for people**: Name, role, company, relationship
3. **Include timestamps for decisions/events**: Makes temporal queries work
4. **Add relationship context**: How entities connect (works_at, interested_in, manages)
5. **Verify after adding**: Use search to confirm entity was created

## Future Enhancements

- **Voice input**: Transcribe and categorize voice memos
- **Email extraction**: Parse emails for people/companies
- **Calendar integration**: Auto-add meeting participants
- **Relationship mapping**: Visualize entity connections
- **Temporal queries**: "What was I working on in Q3?"

## Troubleshooting

**Memory not appearing in search**:
- Wait 10-30 seconds for indexing
- Check correct instance: `mcp__graphiti__search_memory_nodes({ query: "...", group_ids: ["mokai-business"] })`

**Entity extraction not working**:
- Use JSON source type for structured data
- Include explicit relationship keywords (works_at, manages, interested_in)

**Wrong instance selected**:
- Override with `--instance=graphiti-mokai` flag (future enhancement)
- Keywords to force routing: "mokai", "mokhouse", "accounting", "crypto"

---

**Version**: 1.0
**Dependencies**: Graphiti MCP (`mcp__graphiti__*`)
**Related**: `/extract-daily-content`, `/graphiti-tree`, `/remember`
