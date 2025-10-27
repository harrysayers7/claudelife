#!/usr/bin/env python3
"""
Tax Bracket Calculator for FY2025-26 - Supabase Integration

Calculates tax payable on income using Australian tax brackets, including
Medicare levy and Low Income Tax Offset (LITO). Now supports querying entity
income directly from Supabase database.

Usage:
    # Query entity income from Supabase
    python calculate_tax_bracket.py --entity "Harrison Robert Sayers"
    python calculate_tax_bracket.py --abn "38 690 628 212"

    # Manual income input (original functionality)
    python calculate_tax_bracket.py --income 45000
    python calculate_tax_bracket.py --income 45000 --entity-type individual
    python calculate_tax_bracket.py --income 100000 --entity-type company

    # Compare scenarios
    python calculate_tax_bracket.py --compare 35000,45000,50000,60000

Requires:
    - SUPABASE_URL environment variable
    - SUPABASE_KEY environment variable (service role key)
    - pip install supabase (install with: pip3 install supabase)
"""

import argparse
import sys
import os
from typing import Dict, Optional
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

# FY2025-26 Tax Brackets
INDIVIDUAL_BRACKETS = [
    (18200, 0.0),      # $0 - $18,200: 0%
    (45000, 0.19),     # $18,201 - $45,000: 19%
    (135000, 0.325),   # $45,001 - $135,000: 32.5%
    (190000, 0.37),    # $135,001 - $190,000: 37%
    (float('inf'), 0.45),  # $190,001+: 45%
]

# Tax rates for other entity types
COMPANY_TAX_RATE = 0.25  # 25% for Base Rate Entities
TRUST_DISTRIBUTED_RATE = 0.0  # 0% if distributed
TRUST_UNDISTRIBUTED_RATE = 0.45  # 45% if accumulated

# Medicare Levy
MEDICARE_LEVY_RATE = 0.02  # 2%
MEDICARE_LEVY_THRESHOLD = 26000  # Exemption threshold

# Low Income Tax Offset (LITO)
LITO_MAX = 700  # Maximum offset
LITO_TAPER_START = 37500  # Income where taper begins
LITO_TAPER_RATE = 0.05  # 5 cents per dollar over $37,500


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
                print(f"   - {entity['name']} (ABN: {entity.get('abn', 'N/A')})")
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


def calculate_entity_income_from_db(supabase: Client, entity_id: str) -> Dict[str, float]:
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


def calculate_individual_tax(income: float) -> Dict[str, float]:
    """
    Calculate tax for an individual, including Medicare and LITO.

    Returns:
        Dict with base_tax, medicare_levy, lito, total_tax, effective_rate
    """
    # Calculate base tax
    base_tax = 0.0
    remaining_income = income
    previous_threshold = 0

    for threshold, rate in INDIVIDUAL_BRACKETS:
        if remaining_income <= 0:
            break

        taxable_in_bracket = min(remaining_income, threshold - previous_threshold)
        base_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
        previous_threshold = threshold

    # Calculate Medicare Levy (2% on income above threshold)
    if income >= MEDICARE_LEVY_THRESHOLD:
        medicare_levy = income * MEDICARE_LEVY_RATE
    else:
        medicare_levy = 0.0

    # Calculate Low Income Tax Offset (LITO)
    if income <= LITO_TAPER_START:
        lito = LITO_MAX
    elif income <= LITO_TAPER_START + (LITO_MAX / LITO_TAPER_RATE):
        # Taper at 5 cents per dollar over $37,500
        lito = max(0, LITO_MAX - ((income - LITO_TAPER_START) * LITO_TAPER_RATE))
    else:
        lito = 0.0

    # Total tax (base + medicare - LITO)
    total_tax = base_tax + medicare_levy - lito
    total_tax = max(0, total_tax)  # Ensure non-negative

    # Effective rate
    effective_rate = (total_tax / income * 100) if income > 0 else 0.0

    return {
        "base_tax": base_tax,
        "medicare_levy": medicare_levy,
        "lito": lito,
        "total_tax": total_tax,
        "effective_rate": effective_rate,
    }


def calculate_company_tax(income: float) -> Dict[str, float]:
    """Calculate tax for a company (25% flat rate for BRE)."""
    total_tax = income * COMPANY_TAX_RATE
    effective_rate = COMPANY_TAX_RATE * 100

    return {
        "base_tax": total_tax,
        "medicare_levy": 0.0,
        "lito": 0.0,
        "total_tax": total_tax,
        "effective_rate": effective_rate,
    }


def calculate_trust_tax(income: float, distributed: bool = True) -> Dict[str, float]:
    """
    Calculate tax for a trust.

    Args:
        income: Trust net income
        distributed: If True, assumes 100% distributed (0% tax)
                    If False, treats as undistributed (45% tax)
    """
    if distributed:
        # Flow-through entity - beneficiaries pay tax
        return {
            "base_tax": 0.0,
            "medicare_levy": 0.0,
            "lito": 0.0,
            "total_tax": 0.0,
            "effective_rate": 0.0,
            "note": "Beneficiaries taxed at marginal rates",
        }
    else:
        # Undistributed income taxed at top rate
        total_tax = income * TRUST_UNDISTRIBUTED_RATE
        return {
            "base_tax": total_tax,
            "medicare_levy": 0.0,
            "lito": 0.0,
            "total_tax": total_tax,
            "effective_rate": TRUST_UNDISTRIBUTED_RATE * 100,
            "note": "⚠️ Avoid accumulating income in trust!",
        }


def format_currency(amount: float) -> str:
    """Format amount as Australian currency."""
    return f"${amount:,.2f}"


def print_separator(char: str = "─", length: int = 60):
    """Print a separator line."""
    print(char * length)


def print_tax_breakdown(
    income: float,
    entity_type: str,
    distributed: bool = True,
    entity_name: Optional[str] = None,
    entity_abn: Optional[str] = None,
):
    """Print detailed tax breakdown for given income and entity type."""

    # Calculate tax based on entity type
    if entity_type == "individual":
        result = calculate_individual_tax(income)
    elif entity_type == "company":
        result = calculate_company_tax(income)
    elif entity_type == "trust":
        result = calculate_trust_tax(income, distributed)
    else:
        print(f"❌ Error: Unknown entity type '{entity_type}'")
        sys.exit(1)

    # Print header
    print_separator("═")
    print(f"TAX CALCULATION - FY2025-26")
    print_separator("═")
    print()

    # Entity info
    if entity_name:
        print(f"Entity Name: {entity_name}")
    if entity_abn:
        print(f"ABN: {entity_abn}")
    print(f"Entity Type: {entity_type.upper()}")
    if entity_type == "trust":
        status = "Distributed" if distributed else "Undistributed"
        print(f"Trust Status: {status}")
    print(f"Taxable Income: {format_currency(income)}")
    print()

    # Tax breakdown
    print_separator()
    print("TAX BREAKDOWN")
    print_separator()

    if entity_type == "individual":
        print(f"Base Tax:        {format_currency(result['base_tax']):>12s}")
        print(f"Medicare Levy:   {format_currency(result['medicare_levy']):>12s}")
        print(f"LITO Offset:    -{format_currency(result['lito']):>12s}")
        print_separator()
        print(f"Total Tax:       {format_currency(result['total_tax']):>12s}")
    else:
        print(f"Total Tax:       {format_currency(result['total_tax']):>12s}")

    print()
    print(f"Effective Rate:  {result['effective_rate']:.2f}%")

    # After-tax income
    after_tax = income - result['total_tax']
    print(f"After-Tax Income: {format_currency(after_tax)}")

    # Note if present
    if "note" in result:
        print()
        print(f"📋 {result['note']}")

    print()

    # Marginal rate guidance (for individuals)
    if entity_type == "individual":
        print_separator()
        print("MARGINAL RATE GUIDANCE")
        print_separator()

        if income <= 18200:
            print("  🟢 Tax-free threshold (0%)")
            print(f"  Remaining capacity: {format_currency(18200 - income)}")
        elif income <= 45000:
            print("  🟢 19% bracket")
            print(f"  Remaining capacity: {format_currency(45000 - income)}")
            print("  Next dollar taxed at: 32.5%")
        elif income <= 135000:
            print("  🟡 32.5% bracket")
            print(f"  Remaining capacity: {format_currency(135000 - income)}")
            print("  Next dollar taxed at: 37%")
        elif income <= 190000:
            print("  🟠 37% bracket")
            print(f"  Remaining capacity: {format_currency(190000 - income)}")
            print("  Next dollar taxed at: 45%")
        else:
            print("  🔴 45% bracket (top rate)")

        print()

    # Harry-specific insights
    if entity_type == "individual" and 30000 <= income <= 50000:
        print_separator()
        print("💡 HARRY'S TAX STRATEGY")
        print_separator()
        print("  • Target: Stay below $45K (19% bracket)")
        print(f"  • Current income: {format_currency(income)}")

        if income < 45000:
            remaining = 45000 - income
            print(f"  • Can earn {format_currency(remaining)} more at 19%")
        else:
            excess = income - 45000
            extra_tax = excess * 0.325
            if_lower = excess * 0.19
            penalty = extra_tax - if_lower
            print(f"  • Over threshold by {format_currency(excess)}")
            print(f"  • Paying extra {format_currency(penalty)} vs 19% bracket")

        print()

    print_separator()


def compare_scenarios(scenarios: list):
    """Compare multiple income scenarios side by side."""
    print_separator("═")
    print("INCOME SCENARIO COMPARISON")
    print_separator("═")
    print()

    print(f"{'Income':>15s}  {'Total Tax':>12s}  {'After Tax':>12s}  {'Effective Rate':>15s}")
    print_separator()

    for income in scenarios:
        result = calculate_individual_tax(income)
        after_tax = income - result['total_tax']
        print(
            f"{format_currency(income):>15s}  "
            f"{format_currency(result['total_tax']):>12s}  "
            f"{format_currency(after_tax):>12s}  "
            f"{result['effective_rate']:>14.2f}%"
        )

    print_separator()
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Australian tax for FY2025-26 with Supabase integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  SUPABASE_URL    Supabase project URL (default: gshsshaodoyttdxippwx.supabase.co)
  SUPABASE_KEY    Supabase service role key (required for entity queries)

Examples:
  # Query entity income from Supabase
  python calculate_tax_bracket.py --entity "Harrison Robert Sayers"
  python calculate_tax_bracket.py --abn "38 690 628 212"

  # Query entity and override entity type
  python calculate_tax_bracket.py --entity "MOK HOUSE" --entity-type company

  # Manual income input (original functionality)
  python calculate_tax_bracket.py --income 45000
  python calculate_tax_bracket.py --income 100000 --entity-type company
  python calculate_tax_bracket.py --income 50000 --entity-type trust

  # Compare scenarios
  python calculate_tax_bracket.py --compare 35000,45000,50000,60000
        """,
    )

    parser.add_argument(
        "--entity",
        type=str,
        help="Entity name to query income from Supabase (e.g., 'Harrison Robert Sayers', 'MOK HOUSE')",
    )

    parser.add_argument(
        "--abn",
        type=str,
        help="Entity ABN to query income from Supabase (e.g., '38 690 628 212')",
    )

    parser.add_argument(
        "--income",
        type=float,
        help="Manual taxable income amount (bypasses Supabase query)",
    )

    parser.add_argument(
        "--entity-type",
        type=str,
        default="individual",
        choices=["individual", "company", "trust"],
        help="Entity type (default: individual, or auto-detected from Supabase)",
    )

    parser.add_argument(
        "--trust-undistributed",
        action="store_true",
        help="For trusts: calculate as undistributed income (45%% penalty)",
    )

    parser.add_argument(
        "--compare",
        type=str,
        help="Compare multiple income scenarios (comma-separated)",
    )

    args = parser.parse_args()

    # Validate arguments
    if args.compare:
        # Comparison mode
        try:
            scenarios = [float(x.strip()) for x in args.compare.split(",")]
            compare_scenarios(scenarios)
        except ValueError:
            parser.error("--compare must be comma-separated numbers (e.g., 35000,45000,60000)")
    elif args.entity or args.abn:
        # Supabase query mode
        supabase = get_supabase_client()

        # Fetch entity
        if args.abn:
            entity = get_entity_by_abn(supabase, args.abn)
            if not entity:
                print(f"❌ No entity found with ABN: {args.abn}")
                sys.exit(1)
        elif args.entity:
            entity = get_entity_by_name(supabase, args.entity)
            if not entity:
                print(f"❌ No entity found matching: {args.entity}")
                sys.exit(1)

        # Calculate income
        income_data = calculate_entity_income_from_db(supabase, entity["id"])
        income = income_data["total_income"]

        if income == 0:
            print(f"⚠️  Warning: No income found for {entity['name']} in rolling 12 months")
            print("    You may want to use --income flag for manual input")
            sys.exit(1)

        # Determine entity type (use CLI override or database value)
        entity_type = args.entity_type
        if "entity_type" in entity and not args.entity_type:
            entity_type = entity["entity_type"]

        # Print breakdown
        distributed = not args.trust_undistributed
        print_tax_breakdown(
            income,
            entity_type,
            distributed,
            entity_name=entity["name"],
            entity_abn=entity.get("abn")
        )

    elif args.income is not None:
        # Manual calculation mode (original functionality)
        distributed = not args.trust_undistributed
        print_tax_breakdown(args.income, args.entity_type, distributed)
    else:
        parser.error("Must provide either --entity, --abn, --income, or --compare")


if __name__ == "__main__":
    main()
