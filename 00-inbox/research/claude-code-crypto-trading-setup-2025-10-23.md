---
research-type: deep research
keywords:
  - claude-code-2025
  - crypto-trading-automation
  - backtesting-py
  - trading-skills
  - agent-orchestration
  - real-time-data-feeds
  - strategy-validation-pipeline
  - production-deployment
tags:
  - claude-code
  - crypto
  - trading
  - automation
  - backtesting
  - deep-research
source:
  - https://blog.pickmytrade.trade/claude-4-1-for-trading-guide/
  - https://dev.to/holasoymalva/the-ultimate-claude-code-guide-every-hidden-trick-hack-and-power-feature-you-need-to-know-2l45
  - https://algotrading101.com/learn/backtesting-py-guide/
  - https://www.interactivebrokers.com/campus/ibkr-quant-news/backtesting-py-an-introductory-guide-to-backtesting-with-python/
  - https://medium.com/@algorithmictrading/develop-a-trading-idea-using-chatgpt-and-claude-from-data-to-backtesting-40a5beb3f370
category: trading-systems
description: Production-ready guide for setting up Claude Code (October 2025) for effective crypto trading using backtesting.py framework, including skills, slash commands, MCP servers, and agent orchestration patterns for automated strategy development and validation.
date: 2025-10-23
date created: Thu, 10 23rd 25, 8:42:13 am
date modified: Thu, 10 23rd 25, 8:54:03 am
---

# Setting Up Claude Code for Effective Crypto Trading (2025)

## Executive Summary

Claude Code has evolved into a powerful AI-assisted development environment with advanced capabilities perfect for building production-ready crypto trading systems. This guide demonstrates how to leverage **Skills** (reusable workflows), **Slash Commands** (custom automation), **Agents** (specialized task executors), **MCP Servers** (Model Context Protocol integrations), and **Git Worktrees** (parallel development) to create an automated strategy development pipeline using the backtesting.py framework.

### 🎯 Key Findings

- **Claude 4.1 (August 2025)** introduced financial services readiness with 64K token context windows and MCP connectors
- **Skills system** enables reusable strategy development workflows that can be invoked with simple commands
- **Agent orchestration** allows parallel backtesting across multiple timeframes/assets simultaneously
- **MCP servers** provide real-time crypto data feeds and exchange API integrations
- **backtesting.py** integrates seamlessly with Claude Code for rapid strategy prototyping and validation
- **Production deployment** requires strict security practices for API key management and human-in-the-loop safeguards

---

## 1. Claude Code Project Architecture for Trading

### Recommended Directory Structure

```
crypto-trading/
├── .claude/
│   ├── commands/                    # Slash commands
│   │   ├── test-strategy.md         # Quick strategy testing
│   │   ├── deploy-strategy.md       # Deployment validation checklist
│   │   ├── sync-trades.md          # Exchange data sync
│   │   └── optimize-params.md      # Parameter optimization
│   ├── skills/                      # Reusable workflows
│   │   ├── create-strategy/
│   │   │   └── SKILL.md            # Interactive strategy scaffolding
│   │   ├── backtest-validate/
│   │   │   └── SKILL.md            # Multi-timeframe validation
│   │   └── optimize-strategy/
│   │       └── SKILL.md            # Walk-forward analysis
│   └── settings.json               # Tool permissions
├── .mcp.json                       # MCP server config
├── strategies/                     # backtesting.py strategies
│   ├── opening_range_breakout.py
│   ├── sma_crossover.py
│   └── mean_reversion.py
├── data/                          # Historical data cache
│   ├── btc_1m_2024.csv
│   └── eth_5m_2024.csv
├── backtests/                     # Backtest results
│   ├── results/
│   └── optimizations/
├── live/                          # Production deployment
│   ├── deployed_strategies/
│   └── logs/
└── scripts/                       # Automation scripts
    ├── fetch_data.py
    └── sync_supabase.py
```

### Version Control Strategy

```bash
# Main branch: stable production strategies
git worktree add ../crypto-backtest feature/new-strategy
git worktree add ../crypto-optimize feature/parameter-tuning
git worktree add ../crypto-deploy feature/live-deployment

# Run Claude Code in each worktree for parallel development
cd ../crypto-backtest && claude     # Terminal 1: Strategy development
cd ../crypto-optimize && claude     # Terminal 2: Parameter optimization
cd ../crypto-deploy && claude       # Terminal 3: Deployment prep
```

---

## 2. Essential MCP Servers for Crypto Trading

### Core MCP Server Configuration

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "crypto-data-feed": {
      "command": "npx",
      "args": ["-y", "crypto-websocket-mcp"],
      "env": {
        "BINANCE_API_KEY": "${BINANCE_API_KEY}",
        "COINBASE_API_KEY": "${COINBASE_API_KEY}",
        "KRAKEN_API_KEY": "${KRAKEN_API_KEY}"
      }
    },
    "supabase-logger": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_KEY": "${SUPABASE_KEY}"
      }
    },
    "upbank-tracker": {
      "command": "node",
      "args": ["./mcp-servers/upbank-integration.js"],
      "env": {
        "UPBANK_API_KEY": "${UPBANK_API_KEY}"
      }
    }
  }
}
```

### Enable in `~/.claude/settings.local.json`

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": [
    "crypto-data-feed",
    "supabase-logger",
    "upbank-tracker"
  ]
}
```

### Recommended MCP Servers for Trading

| Server | Purpose | Key Features |
|--------|---------|-------------|
| **crypto-websocket-mcp** | Real-time price feeds | WebSocket streaming, multiple exchanges |
| **supabase-mcp** | Trade logging & analytics | Store backtests, live trades, performance metrics |
| **upbank-mcp** | Financial tracking | Sync funding flows to/from exchanges |
| **trigger-dev-mcp** | Background job automation | Schedule data fetches, rebalancing tasks |
| **github-mcp** | Version control integration | Commit strategies, create deployment PRs |

---

## 3. Skills for Strategy Development Workflows

### Skill: `/create-strategy`

Create `.claude/skills/create-strategy/SKILL.md`:

```markdown
# Create Trading Strategy Skill

You are an expert trading strategy architect using Claude Code and backtesting.py.

## Process

1. **Strategy Discovery**
   - Ask user for strategy concept (e.g., "mean reversion on RSI oversold")
   - Identify: entry signals, exit signals, risk management, timeframe

2. **Template Selection**
   - Determine if strategy is: trend-following, mean-reversion, breakout, or momentum
   - Select appropriate backtesting.py template

3. **Strategy Scaffolding**
   - Generate Python class inheriting from `backtesting.Strategy`
   - Implement `init()` method with indicator setup
   - Implement `next()` method with trading logic
   - Add stop-loss and take-profit parameters

4. **Data Preparation**
   - Generate `fetch_data.py` script for historical data (yfinance or Hydra)
   - Create OHLCV DataFrame with proper datetime index
   - Save to `data/` directory

5. **Initial Backtest**
   - Create backtest runner script
   - Set initial capital, commission (0.2% for crypto typical)
   - Run baseline backtest and display stats

6. **Documentation**
   - Create strategy README with: concept, parameters, expected metrics
   - Add to git with proper commit message

## Output Template

```python
from backtesting import Strategy, Backtest
from backtesting.lib import crossover
import pandas as pd

class {StrategyName}(Strategy):
    # Optimizable parameters
    param1 = 10
    param2 = 20

    def init(self):
        # Pre-calculate indicators
        self.indicator1 = self.I(SMA, self.data.Close, self.param1)

    def next(self):
        # Trading logic
        if {entry_condition}:
            self.buy(sl={stop_loss}, tp={take_profit})
        elif {exit_condition}:
            self.position.close()
```

Use with: `Skill({ command: "create-strategy" })`
```

### Skill: `/backtest-validate`

Create `.claude/skills/backtest-validate/SKILL.md`:

```markdown
# Backtest Validation Skill

Comprehensive multi-timeframe validation pipeline to avoid overfitting.

## Validation Steps

1. **In-Sample Backtest** (First 70% of data)
   - Run baseline strategy
   - Capture: Return %, Sharpe Ratio, Max Drawdown, Win Rate, # Trades

2. **Out-of-Sample Test** (Next 20% of data)
   - Run with same parameters (NO optimization)
   - Compare metrics to in-sample (should be within 20%)
   - Flag if OOS performance degrades >30%

3. **Walk-Forward Analysis**
   - Split data into 6-month windows
   - Optimize on window N, test on window N+1
   - Repeat sliding forward
   - Report consistency across windows

4. **Multi-Timeframe Test**
   - Test same strategy on: 1m, 5m, 15m, 1h, 4h bars
   - Identify optimal timeframe(s)

5. **Multi-Asset Test**
   - Run on: BTC, ETH, BNB, SOL (major cryptos)
   - Check if logic generalizes or is asset-specific

6. **Validation Report**
   - Generate markdown report with all metrics
   - Create recommendation: PASS (deploy), CAUTION (improve), FAIL (redesign)

## Output

Saves to: `backtests/validation-reports/{strategy-name}-{date}.md`

Use with: `Skill({ command: "backtest-validate" })`
```

### Skill: `/optimize-strategy`

Create `.claude/skills/optimize-strategy/SKILL.md`:

```markdown
# Strategy Optimization Skill

Parameter optimization with walk-forward validation to prevent overfitting.

## Optimization Process

1. **Define Parameter Space**
   - Extract all optimizable parameters from strategy class
   - Ask user for reasonable ranges (e.g., SMA period: 5-60 days)

2. **Grid Search Optimization**
   - Use `bt.optimize()` with parameter ranges
   - Maximize: 'SQN' (System Quality Number) or 'Sharpe Ratio'
   - Add constraints (e.g., tp_pct > sl_pct)

3. **Walk-Forward Validation**
   - Split data into training/testing windows
   - Optimize on training window
   - Test on following window
   - Repeat across all windows

4. **Stability Analysis**
   - Generate heatmap for 2-parameter optimization
   - Check for broad performance plateau (good) vs. single spike (overfitting)
   - Calculate parameter sensitivity

5. **Best Parameters Report**
   - List optimal parameters
   - Show performance across in-sample and OOS periods
   - Warn if parameters are near edges of search space

## Output

```python
# Optimization results
stats = bt.optimize(
    param1=range(5, 60, 5),
    param2=range(10, 100, 10),
    maximize='SQN',
    constraint=lambda p: p.param2 > p.param1
)
print(stats._strategy)  # Best parameters
```

Saves: `backtests/optimizations/{strategy}-optimized-{date}.json`

Use with: `Skill({ command: "optimize-strategy" })`
```

---

## 4. Slash Commands for Rapid Iteration

### Command: `/test-strategy`

Create `.claude/commands/test-strategy.md`:

```markdown
---
name: test-strategy
description: Quick backtest execution for rapid iteration
params: [ticker, timeframe, strategy_name]
---

# Test Strategy Command

Quickly backtest a strategy on specified asset and timeframe.

## Usage

```bash
/test-strategy BTC 1h sma_crossover
```

## Process

1. **Validate Inputs**
   - Check if strategy file exists in `strategies/`
   - Validate ticker format and timeframe

2. **Fetch Data**
   - Check cache in `data/{ticker}_{timeframe}_*.csv`
   - If missing or >24h old, fetch new data from exchange API
   - Save to cache

3. **Run Backtest**
   - Import strategy class
   - Create Backtest instance with:
     - Cash: $100,000
     - Commission: 0.002 (0.2%)
     - Exclusive orders: True
   - Execute backtest

4. **Display Results**
   - Print key metrics table:
     - Return %
     - Buy & Hold %
     - Sharpe Ratio
     - Max Drawdown
     - Win Rate
     - # Trades
   - Generate interactive plot
   - Save results to `backtests/results/{strategy}-{ticker}-{date}.html`

5. **Quick Analysis**
   - Compare to buy-and-hold
   - Flag concerning metrics (Sharpe < 1, Drawdown > 20%, Trades < 30)

## Example Output

```
✅ Backtest Complete: sma_crossover on BTC-1h

📊 Performance Metrics:
   Return:           32.5%
   Buy & Hold:       18.2%
   Sharpe Ratio:     1.45
   Max Drawdown:     12.3%
   Win Rate:         58.2%
   Total Trades:     87

🎯 Verdict: SOLID - Outperforms buy-and-hold with acceptable drawdown
```
```

### Command: `/deploy-strategy`

Create `.claude/commands/deploy-strategy.md`:

```markdown
---
name: deploy-strategy
description: Validate strategy and prepare for live deployment
params: [strategy_name]
---

# Deploy Strategy Command

Comprehensive pre-deployment checklist before going live.

## Usage

```bash
/deploy-strategy opening_range_breakout
```

## Deployment Checklist

### 1. Code Validation ✓
- [ ] Strategy passes all unit tests
- [ ] No hardcoded API keys or secrets
- [ ] Error handling for exchange API failures
- [ ] Proper logging configured

### 2. Backtest Validation ✓
- [ ] OOS performance within 20% of in-sample
- [ ] Tested across multiple timeframes
- [ ] Tested on multiple assets
- [ ] Walk-forward analysis shows consistency
- [ ] Sharpe Ratio > 1.0
- [ ] Max Drawdown < 20%
- [ ] Sufficient trades (>50) for statistical significance

### 3. Risk Management ✓
- [ ] Stop-loss configured
- [ ] Take-profit configured
- [ ] Position sizing limits (max 2% per trade)
- [ ] Daily loss limit (-5% stops trading for day)
- [ ] Maximum open positions (3-5 simultaneous)

### 4. Infrastructure ✓
- [ ] Supabase tables created for trade logging
- [ ] Exchange API keys in environment variables (not code)
- [ ] Webhook alerts configured (Discord/Telegram)
- [ ] Monitoring dashboard set up
- [ ] Backup/recovery plan documented

### 5. Paper Trading ✓
- [ ] Run on exchange testnet for 7 days minimum
- [ ] Monitor for execution errors
- [ ] Verify trade logging to Supabase
- [ ] Confirm alert notifications working

### 6. Legal/Compliance ✓
- [ ] Understand tax implications of crypto trading
- [ ] Human review process for all trades (required)
- [ ] Trade journal for audit trail
- [ ] Position limits documented

## Deployment Workflow

1. Create deployment branch: `git checkout -b deploy/{strategy-name}`
2. Move strategy to `live/deployed_strategies/`
3. Create environment-specific config
4. Set up systemd service or Docker container
5. Enable monitoring and alerts
6. Start with minimal capital ($100-500)
7. Gradual scale-up after 30 days successful operation

## Output

Generates: `live/deployed_strategies/{strategy}/DEPLOYMENT_CHECKLIST.md`

⚠️ **CRITICAL**: Never auto-deploy without human approval
```

### Command: `/sync-trades`

Create `.claude/commands/sync-trades.md`:

```markdown
---
name: sync-trades
description: Pull exchange data and reconcile with local database
params: [exchange]
---

# Sync Trades Command

Fetch recent trades from exchange and update Supabase.

## Usage

```bash
/sync-trades binance
```

## Process

1. **Fetch Exchange Data**
   - Use exchange MCP server or direct API
   - Pull last 24h of executed trades
   - Filter by strategy_id if multiple strategies running

2. **Parse Trade Data**
   - Extract: timestamp, symbol, side (buy/sell), price, quantity, fee
   - Calculate: PnL per trade, cumulative PnL

3. **Update Supabase**
   - Insert new trades into `crypto_trades` table
   - Update `strategy_performance` table with daily metrics
   - Check for duplicates (use trade_id as unique key)

4. **Reconciliation**
   - Compare local Supabase records vs. exchange
   - Flag any missing trades or discrepancies
   - Update UpBank integration for funding flows

5. **Generate Report**
   - Daily PnL summary
   - Win rate today
   - Number of trades executed
   - Current positions

## Example Output

```
🔄 Syncing trades from Binance...

✅ Synced 12 trades from last 24h
📊 Daily Summary (2025-10-23):
   PnL: +$127.50 (+1.28%)
   Trades: 12 (8 wins, 4 losses)
   Win Rate: 66.7%
   Current Positions: 2 open (BTC, ETH)

💾 Updated Supabase: crypto_trades (12 new rows)
```
```

---

## 5. Agent Orchestration Patterns

### Parallel Backtesting with Sub-Agents

Use Claude Code's agent system to run multiple backtests simultaneously:

```python
# Pseudo-code for agent orchestration
Task({
  subagent_type: "task-executor",
  prompt: """
  Run backtests in parallel on the following:

  Agents to deploy:
  1. Agent 1: Backtest sma_crossover on BTC-1h (2024 data)
  2. Agent 2: Backtest sma_crossover on ETH-1h (2024 data)
  3. Agent 3: Backtest sma_crossover on BNB-1h (2024 data)
  4. Agent 4: Backtest mean_reversion on BTC-5m (2024 data)

  Each agent should:
  - Fetch data from cache or yfinance
  - Run backtest with standard config (100k capital, 0.2% commission)
  - Save results to backtests/results/
  - Return summary metrics

  Once all complete, generate comparison report showing which asset/strategy combo performed best.
  """
})
```

### Validation Pipeline with Agent Chain

```
[Agent 1: Data Preparation]
    ↓ (Pass clean data)
[Agent 2: In-Sample Backtest]
    ↓ (Pass baseline metrics)
[Agent 3: Out-of-Sample Test]
    ↓ (Pass OOS results)
[Agent 4: Walk-Forward Analysis]
    ↓ (Pass validation report)
[Agent 5: Generate Recommendation]
```

---

## 6. Integration with backtesting.py Framework

### Adapting Opening Range Breakout to Claude Code

From your reference document, here's how to make the ORB strategy command-driven:

#### Create Strategy File: `strategies/opening_range_breakout.py`

```python
from backtesting import Strategy
import pandas as pd

class OpeningRangeBreakout(Strategy):
    """
    Opening Range Breakout strategy adapted for 24/7 crypto markets.
    Unlike stock markets, crypto trades continuously, so we define
    "market open" as midnight UTC or configurable time.
    """

    # Optimizable parameters
    opening_range_minutes = 15
    sl_pct = 1.0  # Stop-loss %
    tp_pct = 2.0  # Take-profit %
    market_open_hour = 0  # UTC midnight

    def init(self):
        self.daily_high = None
        self.daily_low = None
        self.range_established = False
        self.current_day = None

    def next(self):
        current_time = self.data.index[-1]
        current_price = self.data.Close[-1]

        # Reset daily state
        if self.current_day != current_time.date():
            self.current_day = current_time.date()
            self.daily_high = None
            self.daily_low = None
            self.range_established = False
            if self.position:
                self.position.close()

        # Define opening range window
        market_open = current_time.replace(
            hour=self.market_open_hour,
            minute=0,
            second=0
        )
        range_end = market_open + pd.Timedelta(minutes=self.opening_range_minutes)

        # Calculate opening range
        if market_open <= current_time < range_end:
            if self.daily_high is None or self.data.High[-1] > self.daily_high:
                self.daily_high = self.data.High[-1]
            if self.daily_low is None or self.data.Low[-1] < self.daily_low:
                self.daily_low = self.data.Low[-1]
            self.range_established = True
            return  # Don't trade during opening range

        # Breakout trading logic
        if self.range_established and current_time >= range_end:
            if not self.position:
                # Long breakout
                if current_price > self.daily_high:
                    sl = self.daily_high * (1 - self.sl_pct / 100)
                    tp = self.daily_high * (1 + self.tp_pct / 100)
                    self.buy(sl=sl, tp=tp)

                # Short breakout
                elif current_price < self.daily_low:
                    sl = self.daily_low * (1 + self.sl_pct / 100)
                    tp = self.daily_low * (1 - self.tp_pct / 100)
                    self.sell(sl=sl, tp=tp)
```

#### Command-Driven Testing with `/test-strategy`

```bash
# Quick test
/test-strategy BTC 15m opening_range_breakout

# This automatically:
# 1. Fetches BTC 15-minute data
# 2. Runs ORB strategy with default params
# 3. Displays results + plot
# 4. Saves to backtests/results/
```

#### Optimization with `/optimize-strategy` Skill

```bash
# Invoke optimization skill
Skill({ command: "optimize-strategy" })

# Interactively define ranges:
# opening_range_minutes: 5-60 (step 5)
# sl_pct: 0.5-3.0 (step 0.5)
# tp_pct: 1.0-5.0 (step 0.5)

# System runs:
bt.optimize(
    opening_range_minutes=range(5, 61, 5),
    sl_pct=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
    tp_pct=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
    maximize='SQN',
    constraint=lambda p: p.tp_pct > p.sl_pct
)
```

### Adapting SMA Crossover with Real-Time Data

```python
# strategies/sma_crossover_live.py
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class SMACrossoverLive(Strategy):
    """
    SMA Crossover adapted for live trading with MCP data feeds.
    """
    n1 = 10  # Fast MA
    n2 = 20  # Slow MA

    def init(self):
        close = self.data.Close
        self.sma_fast = self.I(SMA, close, self.n1)
        self.sma_slow = self.I(SMA, close, self.n2)

    def next(self):
        # Golden cross: fast MA crosses above slow MA
        if crossover(self.sma_fast, self.sma_slow):
            if not self.position:
                self.buy()

        # Death cross: slow MA crosses above fast MA
        elif crossover(self.sma_slow, self.sma_fast):
            if self.position:
                self.position.close()

# For live deployment, wrap in MCP-connected real-time loop
# that fetches latest candles via crypto-websocket-mcp
```

---

## 7. Security & Production Deployment

### API Key Management (CRITICAL)

**❌ NEVER do this:**

```python
# BAD: Hardcoded keys in code
BINANCE_API_KEY = "abc123xyz"
```

**✅ ALWAYS do this:**

```python
# GOOD: Environment variables
import os

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
if not BINANCE_API_KEY:
    raise ValueError("Missing BINANCE_API_KEY environment variable")
```

### Secure `.mcp.json` Configuration

```json
{
  "mcpServers": {
    "binance-live": {
      "command": "node",
      "args": ["./mcp-servers/binance-live.js"],
      "env": {
        "BINANCE_API_KEY": "${BINANCE_API_KEY}",
        "BINANCE_SECRET_KEY": "${BINANCE_SECRET_KEY}",
        "TESTNET": "true"
      }
    }
  }
}
```

**Set environment variables in `~/.bashrc` or `~/.zshrc`:**

```bash
export BINANCE_API_KEY="your_key_here"
export BINANCE_SECRET_KEY="your_secret_here"
```

### Pre-Deployment Security Checklist

- [ ] All API keys in environment variables (not code or `.mcp.json`)
- [ ] `.env` files in `.gitignore`
- [ ] API key permissions set to read-only for data fetching (no trading keys in backtest code)
- [ ] Separate API keys for testnet vs. mainnet
- [ ] IP whitelist configured on exchange (if supported)
- [ ] 2FA enabled on all exchange accounts
- [ ] Trade size limits enforced in code
- [ ] Daily loss limits configured
- [ ] Supabase row-level security (RLS) enabled
- [ ] Webhook URLs use HTTPS with authentication

### Production Deployment with Docker

```dockerfile
# Dockerfile for live trading bot
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy strategy code
COPY strategies/ ./strategies/
COPY live/ ./live/

# Non-root user for security
RUN useradd -m -u 1000 trader && chown -R trader:trader /app
USER trader

# Environment variables passed at runtime
CMD ["python", "live/deployed_strategies/opening_range_breakout/main.py"]
```

**Run with secrets:**

```bash
docker run -d \
  --name crypto-trader \
  --env-file .env.production \
  --restart unless-stopped \
  crypto-trading:latest
```

---

## 8. Complete Example Workflow

### End-to-End: Idea → Deployment

#### Step 1: Strategy Creation

```bash
# Invoke create-strategy skill
Skill({ command: "create-strategy" })

# AI prompts: "What strategy concept?"
User: "Mean reversion on Bollinger Bands for BTC on 1-hour timeframe"

# AI generates:
# - strategies/bollinger_mean_reversion.py
# - data fetching script
# - Initial backtest runner
# - README documentation
```

#### Step 2: Initial Backtesting

```bash
# Quick test
/test-strategy BTC 1h bollinger_mean_reversion

# Review results:
# Return: 28.3%
# Sharpe: 1.62
# Max DD: 14.2%
# Trades: 143
```

#### Step 3: Validation Pipeline

```bash
# Invoke validation skill
Skill({ command: "backtest-validate" })

# AI runs:
# 1. In-sample test (70% data)
# 2. Out-of-sample test (20% data)
# 3. Walk-forward analysis
# 4. Multi-timeframe test (1h, 4h, 1d)
# 5. Multi-asset test (BTC, ETH, BNB)

# Output: backtests/validation-reports/bollinger_mean_reversion-2025-10-23.md
# Verdict: PASS - Strategy shows consistency across assets and timeframes
```

#### Step 4: Parameter Optimization

```bash
# Invoke optimize-strategy skill
Skill({ command: "optimize-strategy" })

# AI asks for parameter ranges
# User defines or accepts defaults
# AI runs grid search with walk-forward validation

# Best parameters found:
# bb_period = 20
# bb_std = 2.5
# tp_pct = 1.8
```

#### Step 5: Parallel Multi-Asset Testing

```bash
# Deploy agents in parallel
Task({
  subagent_type: "task-executor",
  prompt: "Run optimized bollinger_mean_reversion on BTC, ETH, BNB, SOL simultaneously"
})

# Results aggregated:
# BTC-1h: 31.2% return, Sharpe 1.71
# ETH-1h: 24.8% return, Sharpe 1.45
# BNB-1h: 19.3% return, Sharpe 1.22
# SOL-1h: 15.7% return, Sharpe 0.98

# Decision: Deploy on BTC and ETH only (Sharpe > 1.4)
```

#### Step 6: Paper Trading

```bash
# Update .mcp.json to use testnet
{
  "mcpServers": {
    "binance-testnet": {
      "env": { "TESTNET": "true" }
    }
  }
}

# Run for 7 days on testnet
# Monitor via Supabase dashboard
# Verify all alerts working
```

#### Step 7: Production Deployment

```bash
# Run deployment checklist
/deploy-strategy bollinger_mean_reversion

# AI validates all checklist items
# Generates deployment documentation
# Creates Docker container config
# Sets up monitoring alerts

# Final approval required from user before live trading
```

---

## 9. Crypto-Specific Considerations

### 24/7 Market Handling

Unlike stocks, crypto markets never close. Adjust strategies:

```python
# Stock ORB: Only trade 9:30 AM - 4:00 PM ET
# Crypto ORB: Define "market open" as UTC midnight or configurable

class CryptoORB(Strategy):
    market_open_hour = 0  # UTC midnight
    end_of_day_hour = 23  # Close positions before daily reset

    def next(self):
        current_hour = self.data.index[-1].hour

        # Close positions before daily reset
        if current_hour == self.end_of_day_hour and self.position:
            self.position.close()
```

### High-Frequency Data Patterns

Crypto exchanges provide 1-minute, 1-second, or even tick data:

```python
# Efficient data caching strategy
import pandas as pd
from pathlib import Path

def fetch_or_cache(symbol, interval, days_back=60):
    cache_file = Path(f"data/{symbol}_{interval}_{days_back}d.csv")

    # Check if cache exists and is <24h old
    if cache_file.exists():
        cache_age = time.time() - cache_file.stat().st_mtime
        if cache_age < 86400:  # 24 hours
            print(f"Loading {symbol} from cache")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True)

    # Fetch fresh data
    print(f"Fetching {symbol} from exchange API")
    data = fetch_from_binance(symbol, interval, days_back)
    data.to_csv(cache_file)
    return data
```

### Exchange API Rate Limits

Implement exponential backoff:

```python
import time
from functools import wraps

def rate_limit_retry(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limited. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@rate_limit_retry(max_retries=5, base_delay=2)
def fetch_trades_from_exchange(symbol):
    # Exchange API call
    pass
```

### Volatility Management

Crypto is 3-5x more volatile than stocks. Adjust risk parameters:

```python
class CryptoStrategy(Strategy):
    # Wider stop-loss for crypto volatility
    sl_pct = 3.0  # vs. 1.0% for stocks
    tp_pct = 6.0  # vs. 2.0% for stocks

    # Smaller position sizes
    max_position_size = 0.02  # 2% of capital per trade

    # Daily loss limit
    daily_loss_limit = 0.05  # Stop trading if down 5% in a day
```

---

## 10. Performance Optimization

### Historical Data Caching

```python
# scripts/fetch_data.py - Run once daily via cron
import yfinance as yf
import pandas as pd
from pathlib import Path

SYMBOLS = ["BTC-USD", "ETH-USD", "BNB-USD"]
INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]

for symbol in SYMBOLS:
    for interval in INTERVALS:
        data = yf.download(symbol, interval=interval, period="60d")
        output_path = Path(f"data/{symbol}_{interval}_60d.csv")
        data.to_csv(output_path)
        print(f"Cached {symbol} {interval}")
```

### Async Patterns for Real-Time Feeds

```python
import asyncio
import websockets
import json

async def binance_websocket(symbol, callback):
    """
    Real-time WebSocket feed from Binance.
    Use this in live trading, not backtesting.
    """
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_1m"

    async with websockets.connect(uri) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            kline = data['k']

            if kline['x']:  # Candle closed
                await callback({
                    'time': pd.to_datetime(kline['t'], unit='ms'),
                    'open': float(kline['o']),
                    'high': float(kline['h']),
                    'low': float(kline['l']),
                    'close': float(kline['c']),
                    'volume': float(kline['v'])
                })

# Usage with MCP integration
async def handle_new_candle(candle):
    # Update strategy with new data point
    # Log to Supabase via MCP
    await supabase_logger.insert('live_candles', candle)

    # Trigger strategy evaluation
    signal = strategy.evaluate(candle)
    if signal:
        await execute_trade(signal)
```

### Database Query Optimization

```sql
-- Supabase table for trade logging
CREATE TABLE crypto_trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL,
    strategy_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(4) NOT NULL, -- 'buy' or 'sell'
    price DECIMAL(20, 8) NOT NULL,
    quantity DECIMAL(20, 8) NOT NULL,
    fee DECIMAL(20, 8),
    pnl DECIMAL(20, 8),

    -- Indexes for fast queries
    INDEX idx_strategy_timestamp (strategy_id, timestamp DESC),
    INDEX idx_symbol (symbol)
);

-- Query recent trades efficiently
SELECT * FROM crypto_trades
WHERE strategy_id = 'bollinger_mean_reversion'
  AND timestamp >= NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC
LIMIT 100;
```

### Resource Management for Long-Running Backtests

```python
import multiprocessing as mp

def run_backtest_parallel(strategies, data):
    """
    Run multiple backtests in parallel using CPU cores.
    """
    with mp.Pool(mp.cpu_count() - 1) as pool:
        results = pool.starmap(run_single_backtest, [
            (strategy, data) for strategy in strategies
        ])
    return results

def run_single_backtest(strategy_class, data):
    bt = Backtest(data, strategy_class, cash=100_000, commission=0.002)
    stats = bt.run()
    return {
        'strategy': strategy_class.__name__,
        'return': stats['Return [%]'],
        'sharpe': stats['Sharpe Ratio'],
        'max_dd': stats['Max. Drawdown [%]']
    }

# Usage
strategies = [SMACrossover, BollingerMeanReversion, OpeningRangeBreakout]
btc_data = fetch_or_cache('BTC-USD', '1h')
results = run_backtest_parallel(strategies, btc_data)
```

---

## Conclusion & Next Steps

### What You've Learned

✅ **Claude Code Architecture** for trading projects using skills, commands, agents, and MCP servers
✅ **backtesting.py Integration** with Opening Range Breakout and SMA Crossover strategies adapted for crypto
✅ **Production Deployment** with security best practices, API key management, and human oversight
✅ **Automation Workflows** from strategy creation → validation → optimization → deployment
✅ **Crypto-Specific Patterns** for 24/7 markets, volatility management, and exchange API handling

### Immediate Action Items

1. **Set up project structure** following recommended directory layout
2. **Configure MCP servers** for crypto data feeds and Supabase logging
3. **Create first skill**: `/create-strategy` for rapid strategy scaffolding
4. **Test with sample strategy**: Run backtesting.py SMA crossover on BTC
5. **Build first command**: `/test-strategy` for quick iteration
6. **Start with paper trading**: Use exchange testnet before live funds

### Resources

- **Claude Code Docs**: [docs.claude.com](https://docs.claude.com)
- **backtesting.py**: [kernc/backtesting.py](https://github.com/kernc/backtesting.py)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Crypto Exchange APIs**: Binance, Coinbase, Kraken official docs
- **Your Reference**: `04-resources/research/trading/A Developer's Guide to Building and Validating Trading Strategies with backtesting.py.md`

---

## ⚠️ Critical Warnings

🚨 **Claude is NOT a trading autopilot** - Always require human review before executing trades
🚨 **Backtesting success ≠ live trading success** - Markets change, overfitting is real
🚨 **Start small** - Test with $100-500 before scaling up
🚨 **Risk management is mandatory** - Stop-losses, position limits, daily loss caps
🚨 **Compliance matters** - Understand tax implications and regulatory requirements
🚨 **Never trade what you can't afford to lose** - Crypto is highly volatile and risky

**"Successful trading depends on using AI responsibly: validate results, keep oversight in place, and align usage with your risk tolerance and regulatory standards."** — Claude 4.1 Trading Guide (2025)
