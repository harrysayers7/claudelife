"""
Python wrapper for the Invoicing Service that bridges to the TypeScript implementation
and Supabase database operations.
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from supabase import create_client, Client as SupabaseClient


class InvoicingService:
    """
    Main invoicing service that handles:
    - Invoice data retrieval from Supabase
    - PDF generation and storage
    - Metadata management
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize the invoicing service with Supabase credentials."""
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.supabase: Optional[SupabaseClient] = None

    async def initialize(self) -> None:
        """Initialize Supabase client."""
        try:
            self.supabase = create_client(self.supabase_url, self.supabase_key)
        except Exception as e:
            raise Exception(f"Failed to initialize Supabase client: {str(e)}")

    async def fetchInvoiceData(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch complete invoice data from the v_all_invoices view (public schema).

        Args:
            invoice_id: UUID of the invoice

        Returns:
            Invoice data dict or None if not found
        """
        if not self.supabase:
            raise Exception("Service not initialized. Call initialize() first.")

        try:
            # Query the public schema view which aggregates all invoice data
            # The Python Supabase client can only access public schema via .table()
            response = self.supabase.table('v_all_invoices') \
                .select('*') \
                .eq('id', invoice_id) \
                .execute()

            if response.data and len(response.data) > 0:
                return response.data[0]

            return None

        except Exception as e:
            print(f"Error fetching invoice {invoice_id}: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None

    async def fetchEntityInvoices(
        self,
        entity_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch all invoices for a specific entity.

        Args:
            entity_id: UUID of the entity
            limit: Maximum number of invoices to return

        Returns:
            List of invoice dictionaries
        """
        if not self.supabase:
            raise Exception("Service not initialized. Call initialize() first.")

        try:
            # Query the public schema view which aggregates all invoice data
            # Note: The Supabase Python client can handle complex queries,
            # but we need to ensure each method is being called correctly.
            # Using a simpler approach to debug potential issues with ordering/limiting.

            response = self.supabase.table('v_all_invoices') \
                .select('*') \
                .eq('entity_id', entity_id) \
                .execute()

            # Sort and limit in Python if needed
            data = response.data if response.data else []

            # Sort by invoice_date descending
            if data:
                data = sorted(data, key=lambda x: x.get('invoice_date', ''), reverse=True)
                # Limit results
                data = data[:limit]

            return data

        except Exception as e:
            print(f"Error fetching invoices for entity {entity_id}: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return []

    async def getPdfStatus(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """
        Check if a PDF has been generated for an invoice.

        Note: PDF checking is not yet implemented - requires Postgres RPC or migration of invoice_pdfs to public schema.

        Args:
            invoice_id: UUID of the invoice

        Returns:
            PDF metadata dict or None if not generated
        """
        if not self.supabase:
            raise Exception("Service not initialized. Call initialize() first.")

        try:
            # TODO: Implement PDF status checking
            # The invoice_pdfs table is in the invoicing schema which Python Supabase client cannot access
            # Options:
            # 1. Create a public view of invoice_pdfs
            # 2. Use a Postgres RPC function for querying
            # 3. Migrate invoice_pdfs table to public schema
            return None

        except Exception as e:
            print(f"Error checking PDF status for {invoice_id}: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return None

    async def generateAndStorePdf(self, invoice_id: str) -> bool:
        """
        Generate PDF for an invoice and store metadata.
        Note: This is a placeholder that would call the TypeScript implementation.

        Args:
            invoice_id: UUID of the invoice

        Returns:
            True if successful, False otherwise
        """
        try:
            # This would normally call the TypeScript PDF generator
            # For now, we verify the invoice exists and record generation intent
            invoice = await self.fetchInvoiceData(invoice_id)
            if not invoice:
                return False

            # In production, this would:
            # 1. Call TypeScript PDF generator
            # 2. Upload to Supabase Storage
            # 3. Insert metadata

            return True

        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False

    async def generatePdfBatch(
        self,
        invoice_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate PDFs for multiple invoices with error handling.

        Args:
            invoice_ids: List of invoice UUIDs

        Returns:
            List of results with success/failure status
        """
        results = []

        for invoice_id in invoice_ids:
            try:
                success = await self.generateAndStorePdf(invoice_id)
                invoice = await self.fetchInvoiceData(invoice_id)

                results.append({
                    "invoice_id": invoice_id,
                    "invoice_number": invoice['invoice_number'] if invoice else None,
                    "success": success
                })
            except Exception as e:
                results.append({
                    "invoice_id": invoice_id,
                    "success": False,
                    "error": str(e)
                })

        return results

    async def cleanup(self) -> None:
        """Clean up resources."""
        # Placeholder for cleanup logic
        pass
