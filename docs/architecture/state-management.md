# State Management Architecture

## Global State (React Context)

**Entity Context**:
```typescript
// contexts/EntityContext.tsx
interface EntityContextType {
  entityId: string | null
  entity: Entity | null
  entities: Entity[]
  setEntityId: (id: string) => void
  isLoading: boolean
}

export const EntityContext = createContext<EntityContextType>()

export function EntityProvider({ children }) {
  const [entityId, setEntityId] = useState<string | null>(
    localStorage.getItem('selectedEntityId')
  )

  // Fetch entities from Supabase
  // Persist selection to localStorage

  return (
    <EntityContext.Provider value={...}>
      {children}
    </EntityContext.Provider>
  )
}
```

**Usage**:
```typescript
import { useEntity } from '@/contexts/EntityContext'

export function Dashboard() {
  const { entityId } = useEntity()
  // Query filtered by entityId
}
```

## Server State (TanStack Query - Optional)

**Transaction Queries**:
```typescript
import { useQuery } from '@tanstack/react-query'

export function useTransactions(entityId: string) {
  return useQuery({
    queryKey: ['transactions', entityId],
    queryFn: () => fetchTransactions(entityId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}
```

**Optimistic Updates**:
```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

export function useCategoryUpdate() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateCategory,
    onMutate: async (variables) => {
      // Optimistic update
      await queryClient.cancelQueries(['transactions'])
      const previous = queryClient.getQueryData(['transactions'])
      queryClient.setQueryData(['transactions'], (old) => {
        // Update transaction in cache
      })
      return { previous }
    },
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(['transactions'], context.previous)
    },
  })
}
```

## Form State (React Hook Form)

**Invoice Form**:
```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const invoiceSchema = z.object({
  client_id: z.string().uuid(),
  issue_date: z.date(),
  line_items: z.array(z.object({
    description: z.string(),
    quantity: z.number().positive(),
    unit_price_cents: z.number().int().positive(),
  })).min(1),
})

export function InvoiceForm() {
  const form = useForm({
    resolver: zodResolver(invoiceSchema),
  })

  const onSubmit = form.handleSubmit(async (data) => {
    // Submit to Supabase
  })
}
```

## URL State (Next.js Routing)

**Filters in URL**:
```typescript
import { useRouter, useSearchParams } from 'next/navigation'

export function TransactionFilters() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const updateFilters = (newFilters) => {
    const params = new URLSearchParams(searchParams)
    params.set('category', newFilters.category)
    params.set('startDate', newFilters.startDate)
    router.push(`/transactions?${params.toString()}`)
  }
}
```

## Local State (useState)

**Modal Open/Close**:
```typescript
const [isOpen, setIsOpen] = useState(false)
```

**Selection State**:
```typescript
const [selectedIds, setSelectedIds] = useState<string[]>([])
```
