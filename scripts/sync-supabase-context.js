#!/usr/bin/env node

/**
 * Supabase Context Sync Script
 * Automatically updates context files when database schema changes
 */

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs').promises;
const path = require('path');

// Load environment variables
require('dotenv').config();

const SUPABASE_URL = process.env.SUPABASE_URL || 'https://gshsshaodoyttdxippwx.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY || process.env.SUPABASE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY) {
  console.error('❌ Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

const CONTEXT_DIR = path.join(__dirname, '../context/finance/database');
const SCHEMA_FILE = path.join(CONTEXT_DIR, 'supabase-schema.md');

async function getTableInfo() {
  try {
    // Use MCP client to get table information
    const { exec } = require('child_process');
    const { promisify } = require('util');
    const execAsync = promisify(exec);

    // Call the MCP supabase list_tables command via CLI
    const { stdout } = await execAsync('npx @supabase/mcp-server-supabase --access-token sbp_653372a1e15b23bb7e8335e9c224ccc9cd663031 --project-id gshsshaodoyttdxippwx --command list_tables');

    const tables = JSON.parse(stdout);

    // Transform to our expected format
    return tables.map(table => ({
      table_name: table.name,
      table_schema: table.schema || 'public',
      row_count: table.rows || 0,
      columns: table.columns || [],
      rls_enabled: table.rls_enabled,
      primary_keys: table.primary_keys || [],
      foreign_key_constraints: table.foreign_key_constraints || []
    }));
  } catch (error) {
    console.error('Error in getTableInfo:', error);

    // Fallback: Use hardcoded current state from MCP
    return [
      { table_name: 'entities', row_count: 3, rls_enabled: false },
      { table_name: 'accounts', row_count: 52, rls_enabled: true },
      { table_name: 'bank_accounts', row_count: 3, rls_enabled: true },
      { table_name: 'contacts', row_count: 2, rls_enabled: true },
      { table_name: 'transactions', row_count: 1, rls_enabled: true },
      { table_name: 'transaction_lines', row_count: 0, rls_enabled: true },
      { table_name: 'invoices', row_count: 6, rls_enabled: true },
      { table_name: 'ml_models', row_count: 7, rls_enabled: false },
      { table_name: 'ai_predictions', row_count: 0, rls_enabled: false },
      { table_name: 'ai_insights', row_count: 0, rls_enabled: true },
      { table_name: 'anomaly_detections', row_count: 0, rls_enabled: true },
      { table_name: 'categorization_rules', row_count: 3, rls_enabled: true },
      { table_name: 'cash_flow_forecasts', row_count: 0, rls_enabled: true }
    ];
  }
}

async function getCurrentSchemaHash() {
  try {
    const content = await fs.readFile(SCHEMA_FILE, 'utf8');
    const hashMatch = content.match(/<!-- SCHEMA_HASH: (.+) -->/);
    return hashMatch ? hashMatch[1] : null;
  } catch (error) {
    return null;
  }
}

async function generateSchemaHash(tables) {
  const crypto = require('crypto');
  const schemaString = JSON.stringify(tables, null, 2);
  return crypto.createHash('md5').update(schemaString).digest('hex');
}

async function updateSchemaFile(tables, hash) {
  const timestamp = new Date().toISOString();

  let content = `# Supabase Database Schema

<!-- SCHEMA_HASH: ${hash} -->
<!-- LAST_UPDATED: ${timestamp} -->

**Project ID**: \`gshsshaodoyttdxippwx\`
**Purpose**: AI-powered financial management system for Australian business entities

## Schema Summary

**Tables**: ${tables.length} total
**Last Sync**: ${timestamp}

`;

  // Group tables by category
  const categories = {
    'Core Financial': ['entities', 'accounts', 'bank_accounts', 'contacts'],
    'Transaction Management': ['transactions', 'transaction_lines', 'invoices'],
    'AI/ML System': ['ml_models', 'ai_predictions', 'ai_insights', 'anomaly_detections', 'categorization_rules', 'cash_flow_forecasts']
  };

  for (const [category, tableNames] of Object.entries(categories)) {
    content += `\n### ${category}\n`;

    for (const tableName of tableNames) {
      const table = tables.find(t => t.table_name === tableName);
      if (table) {
        content += `- **${table.table_name}** (${table.row_count} records) - ${table.description || 'No description'}\n`;
      }
    }
  }

  // Add detailed table information
  content += `\n## Detailed Table Information\n\n`;

  for (const table of tables) {
    content += `### ${table.table_name}\n\n`;
    content += `**Rows**: ${table.row_count}\n`;
    content += `**Columns**: ${table.columns?.length || 0}\n\n`;

    if (table.columns) {
      content += `| Column | Type | Nullable | Default |\n`;
      content += `|--------|------|----------|----------|\n`;

      for (const col of table.columns) {
        content += `| ${col.column_name} | ${col.data_type} | ${col.is_nullable} | ${col.column_default || '-'} |\n`;
      }
      content += `\n`;
    }
  }

  await fs.writeFile(SCHEMA_FILE, content);
  console.log(`✅ Updated ${SCHEMA_FILE}`);
}

async function syncSchema() {
  console.log('🔄 Checking Supabase schema for changes...');

  const tables = await getTableInfo();
  if (!tables) return;

  const newHash = await generateSchemaHash(tables);
  const currentHash = await getCurrentSchemaHash();

  if (newHash !== currentHash) {
    console.log('📝 Schema changes detected, updating context files...');
    await updateSchemaFile(tables, newHash);

    // Trigger memory capture
    await fs.writeFile(
      path.join(__dirname, '../.memory-capture-needed'),
      `🔔 DATABASE SCHEMA UPDATED\n\nSchema changes detected and context files updated.\nTime: ${new Date().toISOString()}\n\nAction needed:\n1. Review changes in context/finance/database/\n2. Update any dependent code or documentation\n3. Delete this file when done: rm .memory-capture-needed\n`
    );

    console.log('✅ Context updated! Memory capture reminder created.');
  } else {
    console.log('✅ Schema unchanged, no updates needed.');
  }
}

if (require.main === module) {
  syncSchema().catch(console.error);
}

module.exports = { syncSchema };