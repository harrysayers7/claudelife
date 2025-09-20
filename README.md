# Personal Assistant System

A comprehensive AI-powered personal assistant system that helps organize work across multiple projects, automates routine tasks, and improves productivity using Claude Code and AI agents.

## Directory Structure

```
claudelife/ (Personal Assistant Root)
├── CLAUDE.md              # Main system context and instructions
├── config.json            # System-wide configuration
├── README.md              # This file - system documentation
├── .taskmaster/           # Task Master AI files
│   ├── tasks/            # Task files and database
│   ├── docs/             # PRD and documentation
│   └── config.json       # Task Master configuration
├── projects/             # Project-specific workspaces
│   ├── mokai/           # MOKAI business projects
│   ├── mok-music/       # Music-related projects
│   ├── brain/           # AI system projects
│   └── mac/             # Mac-related projects
├── shared/              # Shared resources
│   ├── agents/          # AI agent definitions
│   ├── commands/        # Custom slash commands
│   └── utils/           # Utility scripts and tools
├── context/             # Global context files
├── memory/              # Learning and performance data
└── output/              # Generated outputs and reports
```

## Project Workspaces

Each project directory contains:
- `CLAUDE.md` - Project-specific context and instructions
- `tasks.json` - Project-specific task tracking
- `context/` - Additional context files
- `config.json` - Project-specific settings

## Quick Start

1. **View available tasks**: `task-master list`
2. **Get next task**: `task-master next`
3. **Switch projects**: Use custom project switching mechanism (TBD)
4. **Add tasks**: `task-master add-task --prompt="description"`

## Key Features

- **Multi-project organization** with isolated contexts
- **AI-powered task management** with Task Master integration
- **Intelligent context loading** with token awareness
- **Custom automation** through slash commands
- **Learning system** that improves over time
- **Background job processing** with Trigger.dev

## System Status

- ✅ Task Master initialized and configured
- ✅ Directory structure created
- ⏳ Project-specific configurations (in progress)
- ⏳ Agent framework development
- ⏳ Automation system setup

For detailed implementation status, run: `task-master list`