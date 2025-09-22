const Imap = require('imap');
require('dotenv').config();

function checkSentEmails() {
  return new Promise((resolve, reject) => {
    const imap = new Imap({
      user: process.env.GMAIL_EMAIL,
      password: process.env.GMAIL_APP_PASSWORD,
      host: 'imap.gmail.com',
      port: 993,
      tls: true,
      tlsOptions: { rejectUnauthorized: false }
    });

    imap.once('ready', function() {
      console.log('📧 Connected to Gmail IMAP');

      // Open the Sent folder
      imap.openBox('[Gmail]/Sent Mail', true, function(err, box) {
        if (err) {
          console.error('❌ Error opening sent folder:', err.message);
          imap.end();
          return reject(err);
        }

        console.log(`📬 Found ${box.messages.total} sent emails`);

        if (box.messages.total === 0) {
          console.log('No sent emails found.');
          imap.end();
          return resolve();
        }

        // Fetch the last sent email
        const fetch = imap.seq.fetch(box.messages.total + ':*', {
          bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)',
          struct: true
        });

        let lastEmail = {};

        fetch.on('message', function(msg, seqno) {
          msg.on('body', function(stream, info) {
            let buffer = '';
            stream.on('data', function(chunk) {
              buffer += chunk.toString('utf8');
            });
            stream.once('end', function() {
              lastEmail.headers = buffer;
            });
          });

          msg.once('end', function() {
            console.log('\n📧 Last Sent Email:');
            console.log('===================');
            console.log(lastEmail.headers);
            console.log('===================');
          });
        });

        fetch.once('error', function(err) {
          console.error('❌ Fetch error:', err.message);
          reject(err);
        });

        fetch.once('end', function() {
          imap.end();
          resolve();
        });
      });
    });

    imap.once('error', function(err) {
      console.error('❌ IMAP connection error:', err.message);
      reject(err);
    });

    imap.connect();
  });
}

checkSentEmails().catch(console.error);