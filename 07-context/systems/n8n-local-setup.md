---
location: "[[claudelife]]"
---
# n8n Local Setup

## Overview
Local n8n instance running via Docker for development and testing workflows before deploying to production server (134.199.159.190).

## Installation Details

### Docker Configuration
Location: `/Users/harrysayers/Developer/claudelife/docker-compose.yml`

```yaml
version: "3.8"
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n-local
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      - NODE_ENV=development
      - GENERIC_TIMEZONE=Australia/Sydney
      - TZ=Australia/Sydney
    volumes:
      - n8n_data:/home/node/.n8n
      - ./n8n_files:/files
volumes:
  n8n_data:
```

### Access Details
- **URL**: http://localhost:5678
- **API Endpoint**: http://localhost:5678/api/v1
- **Timezone**: Australia/Sydney
- **Mode**: Development (no PostgreSQL, simplified setup)

### API Authentication
- **API Key**: Stored in `~/.zshrc` as `N8N_API_KEY`

## MCP Server Integration

### Configuration
Location: `~/.mcp.json`

```json
"n8n": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "mcp-n8n-builder"],
  "env": {
    "N8N_HOST": "http://localhost:5678/api/v1",
    "N8N_API_KEY": "$N8N_API_KEY"
  }
}
```

### Available MCP Tools
- `mcp__n8n__n8n_create_workflow` - Create new workflows programmatically
- `mcp__n8n__n8n_trigger_webhook_workflow` - Trigger webhook-based workflows
- `mcp__n8n__list_nodes` - List available n8n nodes

## Docker Management

### Start n8n
```bash
cd /Users/harrysayers/Developer/claudelife
docker-compose up -d
```

### Stop n8n
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f n8n
```

### Check Status
```bash
docker ps | grep n8n-local
```

## Data Persistence
- **Workflow Data**: Stored in Docker volume `n8n_data`
- **File Storage**: `/Users/harrysayers/Developer/claudelife/n8n_files` (mapped to container `/files`)

## Test Workflow
A test workflow (ID: `0wrPgEr133t14fG7`) was created successfully via the n8n MCP server during initial setup, confirming API access works correctly.

## Production Deployment Path
When workflows are tested and ready, they can be deployed to the production server at:
- **Server**: 134.199.159.190 (sayers-server)
- **Location**: `/opt/n8n/`
- **Production Setup**: Uses PostgreSQL, Caddy reverse proxy, full production config

## Planned Workflows

### 1. UpBank → Supabase Sync
- Fetch transactions from UpBank API
- Sync to Supabase `gshsshaodoyttdxippwx` database
- Schedule: Hourly or on-demand via webhook
- Error handling: Checkpoint-based resumable sync

### 2. Financial ML Categorization
- Pull uncategorized transactions from Supabase
- Run ML categorization pipeline
- Auto-categorize high-confidence predictions (>0.9)
- Flag medium-confidence for review (0.7-0.9)
- Manual review for low-confidence (<0.7)

### 3. Anomaly Detection
- Monitor transaction patterns in real-time
- Detect unusual spending/income patterns
- Alert on potential issues
- Severity classification system

## Integration Points

### Supabase
- **Project ID**: `gshsshaodoyttdxippwx`
- **Database**: SAYERS DATA
- **Tables**: transactions, entities, contacts, invoices

### UpBank
- Available via `mcp__upbank__*` tools
- Real-time account and transaction access

### Stripe
- API: `https://api.stripe.com/v1/*`
- Direct API access via HTTP nodes (MCP server connection issues)
- Authentication: Bearer token via live API key

## Notes
- Local instance is for development/testing only
- No account creation required - n8n runs locally without authentication in dev mode
- Workflows can be exported as JSON and imported to production
- Volume persistence ensures workflows survive container restarts
