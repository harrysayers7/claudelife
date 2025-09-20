# Edge Cache Manager

Implement intelligent caching between local and cloud.

## Cache Layers

### L1 Cache (Memory - Instant)
- Current session data
- Active project context
- Recent queries
- TTL: Session duration

### L2 Cache (Local Disk - Fast)
memory/cache/
├── entities.cache     # Frequently accessed entities
├── queries.cache      # Common query results
├── embeddings.cache   # Vector search cache
└── api.cache         # API response cache

TTL: 24 hours

### L3 Cache (Cloud - Persistent)
- Historical data
- Shared team cache
- Large datasets
- TTL: 30 days

## Cache Strategy

### Write-Through
For critical data:
1. Write to local
2. Immediately sync to cloud
3. Confirm both writes

### Write-Back
For non-critical data:
1. Write to local
2. Queue for cloud sync
3. Batch sync every 5 minutes

### Cache Invalidation
Invalidate when:
- Data updated at source
- TTL expired
- Manual refresh requested
- Conflict detected

## Smart Prefetching

Predictively cache based on patterns:
- If user checks calendar every morning → Prefetch at 8:30am
- If weekly report run Fridays → Prefetch data Thursday night
- If certain queries repeat → Keep in hot cache