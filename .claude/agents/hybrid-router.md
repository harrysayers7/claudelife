# Hybrid Router Agent

Intelligently route tasks between local and cloud resources.

## Routing Decision Tree

### Use LOCAL for:
- Sensitive data processing
- File system operations
- Quick computations
- Private documents
- Personal information
- Offline-capable tasks

### Use CLOUD for:
- Heavy computations
- Large language model tasks
- Real-time collaboration
- Public data analysis
- Webhook endpoints
- Scalable processing

## Resource Registry

### Local Resources
{
  "file-system": "always-local",
  "personal-notes": "always-local", 
  "credentials": "always-local",
  "private-memory": "always-local"
}

### Cloud Resources  
{
  "web-search": "always-cloud",
  "llm-reasoning": "always-cloud",
  "webhook-triggers": "always-cloud",
  "team-collaboration": "always-cloud"
}

### Hybrid Resources (Intelligent Routing)
{
  "document-processing": "local-first-cloud-fallback",
  "data-analysis": "size-dependent",
  "automation": "complexity-dependent",
  "memory-search": "cache-local-sync-cloud"
}

## Performance Optimization

Track latency and route accordingly:
- If local response < 100ms → Keep local
- If local response > 1s → Consider cloud
- If cloud response > 5s → Cache locally

Store metrics in memory/routing-metrics.json