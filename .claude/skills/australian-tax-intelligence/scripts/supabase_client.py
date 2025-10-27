"""
Supabase client wrapper with schema migration support.

Automatically routes queries to correct schema while maintaining
backward compatibility with public schema queries.

Usage:
    from supabase_client import get_schema_aware_client

    client = get_schema_aware_client()

    # Auto-routes to correct schema based on entity
    invoices = client.table('invoices', entity_name='MOK HOUSE PTY LTD').select('*').execute()

    # Or use raw client for direct queries
    raw_client = client.raw()
    result = raw_client.schema('mokhouse').table('invoices').select('*').execute()

Environment Variables:
    SUPABASE_USE_NEW_SCHEMAS: Set to 'true' to enable new schema routing (default: 'false')
"""

import os
import sys
from typing import Optional, Dict, Any

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Error: supabase package not installed")
    print("\nInstall with:")
    print("  pip3 install supabase")
    sys.exit(1)


# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://gshsshaodoyttdxippwx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Migration feature flag - flip to True when ready to use new schemas
USE_NEW_SCHEMAS = os.getenv("SUPABASE_USE_NEW_SCHEMAS", "false").lower() == "true"

# Schema mapping for entity-aware routing
ENTITY_SCHEMA_MAP = {
    "MOK HOUSE PTY LTD": "mokhouse",
    "MOKAI PTY LTD": "mokai",
    "Harrison Robert Sayers": "personal",
    "HS Family Trust": "personal",
    "SAFIA Unit Trust": "personal",
}

# Table to schema mapping (for tables not tied to specific entities)
TABLE_SCHEMA_MAP = {
    # Finance schema (shared/consolidated)
    "entities": "finance",
    "consolidated_transactions": "finance",
    "tax_calculations": "finance",

    # Personal schema
    "personal_transactions": "personal",
    "upbank_transactions": "personal",

    # Add more as you migrate tables
}


class SchemaAwareSupabase:
    """
    Wrapper around Supabase client that automatically routes queries
    to correct schema based on entity or table name, with fallback to public schema.

    This enables zero-downtime migration from public schema to multi-schema architecture.
    """

    def __init__(self, client: Client, use_new_schemas: bool = USE_NEW_SCHEMAS):
        self._client = client
        self._use_new_schemas = use_new_schemas
        self._fallback_count = 0

    def raw(self) -> Client:
        """Get raw Supabase client for direct schema access."""
        return self._client

    def table(self, table_name: str, entity_name: Optional[str] = None):
        """
        Get table reference, auto-routing to correct schema.

        Args:
            table_name: Name of table (e.g., 'invoices', 'transactions')
            entity_name: Optional entity name to determine schema

        Returns:
            Supabase table reference

        Examples:
            # Entity-aware routing
            client.table('invoices', entity_name='MOK HOUSE PTY LTD')
            # -> mokhouse.invoices (if USE_NEW_SCHEMAS=true)
            # -> public.invoices (if USE_NEW_SCHEMAS=false)

            # Table-based routing
            client.table('entities')
            # -> finance.entities (if USE_NEW_SCHEMAS=true)
            # -> public.entities (if USE_NEW_SCHEMAS=false)
        """
        if not self._use_new_schemas:
            # Legacy mode - always use public schema (or default schema)
            return self._client.table(table_name)

        # Determine target schema
        target_schema = None

        # 1. Try entity-based routing
        if entity_name and entity_name in ENTITY_SCHEMA_MAP:
            target_schema = ENTITY_SCHEMA_MAP[entity_name]

        # 2. Try table-based routing
        elif table_name in TABLE_SCHEMA_MAP:
            target_schema = TABLE_SCHEMA_MAP[table_name]

        # Route to schema or fall back to public
        if target_schema:
            return self._client.schema(target_schema).table(table_name)
        else:
            # No mapping found - use public schema
            return self._client.table(table_name)

    def schema(self, schema_name: str):
        """
        Direct schema access (for advanced use cases).

        Args:
            schema_name: Schema name (e.g., 'mokhouse', 'mokai', 'finance')

        Returns:
            Schema-scoped client
        """
        return self._client.schema(schema_name)

    def execute_with_fallback(self, query_fn, error_msg: str = "Query failed"):
        """
        Execute query with automatic fallback to public schema on schema-related errors.

        This is useful during migration when some tables may not exist in new schemas yet.

        Args:
            query_fn: Lambda function that executes the query
            error_msg: Custom error message prefix

        Returns:
            Query result

        Example:
            result = client.execute_with_fallback(
                lambda: client.table('invoices', 'MOK HOUSE').select('*').execute(),
                error_msg="Failed to fetch MOK HOUSE invoices"
            )
        """
        try:
            return query_fn()
        except Exception as e:
            error_str = str(e).lower()

            # Check if it's a schema-related error
            if any(keyword in error_str for keyword in ["schema", "does not exist", "not found"]):
                self._fallback_count += 1
                print(f"⚠️  {error_msg} - Schema error detected, falling back to public schema")
                print(f"   Error: {e}")

                # Temporarily disable new schemas and retry
                original_flag = self._use_new_schemas
                self._use_new_schemas = False

                try:
                    result = query_fn()
                    print(f"✅ Fallback successful (fallback count: {self._fallback_count})")
                    return result
                finally:
                    # Restore original flag
                    self._use_new_schemas = original_flag
            else:
                # Not a schema error - re-raise
                raise

    def get_fallback_stats(self) -> Dict[str, Any]:
        """Get statistics about fallback usage (for monitoring migration)."""
        return {
            "use_new_schemas": self._use_new_schemas,
            "fallback_count": self._fallback_count,
            "entity_mappings": len(ENTITY_SCHEMA_MAP),
            "table_mappings": len(TABLE_SCHEMA_MAP),
        }


def get_supabase_client() -> Client:
    """
    Initialize raw Supabase client (legacy function for backward compatibility).

    For new code, use get_schema_aware_client() instead.
    """
    if not SUPABASE_KEY:
        print("❌ Error: SUPABASE_KEY environment variable not set")
        print("\nSet it with:")
        print("  export SUPABASE_KEY='your-service-role-key'")
        sys.exit(1)

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_schema_aware_client(use_new_schemas: Optional[bool] = None) -> SchemaAwareSupabase:
    """
    Get schema-aware Supabase client with automatic routing.

    Args:
        use_new_schemas: Override USE_NEW_SCHEMAS environment variable

    Returns:
        SchemaAwareSupabase wrapper instance

    Example:
        # Use default (from environment variable)
        client = get_schema_aware_client()

        # Force new schemas
        client = get_schema_aware_client(use_new_schemas=True)

        # Force legacy public schema
        client = get_schema_aware_client(use_new_schemas=False)
    """
    raw_client = get_supabase_client()

    if use_new_schemas is None:
        use_new_schemas = USE_NEW_SCHEMAS

    return SchemaAwareSupabase(raw_client, use_new_schemas=use_new_schemas)


# Convenience exports
__all__ = [
    "get_supabase_client",
    "get_schema_aware_client",
    "SchemaAwareSupabase",
    "ENTITY_SCHEMA_MAP",
    "TABLE_SCHEMA_MAP",
]
