---
date created: Mon, 09 29th 25, 6:24:11 pm
date modified: Fri, 10 3rd 25, 5:11:58 pm
---
# n8n Function Node Script

Copy and paste this exact script into your n8n Function node:

```javascript
const { execSync } = require('child_process');

try {
  // Execute your existing UpBank sync script
  const result = execSync('node scripts/sync-upbank-data.js full', {
    cwd: '/Users/harrysayers/Developer/claudelife',
    encoding: 'utf8',
    env: process.env,
    timeout: 300000
  });

  // Log success
  console.log('✅ UpBank sync completed successfully');
  console.log(result);

  // Return success data
  return [{
    json: {
      status: 'success',
      message: 'UpBank sync completed',
      output: result,
      timestamp: new Date().toISOString()
    }
  }];

} catch (error) {
  // Log error
  console.error('❌ UpBank sync failed:', error.message);

  // Return error data
  return [{
    json: {
      status: 'error',
      message: 'UpBank sync failed',
      error: error.message,
      timestamp: new Date().toISOString()
    }
  }];
}
```

## Instructions:
1. Select ALL the code between the triple backticks
2. Copy it (Cmd+C)
3. Go to your n8n Function node
4. Delete any existing code
5. Paste this code (Cmd+V)
6. Click "Execute step" to test
