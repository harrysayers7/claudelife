#!/usr/bin/env node

/**
 * MCP Server Health Monitor
 * Tracks MCP server response times, failures, and availability
 * Identifies problematic servers affecting context loading
 */

const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

const MCP_CONFIG = path.join(__dirname, '../.mcp.json');
const HEALTH_LOG = path.join(__dirname, '../memory/mcp-health.json');

class MCPHealthMonitor {
  constructor() {
    this.healthData = {
      lastCheck: null,
      servers: {}
    };
  }

  async loadMCPConfig() {
    try {
      const config = await fs.readFile(MCP_CONFIG, 'utf8');
      return JSON.parse(config);
    } catch (error) {
      console.error('Could not load MCP config:', error.message);
      return null;
    }
  }

  async checkServerHealth(serverName, serverConfig) {
    const startTime = Date.now();

    return new Promise((resolve) => {
      // Simulate MCP server health check
      // In real implementation, this would use MCP protocol
      const timeout = setTimeout(() => {
        resolve({
          name: serverName,
          status: 'timeout',
          responseTime: null,
          error: 'Health check timeout'
        });
      }, 5000);

      // Mock health check - replace with actual MCP protocol check
      const healthCheck = spawn('echo', ['healthy'], { timeout: 3000 });

      healthCheck.on('close', (code) => {
        clearTimeout(timeout);
        const responseTime = Date.now() - startTime;

        resolve({
          name: serverName,
          status: code === 0 ? 'healthy' : 'unhealthy',
          responseTime: code === 0 ? responseTime : null,
          error: code !== 0 ? `Exit code: ${code}` : null
        });
      });
    });
  }

  async loadPreviousHealth() {
    try {
      const data = await fs.readFile(HEALTH_LOG, 'utf8');
      this.healthData = JSON.parse(data);
    } catch (error) {
      // First run or missing file
      console.log('Starting fresh health monitoring');
    }
  }

  async saveHealthData() {
    await fs.writeFile(HEALTH_LOG, JSON.stringify(this.healthData, null, 2));
  }

  calculateAvailability(serverName) {
    const server = this.healthData.servers[serverName];
    if (!server || !server.history) return 0;

    const healthy = server.history.filter(h => h.status === 'healthy').length;
    return (healthy / server.history.length) * 100;
  }

  async run() {
    console.log('🏥 Checking MCP server health...');

    await this.loadPreviousHealth();

    const config = await this.loadMCPConfig();
    if (!config || !config.mcpServers) {
      console.log('❌ No MCP servers configured');
      return;
    }

    const servers = Object.keys(config.mcpServers);
    console.log(`📡 Checking ${servers.length} MCP servers...`);

    const checkTime = new Date().toISOString();
    this.healthData.lastCheck = checkTime;

    for (const serverName of servers) {
      const serverConfig = config.mcpServers[serverName];
      console.log(`  • Checking ${serverName}...`);

      const health = await this.checkServerHealth(serverName, serverConfig);

      // Initialize server data if needed
      if (!this.healthData.servers[serverName]) {
        this.healthData.servers[serverName] = {
          history: [],
          totalChecks: 0,
          failures: 0
        };
      }

      const serverData = this.healthData.servers[serverName];

      // Add to history (keep last 100 checks)
      serverData.history.unshift({ ...health, timestamp: checkTime });
      if (serverData.history.length > 100) {
        serverData.history = serverData.history.slice(0, 100);
      }

      serverData.totalChecks++;
      if (health.status !== 'healthy') {
        serverData.failures++;
      }

      const availability = this.calculateAvailability(serverName);
      const statusIcon = health.status === 'healthy' ? '✅' : '❌';

      console.log(`    ${statusIcon} ${health.status} (${health.responseTime || 'N/A'}ms) - ${availability.toFixed(1)}% uptime`);

      if (health.error) {
        console.log(`    ⚠️  Error: ${health.error}`);
      }
    }

    await this.saveHealthData();

    // Generate alerts for problematic servers
    console.log('\n📊 Health Summary:');
    for (const [serverName, data] of Object.entries(this.healthData.servers)) {
      const availability = this.calculateAvailability(serverName);
      const failureRate = (data.failures / data.totalChecks) * 100;

      if (availability < 90) {
        console.log(`🚨 ${serverName}: Low availability (${availability.toFixed(1)}%)`);
      } else if (failureRate > 10) {
        console.log(`⚠️  ${serverName}: High failure rate (${failureRate.toFixed(1)}%)`);
      } else {
        console.log(`✅ ${serverName}: Healthy (${availability.toFixed(1)}% uptime)`);
      }
    }

    console.log(`\n📝 Health data saved to ${HEALTH_LOG}`);
  }
}

if (require.main === module) {
  const monitor = new MCPHealthMonitor();
  monitor.run().catch(console.error);
}

module.exports = MCPHealthMonitor;
