# Evaluate Complexity

Intelligent assessment of whether ideas, implementations, or workflows are becoming counterproductive in the claudelife project. This command helps prevent over-engineering while ensuring business-critical functionality isn't oversimplified.

## Usage

```bash
/overkill "Adding another MCP server for GitHub notifications when we already have email alerts"
/overkill [file-path] --deep-analysis
/overkill --current-workflow="invoice processing automation"
```

## Interactive Process

When you run this command, I will:

1. **Context Identification**
   - Determine artifact type (code, config, workflow, business logic, infrastructure)
   - Identify business domain (MOKAI cybersecurity, MOK HOUSE music, personal automation, core infrastructure)
   - Assess current project phase (experimentation, stabilization, optimization, maintenance)
   - Use Graphiti to search for similar past decisions and outcomes

2. **Multi-Dimensional Evaluation**
   - **Value Analysis**: What specific problem does this solve? How much measurable value does it add?
   - **Complexity Cost**: Cognitive overhead, maintenance burden, learning curve for future developers
   - **Conflict Detection**: Does it conflict with, duplicate, or undermine existing solutions?
   - **Future Impact**: How will this affect project evolution, technical debt, business capabilities?
   - **Integration Analysis**: Using Serena MCP to understand codebase implications

3. **Business Context Weighting**
   - **MOKAI Cybersecurity**: Higher tolerance for security/compliance complexity, strict standards for client-facing features
   - **MOK HOUSE Music**: Prioritize user experience and creative workflow efficiency over technical elegance
   - **Personal Automation**: Focus on time savings vs maintenance burden ratio
   - **Core Infrastructure**: Long-term stability and maintainability over short-term convenience

4. **Pattern Recognition**
   - Search existing codebase patterns using Serena MCP
   - Check Graphiti for similar decision outcomes
   - Identify established architectural principles being followed or violated

## Evaluation Framework

### 🚨 Red Flags (Strong indicators of overkill)
- **Functional Duplication**: Replicates >80% of existing functionality without 2x improvement
- **Dependency Explosion**: Adds >3 dependencies for <20% new functionality
- **Architectural Violation**: Creates circular dependencies, tight coupling, or breaks established patterns
- **Maintenance Burden**: Requires >2 hours/week maintenance for <5 hours/week delivered value
- **Edge Case Optimization**: Only benefits <5% of actual use cases
- **Technology Proliferation**: Introduces new tech stack without compelling necessity
- **Abstraction Overkill**: Creates abstraction layers for single-use cases

### 🟡 Yellow Flags (Requires careful justification)
- **Convenience Over Necessity**: Optimizes inconvenience rather than solving real problems
- **Premature Optimization**: Solves theoretical rather than measured performance issues
- **Knowledge Silos**: Requires specialized knowledge that creates team bottlenecks
- **Reversibility Risk**: No clear rollback or simplification strategy
- **Context Mismatch**: Solution complexity doesn't match problem complexity
- **Integration Friction**: Doesn't follow established project integration patterns

### ✅ Green Signals (Likely worthwhile)
- **Frequent Pain Relief**: Solves problems encountered multiple times per week
- **Automation ROI**: Reduces manual work by >80% for common tasks
- **Pattern Compliance**: Follows and extends established project patterns
- **Measurable Success**: Has clear, trackable success metrics
- **Risk Reduction**: Improves system reliability, security, or compliance significantly
- **Business Enablement**: Unlocks new capabilities or revenue opportunities
- **Technical Debt Reduction**: Simplifies existing complexity while maintaining functionality

## Process

I'll analyze your request by:

1. **Rapid Context Assessment**
   ```
   - What category: [Code|Config|Workflow|Business Logic|Infrastructure]
   - Which domain: [MOKAI|MOK HOUSE|Personal|Core Infrastructure]
   - Current phase: [Experiment|Stabilize|Optimize|Maintain]
   ```

1. **Quick Research Phase**
   - If analyzing code, use Serena to understand current patterns: `mcp__serena__get_symbols_overview`
   - Check for existing solutions or conflicting patterns

3. **Multi-Factor Evaluation**
   ```
   Value Score: [1-10] based on problem frequency, impact, user benefit
   Complexity Score: [1-10] based on implementation, maintenance, learning curve
   Risk Score: [1-10] based on conflicts, dependencies, reversibility
   Business Fit: [1-10] based on domain priorities, project phase, resources
   ```

4. **Final Assessment**
   ```
   Overall Recommendation: [PROCEED|CAUTION|STOP]
   Confidence Level: [Low|Medium|High]
   Key Decision Factors: [Top 3 reasons for recommendation]
   ```

## Output Format

```
## Complexity Assessment: [PROCEED 🟢|CAUTION 🟡|STOP 🚨]

**Context**: [Artifact type] for [business domain] in [project phase]

**Value Analysis**:
- Problem solved: [specific description]
- Value delivered: [quantifiable benefits]
- Usage frequency: [how often this helps]

**Complexity Analysis**:
- Implementation effort: [time/complexity estimate]
- Maintenance overhead: [ongoing costs]
- Integration complexity: [conflicts with existing systems]

**Business Context Weighting**:
- Domain priorities: [how this aligns with MOKAI/MOK HOUSE/personal needs]
- Resource constraints: [team capacity, technical debt impact]
- Risk tolerance: [acceptable complexity for this domain]

**Key Decision Factors**:
1. [Most important factor]
2. [Second most important factor]
3. [Third most important factor]

**Recommendations**:
[Specific actionable advice based on assessment]

**Monitoring Suggestions**:
[How to track whether this decision was correct]

**Alternative Approaches** (if CAUTION/STOP):
[Simpler alternatives that deliver 80% of the value]
```

## Stress-Test Examples

### Example 1: MCP Server Addition
**Input**: `/overkill "Adding a dedicated MCP server for Spotify API to automatically update MOK HOUSE artist metadata in our CRM"`

**Expected Process**:
1. **Context**: Infrastructure addition for MOK HOUSE music business
2. **Graphiti Search**: Look for past MCP server decisions and their outcomes
3. **Value Analysis**: How often is artist metadata updated manually? What's the time cost?
4. **Complexity Check**: Another API to maintain, authentication to manage
5. **Business Fit**: MOK HOUSE is key revenue stream, metadata accuracy affects marketing

**Expected Output**: CAUTION 🟡 - Proceed only if manual metadata updates happen >3x/week and existing music APIs can't provide this data. Consider starting with simple webhook integration before full MCP server.

### Example 2: Workflow Over-Engineering Detection
**Input**: `/overkill scripts/complex-invoice-processor.js --deep-analysis`

**Expected Process**:
1. **Context**: Business workflow for MOKAI financial operations
2. **Serena Analysis**: Examine code complexity, dependencies, integration points
3. **Pattern Check**: Compare with other financial processing workflows
4. **Business Impact**: Invoice processing is critical for cash flow
5. **Maintenance Burden**: How complex is this to debug/modify?

**Expected Output**: Context-dependent based on actual code analysis, but would flag unnecessary complexity while respecting financial accuracy requirements.

### Example 3: Architecture Decision
**Input**: `/overkill "Implementing a custom event sourcing system for our automation workflows instead of using existing database triggers"`

**Expected Process**:
1. **Context**: Core infrastructure architectural change
2. **Research Phase**: Search for event sourcing patterns in existing codebase
3. **Complexity Assessment**: Implementation effort, team learning curve, debugging complexity
4. **Value Analysis**: What problems does event sourcing solve that triggers don't?
5. **Risk Assessment**: Migration complexity, rollback scenarios

**Expected Output**: STOP 🚨 - Event sourcing adds significant complexity. Database triggers with good logging solve 90% of audit/replay needs. Focus on incremental improvements to existing trigger system.

## Integration with Existing Tools

This command automatically leverages:
- **Serena MCP**: Code structure analysis and pattern detection
- **Context7 MCP**: Library/framework best practices research
- **Business APIs**: Understanding of MOKAI/MOK HOUSE operational context

## Success Metrics

A successful evaluation should:
1. **Be Actionable**: Provide specific next steps, not just criticism
2. **Consider Business Context**: Respect domain-specific requirements and constraints
3. **Prevent Technical Debt**: Catch complexity before it compounds
4. **Enable Smart Trade-offs**: Help balance functionality vs maintainability
5. **Learn from History**: Leverage past decisions and their outcomes

## Calibration Notes

This command will improve over time as it learns from:
- Outcomes of previous recommendations
- Evolution of project priorities
- Changes in team capacity and expertise
- New business requirements and constraints

Regular calibration against actual project outcomes ensures recommendations remain practical and valuable.


IMPORTANT: Use Serena to search through the codebase. If you get any errors using Serena, retry with different
Serena tools.
