#!/usr/bin/env node

const fs = require('fs');
const { spawn } = require('child_process');
const path = require('path');

console.log('MCP Server Testing Script');
console.log('=========================');

// Test configurations in order of likelihood
const testConfigs = [
    {
        name: 'Baseline (NPX servers)',
        servers: ['serena', 'context7', 'trigger', 'linear-server', 'ide', 'notion', 'supabase', 'task-master-ai', 'github', 'memory']
    },
    {
        name: 'Add UpBank (FastMCP)',
        servers: ['serena', 'context7', 'trigger', 'linear-server', 'ide', 'notion', 'supabase', 'task-master-ai', 'github', 'memory', 'upbank']
    },
    {
        name: 'Add Graphiti',
        servers: ['serena', 'context7', 'trigger', 'linear-server', 'ide', 'notion', 'supabase', 'task-master-ai', 'github', 'memory', 'upbank', 'graphiti-claudelife']
    },
    {
        name: 'Add GPT-Researcher (LIKELY CULPRIT)',
        servers: ['serena', 'context7', 'trigger', 'linear-server', 'ide', 'notion', 'supabase', 'task-master-ai', 'github', 'memory', 'upbank', 'graphiti-claudelife', 'gptr-mcp']
    },
    {
        name: 'Add SSE servers',
        servers: ['serena', 'context7', 'trigger', 'linear-server', 'ide', 'notion', 'supabase', 'task-master-ai', 'github', 'memory', 'upbank', 'graphiti-claudelife', 'gptr-mcp', 'claudelife-business-api', 'claudelife-financial-api']
    }
];

// Full server configurations
const allServers = JSON.parse(fs.readFileSync('.mcp.json.all-disabled', 'utf8')).mcpServers;

async function testConfiguration(config) {
    console.log(`\n🧪 Testing: ${config.name}`);
    console.log(`   Servers: ${config.servers.join(', ')}`);

    // Create test config
    const testConfig = {
        mcpServers: {}
    };

    for (const serverName of config.servers) {
        const cleanName = serverName.startsWith('_') ? serverName.substring(1) : serverName;
        const originalName = `_${cleanName}`;

        if (allServers[originalName]) {
            testConfig.mcpServers[cleanName] = allServers[originalName];
        } else {
            console.log(`   ⚠️  Server ${serverName} not found in disabled config`);
        }
    }

    // Write test config
    fs.writeFileSync('.mcp-test.json', JSON.stringify(testConfig, null, 2));

    console.log(`   📄 Created test config with ${Object.keys(testConfig.mcpServers).length} servers`);
    console.log(`   👆 Now test this configuration in Claude Code`);
    console.log(`   📋 Copy .mcp-test.json to .mcp.json to test`);

    return testConfig;
}

// Check if gptr-mcp is likely the issue
console.log('\n🔍 Analysis based on error "tools.305.custom.input_schema":');
console.log('   - Error suggests 305th tool has schema issues');
console.log('   - GPT-Researcher MCP typically has 300+ tools');
console.log('   - This makes gptr-mcp the most likely culprit');

console.log('\n📋 Testing Strategy:');
console.log('1. Start with baseline NPX servers (lowest risk)');
console.log('2. Add custom Python servers one by one');
console.log('3. Identify which server causes the error');

// Run tests
async function runTests() {
    for (const config of testConfigs) {
        await testConfiguration(config);

        console.log('\n   ⏸️  PAUSE HERE - Test this configuration');
        console.log('   ✅ If it works, continue to next test');
        console.log('   ❌ If it fails, this is your problematic server');
        console.log('   📝 Press Enter to continue...');

        // Wait for user input (simplified for script)
        // In real use, you'd test each configuration manually
    }
}

runTests();

console.log('\n🚨 If gptr-mcp is the problem:');
console.log('   1. Check if it needs updates');
console.log('   2. Verify Python environment');
console.log('   3. Consider disabling temporarily');
console.log('   4. Check server logs for schema errors');
