const { google } = require('googleapis');
const readline = require('readline');
require('dotenv').config();

async function fixGmailOAuth() {
  const oauth2Client = new google.auth.OAuth2(
    process.env.GMAIL_CLIENT_ID,
    process.env.GMAIL_CLIENT_SECRET,
    'urn:ietf:wg:oauth:2.0:oob'
  );

  // Generate auth URL with ALL necessary scopes
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    prompt: 'consent', // Force consent screen to get refresh token
    scope: [
      'https://www.googleapis.com/auth/gmail.readonly',
      'https://www.googleapis.com/auth/gmail.send',
      'https://www.googleapis.com/auth/gmail.modify',
      'https://www.googleapis.com/auth/gmail.metadata'
    ]
  });

  console.log('\n=================================');
  console.log('IMPORTANT: Make sure to REVOKE previous authorization first!');
  console.log('Go to: https://myaccount.google.com/permissions');
  console.log('Remove any previous "Sensei App" or similar authorization');
  console.log('\nThen authorize this app by visiting this url:');
  console.log('\n' + authUrl);
  console.log('\n=================================\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  rl.question('Enter the authorization code from that page here: ', async (code) => {
    try {
      const { tokens } = await oauth2Client.getToken(code);

      console.log('\n=================================');
      console.log('SUCCESS! Here are your new tokens:');
      console.log('\nRefresh Token:');
      console.log(tokens.refresh_token);
      console.log('\nAccess Token (expires):');
      console.log(tokens.access_token);
      console.log('\n=================================');
      console.log('\nUpdate your .env file with:');
      console.log(`GMAIL_REFRESH_TOKEN=${tokens.refresh_token}`);
      console.log('=================================\n');

      // Test the tokens immediately
      oauth2Client.setCredentials(tokens);
      const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

      const profile = await gmail.users.getProfile({ userId: 'me' });
      console.log('✅ Token test successful!');
      console.log(`Connected to: ${profile.data.emailAddress}`);
      console.log(`Total messages: ${profile.data.messagesTotal}`);

    } catch (error) {
      console.error('❌ Error getting token:', error.message);
    }

    rl.close();
  });
}

fixGmailOAuth();
