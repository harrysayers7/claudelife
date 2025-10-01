---
description: |
  Analyzes your project requirements based on your description
  Scans the BMad core library (agents, workflows, templates)
  Recommends the optimal setup:
    - Which workflow to use (greenfield vs brownfield, fullstack vs service vs UI)
    - Which agents you need in what order
    - Which templates are critical
    - Any config customizations needed
  Generates a new kickoff command in .claude/commands/bmad-{project-name}.md with:
    - Complete agent execution sequence
    - Step-by-step instructions
    - Template checklist
    - Project-specific configuration

examples:
  - /bmad-scan "Building a SaaS invoicing platform with Stripe integration"
  - /bmad-scan "Adding real-time notifications to existing Next.js app"
  - /bmad-scan "New Python microservice for ML model serving"

determines:
  - "Greenfield or Brownfield: Based on 'new' vs 'existing' keywords"
  - "Project type: Fullstack, Service, or UI based on description"
  - "Agent team: Which BMad agents you need and in what order"
  - "Workflow file: The exact .yaml file to follow"
---

# BMad Scan: Intelligent Project Setup Assistant

Scan the BMad Method core library to determine the optimal agents, workflows, and templates for your new project.

## Purpose

Analyze your project requirements and intelligently recommend the best BMad Method resources from `/Users/harrysayers/Developer/claudelife/.claude/.bmad-core/` to kickstart development with the right foundation.

## Usage

```bash
/bmad-scan "I want to build a SaaS dashboard with Next.js and Supabase"
/bmad-scan "Adding payment processing to existing e-commerce platform"
/bmad-scan "New microservice for user authentication"
```

## Steps

### 1. Understand Project Context

Ask clarifying questions if the description is vague:
- Is this greenfield (new) or brownfield (existing)?
- What type of project? (fullstack, frontend, backend, service)
- What's the primary goal? (MVP, feature addition, refactor, migration)
- Tech stack preferences or constraints?
- Team size and roles available?

### 2. Scan BMad Core Library

Analyze available resources in `.claude/.bmad-core/`:

**Agents** (`agents/`):
- `analyst.md` - Market research, competitor analysis, brainstorming
- `architect.md` - System design, technical architecture
- `pm.md` - Product requirements, PRD creation
- `po.md` - Product ownership, document alignment, sharding
- `ux-expert.md` - UI/UX specifications, design systems
- `dev.md` - Implementation, coding standards
- `qa.md` - Test strategies, quality gates
- `sm.md` - Sprint management, story breakdown
- `bmad-orchestrator.md` - Multi-agent coordination
- `bmad-master.md` - Overall method guidance

**Workflows** (`workflows/`):
- `greenfield-fullstack.yaml` - New full-stack applications
- `greenfield-service.yaml` - New backend services
- `greenfield-ui.yaml` - New frontend applications
- `brownfield-fullstack.yaml` - Existing full-stack projects
- `brownfield-service.yaml` - Existing backend services
- `brownfield-ui.yaml` - Existing frontend applications

**Templates** (`templates/`):
- `prd-tmpl.yaml` - Product Requirements Document
- `architecture-tmpl.yaml` - System architecture
- `project-brief-tmpl.yaml` - Initial project brief
- `front-end-spec-tmpl.yaml` - Frontend specifications
- `story-tmpl.yaml` - User story template
- `qa-gate-tmpl.yaml` - Quality checkpoints
- `market-research-tmpl.yaml` - Market analysis
- `competitor-analysis-tmpl.yaml` - Competitive landscape

### 3. Recommend BMad Setup

Based on analysis, provide:

**A. Primary Workflow**
- Which workflow file to use (greenfield vs brownfield, fullstack vs service vs UI)
- Justification for selection

**B. Agent Team Composition**
Priority order of agents needed:
1. **Phase 1 - Planning**: Analyst → PM → Architect → (optional: UX Expert)
2. **Phase 2 - Validation**: PO → QA
3. **Phase 3 - Execution**: SM → Dev → QA

**C. Key Templates**
- Which templates are critical for this project
- Suggested order of completion

**D. Customization Needs**
- Any `.bmad-core/core-config.yaml` modifications
- Custom technical documents to create

### 4. Generate Kickoff Command

Create a new slash command in `.claude/commands/` with naming pattern:
- `bmad-{project-type}-{brief-name}.md`
- Example: `bmad-fullstack-saas-dashboard.md`

The generated command should contain:

```markdown
# BMad: [Project Name]

[Brief project description]

## Project Type
[Greenfield/Brownfield] [Fullstack/Service/UI]

## Recommended BMad Workflow
Use: `.claude/.bmad-core/workflows/[selected-workflow].yaml`

## Agent Execution Sequence

### Planning Phase
1. **Analyst** (if needed for research)
   - Run: Market research, competitor analysis
   - Output: Project brief

2. **PM**
   - Create PRD from brief
   - Output: `docs/prd.md`

3. **Architect**
   - Design system architecture
   - Output: `docs/architecture.md`

4. (Optional) **UX Expert**
   - Create frontend specifications
   - Output: `docs/front-end-spec.md`

### Validation Phase
5. **PO**
   - Run master checklist
   - Shard documents
   - Output: Sharded epics/stories in `docs/prd/` and `docs/architecture/`

6. **QA**
   - Early test strategy
   - Output: `docs/qa/test-strategy.md`

### Execution Phase
7. **SM**
   - Sprint planning
   - Story breakdown

8. **Dev**
   - Implementation
   - Follow coding standards

9. **QA**
   - Test execution
   - Quality gates

## Quick Start

1. Install BMad Method to project root (if not already done)
2. Follow agent sequence above
3. Use recommended templates from `.bmad-core/templates/`
4. Reference workflow file for detailed steps

## Key Configuration

[Any specific core-config.yaml settings or customizations needed]

## Templates to Use

- [ ] [template-name-1]
- [ ] [template-name-2]
- [ ] [template-name-3]

## Notes

[Any project-specific considerations, constraints, or special requirements]
```

### 5. Provide Next Steps

After creating the kickoff command:

1. **Immediate Actions**:
   - Review generated command: `.claude/commands/bmad-[project-name].md`
   - Customize any sections as needed
   - Run the command to begin planning phase

2. **Planning Phase Checklist**:
   - [ ] Run Analyst (if market research needed)
   - [ ] Create Project Brief
   - [ ] Generate PRD with PM
   - [ ] Design Architecture
   - [ ] (Optional) UX Specifications
   - [ ] PO Document Alignment
   - [ ] PO Document Sharding

3. **Development Ready**:
   - [ ] SM Sprint Planning
   - [ ] Dev Implementation
   - [ ] QA Testing

## Example Decision Matrix

### Greenfield vs Brownfield

**Choose Greenfield** if:
- Starting from scratch
- No existing codebase
- Clean slate architecture

**Choose Brownfield** if:
- Existing codebase
- Adding features/refactoring
- Working with legacy systems

### Fullstack vs Service vs UI

**Fullstack** if:
- Frontend + Backend together
- Integrated application
- Example: SaaS dashboard, web app

**Service** if:
- Backend/API only
- Microservice architecture
- Example: Auth service, payment processor

**UI** if:
- Frontend only
- Consuming existing APIs
- Example: Admin panel, mobile web app

### Agent Selection Priority

**Always Need**:
- PM (PRD creation)
- Architect (system design)
- PO (document validation)
- Dev (implementation)

**Situational**:
- Analyst (market research for new products)
- UX Expert (complex UI requirements)
- QA (high-risk/regulated systems)
- SM (large teams, complex coordination)

## Output Format

The scan will produce:

1. **Analysis Summary**: Project type, recommended approach
2. **Resource Recommendations**: Specific workflows, agents, templates
3. **Generated Command**: New slash command file in `.claude/commands/`
4. **Next Steps**: Immediate actions to take

## Notes

- BMad Method must be installed at project root before use
- For Brownfield projects, also review `.bmad-core/working-in-the-brownfield.md`
- Workflow files are YAML-based step-by-step guides
- Agent files contain role-specific prompts and responsibilities
- Templates provide structured document formats
