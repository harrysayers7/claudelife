---
description: Update Serena MCP's memory with MOKAI business context after adding services, clients, or compliance changes
tags: [mokai, serena, memory, business, compliance, cybersecurity]
---

# Update MOKAI Context in Serena

Update Serena MCP's memory to reflect changes in MOKAI business operations, services, compliance frameworks, or client engagements.

## Usage

```bash
/mokai:update-context
/mokai:update-context [what-changed]
```

## When to Use

Run this command after:
- ✅ Adding new cybersecurity services (pen testing, IRAP, GRC)
- ✅ Onboarding new clients or completing projects
- ✅ Updating compliance frameworks (Essential 8, ISO 27001, SOC2)
- ✅ Adding vendor partnerships or technology solutions
- ✅ Creating new MOKAI-specific slash commands or workflows
- ✅ Changing business processes or delivery models
- ✅ Updating Indigenous procurement positioning (IPP, Supply Nation)

## MOKAI-Specific Memory Categories

### 1. Services & Capabilities
What MOKAI offers and how we deliver:
- Cybersecurity services (pen testing, vulnerability assessments, architecture reviews)
- GRC consulting (IRAP, Essential 8, compliance frameworks)
- Technology solution delivery (prime contractor model)
- Managed services and continuous compliance

### 2. Client Context
Active engagements and delivery patterns:
- Government agencies and enterprise clients
- Project types and common engagement models
- Success stories and case studies
- Client-specific compliance requirements

### 3. Compliance Frameworks
Technical expertise and certification knowledge:
- IRAP assessment processes and requirements
- Essential 8 maturity levels and controls
- ISO 27001, SOC2, NIST frameworks
- Government procurement requirements (AusTender, IPP policies)

### 4. Indigenous Business Context
Unique market positioning:
- Indigenous ownership and Supply Nation certification
- Direct procurement eligibility (IPP, Exemption 16)
- Cultural capability and Indigenous employment
- Partnership and subcontracting approaches

### 5. Technology Stack & Tools
Platforms and solutions MOKAI works with:
- Security tools and technologies
- Vendor partnerships and preferred solutions
- Internal automation and operations tools
- Client delivery platforms

### 6. Business Operations
How MOKAI runs day-to-day:
- Prime contractor delivery model
- Subcontractor management and vetting
- Quality assurance and compliance processes
- Financial management and invoicing workflows

## Execution Steps

### Step 1: Identify What Changed

Ask clarifying questions:
- "What new MOKAI service or capability was added?"
- "Did we onboard a new client or complete a project?"
- "Were compliance frameworks or certifications updated?"
- "Did we add new vendor partnerships or technology solutions?"
- "Are there new business processes or delivery models?"

### Step 2: Read Current Memory State

```javascript
mcp__serena__list_memories()

// Read relevant business memory
mcp__serena__read_memory({
  memory_name: "suggested_commands"
})

mcp__serena__read_memory({
  memory_name: "system_patterns_and_guidelines"
})
```

### Step 3: Update Relevant Memories

#### Example: New Cybersecurity Service

```javascript
mcp__serena__write_memory({
  memory_name: "system_patterns_and_guidelines",
  content: `
# System Patterns and Guidelines

[... existing content ...]

## MOKAI Business Operations

### Cybersecurity Services
- **Penetration Testing**: External/internal network testing, web app testing, cloud security assessments
- **IRAP Assessments**: Information Security Registered Assessors Program for government systems
- **Vulnerability Assessments**: Automated and manual vulnerability identification
- **Security Architecture Reviews**: Design validation against Essential 8 and ISO 27001
- **Cloud Security Audits**: AWS, Azure, GCP security posture assessments (NEW)

### Service Delivery Model
- Prime contractor model: MOKAI manages compliance, insurance, quality
- Subcontractor network: Vetted cybersecurity specialists
- Single point of accountability for clients
- Direct procurement eligibility via Indigenous participation policies

[... rest of content ...]
  `
})
```

#### Example: New Client Engagement

```javascript
mcp__serena__write_memory({
  memory_name: "project_overview",
  content: `
# Project Overview

[... existing content ...]

## MOKAI - Indigenous Technology Consultancy

### Active Client Engagements
- **Department of Defence**: IRAP assessment for classified systems
- **NSW Government Agency**: Essential 8 maturity improvement program (NEW)
- **Enterprise Healthcare**: ISO 27001 compliance roadmap (NEW)

### Common Engagement Patterns
- Initial security assessment (2-4 weeks)
- Remediation planning and implementation (3-6 months)
- Continuous compliance monitoring (ongoing)
- Annual security reviews and updates

[... rest of content ...]
  `
})
```

#### Example: New Compliance Framework

```javascript
mcp__serena__write_memory({
  memory_name: "tech_stack",
  content: `
# Tech Stack

[... existing content ...]

## MOKAI Compliance Frameworks

### Government Requirements
- **IRAP**: Information Security Registered Assessors Program
- **Essential 8**: ASD's baseline security strategies
- **ISM**: Information Security Manual (Australian Government)
- **PSPF**: Protective Security Policy Framework (NEW)

### International Standards
- **ISO 27001**: Information security management
- **SOC2**: Service organization controls
- **NIST CSF**: Cybersecurity framework (NEW)

### Assessment Tools
- ACSC Essential 8 Assessment Tool
- ISO 27001 compliance checkers
- Custom GRC platforms for client reporting

[... rest of content ...]
  `
})
```

#### Example: New Slash Commands or Workflows

```javascript
mcp__serena__write_memory({
  memory_name: "suggested_commands",
  content: `
# Suggested Commands

[... existing content ...]

## MOKAI Business Operations

### Client Management
- /mokai:new-client - Onboard new MOKAI client with compliance setup
- /mokai:project-status - Check status of active cybersecurity engagements
- /mokai:compliance-check - Verify client meets Essential 8/IRAP requirements

### Vendor & Partner Management
- /mokai:check-vendor-compliance - Verify subcontractor meets MOKAI standards
- /mokai:add-vendor - Onboard new technology vendor or subcontractor

### Tender & Procurement
- /mokai:search-tenders - Find relevant AusTender opportunities
- /mokai:tender-response - Generate tender response using Indigenous procurement positioning

### Financial Operations
- /mokai:invoice-client - Create invoice for completed cybersecurity work
- /mokai:revenue-dashboard - View MOKAI financial metrics and pipeline

[... rest of content ...]
  `
})
```

### Step 4: Update Business API Context

If changes affect the FastAPI Business MCP server:

```javascript
mcp__serena__write_memory({
  memory_name: "tech_stack",
  content: `
# Tech Stack

[... existing content ...]

## MCP Servers

### claudelife-business-api (FastAPI)
Endpoints for MOKAI business operations:
- GET /api/vendor-compliance/{vendor_name} - Check vendor IRAP/Essential8 status
- GET /api/tenders/search - Search AusTender for relevant opportunities
- GET /api/business/metrics - MOKAI revenue, pipeline, KPIs
- GET /api/clients/{client_id}/projects - Client project status
- POST /api/clients - Create new client with compliance setup (NEW)

Usage in slash commands:
- /mokai:check-vendor-compliance uses vendor-compliance endpoint
- /mokai:search-tenders uses tenders/search endpoint
- /mokai:revenue-dashboard uses business/metrics endpoint

[... rest of content ...]
  `
})
```

### Step 5: Verify Updates

```javascript
// Confirm updates were saved
mcp__serena__read_memory({
  memory_name: "system_patterns_and_guidelines"
})

mcp__serena__read_memory({
  memory_name: "suggested_commands"
})
```

## Common Update Scenarios

### Scenario 1: New IRAP Assessment Capability

```
Changes:
- Added PROTECTED-level IRAP assessment capability
- Requires certified IRAP assessors on team
- New compliance documentation requirements

Memories to update:
✅ system_patterns_and_guidelines - Add IRAP PROTECTED service details
✅ suggested_commands - Add /mokai:irap-assessment command
✅ tech_stack - Add IRAP assessment tools and frameworks
```

### Scenario 2: Government Tender Win

```
Changes:
- Won Department of Defence cybersecurity contract
- New client engagement pattern for classified systems
- Additional compliance requirements (security clearances)

Memories to update:
✅ project_overview - Add Defence as active client
✅ system_patterns_and_guidelines - Document classified system workflows
✅ suggested_commands - Add /mokai:classified-project-setup command
```

### Scenario 3: New Technology Partnership

```
Changes:
- Partnership with major SIEM vendor (e.g., Splunk, Microsoft Sentinel)
- Can now deliver managed SIEM services
- New revenue stream and service offering

Memories to update:
✅ system_patterns_and_guidelines - Add managed SIEM service delivery model
✅ tech_stack - Add SIEM platforms to technology stack
✅ suggested_commands - Add /mokai:siem-deployment command
```

### Scenario 4: Indigenous Procurement Update

```
Changes:
- Updated Supply Nation certification (Silver → Gold)
- New direct procurement thresholds
- Enhanced Indigenous employment targets

Memories to update:
✅ project_overview - Update Indigenous business credentials
✅ system_patterns_and_guidelines - Update procurement positioning
✅ suggested_commands - Update /mokai:tender-response with new credentials
```

## Interactive Mode

When run without arguments, guide the user through:

1. **Detect recent changes**
   ```bash
   # Check for new MOKAI-related files
   git log --since="7 days ago" --name-only | grep -i "mokai\|irap\|essential"

   # Check for new business slash commands
   ls .claude/commands/business/mokai/

   # Check FastAPI business server changes
   git diff HEAD~5 -- '*business*api*'
   ```

2. **Ask clarifying questions**
   - "What MOKAI service or capability changed?"
   - "Is this related to a new client, vendor, or partnership?"
   - "Does this affect compliance frameworks or certifications?"
   - "Should slash commands or automation be updated?"

3. **Suggest memory updates**
   Based on responses, recommend specific memories to update

4. **Execute updates**
   Update each identified memory category with new MOKAI context

5. **Verify and confirm**
   Show updated memory sections and confirm accuracy

## Integration with Other Commands

### After Creating New MOKAI Slash Command

```bash
# 1. Create the new command
/create-command "mokai:irap-assessment"

# 2. Update Serena's memory
/mokai:update-context "Added new IRAP assessment command"

# 3. Document the system (if major feature)
/document-system "MOKAI IRAP Assessment Workflow"
```

### After Onboarding New Client

```bash
# 1. Add client via Business API or Notion
mcp__claudelife-business-api__create_client(...)

# 2. Update Serena's memory
/mokai:update-context "New client: Department of Defence IRAP engagement"

# 3. Set up project tracking
/mokai:new-client "Department of Defence"
```

### After Compliance Framework Update

```bash
# 1. Update documentation
# Edit 01-areas/business/mokai/docs/compliance/essential8.md

# 2. Update Serena's memory
/mokai:update-context "Updated Essential 8 framework to v3.6"

# 3. Update related slash commands
# Review and update /mokai:compliance-check if needed
```

## Best Practices

1. **Update immediately** - Don't let MOKAI context become stale
2. **Be business-specific** - Include client names, compliance details, service specifics
3. **Link to documentation** - Reference MOKAI docs in 01-areas/business/mokai/
4. **Maintain consistency** - Use same terminology as business documents
5. **Think about slash commands** - Update suggested_commands when new workflows emerge

## Quarterly Review Checklist

Run `/mokai:update-context` quarterly to review:

- [ ] Active client list and engagement types
- [ ] Services and capabilities offered
- [ ] Compliance frameworks and certifications
- [ ] Vendor partnerships and technology stack
- [ ] Indigenous procurement credentials
- [ ] Slash commands and automation workflows
- [ ] Revenue metrics and business model updates

## Related Commands

- `/update-serena-memory` - General Serena memory updates
- `/document-system` - Create comprehensive MOKAI system documentation
- `/mokai:revenue-dashboard` - View current MOKAI business metrics
- `/mokai:check-vendor-compliance` - Verify vendor compliance status
- `/generate-mokai-flashcards` - Create learning flashcards from MOKAI research

## Notes

- MOKAI context lives in multiple memories: `suggested_commands`, `system_patterns_and_guidelines`, `project_overview`, `tech_stack`
- Always maintain Indigenous business positioning in updates
- Link MOKAI services to compliance frameworks for context
- Update FastAPI Business MCP server documentation when endpoints change
