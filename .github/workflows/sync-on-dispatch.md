# Instant Sync Setup (Optional)

To sync immediately when ai-brain repo changes, add this workflow to your ai-brain repo:

## In ai-brain repo: `.github/workflows/trigger-claudelife-sync.yml`

```yaml
name: Trigger Claudelife Sync

on:
  push:
    paths:
      - 'ai/context/tasks-ai-management.md'
    branches:
      - main

jobs:
  trigger-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger claudelife workflow
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Authorization: token ${{ secrets.CLAUDELIFE_PAT }}" \
            https://api.github.com/repos/sayersauce/claudelife/dispatches \
            -d '{"event_type":"ai-brain-updated"}'
```

## Setup Steps:
1. Create a Personal Access Token (PAT) with `repo` scope
2. Add it to ai-brain repo secrets as `CLAUDELIFE_PAT`
3. Every push to tasks-ai-management.md will trigger immediate sync