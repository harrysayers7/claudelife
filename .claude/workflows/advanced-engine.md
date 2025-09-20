# Advanced Workflow Engine v2

## Enhanced Features

### Conditional Branching
conditions:
  - if: "context.priority == 'urgent'"
    goto: "fast_track"
  - elif: "context.budget > 10000"
    goto: "detailed_analysis"
  - else:
    goto: "standard_process"

### Parallel Execution
parallel_tasks:
  - branch: "research"
    agent: "@web-researcher"
    timeout: 300
  - branch: "analysis"
    agent: "@data-miner"
    timeout: 300

wait_for: "all|any|specific"
merge_strategy: "combine|override|manual"

### Sub-Workflows
sub_workflows:
  - trigger: "approval_needed"
    workflow: "approval_process"
    pass_context: true
    wait_for_completion: true
    on_complete: "continue"
    on_reject: "abort"

### Dynamic State Generation
dynamic_states:
  - template: "review_stage_{n}"
    count: "context.review_stages"
    generator: "create_review_state"

### Error Recovery
error_handling:
  retry_policy:
    max_attempts: 3
    backoff: "exponential"
    retry_on: ["timeout", "api_error"]

  fallback_chain:
    - try: "primary_method"
    - catch: "backup_method"
    - finally: "cleanup"

### State Persistence
checkpoints:
  - before: "expensive_operation"
  - after: "critical_decision"
  - every: "5_minutes"

recovery:
  - on_restart: "from_last_checkpoint"
  - cleanup: "temp_files"
  - notify: "user"