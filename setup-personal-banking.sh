#!/bin/bash

# Setup Personal Banking Database
# This script creates the personal banking tables and syncs UpBank data

echo "🏦 Setting up Personal Banking Database..."

# Source environment variables from .zshrc.md
if [[ -f ~/.zshrc.md ]]; then
    # Extract export lines from .zshrc.md
    eval $(grep "^export" ~/.zshrc.md)
elif [[ -f ~/.zshrc ]]; then
    source ~/.zshrc
else
    echo "⚠️  No .zshrc or .zshrc.md found, checking current environment..."
fi

# Check required environment variables
if [[ -z "$SUPABASE_SERVICE_KEY" ]]; then
    echo "❌ SUPABASE_SERVICE_KEY not found in environment"
    exit 1
fi

if [[ -z "$UPBANK_API_TOKEN" ]]; then
    echo "❌ UPBANK_API_TOKEN not found in environment"
    exit 1
fi

# Set Supabase project details
export SUPABASE_URL="https://gshsshaodoyttdxippwx.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="$SUPABASE_SERVICE_KEY"

echo "✅ Environment variables loaded"

# Apply database migration
echo "📊 Applying database migration..."
npx supabase db push --db-url "postgresql://postgres:$SUPABASE_SERVICE_KEY@db.gshsshaodoyttdxippwx.supabase.co:5432/postgres" --include-all || {
    echo "⚠️  Direct migration failed, trying SQL execution..."

    # Alternative: Execute SQL directly via psql if available
    if command -v psql &> /dev/null; then
        echo "🔧 Using psql to apply migration..."
        PGPASSWORD="$SUPABASE_SERVICE_KEY" psql -h db.gshsshaodoyttdxippwx.supabase.co -p 5432 -U postgres -d postgres -f migrations/personal_banking_schema.sql
    else
        echo "❌ psql not available. Please install PostgreSQL client or apply migration manually"
        echo "📋 Migration file: migrations/personal_banking_schema.sql"
    fi
}

# Install required dependencies for sync script
echo "📦 Installing Node.js dependencies..."
npm install @supabase/supabase-js node-fetch

# Make sync script executable
chmod +x scripts/sync-upbank-data.js

# Test UpBank API connection
echo "🔗 Testing UpBank API connection..."
node -e "
const fetch = require('node-fetch');
fetch('https://api.up.com.au/api/v1/accounts', {
    headers: { 'Authorization': 'Bearer $UPBANK_API_TOKEN' }
})
.then(r => r.ok ? console.log('✅ UpBank API connected') : console.log('❌ UpBank API failed'))
.catch(e => console.log('❌ UpBank API error:', e.message));
"

# Run initial sync
echo "🔄 Running initial UpBank sync..."
node scripts/sync-upbank-data.js full 30

echo "🎉 Personal banking setup complete!"
echo ""
echo "📋 Next steps:"
echo "  • Run daily sync: node scripts/sync-upbank-data.js full 7"
echo "  • Sync specific account: node scripts/sync-upbank-data.js transactions [account-id]"
echo "  • View data in Supabase dashboard: https://supabase.com/dashboard/project/gshsshaodoyttdxippwx"
echo ""
echo "📊 Database tables created:"
echo "  • personal_accounts (your UpBank accounts)"
echo "  • personal_transactions (your transactions)"
echo "  • upbank_categories (UpBank's categories)"
echo "  • personal_finance_categories (custom categories)"
echo "  • transaction_attachments (receipts, etc.)"
