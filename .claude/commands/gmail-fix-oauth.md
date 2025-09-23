# Gmail OAuth Fix

Fix the Gmail OAuth invalid_grant error by re-authorizing with proper scopes.

Steps:
1. Check Linear issue SAY-74 status: `mcp__linear-server__get_issue SAY-74`
2. Run the OAuth fix script: `node scripts/fix-gmail-oauth.js`
3. Follow the authorization flow with consent prompt
4. Update .env with new refresh token
5. Test Gmail API with: `node scripts/send-test-email.js`
6. Update Linear issue with progress

This addresses the OAuth bug preventing Gmail API email reading functionality.
