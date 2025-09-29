---
relation: "[[AI-Research]]"
tags:
description:
date:
when:
---
---
<font color="#595959">Created: {{date}} {{time}}</font>

Tags: [[context/ai-brain/system-prompts/claude-code]]


Perfect! Since you already have an Ubuntu server, here's how to set up Claude Code:

## Connect via Termius
Make sure you can SSH into your Ubuntu server through Termius with your credentials.

## Install Claude Code on Your Ubuntu Server

```bash
# First, update your system
sudo apt update

# Install Node.js if you don't have it
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Claude Code globally
npm install -g @anthropic-ai/claude-code
```

## Set Up Authentication

```bash
# Add your Anthropic API key to your environment
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Verify it's set
echo $ANTHROPIC_API_KEY
```

## Test Installation

```bash
# Check if Claude Code is installed
claude-code --version

# Navigate to a project directory
cd /path/to/your/code

# Start using Claude Code
claude-code "help me understand this codebase"
```

## Clone Your GitHub Repos

```bash
# Set up git if needed
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Clone your repositories
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

# Now you can use Claude Code on your project
claude-code "review this code and suggest improvements"
```

You'll get your Anthropic API key from your account dashboard. Once this is set up, you can code on your Ubuntu server from anywhere using Termius + Claude Code!

Need help with any of these steps?

##### References
