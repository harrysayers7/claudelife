#!/usr/bin/env node

/**
 * Context Usage Analytics
 * Tracks which context packs are most valuable and token efficiency
 * Based on context engineering best practices
 */

const fs = require('fs').promises;
const path = require('path');

const MEMORY_DIR = path.join(__dirname, '../memory');
const LOGS_DIR = path.join(__dirname, '../.claude/logs');

class ContextAnalytics {
  constructor() {
    this.metrics = {
      packUsage: {}, // Which packs loaded most frequently
      tokenEfficiency: {}, // Tokens used vs conversation length
      loadingPatterns: [], // When packs get loaded
      missingContext: [] // When gap detection triggers
    };
  }

  async analyzeConversationContext() {
    try {
      const contextFile = path.join(MEMORY_DIR, 'conversation-context.md');
      const content = await fs.readFile(contextFile, 'utf8');

      // Extract pack loading events
      const packLoads = content.match(/loaded (business|technical|automation)-pack/gi) || [];
      const tokenUsage = content.match(/tokens: (\d+)/g) || [];

      return {
        packsLoaded: packLoads.length,
        averageTokens: this.calculateAverageTokens(tokenUsage),
        efficiency: packLoads.length > 0 ? tokenUsage.length / packLoads.length : 0
      };
    } catch (error) {
      console.warn('Could not analyze conversation context:', error.message);
      return null;
    }
  }

  calculateAverageTokens(tokenMatches) {
    if (tokenMatches.length === 0) return 0;
    const tokens = tokenMatches.map(m => parseInt(m.match(/\d+/)[0]));
    return Math.round(tokens.reduce((a, b) => a + b, 0) / tokens.length);
  }

  async generateRecommendations(analysis) {
    const recommendations = [];

    if (analysis.efficiency < 0.5) {
      recommendations.push({
        type: 'token-optimization',
        priority: 'high',
        suggestion: 'Consider implementing graduated loading - many packs loaded with low token usage'
      });
    }

    if (analysis.averageTokens > 40000) {
      recommendations.push({
        type: 'context-compression',
        priority: 'medium',
        suggestion: 'Approaching token limit - implement context compression for older conversations'
      });
    }

    return recommendations;
  }

  async run() {
    console.log('🔍 Analyzing context usage patterns...');

    const analysis = await this.analyzeConversationContext();
    if (!analysis) {
      console.log('❌ No conversation data to analyze');
      return;
    }

    console.log('\n📊 Context Usage Analysis:');
    console.log(`• Packs loaded: ${analysis.packsLoaded}`);
    console.log(`• Average tokens: ${analysis.averageTokens}`);
    console.log(`• Efficiency: ${(analysis.efficiency * 100).toFixed(1)}%`);

    const recommendations = await this.generateRecommendations(analysis);

    if (recommendations.length > 0) {
      console.log('\n💡 Recommendations:');
      recommendations.forEach((rec, i) => {
        console.log(`${i + 1}. [${rec.priority.toUpperCase()}] ${rec.suggestion}`);
      });
    } else {
      console.log('\n✅ Context usage looks optimal!');
    }

    // Save analysis for tracking trends
    const reportPath = path.join(MEMORY_DIR, 'context-usage-analysis.json');
    await fs.writeFile(reportPath, JSON.stringify({
      timestamp: new Date().toISOString(),
      analysis,
      recommendations
    }, null, 2));

    console.log(`\n📝 Analysis saved to ${reportPath}`);
  }
}

if (require.main === module) {
  const analyzer = new ContextAnalytics();
  analyzer.run().catch(console.error);
}

module.exports = ContextAnalytics;
