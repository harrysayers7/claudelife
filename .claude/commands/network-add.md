---
created: "2025-10-20 06:30"
updated: "2025-10-20 07:15"
version_history:
  - version: "1.1"
    date: "2025-10-20 07:15"
    changes: "Added automatic Graphiti memory integration - profiles now sync to knowledge graph"
  - version: "1.0"
    date: "2025-10-20 06:30"
    changes: "Initial creation"
description: |
  Creates a new network profile for a person or business in 04-resources/network/ and automatically adds them to Graphiti memory.
  Generates a structured markdown file with proper YAML frontmatter including:
    - Entity metadata (type, name, location, relationship strength)
    - Contact information and social links
    - Relationship context and relevance to your work
    - Capabilities/expertise breakdown
    - AI context notes for strategic reasoning
  Additionally creates a Graphiti memory entry with proper entity categorization and relationship mapping for AI-powered network reasoning.
examples:
  - /network-add "Sarah Chen from Flux Studios, creative director I met at design conference"
  - /network-add "ComplianceHub - SaaS vendor for cybersecurity compliance tracking"
  - /network-add "Michael Torres, pen testing specialist, worked together on MOKAI project"
---

# Network Add

This command helps you create a new network profile for a person or business in `04-resources/network/`, following the established profile template and metadata structure. These profiles serve as a **relational map** that AI can reference when brainstorming collaborations, business ideas, or outreach strategies.

## Usage

```bash
/network-add "brief description of person/business"
```

## Interactive Process

When you run this command, I will:

1. **Ask clarifying questions** to gather complete profile information:
   - Full name and entity type (person/business/organization)
   - Their role, company, or business focus
   - How you know them (relationship origin)
   - Relationship strength (weak/moderate/strong/key)
   - Location and contact information
   - Key capabilities or expertise
   - Current projects or affiliations
   - Relevant context for AI reasoning

2. **Confirm understanding** by presenting the gathered information

3. **Generate the profile file** in `04-resources/network/` with:
   - Proper YAML frontmatter following the profile template
   - Structured content sections (Summary, Relationship, Capabilities, etc.)
   - Date metadata (created/modified)
   - Appropriate tags and categorization

4. **Validate the output** to ensure it matches the established pattern (see `Daniel Sant.md` as reference)

5. **Add to Graphiti memory** with:
   - Comprehensive episode body containing all profile information
   - Proper entity categorization (person/business/organization)
   - Relationship mapping to existing entities (Harry Sayers, MOKAI, MOK HOUSE, SAFIA, etc.)
   - Strategic context for AI-powered network reasoning
   - Automatic knowledge graph integration

## Input Requirements

**IMPORTANT**: Use Serena to search through the codebase. If you get any errors using Serena, retry with different Serena tools.

Before running this command, have ready:
1. **Basic identification**: Name, company/role, location
2. **Relationship context**: How you met, professional/personal connection, collaboration history
3. **Contact details** (if available): Email, website, LinkedIn, other socials
4. **Expertise areas**: What they do, their skills, services they offer
5. **Strategic context**: Why they're relevant to your work (MOKAI, MOK HOUSE, personal projects)

## Process

I'll help you create a network profile by:

1. **Gathering comprehensive information** through targeted questions about:
   - Entity type (person vs. business)
   - Professional background and current role
   - Connection history and relationship strength
   - Contact information and social presence
   - Capabilities relevant to your business ecosystem

2. **Structuring YAML frontmatter** with required fields:
   ```yaml
   type: profile
   entity_type: person | business | organization
   name: Full Name
   relation: [["linked-entity-1"], ["linked-entity-2"]]
   category: industry-or-role
   location: City, Country
   tags: [relevant, tags]
   relationship:
     to_me: description-of-connection
     strength: weak | moderate | strong | key
   contact_info:
     email: email@example.com
     website: https://example.com
     socials:
       linkedin: url
       twitter: url
   aliases:
     - Common Name
     - Nickname
   date created: Day, MM DD YY, HH:MM:SS am/pm
   date modified: Day, MM DD YY, HH:MM:SS am/pm
   ```

3. **Writing structured content sections**:
   - **Summary**: Who they are, what they do, why they're relevant
   - **Relationship & Relevance**: How you know them, potential synergies
   - **Capabilities/Expertise**: Bulleted list of skills/services
   - **Links & References**: Website, socials, shared projects
   - **AI Context Notes**: Strategic reasoning context for collaboration/outreach

4. **Saving to proper location**: `04-resources/network/{Name}.md`

5. **Verifying completeness** against the profile template

6. **Creating Graphiti memory entry**:
   - Construct comprehensive episode body with all gathered information
   - Properly categorize entity type (person/business/organization)
   - Map relationships to existing entities (Harry Sayers, MOKAI, MOK HOUSE, SAFIA, etc.)
   - Include strategic context from AI Context Notes section
   - Add capability/expertise breakdown for knowledge graph
   - Reference location and relationship strength
   - Queue episode for knowledge graph processing via `mcp__graphiti__add_memory`

## Technical Implementation Guide

### File Naming Convention

```javascript
// Format: "FirstName LastName.md" for people
// Format: "Company Name.md" for businesses
const fileName = entity_type === 'person'
  ? `${firstName} ${lastName}.md`
  : `${companyName}.md`;

const filePath = `04-resources/network/${fileName}`;
```

### Frontmatter Structure

```yaml
---
type: profile                          # Always "profile"
entity_type: person                    # person | business | organization
name: Daniel Sant                      # Full name or business name
relation:                              # Wikilink arrays to related entities
  - "[[mokhouse]]"
  - "[[safia]]"
category: booking-agent                # Industry/role/function
location: Sydney                       # Primary location
tags: [music, agent, entertainment]    # Relevant tags for filtering
relationship:
  to_me: "Booking agent for SAFIA, 10+ year professional relationship turned friendship"
  strength: strong                     # weak | moderate | strong | key
contact_info:
  email: dan@cultartists.com.au
  website: https://cultartists.com.au
  socials:
    linkedin: https://linkedin.com/in/dansant
aliases:
  - Dan Sant                           # Common name variations
date created: Mon, 10 20th 25, 6:50:45 am
date modified: Mon, 10 20th 25, 6:54:27 am
---
```

### Content Structure

```markdown
# Daniel Sant

Brief introduction paragraph (1-2 sentences about who they are)

#### Background / Company Context:
Quoted or paraphrased description of their business/role

Personal context paragraph explaining the relationship and history

## 🧠 Summary
Who they are, what they do, why they're relevant to your network

## 🧭 Relationship & Relevance
How you know them, collaboration history, potential synergies with MOKAI/MOK HOUSE

## 🛠️ Capabilities / Expertise
- Skill or service 1
- Skill or service 2
- Skill or service 3

## 🔗 Links & References
- [Website](url)
- [LinkedIn](url)
- [Relevant project or document](internal-link)

## 🧠 AI Context Notes
Strategic context for AI reasoning:
- Why this person/business matters for your goals
- Potential collaboration opportunities
- Special considerations for outreach
- Receptiveness to specific types of work (AI, automation, creative, etc.)
```

### Graphiti Memory Construction

After creating the profile file, automatically construct and add a Graphiti memory entry:

```javascript
// Example Graphiti episode structure
const episodeBody = `
${name} is a ${location}-based ${category} ${entityType === 'person' ? 'professional' : 'business'} ${roleDescription}.

${relationshipContext}

${name}'s expertise includes:
${capabilities.map(cap => `- ${cap}`).join('\n')}

Relationship context:
- Relationship strength: ${relationshipStrength}
- Connection origin: ${connectionOrigin}
- Current status: ${currentStatus}
- Location: ${location}

Strategic relevance to ${relevantEntities.join(', ')}:
${strategicContext}

${collaborationScenarios}

Related entities: ${relatedEntities.join(', ')}.
`;

await mcp__graphiti__add_memory({
  name: `${name} - ${category} Network Addition`,
  episode_body: episodeBody,
  source: "text",
  source_description: "network profile addition"
});
```

## Output Format

I'll provide:

1. **Confirmation summary** of gathered information before file creation
2. **Complete profile file** at `04-resources/network/{Name}.md`
3. **Validation check** confirming all required fields are populated
4. **Suggested tags and relations** based on the profile context
5. **Graphiti memory confirmation** showing the episode was queued for processing
6. **Next steps** for integrating this profile into your network map

## Examples

### Example 1: Adding a Person (Business Contact)

**Input**: `/network-add "Sarah Chen, creative director at Flux Studios, met at Sydney Design Conference"`

**Interactive Process**:
```
Q: Is Sarah Chen a person or business entity?
A: Person

Q: What's Sarah's current role and company?
A: Creative Director at Flux Studios

Q: How would you describe your relationship?
A: Met at Sydney Design Conference 2024, discussed potential collaboration on branding projects

Q: What's the relationship strength?
A: Moderate (new connection, mutual interest)

Q: What are Sarah's key capabilities relevant to your work?
A: - Visual identity and branding
    - Boutique fashion label design
    - Strong Melbourne design network
    - Interest in AI-generated branding

Q: Any contact information?
A: Email: sarah@fluxstudios.com.au, Website: fluxstudios.com.au

Q: Location?
A: Melbourne, Australia

Q: Any AI context notes for strategic reasoning?
A: Highly interested in AI-generated branding and automation tools for creative workflows. Likely receptive to joint offers involving AI + design. Could pair well with MOK HOUSE's sonic branding services.
```

**Output File** (`04-resources/network/Sarah Chen.md`):
```markdown
---
type: profile
entity_type: person
name: Sarah Chen
relation:
  - "[[mokhouse]]"
  - "[[flux-studios]]"
category: creative-director
location: Melbourne, Australia
tags: [design, branding, AI-creative, fashion]
relationship:
  to_me: "Met at Sydney Design Conference 2024, discussed potential collaboration on branding and AI-creative projects"
  strength: moderate
contact_info:
  email: sarah@fluxstudios.com.au
  website: https://fluxstudios.com.au
  socials:
aliases:
  - Sarah
date created: Mon, 10 20th 25, 6:30:00 am
date modified: Mon, 10 20th 25, 6:30:00 am
---

# Sarah Chen

Creative director and founder of Flux Studios in Melbourne

#### Background:
Sarah Chen is a creative director and founder of Flux Studios. She works primarily with boutique fashion labels and has a strong network in the Melbourne design scene.

Met at Sydney Design Conference 2024 where we discussed the intersection of AI and creative branding.

## 🧠 Summary
Sarah is a Melbourne-based creative director specializing in visual identity and branding for boutique fashion labels. She has a strong design network and is actively exploring AI-generated branding tools.

## 🧭 Relationship & Relevance
Met at Sydney Design Conference 2024 during a panel on AI in creative industries. We discussed potential collaboration opportunities combining her visual branding expertise with MOK HOUSE's sonic branding services. She's interested in automation tools for creative workflows.

## 🛠️ Capabilities / Expertise
- Visual identity and brand design
- Boutique fashion label design
- Creative direction for luxury brands
- Melbourne design network access
- AI-creative experimentation

## 🔗 Links & References
- [Flux Studios Website](https://fluxstudios.com.au)
- [LinkedIn](https://linkedin.com/in/sarahchen)

## 🧠 AI Context Notes
Sarah is highly interested in AI-generated branding and is actively exploring automation tools for creative workflows. She's likely receptive to joint offers involving AI + design services.

**Potential synergies**:
- Combining visual identity (Flux) + sonic branding (MOK HOUSE)
- AI-assisted branding projects leveraging both design and sound
- Fashion label clients needing holistic brand experiences
- Co-marketing around AI-creative innovation

**Outreach strategy**: Lead with AI/automation angle, position as innovation partnership rather than traditional vendor relationship.
```

**Graphiti Memory Output**:
```
✅ Added Sarah Chen to Graphiti memory!
Episode "Sarah Chen - Creative Director Network Addition" queued for processing (position: 1)
```

### Example 2: Adding a Business Entity

**Input**: `/network-add "ComplianceHub - SaaS vendor for cybersecurity compliance tracking, potential MOKAI integration"`

**Interactive Process**:
```
Q: Is ComplianceHub a person or business entity?
A: Business

Q: What does ComplianceHub do?
A: SaaS platform for cybersecurity compliance tracking and reporting

Q: How did you discover them?
A: Researched during MOKAI service offering development

Q: What's the relationship strength?
A: Weak (no direct contact yet, potential vendor/partner)

Q: Key capabilities relevant to MOKAI?
A: - Automated compliance tracking
    - IRAP assessment workflows
    - Government reporting templates
    - Integration APIs

Q: Any contact information?
A: Website: compliancehub.com.au

Q: Location?
A: Canberra, Australia

Q: Strategic context for AI?
A: Potential integration partner for MOKAI's compliance services. Could automate client reporting and reduce manual compliance tracking workload. May offer partnership/affiliate opportunities for government clients.
```

**Output File** (`04-resources/network/ComplianceHub.md`):
```markdown
---
type: profile
entity_type: business
name: ComplianceHub
relation:
  - "[[mokai]]"
category: cybersecurity-saas
location: Canberra, Australia
tags: [compliance, IRAP, government, saas, automation]
relationship:
  to_me: "Identified during MOKAI service offering development as potential integration partner"
  strength: weak
contact_info:
  email:
  website: https://compliancehub.com.au
  socials:
aliases:
  - Compliance Hub
date created: Mon, 10 20th 25, 6:35:00 am
date modified: Mon, 10 20th 25, 6:35:00 am
---

# ComplianceHub

SaaS platform for cybersecurity compliance tracking and reporting

#### Website blurb:
"ComplianceHub automates cybersecurity compliance workflows for Australian government and enterprise organizations. Purpose-built for IRAP assessments, Essential Eight reporting, and continuous compliance monitoring."

Identified during MOKAI service offering development as a potential integration partner to automate client compliance tracking.

## 🧠 Summary
ComplianceHub is a Canberra-based SaaS vendor specializing in cybersecurity compliance automation, particularly for Australian government requirements (IRAP, Essential Eight). They provide workflow automation and reporting tools that could complement MOKAI's consulting services.

## 🧭 Relationship & Relevance
No direct relationship yet. Discovered during research for MOKAI's compliance service automation. They offer APIs and integration capabilities that could reduce manual tracking workload for MOKAI's IRAP assessment clients.

**Potential partnership model**: Recommend ComplianceHub to clients → receive affiliate/referral fee → reduce MOKAI's post-assessment support burden.

## 🛠️ Capabilities / Expertise
- Automated compliance tracking and monitoring
- IRAP assessment workflow automation
- Essential Eight maturity reporting
- Government compliance templates (ISM, PSPF)
- Integration APIs for cybersecurity tools
- Continuous compliance dashboards

## 🔗 Links & References
- [ComplianceHub Website](https://compliancehub.com.au)
- [API Documentation](https://docs.compliancehub.com.au)

## 🧠 AI Context Notes
**Strategic value for MOKAI**:
- Automate post-assessment compliance tracking for clients
- Reduce manual reporting workload
- Differentiate MOKAI offering with "ongoing compliance automation"
- Potential white-label or partnership arrangement

**Next steps**:
1. Reach out to ComplianceHub partnership team
2. Test their API for MOKAI client use case
3. Evaluate affiliate vs. reseller vs. white-label models
4. Build integration for MOKAI client onboarding flow

**Positioning**: Position MOKAI as expert implementation partner who helps clients get value from ComplianceHub (not just software vendor).
```

**Graphiti Memory Output**:
```
✅ Added ComplianceHub to Graphiti memory!
Episode "ComplianceHub - Cybersecurity SaaS Network Addition" queued for processing (position: 1)
```

## Evaluation Criteria

A successful network profile should:

1. **Complete frontmatter** with all required YAML fields populated
2. **Accurate entity classification** (person vs. business)
3. **Clear relationship context** explaining how you know them and why they matter
4. **Specific capabilities** listed in actionable bullet points
5. **Strategic AI context** that helps reason about collaboration opportunities
6. **Proper date formatting** matching Obsidian convention (Day, MM DD YY, HH:MM:SS am/pm)
7. **Relevant relations** linked to existing entities (MOKAI, MOK HOUSE, etc.)
8. **Appropriate tags** for filtering and discovery
9. **Relationship strength** accurately categorized (weak/moderate/strong/key)
10. **Contact information** captured where available

## Related Resources

- Template: `98-templates/profile.md`
- Example profile: `04-resources/network/Daniel Sant.md`
- Network context: `04-resources/network/CLAUDE.md`
- Related entities to link: `[[mokai]]`, `[[mokhouse]]`, `[[safia]]`

## Post-Creation Steps

After creating the profile:

1. **Review the file** in Obsidian to ensure proper rendering
2. **Verify Graphiti memory** was queued successfully (confirmation message displayed)
3. **Add cross-links** if this person/business relates to existing profiles
4. **Update related entity files** (e.g., add to MOKAI's network if relevant)
5. **Tag appropriately** for filtering in Dataview queries
6. **Consider creating a project** if collaboration is imminent

The profile is now available in both:
- **Markdown format**: `04-resources/network/{Name}.md` for manual reference
- **Graphiti knowledge graph**: Automatically integrated for AI-powered network reasoning

---

**Ready to add a network profile. Please provide:**
- Name and brief description of the person/business
- Basic context about how you know them or why they're relevant

I'll guide you through gathering the rest of the information interactively.
