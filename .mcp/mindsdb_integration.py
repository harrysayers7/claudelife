#!/usr/bin/env python3
"""
MindsDB Integration for Financial Tracking System
Uses HTTP API to connect to local MindsDB instance for ML predictions
"""

import os
import requests
import json
from dotenv import load_dotenv
import logging
import pandas as pd

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MindsDBIntegration:
    def __init__(self):
        """Initialize MindsDB HTTP API connection"""
        self.base_url = "http://localhost:47344"
        self.api_url = f"{self.base_url}/api/sql/query"
        self.supabase_connection_params = {
            'host': os.getenv('SUPABASE_DB_HOST'),
            'port': int(os.getenv('SUPABASE_DB_PORT', 5432)),
            'database': os.getenv('SUPABASE_DB_NAME'),
            'user': os.getenv('SUPABASE_DB_USER'),
            'password': os.getenv('SUPABASE_DB_PASSWORD'),
            'schema': 'public'
        }

    def execute_query(self, query):
        """Execute SQL query on MindsDB via HTTP API"""
        try:
            response = requests.post(
                self.api_url,
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("type") == "table":
                    # Convert to pandas DataFrame for compatibility
                    data = result.get("data", [])
                    columns = result.get("column_names", [])
                    return pd.DataFrame(data, columns=columns) if data else pd.DataFrame()
                return result
            else:
                logger.error(f"MindsDB query failed: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Failed to execute MindsDB query: {e}")
            return None

    def test_connection(self):
        """Test connection to MindsDB"""
        try:
            result = self.execute_query("SELECT 1 as test")
            return result is not None
        except Exception as e:
            logger.error(f"Failed to test MindsDB connection: {e}")
            return False

    def create_supabase_connection(self):
        """Create connection to Supabase database via MindsDB"""
        try:
            # Check if database already exists
            check_query = "SHOW DATABASES"
            result = self.execute_query(check_query)

            if result is not None and not result.empty:
                existing_dbs = result['Database'].tolist() if 'Database' in result.columns else []
                if 'sayers_data' in existing_dbs:
                    logger.info("Using existing Supabase connection")
                    return True

            # Create new database connection
            create_db_query = f"""
            CREATE DATABASE sayers_data
            WITH ENGINE = "postgres",
            PARAMETERS = {{
                "host": "{self.supabase_connection_params['host']}",
                "port": {self.supabase_connection_params['port']},
                "database": "{self.supabase_connection_params['database']}",
                "user": "{self.supabase_connection_params['user']}",
                "password": "{self.supabase_connection_params['password']}",
                "schema": "{self.supabase_connection_params['schema']}"
            }}
            """

            result = self.execute_query(create_db_query)
            if result is not None:
                logger.info("Created new Supabase database connection")
                return True
            else:
                logger.error("Failed to create Supabase database connection")
                return False

        except Exception as e:
            logger.error(f"Failed to create Supabase connection: {e}")
            return False

    def create_ml_models(self):
        """Create all ML models for financial predictions"""
        models = [
            self._create_transaction_categorizer(),
            self._create_payment_predictor(),
            self._create_cash_flow_forecaster(),
            self._create_anomaly_detector(),
            self._create_expense_optimizer(),
            self._create_tax_optimizer(),
            self._create_vendor_risk_assessor()
        ]

        successful_models = sum(1 for model in models if model)
        logger.info(f"Successfully created {successful_models}/7 ML models")
        return successful_models == 7

    def _create_transaction_categorizer(self):
        """Create ML model for automatic transaction categorization"""
        try:
            query = """
            CREATE OR REPLACE MODEL mindsdb.transaction_categorizer
            FROM sayers_data.transactions t
            JOIN sayers_data.accounts a ON t.account_id = a.id
            JOIN sayers_data.entities e ON a.entity_id = e.id
            PREDICT category_id
            USING
                engine = 'lightgbm',
                tag = 'financial_ai'
            """

            result = self.execute_query(query)
            if result is not None:
                logger.info("Created transaction categorizer model")
                return True
            else:
                logger.error("Failed to create transaction categorizer model")
                return False

        except Exception as e:
            logger.error(f"Failed to create transaction categorizer: {e}")
            return False

    def _create_payment_predictor(self):
        """Create ML model for payment behavior prediction"""
        try:
            query = """
            CREATE OR REPLACE MODEL mindsdb.payment_predictor
            FROM sayers_data.transactions t
            JOIN sayers_data.entities e ON t.entity_id = e.id
            WHERE t.transaction_type = 'payment'
            PREDICT payment_date
            USING
                engine = 'neural',
                tag = 'financial_ai'
            """

            result = self.execute_query(query)
            if result is not None:
                logger.info("Created payment predictor model")
                return True
            else:
                logger.error("Failed to create payment predictor model")
                return False

        except Exception as e:
            logger.error(f"Failed to create payment predictor: {e}")
            return False

    def _create_cash_flow_forecaster(self):
        """Create ML model for cash flow forecasting"""
        try:
            query = """
            CREATE OR REPLACE MODEL mindsdb.cash_flow_forecaster
            FROM sayers_data.cash_flow_forecasts
            PREDICT forecast_amount
            ORDER BY forecast_date
            GROUP BY entity_id
            WINDOW 30
            HORIZON 90
            USING
                engine = 'statsforecast',
                tag = 'financial_ai'
            """

            result = self.execute_query(query)
            if result is not None:
                logger.info("Created cash flow forecaster model")
                return True
            else:
                logger.error("Failed to create cash flow forecaster model")
                return False

        except Exception as e:
            logger.error(f"Failed to create cash flow forecaster: {e}")
            return False

    def _create_anomaly_detector(self):
        """Create ML model for transaction anomaly detection"""
        try:
            query = """
            CREATE OR REPLACE MODEL mindsdb.anomaly_detector
            FROM sayers_data.anomaly_detections
            PREDICT is_anomaly
            USING
                engine = 'anomaly',
                tag = 'financial_ai'
            """

            result = self.execute_query(query)
            if result is not None:
                logger.info("Created anomaly detector model")
                return True
            else:
                logger.error("Failed to create anomaly detector model")
                return False

        except Exception as e:
            logger.error(f"Failed to create anomaly detector: {e}")
            return False

    def _create_expense_optimizer(self):
        """Create ML model for expense optimization"""
        try:
            query = """
            CREATE OR REPLACE MODEL mindsdb.expense_optimizer
            FROM sayers_data.transactions t
            JOIN sayers_data.chart_of_accounts coa ON t.account_id = coa.id
            WHERE coa.account_type = 'expense'
            PREDICT optimization_score
            USING
                engine = 'lightgbm',
                tag = 'financial_ai'
            """

            result = self.execute_query(query)
            if result is not None:
                logger.info("Created expense optimizer model")
                return True
            else:
                logger.error("Failed to create expense optimizer model")
                return False

        except Exception as e:
            logger.error(f"Failed to create expense optimizer: {e}")
            return False

    def _create_tax_optimizer(self):
        """Create ML model for tax optimization"""
        try:
            query = """
            CREATE OR REPLACE MODEL mindsdb.tax_optimizer
            FROM sayers_data.transactions t
            JOIN sayers_data.entities e ON t.entity_id = e.id
            PREDICT tax_deductible_amount
            USING
                engine = 'neural',
                tag = 'financial_ai'
            """

            result = self.execute_query(query)
            if result is not None:
                logger.info("Created tax optimizer model")
                return True
            else:
                logger.error("Failed to create tax optimizer model")
                return False

        except Exception as e:
            logger.error(f"Failed to create tax optimizer: {e}")
            return False

    def _create_vendor_risk_assessor(self):
        """Create ML model for vendor risk assessment"""
        try:
            query = """
            CREATE OR REPLACE MODEL mindsdb.vendor_risk_assessor
            FROM sayers_data.transactions t
            WHERE t.vendor_name IS NOT NULL
            PREDICT risk_score
            USING
                engine = 'lightgbm',
                tag = 'financial_ai'
            """

            result = self.execute_query(query)
            if result is not None:
                logger.info("Created vendor risk assessor model")
                return True
            else:
                logger.error("Failed to create vendor risk assessor model")
                return False

        except Exception as e:
            logger.error(f"Failed to create vendor risk assessor: {e}")
            return False

    def setup_integration(self):
        """Complete setup of MindsDB integration"""
        logger.info("Starting MindsDB integration setup...")

        if not self.test_connection():
            return False

        if not self.create_supabase_connection():
            return False

        if not self.create_ml_models():
            return False

        logger.info("MindsDB integration setup completed successfully!")
        return True

    def predict_transaction_category(self, description, amount, vendor=None):
        """Predict transaction category using ML model"""
        try:
            # Escape single quotes in description and vendor
            description = description.replace("'", "''") if description else ""
            vendor_clause = f" AND vendor_name = '{vendor.replace("'", "''")}'" if vendor else ""

            query = f"""
            SELECT category_id, confidence
            FROM mindsdb.transaction_categorizer
            WHERE description = '{description}'
            AND amount = {amount}{vendor_clause}
            """

            result = self.execute_query(query)
            return result

        except Exception as e:
            logger.error(f"Failed to predict transaction category: {e}")
            return None

    def forecast_cash_flow(self, entity_id, days_ahead=30):
        """Forecast cash flow for entity"""
        try:
            query = f"""
            SELECT forecast_date, forecast_amount, confidence_interval
            FROM mindsdb.cash_flow_forecaster
            WHERE entity_id = {entity_id}
            AND forecast_date > NOW()
            AND forecast_date <= NOW() + INTERVAL {days_ahead} DAY
            ORDER BY forecast_date
            """

            result = self.execute_query(query)
            return result

        except Exception as e:
            logger.error(f"Failed to forecast cash flow: {e}")
            return None

    def detect_anomalies(self, entity_id, limit=10):
        """Detect transaction anomalies"""
        try:
            query = f"""
            SELECT t.*, ad.anomaly_score, ad.anomaly_reason
            FROM sayers_data.transactions t
            JOIN mindsdb.anomaly_detector ad ON t.id = ad.transaction_id
            WHERE t.entity_id = {entity_id}
            AND ad.is_anomaly = 1
            ORDER BY ad.anomaly_score DESC
            LIMIT {limit}
            """

            result = self.execute_query(query)
            return result

        except Exception as e:
            logger.error(f"Failed to detect anomalies: {e}")
            return None


if __name__ == "__main__":
    # Initialize and setup MindsDB integration
    integration = MindsDBIntegration()

    # Test basic connection first
    print("Testing MindsDB connection...")
    if integration.test_connection():
        print("✓ MindsDB connection successful!")

        print("\nTesting database setup...")
        if integration.create_supabase_connection():
            print("✓ Supabase database connection created!")
        else:
            print("✗ Failed to create Supabase database connection")

    else:
        print("✗ MindsDB connection failed!")
        print("Make sure MindsDB is running on localhost:47334")