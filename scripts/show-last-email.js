const { google } = require('googleapis');
require('dotenv').config();

async function showLastEmail() {
  try {
    // Set up OAuth2 client
    const oauth2Client = new google.auth.OAuth2(
      process.env.GMAIL_CLIENT_ID,
      process.env.GMAIL_CLIENT_SECRET,
      'urn:ietf:wg:oauth:2.0:oob'
    );

    oauth2Client.setCredentials({
      refresh_token: process.env.GMAIL_REFRESH_TOKEN
    });

    const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

    // Get the last sent email
    const response = await gmail.users.messages.list({
      userId: 'me',
      labelIds: ['SENT'],
      maxResults: 1
    });

    if (!response.data.messages || response.data.messages.length === 0) {
      console.log('No sent emails found.');
      return;
    }

    const messageId = response.data.messages[0].id;

    // Get the full message details
    const message = await gmail.users.messages.get({
      userId: 'me',
      id: messageId,
      format: 'full'
    });

    const headers = message.data.payload.headers;
    const to = headers.find(h => h.name === 'To')?.value || 'Unknown';
    const subject = headers.find(h => h.name === 'Subject')?.value || 'No Subject';
    const date = headers.find(h => h.name === 'Date')?.value || 'Unknown Date';

    // Get message body
    let body = '';
    if (message.data.payload.body && message.data.payload.body.data) {
      body = Buffer.from(message.data.payload.body.data, 'base64').toString();
    } else if (message.data.payload.parts) {
      // Multi-part message
      for (const part of message.data.payload.parts) {
        if (part.mimeType === 'text/plain' && part.body.data) {
          body = Buffer.from(part.body.data, 'base64').toString();
          break;
        }
      }
    }

    console.log('📧 Last Sent Email:');
    console.log('===================');
    console.log(`To: ${to}`);
    console.log(`Subject: ${subject}`);
    console.log(`Date: ${date}`);
    console.log('===================');
    console.log(`Body:\n${body}`);

  } catch (error) {
    console.error('❌ Error fetching email:', error.message);
    if (error.code === 401) {
      console.log('🔧 OAuth token might be expired. Try regenerating the refresh token.');
    }
  }
}

showLastEmail();