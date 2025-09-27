# MOK Music - Prepare Invoice & Update Project Status

Update project status and prepare invoice materials when a project is complete and ready for billing.

## Usage
```
/mok-music-invoice-ready [project_name]
```

**Example:**
- `/mok-music-invoice-ready Repco`
- `/mok-music-invoice-ready "Nintendo Campaign"`

## Steps

1. **Locate and validate project**
   ```javascript
   mcp__notion__API-post-database-query({
     database_id: "1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac",
     filter: {property: "Name", title: {contains: "[project_name]"}}
   })
   ```

2. **Gather invoice requirements**
   Extract from project:
   - PO number (if available)
   - Demo fee and Award fee amounts
   - Project completion date
   - Client/agency details
   - Any special billing instructions

3. **Update project status**
   ```javascript
   mcp__notion__API-patch-page({
     page_id: "[project_id]",
     properties: {
       "Status": {type: "status", status: {name: "Awaiting PO"}},
       "Invoice Sent": {type: "date", date: {start: [today]}}
     }
   })
   ```

4. **Generate invoice details**
   Create formatted invoice information:
   ```
   📄 INVOICE PREPARATION - [Project Name]

   MOK HOUSE PTY LTD
   ABN: 38690628212 (GST Registered)

   Invoice To: Electric Sheep Music Pty Ltd
   Email: esmusic@dext.cc

   Project: [Project Name]
   PO Number: [PO if available]

   CHARGES:
   • Demo Fee: $[amount] + GST
   • Award/Usage Fee: $[amount] + GST
   TOTAL: $[total_inc_gst]

   BANK DETAILS:
   Account: MOK HOUSE PTY LTD
   BSB: 013943
   Account: 612281562
   ```

5. **Set up monitoring**
   - Add to follow-up workflow for payment tracking
   - Set reminder for 30-day overdue check
   - Update cash flow projections

6. **APRA reminder**
   If APRA status is not "Done":
   - Remind to complete APRA registration
   - Provide APRA work details template

## Context
This command streamlines the invoicing process for completed MOK Music projects, ensuring proper documentation, status updates, and follow-up tracking while maintaining the established workflow with Electric Sheep Music's Xero/Dext system.
