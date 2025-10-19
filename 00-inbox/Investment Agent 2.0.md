---
type: Note
relation:
tags:
project:
ai-context: false
category: research
research-type:
keywords:
source:
description:
ai-treatment:
  - reference
archive: false
date created: Thu, 10 16th 25, 5:59:19 am
date modified: Thu, 10 16th 25, 6:01:20 am
---
# Designing an Autonomous Crypto Investment Analyst Agent

## Introduction

This technical brief outlines the design of an autonomous Claude-based investment analyst agent (with code execution capabilities) that assists a seed-stage crypto investor. The agent discovers and evaluates early-stage crypto projects from Seedify (a major launchpad) and ByteStreet (Neo Tokyo’s VC platform), using historical context from Citizen Capital (Neo Tokyo’s original community fund). The goal is to create a reasoning framework, data architecture, and toolset that enable the agent to score project quality, assess risks, track investments, and operate with a high degree of autonomy (e.g. sending alerts, monitoring token unlocks, etc.). The focus is on:

#### A robust scoring rubric and decision-making framework (team, tokenomics, market timing, etc.).

#### A structured Supabase data schema and knowledge memory for project info and documents.

#### Integration mechanisms for Seedify and ByteStreet data (project discovery, normalization, backtesting on Seedify’s historical IDOs).

#### Agent autonomy workflows (daily/weekly routines, alert triggers, prompt strategies for Claude).

#### MCP tool design (JSON-based tools like get_price, query_supabase, etc., and how the agent orchestrates them).

#### Evaluation metrics to benchmark the agent’s investment recommendations against real outcomes.


Throughout, we include examples from past Seedify launches to illustrate how the agent’s scoring and risk logic would function in practice.

1. Reasoning and Decision Framework for Evaluation

Goal: Equip the agent with a systematic way to analyze projects and reach investment verdicts. This involves a weighted scoring rubric, explicit red flag heuristics, and a chain-of-thought process (ReAct or Plan-and-Execute) that the agent uses to gather information and reason about an investment decision.

1.1 Weighted Scoring Rubric

The agent uses a multi-factor scoring system to rate each project. Each factor is scored (e.g. 1–10) and weighted by importance to compute an overall score. A proven template from institutional crypto research is to weight Token Utility & Tokenomics highest (≈20%), followed by Technology & Differentiation (≈15%) and Team & Backers (~12%), then factors like Market Addressable Market & Value Proposition (~9%), Growth metrics (~8%), Risks (~8%), Financial Runway (~6%), Partnerships/Ecosystem (~5%), Competition (~5%), Milestones/Catalysts (~4%), Community (~4%), and Market Timing/Technicals (~4%). This weighting reflects that token design and economics often dictate long-term value (inflation, utility, vesting), while team quality and tech edge are also critical.

Scoring Example: Each category has clear criteria for low vs high scores. For instance, Tokenomics gets a high score if the token supply is reasonable with slow unlocks and strong utility, whereas it scores low if founders hold an outsized share or a huge fully-diluted valuation (FDV) with little utility (a red flag). Team scores depend on experience and transparency: a team of known builders with relevant track record scores high, while an anonymous or unproven team scores very low. Tech & Differentiation scores reward real innovation or unique product moats, vs. copycat projects which score poorly. This rubric yields a final numeric score (e.g. 0–10) by applying the weights to each category score. We interpret scores with thresholds (e.g. 8+ = “outstanding, strong buy”, 5 = “average, cautious”, <3 = “high risk, avoid”). Any extremely low (1–3) category score triggers a ⚠️ risk warning, as it indicates a serious weakness (e.g. if Team = 1 due to anonymity, or Tokenomics = 2 due to 50% supply unlocking at TGE). These warnings align with known risk factors, described next.

1.2 Red Flags and Risk Heuristics

In addition to numeric scoring, the agent follows a rulebook of red flags – qualitative heuristics that instantly elevate a project’s risk classification. These red flags are derived from common failure patterns in early crypto projects:

Outlandish Promises – The project makes grandiose claims (e.g. “guaranteed 100x returns” or buzzword-loaded visions) with no technical substance. If it sounds too good to be true, the agent flags it. Legitimate projects focus on solving real problems rather than pure hype.

Anonymous/Shady Team – No information or verifiable identities for founders and developers. Lack of a public, experienced team raises rug-pull risk (the team could disappear with funds, as seen in many scams). The agent treats unverified teams as a major red flag unless there’s a compelling reason (e.g. a well-known pseudonymous developer).

Sketchy Tokenomics – Unfavorable token distribution or supply schedule. For example: a huge percentage of tokens allocated to insiders or a very high FDV relative to the amount raised. The agent checks if a few wallets hold most tokens, or if aggressive unlocks are scheduled that could flood supply. Poor tokenomics (like immediate large unlocks or unclear distribution) are flagged as likely to hurt post-listing performance.

Paid Promotions & Fake Hype – The project relies on astroturfed hype: many social media shills, influencer promotions with no disclosure, “spammy” Telegram groups, etc.. This indicates a pump-and-dump scheme where momentum is artificially manufactured. The agent looks for organic community vs. suspicious bot-like activity.

No Real Use Case – The project doesn’t solve a tangible problem or lacks a clear use for its token. For instance, meme coins or copycat tokens riding trends (AI, Metaverse) without substance. If value depends solely on greater fool theory (selling to someone at a higher price) rather than fundamental utility, the agent marks it as high risk.


These red flags map to the scoring rubric: a project triggering multiple red flags will naturally score low in several categories (e.g. an anonymous team → low Team score; pure hype no use case → low Value Prop and Tech scores). The agent’s risk classification logic could be: if any critical red flag is present, label the project “High Risk – Avoid” regardless of other positives. For example, a project might have a flashy product but if the tokenomics are extremely skewed (say 40% of supply unlocks on day 1), the agent will classify it as high risk and demand extraordinary justification to consider investing.

1.3 Agent Reasoning Model: ReAct vs. Plan-then-Execute

To apply the rubric and investigate each project, the agent uses an LLM reasoning architecture. Two complementary approaches are considered:

ReAct (Reason + Act Loop): The agent iteratively interleaves reasoning steps (“Thought”) with tool use actions (“Act”). It examines the project step-by-step, deciding on one query at a time – e.g. Thought: “I need to verify the token supply and unlock schedule.” → Act: call the get_tokenomics tool → Observation: receives tokenomics data → Thought: “The team allocation is 20% with 1-year lock, seems reasonable… now check the team’s background” → Act: call a web search tool for team info, and so on. This chain-of-thought continues until the agent has gathered enough evidence to score each category and conclude an investment verdict. The ReAct paradigm ensures the agent can dynamically react to findings (for example, if a red flag is observed, it might dig deeper or decide to halt further checks and classify as risky). However, ReAct can be inefficient if the agent takes too many steps one-by-one.

Planner–Executor (Plan-and-Execute): In this mode, the agent first forms a plan of all sub-tasks needed, then executes them in sequence. The planner (a prompting step) might output a list such as: (1) Retrieve project overview from DB, (2) Analyze tokenomics, (3) Check team credentials, (4) Fetch vesting schedule, (5) Compute scores, (6) Output recommendation. Executors then carry out each step (often via tools) without requiring the main LLM for every single action. This approach can be faster and more globally optimal, since the agent “thinks through” the entire task list upfront rather than being shortsighted each step. For instance, the agent might plan to get all necessary data in parallel (or with lightweight calls) and only then have Claude analyze it. After executing, the agent can re-plan if something was missed.


Which to use? We can combine both: use plan-and-execute for routine analyses (where the steps are known in advance) and ReAct for unexpected questions or interactive modes. In practice, the agent might maintain a predefined checklist (plan) for evaluating any new project (covering team, tech, token, etc. as per rubric) – this ensures no aspect is forgotten. Within that, it can still react to intermediate findings (e.g. if the tokenomics tool returns an alarming unlock schedule, the agent might insert extra steps like “verify if an audit report exists” as a reaction). The architecture thus marries the reliability of a plan with the flexibility of reaction.

1.4 Example: Scoring a Past Seedify Project

Consider Paradise Tycoon (MOANI) – a gaming project that launched via Seedify in August 2025. The agent would retrieve that: it raised ~$0.45M across platforms, with an initial public price of $0.0022. Post-IDO performance was poor: the token’s current ROI hovered around 0.88× (–12% below IDO price), with an all-time high of only 1.67× (+67%) before dropping. Using our framework, how would the agent have evaluated it at launch?

Team: If the team was known (e.g. game developers with prior experience) the agent might score this moderate-high. If anonymous or first-timers, it would score low, flagging lack of track record.

Tokenomics: Paradise Tycoon had a total supply of 6 billion tokens and an FDV around $15M – high relative to the ~$2.5M actually raised. The public sale was only ~3.4% of supply, meaning most tokens were locked in private rounds or reserves. The agent would note the risk: a large supply overhang with potential unlock waves. Indeed, with only ~0.5B circulating at launch, any unlocking of the remaining 5.5B could severely dilute price. This likely yields a low Tokenomics score (sketchy distribution) and the agent might tag a red flag for high FDV and low float.

Market Timing: Launching in mid-2025 when overall IDO ROI was averaging <1× on Seedify suggests a tough market. The agent’s Market Timing assessment would be cautious (bearish conditions).

Risk Heuristics: No obvious scam flags were present (assuming the project had a real game in development), but the agent would be wary of execution risk – delivering a complex MMO game is challenging, and many GameFi projects have failed to retain users. So, it might markdown the Execution Risk factor.

Overall: Suppose the agent’s rubric yields an overall score of, say, 5/10 (“mixed”). Key weaknesses like the token supply allocation and market conditions would push the verdict toward “Watchlist/Caution”. In hindsight, this would align with the outcome: Paradise Tycoon struggled post-IDO, validating those risk signals.


Contrast this with a highly successful Seedify project like THE P33L (a meme-themed project incubated by Seedify’s venture arm). THE P33L launched in June 2025 with an ultra-low initial market cap (pre-money valuation ~$250K). Backed by heavy community hype, it skyrocketed to an ATH ROI of ~33.5× (i.e., 3350% gain). Our agent’s rubric would have recognized very different signals here: tokenomics might actually score well (low initial supply in circulation relative to demand), but Risks would also score high because meme projects rely on sustained hype. The agent might have scored P33L as high-risk/high-reward: strong short-term momentum but speculative long-term. This illustrates that a high rubric score does not simply equate to high ROI potential – it balances ROI and risk. The agent could issue a positive short-term outlook on a project like P33L (given community strength) but with caution that it’s a speculative play (e.g. an “Speculative Buy” rating). By tracking many such cases, the rubric can be refined – e.g., identifying that projects in hot narratives (AI, meme, etc.) can overshoot fundamentals in bull phases (30×+ peaks), but also crash hard, so the agent’s framework must handle volatility in its risk assessment (perhaps recommending profit-taking strategies or hedges on very high ROI picks).

2. Data and Memory Architecture

Goal: Provide the agent with a structured long-term memory of projects and a knowledge base for analysis. We use Supabase (Postgres) as the primary database for structured data and integrate a document store for unstructured data (whitepapers, research notes). The design emphasizes high-level schema (what tables and fields to use) and how Claude will retrieve and use this information effectively.

2.1 Supabase Schema Design

We propose a relational schema with tables capturing different aspects of projects and investments:

Projects Table: Stores core info for each project (one row per project). Fields: project_id (PK), name, launchpad (e.g. Seedify, ByteStreet), sector/category (Gaming, DeFi, AI, etc.), description (short summary), website_url, whitepaper_url, status (e.g. upcoming/active/launched). Also include team_info (perhaps a JSON or separate table linking team members’ profiles) and backers (key investors or VCs, as an array or relation to a Investors table). This is the main reference table for project identity.

Tokenomics Table: Stores token and sale info (one-to-one with Projects). Fields: project_id (FK), token_symbol, total_supply, initial_circulating_supply, initial_market_cap (at IDO price), public_sale_price, funds_raised (public round), fully_diluted_valuation (FDV at launch), allocation_breakdown (JSON of % to various categories: team, private, public, liquidity, staking rewards, etc.), launch_date. This allows the agent/tooling to quickly fetch how tokens are distributed – critical for evaluating supply unlock risks. For example, the agent can query: SELECT allocation_breakdown WHERE project_id=X to see if “Team: 20%, Private: 15%, Public: 5%, …”.

Vesting Schedule Table: Stores token release schedules for locked allocations. Each entry: project_id (FK), category (e.g. team, private sale, etc.), unlock_date, amount_or_percent. We might record either absolute token amounts unlocking or percentage of total supply. This table lets the agent answer “when is the next big unlock?” by querying upcoming dates for a project. (Large upcoming unlock events could trigger the agent to issue an alert or downgrade the project score due to imminent sell-pressure.)

Market Data Table: Tracks price and performance over time. Fields: project_id, date, price, market_cap, volume, plus computed ROI_vs_IDO. This table will be updated regularly (e.g. daily prices). It enables the agent to compute current ROI or see trends. For Seedify projects, initial IDO price is known, so ROI = current_price / IDO_price (e.g. 0.5x, 2x, etc.). Historical ROI data can validate the agent’s scoring: e.g. if high-scoring projects average higher ROI over 3 months than low-scoring ones, the model is working.

Scores/Analysis Table: Records the agent’s evaluations. Fields: project_id, evaluation_date, scores for each category (team_score, tokenomics_score, market_score, etc.), total_score, verdict (text like “High risk – avoid” or “Consider investing”), and maybe a notes or rationale field (where the agent’s summary of reasoning is stored for review). Each time the agent analyzes a project (initial or update), a new record can be inserted, creating a history of how assessments change as projects develop.

Investments Table: Tracks the user’s actual investments. Fields: project_id, invest_date, amount_invested, tokens_received, current_value, return_multiple. The agent updates this when an investment is made and can periodically update current_value from price data. This ties into the agent’s monitoring duties (e.g. if ROI drops below a stop-loss or exceeds a take-profit threshold, alert the user).


Relationships: The schema is relational with project_id linking most tables. One project has one tokenomics entry, many vesting entries, many market data points, many score entries, and possibly one investment entry if invested. This design is high-level – actual implementation can refine field types (e.g. using numeric types for prices, etc.), but it captures the needed data for the agent’s logic.

2.2 Document Knowledge Store

Not all information fits neatly into tables. Projects have whitepapers, one-pagers, research reports, and community updates. The agent should leverage these for deeper analysis (e.g. reading a whitepaper for tech details, or scanning an audit report for vulnerabilities). We integrate a simple document store approach:

Document Storage: Use Supabase storage or an external blob store to save PDFs or text of whitepapers and reports. Each file can be tagged with project_id and document type (whitepaper, audit, tokenomics PDF, etc.). We don’t need heavy binary processing in Claude; instead, we pre-process important documents by chunking and summarizing them.

Chunked Summaries & Embeddings: For each important document, we run an offline process (could be a script using Claude or another LLM) to break the text into semantically coherent chunks (e.g. 512-word chunks) and create embeddings. The embeddings (vector representation of each chunk) are stored in a vector index (Supabase offers PG vector extension or use an external service). We also store a short summary of each chunk or section in a Project_Docs table (fields: project_id, doc_type, chunk_id, chunk_text, embedding, summary). This way, when the agent needs specific info (say “token unlock schedule details” or “technical architecture”), it can do a semantic search by embedding similarity to find the most relevant chunk of the document, instead of trying to stuff an entire whitepaper into context.

Retrieval for Claude: When analyzing a project, the agent will retrieve key knowledge: e.g., it can query the DB for the project’s summary and tokenomics (small enough to feed directly into prompt), and for deeper questions it can call a search_documents tool that uses the vector index to fetch the top relevant passages from the project’s docs. Those passages (with citations or source identifiers) can be provided to Claude as additional context to reason over. This pattern (Retrieve-Then-Read) ensures Claude has just-in-time knowledge of specifics without permanently storing large texts in its limited memory.


2.3 Memory and Context Management in Claude

Claude (and similar LLMs) has context length limits, so the agent must manage what information to hold at each turn. The strategy:

Short-Term Memory (Context): While evaluating one project, the agent will keep the key data of that project in the prompt (project name, sector, key stats, and any critical findings). The agent’s chain-of-thought (scratchpad) also lives in context as it works through tools and reasoning. Irrelevant details are dropped. For example, if Claude is analyzing Project X, it doesn’t need details of Project Y in the context (unless comparing). We ensure each evaluation prompt is focused.

Long-Term Memory (Database): Everything else (older analyses, historical performance, details of other projects) is offloaded to the Supabase DB or files. The agent can fetch these when needed via tools. This means Claude doesn’t “remember” past projects unless it explicitly queries for them. This is intentional to avoid confusion and to allow practically unlimited memory through the database. The agent might maintain a profile for each project (in the DB) that includes the latest summary or its last assessment; when re-evaluating, it can retrieve that profile and only feed the condensed info into context.

Updating Knowledge: When projects release new info (roadmap updates, new partnerships), those can be appended to the document store or a News table. The agent can be triggered to incorporate those updates: e.g., it could generate an updated summary and replace the old one in the Projects table or add a new entry in Scores table with the date.

Avoiding Information Staleness: The agent should timestamp data fetches. If it’s been a while (say 1 week) since token prices or social metrics were updated for a project, the agent will know to refresh them via tools (like get_price). This ensures the analysis is always using up-to-date information, which is crucial in crypto where things change fast.


In summary, the data architecture provides a single source of truth for structured info (Supabase) and a lightweight knowledge retrieval system for unstructured info, enabling Claude to reason with relevant data on demand without exceeding its context limits.

3. Integration with Seedify and ByteStreet Data

Goal: Ensure the agent can discover new projects and ingest data from Seedify and ByteStreet consistently. Also, leverage historical data from Seedify for calibrating the agent (backtesting the rubric), and use Citizen Capital’s history to inform ByteStreet’s focus.

3.1 Project Discovery & Data Normalization

Seedify Integration: Seedify, being a public launchpad, regularly announces IDOs on their website or Medium blog. We can integrate via:

RSS/Feed or API: Check if Seedify offers an RSS feed or an API for upcoming launches. If not, a web scraper can periodically parse the Seedify Launchpad site (e.g. a page listing “Upcoming IDOs” or their Medium announcements). Key data to extract: project name, token symbol, IDO date, initial price, raise amount, and links to more info (whitepaper, etc.). For example, if Seedify announces Project A IDO on Oct 30, the scraper grabs the details and triggers the agent to create a new entry in the Projects and Tokenomics tables.

Normalization: Different sources may have data in varying formats. The agent (or a preprocessing script) normalizes it to our schema. E.g., Seedify might list “Hard cap: $200k, Initial market cap: $500k, Price per token: $0.05, Vesting: 20% at TGE, rest linear over 6 months.” The agent would split these into structured fields (public_sale_price=0.05, initial_circulating_supply = (20% of total supply), etc.). For now, this can be handled with rule-based parsing or prompts that extract structured data from text (Claude can be good at parsing descriptions into JSON).


ByteStreet (Neo Tokyo) Integration: ByteStreet is a community VC platform for Neo Tokyo NFT holders (evolved from Citizen Capital). It likely operates through Discord or gated channels rather than a public site, but we know its purpose is to “fund innovators of Neo Tokyo”. Integration options:

If ByteStreet has a newsletter or X (Twitter) announcements (the handle @NTLaunchpad or @ByteStreet on X), we can monitor those feeds. For instance, the agent might scrape announcements like “ByteStreet is investing in Project B – a DeFi startup, raising $500k...” and then gather details (perhaps via a deal memo PDF).

Manual Input: Given ByteStreet deals might be semi-private, initially an analyst might manually input deal info into the system (project name, summary, allocation for our investor, etc.). Over time, if ByteStreet uses a standardized platform, we could connect via API or webhook.

Normalization with Citizen Capital context: Citizen Capital (the predecessor fund) had a certain style of deals – mostly seed-stage investments in gaming/metaverse projects (e.g. Midnight Society game studio, Heroes of Mavia MMO, etc.). ByteStreet likely follows suit. We can prepare the agent with contextual knowledge: a list of past Citizen Capital investments and outcomes. For example, Citizen Capital invested in SupraOracles and Nillion in 2022. If data is available (perhaps from RootData or community posts), we can note how those fared (SupraOracles eventually did a token sale; Nillion raised Series A etc.). This historical context can guide ByteStreet evaluations – e.g. if ByteStreet announces a deal similar to a past one, the agent can draw parallels (“This project resembles Heroes of Mavia, which Citizen Capital backed – a game that faced delays; consider execution risk”).

Citizen Capital Portfolio Data: For backtesting, we could compile the list of Citizen Capital portfolio companies and track if they launched tokens or products. This isn’t directly required, but it enriches the agent’s knowledge base to have seen many examples (more “training data” in a sense). It could even be used to augment the rubric: if Citizen Capital’s successful exits had certain traits, incorporate those as positive signals.


3.2 Historical Seedify IDO Data & Backtesting

Seedify has a rich history: over 130 IDOs since 2021. We have metrics like average ROI, ATH ROI, etc. By pulling historical performance data, we can validate and fine-tune the agent’s scoring model:

Data Sources: We will use sources like CryptoRank and ChainBroker which track launchpad performance. For instance, CryptoRank shows that in the last 6 months, Seedify’s average current ROI is only ~0.65× (i.e., most projects are below their IDO price now), while the best performers reached ~6.77× ATH in that period. It also lists top projects by ROI (e.g. AI-focused projects like THE P33L reached 33×, others 16–31×). We can ingest a dataset of each Seedify project: name, date, sector, and actual ROI outcomes (ATH ROI, current ROI, etc.).

Backtesting the Rubric: Using that dataset, simulate the agent’s rubric on each project as if evaluating at launch. This requires some known inputs (team known vs unknown, tokenomics distribution, etc.). Some of this information can be scraped from announcement archives or ICO tracking sites (e.g. initial allocation charts). The agent (or an offline script) can assign approximate rubric scores to each past project, then correlate with outcomes:

Did projects that scored high indeed achieve higher ROI or sustain price better?

Did low-scoring (or red-flagged) projects often flop or rug-pull?

Use statistical measures like the Spearman correlation between score and ROI, or group projects by score tier to see average ROI per tier.

This backtest can help adjust weights: e.g., if “Team” score wasn’t strongly correlated with short-term ROI but “Tokenomics” was, we might keep Tokenomics weight high for predicting initial performance. Or if Community hype was critical for mega-pumps, perhaps include a metric for social traction.


Example Insight from Data: Suppose we find that GameFi projects on Seedify in 2022 had an average ROI of 0.5× (many failed post-IDO), whereas AI projects in 2023 averaged 5× (big hype). The agent can internalize this: certain sectors or launch timing windows matter. It might develop a heuristic like “adjust base score +1 if sector is currently hot and market sentiment is strong” or conversely a penalty if launching in a saturated trend at the tail end.

Continuous Learning: Even after deployment, the agent will keep logging its predictions vs outcomes. This allows refining the model. For instance, if the agent gave a “Buy” verdict to five projects and only two succeeded while three tanked, analyze why. Perhaps one red flag was overlooked – incorporate that next time. The framework thus evolves with more data (this bleeds into the Evaluation section in part 6).


3.3 ByteStreet and Citizen Capital Context

Citizen Capital Historical Context: As noted, Citizen Capital was the official Neo Tokyo community fund, requiring NFT holders to stake BYTES tokens to participate. It invested via a raffle system in seed rounds of projects (often private equity or SAFT deals). The agent doesn’t directly invest in these (since they’re not public tokens yet), but it’s tracking them. ByteStreet appears to be the next evolution: “built to fund the innovators of Neo Tokyo”, presumably opening investments to the community. The agent’s integration here means:

It tracks any deal memos or announcements from ByteStreet. This could be things like “ByteStreet deal: Project C – a Web3 startup raising $1M at valuation X; NeoTokyo allocation: $100k.” The agent would log Project C, perhaps with less quantitative data (since pre-token deals may not have a tokenomics chart yet, just equity or SAFT terms). It can still assess qualitatively (team, idea, market).

Monitoring to Token Event: Many VC deals eventually lead to a token generation event (TGE) or listing. The agent should watch these ByteStreet portfolio projects for when/if they launch a token or product. For example, if ByteStreet invested in Nillion (as Citizen Capital did) and Nillion plans a token sale in 2024, the agent should update that project’s info with tokenomics once available. Essentially, ByteStreet deals might be long-term holds, but the agent’s job is to keep them on the radar (autonomously checking for news like “Project C announced token launch date” – possibly by following their Twitter or blog via a tool).

Neo Tokyo Community Factors: Neo Tokyo has an engaged investor community. Sentiment or involvement from that community can itself be a factor. If a project is being accelerated by Neo Tokyo (via ByteStreet), it likely gets community support (initial buyers, users). The agent could factor this into scoring: e.g., a ByteStreet-backed project might get a slight boost in Community score because hundreds of NT citizens are aware of it and possibly evangelizing it. On the flip side, the agent should ensure not to be biased just because of community affiliation – it should still apply independent analysis (one could imagine the agent diplomatically handling the fact that the user is a Neo Tokyo citizen but still wants objective insight).

Data Sources for ByteStreet: Since ByteStreet is new, we might set up integration to Neo Tokyo’s “Citadel” Discord (if allowed via API) to scrape any announcements. Alternatively, ByteStreet may use a web platform (maybe an evolution of citizencapital.fund) – we’d integrate similarly to Seedify by scraping. In absence of that, the user manually feeding ByteStreet deal info into the system may be simplest initially, then gradually automate.


In summary, the agent’s integration approach: scrape and import public data for Seedify, use community sources/APIs for ByteStreet (with manual backup), and lean on historical databases (like cryptorank, Citizen Capital records) to enrich its analyses and validate its logic.

4. Agent Autonomy and Workflow

Goal: The agent should operate continuously and proactively – not just responding to one-off queries, but performing daily/weekly tasks, issuing alerts, and updating analyses as new data comes in. We outline key workflows and how to implement them in Claude with proper prompting.

4.1 Daily Workflow

Every day (or even multiple times a day), the agent can execute an automated routine, for example at 9:00 AM:

New Project Scan: Check for any new project announcements on Seedify and ByteStreet. This could involve calling a check_new_projects tool (which checks RSS feeds or relevant webpages). If new projects are found, the agent will initialize entries in the database and perhaps generate a brief preliminary report. For Seedify, it might find “Project X IDO announced for next week” – it then scrapes initial details and stores them. For ByteStreet, it might find “ByteStreet deal for Project Y opened” – it logs that too.

Price and ROI Update: The agent calls update_prices (or get_price per project) to fetch latest market prices for all tokens in the portfolio or watchlist. Using the Market Data table, it records new prices and calculates today’s ROI vs initial. This is used for monitoring: e.g., if any token’s price moved significantly (say +20% or -20% in a day), it could flag this in an alert.

Trigger Checks: The agent then evaluates if any conditions are met that require action:

Token Unlock Alerts: It queries the Vesting Schedule table for any unlock events happening in the next few days. If found (e.g. “Project A team tokens unlocking tomorrow (5% of supply)”), it generates an alert to remind the investor that a price impact could occur.

Stop-Loss/Take-Profit: It checks the Investments table. For each holding, compute ROI or % change over last X days. If an investment’s ROI falls below a threshold (e.g. 0.5×, or -50% from cost), it alerts “Investment in Project Z is down 50% – reassess if you want to hold.” Likewise if something mooned above target (e.g. 5×), alert to possibly take profits or at least acknowledge the big gain.

News & Social Sentiment: If possible, integrate a tool to fetch social media mentions or project news. The agent could check each active project for news (Twitter, Discord, etc.). If a project suddenly trends (lots of mentions or a big partnership announced), the agent can surface that (“Project Y announced a major exchange listing – could be a price catalyst”).


Summary Report: After performing updates, the agent could compile a brief summary (for the user or for its own log) of the day’s notable events: e.g. “No new projects today. All investments steady except Project X (-12%). Upcoming unlock: Project Y on Oct 20. Noteworthy news: Project Z released testnet. Portfolio ROI is +5% overall.” This can be delivered via email or chat to the user, or just stored.


All these tasks can be done without user prompt – essentially a cron-job triggers Claude with a system prompt like: “You are an autonomous agent updating the crypto investment dashboard. Perform the daily checks and output alerts as needed.” Within that run, the agent uses tools to gather data and then outputs the summary/alerts.

4.2 Weekly Deep-Dive & Re-Evaluation

On a weekly basis (say every Friday), a more thorough routine occurs:

Project Re-scoring: The agent selects projects that had significant changes (price movement, product updates, etc.) and re-runs the full evaluation rubric on them. For example, if a project launched its mainnet or if its token unlocked a large tranche, the risk profile changes. The agent uses the stored data plus any new info to update category scores. These new scores are stored (so we have a timeline of score changes).

New Launch Analysis: For any IDO that happened that week (projects that went from upcoming to live), the agent does a “post-mortem” analysis. E.g., if Seedify had 3 IDOs this week, the agent checks how they performed (did they pump or dump?) and notes any lessons (perhaps feeding this into the evaluation model improvement). It can also backfill actual data like final raise amounts and initial ROI to the DB.

Market Overview: The agent might also look at macro conditions (fear/greed index, overall market trend) and record a qualitative note like “Market is bullish this week, high appetite for new IDOs – consider that in upcoming evaluations”. This helps contextualize its decisions.

ByteStreet Deal Follow-ups: If ByteStreet made an investment in a project, the agent might do a deeper research on that project over the week (reading its whitepaper, evaluating its tech similar to how one would for an IDO). Essentially, treat it as due diligence for a venture investment. The output could be a detailed memo stored in the Project_Docs or Scores table.


These weekly tasks ensure the agent stays up-to-date and continues learning. The key is scheduling and triggers. Using a combination of cron triggers and in-prompt logic (like checking timestamps of last eval), the agent will know what to do each week.

4.3 Prompt Engineering for Autonomous Operation

Designing prompts for autonomous cycles is crucial so that Claude knows its objectives each time without direct user input:

System Prompt: We will craft a system-level prompt that defines the agent’s role and high-level policy. For example: “You are an AI investment analyst for early-stage crypto projects. Your duties include: monitoring new project launches, updating database info, scoring projects on a rubric, and alerting the user to important changes. Always explain reasoning and provide data. You have tools (DB queries, web fetch, etc.) to assist. When unsure, log the uncertainty but attempt to find an answer via tools.” This serves as a constant guideline.

Contextual Instructions: For specific workflows, the user prompt (or an injected assistant prompt from the scheduler) will specify the task. E.g., the daily job prompt might say: “Today’s date is X. Perform daily monitoring tasks as per your role. Output any alerts or updates for the user.” The weekly prompt might instruct a thorough re-evaluation focus.

Chain-of-Thought Management: We allow Claude to use a scratchpad in the conversation to reason step by step (as per ReAct/Plan). We might include something like: “Use the tools available to gather information. Show your reasoning process (in a hidden scratchpad) and final outputs as clear summaries for the user.” In practice, if using something like LangChain, the scratchpad is not shown to end user, but logs for us. We’ll ensure to use the formatting that the agent expects for tool use, e.g., in JSON or a special syntax per the MCP framework.

Limit Instructions for Each Run: Each autonomous run should have a clear end condition. For example, “Stop when you have compiled the daily summary or if no significant events.” This prevents the agent from going off-track or looping indefinitely. If the agent has nothing to do (no news, no changes), it can output “No significant updates today.” and finish.

Error Handling in Prompts: We also instruct the agent what to do if a tool fails or data is missing (like a try-catch). E.g., “If a data source is unavailable, note it in your log and skip that step.” This is important for robustness (e.g. if the Seedify site is down one day, the agent shouldn’t get stuck – it should try later or proceed with what it has).

Safety and Bias Instructions: Since this agent deals with financial advice area, we include a note: “You provide analysis and suggestions, but never guaranteed financial advice. Always include rationale and highlight uncertainties.” This ensures the agent’s outputs to the user remain measured (like saying “high risk” instead of “definitely will moon”).


By carefully constructing these prompts and combining with the agent’s tool abilities, we achieve an autonomous workflow where Claude essentially acts as a diligent virtual analyst on a schedule, with minimal human prodding.

5. MCP Tooling Design and Orchestration

Goal: Define the set of tools (functions/operations) the agent will use, including their inputs/outputs as JSON schemas, and illustrate how the agent orchestrates them during its reasoning process. These tools allow Claude to extend beyond text generation into actions like querying the database or external data.

5.1 Key Tools and JSON Schemas

We identify the primary tools the agent will need:

query_supabase – Database Query Tool. This allows the agent to run parameterized queries on the Supabase database. We might restrict it to read-only SELECT queries on specific tables to avoid complexity. Input schema: a JSON with fields like table, filter (a condition or key), and maybe fields to select. For example: {"table": "Projects", "filter": {"name": "Paradise Tycoon"}} could return the row for that project. The tool’s output would be the query result in JSON (or a formatted table). We will implement some templated queries too, e.g., get_vesting(project_id) that internally does SELECT * FROM Vesting WHERE project_id=X. But conceptually, query_supabase covers any DB retrieval. Schema example:


{
  "name": "query_supabase",
  "description": "Query the project database for specific information.",
  "parameters": {
    "type": "object",
    "properties": {
      "table": {
        "type": "string",
        "description": "Name of the table to query (Projects, Tokenomics, Vesting, MarketData, etc.)."
      },
      "filter": {
        "type": "object",
        "description": "Filter conditions to apply (e.g. {\"project_id\": 123} or {\"name\": \"ProjectX\"})."
      },
      "fields": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Optional list of fields to retrieve (defaults to all)."
      }
    },
    "required": ["table","filter"]
  }
}

This schema means the agent can call e.g. query_supabase with a JSON argument specifying which table and filters. The tool will respond with data.

get_price – Price/Market Data Tool. This tool fetches the latest price (and perhaps market cap/volume) for a given token symbol from an API (or our own price DB). Input: {"symbol": "TOKEN"}. Output: the price and perhaps 24h change or ROI vs initial (the tool could compute ROI if it looks up the IDO price from DB). Example usage: get_price{"symbol": "MOANI"} returns {"price": 0.0019, "24h_change": -5%}. We might integrate a third-party API (CoinGecko or CMC) for real-time prices via this tool.

get_tokenomics – Tokenomics Summary Tool. This could encapsulate fetching tokenomics info either from the DB or from a live source (like reading a Medium post or whitepaper if not in DB). Likely easier is to implement it as a DB lookup that returns the tokenomics table entry for a project (so essentially a wrapper around query_supabase for the Tokenomics table). Input: {"project_id": X} or {"name": "ProjectX"}. Output: structured token distribution and vesting info. Example output: {"total_supply": 1000000000, "initial_circulation": 100000000, "team_alloc": "15%, 12 months lock", "public_alloc": "5%, no lock", ...}. This saves the agent from manually interpreting raw numbers; the tool can pre-format the data.

search_documents – Knowledge Retrieval Tool. Input: {"project_id": X, "query": "vesting schedule"}. This tool would perform an embedding search on stored docs for that project, returning the most relevant text snippet (and source if needed). For instance, if asked about “team background”, it might retrieve a paragraph from the whitepaper’s team section. The output could be {"text": "...snippet from doc...", "source": "whitepaper.pdf#section5"}. The agent can then incorporate that info into its reasoning (with a citation in the final answer if output to user).

web_search or web_fetch – If the agent needs info not in the database (like checking Twitter or latest news), a generic web search tool could be provided. Input: {"query": "ProjectX latest partnership"}. Output: search results or scraped content. However, web access might be limited for our agent’s environment, so this tool’s use could be moderated. We might rely mostly on pre-fed data to reduce unpredictability. But it’s good to design one for extensibility.

notify_user – Alert/Notification Tool. Rather than always printing alerts, we could have a tool that directly sends a notification (email, etc.). Input: {"message": "Your investment in ABC dropped 20% today."}. For design completeness, mention it, though it’s more an integration point than an analytical tool.


Each tool will have a defined JSON schema as above, ensuring the agent calls it with the correct params. The MCP (function calling) interface in Claude will handle taking these JSON inputs and returning JSON outputs for the agent to parse.

5.2 Tool Orchestration Examples

To illustrate how the agent uses these tools in practice, consider a scenario:

Scenario: The user asks, “Evaluate the new Seedify project ‘XYZ’ and should I invest?” (Or the agent autonomously picks up ‘XYZ’ as new and needs to evaluate.)

Agent thought process (ReAct style):

1. Thought: “First, I need basic info on XYZ (tokenomics, team, etc.).”
Action: query_supabase with {"table": "Projects", "filter": {"name": "XYZ"}} – to retrieve any stored info (maybe the scraper already saved some).
Observation: The tool returns: {"name": "XYZ", "sector": "DeFi", "launch_date": "2025-11-01", "website": "...", "description": "...", "project_id": 42}.


2. Thought: “Got the project profile. Next, check tokenomics details.”
Action: query_supabase with {"table": "Tokenomics", "filter": {"project_id": 42}}.
Observation: Returns: {"total_supply": "100M", "public_price": "$0.10", "initial_mcap": "$1M", "allocation_breakdown": {"Public":10%, "Team":20% (12m lock), "Private":15% (3m cliff)...}, ...}.


3. Thought: “Tokenomics show team has 20% locked 12 months – that’s fairly standard; private 15% with 3-month cliff – need to note that unlock. Let’s see the vesting schedule for details.”
Action: query_supabase with {"table": "Vesting", "filter": {"project_id": 42, "category": "Private"}}.
Observation: Returns a list of unlock events, e.g., [{ "unlock_date": "2026-02-01", "amount_percent": 15%}, {...}]. The agent parses that the private sale tokens (15%) unlock starting 3 months after TGE. It flags a calendar note internally.


4. Thought: “What about the team? Is the team known?”
If the Projects table had a team_info field with names, the agent might see names. If names are present, it could then verify them via web:
Action: web_search with {"query": "XYZ project founder Alice crypto background"}.
Observation: The search might return a bio or LinkedIn info like “Alice – former CTO at KnownDeFi, etc.” The agent would extract relevant credibility info.

If the team was blank/anonymous, that itself is a warning sign. The agent would note: “Team unknown – red flag.”


5. Thought: “Check if an audit exists or any red flags in whitepaper.”
Action: search_documents with {"project_id": 42, "query": "audit"}.
Observation: Suppose it finds no mention of audit in docs (meaning likely no audit done). That’s another risk flag to mention.


6. Thought: “Now I have enough info. Let me apply the scoring rubric.”
(No tool, just internal reasoning – or it could call a score_project pseudo-tool that implements the rubric calculation based on gathered data. But it can also just reason it out and then maybe store via query_supabase inserting into Scores.)

The agent would assemble something like:

Team: 5/10 (some experience but not well-known)

Tech: 7/10 (idea is solid, using new AI-DeFi approach)

Tokenomics: 6/10 (decent distribution, though private unlock in 3 months is a risk)

Market Timing: 8/10 (launching in bull market, good community buzz)

etc., and then weighted sum to final ~6.5/10.



7. Thought: “Any immediate recommendation? Possibly a moderate buy with caution on unlocks.”
The agent compiles the final answer to user: a summary of project, the scores, and verdict, including references to data (as we have in DB or from docs). E.g.: “Project XYZ is a DeFi platform doing X. The team has relevant experience (ex-CTO of Y) but not high-profile【citation】. Tokenomics are fairly standard, with a $1M initial market cap and moderate investor allocation (15% private with a 3-month cliff) – this raises some risk of sell pressure after the cliff【citation】. No security audit is mentioned, which is a concern. Considering these factors, I’d score XYZ around 6.5/10. It has potential, but also a couple of red flags (team anonymity and upcoming unlock). The recommendation is to invest cautiously if at all, perhaps a small amount, and be prepared for volatility around February when private tokens unlock.”

This answer would be returned to the user, with the agent’s reasoning trace hidden.



Autonomous use: In an autonomous daily run, the agent’s orchestration is similar but without a user query. For example, a daily check might involve:

Calling query_supabase to get all projects with an upcoming TGE date in next 7 days, then for each, call get_tokenomics to see if any immediate unlock at TGE (if, say, 40% unlock at TGE, that’s a note to caution).

If a token’s price fell, calling get_price and comparing to stored last price.

If it decides to alert, using notify_user or just preparing an output.


All these sequences demonstrate how tools enable the agent to act autonomously and deterministically for data-related tasks, while Claude’s language and reasoning ability wraps around those calls to interpret and decide.

6. Evaluation and Benchmarking

Goal: Establish how we will measure the agent’s performance and the usefulness of its predictions. This is crucial since we need to trust an autonomous agent with investment decisions. We define metrics and methods to regularly evaluate the agent against real outcomes.

6.1 Benchmarking Agent’s Investment Decisions

We will compare the agent’s verdicts vs. actual project outcomes over time:

Return on Investment (ROI): A primary metric. For each project the agent scores/recommends, track the actual ROI after certain time frames (e.g. 1 month after TGE, 3 months, 6 months). If the agent labeled a project as “High potential” or gave a high score, did it achieve higher ROI than those it labeled “Avoid”? Ideally, we’d see a positive correlation: projects the agent liked should, on average, outperform those it didn’t. We can visualize this: plot agent score vs. actual ROI, look for an upward trend. If there’s no correlation or negative, the scoring needs adjustment.

Success Rate / Hit Rate: Define what a “success” is (e.g. a project that maintains >1× ROI or that doesn’t crash/rug within 3 months). Calculate the percentage of successes among those the agent recommended vs. those it said to avoid. For example, if the agent green-lit 10 projects and 7 are successful, that’s a 70% hit rate; if it rejected 10 and 9 of those indeed failed (only 1 surprise success), that’s a good avoidance rate.

Precision and Recall (Classification): We can treat the agent’s decision as a binary classifier (“invest” vs “don’t invest”). Then measure precision (of those it said invest, how many turned out good) and recall (of all good projects, how many did it identify). There’s a trade-off: a very conservative agent might have high precision (only invests in sure winners) but low recall (misses many good opportunities). We might prefer a balanced approach for a seed investor to not miss big winners. We can tune the decision threshold (the rubric score cutoff for “invest”) to find an optimal balance historically.

Risk Assessment Accuracy: Another angle is how well the agent’s risk flags predict volatility or drawdowns. For instance, if the agent flagged “large unlock in 3 months” as a risk, does the token indeed drop around that time? Tracking such specific events can validate the agent’s heuristics. If the agent consistently catches problematic tokenomic structures (which then lead to poor performance), that’s a strong indicator it’s correctly identifying risk. Conversely, if it throws red flags that later prove false alarms, we examine why.

Portfolio Outcome: If the user were to follow the agent’s advice for all investments (perhaps simulate an agent-guided portfolio), what would the performance be? We can simulate investing a fixed amount in every project the agent says “invest” (at IDO price), and not investing in those it says “avoid”. Then track the value of this simulated portfolio over time compared to if we invested in all projects equally or random selection. Ideally, the agent-guided portfolio has a higher ROI or at least lower volatility/less severe losses. Metrics like Sharpe ratio (return vs volatility) could be applied to gauge risk-adjusted performance.

Qualitative Feedback: Since the agent’s outputs include rationales, we can occasionally do human-in-the-loop evaluations. A domain expert can read some of the agent’s reports and verify if the reasoning is sound or if any important factor was missed. This helps catch any blind spots that pure outcome metrics might not show (for example, the agent might get a few right for the wrong reasons, or vice versa).


6.2 Continuous Improvement Metrics

The agent should improve as it gains more experience/data. We set up metrics to track improvement:

Time-to-Decision & Coverage: Measure how quickly and how many projects the agent is able to cover. If at launch it covers 80% of Seedify projects and misses some, aim to reach 100%. Also, ensure it’s catching ByteStreet deals in a timely manner (e.g. ideally analysis ready before the token launch or significant event).

Alert Accuracy: For the automated alerts (like unlock alerts or price alerts), check if acting on those alerts would have been beneficial. For example, if an alert warned of a big unlock and indeed the price dropped X% after unlock, that’s a “true positive” alert. If it alerted and nothing happened (false positive), fine-tune criteria to reduce noise.

User Engagement: If this agent is used interactively, track which of its suggestions the user followed and whether they express satisfaction. Perhaps incorporate a feedback tool where the user can rate the agent’s advice after the fact (“Was this analysis helpful? Did the investment meet expectations?”). This qualitative feedback can be turned into a score for the agent’s service quality.

Benchmark Against Simpler Strategies: It’s important to justify the agent’s complexity. We might benchmark against simpler baselines, e.g. investing in every Seedify project (naive baseline), or invest only if project ROI at ATH >5× (a hindsight Oracle, not realistic real-time). Our agent should aim to beat the naive baseline in returns, or at least significantly reduce downside risk while capturing most upside.


If the agent underperforms or has biases, we iterate: adjust rubric weights, add new data features (maybe the agent needs to consider social media metrics more, etc.), or improve the training (maybe few-shot examples in the prompt of good analysis). The evaluation loop ensures the agent doesn’t remain static – it adapts to new market trends. For example, if a new pattern emerges (say, community fair launches with no private VCs become popular in 2025, changing the risk dynamic), the agent’s criteria should evolve (perhaps lower weight on “VC unlock risk” in such cases and more on community engagement).

Finally, we must consider what metrics indicate a “useful predictive signal.” In finance, even the best models won’t be 100% right, but if our agent can consistently tilt odds in favor of the investor – e.g. avoid most scams and catch some big winners – that’s highly useful. A possible metric: annualized portfolio return if following the agent vs. if not. If the agent’s guidance yields a positive ROI in a flat market or beats the launchpad average ROI by a good margin, it’s adding value. Another metric: drawdown – did the agent help avoid catastrophic losses (e.g. not investing in any of the projects that went to near-zero)? If yes, it’s acting as a good risk manager.

In summary, evaluation is multi-faceted: a mix of quantitative performance metrics, classification accuracy, and qualitative sanity-checks. We will use these to refine the agent. Over time, the goal is that this autonomous Claude agent becomes an indispensable analyst, with a track record that earns the user’s trust (e.g. after 6 months, user sees that projects rated 8/10 by the agent have an average +50% ROI, while those rated 3/10 often failed – a clear signal the scoring has predictive power).


---

Sources: The design choices above are informed by best practices and data from crypto launchpads and Neo Tokyo’s community: for instance, institutional research rubrics weighing tokenomics and team heavily, common crypto investment red flags, the success metrics of Seedify’s IDOs (average ROIs and top performers like THE P33L at 33×), and the context of Citizen Capital’s approach within Neo Tokyo. This ensures the agent’s framework is grounded in real-world crypto investment experience and quantitative outcomes.

