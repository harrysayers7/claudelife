"""
Graphiti Configuration Module

Handles configuration, initialization, and connection management for Graphiti
knowledge graph integration with the personal assistant system.
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from graphiti_core import Graphiti
from neo4j import GraphDatabase
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphitiConfig:
    """Configuration manager for Graphiti integration."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        self.neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD', 'neo4j')

        # LLM Provider configurations
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

        # Graphiti settings
        self.default_provider = 'anthropic' if self.anthropic_api_key else 'openai'

        # Validate configuration
        self._validate_config()

    def _validate_config(self):
        """Validate that required configuration is present."""
        if not self.neo4j_uri or not self.neo4j_user or not self.neo4j_password:
            raise ValueError("Neo4j connection parameters are required")

        if not self.anthropic_api_key and not self.openai_api_key:
            raise ValueError("At least one LLM provider API key is required")

        logger.info(f"Configuration validated - Neo4j: {self.neo4j_uri}, Provider: {self.default_provider}")

    def get_neo4j_config(self) -> Dict[str, str]:
        """Get Neo4j connection configuration."""
        return {
            'uri': self.neo4j_uri,
            'user': self.neo4j_user,
            'password': self.neo4j_password
        }

    def get_llm_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """Get LLM provider configuration."""
        provider = provider or self.default_provider

        if provider == 'anthropic' and self.anthropic_api_key:
            return {
                'provider': 'anthropic',
                'api_key': self.anthropic_api_key,
                'model': 'claude-3-sonnet-20240229'
            }
        elif provider == 'openai' and self.openai_api_key:
            return {
                'provider': 'openai',
                'api_key': self.openai_api_key,
                'model': 'gpt-4'
            }
        else:
            raise ValueError(f"Provider '{provider}' not available or API key not configured")


class GraphitiManager:
    """Main manager for Graphiti operations."""

    def __init__(self, config: Optional[GraphitiConfig] = None):
        """Initialize Graphiti manager with configuration."""
        self.config = config or GraphitiConfig()
        self.graphiti_instance: Optional[Graphiti] = None
        self.neo4j_driver = None

    async def initialize(self, provider: Optional[str] = None) -> Graphiti:
        """Initialize Graphiti with specified provider."""
        try:
            # Test Neo4j connection first
            await self._test_neo4j_connection()

            # Get LLM configuration
            llm_config = self.config.get_llm_config(provider)
            neo4j_config = self.config.get_neo4j_config()

            logger.info(f"Initializing Graphiti with {llm_config['provider']} provider...")

            # Initialize Graphiti instance
            self.graphiti_instance = Graphiti(
                uri=neo4j_config['uri'],
                user=neo4j_config['user'],
                password=neo4j_config['password']
            )

            # Build indices and constraints (first time setup)
            await self.graphiti_instance.build_indices_and_constraints()

            logger.info("✅ Graphiti initialized successfully!")
            return self.graphiti_instance

        except Exception as e:
            logger.error(f"❌ Failed to initialize Graphiti: {e}")
            raise

    async def _test_neo4j_connection(self):
        """Test Neo4j database connectivity."""
        neo4j_config = self.config.get_neo4j_config()

        try:
            # Create a temporary driver to test connection
            driver = GraphDatabase.driver(
                neo4j_config['uri'],
                auth=(neo4j_config['user'], neo4j_config['password'])
            )

            # Test with a simple query (synchronous)
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()

            driver.close()
            logger.info("✅ Neo4j connection test successful")

        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            raise ConnectionError(f"Cannot connect to Neo4j: {e}")

    async def get_instance(self) -> Graphiti:
        """Get the Graphiti instance, initializing if necessary."""
        if not self.graphiti_instance:
            await self.initialize()
        return self.graphiti_instance

    async def close(self):
        """Clean up connections and resources."""
        if self.graphiti_instance:
            await self.graphiti_instance.close()
            self.graphiti_instance = None

        if self.neo4j_driver:
            self.neo4j_driver.close()
            self.neo4j_driver = None

        logger.info("Graphiti manager closed")


# Global manager instance
_manager: Optional[GraphitiManager] = None


async def get_graphiti(provider: Optional[str] = None) -> Graphiti:
    """Get a configured Graphiti instance (singleton pattern)."""
    global _manager

    if not _manager:
        _manager = GraphitiManager()

    return await _manager.get_instance()


async def close_graphiti():
    """Close the global Graphiti manager."""
    global _manager

    if _manager:
        await _manager.close()
        _manager = None


# Example usage and testing functions
async def test_initialization():
    """Test Graphiti initialization with available providers."""
    config = GraphitiConfig()
    manager = GraphitiManager(config)

    # Test with default provider
    try:
        graphiti = await manager.initialize()
        logger.info("✅ Default provider initialization successful")
        await manager.close()
    except Exception as e:
        logger.error(f"❌ Default provider initialization failed: {e}")

    # Test with specific providers if available
    for provider in ['anthropic', 'openai']:
        try:
            manager = GraphitiManager(config)
            graphiti = await manager.initialize(provider)
            logger.info(f"✅ {provider} provider initialization successful")
            await manager.close()
        except Exception as e:
            logger.info(f"ℹ️  {provider} provider not available: {e}")


if __name__ == "__main__":
    # Run test if script is executed directly
    asyncio.run(test_initialization())
