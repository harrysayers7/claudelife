#!/usr/bin/env python3
"""
GST Threshold Validator - Supabase Integration

Monitors GST threshold ($75,000) for Harry's entities by querying Supabase
financial data. Alerts when approaching threshold with 3-tier system.

Usage:
    # Query Supabase for real data
    python validate_gst_threshold.py --entity "MOK HOUSE PTY LTD"

    # Query specific ABN
    python validate_gst_threshold.py --abn "38 690 628 212"

    # Check all entities
    python validate_gst_threshold.py --all

Requires:
    - SUPABASE_URL environment variable
    - SUPABASE_KEY environment variable (service role key)
    - pip install supabase (install with: pip3 install supabase)
"""

import argparse
import sys
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Error: supabase package not installed")
    print("\nInstall with:")
    print("  pip3 install supabase")
    sys.exit(1)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://gshsshaodoyttdxippwx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# GST constants
GST_THRESHOLD = 75000
ALERT_THRESHOLDS = {
    "green": (0, 0.49),      # 0-49%
    "yellow": (0.50, 0.69),  # 50-69%
    "red": (0.70, 0.99),     # 70-99%
    "critical": (1.0, float('inf'))  # 100%+
}


def get_supabase_client() -> Client:
    """Initialize Supabase client."""
    if not SUPABASE_KEY:
        print("❌ Error: SUPABASE_KEY environment variable not set")
        print("\nSet it with:")
        print("  export SUPABASE_KEY='your-service-role-key'")
        sys.exit(1)

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_entity_by_name(supabase: Client, name: str) -> Optional[Dict]:
    """Fetch entity from Supabase by name."""
    try:
        response = supabase.table("entities").select("*").ilike("name", f"%{name}%").execute()

        if not response.data:
            return None

        if len(response.data) > 1:
            print(f"⚠️  Multiple entities found matching '{name}':")
            for entity in response.data:
                print(f"   - {entity['name']} (ABN: {entity['abn']})")
            print("\nPlease specify ABN with --abn flag")
            sys.exit(1)

        return response.data[0]
    except Exception as e:
        print(f"❌ Error fetching entity: {e}")
        sys.exit(1)


def get_entity_by_abn(supabase: Client, abn: str) -> Optional[Dict]:
    """Fetch entity from Supabase by ABN."""
    try:
        response = supabase.table("entities").select("*").eq("abn", abn).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"❌ Error fetching entity: {e}")
        sys.exit(1)


def get_all_entities(supabase: Client) -> List[Dict]:
    """Fetch all entities from Supabase."""
    try:
        response = supabase.table("entities").select("*").execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching entities: {e}")
        sys.exit(1)


def calculate_rolling_12m_income(supabase: Client, entity_id: str) -> Dict[str, float]:
    """
    Calculate rolling 12-month income from transactions and invoices.

    Returns:
        Dict with transaction_income, invoice_income, total_income
    """
    twelve_months_ago = (datetime.now() - timedelta(days=365)).date().isoformat()

    # Get income from transactions (positive total_amount)
    try:
        tx_response = supabase.table("transactions")\
            .select("total_amount")\
            .eq("entity_id", entity_id)\
            .gte("transaction_date", twelve_months_ago)\
            .execute()

        transaction_income = sum(
            float(tx["total_amount"])
            for tx in tx_response.data
            if float(tx["total_amount"]) > 0
        )
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch transactions: {e}")
        transaction_income = 0.0

    # Get income from invoices (receivables)
    try:
        inv_response = supabase.table("invoices")\
            .select("total_amount")\
            .eq("entity_id", entity_id)\
            .eq("invoice_type", "receivable")\
            .gte("invoice_date", twelve_months_ago)\
            .execute()

        invoice_income = sum(float(inv["total_amount"]) for inv in inv_response.data)
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch invoices: {e}")
        invoice_income = 0.0

    # Total income (use max to avoid double-counting if both exist)
    total_income = max(transaction_income, invoice_income)

    return {
        "transaction_income": transaction_income,
        "invoice_income": invoice_income,
        "total_income": total_income,
    }


def get_gst_monitoring_data(supabase: Client, entity_id: str) -> Optional[Dict]:
    """Fetch existing GST monitoring data from gst_threshold_monitoring table."""
    try:
        current_fy = f"FY{datetime.now().year % 100:02d}"

        response = supabase.table("gst_threshold_monitoring")\
            .select("*")\
            .eq("entity_id", entity_id)\
            .eq("financial_year", current_fy)\
            .execute()

        return response.data[0] if response.data else None
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch GST monitoring data: {e}")
        return None


def update_gst_monitoring_table(
    supabase: Client,
    entity_id: str,
    turnover: float,
    projected_annual: Optional[float] = None
):
    """Update or insert GST monitoring record."""
    current_fy = f"FY{datetime.now().year % 100:02d}"
    threshold_pct = (turnover / GST_THRESHOLD) * 100

    data = {
        "entity_id": entity_id,
        "financial_year": current_fy,
        "current_turnover": turnover,
        "threshold_percentage": threshold_pct,
        "last_calculated_at": datetime.now().isoformat(),
    }

    if projected_annual:
        data["projected_annual_turnover"] = projected_annual

    try:
        # Check if record exists
        existing = get_gst_monitoring_data(supabase, entity_id)

        if existing:
            # Update existing record
            supabase.table("gst_threshold_monitoring")\
                .update(data)\
                .eq("id", existing["id"])\
                .execute()
        else:
            # Insert new record
            supabase.table("gst_threshold_monitoring")\
                .insert(data)\
                .execute()

        print(f"✅ Updated gst_threshold_monitoring table")
    except Exception as e:
        print(f"⚠️  Warning: Could not update monitoring table: {e}")


def determine_status(income: float, is_registered: bool) -> Dict:
    """
    Determine GST threshold status based on income.

    Returns:
        Dict with emoji, status_text, color, action
    """
    if is_registered:
        return {
            "emoji": "✅",
            "status": "REGISTERED",
            "color": "blue",
            "action": "Lodge BAS quarterly/monthly as required",
        }

    percentage = income / GST_THRESHOLD

    if percentage < ALERT_THRESHOLDS["yellow"][0]:
        # Green zone (0-49%)
        return {
            "emoji": "🟢",
            "status": "GREEN ZONE (0-49%)",
            "color": "green",
            "action": "No immediate action required",
        }
    elif percentage < ALERT_THRESHOLDS["red"][0]:
        # Yellow zone (50-69%)
        return {
            "emoji": "🟡",
            "status": "YELLOW ZONE (50-69%)",
            "color": "yellow",
            "action": "Prepare for GST registration",
        }
    elif percentage < ALERT_THRESHOLDS["critical"][0]:
        # Red zone (70-99%)
        return {
            "emoji": "🔴",
            "status": "RED ZONE (70-99%)",
            "color": "red",
            "action": "⚠️  Register proactively before hitting $75K",
        }
    else:
        # Critical (100%+)
        return {
            "emoji": "🚨",
            "status": "CRITICAL (100%+)",
            "color": "red",
            "action": "🚨 MUST REGISTER within 21 days of exceeding threshold",
        }


def format_currency(amount: float) -> str:
    """Format as Australian currency."""
    return f"${amount:,.2f}"


def print_separator(char: str = "─", length: int = 60):
    """Print separator line."""
    print(char * length)


def print_entity_status(entity: Dict, income_data: Dict, monitoring_data: Optional[Dict]):
    """Print formatted GST threshold status for an entity."""

    # Extract data
    entity_name = entity["name"]
    abn = entity["abn"]
    is_registered = entity.get("gst_registered", False)

    total_income = income_data["total_income"]
    threshold_pct = (total_income / GST_THRESHOLD) * 100
    remaining = GST_THRESHOLD - total_income

    status = determine_status(total_income, is_registered)

    # Print header
    print_separator("═")
    print("GST THRESHOLD VALIDATION - FY2025-26")
    print_separator("═")
    print()

    # Entity info
    print(f"Entity: {entity_name}")
    print(f"ABN: {abn}")
    print(f"Registration Status: {'✅ Registered' if is_registered else '❌ Not Registered'}")
    print()

    # Income breakdown
    print_separator()
    print("ROLLING 12-MONTH INCOME")
    print_separator()
    print(f"Transaction Income:   {format_currency(income_data['transaction_income'])}")
    print(f"Invoice Income:       {format_currency(income_data['invoice_income'])}")
    print(f"Total Income:         {format_currency(total_income)}")
    print()

    # Threshold analysis
    print_separator()
    print("THRESHOLD ANALYSIS")
    print_separator()
    print(f"GST Threshold:        {format_currency(GST_THRESHOLD)}")
    print(f"Percentage Used:      {threshold_pct:.2f}%")
    print()
    print(f"Status: {status['emoji']} {status['status']}")
    print(f"        {status['action']}")
    print()

    if not is_registered:
        print(f"Remaining Capacity:   {format_currency(remaining)}")
        print()

    # Monitoring data (if exists)
    if monitoring_data:
        print_separator()
        print("MONITORING DATA")
        print_separator()
        print(f"Last Calculated:      {monitoring_data.get('last_calculated_at', 'N/A')}")
        if monitoring_data.get("projected_annual_turnover"):
            print(f"Projected Annual:     {format_currency(monitoring_data['projected_annual_turnover'])}")
        if monitoring_data.get("projected_threshold_date"):
            print(f"Projected Threshold:  {monitoring_data['projected_threshold_date']}")
        print()

    # Recommendations
    print_separator()
    print("📋 RECOMMENDATIONS")
    print_separator()

    if is_registered:
        print("  ✅ GST registered - ensure compliance:")
        print("     • Lodge BAS on time (monthly/quarterly)")
        print("     • Issue tax invoices for sales ≥ $82.50")
        print("     • Claim input tax credits on eligible purchases")
    elif threshold_pct >= 70:
        print("  🚨 Urgent Action Required:")
        print("     • Register for GST proactively")
        print("     • Prepare accounting systems for GST")
        print("     • Review pricing (add GST to quotes)")
        print("     • Notify existing clients of GST changes")
    elif threshold_pct >= 50:
        print("  ⚠️  Prepare for GST Registration:")
        print("     • Monitor income closely (monthly)")
        print("     • Prepare GST-compliant invoicing system")
        print("     • Review accounting software capabilities")
        print("     • Consider registering early for ITC claims")
    else:
        print("  ✅ No action required currently")
        print("     • Continue monitoring quarterly")
        print("     • Consider voluntary registration for ITC benefits")

    print()
    print_separator()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate GST threshold status using Supabase data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  SUPABASE_URL    Supabase project URL (default: gshsshaodoyttdxippwx.supabase.co)
  SUPABASE_KEY    Supabase service role key (required)

Examples:
  # Check specific entity by name
  python validate_gst_threshold.py --entity "MOK HOUSE"

  # Check by ABN
  python validate_gst_threshold.py --abn "38 690 628 212"

  # Check all entities
  python validate_gst_threshold.py --all

  # Update monitoring table
  python validate_gst_threshold.py --entity "MOK HOUSE" --update-db
        """,
    )

    parser.add_argument(
        "--entity",
        type=str,
        help="Entity name to check (e.g., 'MOK HOUSE', 'MOKAI')",
    )

    parser.add_argument(
        "--abn",
        type=str,
        help="Entity ABN to check (e.g., '38 690 628 212')",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Check all entities in Supabase",
    )

    parser.add_argument(
        "--update-db",
        action="store_true",
        help="Update gst_threshold_monitoring table with results",
    )

    args = parser.parse_args()

    # Validate arguments
    if not any([args.entity, args.abn, args.all]):
        parser.error("Must provide --entity, --abn, or --all")

    # Initialize Supabase
    supabase = get_supabase_client()

    # Fetch entities
    entities = []
    if args.all:
        entities = get_all_entities(supabase)
        if not entities:
            print("❌ No entities found in database")
            sys.exit(1)
    elif args.abn:
        entity = get_entity_by_abn(supabase, args.abn)
        if not entity:
            print(f"❌ No entity found with ABN: {args.abn}")
            sys.exit(1)
        entities = [entity]
    elif args.entity:
        entity = get_entity_by_name(supabase, args.entity)
        if not entity:
            print(f"❌ No entity found matching: {args.entity}")
            sys.exit(1)
        entities = [entity]

    # Process each entity
    for entity in entities:
        # Calculate income
        income_data = calculate_rolling_12m_income(supabase, entity["id"])

        # Get monitoring data
        monitoring_data = get_gst_monitoring_data(supabase, entity["id"])

        # Print status
        print_entity_status(entity, income_data, monitoring_data)

        # Update database if requested
        if args.update_db:
            update_gst_monitoring_table(
                supabase,
                entity["id"],
                income_data["total_income"]
            )

        # Add separator between entities
        if len(entities) > 1:
            print("\n" * 2)


if __name__ == "__main__":
    main()
