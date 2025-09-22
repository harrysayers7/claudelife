const Imap = require('imap');
const { simpleParser } = require('mailparser');
require('dotenv').config();

class EmailReader {
  constructor() {
    this.imap = new Imap({
      user: process.env.GMAIL_EMAIL,
      password: process.env.GMAIL_APP_PASSWORD,
      host: 'imap.gmail.com',
      port: 993,
      tls: true,
      tlsOptions: { rejectUnauthorized: false }
    });
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.imap.once('ready', () => {
        console.log('📧 Connected to Gmail IMAP');
        resolve();
      });

      this.imap.once('error', (err) => {
        console.error('❌ IMAP connection error:', err.message);
        reject(err);
      });

      this.imap.connect();
    });
  }

  disconnect() {
    this.imap.end();
  }

  /**
   * Get recent emails from inbox
   * @param {number} count - Number of emails to fetch (default: 10)
   * @param {string} folder - Folder to read from (default: 'INBOX')
   */
  async getRecentEmails(count = 10, folder = 'INBOX') {
    await this.connect();

    return new Promise((resolve, reject) => {
      this.imap.openBox(folder, true, (err, box) => {
        if (err) {
          reject(err);
          return;
        }

        const totalMessages = box.messages.total;
        if (totalMessages === 0) {
          resolve([]);
          this.disconnect();
          return;
        }

        const start = Math.max(1, totalMessages - count + 1);
        const end = totalMessages;

        const fetch = this.imap.seq.fetch(`${start}:${end}`, {
          bodies: '',
          markSeen: false
        });

        const emails = [];

        fetch.on('message', (msg, seqno) => {
          let buffer = '';

          msg.on('body', (stream) => {
            stream.on('data', (chunk) => {
              buffer += chunk.toString('utf8');
            });
          });

          msg.once('end', async () => {
            try {
              const parsed = await simpleParser(buffer);
              emails.push({
                seqno,
                messageId: parsed.messageId,
                from: parsed.from?.text || 'Unknown',
                to: parsed.to?.text || 'Unknown',
                subject: parsed.subject || 'No Subject',
                date: parsed.date,
                text: parsed.text || '',
                html: parsed.html || '',
                attachments: parsed.attachments || []
              });
            } catch (parseErr) {
              console.error('Error parsing email:', parseErr.message);
            }
          });
        });

        fetch.once('error', reject);

        fetch.once('end', () => {
          this.disconnect();
          // Sort by date (newest first)
          emails.sort((a, b) => new Date(b.date) - new Date(a.date));
          resolve(emails);
        });
      });
    });
  }

  /**
   * Search emails by criteria
   * @param {Object} criteria - Search criteria
   * @param {string} criteria.from - From email address
   * @param {string} criteria.subject - Subject contains
   * @param {string} criteria.body - Body contains
   * @param {Date} criteria.since - Since date
   * @param {number} criteria.limit - Max results (default: 50)
   */
  async searchEmails(criteria, folder = 'INBOX') {
    await this.connect();

    return new Promise((resolve, reject) => {
      this.imap.openBox(folder, true, (err, box) => {
        if (err) {
          reject(err);
          return;
        }

        // Build search criteria for IMAP
        const searchCriteria = [];

        if (criteria.from) {
          searchCriteria.push(['FROM', criteria.from]);
        }
        if (criteria.subject) {
          searchCriteria.push(['SUBJECT', criteria.subject]);
        }
        if (criteria.body) {
          searchCriteria.push(['BODY', criteria.body]);
        }
        if (criteria.since) {
          searchCriteria.push(['SINCE', criteria.since]);
        }

        // If no criteria, get recent emails
        if (searchCriteria.length === 0) {
          searchCriteria.push(['ALL']);
        }

        this.imap.search(searchCriteria, (err, results) => {
          if (err) {
            reject(err);
            return;
          }

          if (!results || results.length === 0) {
            resolve([]);
            this.disconnect();
            return;
          }

          // Limit results
          const limitedResults = results.slice(-1 * (criteria.limit || 50));

          const fetch = this.imap.fetch(limitedResults, {
            bodies: '',
            markSeen: false
          });

          const emails = [];

          fetch.on('message', (msg, seqno) => {
            let buffer = '';

            msg.on('body', (stream) => {
              stream.on('data', (chunk) => {
                buffer += chunk.toString('utf8');
              });
            });

            msg.once('end', async () => {
              try {
                const parsed = await simpleParser(buffer);
                emails.push({
                  uid: msg.attributes.uid,
                  messageId: parsed.messageId,
                  from: parsed.from?.text || 'Unknown',
                  to: parsed.to?.text || 'Unknown',
                  subject: parsed.subject || 'No Subject',
                  date: parsed.date,
                  text: parsed.text || '',
                  html: parsed.html || '',
                  attachments: parsed.attachments || []
                });
              } catch (parseErr) {
                console.error('Error parsing email:', parseErr.message);
              }
            });
          });

          fetch.once('error', reject);

          fetch.once('end', () => {
            this.disconnect();
            // Sort by date (newest first)
            emails.sort((a, b) => new Date(b.date) - new Date(a.date));
            resolve(emails);
          });
        });
      });
    });
  }

  /**
   * Get unread emails
   */
  async getUnreadEmails() {
    await this.connect();

    return new Promise((resolve, reject) => {
      this.imap.openBox('INBOX', false, (err, box) => {
        if (err) {
          reject(err);
          return;
        }

        this.imap.search(['UNSEEN'], (err, results) => {
          if (err) {
            reject(err);
            return;
          }

          if (!results || results.length === 0) {
            resolve([]);
            this.disconnect();
            return;
          }

          const fetch = this.imap.fetch(results, {
            bodies: '',
            markSeen: false
          });

          const emails = [];

          fetch.on('message', (msg, seqno) => {
            let buffer = '';

            msg.on('body', (stream) => {
              stream.on('data', (chunk) => {
                buffer += chunk.toString('utf8');
              });
            });

            msg.once('end', async () => {
              try {
                const parsed = await simpleParser(buffer);
                emails.push({
                  uid: msg.attributes.uid,
                  messageId: parsed.messageId,
                  from: parsed.from?.text || 'Unknown',
                  to: parsed.to?.text || 'Unknown',
                  subject: parsed.subject || 'No Subject',
                  date: parsed.date,
                  text: parsed.text || '',
                  html: parsed.html || '',
                  attachments: parsed.attachments || []
                });
              } catch (parseErr) {
                console.error('Error parsing email:', parseErr.message);
              }
            });
          });

          fetch.once('error', reject);

          fetch.once('end', () => {
            this.disconnect();
            emails.sort((a, b) => new Date(b.date) - new Date(a.date));
            resolve(emails);
          });
        });
      });
    });
  }
}

module.exports = EmailReader;