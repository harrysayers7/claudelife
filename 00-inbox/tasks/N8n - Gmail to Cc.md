---
Done: false
today: false
follow up: false
this week: true
back burner: false
ASAP: false
type: Task
status:
relation:
description:
effort:
ai-assigned: true
ai-ignore: true
ai-ask: false
priority:
agent:
slash-command:
title: N8n - Gmail to Cc
date created: Sat, 10 18th 25, 4:47:49 am
date modified: Sat, 10 18th 25, 4:48:40 am
---
I want to automate the /mokhouse-create-project command - help me discuss this


### From ChatGPT:

---

🧠 Goal restated

👉 You already have slash commands that trigger Claude Code scripts.
👉 You want: “When a Gmail email arrives and matches X condition → run Claude Code with Y slash command.”


---

### 🛠️ Best-Practice Setup (Recommended Path)

1. Use  n8n to watch Gmail

Set up a simple scenario:

Trigger: Gmail → “New email matches search query”
e.g. subject:Invoice from:client@example.com

Action: Call a Webhook URL on your Mac or server.


This webhook is the bridge that will fire Claude Code.


---

### 2. Run a webhook listener locally that calls Claude Code

Use a lightweight local HTTP listener (like a tiny Python or Node script).
When the webhook receives a request, it runs your Claude Code slash command.

Example: Python listener (webhook_runner.py)

from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        # Optional: match extra criteria here
        subject = data.get("subject", "")
        if "Invoice" in subject:
            subprocess.run(["claude", "code", "run", "invoice-handler.cl"])

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8000), WebhookHandler)
    print("Listening on port 8000...")
    server.serve_forever()

Then just keep this script running in the background (e.g. with launchd or pm2).


---

3. Expose it to  n8n

If it’s only local: use ngrok to expose localhost:8000 to the internet.

If you have a remote server (like your DigitalOcean droplet), run the webhook there and skip ngrok.



---

4. Call your slash command from the webhook

Because you already built slash commands for Claude Code, just call them from the webhook.
For example:

claude code run /Users/harrysayers/Developer/claudelife/agents/trigger-email.cl --arg "email_subject=Invoice"


---

🧰 Variations

🔁 n8n self-hosted: You could skip the webhook and run the Claude Code CLI directly from a local exec node inside n8n if it’s on the same machine.

⚡ Apple Shortcut: On macOS, you could also have a Shortcut triggered by a mail rule → run shell script → claude code run .... That’s simpler but less flexible.



---

🧪 TL;DR — What’s Happening

1. 📬 Gmail sees a new email → triggers Make.com (or n8n)


2. 🌐 Make.com POSTs to your local webhook listener


3. 🧠 Listener runs your existing Claude Code slash command


4. 🤖 Claude executes the automation instantly




---

If you want, I can generate a ready-to-run version of that webhook script tailored to your slash command (with args, logging, etc.).

👉 Can you paste one example of a slash command you’d want triggered (the exact claude code ... command)? Then I’ll give you a complete runnable setup.
