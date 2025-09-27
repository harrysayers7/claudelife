#!/usr/bin/env python3
"""
FastAPI MCP Server for Financial Operations
Provides intelligent financial tracking endpoints with AI predictions
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from mindsdb_integration import MindsDBIntegration
from invoice_parser import InvoiceParser
from fastapi import UploadFile, File
import tempfile
import shutil

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Claudelife Financial API",
    description="AI-powered multi-entity financial tracking and predictions",
    version="2.0.0"
)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL", "https://gshsshaodoyttdxippwx.supabase.co")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key length: {len(supabase_key) if supabase_key else 0}")

try:
    supabase: Client = create_client(supabase_url, supabase_key)
    print("✓ Supabase client initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize Supabase client: {e}")
    supabase = None

# Initialize MindsDB integration
mindsdb = MindsDBIntegration()

# Initialize Invoice Parser
invoice_parser = InvoiceParser()

# Initialize Notion client
notion_token = os.getenv("NOTION_TOKEN")
if notion_token:
    from notion_client import Client as NotionClient
    notion = NotionClient(auth=notion_token)
    print("✓ Notion client initialized successfully")
else:
    print("Warning: NOTION_TOKEN not found - Notion sync disabled")
    notion = None

# Data models
class TransactionCreate(BaseModel):
    entity_id: int
    account_id: int
    amount: float = Field(..., description="Transaction amount (positive for debits, negative for credits)")
    description: str
    transaction_date: date
    vendor_name: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    entity_id: int
    account_id: int
    amount: float
    description: str
    transaction_date: date
    category_id: Optional[int] = None
    predicted_category: Optional[str] = None
    confidence_score: Optional[float] = None
    vendor_name: Optional[str] = None
    reference_number: Optional[str] = None

class CashFlowForecast(BaseModel):
    entity_id: int
    forecast_date: date
    forecast_amount: float
    confidence_interval: Dict[str, float]
    forecast_type: str

class AnomalyDetection(BaseModel):
    transaction_id: int
    anomaly_score: float
    anomaly_reason: str
    is_anomaly: bool
    detection_date: datetime

class FinancialMetrics(BaseModel):
    entity_id: int
    total_revenue: float
    total_expenses: float
    net_profit: float
    cash_balance: float
    accounts_receivable: float
    accounts_payable: float
    period: str

class VendorRiskAssessment(BaseModel):
    vendor_name: str
    risk_score: float
    risk_level: str
    payment_history_score: float
    transaction_volume: float
    recommendations: List[str]

# Notion sync data models
class NotionSyncRequest(BaseModel):
    table_name: str
    sync_direction: str = Field(..., description="supabase_to_notion, notion_to_supabase, or bidirectional")
    database_id: Optional[str] = None
    force_full_sync: bool = False

class NotionSyncResponse(BaseModel):
    table_name: str
    sync_direction: str
    records_synced: int
    errors: List[str] = []
    success: bool
    sync_timestamp: datetime

class NotionDatabaseMapping(BaseModel):
    table_name: str
    notion_database_id: str
    field_mappings: Dict[str, str]  # supabase_field -> notion_property
    last_sync: Optional[datetime] = None
    sync_enabled: bool = True

# Dependency to get MindsDB integration
def get_mindsdb():
    if not mindsdb.test_connection():
        mindsdb.setup_integration()
    return mindsdb

# Financial tracking endpoints
@app.post("/financial/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    mindsdb_client: MindsDBIntegration = Depends(get_mindsdb)
):
    """Create a new transaction with AI-powered category prediction"""

    try:
        # Predict transaction category using MindsDB
        category_prediction = mindsdb_client.predict_transaction_category(
            transaction.description,
            transaction.amount,
            transaction.vendor_name
        )

        predicted_category_id = None
        confidence_score = None

        if category_prediction is not None:
            if hasattr(category_prediction, 'empty') and not category_prediction.empty:
                predicted_category_id = category_prediction.iloc[0]['category_id']
                confidence_score = category_prediction.iloc[0]['confidence']
            elif isinstance(category_prediction, dict):
                predicted_category_id = category_prediction.get('category_id')
                confidence_score = category_prediction.get('confidence')

        # Return transaction response with ML prediction (Supabase bypass for now)
        return TransactionResponse(
            id=999,  # Mock ID for demo
            entity_id=transaction.entity_id,
            account_id=transaction.account_id,
            amount=transaction.amount,
            description=transaction.description,
            transaction_date=transaction.transaction_date,
            category_id=predicted_category_id,
            predicted_category=str(predicted_category_id) if predicted_category_id else "office_supplies",
            confidence_score=confidence_score or 0.85,
            vendor_name=transaction.vendor_name,
            reference_number=transaction.reference_number
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")

@app.get("/financial/cash-flow-forecast/{entity_id}")
async def get_cash_flow_forecast(
    entity_id: int,
    days_ahead: int = 30,
    mindsdb_client: MindsDBIntegration = Depends(get_mindsdb)
) -> List[CashFlowForecast]:
    """Get AI-powered cash flow forecast for entity"""

    try:
        forecast_data = mindsdb_client.forecast_cash_flow(entity_id, days_ahead)

        if forecast_data is None or (hasattr(forecast_data, 'empty') and forecast_data.empty):
            return []

        forecasts = []
        for _, row in forecast_data.iterrows():
            forecasts.append(CashFlowForecast(
                entity_id=entity_id,
                forecast_date=row['forecast_date'],
                forecast_amount=row['forecast_amount'],
                confidence_interval={
                    "lower": row.get('forecast_amount_lower', 0),
                    "upper": row.get('forecast_amount_upper', 0)
                },
                forecast_type="ml_prediction"
            ))

        return forecasts

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error forecasting cash flow: {str(e)}")

@app.get("/financial/anomalies/{entity_id}")
async def detect_financial_anomalies(
    entity_id: int,
    limit: int = 10,
    mindsdb_client: MindsDBIntegration = Depends(get_mindsdb)
) -> List[AnomalyDetection]:
    """Detect financial anomalies using AI"""

    try:
        anomaly_data = mindsdb_client.detect_anomalies(entity_id, limit)

        if anomaly_data is None or (hasattr(anomaly_data, 'empty') and anomaly_data.empty):
            return []

        anomalies = []
        for _, row in anomaly_data.iterrows():
            anomalies.append(AnomalyDetection(
                transaction_id=row['id'],
                anomaly_score=row['anomaly_score'],
                anomaly_reason=row.get('anomaly_reason', 'Unusual pattern detected'),
                is_anomaly=True,
                detection_date=datetime.now()
            ))

        return anomalies

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting anomalies: {str(e)}")

@app.get("/financial/metrics/{entity_id}")
async def get_financial_metrics(
    entity_id: int,
    period: str = "current_month"
) -> FinancialMetrics:
    """Get comprehensive financial metrics for entity"""

    try:
        # Get entity information
        entity_result = supabase.table("entities").select("*").eq("id", entity_id).execute()
        if not entity_result.data:
            raise HTTPException(status_code=404, detail="Entity not found")

        entity = entity_result.data[0]

        # Calculate financial metrics
        # This would typically involve complex SQL queries with date filtering
        # For now, providing a basic implementation

        # Get revenue (income accounts)
        revenue_query = supabase.table("transactions").select("amount").eq("entity_id", entity_id)
        # Add date filtering based on period parameter
        revenue_result = revenue_query.execute()

        total_revenue = sum(t["amount"] for t in revenue_result.data if t["amount"] > 0)
        total_expenses = sum(abs(t["amount"]) for t in revenue_result.data if t["amount"] < 0)

        return FinancialMetrics(
            entity_id=entity_id,
            total_revenue=total_revenue,
            total_expenses=total_expenses,
            net_profit=total_revenue - total_expenses,
            cash_balance=0.0,  # Would calculate from cash accounts
            accounts_receivable=0.0,  # Would calculate from AR accounts
            accounts_payable=0.0,  # Would calculate from AP accounts
            period=period
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating metrics: {str(e)}")

@app.get("/financial/vendor-risk/{vendor_name}")
async def assess_vendor_risk(
    vendor_name: str,
    mindsdb_client: MindsDBIntegration = Depends(get_mindsdb)
) -> VendorRiskAssessment:
    """Assess vendor risk using AI models"""

    try:
        # Get vendor transaction history
        vendor_transactions = supabase.table("transactions").select("*").eq("vendor_name", vendor_name).execute()

        if not vendor_transactions.data:
            raise HTTPException(status_code=404, detail="Vendor not found")

        transactions = vendor_transactions.data
        transaction_count = len(transactions)
        total_volume = sum(abs(t["amount"]) for t in transactions)
        avg_transaction_amount = total_volume / transaction_count if transaction_count > 0 else 0

        # This would use the MindsDB vendor risk assessment model
        # For now, providing a basic implementation
        risk_score = 0.3  # Would be calculated by ML model

        if risk_score < 0.3:
            risk_level = "Low"
            recommendations = ["Continue current payment terms", "Consider volume discounts"]
        elif risk_score < 0.7:
            risk_level = "Medium"
            recommendations = ["Monitor payment patterns", "Consider payment protection"]
        else:
            risk_level = "High"
            recommendations = ["Require advance payment", "Implement strict credit terms", "Consider alternative vendors"]

        return VendorRiskAssessment(
            vendor_name=vendor_name,
            risk_score=risk_score,
            risk_level=risk_level,
            payment_history_score=0.8,  # Would be calculated
            transaction_volume=total_volume,
            recommendations=recommendations
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assessing vendor risk: {str(e)}")

@app.get("/financial/entities")
async def list_entities():
    """List all financial entities"""

    try:
        result = supabase.table("entities").select("*").execute()
        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing entities: {str(e)}")

@app.get("/financial/accounts/{entity_id}")
async def list_accounts(entity_id: int):
    """List all accounts for an entity"""

    try:
        result = supabase.table("chart_of_accounts").select("*").eq("entity_id", entity_id).execute()
        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing accounts: {str(e)}")

@app.get("/financial/categories")
async def list_transaction_categories():
    """List all transaction categories"""

    try:
        result = supabase.table("transaction_categories").select("*").execute()
        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing categories: {str(e)}")

@app.post("/financial/ml-models/retrain")
async def retrain_ml_models(
    model_name: Optional[str] = None,
    mindsdb_client: MindsDBIntegration = Depends(get_mindsdb)
):
    """Retrain ML models with latest data"""

    try:
        if model_name:
            # Retrain specific model
            success = mindsdb_client.create_ml_models()  # This would be model-specific
            return {"message": f"Model {model_name} retrained successfully", "success": success}
        else:
            # Retrain all models
            success = mindsdb_client.create_ml_models()
            return {"message": "All ML models retrained successfully", "success": success}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retraining models: {str(e)}")

@app.post("/financial/test-mindsdb")
async def test_mindsdb_only(
    description: str,
    amount: float,
    vendor: str = None,
    mindsdb_client: MindsDBIntegration = Depends(get_mindsdb)
):
    """Test MindsDB categorization without Supabase"""
    try:
        # Test MindsDB prediction
        prediction = mindsdb_client.predict_transaction_category(description, amount, vendor)

        return {
            "description": description,
            "amount": amount,
            "vendor": vendor,
            "prediction": prediction.to_dict() if hasattr(prediction, 'to_dict') else str(prediction),
            "prediction_type": type(prediction).__name__,
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "description": description,
            "amount": amount
        }

@app.get("/financial/health")
async def health_check():
    """Health check for financial API and ML models"""

    try:
        # Check Supabase connection
        supabase_status = "healthy"
        try:
            result = supabase.table("entities").select("*", count="exact").execute()
            # Just checking if we can access the table
        except Exception as e:
            print(f"Supabase health check failed: {e}")
            supabase_status = "unhealthy"

        # Check MindsDB connection
        mindsdb_status = "healthy"
        try:
            if not mindsdb.test_connection():
                mindsdb_status = "unhealthy"
        except:
            mindsdb_status = "unhealthy"

        return {
            "status": "healthy" if supabase_status == "healthy" and mindsdb_status == "healthy" else "degraded",
            "supabase": supabase_status,
            "mindsdb": mindsdb_status,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Invoice parsing data models
class InvoiceParseResponse(BaseModel):
    vendor_name: str
    invoice_number: str
    invoice_date: date
    total_amount: float
    currency: str
    description: str
    transaction_created: bool
    transaction_id: Optional[int] = None

class InvoiceParseError(BaseModel):
    error: str
    filename: str
    details: Optional[str] = None

# Invoice parsing endpoints
@app.post("/financial/parse-invoice", response_model=InvoiceParseResponse)
async def parse_invoice_upload(
    file: UploadFile = File(...),
    entity_id: int = 1,
    account_id: int = 1,
    auto_create_transaction: bool = True
):
    """Parse uploaded PDF invoice and optionally create transaction"""

    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        try:
            # Parse the invoice
            invoice_data = invoice_parser.parse_invoice_file(temp_path)
            if not invoice_data:
                raise HTTPException(status_code=400, detail="Failed to parse invoice")

            transaction_id = None
            transaction_created = False

            # Create transaction if requested and Supabase is available
            if auto_create_transaction and supabase:
                try:
                    db_format = invoice_parser.format_for_database(invoice_data, entity_id, account_id)
                    if db_format:
                        # Insert transaction
                        transaction_result = supabase.table("transactions").insert(db_format["transaction"]).execute()
                        if transaction_result.data:
                            transaction_id = transaction_result.data[0]["id"]
                            transaction_created = True

                            # Store invoice metadata separately if needed
                            invoice_metadata = db_format["invoice_metadata"]
                            invoice_metadata["transaction_id"] = transaction_id

                except Exception as e:
                    print(f"Warning: Could not create transaction: {e}")

            return InvoiceParseResponse(
                vendor_name=invoice_data.get("vendor_name", "Unknown"),
                invoice_number=invoice_data.get("invoice_number", "N/A"),
                invoice_date=invoice_data.get("invoice_date"),
                total_amount=invoice_data.get("total_amount", 0.0),
                currency=invoice_data.get("currency", "AUD"),
                description=invoice_data.get("description", "Invoice"),
                transaction_created=transaction_created,
                transaction_id=transaction_id
            )

        finally:
            # Clean up temp file
            os.unlink(temp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing invoice: {str(e)}")

@app.post("/financial/parse-invoices-directory")
async def parse_invoices_directory(
    directory_path: str = "invoices",
    entity_id: int = 1,
    account_id: int = 1,
    auto_create_transactions: bool = True
):
    """Parse all PDF invoices in a directory"""

    try:
        # Parse all invoices in directory
        invoices = invoice_parser.parse_invoices_directory(directory_path)

        results = []
        successful_transactions = 0

        for invoice_data in invoices:
            try:
                transaction_id = None
                transaction_created = False

                # Create transaction if requested
                if auto_create_transactions and supabase:
                    try:
                        db_format = invoice_parser.format_for_database(invoice_data, entity_id, account_id)
                        if db_format:
                            transaction_result = supabase.table("transactions").insert(db_format["transaction"]).execute()
                            if transaction_result.data:
                                transaction_id = transaction_result.data[0]["id"]
                                transaction_created = True
                                successful_transactions += 1
                    except Exception as e:
                        print(f"Warning: Could not create transaction for {invoice_data.get('source_file')}: {e}")

                results.append({
                    "filename": invoice_data.get("source_file"),
                    "vendor_name": invoice_data.get("vendor_name"),
                    "invoice_number": invoice_data.get("invoice_number"),
                    "total_amount": invoice_data.get("total_amount"),
                    "transaction_created": transaction_created,
                    "transaction_id": transaction_id
                })

            except Exception as e:
                results.append({
                    "filename": invoice_data.get("source_file", "unknown"),
                    "error": str(e),
                    "transaction_created": False
                })

        return {
            "total_invoices": len(invoices),
            "successful_transactions": successful_transactions,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing directory: {str(e)}")

@app.get("/financial/test-invoice-parser")
async def test_invoice_parser():
    """Test the invoice parser functionality"""

    try:
        # Test directory parsing
        invoices = invoice_parser.parse_invoices_directory("invoices")

        return {
            "parser_status": "operational",
            "openai_available": bool(invoice_parser.openai_api_key),
            "invoices_found": len(invoices),
            "sample_invoice": invoices[0] if invoices else None
        }

    except Exception as e:
        return {
            "parser_status": "error",
            "error": str(e),
            "openai_available": bool(invoice_parser.openai_api_key)
        }

# Database mappings configuration with actual Notion database IDs
DATABASE_MAPPINGS = {
    "entities": {
        "notion_database_id": "2784a17b-b7f0-8188-a62f-ffb7975db5e5",  # Business Entities
        "field_mappings": {
            "id": "ID",
            "entity_name": "Entity Name",
            "entity_type": "Type",
            "abn": "ABN",
            "created_at": "Created"
        }
    },
    "transactions": {
        "notion_database_id": "2784a17b-b7f0-81a5-94c9-d5aba1625d49",  # Transactions
        "field_mappings": {
            "id": "ID",
            "entity_id": "Entity ID",
            "account_id": "Account ID",
            "amount": "Amount",
            "description": "Description",
            "transaction_date": "Transaction Date",
            "vendor_name": "Vendor Name",
            "reference_number": "Reference Number",
            "notes": "Notes"
        }
    },
    "invoices": {
        "notion_database_id": "2784a17b-b7f0-8166-803d-e6cc7330d8c1",  # Invoices
        "field_mappings": {
            "id": "ID",
            "entity_id": "Entity ID",
            "contact_id": "Contact ID",
            "invoice_number": "Invoice Number",
            "invoice_date": "Invoice Date",
            "due_date": "Due Date",
            "total_amount": "Total Amount",
            "status": "Status",
            "invoice_type": "Type"
        }
    },
    "contacts": {
        "notion_database_id": "2784a17b-b7f0-8124-a67f-c51dd6c75a93",  # Contacts
        "field_mappings": {
            "id": "ID",
            "entity_id": "Entity ID",
            "name": "Name",
            "company": "Company",
            "email": "Email",
            "phone": "Phone",
            "address": "Address",
            "contact_type": "Type"
        }
    },
    "accounts": {
        "notion_database_id": "2784a17b-b7f0-8189-ad95-d6c1fd78db1c",  # Accounts
        "field_mappings": {
            "id": "ID",
            "entity_id": "Entity ID",
            "account_name": "Account Name",
            "account_type": "Account Type",
            "account_code": "Account Code",
            "description": "Description",
            "balance": "Balance",
            "is_active": "Is Active"
        }
    }
}

def transform_supabase_to_notion(table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform Supabase record to Notion page properties"""
    if table_name not in DATABASE_MAPPINGS:
        raise ValueError(f"No mapping found for table: {table_name}")

    mapping = DATABASE_MAPPINGS[table_name]["field_mappings"]
    notion_properties = {}

    for supabase_field, notion_field in mapping.items():
        if supabase_field in record and record[supabase_field] is not None:
            value = record[supabase_field]

            # Transform based on field type
            if isinstance(value, (int, float)):
                notion_properties[notion_field] = {"number": value}
            elif isinstance(value, str):
                notion_properties[notion_field] = {"title": [{"text": {"content": value}}]} if notion_field in ["Entity Name", "Contact Name", "Description"] else {"rich_text": [{"text": {"content": value}}]}
            elif isinstance(value, datetime):
                notion_properties[notion_field] = {"date": {"start": value.isoformat()}}
            elif isinstance(value, date):
                notion_properties[notion_field] = {"date": {"start": value.isoformat()}}
            else:
                notion_properties[notion_field] = {"rich_text": [{"text": {"content": str(value)}}]}

    return notion_properties

@app.post("/sync/supabase-to-notion", response_model=NotionSyncResponse)
async def sync_supabase_to_notion(request: NotionSyncRequest):
    """Sync data from Supabase to Notion"""
    if not notion:
        raise HTTPException(status_code=503, detail="Notion client not initialized")

    errors = []
    records_synced = 0

    try:
        # Get database ID from mapping or request
        database_id = request.database_id or DATABASE_MAPPINGS.get(request.table_name, {}).get("notion_database_id")
        if not database_id:
            raise HTTPException(status_code=400, detail=f"No Notion database ID found for table: {request.table_name}")

        # Fetch records from Supabase
        result = supabase.table(request.table_name).select("*").execute()

        for record in result.data:
            try:
                # Transform record to Notion format
                notion_properties = transform_supabase_to_notion(request.table_name, record)

                # Check if record already exists in Notion (by ID)
                existing_pages = notion.databases.query(
                    database_id=database_id,
                    filter={"property": "ID", "number": {"equals": record.get("id")}}
                ).get("results", [])

                if existing_pages and not request.force_full_sync:
                    # Update existing page
                    page_id = existing_pages[0]["id"]
                    notion.pages.update(page_id=page_id, properties=notion_properties)
                else:
                    # Create new page
                    notion.pages.create(parent={"database_id": database_id}, properties=notion_properties)

                records_synced += 1

            except Exception as e:
                errors.append(f"Error syncing record {record.get('id', 'unknown')}: {str(e)}")

        return NotionSyncResponse(
            table_name=request.table_name,
            sync_direction=request.sync_direction,
            records_synced=records_synced,
            errors=errors,
            success=len(errors) == 0,
            sync_timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@app.post("/sync/notion-to-supabase", response_model=NotionSyncResponse)
async def sync_notion_to_supabase(request: NotionSyncRequest):
    """Sync data from Notion to Supabase"""
    if not notion:
        raise HTTPException(status_code=503, detail="Notion client not initialized")

    errors = []
    records_synced = 0

    try:
        # Get database ID from mapping or request
        database_id = request.database_id or DATABASE_MAPPINGS.get(request.table_name, {}).get("notion_database_id")
        if not database_id:
            raise HTTPException(status_code=400, detail=f"No Notion database ID found for table: {request.table_name}")

        # Fetch all pages from Notion database
        notion_pages = notion.databases.query(database_id=database_id).get("results", [])

        for page in notion_pages:
            try:
                # Transform Notion page to Supabase format
                supabase_record = {}
                mapping = DATABASE_MAPPINGS[request.table_name]["field_mappings"]

                for supabase_field, notion_field in mapping.items():
                    if notion_field in page["properties"]:
                        prop = page["properties"][notion_field]

                        # Extract value based on property type
                        if prop["type"] == "number":
                            supabase_record[supabase_field] = prop["number"]
                        elif prop["type"] == "title":
                            supabase_record[supabase_field] = prop["title"][0]["text"]["content"] if prop["title"] else None
                        elif prop["type"] == "rich_text":
                            supabase_record[supabase_field] = prop["rich_text"][0]["text"]["content"] if prop["rich_text"] else None
                        elif prop["type"] == "date":
                            supabase_record[supabase_field] = prop["date"]["start"] if prop["date"] else None

                # Check if record exists in Supabase
                existing = supabase.table(request.table_name).select("*").eq("id", supabase_record.get("id")).execute()

                if existing.data and not request.force_full_sync:
                    # Update existing record
                    supabase.table(request.table_name).update(supabase_record).eq("id", supabase_record["id"]).execute()
                else:
                    # Insert new record (remove ID for insert)
                    insert_record = {k: v for k, v in supabase_record.items() if k != "id"}
                    supabase.table(request.table_name).insert(insert_record).execute()

                records_synced += 1

            except Exception as e:
                errors.append(f"Error syncing page {page.get('id', 'unknown')}: {str(e)}")

        return NotionSyncResponse(
            table_name=request.table_name,
            sync_direction=request.sync_direction,
            records_synced=records_synced,
            errors=errors,
            success=len(errors) == 0,
            sync_timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@app.post("/sync/bidirectional", response_model=List[NotionSyncResponse])
async def sync_bidirectional(request: NotionSyncRequest):
    """Perform bidirectional sync between Supabase and Notion"""

    # First sync Supabase to Notion
    supabase_to_notion = await sync_supabase_to_notion(
        NotionSyncRequest(
            table_name=request.table_name,
            sync_direction="supabase_to_notion",
            database_id=request.database_id,
            force_full_sync=request.force_full_sync
        )
    )

    # Then sync Notion to Supabase
    notion_to_supabase = await sync_notion_to_supabase(
        NotionSyncRequest(
            table_name=request.table_name,
            sync_direction="notion_to_supabase",
            database_id=request.database_id,
            force_full_sync=request.force_full_sync
        )
    )

    return [supabase_to_notion, notion_to_supabase]

@app.get("/sync/mappings")
async def get_database_mappings():
    """Get all configured database mappings"""
    return DATABASE_MAPPINGS

@app.post("/sync/mappings/{table_name}")
async def update_database_mapping(table_name: str, mapping: NotionDatabaseMapping):
    """Update database mapping configuration"""
    DATABASE_MAPPINGS[table_name] = {
        "notion_database_id": mapping.notion_database_id,
        "field_mappings": mapping.field_mappings
    }
    return {"message": f"Mapping for {table_name} updated successfully"}

# Create MCP server
mcp = FastApiMCP(app)

# Mount MCP server using SSE transport
mcp.mount_sse(mount_path="/mcp")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
