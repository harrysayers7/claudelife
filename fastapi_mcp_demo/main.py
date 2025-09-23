from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(
    title="Claudelife Business API",
    description="MOKAI business operations exposed as MCP tools",
    version="1.0.0"
)

# Data models
class ComplianceCheck(BaseModel):
    vendor_abn: str
    framework: str  # "IRAP", "Essential8", etc.

class ComplianceResult(BaseModel):
    vendor_abn: str
    framework: str
    status: str
    score: int
    details: Dict[str, Any]

class TenderRequest(BaseModel):
    keywords: str
    max_value: int = 1000000

# Business endpoints that become MCP tools
@app.post("/compliance/check", response_model=ComplianceResult)
async def check_vendor_compliance(request: ComplianceCheck):
    """Check vendor compliance against security frameworks"""

    # Mock compliance logic - replace with real checks
    mock_score = 85 if "cyber" in request.vendor_abn.lower() else 72

    return ComplianceResult(
        vendor_abn=request.vendor_abn,
        framework=request.framework,
        status="compliant" if mock_score >= 75 else "non-compliant",
        score=mock_score,
        details={
            "last_assessment": "2024-01-15",
            "certifications": ["ISO27001", "SOC2"],
            "risk_level": "low" if mock_score >= 75 else "medium"
        }
    )

@app.get("/tenders/search")
async def search_government_tenders(keywords: str, max_value: int = 1000000):
    """Search for relevant government tenders"""

    # Mock tender data - replace with real scraping/API calls
    mock_tenders = [
        {
            "id": "ATM001",
            "title": f"Cybersecurity Assessment Services - {keywords}",
            "agency": "Department of Defence",
            "value": 750000,
            "deadline": "2024-02-15",
            "requirements": ["IRAP assessment", "Security clearance"]
        },
        {
            "id": "ATM002",
            "title": f"IT Infrastructure Review - {keywords}",
            "agency": "Services Australia",
            "value": 450000,
            "deadline": "2024-03-01",
            "requirements": ["Essential 8", "Risk assessment"]
        }
    ]

    # Filter by value
    filtered_tenders = [t for t in mock_tenders if t["value"] <= max_value]

    return {
        "query": keywords,
        "max_value": max_value,
        "results": filtered_tenders,
        "count": len(filtered_tenders)
    }

@app.get("/client/{client_id}/status")
async def get_client_project_status(client_id: str):
    """Get current project status for a client"""

    # Mock client data - replace with real database queries
    mock_status = {
        "client_id": client_id,
        "projects": [
            {
                "name": "IRAP Assessment",
                "status": "in_progress",
                "completion": 65,
                "next_milestone": "Security control testing",
                "due_date": "2024-02-28"
            },
            {
                "name": "Penetration Testing",
                "status": "scheduled",
                "completion": 0,
                "next_milestone": "Scope definition",
                "due_date": "2024-03-15"
            }
        ],
        "total_value": 125000,
        "last_updated": "2024-01-20"
    }

    return mock_status

@app.get("/dashboard/metrics")
async def get_business_metrics():
    """Get key business metrics for MOKAI"""

    return {
        "active_projects": 8,
        "revenue_ytd": 750000,
        "compliance_assessments_completed": 23,
        "tender_responses_submitted": 12,
        "pipeline_value": 2100000,
        "client_satisfaction": 4.8
    }

# Create MCP server
mcp = FastApiMCP(app)

# Mount MCP server using SSE transport (makes all endpoints available as MCP tools)
mcp.mount_sse(mount_path="/mcp")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
