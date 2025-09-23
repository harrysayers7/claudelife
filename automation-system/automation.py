#!/usr/bin/env python3
"""
Automation System - Main Entry Point
Integrates Claude Code personal assistant system with server infrastructure
"""

import asyncio
import logging
import yaml
from pathlib import Path
from typing import Dict, Any

from workflows import WorkflowEngine
from integrations import NotionClient, SupabaseClient, N8NClient
from utils import Logger, ConfigManager

class AutomationSystem:
    """Main automation system orchestrator"""

    def __init__(self, config_path: str = "config.yaml"):
        self.config = ConfigManager.load_config(config_path)
        self.logger = Logger.setup_logging(self.config.get('logging', {}))

        # Initialize clients
        self.notion = NotionClient(self.config['notion'])
        self.supabase = SupabaseClient(self.config['supabase'])
        self.n8n = N8NClient(self.config['n8n'])

        # Initialize workflow engine
        self.workflow_engine = WorkflowEngine(
            notion=self.notion,
            supabase=self.supabase,
            n8n=self.n8n
        )

    async def start(self):
        """Start the automation system"""
        self.logger.info("Starting Automation System...")

        # Initialize all clients
        await self.notion.initialize()
        await self.supabase.initialize()
        await self.n8n.initialize()

        # Start workflow engine
        await self.workflow_engine.start()

        self.logger.info("Automation System started successfully")

    async def stop(self):
        """Stop the automation system"""
        self.logger.info("Stopping Automation System...")

        await self.workflow_engine.stop()
        await self.notion.close()
        await self.supabase.close()
        await self.n8n.close()

        self.logger.info("Automation System stopped")

async def main():
    """Main entry point"""
    system = AutomationSystem()

    try:
        await system.start()

        # Keep running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        await system.stop()
    except Exception as e:
        logging.error(f"System error: {e}")
        await system.stop()

if __name__ == "__main__":
    asyncio.run(main())
