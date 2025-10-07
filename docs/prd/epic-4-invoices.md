# Epic 4: Invoice Management & PDF Generation

**Epic Goal**: Complete invoice lifecycle management from creation to payment tracking with professional PDF generation.

**Dependencies**: Epic 1 (Foundation)

**Key Stories** (7 total):
- 4.1: Invoice List Page with Status Filtering
- 4.2: Invoice Creation Form with Line Items
- 4.3: PDF Invoice Generation with Branding
- 4.4: Invoice Status Tracking & Payment Recording
- 4.5: Invoice Edit & Delete Functionality
- 4.6: Client/Supplier Quick Add from Invoice Form
- 4.7: Invoice Batch Actions & Export

**Success Criteria**:
- Invoice CRUD with status workflow (draft→sent→paid)
- Multi-line item support with GST calculation
- Professional PDF generation (@react-pdf/renderer)
- Payment tracking with partial payment support
- Batch operations (download PDFs, mark paid, export)
- Automatic overdue flagging

**Testing**: Unit (GST calculations), Integration (PDF generation), E2E (invoice creation flow)

**Estimated Effort**: 10-12 days
**Priority**: P1 (Core Feature)
