# Financial Calculations Architecture

## GST Calculation (10% Australian GST)

**Using decimal.js for Precision**:
```typescript
import Decimal from 'decimal.js'

export function calculateGST(subtotalCents: number): number {
  const subtotal = new Decimal(subtotalCents)
  const gst = subtotal.mul(0.1).toDecimalPlaces(0, Decimal.ROUND_HALF_UP)
  return gst.toNumber()
}

export function calculateTotal(subtotalCents: number, gstCents: number): number {
  const subtotal = new Decimal(subtotalCents)
  const gst = new Decimal(gstCents)
  return subtotal.add(gst).toNumber()
}
```

**Invoice Line Item Calculation**:
```typescript
export function calculateLineItem(
  quantity: number,
  unitPriceCents: number,
  gstApplicable: boolean
): { amountCents: number; gstCents: number } {
  const qty = new Decimal(quantity)
  const price = new Decimal(unitPriceCents)
  const amount = qty.mul(price).toDecimalPlaces(0, Decimal.ROUND_HALF_UP)

  const gst = gstApplicable
    ? amount.mul(0.1).toDecimalPlaces(0, Decimal.ROUND_HALF_UP)
    : new Decimal(0)

  return {
    amountCents: amount.toNumber(),
    gstCents: gst.toNumber(),
  }
}
```

## BAS Calculations

**G1: Total Sales (Including GST)**:
```typescript
export function calculateG1TotalSales(
  entityId: string,
  startDate: Date,
  endDate: Date
): Promise<number> {
  // Sum of all sales transactions with GST
  const result = await supabase
    .from('invoices')
    .select('total_cents')
    .eq('entity_id', entityId)
    .eq('invoice_type', 'RECEIVABLE')
    .gte('payment_date', startDate)
    .lte('payment_date', endDate)
    .eq('status', 'PAID')

  return result.data.reduce((sum, inv) =>
    new Decimal(sum).add(inv.total_cents).toNumber(), 0
  )
}
```

**Field 1A: GST on Sales**:
```typescript
export function calculate1AGSTOnSales(
  entityId: string,
  startDate: Date,
  endDate: Date
): Promise<number> {
  // Sum of GST collected on sales
  const result = await supabase
    .from('invoices')
    .select('gst_cents')
    .eq('entity_id', entityId)
    .eq('invoice_type', 'RECEIVABLE')
    .gte('payment_date', startDate)
    .lte('payment_date', endDate)
    .eq('status', 'PAID')

  return result.data.reduce((sum, inv) =>
    new Decimal(sum).add(inv.gst_cents).toNumber(), 0
  )
}
```

**Field 7: Net GST (Amount Owed or Refund)**:
```typescript
export function calculate7NetGST(
  gstOnSales: number,
  gstOnPurchases: number
): number {
  const sales = new Decimal(gstOnSales)
  const purchases = new Decimal(gstOnPurchases)
  return sales.sub(purchases).toNumber() // Positive = owe, Negative = refund
}
```

## Profit/Loss Calculation

```typescript
export function calculateProfit(
  revenueCents: number,
  expensesCents: number
): number {
  const revenue = new Decimal(revenueCents)
  const expenses = new Decimal(Math.abs(expensesCents)) // Ensure positive
  return revenue.sub(expenses).toNumber()
}
```

## Currency Formatting

```typescript
export function formatAUD(cents: number): string {
  const dollars = new Decimal(cents).div(100)
  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD',
  }).format(dollars.toNumber())
}
```

## Rounding Rules

**Australian Tax Office Rounding**:
- GST amounts: Round to nearest cent (HALF_UP)
- Totals: Round to nearest cent (HALF_UP)
- BAS fields: Round to nearest dollar (amounts in cents internally)

```typescript
Decimal.set({ rounding: Decimal.ROUND_HALF_UP })
```
