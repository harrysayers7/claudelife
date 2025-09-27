# Create ESM Invoice

This command helps you quickly create Stripe invoices for ESM (esmusic@dext.cc) music composition projects in the claudelife system, following MOK HOUSE PTY LTD business patterns and requirements.

IMPORTANT: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

## Usage

```bash
/create-esm-invoice [job-name] [amount] [fee-type]
```

## Interactive Process

When you run this command, I will:
1. Ask you to describe the specific music composition project
2. Confirm the job name, amount, and fee type (usage or demo)
3. Ask clarifying questions about:
   - Project-specific details for the description
   - Any additional line items needed
   - Special payment terms or notes
4. Generate the complete Stripe invoice using MCP tools
5. Confirm the invoice is created as a draft for your review

## Input Requirements

Before running this command, prepare:
1. **Job Name**: The project/campaign name (e.g., "Woolworths Summer Campaign")
2. **Amount**: Total fee in AUD (will be converted to cents for Stripe)
3. **Fee Type**: Either "usage fee" or "demo fee"

## Process

I'll help you create the ESM invoice by:

1. **Verify ESM Customer**: Confirm esmusic@dext.cc exists in Stripe customers
2. **Create Invoice**: Generate new invoice for ESM customer
3. **Add Line Items**: Add music composition service with proper description
4. **Set Payment Details**: Include MOK HOUSE bank details in invoice notes
5. **Leave as Draft**: Keep invoice in draft status for your review

## Technical Implementation Guide

### Customer Verification
```javascript
// Verify ESM customer exists
mcp__stripe__list_customers({ email: "esmusic@dext.cc" })
```

### Invoice Creation
```javascript
// Create invoice for ESM
mcp__stripe__create_invoice({
  customer: "cus_esm_customer_id",
  // No days_until_due - no specific due date requirement
})
```

### Line Item Addition
```javascript
// Add composition service line item
mcp__stripe__create_invoice_item({
  customer: "cus_esm_customer_id",
  invoice: "in_invoice_id",
  price: "price_id_for_service"
})
```

## Output Format

I'll provide:
1. **Invoice Confirmation**: Stripe invoice ID and status
2. **Invoice Summary**: Customer, amount, description, and draft status
3. **Next Steps**: Instructions for finalizing when ready
4. **Payment Details**: Confirmation that MOK HOUSE bank details are included

## Examples

### Example 1: Usage Fee Invoice

**Input**:
- Job: "Woolworths Summer Campaign"
- Amount: $5000
- Type: "usage fee"

**Generated Description**: "Woolworths Summer Campaign usage fee"

**Invoice Notes**:
```
Payment Details:
Account Name: MOK HOUSE PTY LTD
Bank Account: 612281562
BSB: 013943
```

### Example 2: Demo Fee Invoice

**Input**:
- Job: "Nike Brand Refresh"
- Amount: $1500
- Type: "demo fee"

**Generated Description**: "Nike Brand Refresh demo fee"

## Evaluation Criteria

A successful ESM invoice should:
1. **Correct Customer**: Target esmusic@dext.cc customer record
2. **Proper Description**: Include job name + fee type format
3. **Draft Status**: Left as draft for manual review and finalization
4. **Payment Details**: Include complete MOK HOUSE banking information
5. **Clean Format**: Professional invoice suitable for B2B music industry

## Related Resources

- ESM customer management: Stripe MCP customer tools
- Invoice finalization: Use `mcp__stripe__finalize_invoice` when ready
- Payment tracking: Monitor via `mcp__stripe__list_payment_intents`

## Starting the Invoice Creation Process

What music composition project would you like to invoice ESM for? Please provide:
- **Job/Campaign Name**: The specific project name
- **Amount**: Total fee in AUD
- **Fee Type**: "usage fee" or "demo fee"
- **Additional Details**: Any special notes or requirements for this invoice
