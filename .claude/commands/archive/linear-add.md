Create a Linear issue from the conversation context: $ARGUMENTS

Steps:
1. Extract the main topic/problem from recent conversation
2. Format as a structured Linear issue with:
   - Clear title
   - Problem description
   - Proposed solution (if discussed)
   - Implementation steps (if applicable)
   - Acceptance criteria
3. Create issue using mcp__linear-server__create_issue:
   - team: "Sayers"
   - priority: 3 (Medium) unless specified
4. Return the Linear URL for reference

Parse $ARGUMENTS for:
- Additional labels (e.g., "optimization", "bug", "enhancement")
- Priority override (e.g., "high priority" → priority: 2)
- Team override (default: "Sayers")
