# Supabase Integration Patterns

## Client Initialization

**Server Components**:
```typescript
// lib/supabase-server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createClient() {
  const cookieStore = cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
      },
    }
  )
}
```

**Client Components**:
```typescript
// lib/supabase-client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

## Row Level Security (RLS) Patterns

**Entity-Based Access**:
```sql
-- All queries auto-filtered by entity_id
CREATE POLICY "Users can access their entity data"
ON transactions FOR SELECT
USING (entity_id IN (
  SELECT entity_id FROM user_entities WHERE user_id = auth.uid()
));
```

**Client-Side Enforcement**:
```typescript
// Always include entity_id filter
const { data } = await supabase
  .from('transactions')
  .select('*')
  .eq('entity_id', entityId)  // REQUIRED
```

## Query Patterns

**Server Component Fetching**:
```typescript
// app/dashboard/page.tsx
import { createClient } from '@/lib/supabase-server'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: transactions } = await supabase
    .from('transactions')
    .select('*')
    .eq('entity_id', entityId)
    .order('created_at', { ascending: false })
    .limit(10)

  return <Dashboard transactions={transactions} />
}
```

**Client Component Mutations**:
```typescript
// components/TransactionForm.tsx
'use client'
import { createClient } from '@/lib/supabase-client'

async function updateCategory(id: string, category: string) {
  const supabase = createClient()
  const { error } = await supabase
    .from('transactions')
    .update({
      manual_category: category,
      ai_category_override: true
    })
    .eq('id', id)

  if (error) throw error
}
```

## Type Safety

```typescript
// types/supabase.ts (generated)
import { Database } from '@/types/supabase'

type Transaction = Database['public']['Tables']['transactions']['Row']
type TransactionInsert = Database['public']['Tables']['transactions']['Insert']
```

## Real-Time Subscriptions (Optional)

```typescript
const channel = supabase
  .channel('transactions')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'transactions' },
    (payload) => {
      console.log('New transaction:', payload.new)
    }
  )
  .subscribe()
```

## Error Handling

```typescript
try {
  const { data, error } = await supabase.from('transactions').select('*')
  if (error) throw error
  return data
} catch (err) {
  console.error('Supabase query failed:', err)
  toast.error('Failed to load transactions')
  return []
}
```
