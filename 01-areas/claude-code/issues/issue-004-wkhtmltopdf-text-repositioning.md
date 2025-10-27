---
title: wkhtmltopdf repositioning text in invoice PDF
type:
  - issue
aliases:
  - issue-004
id: issue-004
category: script
relation:
complete: false
solved: false
lesson:
created: Sun, 10 26th 25, 3:15:00 pm
severity: high
attempted-solutions:
  - Verified HTML rendering is correct (template renders properly in `/tmp/invoice-TEST-001.html`)
  - Confirmed generate-invoice.js only fills Handlebars variables, doesn't modify CSS or layout
  - Identified wkhtmltopdf as root cause (has limited CSS3 support, poor grid/flexbox rendering)
error-messages: |
  No console errors, but PDF output shows misaligned text positioning
  HTML layout is correct, but wkhtmltopdf converts it with repositioned elements
related-files:
  - /src/invoicing/generate-invoice.js
  - /src/invoicing/templates/invoice.html
  - /tmp/invoice-TEST-001.html (rendered HTML - correct layout)
  - /tmp/invoice-TEST-001.pdf (generated PDF - text mispositioned)
---

## Problem Description

The invoice PDF generation process is working, but `wkhtmltopdf` is not accurately preserving text positioning from the HTML template during PDF conversion. The HTML renders correctly with proper grid layout and text alignment, but when converted to PDF, text elements are repositioned and spacing is incorrect.

## Expected Behavior

Generated PDF should visually match the HTML layout exactly:
- Company name [MOK HOUSE] centered at 70px
- Invoice number, PO, and DATE properly aligned
- Line items table with correct column spacing
- Totals right-aligned with proper formatting
- Payment section in 2-column grid layout

## Actual Behavior

PDF output has:
- Text repositioned from original positions
- Spacing and alignment broken
- Grid layout not rendering correctly (CSS3 limitations)
- Professional appearance compromised

## Steps to Reproduce

1. Run invoice generation: `node src/invoicing/generate-invoice.js`
2. Check rendered HTML: `cat /tmp/invoice-TEST-001.html` (layout is correct)
3. Check generated PDF: `open /tmp/invoice-TEST-001.pdf` (text is mispositioned)

## Environment

- Node.js: v18+ (npm installed)
- PDF tool: wkhtmltopdf 0.12.x
- Template: HTML with CSS Grid, Flexbox
- Handlebars: 4.7.x
- OS: macOS/Linux

## Root Cause

`wkhtmltopdf` has limited CSS3 support and doesn't properly handle:
- CSS Grid layouts (`display: grid`)
- Flexbox layouts (`display: flex`)
- Modern spacing/alignment techniques
- Complex positioning

This is a known limitation of wkhtmltopdf (last major update 2014).

## Additional Context

**Current generation flow:**
1. Load template HTML (has proper CSS Grid layout)
2. Compile with Handlebars
3. Render with test data
4. Convert to PDF with wkhtmltopdf ← **Issue here**

**What's working:**
- HTML rendering and variable substitution is perfect
- Template design is professional and correct
- Script logic is sound

**What's broken:**
- wkhtmltopdf PDF conversion accuracy

## Proposed Solution

Replace `wkhtmltopdf` with **Puppeteer** (Chromium-based):
- Uses real browser engine for rendering
- Handles CSS3 Grid, Flexbox, modern CSS properly
- Better PDF output quality
- More reliable for complex layouts

**Implementation approach:**
1. Install `puppeteer` npm package
2. Update `generate-invoice.js` to use Puppeteer instead of wkhtmltopdf
3. Test with invoice template to verify layout preservation
4. Update documentation

## Resolution

[To be filled when issue is resolved via `/issue-call 004`]
