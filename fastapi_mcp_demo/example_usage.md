# FastAPI-MCP: What It Actually Does

## The Problem Without FastAPI-MCP

**Before:** You have business logic in FastAPI endpoints, but Claude Code can't use them:

```bash
# Manual API call - Claude Code can't do this automatically
curl -X POST http://localhost:8001/compliance/check \
  -H "Content-Type: application/json" \
  -d '{"vendor_abn": "12345678901", "framework": "IRAP"}'

# Response: {"vendor_abn":"12345678901","framework":"IRAP","status":"non-compliant","score":72}
```

## The Solution With FastAPI-MCP

**After:** Claude Code can directly call your business functions as tools:

## Real Example: MOKAI Compliance Checking

### What You Can Now Ask Claude Code:

> "Check if vendor ABN 12345678901 is IRAP compliant"

### What Claude Code Will Do Automatically:

1. **Recognizes the request** as needing compliance checking
2. **Calls the check_vendor_compliance tool** (your FastAPI endpoint)
3. **Returns structured business data**:
   - Status: non-compliant
   - Score: 72/100
   - Risk level: medium
   - Certifications: ISO27001, SOC2

### What You Can Ask Next:

> "Find all government tenders related to cybersecurity under $500k"

Claude Code will automatically:
1. Call the `search_government_tenders` tool
2. Filter by keywords="cybersecurity" and max_value=500000
3. Return matching tender opportunities

## Business Value Examples

### 1. **Automated Tender Monitoring**
```
You: "Monitor tenders for 'penetration testing' this week"
Claude: *Automatically searches and filters relevant opportunities*
Result: 3 matching tenders found, total value $1.2M
```

### 2. **Client Status Updates**
```
You: "What's the status of client DEPT-001?"
Claude: *Calls client status API*
Result: IRAP Assessment 65% complete, next milestone due Feb 28
```

### 3. **Compliance Workflows**
```
You: "Check these 5 vendors for Essential 8 compliance"
Claude: *Automatically calls compliance API for each vendor*
Result: 2 compliant, 3 need remediation work
```

## Technical Magic

FastAPI-MCP automatically:
- **Converts your REST endpoints** → **Claude Code tools**
- **Handles authentication** and request formatting
- **Provides intelligent descriptions** of what each tool does
- **Validates inputs** using your Pydantic models
- **Returns structured data** Claude Code can reason about

## Before vs After

### Before FastAPI-MCP:
- Business logic locked in APIs
- Manual curl commands needed
- Claude Code couldn't access MOKAI systems
- No integration between AI and business processes

### After FastAPI-MCP:
- Business logic becomes AI-accessible tools
- Natural language requests work automatically
- Claude Code can perform MOKAI business tasks
- Seamless AI-business integration

## What This Means for MOKAI

You can now ask Claude Code to:
- Monitor compliance across your vendor network
- Search and filter government tenders automatically
- Generate client status reports
- Analyze business metrics and trends
- Automate procurement workflows

**All using your existing FastAPI business logic - no rewrites needed!**
