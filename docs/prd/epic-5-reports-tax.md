# Epic 5: Reports & Tax Compliance

**Epic Goal**: Implement BAS calculation, income statements, and flexible data export for tax compliance.

**Dependencies**: Epic 1 (Foundation), Epic 3 (Transactions), Epic 4 (Invoices)

**Key Stories** (7 total):
- 5.1: BAS Calculation Engine & Data Service
- 5.2: BAS Report Generation Page
- 5.3: Income Statement (P&L) Generation
- 5.4: Report Period Selection & Fiscal Year Support
- 5.5: Transaction Data Export (CSV, Excel, Accounting Formats)
- 5.6: Report Preview & Validation
- 5.7: Scheduled Report Generation & Email Delivery

**Success Criteria**:
- Accurate BAS calculations following Australian tax rules
- P&L reports with category grouping
- Period selection (monthly, quarterly, fiscal year, custom)
- Export formats: CSV, Excel, Xero, MYOB compatible
- Report preview with validation warnings
- Scheduled report automation (optional)

**Testing**: Unit (GST calculations - 100% coverage), Integration (report generation), E2E (BAS generation flow)

**Estimated Effort**: 8-10 days
**Priority**: P1 (Critical for Tax Compliance)
