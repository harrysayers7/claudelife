#!/usr/bin/env node

/**
 * Enhanced UpBank to Supabase Sync Script
 * With comprehensive error handling, recovery, and monitoring
 */

const { createClient } = require('@supabase/supabase-js');
const { v4: uuidv4 } = require('uuid');

// Configuration
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://gshsshaodoyttdxippwx.supabase.co';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
const UPBANK_TOKEN = process.env.UPBANK_API_TOKEN;

// Error types
const ErrorTypes = {
  AUTH: 'AUTH_ERROR',
  RATE_LIMIT: 'RATE_LIMIT',
  NETWORK: 'NETWORK_ERROR',
  DATABASE: 'DATABASE_ERROR',
  DATA_INTEGRITY: 'DATA_INTEGRITY',
  CONSTRAINT_VIOLATION: 'CONSTRAINT_VIOLATION',
  UNKNOWN: 'UNKNOWN_ERROR'
};

// Validate environment
if (!SUPABASE_SERVICE_KEY) {
  console.error('❌ SUPABASE_SERVICE_ROLE_KEY environment variable is required');
  process.exit(1);
}

if (!UPBANK_TOKEN) {
  console.error('❌ UPBANK_API_TOKEN environment variable is required');
  console.log('📝 To fix:');
  console.log('1. Go to https://api.up.com.au');
  console.log('2. Generate a personal access token');
  console.log('3. Add to ~/.zshrc: export UPBANK_API_TOKEN="your_token"');
  console.log('4. Run: source ~/.zshrc');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

/**
 * ML Pipeline Integration for Automatic Transaction Categorization
 * Integrates with MindsDB models for real-time financial intelligence
 */
class MLPipeline {
  constructor() {
    this.models = {
      categorizer: 'transaction_categorizer',
      anomalyDetector: 'anomaly_detector',
      vendorClassifier: 'vendor_classifier'
    };
    this.confidenceThresholds = {
      auto: 0.9,      // Auto-apply categorization
      review: 0.7,    // Suggest with review
      manual: 0.0     // Manual categorization required
    };
  }

  /**
   * Get AI-powered transaction categorization
   */
  async categorizeTransaction(transaction) {
    try {
      // Prepare features for ML model
      const features = {
        description: transaction.description || '',
        amount: Math.abs(transaction.amount_cents) / 100,
        vendor_name: this.extractVendor(transaction.description),
        account_type: transaction.account_type || 'unknown'
      };

      // Query MindsDB transaction categorizer
      const { data: prediction, error } = await supabase.rpc('predict_transaction_category', {
        p_description: features.description,
        p_amount: features.amount,
        p_vendor_name: features.vendor_name
      });

      if (error) {
        console.warn('ML categorization failed, using fallback:', error.message);
        return this.getFallbackCategory(transaction);
      }

      if (prediction && prediction.length > 0) {
        const result = prediction[0];
        return {
          category: result.ai_category,
          confidence: result.ai_confidence || 0,
          method: 'ml_prediction',
          model_used: this.models.categorizer,
          features_used: Object.keys(features)
        };
      }

      return this.getFallbackCategory(transaction);

    } catch (error) {
      console.warn('ML Pipeline error:', error.message);
      return this.getFallbackCategory(transaction);
    }
  }

  /**
   * Detect anomalies in transactions using ML
   */
  async detectAnomalies(transaction) {
    try {
      const { data: anomaly, error } = await supabase.rpc('detect_transaction_anomaly', {
        p_description: transaction.description,
        p_amount: Math.abs(transaction.amount_cents) / 100,
        p_vendor_name: this.extractVendor(transaction.description),
        p_transaction_date: transaction.created_at
      });

      if (error || !anomaly || anomaly.length === 0) {
        return { is_anomaly: false, anomaly_score: 0 };
      }

      const result = anomaly[0];
      return {
        is_anomaly: result.is_anomaly || false,
        anomaly_score: result.anomaly_score || 0,
        anomaly_reason: result.anomaly_reason || null,
        severity: this.getAnomalySeverity(result.anomaly_score)
      };

    } catch (error) {
      console.warn('Anomaly detection failed:', error.message);
      return { is_anomaly: false, anomaly_score: 0 };
    }
  }

  /**
   * Enhance transaction with ML insights
   */
  async enhanceTransaction(transaction) {
    const [categorization, anomaly] = await Promise.all([
      this.categorizeTransaction(transaction),
      this.detectAnomalies(transaction)
    ]);

    return {
      ...transaction,
      // AI Categorization
      ai_category: categorization.category,
      ai_confidence: categorization.confidence,
      categorization_method: categorization.method,

      // Anomaly Detection
      is_anomaly: anomaly.is_anomaly,
      anomaly_score: anomaly.anomaly_score,
      anomaly_reason: anomaly.anomaly_reason,
      anomaly_severity: anomaly.severity,

      // ML Metadata
      ml_processed_at: new Date().toISOString(),
      ml_models_used: [categorization.model_used, 'anomaly_detector']
    };
  }

  /**
   * Extract vendor name from transaction description
   */
  extractVendor(description) {
    if (!description) return null;

    // Common patterns for vendor extraction
    const patterns = [
      /^([A-Z\s]+)/,  // All caps at start
      /([A-Za-z\s]+)(?=\s+\*|\s+\d)/,  // Before asterisk or numbers
      /^([^0-9*]+)/   // Before numbers or asterisks
    ];

    for (const pattern of patterns) {
      const match = description.match(pattern);
      if (match && match[1]) {
        return match[1].trim().substring(0, 50); // Limit length
      }
    }

    return description.substring(0, 50);
  }

  /**
   * Get fallback category when ML fails
   */
  getFallbackCategory(transaction) {
    // Use UpBank's category if available
    if (transaction.category_name) {
      return {
        category: transaction.category_name,
        confidence: 0.5,
        method: 'upbank_category',
        model_used: null
      };
    }

    // Basic rule-based fallback
    const description = (transaction.description || '').toLowerCase();

    if (description.includes('transfer') || description.includes('payment')) {
      return { category: 'Transfer', confidence: 0.6, method: 'rule_based' };
    }

    if (description.includes('salary') || description.includes('wage')) {
      return { category: 'Income', confidence: 0.7, method: 'rule_based' };
    }

    return { category: 'Uncategorized', confidence: 0.1, method: 'fallback' };
  }

  /**
   * Determine anomaly severity level
   */
  getAnomalySeverity(score) {
    if (score >= 0.9) return 'critical';
    if (score >= 0.7) return 'high';
    if (score >= 0.5) return 'medium';
    return 'low';
  }

  /**
   * Should categorization be applied automatically?
   */
  shouldAutoApply(confidence) {
    return confidence >= this.confidenceThresholds.auto;
  }

  /**
   * Should categorization be suggested for review?
   */
  shouldSuggestReview(confidence) {
    return confidence >= this.confidenceThresholds.review &&
           confidence < this.confidenceThresholds.auto;
  }
}

class ErrorHandler {
  static categorizeError(error) {
    if (error.message?.includes('401') || error.message?.includes('Unauthorized')) {
      return ErrorTypes.AUTH;
    }
    if (error.message?.includes('429') || error.message?.includes('Too Many Requests')) {
      return ErrorTypes.RATE_LIMIT;
    }
    if (error.code === 'ETIMEDOUT' || error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      return ErrorTypes.NETWORK;
    }
    if (error.code === '23505' || error.message?.includes('duplicate key')) {
      return ErrorTypes.CONSTRAINT_VIOLATION;
    }
    if (error.code?.startsWith('23') || error.message?.includes('violates')) {
      return ErrorTypes.DATABASE;
    }
    return ErrorTypes.UNKNOWN;
  }

  static async logError(syncId, error, context = {}) {
    const errorType = this.categorizeError(error);

    try {
      await supabase.from('sync_errors').insert({
        sync_id: syncId,
        error_type: errorType,
        error_message: error.message,
        error_stack: error.stack,
        context: context,
        created_at: new Date()
      });
    } catch (logError) {
      console.error('Failed to log error:', logError);
    }

    return errorType;
  }
}

class UpBankAPI {
  constructor(token) {
    this.token = token;
    this.baseURL = 'https://api.up.com.au/api/v1';
    this.rateLimitRemaining = 1000;
    this.rateLimitReset = null;
  }

  async request(endpoint, retries = 3) {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        // Check rate limit
        if (this.rateLimitRemaining < 10) {
          const waitTime = this.rateLimitReset ?
            Math.max(0, this.rateLimitReset - Date.now()) :
            60000;

          console.log(`⏳ Rate limit approaching. Waiting ${waitTime/1000}s...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
          },
          timeout: 30000 // 30 second timeout
        });

        // Update rate limit info
        this.rateLimitRemaining = parseInt(response.headers.get('x-ratelimit-remaining') || 1000);
        const resetTime = response.headers.get('x-ratelimit-reset');
        if (resetTime) {
          this.rateLimitReset = new Date(resetTime).getTime();
        }

        if (response.status === 429) {
          const retryAfter = parseInt(response.headers.get('retry-after') || 60);
          throw new Error(`429 Too Many Requests. Retry after ${retryAfter} seconds`);
        }

        if (response.status === 401) {
          throw new Error('401 Unauthorized. API token may be invalid or revoked');
        }

        if (!response.ok) {
          throw new Error(`UpBank API error: ${response.status} ${response.statusText}`);
        }

        return await response.json();

      } catch (error) {
        const errorType = ErrorHandler.categorizeError(error);

        if (errorType === ErrorTypes.AUTH) {
          console.error('❌ Authentication failed. Please check your API token.');
          throw error; // Don't retry auth errors
        }

        if (errorType === ErrorTypes.RATE_LIMIT) {
          const waitTime = 60000 * attempt; // Exponential backoff
          console.log(`⏳ Rate limited. Waiting ${waitTime/1000}s before retry ${attempt}/${retries}`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
          continue;
        }

        if (errorType === ErrorTypes.NETWORK && attempt < retries) {
          const backoff = Math.min(1000 * Math.pow(2, attempt), 10000);
          console.log(`🔄 Network error. Retrying in ${backoff/1000}s (attempt ${attempt}/${retries})`);
          await new Promise(resolve => setTimeout(resolve, backoff));
          continue;
        }

        if (attempt === retries) {
          throw error;
        }
      }
    }
  }

  async getAccounts() {
    const data = await this.request('/accounts');
    return data.data;
  }

  async getAccount(accountId) {
    const data = await this.request(`/accounts/${accountId}`);
    return data.data;
  }

  async getTransactions(accountId = null, limit = 100, before = null) {
    let endpoint = '/transactions';
    const params = new URLSearchParams();

    if (accountId) {
      endpoint = `/accounts/${accountId}/transactions`;
    }

    params.append('page[size]', limit.toString());
    if (before) {
      params.append('page[before]', before);
    }

    const data = await this.request(`${endpoint}?${params}`);
    return data;
  }

  async getCategories() {
    const data = await this.request('/categories');
    return data.data;
  }
}

class SyncStateManager {
  constructor(syncId) {
    this.syncId = syncId;
    this.checkpointInterval = 50; // Checkpoint every 50 transactions
    this.transactionCount = 0;
  }

  async createSyncSession() {
    const { data, error } = await supabase
      .from('sync_sessions')
      .insert({
        id: this.syncId,
        status: 'started',
        started_at: new Date(),
        metadata: {
          source: 'upbank',
          version: '2.0'
        }
      })
      .select()
      .single();

    if (error) {
      console.error('Failed to create sync session:', error);
    }

    return data;
  }

  async updateProgress(progress) {
    const { error } = await supabase
      .from('sync_sessions')
      .update({
        progress: progress,
        updated_at: new Date()
      })
      .eq('id', this.syncId);

    if (error) {
      console.error('Failed to update progress:', error);
    }
  }

  async createCheckpoint(state) {
    this.transactionCount++;

    if (this.transactionCount % this.checkpointInterval === 0) {
      const { error } = await supabase
        .from('sync_checkpoints')
        .insert({
          sync_id: this.syncId,
          accounts_synced: state.accountsCompleted || 0,
          transactions_synced: state.transactionsCompleted || 0,
          last_transaction_id: state.lastTransactionId,
          last_account_id: state.lastAccountId,
          state_data: state,
          created_at: new Date()
        });

      if (!error) {
        console.log(`📌 Checkpoint saved: ${state.transactionsCompleted} transactions`);
      }
    }
  }

  async getLastCheckpoint() {
    const { data, error } = await supabase
      .from('sync_checkpoints')
      .select('*')
      .eq('sync_id', this.syncId)
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    return data;
  }

  async completeSyncSession(summary) {
    const { error } = await supabase
      .from('sync_sessions')
      .update({
        status: 'completed',
        completed_at: new Date(),
        summary: summary
      })
      .eq('id', this.syncId);

    if (error) {
      console.error('Failed to complete sync session:', error);
    }
  }

  async failSyncSession(error) {
    await supabase
      .from('sync_sessions')
      .update({
        status: 'failed',
        failed_at: new Date(),
        error: {
          message: error.message,
          type: ErrorHandler.categorizeError(error)
        }
      })
      .eq('id', this.syncId);
  }
}

class DataValidator {
  static async validateAccountBalance(account, transactions) {
    const upbankBalance = Math.round(parseFloat(account.attributes.balance.value) * 100);

    const transactionSum = transactions
      .filter(t => t.attributes.status === 'SETTLED')
      .reduce((sum, t) => sum + Math.round(parseFloat(t.attributes.amount.value) * 100), 0);

    const difference = Math.abs(upbankBalance - transactionSum);

    if (difference > 100) { // $1 tolerance
      return {
        valid: false,
        upbankBalance,
        calculatedBalance: transactionSum,
        difference,
        message: `Balance mismatch: UpBank shows $${upbankBalance/100}, calculated $${transactionSum/100}`
      };
    }

    return { valid: true };
  }

  static async checkForDuplicates(transactions) {
    const ids = transactions.map(t => t.id);
    const uniqueIds = [...new Set(ids)];

    if (ids.length !== uniqueIds.length) {
      return {
        hasDuplicates: true,
        count: ids.length - uniqueIds.length
      };
    }

    return { hasDuplicates: false };
  }

  static async validateTransactionIntegrity(transaction) {
    const issues = [];

    // Check required fields
    if (!transaction.id) issues.push('Missing transaction ID');
    if (!transaction.attributes?.amount?.value) issues.push('Missing amount');
    if (!transaction.attributes?.createdAt) issues.push('Missing creation date');
    if (!transaction.relationships?.account?.data?.id) issues.push('Missing account reference');

    // Validate amount format
    const amount = parseFloat(transaction.attributes?.amount?.value);
    if (isNaN(amount)) issues.push('Invalid amount format');

    // Validate date
    const date = new Date(transaction.attributes?.createdAt);
    if (isNaN(date.getTime())) issues.push('Invalid date format');

    return {
      valid: issues.length === 0,
      issues
    };
  }
}

class EnhancedUpBankSyncer {
  constructor(syncId = null) {
    this.syncId = syncId || uuidv4();
    this.upbank = new UpBankAPI(UPBANK_TOKEN);
    this.stateManager = new SyncStateManager(this.syncId);
    this.mlPipeline = new MLPipeline();
    this.errors = [];
    this.warnings = [];
    this.summary = {
      accountsSynced: 0,
      categoriesSynced: 0,
      transactionsSynced: 0,
      transactionsFailed: 0,
      duplicatesSkipped: 0,
      mlCategorized: 0,
      anomaliesDetected: 0,
      highConfidenceML: 0,
      businessExpensesCategorized: 0
    };

    // Business expense keywords from Notion formula
    this.businessExpenseKeywords = [
      'apple', 'dropbox', 'notion', 'raycast', 'youtube',
      'make', 'anthropic', 'openai', 'setapp', 'quickbooks', 'splice'
    ];
  }

  /**
   * Categorize business expenses based on keywords (similar to Notion formula)
   */
  categorizeBusinessExpense(transaction) {
    const description = (transaction.description || '').toLowerCase();

    // Check if description contains any business expense keywords
    const isBusinessExpense = this.businessExpenseKeywords.some(keyword =>
      description.includes(keyword.toLowerCase())
    );

    if (isBusinessExpense) {
      return {
        is_business_related: true,
        is_tax_deductible: true,
        personal_category: 'Business Subscription',
        business_category: 'Software & Tools',
        business_subcategory: 'Subscription Services'
      };
    }

    return {
      is_business_related: false,
      is_tax_deductible: false,
      personal_category: null,
      business_category: null,
      business_subcategory: null
    };
  }

  async ensureAccountExists(upbankAccountId) {
    try {
      // Check if account exists
      const { data: existingAccount } = await supabase
        .from('personal_accounts')
        .select('id')
        .eq('upbank_account_id', upbankAccountId)
        .single();

      if (!existingAccount) {
        console.log(`🔄 Account ${upbankAccountId} not found, fetching from UpBank...`);

        // Fetch and create account
        const upbankAccount = await this.upbank.getAccount(upbankAccountId);

        const accountData = {
          upbank_account_id: upbankAccount.id,
          display_name: upbankAccount.attributes.displayName,
          account_type: upbankAccount.attributes.accountType,
          ownership_type: upbankAccount.attributes.ownershipType,
          balance_cents: Math.round(parseFloat(upbankAccount.attributes.balance.value) * 100),
          balance_currency_code: upbankAccount.attributes.balance.currencyCode
        };

        const { data, error } = await supabase
          .from('personal_accounts')
          .upsert(accountData, {
            onConflict: 'upbank_account_id',
            ignoreDuplicates: false
          })
          .select()
          .single();

        if (error) throw error;

        console.log(`✅ Created missing account: ${upbankAccount.attributes.displayName}`);
        return data.id;
      }

      return existingAccount.id;

    } catch (error) {
      console.error(`❌ Failed to ensure account exists: ${error.message}`);
      throw error;
    }
  }

  async ensureCategoryExists(categoryId) {
    if (!categoryId) return null;

    try {
      const { data: exists } = await supabase
        .from('upbank_categories')
        .select('id')
        .eq('id', categoryId)
        .single();

      if (!exists) {
        console.log(`📝 New category found: ${categoryId}. Syncing categories...`);
        await this.syncCategories();

        // Verify category now exists
        const { data: category } = await supabase
          .from('upbank_categories')
          .select('id')
          .eq('id', categoryId)
          .single();

        if (!category) {
          this.warnings.push(`Category ${categoryId} couldn't be synced`);
          return null;
        }
      }

      return categoryId;

    } catch (error) {
      this.warnings.push(`Category validation failed: ${error.message}`);
      return null;
    }
  }

  async handleDuplicateTransaction(transaction, error) {
    if (error.code === '23505') { // PostgreSQL unique violation
      try {
        // Check if existing transaction needs update
        const { data: existing } = await supabase
          .from('personal_transactions')
          .select('status, amount_cents')
          .eq('upbank_transaction_id', transaction.id)
          .single();

        if (existing) {
          const newStatus = transaction.attributes.status;
          const newAmount = Math.round(parseFloat(transaction.attributes.amount.value) * 100);

          // Update if status or amount changed
          if (existing.status !== newStatus || existing.amount_cents !== newAmount) {
            console.log(`🔄 Updating transaction ${transaction.id}: ${existing.status} → ${newStatus}`);

            const { error: updateError } = await supabase
              .from('personal_transactions')
              .update({
                status: newStatus,
                amount_cents: newAmount,
                settled_at: transaction.attributes.settledAt,
                updated_at: new Date()
              })
              .eq('upbank_transaction_id', transaction.id);

            if (!updateError) {
              return { updated: true };
            }
          }

          this.summary.duplicatesSkipped++;
          return { skipped: true };
        }
      } catch (checkError) {
        console.error('Error checking duplicate:', checkError);
      }
    }

    throw error;
  }

  async syncAccounts() {
    console.log('📦 Syncing accounts...');

    try {
      const accounts = await this.upbank.getAccounts();

      for (const account of accounts) {
        try {
          const accountData = {
            upbank_account_id: account.id,
            display_name: account.attributes.displayName,
            account_type: account.attributes.accountType,
            ownership_type: account.attributes.ownershipType,
            balance_cents: Math.round(parseFloat(account.attributes.balance.value) * 100),
            balance_currency_code: account.attributes.balance.currencyCode
          };

          const { error } = await supabase
            .from('personal_accounts')
            .upsert(accountData, {
              onConflict: 'upbank_account_id',
              ignoreDuplicates: false
            });

          if (error) throw error;

          this.summary.accountsSynced++;
          console.log(`✅ Synced account: ${account.attributes.displayName} ($${account.attributes.balance.value})`);

        } catch (error) {
          const errorType = await ErrorHandler.logError(this.syncId, error, { account: account.id });
          this.errors.push(`Account ${account.id}: ${error.message}`);
          console.error(`❌ Error syncing account ${account.id}:`, error.message);
        }
      }

      console.log(`📦 Synced ${this.summary.accountsSynced}/${accounts.length} accounts`);
      return accounts;

    } catch (error) {
      console.error('❌ Failed to fetch accounts:', error);
      throw error;
    }
  }

  async syncCategories() {
    console.log('🏷️  Syncing categories...');

    try {
      const categories = await this.upbank.getCategories();

      for (const category of categories) {
        try {
          const categoryData = {
            id: category.id,
            name: category.attributes.name,
            parent_id: category.relationships?.parent?.data?.id || null
          };

          const { error } = await supabase
            .from('upbank_categories')
            .upsert(categoryData, {
              onConflict: 'id',
              ignoreDuplicates: false
            });

          if (error) throw error;

          this.summary.categoriesSynced++;

        } catch (error) {
          this.warnings.push(`Category ${category.id}: ${error.message}`);
        }
      }

      console.log(`🏷️  Synced ${this.summary.categoriesSynced}/${categories.length} categories`);

    } catch (error) {
      console.error('❌ Failed to sync categories:', error);
      this.warnings.push(`Category sync failed: ${error.message}`);
    }
  }

  async syncTransactionBatch(transactions, accountMapping) {
    const results = {
      success: 0,
      failed: 0,
      skipped: 0,
      updated: 0
    };

    for (const transaction of transactions) {
      try {
        // Validate transaction integrity
        const validation = await DataValidator.validateTransactionIntegrity(transaction);
        if (!validation.valid) {
          console.warn(`⚠️ Invalid transaction ${transaction.id}:`, validation.issues);
          results.failed++;
          continue;
        }

        // Ensure account exists
        const upbankAccountId = transaction.relationships.account.data.id;
        const accountId = accountMapping[upbankAccountId] ||
                         await this.ensureAccountExists(upbankAccountId);

        if (!accountId) {
          throw new Error(`No account mapping for ${upbankAccountId}`);
        }

        // Ensure categories exist
        const categoryId = await this.ensureCategoryExists(
          transaction.relationships?.category?.data?.id
        );
        const parentCategoryId = await this.ensureCategoryExists(
          transaction.relationships?.parentCategory?.data?.id
        );

        // Prepare base transaction data
        const baseTransactionData = {
          upbank_transaction_id: transaction.id,
          account_id: accountId,
          description: transaction.attributes.description,
          message: transaction.attributes.message,
          amount_cents: Math.round(parseFloat(transaction.attributes.amount.value) * 100),
          currency_code: transaction.attributes.amount.currencyCode,
          transaction_date: transaction.attributes.createdAt,
          settled_at: transaction.attributes.settledAt,
          status: transaction.attributes.status,
          is_categorizable: transaction.attributes.isCategorizable,
          hold_info: transaction.attributes.holdInfo,
          round_up: transaction.attributes.roundUp,
          cashback: transaction.attributes.cashback,
          upbank_category_id: categoryId,
          upbank_parent_category_id: parentCategoryId,
          raw_data: transaction
        };

        // Enhance transaction with ML insights
        let transactionData = baseTransactionData;
        try {
          const enhancedTransaction = await this.mlPipeline.enhanceTransaction(baseTransactionData);

          transactionData = {
            ...baseTransactionData,
            // AI Categorization
            ai_category: enhancedTransaction.ai_category,
            ai_confidence: enhancedTransaction.ai_confidence,
            categorization_method: enhancedTransaction.categorization_method,

            // Anomaly Detection
            is_anomaly: enhancedTransaction.is_anomaly,
            anomaly_score: enhancedTransaction.anomaly_score,
            anomaly_reason: enhancedTransaction.anomaly_reason,
            anomaly_severity: enhancedTransaction.anomaly_severity,

            // ML Metadata
            ml_processed_at: enhancedTransaction.ml_processed_at,
            ml_models_used: enhancedTransaction.ml_models_used
          };

          // Add business expense categorization
          const businessExpenseInfo = this.categorizeBusinessExpense(baseTransactionData);

          transactionData = {
            ...transactionData,
            // Business Expense Classification
            is_business_related: businessExpenseInfo.is_business_related,
            is_tax_deductible: businessExpenseInfo.is_tax_deductible,
            personal_category: businessExpenseInfo.personal_category,
            business_category: businessExpenseInfo.business_category,
            business_subcategory: businessExpenseInfo.business_subcategory
          };

          // Update summary if categorized as business expense
          if (businessExpenseInfo.is_business_related) {
            this.summary.businessExpensesCategorized++;
            console.log(`💼 Business expense detected: "${baseTransactionData.description}" → ${businessExpenseInfo.personal_category}`);
          }

          // Update summary counters
          this.summary.mlCategorized++;
          if (enhancedTransaction.ai_confidence >= 0.9) {
            this.summary.highConfidenceML++;
          }
          if (enhancedTransaction.is_anomaly) {
            this.summary.anomaliesDetected++;

            // Log high-severity anomalies
            if (enhancedTransaction.anomaly_severity === 'critical' ||
                enhancedTransaction.anomaly_severity === 'high') {
              console.warn(`🚨 ${enhancedTransaction.anomaly_severity.toUpperCase()} anomaly detected:`);
              console.warn(`   Description: ${baseTransactionData.description}`);
              console.warn(`   Amount: $${Math.abs(baseTransactionData.amount_cents) / 100}`);
              console.warn(`   Reason: ${enhancedTransaction.anomaly_reason}`);
              console.warn(`   Score: ${enhancedTransaction.anomaly_score}`);
            }
          }

          // Log high-confidence categorizations
          if (this.mlPipeline.shouldAutoApply(enhancedTransaction.ai_confidence)) {
            console.log(`🧠 Auto-categorized: "${enhancedTransaction.ai_category}" (${Math.round(enhancedTransaction.ai_confidence * 100)}% confidence)`);
          } else if (this.mlPipeline.shouldSuggestReview(enhancedTransaction.ai_confidence)) {
            console.log(`🤔 Suggest review: "${enhancedTransaction.ai_category}" (${Math.round(enhancedTransaction.ai_confidence * 100)}% confidence)`);
          }

        } catch (mlError) {
          console.warn(`⚠️ ML processing failed for transaction ${transaction.id}:`, mlError.message);

          // Still apply business expense categorization even if ML fails
          const businessExpenseInfo = this.categorizeBusinessExpense(baseTransactionData);

          transactionData = {
            ...baseTransactionData,
            // Business Expense Classification (fallback when ML fails)
            is_business_related: businessExpenseInfo.is_business_related,
            is_tax_deductible: businessExpenseInfo.is_tax_deductible,
            personal_category: businessExpenseInfo.personal_category,
            business_category: businessExpenseInfo.business_category,
            business_subcategory: businessExpenseInfo.business_subcategory
          };

          // Update summary if categorized as business expense
          if (businessExpenseInfo.is_business_related) {
            this.summary.businessExpensesCategorized++;
            console.log(`💼 Business expense detected (ML failed): "${baseTransactionData.description}" → ${businessExpenseInfo.personal_category}`);
          }
        }

        const { error } = await supabase
          .from('personal_transactions')
          .insert(transactionData);

        if (error) {
          const result = await this.handleDuplicateTransaction(transaction, error);
          if (result.skipped) {
            results.skipped++;
          } else if (result.updated) {
            results.updated++;
          }
        } else {
          results.success++;
          this.summary.transactionsSynced++;
        }

        // Create checkpoint
        await this.stateManager.createCheckpoint({
          accountsCompleted: this.summary.accountsSynced,
          transactionsCompleted: this.summary.transactionsSynced,
          lastTransactionId: transaction.id,
          lastAccountId: accountId
        });

      } catch (error) {
        const errorType = await ErrorHandler.logError(this.syncId, error, {
          transaction: transaction.id
        });

        results.failed++;
        this.summary.transactionsFailed++;
        this.errors.push(`Transaction ${transaction.id}: ${error.message}`);

        console.error(`❌ Error syncing transaction ${transaction.id}:`, error.message);
      }
    }

    return results;
  }

  async syncTransactions(accountId = null, daysBack = 90) {
    console.log(`💳 Syncing transactions${accountId ? ` for account ${accountId}` : ''}...`);

    try {
      // Get account mapping
      const { data: accounts } = await supabase
        .from('personal_accounts')
        .select('id, upbank_account_id');

      const accountMapping = {};
      accounts?.forEach(acc => {
        accountMapping[acc.upbank_account_id] = acc.id;
      });

      // Get existing transaction IDs to avoid duplicates
      const { data: existingTransactions } = await supabase
        .from('personal_transactions')
        .select('upbank_transaction_id');

      const existingIds = new Set(existingTransactions?.map(t => t.upbank_transaction_id) || []);

      let allTransactions = [];
      let hasMore = true;
      let before = null;
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - daysBack);

      // Update progress
      await this.stateManager.updateProgress({
        stage: 'fetching_transactions',
        account: accountId
      });

      while (hasMore) {
        try {
          const response = await this.upbank.getTransactions(accountId, 100, before);
          const transactions = response.data;

          if (transactions.length === 0) {
            hasMore = false;
            break;
          }

          // Check if we're going too far back
          const oldestTransaction = new Date(transactions[transactions.length - 1].attributes.createdAt);

          if (oldestTransaction < cutoffDate) {
            // Filter transactions within the date range
            const recentTransactions = transactions.filter(t =>
              new Date(t.attributes.createdAt) >= cutoffDate
            );
            allTransactions.push(...recentTransactions);
            hasMore = false;
          } else {
            allTransactions.push(...transactions);
            // Get the next page
            before = response.links?.prev ? new URL(response.links.prev).searchParams.get('page[before]') : null;
            hasMore = before !== null;
          }

        } catch (error) {
          const errorType = ErrorHandler.categorizeError(error);

          if (errorType === ErrorTypes.RATE_LIMIT) {
            console.log('⏳ Rate limit hit, pausing sync...');
            await new Promise(resolve => setTimeout(resolve, 60000));
            continue;
          }

          throw error;
        }
      }

      // Filter out existing transactions
      const newTransactions = allTransactions.filter(t => !existingIds.has(t.id));
      console.log(`Found ${newTransactions.length} new transactions to sync`);

      // Check for duplicates in the batch
      const duplicateCheck = await DataValidator.checkForDuplicates(newTransactions);
      if (duplicateCheck.hasDuplicates) {
        console.warn(`⚠️ Found ${duplicateCheck.count} duplicate transactions in batch`);
      }

      // Sync in batches
      const batchSize = 50;
      for (let i = 0; i < newTransactions.length; i += batchSize) {
        const batch = newTransactions.slice(i, i + batchSize);
        const results = await this.syncTransactionBatch(batch, accountMapping);

        console.log(`✅ Batch ${Math.floor(i/batchSize) + 1}: ${results.success} success, ${results.skipped} skipped, ${results.updated} updated, ${results.failed} failed`);
      }

      console.log(`💳 Synced ${this.summary.transactionsSynced} new transactions`);

    } catch (error) {
      console.error('❌ Transaction sync failed:', error);
      throw error;
    }
  }

  async reconcileBalances(accounts) {
    console.log('💰 Reconciling account balances...');

    const reconciliationResults = [];

    for (const account of accounts) {
      try {
        // Get all transactions for this account
        const { data: transactions } = await supabase
          .from('personal_transactions')
          .select('amount_cents, status')
          .eq('account_id', account.id);

        const dbBalance = transactions
          ?.filter(t => t.status === 'SETTLED')
          ?.reduce((sum, t) => sum + t.amount_cents, 0) || 0;

        const upbankBalance = Math.round(parseFloat(account.attributes.balance.value) * 100);
        const difference = Math.abs(upbankBalance - dbBalance);

        if (difference > 100) { // $1 tolerance
          console.warn(`⚠️ Balance mismatch for ${account.attributes.displayName}:`);
          console.warn(`  UpBank: $${upbankBalance / 100}`);
          console.warn(`  Database: $${dbBalance / 100}`);
          console.warn(`  Difference: $${difference / 100}`);

          reconciliationResults.push({
            account: account.attributes.displayName,
            upbankBalance,
            dbBalance,
            difference,
            status: 'mismatch'
          });
        } else {
          console.log(`✅ ${account.attributes.displayName}: $${upbankBalance / 100} ✓`);

          reconciliationResults.push({
            account: account.attributes.displayName,
            upbankBalance,
            dbBalance,
            difference,
            status: 'matched'
          });
        }

      } catch (error) {
        console.error(`❌ Failed to reconcile ${account.attributes.displayName}:`, error);
        reconciliationResults.push({
          account: account.attributes.displayName,
          status: 'error',
          error: error.message
        });
      }
    }

    return reconciliationResults;
  }

  async generateSyncReport() {
    const report = {
      syncId: this.syncId,
      timestamp: new Date(),
      summary: this.summary,
      errors: this.errors,
      warnings: this.warnings
    };

    // Get spending by category
    const { data: categorySpending } = await supabase
      .from('personal_transactions')
      .select('upbank_category_id, amount_cents')
      .gte('created_at', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000))
      .lt('amount_cents', 0); // Only expenses

    if (categorySpending) {
      const spending = {};
      categorySpending.forEach(tx => {
        const category = tx.upbank_category_id || 'uncategorized';
        spending[category] = (spending[category] || 0) + Math.abs(tx.amount_cents);
      });

      report.spendingByCategory = spending;
    }

    return report;
  }

  async resumeFromCheckpoint() {
    console.log('🔍 Checking for previous sync checkpoint...');

    const checkpoint = await this.stateManager.getLastCheckpoint();

    if (checkpoint) {
      console.log(`📌 Resuming from checkpoint: ${checkpoint.transactions_synced} transactions completed`);
      this.summary.transactionsSynced = checkpoint.transactions_synced;
      this.summary.accountsSynced = checkpoint.accounts_synced;
      return checkpoint;
    }

    return null;
  }

  async fullSync(daysBack = 90) {
    console.log('🚀 Starting enhanced UpBank sync...');
    console.log(`📅 Sync ID: ${this.syncId}`);

    try {
      // Create sync session
      await this.stateManager.createSyncSession();

      // Check for resume point
      const checkpoint = await this.resumeFromCheckpoint();

      if (!checkpoint) {
        // 1. Sync categories first
        await this.syncCategories();

        // 2. Sync accounts
        var accounts = await this.syncAccounts();
      } else {
        // Resume from checkpoint
        console.log('📌 Resuming from checkpoint...');

        // Get accounts
        const { data: accountData } = await supabase
          .from('personal_accounts')
          .select('*');

        accounts = accountData;
      }

      // 3. Sync transactions for each account
      for (const account of accounts) {
        try {
          await this.syncTransactions(account.upbank_account_id || account.id, daysBack);
        } catch (error) {
          console.error(`❌ Failed to sync transactions for ${account.display_name || account.id}:`, error);
          this.errors.push(`Account ${account.id}: ${error.message}`);
        }
      }

      // 4. Reconcile balances
      const reconciliation = await this.reconcileBalances(accounts);

      // 5. Generate report
      const report = await this.generateSyncReport();
      report.reconciliation = reconciliation;

      // Complete sync session
      await this.stateManager.completeSyncSession(report);

      // Display summary
      console.log('\n📊 Sync Complete!');
      console.log('─'.repeat(40));
      console.log(`✅ Accounts: ${this.summary.accountsSynced}`);
      console.log(`✅ Categories: ${this.summary.categoriesSynced}`);
      console.log(`✅ Transactions: ${this.summary.transactionsSynced}`);

      // ML Processing Results
      if (this.summary.mlCategorized > 0) {
        console.log(`🤖 ML Categorized: ${this.summary.mlCategorized} (${this.summary.highConfidenceML} high confidence)`);
      }

      if (this.summary.businessExpensesCategorized > 0) {
        console.log(`💼 Business Expenses: ${this.summary.businessExpensesCategorized} automatically categorized`);
      }

      if (this.summary.anomaliesDetected > 0) {
        console.log(`🚨 Anomalies Detected: ${this.summary.anomaliesDetected}`);
      }

      if (this.summary.duplicatesSkipped > 0) {
        console.log(`⏭️  Skipped: ${this.summary.duplicatesSkipped} duplicates`);
      }

      if (this.summary.transactionsFailed > 0) {
        console.log(`❌ Failed: ${this.summary.transactionsFailed} transactions`);
      }

      if (this.warnings.length > 0) {
        console.log(`\n⚠️  Warnings: ${this.warnings.length}`);
        this.warnings.slice(0, 5).forEach(w => console.log(`  - ${w}`));
      }

      if (this.errors.length > 0) {
        console.log(`\n❌ Errors: ${this.errors.length}`);
        this.errors.slice(0, 5).forEach(e => console.log(`  - ${e}`));
      }

      console.log('─'.repeat(40));
      console.log(`📝 Full report saved to sync session ${this.syncId}`);

      return report;

    } catch (error) {
      console.error('❌ Sync failed:', error);

      await this.stateManager.failSyncSession(error);
      await ErrorHandler.logError(this.syncId, error);

      throw error;
    }
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'full';

  // Resume from previous sync if available
  const resumeSyncId = args.includes('--resume') ? args[args.indexOf('--resume') + 1] : null;

  const syncer = new EnhancedUpBankSyncer(resumeSyncId);

  try {
    switch (command) {
      case 'accounts':
        await syncer.syncAccounts();
        break;

      case 'categories':
        await syncer.syncCategories();
        break;

      case 'transactions':
        const accountId = args[1] || null;
        const daysBack = parseInt(args[2]) || 90;
        await syncer.syncTransactions(accountId, daysBack);
        break;

      case 'full':
        const fullDaysBack = parseInt(args[1]) || 90;
        await syncer.fullSync(fullDaysBack);
        break;

      case 'check':
        // Health check
        console.log('🏥 Running sync health check...');

        // Test API connection
        try {
          await syncer.upbank.request('/util/ping');
          console.log('✅ UpBank API: Connected');
        } catch (error) {
          console.log('❌ UpBank API: Failed');
        }

        // Test database connection
        try {
          const { error } = await supabase.from('sync_sessions').select('id').limit(1);
          if (error) throw error;
          console.log('✅ Supabase: Connected');
        } catch (error) {
          console.log('❌ Supabase: Failed');
        }

        // Check last sync
        const { data: lastSync } = await supabase
          .from('sync_sessions')
          .select('*')
          .eq('status', 'completed')
          .order('completed_at', { ascending: false })
          .limit(1)
          .single();

        if (lastSync) {
          console.log(`📅 Last sync: ${new Date(lastSync.completed_at).toLocaleString()}`);
          console.log(`📊 Results: ${JSON.stringify(lastSync.summary?.summary || {})}`);
        } else {
          console.log('📅 No previous syncs found');
        }

        break;

      default:
        console.log(`
Usage: node sync-upbank-enhanced.js [command] [options]

Commands:
  full [days]              - Full sync with error recovery (default: 90 days)
  accounts                 - Sync accounts only
  categories               - Sync categories only
  transactions [id] [days] - Sync transactions for account
  check                    - Health check and last sync info

Options:
  --resume [sync-id]       - Resume from previous sync checkpoint

Examples:
  node sync-upbank-enhanced.js full 30
  node sync-upbank-enhanced.js check
  node sync-upbank-enhanced.js full --resume abc-123-def
        `);
    }
  } catch (error) {
    console.error('Fatal error:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { EnhancedUpBankSyncer };
