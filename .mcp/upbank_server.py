#!/usr/bin/env python3
"""FastMCP UpBank Server - Clean Up Bank transaction tracking and account management"""

from fastmcp import FastMCP
from typing import Dict, List, Optional, Any
import os
import requests
from datetime import datetime, timedelta
from dateutil.parser import parse
import json

# Initialize MCP server
mcp = FastMCP("UpBank Assistant")

# Up Bank API configuration
API_BASE_URL = os.environ.get("UPBANK_API_BASE_URL", "https://api.up.com.au/api/v1")
API_TOKEN = os.environ.get("UPBANK_API_TOKEN", "")

class UpBankError(Exception):
    """Custom exception for Up Bank API errors"""
    pass

def make_api_request(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """Make authenticated request to Up Bank API"""
    if not API_TOKEN:
        raise UpBankError("UPBANK_API_TOKEN environment variable not set")

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }
    url = f"{API_BASE_URL}/{endpoint}"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise UpBankError(f"API request failed: {str(e)}")

@mcp.tool()
def get_accounts() -> str:
    """Get all your Up Bank accounts with current balances

    Returns:
        JSON string with account information including balances
    """
    try:
        result = make_api_request("accounts")
        accounts = []

        for acc in result.get("data", []):
            accounts.append({
                "id": acc["id"],
                "name": acc["attributes"]["displayName"],
                "type": acc["attributes"]["accountType"],
                "balance": float(acc["attributes"]["balance"]["value"]),
                "currency": acc["attributes"]["balance"]["currencyCode"],
                "created": acc["attributes"]["createdAt"]
            })

        return json.dumps({
            "success": True,
            "accounts": accounts,
            "total_accounts": len(accounts)
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)

@mcp.tool()
def get_recent_transactions(account_id: str = "", days: int = 7, limit: int = 20) -> str:
    """Get recent transactions from Up Bank

    Args:
        account_id: Specific account ID (optional, gets from all accounts if empty)
        days: Number of days to look back (default: 7)
        limit: Maximum number of transactions to return (default: 20)

    Returns:
        JSON string with transaction details
    """
    try:
        # Calculate date filter
        since_date = (datetime.now() - timedelta(days=days)).isoformat()

        params = {
            "filter[since]": since_date,
            "page[size]": str(limit)
        }

        # Add account filter if specified
        if account_id:
            params["filter[account]"] = account_id

        result = make_api_request("transactions", params)
        transactions = []

        for txn in result.get("data", []):
            attr = txn["attributes"]

            # Parse transaction details
            transaction = {
                "id": txn["id"],
                "description": attr["description"],
                "amount": float(attr["amount"]["value"]),
                "currency": attr["amount"]["currencyCode"],
                "status": attr["status"],
                "created": attr["createdAt"],
                "settled": attr.get("settledAt"),
                "account_id": txn["relationships"]["account"]["data"]["id"]
            }

            # Add merchant info if available
            if "merchant" in txn["relationships"] and txn["relationships"]["merchant"]["data"]:
                merchant_id = txn["relationships"]["merchant"]["data"]["id"]
                # Find merchant in included data
                for included in result.get("included", []):
                    if included["id"] == merchant_id:
                        transaction["merchant"] = included["attributes"]["name"]
                        break

            transactions.append(transaction)

        return json.dumps({
            "success": True,
            "transactions": transactions,
            "count": len(transactions),
            "period_days": days
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)

@mcp.tool()
def get_spending_summary(days: int = 30) -> str:
    """Get spending summary with category analysis based on Up Bank categories

    Args:
        days: Number of days to analyze (default: 30)

    Returns:
        JSON string with spending analysis including categories
    """
    try:
        # Get recent transactions with pagination
        since_date = (datetime.now() - timedelta(days=days)).isoformat()

        all_transactions = []
        next_page = None

        # Paginate through all transactions
        while True:
            params = {
                "filter[since]": since_date,
                "page[size]": "100"
            }
            if next_page:
                params["page[after]"] = next_page

            result = make_api_request("transactions", params)
            all_transactions.extend(result.get("data", []))

            # Check if there are more pages
            links = result.get("links", {})
            if "next" not in links:
                break
            next_page = links["next"].split("page[after]=")[-1].split("&")[0] if "page[after]=" in links["next"] else None
            if not next_page:
                break

        spending_total = 0.0
        income_total = 0.0
        transaction_count = 0
        merchants = {}
        categories = {}

        for txn in all_transactions:
            attr = txn["attributes"]
            amount = float(attr["amount"]["value"])
            transaction_count += 1

            if amount < 0:  # Spending (negative amounts)
                spending_total += abs(amount)
            else:  # Income (positive amounts)
                income_total += amount

            # Track merchant spending
            merchant_name = "Unknown"
            if "merchant" in txn["relationships"] and txn["relationships"]["merchant"]["data"]:
                merchant_id = txn["relationships"]["merchant"]["data"]["id"]
                for included in result.get("included", []):
                    if included["id"] == merchant_id:
                        merchant_name = included["attributes"]["name"]
                        break

            # Track category spending
            category_name = "Uncategorized"
            if "category" in txn["relationships"] and txn["relationships"]["category"]["data"]:
                category_id = txn["relationships"]["category"]["data"]["id"]
                for included in result.get("included", []):
                    if included["id"] == category_id and included["type"] == "categories":
                        category_name = included["attributes"]["name"]
                        break

            if amount < 0:  # Only track spending
                if merchant_name not in merchants:
                    merchants[merchant_name] = 0.0
                merchants[merchant_name] += abs(amount)

                if category_name not in categories:
                    categories[category_name] = 0.0
                categories[category_name] += abs(amount)

        # Sort by spending amount
        top_merchants = sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:10]
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        spending_transactions = [t for t in all_transactions if float(t["attributes"]["amount"]["value"]) < 0]
        avg_transaction = spending_total / max(1, len(spending_transactions))

        return json.dumps({
            "success": True,
            "period_days": days,
            "summary": {
                "total_spending": round(spending_total, 2),
                "total_income": round(income_total, 2),
                "net_change": round(income_total - spending_total, 2),
                "transaction_count": transaction_count,
                "spending_transactions": len(spending_transactions),
                "avg_transaction": round(avg_transaction, 2)
            },
            "top_merchants": [{"name": name, "amount": round(amount, 2)} for name, amount in top_merchants],
            "categories": [{"name": name, "amount": round(amount, 2)} for name, amount in top_categories]
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)

@mcp.tool()
def search_transactions(description: str = "", amount_min: float = 0, amount_max: float = 0, days: int = 30) -> str:
    """Search transactions by description or amount range

    Args:
        description: Search term for transaction description
        amount_min: Minimum amount (optional)
        amount_max: Maximum amount (optional)
        days: Number of days to search back (default: 30)

    Returns:
        JSON string with matching transactions
    """
    try:
        since_date = (datetime.now() - timedelta(days=days)).isoformat()

        params = {
            "filter[since]": since_date,
            "page[size]": "100"
        }

        result = make_api_request("transactions", params)
        matching_transactions = []

        for txn in result.get("data", []):
            attr = txn["attributes"]
            amount = float(attr["amount"]["value"])
            desc = attr["description"].lower()

            # Apply filters
            matches = True

            if description and description.lower() not in desc:
                matches = False

            if amount_min > 0 and abs(amount) < amount_min:
                matches = False

            if amount_max > 0 and abs(amount) > amount_max:
                matches = False

            if matches:
                transaction = {
                    "id": txn["id"],
                    "description": attr["description"],
                    "amount": amount,
                    "currency": attr["amount"]["currencyCode"],
                    "status": attr["status"],
                    "created": attr["createdAt"],
                    "account_id": txn["relationships"]["account"]["data"]["id"]
                }
                matching_transactions.append(transaction)

        return json.dumps({
            "success": True,
            "matches": matching_transactions,
            "count": len(matching_transactions),
            "search_criteria": {
                "description": description,
                "amount_min": amount_min,
                "amount_max": amount_max,
                "days": days
            }
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)

@mcp.tool()
def get_categories() -> str:
    """Get all available Up Bank transaction categories

    Returns:
        JSON string with category information
    """
    try:
        result = make_api_request("categories")
        categories = []

        for cat in result.get("data", []):
            categories.append({
                "id": cat["id"],
                "name": cat["attributes"]["name"],
                "parent": cat["relationships"]["parent"]["data"]["id"] if cat["relationships"]["parent"]["data"] else None
            })

        return json.dumps({
            "success": True,
            "categories": categories,
            "count": len(categories)
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)

@mcp.tool()
def get_transaction_by_id(transaction_id: str) -> str:
    """Get detailed information about a specific transaction

    Args:
        transaction_id: The Up Bank transaction ID

    Returns:
        JSON string with detailed transaction information
    """
    try:
        result = make_api_request(f"transactions/{transaction_id}")
        txn = result.get("data", {})

        if not txn:
            return json.dumps({
                "success": False,
                "error": "Transaction not found"
            }, indent=2)

        attr = txn["attributes"]
        transaction_detail = {
            "id": txn["id"],
            "description": attr["description"],
            "message": attr.get("message"),
            "amount": float(attr["amount"]["value"]),
            "currency": attr["amount"]["currencyCode"],
            "status": attr["status"],
            "created": attr["createdAt"],
            "settled": attr.get("settledAt"),
            "hold_info": attr.get("holdInfo"),
            "round_up": attr.get("roundUp"),
            "cashback": attr.get("cashback"),
            "account_id": txn["relationships"]["account"]["data"]["id"]
        }

        # Add category if available
        if "category" in txn["relationships"] and txn["relationships"]["category"]["data"]:
            category_id = txn["relationships"]["category"]["data"]["id"]
            for included in result.get("included", []):
                if included["id"] == category_id and included["type"] == "categories":
                    transaction_detail["category"] = included["attributes"]["name"]
                    break

        # Add merchant if available
        if "merchant" in txn["relationships"] and txn["relationships"]["merchant"]["data"]:
            merchant_id = txn["relationships"]["merchant"]["data"]["id"]
            for included in result.get("included", []):
                if included["id"] == merchant_id and included["type"] == "merchants":
                    transaction_detail["merchant"] = {
                        "name": included["attributes"]["name"],
                        "location": included["attributes"].get("location")
                    }
                    break

        # Add tags if available
        if "tags" in txn["relationships"]:
            tag_ids = [tag["id"] for tag in txn["relationships"]["tags"]["data"]]
            tags = []
            for included in result.get("included", []):
                if included["id"] in tag_ids and included["type"] == "tags":
                    tags.append(included["attributes"]["label"])
            if tags:
                transaction_detail["tags"] = tags

        return json.dumps({
            "success": True,
            "transaction": transaction_detail
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)

@mcp.tool()
def get_account_balance_history(account_id: str = "", days: int = 30) -> str:
    """Get account balance changes over time by analyzing transactions

    Args:
        account_id: Specific account ID (optional, uses first account if empty)
        days: Number of days to analyze (default: 30)

    Returns:
        JSON string with balance history analysis
    """
    try:
        # Get accounts first
        accounts_result = make_api_request("accounts")
        target_account = None

        if account_id:
            for acc in accounts_result.get("data", []):
                if acc["id"] == account_id:
                    target_account = acc
                    break
        else:
            # Use first account if no ID specified
            if accounts_result.get("data"):
                target_account = accounts_result["data"][0]

        if not target_account:
            return json.dumps({
                "success": False,
                "error": "Account not found"
            }, indent=2)

        current_balance = float(target_account["attributes"]["balance"]["value"])
        account_name = target_account["attributes"]["displayName"]

        # Get transactions for this account
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        params = {
            "filter[since]": since_date,
            "filter[account]": target_account["id"],
            "page[size]": "100"
        }

        result = make_api_request("transactions", params)
        transactions = result.get("data", [])

        # Calculate balance changes
        balance_changes = []
        running_balance = current_balance

        # Sort transactions by date (newest first, then work backwards)
        sorted_transactions = sorted(transactions,
                                   key=lambda x: x["attributes"]["createdAt"],
                                   reverse=True)

        for txn in sorted_transactions:
            amount = float(txn["attributes"]["amount"]["value"])
            date = txn["attributes"]["createdAt"]

            balance_changes.append({
                "date": date,
                "amount": amount,
                "balance_after": running_balance,
                "description": txn["attributes"]["description"]
            })

            # Work backwards to get balance before this transaction
            running_balance -= amount

        # Reverse to show chronological order (oldest first)
        balance_changes.reverse()

        return json.dumps({
            "success": True,
            "account": {
                "id": target_account["id"],
                "name": account_name,
                "current_balance": current_balance
            },
            "period_days": days,
            "balance_history": balance_changes,
            "starting_balance": running_balance if balance_changes else current_balance,
            "net_change": current_balance - running_balance if balance_changes else 0.0
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)

@mcp.tool()
def ping_api() -> str:
    """Test connection to Up Bank API

    Returns:
        JSON string with API status
    """
    try:
        result = make_api_request("util/ping")
        return json.dumps({
            "success": True,
            "api_status": "connected",
            "response": result
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "api_status": "error",
            "error": str(e)
        }, indent=2)

if __name__ == "__main__":
    mcp.run()