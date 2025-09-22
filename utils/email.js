const nodemailer = require('nodemailer');
require('dotenv').config();

// Create reusable transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.GMAIL_EMAIL,
    pass: process.env.GMAIL_APP_PASSWORD
  }
});

/**
 * Send email via Gmail SMTP
 * @param {Object} options - Email options
 * @param {string} options.to - Recipient email
 * @param {string} options.subject - Email subject
 * @param {string} options.text - Plain text body
 * @param {string} [options.html] - HTML body (optional)
 * @param {string} [options.from] - Sender email (defaults to GMAIL_EMAIL)
 */
async function sendEmail({ to, subject, text, html, from }) {
  try {
    const mailOptions = {
      from: from || process.env.GMAIL_EMAIL,
      to,
      subject,
      text,
      html
    };

    const info = await transporter.sendMail(mailOptions);

    return {
      success: true,
      messageId: info.messageId,
      message: `Email sent successfully to ${to}`
    };

  } catch (error) {
    return {
      success: false,
      error: error.message,
      message: `Failed to send email to ${to}`
    };
  }
}

/**
 * Send a quick notification email
 * @param {string} to - Recipient email
 * @param {string} subject - Email subject
 * @param {string} message - Email message
 */
async function sendNotification(to, subject, message) {
  return await sendEmail({
    to,
    subject: `[Notification] ${subject}`,
    text: message,
    html: `
      <div style="font-family: Arial, sans-serif; max-width: 600px;">
        <h3>📬 Notification</h3>
        <p>${message.replace(/\n/g, '<br>')}</p>
        <hr>
        <small style="color: #666;">Sent from your AI Assistant</small>
      </div>
    `
  });
}

module.exports = {
  sendEmail,
  sendNotification
};