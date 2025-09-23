Compress current context to essential information:

1. Save full state to memory/checkpoints/[timestamp].json
2. Extract only:
   - Current task and its requirements
   - Key decisions made
   - Essential data for continuation
   - Active errors or blockers
3. Clear conversation
4. Load only Level 0 context
5. Restore minimal working state

Output: "✅ Context compacted. Retained: [what was kept]"
