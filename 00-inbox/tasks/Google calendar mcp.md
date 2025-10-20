---
Done: false
today: false
follow up: false
this week: false
back burner: false
ASAP: false
type: Task
status:
relation:
description:
effort:
ai-assigned: true
ai-ignore: false
ai-ask: false
priority:
agent:
---
instructions for @takumi0706/google-calendar-mcp

Here are the setup and usage instructions for **@takumi0706/google-calendar-mcp**, the recommended Google Calendar MCP server for Claude Code integration:

### Installation

- **Quick Start:**
  ```
  npm install -g @takumi0706/google-calendar-mcp
  ```
  or run directly:
  ```
  npx @takumi0706/google-calendar-mcp@latest
  ```


### Prerequisites

1. **Google Cloud Project:**
   - Create a Google Cloud Project and enable the Google Calendar API.
   - Set up OAuth2 credentials in your Google Cloud Console.

2. **Environment Variables:**
   - Create a `.env` file with:
     ```
     GOOGLE_CLIENT_ID=your_client_id
     GOOGLE_CLIENT_SECRET=your_client_secret
     GOOGLE_REDIRECT_URI=http://localhost:4153/oauth2callback
     ```
   - Optionally:
     ```
     TOKEN_ENCRYPTION_KEY=32-byte-hex-key      # Token security (auto-generated if omitted)
     AUTH_PORT=4153                            # Default auth port
     AUTH_HOST=localhost                       # Default
     PORT=3000                                 # Server port
     HOST=localhost                            # Default
     USE_MANUAL_AUTH=true                      # For remote/server environments
     ```

### Claude Desktop/Code Configuration

- Add the server to your Claude desktop configuration:
  ```json
  {
    "mcpServers": {
      "google-calendar": {
        "command": "npx",
        "args": ["-y", "@takumi0706/google-calendar-mcp"],
        "env": {
          "GOOGLE_CLIENT_ID": "your_client_id",
          "GOOGLE_CLIENT_SECRET": "your_client_secret",
          "GOOGLE_REDIRECT_URI": "http://localhost:4153/oauth2callback"
        }
      }
    }
  }
  ```

### Authentication

- **OAuth2:**
  Secure authentication flow for linking your Google account.
- **Manual Mode:**
  If running where `localhost` is not accessible, set `USE_MANUAL_AUTH=true` and enter the code shown by Google manually.

### Tools Provided

- `getEvents`: List events with filters (calendarId, timeMin, timeMax, maxResults, orderBy).
- `createEvent`: Create events (supports title, description, location, start/end, attendees, colorId, recurrence).
- `updateEvent`: Update events, merge changes with existing data, partial updates supported.
- `deleteEvent`: Remove events.
- `authenticate`: Re-authenticate, switch accounts within Claude session without restart.

### Security

- Tokens are stored in memory only.
- Sensitive credentials are handled as environment variables.
- AES-256-GCM token encryption.
- PKCE OAuth flow for best security.

### Troubleshooting

- Double check your OAuth credentials and API access.
- Single server instance only.
- Use latest version to avoid JSON parsing and parameter validation errors.
- For environments blocking localhost, set manual auth mode.

### Maintenance

- Regular updates and strong test coverage.
- Version and change tracking in documentation.

**Summary:** Install the npm package, set environment variables for your Google credentials, add to Claude Desktop config, then authenticate. You will be able to create, update, delete, and view Google Calendar events directly with natural language prompts in Claude Code/Desktop [1].

Citations:
[1] takumi0706/google-calendar-mcp https://www.npmjs.com/package/@takumi0706/google-calendar-mcp
