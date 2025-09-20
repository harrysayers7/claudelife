# Workflow Engine

Parse and execute state machine workflows defined in YAML.

## Workflow Structure
- States with entry/exit actions
- Transitions with conditions
- Error handling
- State persistence

## Execution
1. Load workflow definition
2. Retrieve current state from memory/workflows/state.json
3. Execute current state actions
4. Evaluate transitions
5. Move to next state
6. Persist new state

## State Format
{
  "workflowId": "[name]",
  "currentState": "[state]",
  "history": [],
  "context": {},
  "startTime": "[timestamp]",
  "lastUpdate": "[timestamp]"
}