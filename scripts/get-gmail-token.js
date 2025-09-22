const { google } = require('googleapis');
const readline = require('readline');
require('dotenv').config();

const oauth2Client = new google.auth.OAuth2(
  process.env.GMAIL_CLIENT_ID,
  process.env.GMAIL_CLIENT_SECRET,
  'urn:ietf:wg:oauth:2.0:oob'
);

// Generate auth URL
const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
  ]
});

console.log('\n=================================');
console.log('Authorize this app by visiting this url:');
console.log('\n' + authUrl);
console.log('\n=================================\n');

// Get the code from the URL and exchange for tokens
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question('Enter the authorization code from that page here: ', (code) => {
  oauth2Client.getToken(code, (err, token) => {
    if (err) {
      console.error('Error retrieving access token:', err);
      rl.close();
      return;
    }

    console.log('\n=================================');
    console.log('SUCCESS! Here is your refresh token:');
    console.log('\n' + token.refresh_token);
    console.log('\n=================================');
    console.log('\nAdd this to your .env file:');
    console.log(`GMAIL_REFRESH_TOKEN=${token.refresh_token}`);
    console.log('=================================\n');

    rl.close();
  });
});