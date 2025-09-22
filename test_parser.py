#!/usr/bin/env python3
"""
Test the improved invoice parser
"""
import sys
import os
sys.path.append('.mcp')

# Import the parser
from invoice_parser import InvoiceParser

def test_parser():
    print("Testing improved invoice parser...")

    # Set up the parser
    parser = InvoiceParser()

    # Test with multiple invoices that should have purchase orders
    test_invoices = [
        "/Users/harrysayers/Dropbox/03_M4M/0302_M4M_Docs/0302.1_M4M_Invoices/0301.1_M4M_FY26/250915_ESM_INV_Repco_PO-0934.pdf",
        "/Users/harrysayers/Dropbox/03_M4M/0302_M4M_Docs/0302.1_M4M_Invoices/0301.1_M4M_FY26/250818_0302_ESM_Nintendo_PO-0909_INV-57.pdf",
        "/Users/harrysayers/Dropbox/03_M4M/0302_M4M_Docs/0302.1_M4M_Invoices/0301.1_M4M_FY26/250811_03_ESM_DiDi_Flute-intro_INV_PO-0908.pdf"
    ]

    for invoice_path in test_invoices:
        print(f"\n=== Testing: {invoice_path.split('/')[-1]} ===")

        if not os.path.exists(invoice_path):
            print(f"❌ Invoice file not found: {invoice_path}")
            continue

        invoice_data = parser.parse_invoice_file(invoice_path)

        if invoice_data:
            print("✅ Successfully parsed!")
            print(f"Vendor: {invoice_data.get('vendor_name')}")
            print(f"Invoice: {invoice_data.get('invoice_number')}")
            print(f"Purchase Order: {invoice_data.get('purchase_order', 'NOT EXTRACTED')}")
            print(f"Project: {invoice_data.get('project', 'NOT EXTRACTED')}")
            print(f"Amount: ${invoice_data.get('total_amount')}")
        else:
            print("❌ Failed to parse invoice")

if __name__ == "__main__":
    test_parser()