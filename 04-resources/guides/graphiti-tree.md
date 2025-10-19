---
date: "2025-10-19"
---
# Graphiti Knowledge Graph Structure

**Last Updated**: 2025-10-19
**Total Entities**: 23
**Total Relations**: 19

This document provides a visual representation of the Graphiti knowledge graph structure without exposing actual knowledge content.

---

## Entity Type Hierarchy

```
Knowledge Graph Root

   👤 Person (4 entities)
      Harrison Robert Sayers
      Kell Mendoza
      Kate Stenhouse
      Glenn Sarangapany

   🏢 Business (2 entities)
      MOK HOUSE
      MOKAI

   📊 Business Division (2 entities)
      MOK Music
      MOK Studio

   🤝 Client (1 entity)
      Electric Sheep Music

   🏛️ Business Entity (3 entities)
      MOK HOUSE PTY LTD
      MOKAI PTY LTD
      SAFIA Unit Trust

   💰 Financial Domain (2 entities)
      CRYPTO
      SMSF

   📅 Life Domain (2 entities)
      ADMIN
      PERSONAL

   💻 Professional Domain (1 entity)
      DEVELOPER

   ❤️ Personal (1 entity)
      SAFIA

   🚗 Asset (1 entity)
      Tesla Model 3

   📝 Tax Deduction (1 entity)
      Home Office Deductions

   📈 Financial Data (1 entity)
      Personal Cash Flow Oct 2025

   🔧 Infrastructure (1 entity)
      Supabase Financial Database

   🧪 Test (1 entity)
      Test Entity for Issue Tracking
```

---

## Relationship Structure

### Core Ownership & Control
```
Harrison Robert Sayers
   owns → MOK HOUSE
   owns → MOKAI
   works_with_as_composer → Electric Sheep Music
   owns and operates as CEO → MOK HOUSE PTY LTD
   owns and operates as CEO → MOKAI PTY LTD
   is member and beneficiary of → SAFIA Unit Trust
   owns and uses for business → Tesla Model 3
   is eligible for → Home Office Deductions

Kell Mendoza
   is_director_of → MOK HOUSE
```

### Business Structure
```
MOK HOUSE
   has_division → MOK Music
   has_division → MOK Studio

MOK Music
   has_client → Electric Sheep Music
```

### Client Organization
```
Electric Sheep Music
   ← works_at_as_EP (Kate Stenhouse)
   ← works_at_as_creative_director (Glenn Sarangapany)
```

### Financial Infrastructure
```
Supabase Financial Database
   ← financial data stored in (MOK HOUSE PTY LTD)
   ← financial data stored in (MOKAI PTY LTD)
   ← financial data stored in (SAFIA Unit Trust)
   ← tracked in (Personal Cash Flow Oct 2025)

Tesla Model 3
   complements as business expense → Home Office Deductions
```

---

## Entity Statistics by Type

| Entity Type          | Count | Percentage |
|---------------------|-------|------------|
| Person              | 4     | 17.4%      |
| Business Entity     | 3     | 13.0%      |
| Business            | 2     | 8.7%       |
| Business Division   | 2     | 8.7%       |
| Financial Domain    | 2     | 8.7%       |
| Life Domain         | 2     | 8.7%       |
| Client              | 1     | 4.3%       |
| Professional Domain | 1     | 4.3%       |
| Personal            | 1     | 4.3%       |
| Asset               | 1     | 4.3%       |
| Tax Deduction       | 1     | 4.3%       |
| Financial Data      | 1     | 4.3%       |
| Infrastructure      | 1     | 4.3%       |
| Test                | 1     | 4.3%       |
| **Total**           | **23** | **100%**   |

---

## Relationship Statistics

| Relationship Type                      | Count |
|---------------------------------------|-------|
| owns                                  | 2     |
| has_division                          | 2     |
| financial data stored in              | 3     |
| owns and operates as CEO              | 2     |
| works_at_as_EP                        | 1     |
| works_at_as_creative_director         | 1     |
| works_with_as_composer                | 1     |
| has_client                            | 1     |
| is_director_of                        | 1     |
| is member and beneficiary of          | 1     |
| owns and uses for business            | 1     |
| is eligible for                       | 1     |
| tracked in                            | 1     |
| complements as business expense       | 1     |
| **Total**                             | **19** |

---

## Network Density Analysis

- **Most Connected Entity**: Harrison Robert Sayers (8 outgoing relationships)
- **Hub Entities**:
  - Harrison Robert Sayers (8 relationships)
  - Supabase Financial Database (4 relationships)
  - MOK HOUSE (3 relationships)
  - Electric Sheep Music (3 relationships)
- **Isolated Entities**: 4 entities have no relationships (CRYPTO, SMSF, ADMIN, PERSONAL, DEVELOPER, SAFIA, Test Entity for Issue Tracking)

---

## Domain Coverage

### Business & Professional (12 entities - 52.2%)
- Business operations and structure
- Client relationships
- Professional activities
- Business entities and divisions

### Financial & Assets (8 entities - 34.8%)
- Investment and wealth management
- Tax deductions and compliance
- Cash flow tracking
- Infrastructure and assets

### Personal & Life (3 entities - 13.0%)
- Personal relationships
- Life domains and organization
- Admin and personal development

---

## Growth Recommendations

Based on current structure, consider expanding:

1. **Client Network**: Only 1 client entity (Electric Sheep Music) tracked
   - **Action**: Add more MOK Music clients (agencies, brands, government departments)
   - **Example**: Create entities for Nintendo, GWM, Panda Candy, other ESM projects

2. **MOKAI Business Context**: MOKAI entity exists but has minimal operational detail
   - **Action**: Add MOKAI clients, contractors, service offerings
   - **Example**: Create entities for government departments, cybersecurity contractors, IRAP/E8 services

3. **Project/Campaign Entities**: No project-level tracking yet
   - **Action**: Add specific campaigns as entities (Nintendo Exchange Mode, GWM Tank 500)
   - **Benefit**: Track creative patterns, winning strategies, project financials

4. **Personal Relationships**: SAFIA and other personal connections are isolated
   - **Action**: Add relationships to relevant life domains or projects
   - **Example**: Link personal entities to personal development goals

5. **Financial Investment Details**: CRYPTO and SMSF have no connections
   - **Action**: Add specific investment holdings, goals, or strategies
   - **Example**: Create entities for specific crypto holdings, SMSF investment strategy

6. **Clean Up Test Data**: Remove "Test Entity for Issue Tracking" (no longer needed)

---

## Usage Notes

- This structure represents the **current state** of the Graphiti knowledge graph
- Entities contain observations (factual data points) not shown here
- Relationships are directional (from → to)
- Use `mcp__memory__*` tools to query, add, or modify entities
- Isolated entities (no relationships) may need connections for better knowledge retrieval

---

## Query Patterns

### Find all business entities:
```javascript
mcp__memory__search_nodes({ query: "Business" })
```

### Find Harrison's relationships:
```javascript
mcp__memory__open_nodes({ names: ["Harrison Robert Sayers"] })
```

### Add new client:
```javascript
mcp__memory__create_entities({
  entities: [{
    name: "New Client Name",
    entityType: "Client",
    observations: ["Client details..."]
  }]
})

mcp__memory__create_relations({
  relations: [{
    from: "MOK Music",
    to: "New Client Name",
    relationType: "has_client"
  }]
})
```

### Find financial data:
```javascript
mcp__memory__search_nodes({
  query: "financial data invoices cash flow",
  entity: "Financial Data"
})
```

---

## Changelog

### 2025-10-19 (Current Update)

**Added Entities** (+8):
- Business Entity: MOK HOUSE PTY LTD, MOKAI PTY LTD, SAFIA Unit Trust
- Asset: Tesla Model 3
- Tax Deduction: Home Office Deductions
- Financial Data: Personal Cash Flow Oct 2025
- Infrastructure: Supabase Financial Database
- Test: Test Entity for Issue Tracking

**Added Relationships** (+10):
- Harrison Robert Sayers → owns and operates as CEO → MOK HOUSE PTY LTD
- Harrison Robert Sayers → owns and operates as CEO → MOKAI PTY LTD
- Harrison Robert Sayers → is member and beneficiary of → SAFIA Unit Trust
- Harrison Robert Sayers → owns and uses for business → Tesla Model 3
- Harrison Robert Sayers → is eligible for → Home Office Deductions
- MOK HOUSE PTY LTD → financial data stored in → Supabase Financial Database
- MOKAI PTY LTD → financial data stored in → Supabase Financial Database
- SAFIA Unit Trust → financial data stored in → Supabase Financial Database
- Personal Cash Flow Oct 2025 → tracked in → Supabase Financial Database
- Tesla Model 3 → complements as business expense → Home Office Deductions

**Statistics**:
- Total entities: 15 → 23 (+8, +53.3%)
- Total relationships: 9 → 19 (+10, +111.1%)
- Isolated entities: 6 → 4 (-2, improved connectivity)
- New entity types: Business Entity, Asset, Tax Deduction, Financial Data, Infrastructure, Test

**Key Improvements**:
- ✅ Financial infrastructure now mapped (Supabase as central hub)
- ✅ Business entities distinguished from conceptual businesses
- ✅ Tax optimization opportunities tracked (Tesla, Home Office)
- ✅ Cash flow data connected to infrastructure
- ⚠️ Still missing: Client projects, MOKAI operational detail, personal relationship connections

---

**Last synchronized**: 2025-10-19
