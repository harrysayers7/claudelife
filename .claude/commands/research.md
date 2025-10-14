---
created: "2025-10-13 10:30"
description: |
  Conducts deep research on any topic using GPT Researcher MCP with optimized prompt engineering.
  Uses the COSTAR framework (Context, Objective, Style, Tone, Audience, Response) to craft
  research queries that produce comprehensive, accurate, and well-structured results.
  Capabilities:
    - Transforms user's research topic into optimized research query
    - Applies proven prompt engineering frameworks for maximum effectiveness
    - Conducts deep web research with source citations
    - Generates comprehensive reports with actionable insights
    - Automatically saves research to vault (/00-inbox/research/) with proper metadata
    - Extracts keywords, tags, and descriptions optimized for RAG retrieval
    - Suitable for business analysis, technical research, market analysis, and more
examples:
  - /research "latest developments in AI agent frameworks"
  - /research "Australian government cybersecurity compliance requirements for Indigenous businesses"
  - /research "best practices for FastAPI MCP server development 2025"
---

# Deep Research with GPT Researcher

This command conducts comprehensive research on any topic using the GPT Researcher MCP server, applying advanced prompt engineering techniques to ensure high-quality, actionable results.

## Usage

```bash
/research $ARGUMENTS
```

Where `$ARGUMENTS` is your research topic or question.

## What This Command Does

When you run this command, I will:

1. **Analyze your research topic** to understand the core question, domain, and desired outcomes
2. **Apply the COSTAR framework** to engineer an optimized research prompt:
   - **C**ontext: Background and domain knowledge needed
   - **O**bjective: Specific research goals and success criteria
   - **S**tyle: Appropriate format (analytical, comprehensive, technical)
   - **T**one: Professional and objective research approach
   - **A**udience: Tailored to your expertise level and use case
   - **R**esponse: Structured output with citations and actionable insights
3. **Conduct deep research** using `mcp__gpt-researcher__deep_research`
4. **Present findings** with proper structure, sources, and next steps

## Research Prompt Engineering Framework

Based on research into effective AI research prompting, I will optimize your query using:

### COSTAR Elements for Research

**Context (C)**: Provide domain-specific background
- Technical domain context (cybersecurity, AI, business, etc.)
- Current state of knowledge or industry standards
- Specific challenges or gaps to address
- Timeframe relevance (latest developments, historical analysis)

**Objective (O)**: Define clear research goals
- Primary question to answer
- Specific outcomes needed (decision support, implementation guide, market analysis)
- Depth level required (overview vs. deep technical analysis)
- Success criteria for useful results

**Style (S)**: Specify research approach
- Analytical with data and metrics
- Comprehensive with multiple perspectives
- Technical with implementation details
- Strategic with business implications
- Comparative analysis of options

**Tone (T)**: Set research stance
- Objective and evidence-based
- Critical analysis with pros/cons
- Forward-looking and predictive
- Practical and actionable

**Audience (A)**: Tailor complexity and focus
- Technical expert vs. business stakeholder
- Implementation team vs. decision maker
- Domain specialist vs. generalist
- Your specific claudelife context (MOKAI, automation, etc.)

**Response (R)**: Define output structure
- Executive summary with key findings
- Detailed analysis by category
- Source citations and credibility assessment
- Actionable recommendations
- Related topics for further research

### Additional Research Optimization

**Specificity**: Transform broad topics into focused research questions
- ❌ "AI trends"
- ✅ "Enterprise AI agent frameworks for production deployment in 2025: architecture patterns, security considerations, and cost analysis"

**Temporal Context**: Include timeframe when relevant
- Add "latest", "2025", "current" for recent developments
- Add "historical", "evolution" for trend analysis
- Add "future", "emerging" for predictions

**Scope Definition**: Clarify boundaries
- Geographic focus (Australian market, global trends)
- Industry vertical (fintech, cybersecurity, healthcare)
- Technical stack (Python, FastAPI, MCP)
- Business context (SMB, enterprise, government)

## Process

**IMPORTANT**: Use Serena to search through the codebase if the research relates to existing systems or integrations. If you get any errors using Serena, retry with different Serena tools.

I'll help you conduct research by:

1. **Understanding Your Research Needs**
   - Clarify your research topic and objectives
   - Identify the domain and context
   - Determine your intended use of the findings
   - Assess depth and breadth requirements

2. **Engineering the Optimal Research Prompt**
   - Apply COSTAR framework to structure the query
   - Add relevant context from claudelife project if applicable
   - Specify desired output format and structure
   - Include any domain-specific terminology or requirements

3. **Executing Deep Research**
   - Call `mcp__gpt-researcher__deep_research` with optimized prompt
   - GPT Researcher will:
     - Search multiple authoritative sources
     - Synthesize information from diverse perspectives
     - Evaluate source credibility
     - Generate comprehensive analysis

4. **Presenting Results**
   - Structured summary of key findings
   - Detailed analysis organized by theme
   - Source citations with credibility notes
   - Actionable recommendations
   - Related topics for further exploration

5. **Saving Research to Vault**
   - Create markdown file in `/Users/harrysayers/Developer/claudelife/00-inbox/research/`
   - Use template from `/Users/harrysayers/Developer/claudelife/98-templates/research.md`
   - Automatically extract and populate:
     - **research-type**: "deep research"
     - **keywords**: 5-7 specific terms optimized for RAG retrieval (technical terms, proper nouns, key concepts)
     - **tags**: 3-5 tags prioritizing existing vault tags (check relations property and vault patterns)
     - **source**: 3-5 most authoritative sources from research
     - **category**: Research domain area (e.g., ai-development, business-strategy, technical-implementation)
     - **description**: 1-2 sentence summary capturing core findings and purpose
   - Follow extraction rules from `/tag-keyword-DR-extractor` command
   - Generate filename: `{topic-slug}-{YYYY-MM-DD}.md` (e.g., `claude-code-best-practices-oct-2025.md`)

## Example Transformations

### Example 1: Technical Research

**Your input**:
```bash
/research "MCP server best practices"
```

**Optimized research prompt**:
```
Context: Model Context Protocol (MCP) is Anthropic's standard for connecting AI assistants
to external tools and data sources. FastMCP is a Python framework for building MCP servers.

Objective: Identify production-ready best practices for developing, deploying, and maintaining
MCP servers in 2025, with focus on security, reliability, performance, and developer experience.

Style: Technical analysis with code examples, architecture patterns, and implementation guidance.

Tone: Practical and authoritative, emphasizing proven production patterns over experimental approaches.

Audience: Experienced Python developer building production MCP infrastructure for AI automation systems.

Response: Structure findings as:
1. Architecture patterns (server design, state management, error handling)
2. Security best practices (authentication, authorization, data protection)
3. Deployment strategies (Docker, systemd, monitoring, health checks)
4. Performance optimization (caching, connection pooling, async patterns)
5. Developer experience (testing, debugging, documentation)
6. Real-world examples from production deployments
7. Common pitfalls and solutions
Include source citations and prioritize recently updated (2024-2025) resources.
```

### Example 2: Business Research

**Your input**:
```bash
/research "Indigenous procurement advantages Australian government"
```

**Optimized research prompt**:
```
Context: MOKAI PTY LTD is an Indigenous-owned technology consultancy in Australia focusing
on cybersecurity and government contracts. Understanding Indigenous procurement pathways
is critical for business development strategy.

Objective: Analyze current Australian government Indigenous procurement policies, frameworks,
and practical advantages for Indigenous-owned businesses competing for government technology
and cybersecurity contracts in 2025.

Style: Strategic business analysis combining policy details with practical implementation guidance.

Tone: Authoritative and actionable, emphasizing concrete opportunities and compliance requirements.

Audience: Indigenous business owner and CEO navigating government procurement landscape for
technology services.

Response: Structure findings as:
1. Key policies and frameworks (IPP, Exemption 16, Supply Nation certification)
2. Quantifiable advantages (set-asides, direct procurement thresholds, preference points)
3. Eligibility requirements and certification processes
4. Practical application to cybersecurity and IT services
5. Case studies of successful Indigenous tech contractors
6. Common compliance requirements and best practices
7. Upcoming policy changes or opportunities
Prioritize official government sources, recent policy updates (2024-2025), and practical
guidance over general information.
```

### Example 3: Technical Implementation Research

**Your input**:
```bash
/research "automated financial transaction categorization machine learning"
```

**Optimized research prompt**:
```
Context: Building automated financial management system for small business with mixed
personal/business transactions from UpBank. Need ML-based categorization with confidence
scoring to minimize manual review.

Objective: Research proven approaches for automated transaction categorization using machine
learning, including model selection, training data requirements, confidence threshold strategies,
and integration with real-time banking APIs.

Style: Technical implementation guide with architecture patterns, model comparisons, and code examples.

Tone: Practical and evidence-based, prioritizing production-ready solutions over academic research.

Audience: Full-stack developer with Python/ML experience building financial automation for SMB context.

Response: Structure findings as:
1. ML model options (classification algorithms, transformer models, embeddings)
2. Feature engineering (transaction description parsing, merchant data, temporal patterns)
3. Training data strategies (labeled datasets, active learning, transfer learning)
4. Confidence scoring and threshold optimization (auto-categorize vs. manual review)
5. Real-time integration patterns (API webhook processing, async categorization)
6. Accuracy metrics and validation approaches
7. Open-source implementations and libraries
8. Cost considerations (API costs, compute requirements)
Include recent (2024-2025) implementations and prioritize Python-based solutions.
```

## Output Format

I'll provide research results in this structure:

### 1. Executive Summary
- Key findings in 3-5 bullet points
- Primary answer to your research question
- Most important insights and recommendations

### 2. Detailed Analysis
- Organized by themes or categories
- Supporting evidence and data
- Multiple perspectives considered
- Technical details as appropriate

### 3. Source Assessment
- Number of sources consulted
- Source credibility notes
- Links to key references
- Date relevance (prioritizing recent sources)

### 4. Actionable Recommendations
- Next steps based on findings
- Implementation considerations
- Potential challenges to address
- Resources for deeper exploration

### 5. Related Research Topics
- Adjacent areas for further investigation
- Gaps in current knowledge
- Emerging trends to monitor

## Best Practices for Research Topics

### For Technical Research
- Include specific technologies/frameworks/versions
- Specify your use case or constraints
- Mention your technical stack if relevant
- Indicate production vs. experimental context

**Good examples**:
- "FastAPI MCP server authentication patterns for production deployment"
- "Supabase RLS policies for multi-tenant SaaS applications"
- "Python async patterns for long-running background tasks"

### For Business Research
- Include industry vertical and market context
- Specify geographic region if relevant
- Mention your business model or constraints
- Indicate competitive or strategic focus

**Good examples**:
- "Australian cybersecurity market opportunities for Indigenous SMBs 2025"
- "Government procurement compliance requirements for IT consultancies"
- "Pricing strategies for cybersecurity consulting services in enterprise market"

### For Market/Trend Research
- Include timeframe (current, emerging, future)
- Specify market segment or audience
- Mention decision criteria or evaluation factors
- Indicate depth needed (overview vs. deep analysis)

**Good examples**:
- "Enterprise AI automation platforms comparison: features, pricing, integration complexity"
- "Emerging trends in AI agent frameworks for production deployment 2025"
- "Email automation market analysis for professional service businesses"

## Evaluation Criteria

Successful research output should:

1. **Directly answer** your core research question with clear evidence
2. **Provide actionable insights** you can use for decisions or implementation
3. **Include credible sources** with recent, authoritative information
4. **Offer context** explaining why findings matter to your situation
5. **Identify next steps** for applying the research or investigating further
6. **Acknowledge limitations** in current knowledge or conflicting information
7. **Maintain objectivity** presenting multiple perspectives where appropriate

## Integration with Claudelife Systems

This command can research topics directly relevant to your infrastructure:

- **MCP Servers**: Research MCP patterns to improve your existing servers
- **MOKAI Business**: Research procurement, compliance, cybersecurity markets
- **Automation**: Research n8n, Trigger.dev, workflow patterns
- **AI/ML**: Research models, frameworks, integration approaches
- **Financial Systems**: Research fintech APIs, accounting automation
- **Infrastructure**: Research Docker, systemd, server management

Results can inform decisions about:
- New MCP server capabilities to build
- Business development strategies for MOKAI
- Technical architecture improvements
- Integration opportunities with existing systems
- Automation workflow enhancements

## Tips for Better Research

1. **Be specific**: "Latest FastAPI features" → "FastAPI 0.109.0 new features and migration guide"
2. **Add context**: "Cybersecurity compliance" → "Australian government cybersecurity compliance for SMBs delivering services to federal agencies"
3. **Include constraints**: "Email automation" → "Email automation for Gmail with MCP integration for personal assistant workflow"
4. **Specify use case**: "Machine learning" → "Machine learning transaction categorization for small business accounting with <1000 monthly transactions"
5. **Set timeframe**: "AI trends" → "Production-ready AI agent frameworks released or updated in 2024-2025"

## Complete Workflow Example

Here's what happens when you run `/research "Claude Code best practices"`:

1. **Query Analysis**: Topic identified as AI development tools, current timeframe needed
2. **COSTAR Optimization**: Prompt engineered with technical context, production focus, structured response
3. **Deep Research**: GPT Researcher searches 10+ sources, synthesizes findings
4. **Present Results**: Comprehensive markdown report with executive summary, 8 detailed sections, actionable recommendations
5. **Save to Vault**: Automatically creates `/00-inbox/research/claude-code-best-practices-2025-10-13.md` with:
   ```yaml
   ---
   research-type: deep research
   keywords: [claude-code-2.0, multi-agent-workflows, plan-mode, MCP-integration, subagents, git-worktrees]
   tags: [ai-development, claude-code, productivity, deep-research]
   source:
     - https://www.claudelog.com/claude-code-changelog/
     - https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
     - https://alirezarezvani.medium.com/the-complete-claude-code-2-0-0051c3ee737e
   category: research
   description: "Comprehensive analysis of Claude Code best practices as of October 2025, covering latest features, MCP integration patterns, and production-ready development strategies."
   ---
   ```

## Related Commands

- `/create-command` - Create new commands based on research findings
- `/coding:create-mcp-server` - Implement MCP servers based on technical research
- `/tag-keyword-DR-extractor` - Enhance existing research files with keywords and tags
- Use research to inform business strategy, technical decisions, and system improvements

## Notes

- Research quality depends on available online sources and their recency
- For highly specialized or proprietary topics, results may be limited
- Always validate critical findings with official documentation or expert consultation
- GPT Researcher includes source URLs for verification and deeper investigation
- This command is powered by `mcp__gpt-researcher__deep_research` which searches and synthesizes information from multiple authoritative web sources

Let me know your research topic and I'll conduct comprehensive research with optimized prompting!
