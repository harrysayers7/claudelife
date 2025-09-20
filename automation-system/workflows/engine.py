"""
Workflow Engine - Core orchestration system
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .state_machine import StateMachine
from .scheduler import WorkflowScheduler

class WorkflowEngine:
    """Main workflow orchestration engine"""

    def __init__(self, notion=None, supabase=None, n8n=None):
        self.notion = notion
        self.supabase = supabase
        self.n8n = n8n

        self.logger = logging.getLogger(__name__)
        self.scheduler = WorkflowScheduler()
        self.active_workflows: Dict[str, StateMachine] = {}
        self.running = False

    async def start(self):
        """Start the workflow engine"""
        self.logger.info("Starting Workflow Engine")
        self.running = True

        # Start scheduler
        await self.scheduler.start()

        # Start workflow monitoring loop
        asyncio.create_task(self._monitor_workflows())

    async def stop(self):
        """Stop the workflow engine"""
        self.logger.info("Stopping Workflow Engine")
        self.running = False

        # Stop all active workflows
        for workflow_id, workflow in self.active_workflows.items():
            await workflow.stop()

        # Stop scheduler
        await self.scheduler.stop()

    async def execute_workflow(self, workflow_name: str, context: Dict[str, Any]) -> str:
        """Execute a workflow"""
        workflow_id = f"{workflow_name}_{datetime.now().isoformat()}"

        try:
            # Create state machine for workflow
            workflow = StateMachine(
                workflow_name=workflow_name,
                context=context,
                notion=self.notion,
                supabase=self.supabase,
                n8n=self.n8n
            )

            # Store active workflow
            self.active_workflows[workflow_id] = workflow

            # Execute workflow
            result = await workflow.execute()

            self.logger.info(f"Workflow {workflow_name} completed: {workflow_id}")
            return workflow_id

        except Exception as e:
            self.logger.error(f"Workflow {workflow_name} failed: {e}")
            raise
        finally:
            # Clean up
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]

    async def _monitor_workflows(self):
        """Monitor running workflows"""
        while self.running:
            try:
                # Check for stuck workflows
                current_time = datetime.now()

                for workflow_id, workflow in list(self.active_workflows.items()):
                    if workflow.is_stuck(current_time):
                        self.logger.warning(f"Workflow {workflow_id} appears stuck, attempting recovery")
                        await workflow.recover()

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                self.logger.error(f"Error in workflow monitoring: {e}")
                await asyncio.sleep(60)