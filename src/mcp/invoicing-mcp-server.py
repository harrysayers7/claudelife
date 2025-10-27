#!/usr/bin/env python3
"""
FastMCP server for invoice PDF generation and management.

Exposes tools for:
- Generating invoice PDFs
- Querying invoice data
- Listing invoices
- Managing PDF storage
"""

import sys
import os

# Add project root to path so we can import src package
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from fastmcp import FastMCP
from fastmcp import Context
from typing import Optional
import json
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP(name="Invoicing Service")


# Tool 1: Generate Invoice PDF
@mcp.tool
async def generate_invoice_pdf(invoice_id: str, ctx: Optional[Context] = None) -> dict:
    """
    Generate a PDF for a specific invoice.

    Args:
        invoice_id: UUID of the invoice to generate PDF for

    Returns:
        Dictionary with PDF generation result including URL and file size
    """
    if ctx:
        await ctx.info(f"Generating PDF for invoice: {invoice_id}")

    try:
        from src.invoicing.invoicing_service import InvoicingService

        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            return {
                "success": False,
                "error": "Missing SUPABASE_URL or SUPABASE_KEY environment variables"
            }

        service = InvoicingService(supabase_url, supabase_key)
        await service.initialize()

        # Generate and store PDF
        success = await service.generateAndStorePdf(invoice_id)

        if success:
            # Fetch the metadata
            result = await service.fetchInvoiceData(invoice_id)
            return {
                "success": True,
                "message": f"PDF generated successfully for invoice {result['invoice_number']}",
                "invoice_number": result['invoice_number'],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": "Failed to generate PDF"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        try:
            await service.cleanup()
        except:
            pass


# Tool 2: Get Invoice Data
@mcp.tool
async def get_invoice(invoice_id: str, ctx: Optional[Context] = None) -> dict:
    """
    Retrieve invoice data including client info and line items.

    Args:
        invoice_id: UUID of the invoice

    Returns:
        Complete invoice data with line items as JSON
    """
    if ctx:
        await ctx.info(f"Fetching invoice data: {invoice_id}")

    try:
        from src.invoicing.invoicing_service import InvoicingService

        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            return {
                "success": False,
                "error": "Missing SUPABASE_URL or SUPABASE_KEY environment variables"
            }

        service = InvoicingService(supabase_url, supabase_key)
        await service.initialize()

        invoice_data = await service.fetchInvoiceData(invoice_id)

        if invoice_data:
            return {
                "success": True,
                "data": invoice_data
            }
        else:
            return {
                "success": False,
                "error": f"Invoice {invoice_id} not found"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        try:
            await service.cleanup()
        except:
            pass


# Tool 3: List Entity Invoices
@mcp.tool
async def list_entity_invoices(entity_id: str, limit: int = 10, ctx: Optional[Context] = None) -> dict:
    """
    List invoices for a specific entity.

    Args:
        entity_id: UUID of the entity (MOK HOUSE, MOKAI, etc)
        limit: Maximum number of invoices to return (default: 10)

    Returns:
        List of invoices with basic info (number, date, total, status)
    """
    if ctx:
        await ctx.info(f"Listing invoices for entity: {entity_id}")

    try:
        from src.invoicing.invoicing_service import InvoicingService

        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            return {
                "success": False,
                "error": "Missing SUPABASE_URL or SUPABASE_KEY environment variables"
            }

        service = InvoicingService(supabase_url, supabase_key)
        await service.initialize()

        invoices = await service.fetchEntityInvoices(entity_id, limit=limit)

        return {
            "success": True,
            "entity_id": entity_id,
            "count": len(invoices),
            "invoices": [
                {
                    "id": inv['id'],
                    "invoice_number": inv['invoice_number'],
                    "date": inv['invoice_date'],
                    "client": inv.get('client_name', 'Unknown'),
                    "total": float(inv.get('total_amount', 0)),
                    "status": inv.get('status', 'pending'),
                    "po_number": inv.get('purchase_order_number')
                }
                for inv in invoices
            ]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        try:
            await service.cleanup()
        except:
            pass


# Tool 4: Get PDF Status
@mcp.tool
async def get_pdf_status(invoice_id: str, ctx: Optional[Context] = None) -> dict:
    """
    Check if a PDF has been generated for an invoice.

    Args:
        invoice_id: UUID of the invoice

    Returns:
        PDF status including URL if generated
    """
    if ctx:
        await ctx.info(f"Checking PDF status for invoice: {invoice_id}")

    try:
        from src.invoicing.invoicing_service import InvoicingService

        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            return {
                "success": False,
                "error": "Missing SUPABASE_URL or SUPABASE_KEY environment variables"
            }

        service = InvoicingService(supabase_url, supabase_key)
        await service.initialize()

        pdf_status = await service.getPdfStatus(invoice_id)

        if pdf_status:
            return {
                "success": True,
                "generated": True,
                "pdf_url": pdf_status.get('pdf_url'),
                "file_size_bytes": pdf_status.get('pdf_size_bytes'),
                "generated_at": pdf_status.get('generated_at')
            }
        else:
            return {
                "success": True,
                "generated": False,
                "message": "PDF not yet generated for this invoice"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        try:
            await service.cleanup()
        except:
            pass


# Tool 5: Batch Generate PDFs
@mcp.tool
async def batch_generate_pdfs(invoice_ids: list[str], ctx: Optional[Context] = None) -> dict:
    """
    Generate PDFs for multiple invoices.

    Args:
        invoice_ids: List of invoice UUIDs

    Returns:
        Status of batch generation including successes and failures
    """
    if ctx:
        await ctx.info(f"Batch generating PDFs for {len(invoice_ids)} invoices")

    try:
        from src.invoicing.invoicing_service import InvoicingService

        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')

        if not supabase_url or not supabase_key:
            return {
                "success": False,
                "error": "Missing SUPABASE_URL or SUPABASE_KEY environment variables"
            }

        service = InvoicingService(supabase_url, supabase_key)
        await service.initialize()

        results = await service.generatePdfBatch(invoice_ids)

        successful = sum(1 for r in results if r.get('success'))
        failed = len(results) - successful

        return {
            "success": True,
            "total": len(results),
            "successful": successful,
            "failed": failed,
            "results": results
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        try:
            await service.cleanup()
        except:
            pass


# Resource: Invoice Template Configuration
@mcp.resource("resource://invoicing/config")
async def get_invoicing_config() -> dict:
    """
    Get invoicing system configuration and templates.

    Returns:
        Configuration including entity prefixes, GST rate, storage paths
    """
    return {
        "entities": {
            "MOK_HOUSE": {
                "name": "MOK HOUSE PTY LTD",
                "prefix": "MH",
                "abn": "14 657 147 652"
            },
            "MOKAI": {
                "name": "MOKAI PTY LTD",
                "prefix": "MK",
                "abn": "89 184 087 850"
            }
        },
        "invoice_format": {
            "pattern": "PREFIX-NNN",
            "example": "MH-001",
            "description": "Simple sequential numbering without year component"
        },
        "tax_rate": 0.10,
        "currency": "AUD",
        "storage": {
            "bucket": "invoice-pdfs",
            "path_pattern": "entity-id/year/invoice-number.pdf"
        }
    }


# Resource: Available Invoice Templates
@mcp.resource("resource://invoicing/templates")
async def get_invoice_templates() -> dict:
    """
    Get available invoice template information.

    Returns:
        List of template types and their features
    """
    return {
        "templates": [
            {
                "name": "Australian Standard Invoice",
                "file": "templates/invoice.html",
                "features": [
                    "A4 page format",
                    "ABN support",
                    "GST calculation",
                    "Line items with tax",
                    "Payment terms",
                    "Bank details section"
                ],
                "compliance": "Australian tax law compliant"
            }
        ]
    }


# Resource: Invoicing Documentation
@mcp.resource("resource://invoicing/docs")
async def get_invoicing_docs() -> dict:
    """
    Get documentation for the invoicing MCP server.

    Returns:
        Usage guide and examples
    """
    return {
        "title": "Invoicing MCP Server Documentation",
        "version": "1.0.0",
        "tools": [
            {
                "name": "generate_invoice_pdf",
                "description": "Generate PDF for a specific invoice",
                "example": "generate_invoice_pdf('invoice-uuid-here')"
            },
            {
                "name": "get_invoice",
                "description": "Retrieve complete invoice data",
                "example": "get_invoice('invoice-uuid-here')"
            },
            {
                "name": "list_entity_invoices",
                "description": "List all invoices for an entity",
                "example": "list_entity_invoices('entity-uuid-here', limit=20)"
            },
            {
                "name": "get_pdf_status",
                "description": "Check if PDF has been generated",
                "example": "get_pdf_status('invoice-uuid-here')"
            },
            {
                "name": "batch_generate_pdfs",
                "description": "Generate PDFs for multiple invoices",
                "example": "batch_generate_pdfs(['uuid1', 'uuid2', 'uuid3'])"
            }
        ]
    }


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
