# Team Collaboration Configuration

## Workspace Structure

### Shared Resources
team/
├── shared-context/      # Team knowledge base
├── shared-memory/       # Shared entity graph
├── shared-commands/     # Team commands
├── shared-automations/  # Team workflows
└── shared-templates/    # Team templates

### Private Resources  
private/
├── personal-notes/      # Never shared
├── personal-memory/     # Personal graph
├── personal-context/    # Personal preferences
└── credentials/         # Private keys

## Permission Model

### Roles
- **Owner**: Full access to everything
- **Admin**: Manage team resources, can't access private
- **Member**: Read/write shared, read-only admin
- **Viewer**: Read-only access to shared

### Resource Permissions
{
  "shared-context": ["owner", "admin", "member:write", "viewer:read"],
  "shared-memory": ["owner", "admin", "member:write", "viewer:read"],
  "personal-*": ["owner-only"],
  "credentials": ["owner-only"],
  "team-settings": ["owner", "admin"]
}

## Collaboration Features

### Handoffs
@handoff [agent] [to-user]
- Package current context
- Include relevant history
- Transfer ownership
- Notify recipient

### Co-working
@collaborate [with-user] [on-task]
- Share context
- Split subtasks
- Merge results
- Coordinate actions

### Reviews
@request-review [from-user]
- Package work
- Include context
- Wait for feedback
- Apply suggestions