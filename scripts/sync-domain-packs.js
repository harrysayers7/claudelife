#!/usr/bin/env node

/**
 * Domain Pack Sync Script
 * Auto-updates domain pack files when project context changes
 * Triggers: Database changes, MCP additions, workflow updates
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

const PACKS_DIR = path.join(__dirname, '../.claude/instructions');
const CONTEXT_DIR = path.join(__dirname, '../context');

// Track what contexts belong to which packs
const PACK_MAPPINGS = {
  'business-pack.md': {
    sources: [
      '01-areas/business/mokai/mokai-profile.md',
      '01-areas/business/mokhouse/mokhouse-profile.md',
      '01-areas/business/projects.md'
    ],
    triggers: ['MOKAI', 'mokai', 'cybersecurity', 'compliance', 'IRAP', 'Essential8', 'tender', 'government', 'mok house', 'music business']
  },
  'technical-pack.md': {
    sources: [
      'context/finance/database/supabase-schema.md',
      'context/finance/database/supabase-purpose.md',
      'context/finance/database/supabase-ml-pipeline.md',
      '.mcp.json'
    ],
    triggers: ['MCP', 'database', 'supabase', 'API', 'FastAPI', 'infrastructure', 'server', 'docker', 'n8n', 'FastMCP']
  },
  'automation-pack.md': {
    sources: [
      'context/automations/workflows.md',
      'context/finance/database/supabase-ml-pipeline.md',
      'scripts/sync-upbank-enhanced.js'
    ],
    triggers: ['workflow', 'automation', 'trigger', 'schedule', 'integration', 'sync', 'n8n']
  }
};

async function getFileHash(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf8');
    return crypto.createHash('md5').update(content).digest('hex');
  } catch (error) {
    return null;
  }
}

async function getCurrentPackHash(packFile) {
  try {
    const content = await fs.readFile(path.join(PACKS_DIR, packFile), 'utf8');
    const hashMatch = content.match(/<!-- PACK_HASH: (.+) -->/);
    return hashMatch ? hashMatch[1] : null;
  } catch (error) {
    return null;
  }
}

async function generatePackHash(sources) {
  const hashes = await Promise.all(
    sources.map(async (source) => {
      const fullPath = path.join(__dirname, '..', source);
      return await getFileHash(fullPath);
    })
  );
  return crypto.createHash('md5').update(hashes.join('')).digest('hex');
}

async function readSourceContent(sourcePath) {
  const fullPath = path.join(__dirname, '..', sourcePath);
  try {
    const content = await fs.readFile(fullPath, 'utf8');
    // Extract relevant sections (remove metadata comments)
    return content.replace(/<!-- .+ -->/g, '').trim();
  } catch (error) {
    console.warn(`⚠️  Could not read ${sourcePath}: ${error.message}`);
    return null;
  }
}

async function updateBusinessPack(sources, hash) {
  const timestamp = new Date().toISOString();

  // Read source contents
  const mokaiProfile = await readSourceContent(sources[0]);
  const mokhouseProfile = await readSourceContent(sources[1]);
  const projects = await readSourceContent(sources[2]);
  const businessExpenses = await readSourceContent(sources[3]);

  const content = `# Automation & Workflow Pack

<!-- PACK_HASH: ${hash} -->
<!-- LAST_UPDATED: ${timestamp} -->

**Load when**: Keywords detected - "MOKAI", "mokai", "cybersecurity", "compliance", "IRAP", "Essential8", "tender", "government", "mok house", "music business"

## MOKAI PTY LTD

${mokaiProfile || '*Profile content pending*'}

## MOK HOUSE PTY LTD

${mokhouseProfile || '*Profile content pending*'}

## Active Projects

${projects || '*Projects list pending*'}

## Financial Context

${businessExpenses || '*Business expenses tracking pending*'}
`;

  await fs.writeFile(path.join(PACKS_DIR, 'business-pack.md'), content);
  console.log('✅ Updated business-pack.md');
}

async function updateTechnicalPack(sources, hash) {
  const timestamp = new Date().toISOString();

  const schemaDoc = await readSourceContent(sources[0]);
  const purposeDoc = await readSourceContent(sources[1]);
  const mlPipeline = await readSourceContent(sources[2]);
  const mcpConfig = await readSourceContent(sources[3]);

  const content = `# Technical & Infrastructure Pack

<!-- PACK_HASH: ${hash} -->
<!-- LAST_UPDATED: ${timestamp} -->

**Load when**: Keywords detected - "MCP", "database", "supabase", "API", "FastAPI", "infrastructure", "server", "docker", "n8n", "FastMCP"

## Supabase Database

${schemaDoc || '*Schema documentation pending*'}

### Database Purpose

${purposeDoc || '*Purpose documentation pending*'}

### ML Pipeline

${mlPipeline || '*ML pipeline documentation pending*'}

## MCP Server Infrastructure

${mcpConfig ? '```json\n' + mcpConfig + '\n```' : '*MCP configuration pending*'}

## Server Infrastructure

- **Primary Server**: 134.199.159.190 (sayers-server)
- **Services**: n8n automation, Supabase database, Docker containers
- **Platform**: Ubuntu, 4 CPU, 7.8GB RAM
`;

  await fs.writeFile(path.join(PACKS_DIR, 'technical-pack.md'), content);
  console.log('✅ Updated technical-pack.md');
}

async function updateAutomationPack(sources, hash) {
  const timestamp = new Date().toISOString();

  const workflows = await readSourceContent(sources[0]);
  const mlPipeline = await readSourceContent(sources[1]);
  const upbankSync = await readSourceContent(sources[2]);

  const content = `# Automation & Workflow Pack

<!-- PACK_HASH: ${hash} -->
<!-- LAST_UPDATED: ${timestamp} -->

**Load when**: Keywords detected - "workflow", "automation", "trigger", "schedule", "integration", "sync", "n8n"

## Active Automations

${workflows || '*Workflows documentation pending*'}

## Financial ML Pipeline

${mlPipeline || '*ML pipeline documentation pending*'}

## UpBank Sync System

Enhanced sync script with error recovery and checkpoint management.

${upbankSync ? '### Implementation Details\n```javascript\n' + upbankSync.slice(0, 1000) + '\n...\n```' : '*Sync implementation pending*'}

## Workflow Patterns

### Error Recovery
- Categorized retries (network, data, system errors)
- Checkpoint system for resume capability
- State management via database

### Business Rule Automation
- Keyword matching for business expense detection
- Tax deductibility auto-flagging
- ML prediction threshold routing
`;

  await fs.writeFile(path.join(PACKS_DIR, 'automation-pack.md'), content);
  console.log('✅ Updated automation-pack.md');
}

async function syncPack(packFile, config) {
  console.log(`\n🔄 Checking ${packFile}...`);

  const newHash = await generatePackHash(config.sources);
  const currentHash = await getCurrentPackHash(packFile);

  if (newHash !== currentHash) {
    console.log('📝 Changes detected, updating pack...');

    if (packFile === 'business-pack.md') {
      await updateBusinessPack(config.sources, newHash);
    } else if (packFile === 'technical-pack.md') {
      await updateTechnicalPack(config.sources, newHash);
    } else if (packFile === 'automation-pack.md') {
      await updateAutomationPack(config.sources, newHash);
    }

    return true;
  } else {
    console.log('✅ No changes detected');
    return false;
  }
}

async function syncAllPacks() {
  console.log('🔄 Syncing domain packs with source contexts...\n');

  let updatedCount = 0;

  for (const [packFile, config] of Object.entries(PACK_MAPPINGS)) {
    const updated = await syncPack(packFile, config);
    if (updated) updatedCount++;
  }

  if (updatedCount > 0) {
    // Create memory capture reminder
    await fs.writeFile(
      path.join(__dirname, '../.domain-packs-updated'),
      `🔔 DOMAIN PACKS UPDATED\n\n${updatedCount} pack(s) updated with latest context.\nTime: ${new Date().toISOString()}\n\nUpdated packs will auto-load on next Claude session.\nDelete this file when acknowledged: rm .domain-packs-updated\n`
    );
    console.log(`\n✅ ${updatedCount} pack(s) updated! Reminder created.`);
  } else {
    console.log('\n✅ All packs up to date!');
  }
}

if (require.main === module) {
  syncAllPacks().catch(console.error);
}

module.exports = { syncAllPacks };
