const { google } = require('googleapis');
require('dotenv').config();

async function sendTestEmail() {
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

    // Create email content
    const message = [
      'To: harrysayers96@gmail.com',
      'Subject: Test Email from Claude Code',
      'Content-Type: text/plain; charset=utf-8',
      '',
      'This is a test email sent from Claude Code!',
      '',
      'If you received this, Gmail API integration is working correctly.',
      '',
      '- Your AI Assistant'
    ].join('\n');

    // Encode message
    const encodedMessage = Buffer.from(message)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    // Send email
    const result = await gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedMessage
      }
    });

    console.log('✅ Email sent successfully!');
    console.log('Message ID:', result.data.id);
    console.log('Check your inbox: harrysayers96@gmail.com');

  } catch (error) {
    console.error('❌ Error sending email:', error.message);
    if (error.code === 401) {
      console.log('🔧 Try regenerating your refresh token - it might be expired');
    }
  }
}

sendTestEmail();
