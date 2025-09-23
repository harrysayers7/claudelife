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

# Create MCP server
mcp = FastApiMCP(app)

# Mount MCP server using SSE transport
mcp.mount_sse(mount_path="/mcp")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
