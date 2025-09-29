// HTTP wrapper for UpBank sync
// Save as: scripts/http-sync.js

const express = require('express');
const { execSync } = require('child_process');
const app = express();

app.post('/sync', async (req, res) => {
  try {
    const result = execSync('node scripts/sync-upbank-data.js full', {
      cwd: '/Users/harrysayers/Developer/claudelife',
      encoding: 'utf8',
      timeout: 300000
    });

    res.json({
      success: true,
      output: result,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

app.listen(3001, () => {
  console.log('Sync HTTP server running on port 3001');
});
