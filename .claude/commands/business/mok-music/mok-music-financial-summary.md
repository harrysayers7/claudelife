# MOK Music - Financial Analysis & Projections

Generate comprehensive financial reports for MOK Music operations with cash flow analysis and projections.

## Usage
```
/mok-music-financial-summary [period] [type]
```

**Periods:**
- `monthly` - Current month analysis
- `quarterly` - Current quarter analysis
- `yearly` - Current year analysis
- `custom` - Prompt for date range

**Types:**
- `cashflow` - Focus on cash flow and outstanding
- `performance` - Revenue and project performance
- `projections` - Forward-looking analysis
- `tax` - Tax preparation summary

## Steps

1. **Gather financial data**
   ```javascript
   mcp__notion__API-post-database-query({
     database_id: "1e64a17b-b7f0-807d-b0f3-fe2cf5a6e3ac",
     page_size: 100,
     filter: {
       property: "Date Received",
       date: {on_or_after: "[period_start]"}
     }
   })
   ```

2. **Calculate key metrics**
   - **Revenue Analysis:**
     - Total invoiced (completed projects)
     - Total outstanding (awaiting payment)
     - Average project value (demo + award fees)
     - Project completion rate

   - **Cash Flow:**
     - Current month receipts
     - Outstanding receivables by age
     - Average payment cycle (submission to payment)
     - Projected monthly income

3. **Generate comprehensive report**
   ```
   💰 MOK MUSIC FINANCIAL SUMMARY - [Period]

   REVENUE PERFORMANCE
   • Total Projects: [count]
   • Total Invoiced: $[amount]
   • Total Outstanding: $[amount] ([count] projects)
   • Average Project Value: $[amount]

   CASH FLOW ANALYSIS
   • Current Period Income: $[amount]
   • Outstanding 0-30 days: $[amount] ([count] projects)
   • Outstanding 30+ days: $[amount] ([count] projects)
   • Projected Next 30 days: $[amount]

   PROJECT BREAKDOWN
   • Demo Fees: $[total] (avg: $[avg])
   • Award Fees: $[total] (avg: $[avg])
   • Completion Rate: [percentage]%

   APRA STATUS
   • Registered: [count] projects
   • Pending: [count] projects
   • Not Done: [count] projects
   ```

4. **Identify trends and insights**
   - Seasonal patterns in project volume
   - Average payment delay trends
   - Most profitable project types
   - Client performance patterns

5. **Generate actionable recommendations**
   ```
   📈 INSIGHTS & RECOMMENDATIONS

   CASH FLOW:
   • [Specific recommendations for improving cash flow]

   BUSINESS DEVELOPMENT:
   • [Opportunities based on performance data]

   OPERATIONAL:
   • [Process improvements based on analysis]
   ```

6. **Integration with broader financial system**
   If Supabase financial API is available:
   ```javascript
   mcp__claudelife-financial-api__get_financial_metrics({
     entity_id: [MOK_HOUSE_ENTITY_ID],
     period: "[selected_period]"
   })
   ```

7. **Tax preparation assistance** (when type=tax)
   - Categorize income by tax year
   - Identify deductible expenses
   - Prepare GST summary
   - Flag items needing accountant review

8. **Export capabilities**
   - Generate CSV for external analysis
   - Create PDF report for stakeholders
   - Prepare data for accounting software

## Context
This command provides Harry with comprehensive financial visibility into MOK Music operations, enabling data-driven business decisions, cash flow management, and strategic planning. It connects with the existing ESM Projects database to provide actionable insights.
