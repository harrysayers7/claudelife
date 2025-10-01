#!/bin/bash
# Stripe MCP wrapper script
# Reads STRIPE_SECRET_KEY from environment and passes to @stripe/mcp

if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo "Error: STRIPE_SECRET_KEY environment variable not set" >&2
    exit 1
fi

npx -y @stripe/mcp --tools=all --api-key="$STRIPE_SECRET_KEY"
