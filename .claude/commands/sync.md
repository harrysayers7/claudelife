# Sync System

Synchronize local and cloud resources intelligently.

## Sync Operations

### Pull from Cloud
/sync pull [resource]
- Notion databases → Local cache
- Google Drive → Local index
- GitHub repos → Local mirror
- Team memory → Local graph

### Push to Cloud
/sync push [resource]
- Local notes → Notion
- Memory graph → Cloud backup
- Performance metrics → Analytics
- Learned patterns → Team knowledge

### Bidirectional Sync
/sync all
1. Detect conflicts
2. Resolve by timestamp (newest wins)
3. Or prompt user for resolution
4. Update both sides
5. Log sync history

## Conflict Resolution

Handle conflicts intelligently:
{
  "strategy": "newest-wins|local-wins|cloud-wins|manual",
  "conflicts": [
    {
      "resource": "path/to/file",
      "local_updated": "timestamp",
      "cloud_updated": "timestamp",
      "resolution": "chosen_version",
      "backup": "path/to/backup"
    }
  ]
}

## Sync Schedule

- **Continuous**: Critical data (tasks, calendar)
- **5 minutes**: Active project data
- **Hourly**: Memory graph, performance metrics
- **Daily**: Full backup, archived data
- **Weekly**: Clean up orphaned data

Store status in memory/sync-status.json