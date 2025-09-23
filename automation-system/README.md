# Automation System

A production-ready automation system that integrates Claude Code personal assistant capabilities with server infrastructure.

## Features

- **Tasks-AI Integration**: Direct connection to Notion Tasks-AI database
- **Workflow Engine**: Advanced state machine workflows with error recovery
- **Multi-Service Integration**: Notion, Supabase, and n8n automation
- **Predictive Automation**: Pattern-based task anticipation
- **Real-time Monitoring**: System health and performance tracking

## Architecture

```
automation-system/
├── automation.py          # Main entry point
├── config.yaml           # Configuration
├── workflows/            # Workflow engine
│   ├── engine.py        # Core orchestration
│   ├── state_machine.py # State machine implementation
│   └── scheduler.py     # Workflow scheduling
├── integrations/        # External service clients
│   ├── notion_client.py # Tasks-AI integration
│   ├── supabase_client.py # Database operations
│   └── n8n_client.py    # Automation triggers
└── utils/              # Common utilities
    ├── logger.py       # Structured logging
    ├── config_manager.py # Configuration handling
    └── cache.py        # Intelligent caching
```

## Quick Start

### 1. Environment Setup

```bash
# Clone and setup
git clone <repository>
cd automation-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys
```

### 2. Configuration

Update `config.yaml` with your specific settings:

- Notion API key and database IDs
- Supabase connection details
- n8n webhook URLs
- Workflow schedules

### 3. Run the System

```bash
# Development
python automation.py

# Production (with systemd)
sudo systemctl start automation-system
```

## Integration Points

### Notion Tasks-AI

- **Database ID**: `bb278d48-954a-4c93-85b7-88bd4979f467`
- **Operations**: Create, read, update tasks
- **Auto-categorization**: MOKAI, Mok Music, Brain, Mac areas
- **Priority detection**: P0-Critical through P4-Someday

### Supabase Database

- **URL**: `https://supa.sayers.app`
- **Operations**: Memory graph, cache, analytics
- **Real-time**: Live updates and sync

### n8n Workflows

- **Base URL**: `http://134.199.159.190:5678`
- **Available workflows**:
  - `daily-summary`: Morning/evening reports
  - `process-inbox`: Email automation
  - `backup-workspace`: Data backup
  - `send-update`: Stakeholder communications

## Workflows

### Daily Automation

**Morning Routine (9:00 AM)**:
1. Query Tasks-AI for today's priorities
2. Fetch calendar and check conflicts
3. Generate daily brief
4. Send morning summary

**Evening Review (5:00 PM)**:
1. Update completed tasks
2. Generate daily summary
3. Plan tomorrow's priorities
4. Archive completed work

### Task Management

**Auto-Task Creation**:
- Voice command detection ("I need to...")
- Document action item extraction
- Email follow-up identification
- Meeting note processing

**Smart Categorization**:
- **MOKAI**: cybersecurity, compliance, government
- **Mok Music**: production, SAFIA, composing
- **Brain**: AI, automation, development
- **Mac**: system maintenance, scripts

## API Endpoints

```bash
# Health check
GET /health

# Create task
POST /tasks
{
  "title": "Review security audit",
  "area": ["MOKAI"],
  "priority": "P1 - High",
  "category": "Review"
}

# Get tasks
GET /tasks?status=Not%20Started&area=MOKAI

# Execute workflow
POST /workflows/daily-summary
{
  "context": {"user_id": "harry"}
}
```

## Monitoring

### Logs

```bash
# View live logs
tail -f logs/automation.log

# System status
curl http://localhost:8000/health
```

### Metrics

- Task completion rates by area
- Workflow execution times
- Error rates and recovery
- Automation time savings

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black .

# Lint
flake8 .

# Type checking
mypy .
```

## Deployment

### Systemd Service

```bash
# Copy service file
sudo cp automation-system.service /etc/systemd/system/

# Enable and start
sudo systemctl enable automation-system
sudo systemctl start automation-system

# View status
sudo systemctl status automation-system
```

### Environment Variables

Required environment variables:
- `NOTION_API_KEY`: Notion integration token
- `SUPABASE_URL`: Database URL
- `SUPABASE_SERVICE_KEY`: Database service key
- `ANTHROPIC_API_KEY`: Claude API access

## Troubleshooting

### Common Issues

1. **Notion Connection Failed**
   - Verify API key in `.env`
   - Check database sharing permissions

2. **Workflow Stuck**
   - Check logs for error details
   - Restart system: `sudo systemctl restart automation-system`

3. **n8n Integration Issues**
   - Verify server accessibility: `curl http://134.199.159.190:5678/health`
   - Check webhook URLs in config

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python automation.py
```

## License

Private - MOKAI Pty Ltd / Harry Sayers
