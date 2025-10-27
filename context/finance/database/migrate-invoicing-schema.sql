-- ============================================================
-- Supabase Invoicing Schema Migration
-- Integrated with existing public schema
-- ============================================================
--
-- This script creates a new `invoicing` schema that:
-- 1. REUSES existing contacts (Electric Sheep Music, etc.)
-- 2. EXTENDS existing invoices with invoice items & payments
-- 3. INTEGRATES with existing project_id system
-- 4. MAINTAINS backward compatibility with public schema
--
-- NO data duplication - foreign keys reference existing tables
--
-- ============================================================

-- ============================================================
-- PHASE 1: Create Invoicing Schema
-- ============================================================

CREATE SCHEMA IF NOT EXISTS invoicing;

COMMENT ON SCHEMA invoicing IS 'Invoice generation, PDF rendering, email delivery, and payment tracking';


-- ============================================================
-- PHASE 2: Create Invoice-Specific Tables
-- ============================================================

-- 2.1: Invoice Items (line items for each invoice)
CREATE TABLE IF NOT EXISTS invoicing.invoice_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES public.invoices(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  quantity DECIMAL(10,2) NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL,
  tax_rate DECIMAL(4,2) DEFAULT 10.0,
  line_total DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
  line_tax DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price * (tax_rate / 100)) STORED,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_invoicing_items_invoice ON invoicing.invoice_items(invoice_id);

COMMENT ON TABLE invoicing.invoice_items IS 'Line items for invoices - references existing public.invoices';
COMMENT ON COLUMN invoicing.invoice_items.invoice_id IS 'Foreign key to public.invoices - maintains integration with existing invoice system';


-- 2.2: Invoice Payments (track partial/full payments)
CREATE TABLE IF NOT EXISTS invoicing.invoice_payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES public.invoices(id) ON DELETE CASCADE,
  amount_paid DECIMAL(12,2) NOT NULL,
  payment_date DATE NOT NULL,
  payment_method TEXT,
  reference TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_invoicing_payments_invoice ON invoicing.invoice_payments(invoice_id);

COMMENT ON TABLE invoicing.invoice_payments IS 'Payment records for invoices - tracks partial and full payments';


-- 2.3: Invoice Settings (per-entity configuration)
CREATE TABLE IF NOT EXISTS invoicing.invoice_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_id UUID NOT NULL REFERENCES public.entities(id) ON DELETE CASCADE,
  next_invoice_number INT DEFAULT 1,
  invoice_prefix TEXT NOT NULL,
  default_payment_terms_days INT DEFAULT 14,
  bank_details JSONB,
  logo_url TEXT,
  footer_text TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(entity_id)
);

CREATE INDEX idx_invoicing_settings_entity ON invoicing.invoice_settings(entity_id);

COMMENT ON TABLE invoicing.invoice_settings IS 'Invoice generation settings per entity (MOK HOUSE, MOKAI, etc.)';
COMMENT ON COLUMN invoicing.invoice_settings.invoice_prefix IS 'Prefix for invoice numbering (e.g., "MH", "MK", "ESP")';


-- ============================================================
-- PHASE 3: Create PDF & Email Delivery Tables
-- ============================================================

-- 3.1: Invoice PDFs (store generated PDFs with metadata)
CREATE TABLE IF NOT EXISTS invoicing.invoice_pdfs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES public.invoices(id) ON DELETE CASCADE,
  pdf_url TEXT NOT NULL,
  pdf_size_bytes INT,
  generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  file_name TEXT,
  storage_path TEXT
);

CREATE INDEX idx_invoicing_pdfs_invoice ON invoicing.invoice_pdfs(invoice_id);

COMMENT ON TABLE invoicing.invoice_pdfs IS 'Generated PDF invoices - stored in Supabase Storage';


-- 3.2: Email Delivery Log
CREATE TABLE IF NOT EXISTS invoicing.email_deliveries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES public.invoices(id) ON DELETE CASCADE,
  recipient_email TEXT NOT NULL,
  sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  status TEXT DEFAULT 'pending', -- pending, sent, failed, bounced, opened
  error_message TEXT,
  smtp_message_id TEXT,
  opened_at TIMESTAMP WITH TIME ZONE,
  opened_count INT DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_invoicing_email_invoice ON invoicing.email_deliveries(invoice_id);
CREATE INDEX idx_invoicing_email_status ON invoicing.email_deliveries(status);

COMMENT ON TABLE invoicing.email_deliveries IS 'Track invoice email deliveries - integration with SMTP service';


-- ============================================================
-- PHASE 4: Create Views for Easy Integration
-- ============================================================

-- 4.1: Invoice with Items View (for PDF generation)
CREATE OR REPLACE VIEW invoicing.v_invoice_details AS
SELECT
  i.id,
  i.entity_id,
  i.contact_id,
  i.invoice_number,
  i.invoice_date,
  i.due_date,
  i.project,
  i.project_id,
  i.subtotal_amount,
  i.gst_amount,
  i.total_amount,
  i.status,
  c.name as client_name,
  c.email as client_email,
  c.abn as client_abn,
  c.billing_address,
  e.name as entity_name,
  e.abn as entity_abn,
  e.trading_name,
  COALESCE(s.invoice_prefix, 'INV') as invoice_prefix,
  COALESCE(s.bank_details, '{}'::jsonb) as bank_details,
  s.footer_text
FROM public.invoices i
LEFT JOIN public.contacts c ON i.contact_id = c.id
LEFT JOIN public.entities e ON i.entity_id = e.id
LEFT JOIN invoicing.invoice_settings s ON i.entity_id = s.entity_id;

COMMENT ON VIEW invoicing.v_invoice_details IS 'Complete invoice data with client, entity, and settings - for PDF generation';


-- 4.2: Invoice with Line Items View
CREATE OR REPLACE VIEW invoicing.v_invoice_with_items AS
SELECT
  i.*,
  json_agg(
    json_build_object(
      'id', it.id,
      'description', it.description,
      'quantity', it.quantity,
      'unit_price', it.unit_price,
      'tax_rate', it.tax_rate,
      'line_total', it.line_total,
      'line_tax', it.line_tax
    ) ORDER BY it.created_at
  ) as items
FROM invoicing.v_invoice_details i
LEFT JOIN invoicing.invoice_items it ON i.id = it.invoice_id
GROUP BY i.id, i.entity_id, i.contact_id, i.invoice_number, i.invoice_date,
         i.due_date, i.project, i.project_id, i.subtotal_amount, i.gst_amount,
         i.total_amount, i.status, i.client_name, i.client_email, i.client_abn,
         i.billing_address, i.entity_name, i.entity_abn, i.trading_name,
         i.invoice_prefix, i.bank_details, i.footer_text;

COMMENT ON VIEW invoicing.v_invoice_with_items IS 'Invoice with all line items aggregated - ready for PDF rendering';


-- 4.3: Payment Status View
CREATE OR REPLACE VIEW invoicing.v_invoice_payment_status AS
SELECT
  i.id,
  i.invoice_number,
  i.entity_id,
  i.contact_id,
  i.total_amount,
  i.paid_amount,
  COALESCE(SUM(ip.amount_paid), 0) as total_recorded_payments,
  (i.total_amount - COALESCE(SUM(ip.amount_paid), 0)) as remaining_balance,
  CASE
    WHEN (i.total_amount - COALESCE(SUM(ip.amount_paid), 0)) <= 0 THEN 'paid'
    WHEN COALESCE(SUM(ip.amount_paid), 0) > 0 THEN 'partial'
    ELSE 'unpaid'
  END as payment_status,
  COUNT(ip.id) as payment_count,
  MAX(ip.payment_date) as last_payment_date
FROM public.invoices i
LEFT JOIN invoicing.invoice_payments ip ON i.id = ip.invoice_id
GROUP BY i.id, i.invoice_number, i.entity_id, i.contact_id, i.total_amount, i.paid_amount;

COMMENT ON VIEW invoicing.v_invoice_payment_status IS 'Track invoice payment status across all invoices';


-- ============================================================
-- PHASE 5: Create Utility Functions
-- ============================================================

-- 5.1: Generate next invoice number
CREATE OR REPLACE FUNCTION invoicing.get_next_invoice_number(p_entity_id UUID)
RETURNS TEXT AS $$
DECLARE
  v_prefix TEXT;
  v_next_number INT;
  v_invoice_number TEXT;
BEGIN
  -- Get or create invoice settings for this entity
  INSERT INTO invoicing.invoice_settings (entity_id, invoice_prefix, next_invoice_number)
  VALUES (p_entity_id, 'INV', 1)
  ON CONFLICT (entity_id) DO NOTHING;

  -- Get current prefix and next number
  SELECT invoice_prefix, next_invoice_number
  INTO v_prefix, v_next_number
  FROM invoicing.invoice_settings
  WHERE entity_id = p_entity_id;

  -- Generate invoice number (e.g., "MH-2025-001")
  v_invoice_number := v_prefix || '-' || TO_CHAR(CURRENT_DATE, 'YYYY') || '-' ||
                      LPAD(v_next_number::TEXT, 3, '0');

  -- Increment counter
  UPDATE invoicing.invoice_settings
  SET next_invoice_number = next_invoice_number + 1,
      updated_at = NOW()
  WHERE entity_id = p_entity_id;

  RETURN v_invoice_number;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION invoicing.get_next_invoice_number(UUID) IS 'Generate next invoice number for entity with auto-increment';


-- 5.2: Calculate invoice totals from items
CREATE OR REPLACE FUNCTION invoicing.calculate_invoice_totals(p_invoice_id UUID)
RETURNS TABLE (subtotal DECIMAL, gst DECIMAL, total DECIMAL) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COALESCE(SUM(it.line_total), 0)::DECIMAL,
    COALESCE(SUM(it.line_tax), 0)::DECIMAL,
    COALESCE(SUM(it.line_total) + SUM(it.line_tax), 0)::DECIMAL
  FROM invoicing.invoice_items it
  WHERE it.invoice_id = p_invoice_id;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION invoicing.calculate_invoice_totals(UUID) IS 'Calculate subtotal, GST, and total from invoice items';


-- ============================================================
-- PHASE 6: Create Triggers for Audit Trail
-- ============================================================

-- 6.1: Audit trigger for invoice updates
CREATE OR REPLACE FUNCTION invoicing.track_invoice_updates()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'UPDATE' THEN
    NEW.updated_at = NOW();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER invoicing_items_audit
BEFORE UPDATE ON invoicing.invoice_items
FOR EACH ROW EXECUTE FUNCTION invoicing.track_invoice_updates();

CREATE TRIGGER invoicing_settings_audit
BEFORE UPDATE ON invoicing.invoice_settings
FOR EACH ROW EXECUTE FUNCTION invoicing.track_invoice_updates();

CREATE TRIGGER invoicing_email_audit
BEFORE UPDATE ON invoicing.email_deliveries
FOR EACH ROW EXECUTE FUNCTION invoicing.track_invoice_updates();


-- ============================================================
-- PHASE 7: Initialize Invoice Settings for Existing Entities
-- ============================================================

-- Insert settings for MOK HOUSE if not exists
INSERT INTO invoicing.invoice_settings (entity_id, invoice_prefix, next_invoice_number)
SELECT id, 'MH', 1
FROM public.entities
WHERE name = 'MOK HOUSE PTY LTD'
ON CONFLICT (entity_id) DO NOTHING;

-- Insert settings for MOKAI if not exists
INSERT INTO invoicing.invoice_settings (entity_id, invoice_prefix, next_invoice_number)
SELECT id, 'MK', 1
FROM public.entities
WHERE name ILIKE '%MOKAI%'
ON CONFLICT (entity_id) DO NOTHING;

-- Insert settings for other entities
INSERT INTO invoicing.invoice_settings (entity_id, invoice_prefix, next_invoice_number)
SELECT id, 'INV', 1
FROM public.entities
WHERE id NOT IN (SELECT entity_id FROM invoicing.invoice_settings)
ON CONFLICT (entity_id) DO NOTHING;


-- ============================================================
-- PHASE 8: Grant Permissions
-- ============================================================

GRANT USAGE ON SCHEMA invoicing TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA invoicing TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA invoicing TO authenticated;


-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Check invoice settings initialized
SELECT entity_id, invoice_prefix, next_invoice_number FROM invoicing.invoice_settings;

-- View invoice details structure
SELECT * FROM invoicing.v_invoice_details LIMIT 1;
