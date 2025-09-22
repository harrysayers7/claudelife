const nodemailer = require('nodemailer');
require('dotenv').config();

async function sendEmailSMTP() {
  try {
    // Create transporter
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_EMAIL,
        pass: process.env.GMAIL_APP_PASSWORD
      }
    });

    // Send email
    const info = await transporter.sendMail({
      from: process.env.GMAIL_EMAIL,
      to: 'harrysayers96@gmail.com',
      subject: 'Test Email from Claude Code (SMTP)',
      text: 'This is a test email sent via Gmail SMTP from Claude Code!\n\nIf you received this, email integration is working.',
      html: `
        <h2>✅ Email Integration Test</h2>
        <p>This is a test email sent via Gmail SMTP from Claude Code!</p>
        <p>If you received this, email integration is working correctly.</p>
        <hr>
        <small>Sent from your AI Assistant</small>
      `
    });

    console.log('✅ Email sent successfully via SMTP!');
    console.log('Message ID:', info.messageId);
    console.log('Check your inbox: harrysayers96@gmail.com');

  } catch (error) {
    console.error('❌ Error sending email:', error.message);
    console.log('\n🔧 To fix this, you need to:');
    console.log('1. Add GMAIL_EMAIL=your_email@gmail.com to .env');
    console.log('2. Add GMAIL_APP_PASSWORD=your_app_password to .env');
    console.log('3. Create App Password: https://myaccount.google.com/apppasswords');
    console.log('   (You need 2FA enabled first)');
  }
}

sendEmailSMTP();