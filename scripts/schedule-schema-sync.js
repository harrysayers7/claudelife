#!/usr/bin/env node

/**
 * Schedule regular schema sync checks
 * Can be run via cron: 0 */6 * * * node scripts/schedule-schema-sync.js
 */

const { syncSchema } = require('./sync-supabase-context.js');

async function scheduledSync() {
  const now = new Date();
  console.log(`[${now.toISOString()}] Running scheduled schema sync...`);

  try {
    await syncSchema();
  } catch (error) {
    console.error('Scheduled sync failed:', error);

    // Create error notification
    const fs = require('fs').promises;
    await fs.writeFile(
      '.schema-sync-error',
      `Schema sync failed at ${now.toISOString()}\nError: ${error.message}\n`
    );
  }
}

scheduledSync();
