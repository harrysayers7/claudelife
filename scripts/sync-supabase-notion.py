#!/usr/bin/env python3
"""
Supabase to Notion Sync Script
Syncs financial data from Supabase to Notion DATABASE MASTER
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

try:
    from supabase import create_client, Client
    from notion_client import Client as NotionClient
    from notion_client.errors import APIResponseError
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("pip install supabase notion-client")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database mappings - Notion Database IDs for each table
DATABASE_MAPPINGS = {
    'entities': '2784a17b-b7f0-8188-a62f-ffb7975db5e5',
    'contacts': '2784a17b-b7f0-8124-a67f-c51dd6c75a93',
    'transactions': '2784a17b-b7f0-81a5-94c9-d5aba1625d49',
    'invoices': '2784a17b-b7f0-8166-803d-e6cc7330d8c1',
    'accounts': '2784a17b-b7f0-8189-ad95-d6c1fd78db1c'
}

class SupabaseNotionSync:
    def __init__(self):
        """Initialize the sync client with environment variables"""

        # Get environment variables - use the working token from ~/.mcp.json
        supabase_url = "https://gshsshaodoyttdxippwx.supabase.co"
        supabase_key = os.getenv('SUPABASE_ACCESS_TOKEN')
        notion_token = os.environ.get("NOTION_TOKEN")

        if not supabase_key:
            raise ValueError("SUPABASE_ACCESS_TOKEN environment variable is required")
        if not notion_token:
            raise ValueError("NOTION_TOKEN environment variable is required")

        # Initialize clients
        self.supabase: Client = create_client(supabase_url, supabase_key)

        # Test with direct MCP first to validate
        print(f"Using Notion token: {notion_token[:20]}...")
        self.notion = NotionClient(auth=notion_token)

        # Sync statistics
        self.stats = {
            'processed': 0,
            'created': 0,
            'updated': 0,
            'errors': 0,
            'skipped': 0
        }

        logger.info("✅ Supabase and Notion clients initialized")

    def uuid_to_number(self, uuid_str: str) -> int:
        """Convert UUID string to consistent integer for Notion number fields"""
        if not uuid_str:
            return 0
        # Create a hash of the UUID string and convert to positive integer
        return abs(int(hashlib.md5(str(uuid_str).encode()).hexdigest()[:8], 16))

    def get_supabase_data(self, table: str) -> List[Dict[str, Any]]:
        """Get all data from a Supabase table"""
        try:
            response = self.supabase.table(table).select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"❌ Failed to fetch data from {table}: {str(e)}")
            return []

    def create_notion_page(self, database_id: str, properties: Dict[str, Any]) -> bool:
        """Create a new page in Notion database"""
        try:
            self.notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            return True
        except APIResponseError as e:
            logger.error(f"❌ Notion API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to create Notion page: {str(e)}")
            return False

    def format_properties_for_notion(self, table: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Format Supabase record properties for Notion"""

        if table == 'entities':
            # Match actual Notion database schema: ID (title), Entity Name (rich_text), Type (select), ABN (rich_text), Created (date)
            return {
                "ID": {"title": [{"text": {"content": str(record.get('id', 0))}}]},
                "Entity Name": {"rich_text": [{"text": {"content": record.get('business_name', 'Unknown')}}]},
                "ABN": {"rich_text": [{"text": {"content": str(record.get('abn', ''))}}]},
                "Type": {"select": {"name": "Sole Trader" if record.get('entity_type') == 'individual' else "Company"}},
                "Created": {"date": {"start": record.get('created_at', datetime.now().isoformat())[:10]}}
            }

        elif table == 'contacts':
            return {
                "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
                "Name": {"rich_text": [{"text": {"content": record.get('name', 'Unknown')}}]},
                "Email": {"email": record.get('email') or None},
                "Phone": {"phone_number": record.get('phone') or None},
                "Company": {"rich_text": [{"text": {"content": record.get('company', '')}}]},
                "Entity ID": {"number": self.uuid_to_number(record.get('entity_id', ''))}
            }

        elif table == 'transactions':
            return {
                "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
                "Description": {"rich_text": [{"text": {"content": record.get('description', 'Unknown Transaction')}}]},
                "Amount": {"number": float(record.get('amount', 0))},
                "Transaction Date": {"date": {"start": record.get('transaction_date', datetime.now().date().isoformat())[:10]}},
                "Account ID": {"number": self.uuid_to_number(record.get('account_id', ''))},
                "Entity ID": {"number": self.uuid_to_number(record.get('entity_id', ''))},
                "Reference Number": {"rich_text": [{"text": {"content": record.get('reference_number', '')}}]},
                "Notes": {"rich_text": [{"text": {"content": record.get('notes', '')}}]},
                "Vendor Name": {"rich_text": [{"text": {"content": record.get('vendor_name', '')}}]}
            }

        elif table == 'invoices':
            # Handle date fields that might be None
            due_date = record.get('due_date')
            due_date_str = due_date[:10] if due_date else datetime.now().date().isoformat()

            invoice_date = record.get('invoice_date')
            invoice_date_str = invoice_date[:10] if invoice_date else datetime.now().date().isoformat()

            return {
                "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
                "Invoice Number": {"rich_text": [{"text": {"content": record.get('invoice_number', 'Unknown')}}]},
                "Total Amount": {"number": float(record.get('total_amount', 0))},
                "Due Date": {"date": {"start": due_date_str}},
                "Invoice Date": {"date": {"start": invoice_date_str}},
                "Status": {"select": {"name": record.get('status', 'draft')}},
                "Entity ID": {"number": self.uuid_to_number(record.get('entity_id', ''))},
                "Contact ID": {"number": self.uuid_to_number(record.get('contact_id', ''))},
                "Type": {"select": {"name": record.get('type', 'receivable')}}
            }

        elif table == 'accounts':
            return {
                "ID": {"title": [{"text": {"content": str(record.get('id', ''))}}]},
                "Account Name": {"rich_text": [{"text": {"content": record.get('account_name', 'Unknown Account')}}]},
                "Account Type": {"select": {"name": record.get('account_type', 'asset')}},
                "Balance": {"number": float(record.get('current_balance', 0))},
                "Entity ID": {"number": self.uuid_to_number(record.get('entity_id', ''))},
                "Account Code": {"rich_text": [{"text": {"content": record.get('account_code', '')}}]},
                "Description": {"rich_text": [{"text": {"content": record.get('description', '')}}]},
                "Is Active": {"checkbox": bool(record.get('is_active', True))}
            }

        else:
            # Generic fallback
            return {
                "ID": {"number": record.get('id', 0)},
                "Name": {"title": [{"text": {"content": str(record.get('name', record.get('id', 'Unknown')))}}]},
                "Data": {"rich_text": [{"text": {"content": json.dumps(record, default=str, indent=2)}}]},
                "Created": {"date": {"start": record.get('created_at', datetime.now().isoformat())}}
            }

    def sync_table(self, table: str) -> Dict[str, int]:
        """Sync a single table from Supabase to Notion"""

        if table not in DATABASE_MAPPINGS:
            logger.warning(f"⚠️ No Notion database mapping found for table: {table}")
            return {'processed': 0, 'created': 0, 'errors': 1}

        database_id = DATABASE_MAPPINGS[table]
        logger.info(f"🔄 Syncing {table}...")

        # Get data from Supabase
        records = self.get_supabase_data(table)

        if not records:
            logger.info(f"📭 No records found in {table}")
            return {'processed': 0, 'created': 0, 'errors': 0}

        table_stats = {'processed': 0, 'created': 0, 'errors': 0}

        for i, record in enumerate(records, 1):
            try:
                # Format properties for Notion
                properties = self.format_properties_for_notion(table, record)

                # Create page in Notion
                success = self.create_notion_page(database_id, properties)

                if success:
                    table_stats['created'] += 1
                    logger.info(f"✅ Created {table} record {i}/{len(records)}")
                else:
                    table_stats['errors'] += 1
                    logger.error(f"❌ Failed to create {table} record {i}/{len(records)}")

                table_stats['processed'] += 1

                # Rate limiting - pause between requests
                time.sleep(0.1)

            except Exception as e:
                logger.error(f"❌ Error processing {table} record {i}: {str(e)}")
                table_stats['errors'] += 1
                table_stats['processed'] += 1

        logger.info(f"📊 {table}: {table_stats['created']} created, {table_stats['errors']} errors")
        return table_stats

    def sync_all_tables(self, tables: Optional[List[str]] = None) -> Dict[str, Any]:
        """Sync all specified tables or all available tables"""

        if tables is None:
            tables = list(DATABASE_MAPPINGS.keys())

        start_time = time.time()
        logger.info(f"🚀 Starting Supabase → Notion sync for tables: {', '.join(tables)}")

        # Reset stats
        self.stats = {'processed': 0, 'created': 0, 'updated': 0, 'errors': 0, 'skipped': 0}

        # Sync each table
        for table in tables:
            try:
                table_stats = self.sync_table(table)

                # Update overall stats
                self.stats['processed'] += table_stats['processed']
                self.stats['created'] += table_stats['created']
                self.stats['errors'] += table_stats['errors']

            except Exception as e:
                logger.error(f"❌ Failed to sync table {table}: {str(e)}")
                self.stats['errors'] += 1

        # Calculate duration
        duration = time.time() - start_time

        # Generate report
        report = {
            'duration': f"{duration:.1f}s",
            'tables_synced': len(tables),
            'stats': self.stats,
            'success': self.stats['errors'] == 0
        }

        return report

    def print_report(self, report: Dict[str, Any]):
        """Print a formatted sync report"""

        print("\n" + "="*50)
        print("📊 SUPABASE → NOTION SYNC REPORT")
        print("="*50)

        print(f"⏱️  Duration: {report['duration']}")
        print(f"📋 Tables synced: {report['tables_synced']}")
        print(f"📈 Records processed: {report['stats']['processed']}")
        print(f"✅ Records created: {report['stats']['created']}")
        print(f"❌ Errors: {report['stats']['errors']}")

        if report['success']:
            print("\n🎉 Sync completed successfully!")
        else:
            print(f"\n⚠️  Sync completed with {report['stats']['errors']} errors")

        print("="*50)

def main():
    """Main execution function"""

    try:
        # Initialize sync client
        sync_client = SupabaseNotionSync()

        # Determine tables to sync
        tables_to_sync = sys.argv[1:] if len(sys.argv) > 1 else None

        if tables_to_sync:
            # Validate table names
            invalid_tables = [t for t in tables_to_sync if t not in DATABASE_MAPPINGS]
            if invalid_tables:
                print(f"❌ Invalid table names: {', '.join(invalid_tables)}")
                print(f"Available tables: {', '.join(DATABASE_MAPPINGS.keys())}")
                sys.exit(1)

        # Execute sync
        report = sync_client.sync_all_tables(tables_to_sync)

        # Print report
        sync_client.print_report(report)

        # Exit with appropriate code
        sys.exit(0 if report['success'] else 1)

    except KeyboardInterrupt:
        print("\n🛑 Sync interrupted by user")
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Critical error: {str(e)}")
        print(f"\n💥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
