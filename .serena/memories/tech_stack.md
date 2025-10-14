# Tech Stack

## Runtime Environment
- **Platform**: macOS (Darwin)
- **Primary Language**: JavaScript/Node.js
- **Secondary Language**: Python (for specific automation scripts and MCP servers)

## Key Dependencies
- `@supabase/supabase-js`: Database operations
- `dotenv`: Environment variable management
- `googleapis`: Google services integration
- `nodemailer`: Email automation
- `playwright`: Browser automation
- `uuid`: Unique identifier generation

## Python Dependencies (MCP Servers)
- `gpt-researcher>=0.14.0`: Autonomous web research agent
- `fastmcp>=2.8.0`: MCP protocol framework
- `fastapi>=0.103.1`: Web framework for MCP servers
- `python-dotenv`: Python environment management

## Infrastructure
- **Database**: Supabase (project: gshsshaodoyttdxippwx "SAYERS DATA")
- **Automation Platform**: n8n (self-hosted at 134.199.159.190)
- **Version Control**: Git/GitHub
- **Task Management**: Task Master AI
- **MCP Servers**: Multiple specialized servers for different integrations

## MCP Servers
- **serena**: Code analysis and semantic search
- **task-master-ai**: Task management and planning
- **notion**: Notion workspace integration
- **context7**: Library documentation lookup
- **graphiti**: Knowledge graph and memory management
- **n8n-mcp**: n8n workflow automation integration
- **gpt-researcher**: Deep web research and information gathering
- **supabase**: Database operations and queries
- **github**: GitHub repository management
- **memory**: Persistent memory storage
- **stripe**: Payment processing integration
- **gmail**: Email integration
- **claudelife-obsidian**: Obsidian vault operations

## External APIs & Services
- **OpenAI API**: GPT models for analysis (used by GPT Researcher)
- **Tavily API**: Web search provider (used by GPT Researcher)
- **Perplexity API**: Alternative research provider (Task Master)
- **UpBank API**: Financial transaction sync
- **Google APIs**: Various Google service integrations
- **GitHub API**: Repository and PR management
- **Linear API**: Issue tracking

## Development Tools
- Node.js package management (npm)
- Pre-commit hooks for security scanning
- Security tools: gitleaks, trufflehog
- Python virtual environments for MCP servers
- Docker (for some deployments)
