#!/usr/bin/env node

/**
 * Memory System Weekly Maintenance
 *
 * Runs weekly to:
 * 1. Prune entities older than 7 days (keep high-access count)
 * 2. Archive old conversation contexts
 * 3. Compact entity graph if needed
 * 4. Update metrics
 */

const fs = require('fs');
const path = require('path');

const ACTIVE_ENTITIES_PATH = path.join(__dirname, '../memory/active-entities.json');
const ENTITIES_PATH = path.join(__dirname, '../memory/graph/entities.json');
const CONVERSATION_CONTEXT_PATH = path.join(__dirname, '../memory/conversation-context.md');
const ARCHIVE_DIR = path.join(__dirname, '../memory/archive');

const RETENTION_DAYS = 7;
const HIGH_ACCESS_THRESHOLD = 10;

async function pruneActiveEntities() {
  console.log('📅 Pruning active entities...');

  const activeData = JSON.parse(fs.readFileSync(ACTIVE_ENTITIES_PATH, 'utf8'));
  const now = new Date();
  const cutoffDate = new Date(now - RETENTION_DAYS * 24 * 60 * 60 * 1000);

  const beforeCount = activeData.entities.length;

  // Keep entities that are either:
  // 1. Accessed within retention period, OR
  // 2. Have high access count (frequently used)
  activeData.entities = activeData.entities.filter(entity => {
    const lastAccessed = new Date(entity.last_accessed);
    const isRecent = lastAccessed > cutoffDate;
    const isHighAccess = entity.access_count >= HIGH_ACCESS_THRESHOLD;

    return isRecent || isHighAccess;
  });

  const afterCount = activeData.entities.length;
  const prunedCount = beforeCount - afterCount;

  // Update metadata
  activeData.last_updated = now.toISOString();
  activeData.pruning_log.push({
    date: now.toISOString().split('T')[0],
    pruned_count: prunedCount,
    reason: `7-day retention, kept ${afterCount} entities`
  });

  fs.writeFileSync(ACTIVE_ENTITIES_PATH, JSON.stringify(activeData, null, 2));
  console.log(`✅ Pruned ${prunedCount} entities (${afterCount} remaining)`);

  return prunedCount;
}

async function archiveOldConversations() {
  console.log('📦 Archiving old conversation contexts...');

  if (!fs.existsSync(ARCHIVE_DIR)) {
    fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  }

  const conversationContent = fs.readFileSync(CONVERSATION_CONTEXT_PATH, 'utf8');
  const now = new Date();
  const archiveFileName = `conversation-context-${now.toISOString().split('T')[0]}.md`;
  const archivePath = path.join(ARCHIVE_DIR, archiveFileName);

  // Archive current conversation context
  fs.writeFileSync(archivePath, conversationContent);

  // Reset conversation context with template
  const newContext = `# Conversation Context

**Last Updated**: ${now.toISOString().split('T')[0]}

## Current Session
- **Working on**: [To be filled by next session]
- **Loaded packs**: None yet
- **Active entities**: None yet

## Previous Session (${now.toISOString().split('T')[0]})
- **Archived**: See ${archiveFileName}

## Active Context Triggers
- "MOKAI", "cybersecurity", "compliance" → Business pack
- "MCP", "database", "API", "infrastructure" → Technical pack
- "workflow", "automation", "n8n" → Automation pack
- "music", "mok house" → Business pack

## Recent Entity Activity (7-day window)
- [Will be populated as entities are accessed]`;

  fs.writeFileSync(CONVERSATION_CONTEXT_PATH, newContext);
  console.log(`✅ Archived to ${archiveFileName}`);

  return archiveFileName;
}

async function compactEntityGraph() {
  console.log('🗜️  Checking if entity graph needs compaction...');

  const entities = JSON.parse(fs.readFileSync(ENTITIES_PATH, 'utf8'));
  const entityCount = Object.keys(entities).length;

  // Only compact if >100 entities
  if (entityCount < 100) {
    console.log(`ℹ️  Entity count (${entityCount}) below threshold, skipping compaction`);
    return false;
  }

  console.log(`📊 Entity graph has ${entityCount} entities - compaction may be needed`);
  console.log('💡 Consider manual review to archive unused entities');

  return true;
}

async function updateMetrics() {
  console.log('📈 Updating maintenance metrics...');

  const metricsPath = path.join(__dirname, '../memory/maintenance-metrics.json');
  let metrics = { runs: [] };

  if (fs.existsSync(metricsPath)) {
    metrics = JSON.parse(fs.readFileSync(metricsPath, 'utf8'));
  }

  metrics.runs.push({
    date: new Date().toISOString(),
    entities_pruned: 0, // Will be updated by actual run
    conversation_archived: true,
    compaction_needed: false
  });

  // Keep last 12 runs (3 months of weekly data)
  if (metrics.runs.length > 12) {
    metrics.runs = metrics.runs.slice(-12);
  }

  fs.writeFileSync(metricsPath, JSON.stringify(metrics, null, 2));
  console.log('✅ Metrics updated');
}

async function syncDomainPacks() {
  console.log('📦 Syncing domain packs with latest context...');

  try {
    const { syncAllPacks } = require('./sync-domain-packs.js');
    await syncAllPacks();
    return true;
  } catch (error) {
    console.error('⚠️  Domain pack sync failed:', error.message);
    return false;
  }
}

async function main() {
  console.log('🧹 Memory System Weekly Maintenance Starting...\n');

  try {
    const prunedCount = await pruneActiveEntities();
    const archiveFile = await archiveOldConversations();
    const compactionNeeded = await compactEntityGraph();
    const packsSynced = await syncDomainPacks();

    // Update metrics with actual values
    const metricsPath = path.join(__dirname, '../memory/maintenance-metrics.json');
    const metrics = JSON.parse(fs.readFileSync(metricsPath, 'utf8'));
    const lastRun = metrics.runs[metrics.runs.length - 1];
    lastRun.entities_pruned = prunedCount;
    lastRun.compaction_needed = compactionNeeded;
    fs.writeFileSync(metricsPath, JSON.stringify(metrics, null, 2));

    console.log('\n✨ Maintenance complete!\n');
    console.log('Summary:');
    console.log(`  - Entities pruned: ${prunedCount}`);
    console.log(`  - Conversation archived: ${archiveFile}`);
    console.log(`  - Compaction needed: ${compactionNeeded ? 'Yes (manual review)' : 'No'}`);
    console.log(`  - Domain packs synced: ${packsSynced ? 'Yes' : 'Failed'}`);

  } catch (error) {
    console.error('❌ Maintenance failed:', error);
    process.exit(1);
  }
}

main();
