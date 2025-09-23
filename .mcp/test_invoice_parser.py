#!/usr/bin/env python3

from invoice_parser import InvoiceParser
import os
import json

def test_invoice_parser():
    print('Testing invoice parser...')
    parser = InvoiceParser()

    invoice_path = '/Users/harrysayers/Dropbox/03_M4M/0302_M4M_Docs/0302.1_M4M_Invoices/0301.1_M4M_FY26/250915_ESM_INV_Repco_PO-0934.pdf'

    if not os.path.exists(invoice_path):
        print(f'❌ Invoice file not found: {invoice_path}')
        return

    print(f'Parsing: {os.path.basename(invoice_path)}')
    result = parser.parse_invoice_file(invoice_path)

    if result:
        print('✅ Parsing successful!')
        print(f"Vendor: {result.get('vendor_name', 'Unknown')}")
        print(f"Invoice #: {result.get('invoice_number', 'Unknown')}")
        print(f"Amount: ${result.get('total_amount', 0)}")
        print(f"Date: {result.get('invoice_date', 'Unknown')}")
        print(f"Currency: {result.get('currency', 'Unknown')}")

        print('\nLine Items:')
        line_items = result.get('line_items', [])
        for item in line_items:
            print(f"  - {item.get('description', 'Unknown')}: ${item.get('total', 0)}")

        print('\nFormatting for database...')
        db_format = parser.format_for_database(result)
        if db_format:
            print('✅ Database format successful!')
            print(f"Transaction description: {db_format['transaction']['description']}")
            print(f"Transaction amount: ${db_format['transaction']['amount']}")

        # Save full result to file for inspection
        output_path = 'parsed_invoice_result.json'
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f'\n📄 Full result saved to: {output_path}')

    else:
        print('❌ Parsing failed')

if __name__ == "__main__":
    test_invoice_parser()
