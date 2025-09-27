Scan the claudelife repository for FastMCP API opportunities and generate use cases based on workflows, automations, and operations.

This command analyzes the codebase to identify potential FastMCP server implementations that could enhance personal and business workflows.

**Analysis Steps:**

1. **Scan Repository Structure**
   - Examine `.mcp/` directory for existing FastMCP implementations
   - Review `context/` for business and personal workflow documentation
   - Analyze `scripts/` for automation opportunities
   - Check `memory/` for knowledge graph integration points

2. **Identify FastMCP Opportunities**
   - Look for Python scripts that could be converted to FastMCP servers
   - Find automation workflows that need API endpoints
   - Discover data processing patterns that would benefit from MCP integration
   - Identify business operations requiring standardized API access

3. **Analyze Workflow Contexts**
   - **Personal workflows**: Routines, habits, productivity automation
   - **MOKAI business**: Cybersecurity operations, compliance tracking, client management
   - **Mok House business**: Creative project management, music business operations
   - **Financial operations**: Transaction processing, ML predictions, invoice handling

4. **Generate Use Cases**
   - Document each opportunity with:
     - Current implementation/manual process
     - Proposed FastMCP API design
     - Integration points with existing MCP servers
     - Workflow bundle assignment
     - Implementation priority and effort estimate

5. **Create Recommendations Document**
   - Output analysis to `MCP_OPPORTUNITIES_ANALYSIS.md`
   - Include:
     - Prioritized list of FastMCP opportunities
     - Use case specifications
     - API endpoint designs
     - Integration patterns
     - Implementation roadmap

**Key Areas to Examine:**

- **`.mcp/` directory**: Existing MCP server implementations, patterns, utilities
- **`scripts/` directory**: Automation scripts that could be MCP-enabled
- **`context/business/`**: MOKAI and Mok House workflows requiring API access
- **`context/personal/`**: Personal productivity and routine automation
- **`memory/` directory**: Knowledge graph operations and AI memory integration
- **Existing MCP servers**: Integration opportunities with current 22+ servers

**Output Format:**

Create a comprehensive analysis document similar to `MCP_BUNDLING_ANALYSIS.md` that includes:

1. **Opportunity Inventory**
   - List of identified FastMCP opportunities
   - Current state vs proposed state
   - Business/personal value proposition

2. **Recommended FastMCP Servers**
   - Server name and purpose
   - API endpoint specifications
   - Integration with existing MCP ecosystem
   - Workflow bundle assignment

3. **Use Case Specifications**
   - Detailed scenarios for each opportunity
   - User workflows enabled
   - Business operations automated
   - Personal productivity enhancements

4. **Implementation Roadmap**
   - Priority ranking (Quick Wins, High Impact, Strategic)
   - Effort estimates
   - Dependencies on existing infrastructure
   - Success metrics

**Example Opportunities to Look For:**

- Convert `sync-upbank-enhanced.js` patterns to FastMCP financial sync server
- Create FastMCP server for Graphiti knowledge graph operations
- Build FastMCP automation server for n8n workflow triggers
- Implement FastMCP context management server for domain pack loading
- Design FastMCP business intelligence server for MOKAI/Mok House metrics

Save the analysis to `MCP_OPPORTUNITIES_ANALYSIS.md` in the repository root.
