#!/usr/bin/env python3
"""
PDF Invoice Parser for Financial API
Extracts structured data from invoice PDFs using AI
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import PyPDF2
import requests
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvoiceParser:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.warning("No OpenAI API key found - AI parsing will be unavailable")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            return ""

    def parse_invoice_with_ai(self, text: str, filename: str) -> Optional[Dict[str, Any]]:
        """Use OpenAI to extract structured data from invoice text"""
        if not self.openai_api_key:
            logger.error("OpenAI API key not available for AI parsing")
            return None

        prompt = f"""
        Extract structured data from this invoice text and return ONLY valid JSON with this exact structure:

        {{
            "vendor_name": "string",
            "invoice_number": "string",
            "purchase_order": "string or null",
            "invoice_date": "YYYY-MM-DD",
            "due_date": "YYYY-MM-DD",
            "total_amount": float,
            "tax_amount": float,
            "subtotal": float,
            "currency": "AUD",
            "description": "brief description of goods/services",
            "project": "string or null",
            "client": "client/customer name if this is an outgoing invoice, or null",
            "paid_on": "YYYY-MM-DD or null if not paid",
            "billed_to": "billing address or client details",
            "line_items": [
                {{"description": "string", "quantity": float, "unit_price": float, "total": float}}
            ],
            "vendor_abn": "string or null",
            "payment_terms": "string or null"
        }}

        IMPORTANT: Look carefully for Purchase Order (PO) numbers in the text. Common formats include:
        - "Purchase Order: XXXX"
        - "PO: XXXX"
        - "P.O. XXXX"
        - "PO Number: XXXX"
        - "Purchase Order Number: XXXX"
        If found, extract the number/identifier as the purchase_order value.

        ALSO IMPORTANT: Extract the project name from the context. Look for:
        - Company names in client/billed_to fields (e.g., "DiDi", "Nintendo", "Repco")
        - Project references in descriptions or line items
        - Campaign names or project codes
        Common projects include: DiDi, Nintendo, Repco, Cabots, Apple, Google, etc.
        Set project to the most relevant business/client name if identifiable.

        Invoice text:
        {text}

        Filename: {filename}

        Return ONLY the JSON, no other text.
        """

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a precise invoice data extraction system. Return only valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 1000
                }
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()

                # Clean up any markdown formatting
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]

                return json.loads(content)
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error parsing invoice with AI: {e}")
            return None

    def parse_invoice_file(self, pdf_path: str) -> Optional[Dict[str, Any]]:
        """Parse a single PDF invoice file"""
        logger.info(f"Parsing invoice: {pdf_path}")

        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        if not text.strip():
            logger.error(f"No text extracted from {pdf_path}")
            return None

        # Parse with AI
        filename = os.path.basename(pdf_path)
        invoice_data = self.parse_invoice_with_ai(text, filename)

        if invoice_data:
            # Add metadata
            invoice_data["source_file"] = filename
            invoice_data["parsed_at"] = datetime.now().isoformat()
            invoice_data["raw_text"] = text[:1000] + "..." if len(text) > 1000 else text

        return invoice_data

    def parse_invoices_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Parse all PDF files in a directory"""
        invoices = []
        directory = Path(directory_path)

        if not directory.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return invoices

        pdf_files = list(directory.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files in {directory_path}")

        for pdf_file in pdf_files:
            try:
                invoice_data = self.parse_invoice_file(str(pdf_file))
                if invoice_data:
                    invoices.append(invoice_data)
                    logger.info(f"Successfully parsed: {pdf_file.name}")
                else:
                    logger.warning(f"Failed to parse: {pdf_file.name}")
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {e}")

        return invoices

    def format_for_database(self, invoice_data: Dict[str, Any], entity_id: int = 1, account_id: int = 1) -> Dict[str, Any]:
        """Format parsed invoice data for database insertion"""
        try:
            # Create transaction record
            transaction = {
                "entity_id": entity_id,
                "account_id": account_id,
                "amount": -float(invoice_data.get("total_amount", 0)),  # Negative for expense
                "description": f"Invoice {invoice_data.get('invoice_number', 'N/A')} - {invoice_data.get('description', 'Unknown')}",
                "transaction_date": invoice_data.get("invoice_date"),
                "vendor_name": invoice_data.get("vendor_name"),
                "reference_number": invoice_data.get("invoice_number"),
                "notes": f"Parsed from {invoice_data.get('source_file', 'unknown file')}"
            }

            # Add invoice metadata
            invoice_metadata = {
                "invoice_number": invoice_data.get("invoice_number"),
                "purchase_order": invoice_data.get("purchase_order"),
                "due_date": invoice_data.get("due_date"),
                "tax_amount": invoice_data.get("tax_amount"),
                "subtotal": invoice_data.get("subtotal"),
                "currency": invoice_data.get("currency", "AUD"),
                "description": invoice_data.get("description"),
                "project": invoice_data.get("project"),
                "client": invoice_data.get("client"),
                "paid_on": invoice_data.get("paid_on"),
                "billed_to": invoice_data.get("billed_to"),
                "vendor_abn": invoice_data.get("vendor_abn"),
                "payment_terms": invoice_data.get("payment_terms"),
                "line_items": invoice_data.get("line_items", []),
                "source_file": invoice_data.get("source_file"),
                "parsed_at": invoice_data.get("parsed_at")
            }

            return {
                "transaction": transaction,
                "invoice_metadata": invoice_metadata
            }

        except Exception as e:
            logger.error(f"Error formatting invoice data for database: {e}")
            return None

if __name__ == "__main__":
    # Test the parser
    parser = InvoiceParser()
    invoices = parser.parse_invoices_directory("../invoices")

    for invoice in invoices:
        print(f"\nParsed Invoice: {invoice.get('vendor_name')} - ${invoice.get('total_amount')}")
        db_format = parser.format_for_database(invoice)
        print(f"Transaction: {db_format['transaction']['description']}")