#!/usr/bin/env python3
"""
Trust Distribution Optimizer for FY2025-26 - Supabase Integration

Calculates optimal trust income distributions to minimize household tax burden.
Models multiple scenarios and compares effective tax rates including franking credits.
Integrates with Supabase database for real trust entity data and beneficiary information.

Usage:
    # Query trust income from Supabase
    python optimize_trust_distribution.py --trust-entity "HS Family Trust"

    # Manual trust income with Supabase beneficiaries
    python optimize_trust_distribution.py --trust-income 50000

    # Query by ABN
    python optimize_trust_distribution.py --trust-abn "12 345 678 901"

    # With franked dividends
    python optimize_trust_distribution.py --trust-entity "HS Family Trust" --franked 30000

    # Save distribution to database
    python optimize_trust_distribution.py --trust-entity "HS Family Trust" --save-distribution

    # Custom beneficiaries (override database)
    python optimize_trust_distribution.py --trust-income 50000 --custom-beneficiary "Sister,35000,0.19"

Requires:
    - SUPABASE_URL environment variable
    - SUPABASE_KEY environment variable (service role key)
    - pip install supabase (install with: pip3 install supabase)
"""

import argparse
import sys
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
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
TAX_BRACKETS = [
    (18200, 0.0),
    (45000, 0.19),
    (135000, 0.325),
    (190000, 0.37),
    (float('inf'), 0.45),
]

MEDICARE_LEVY_RATE = 0.02
COMPANY_TAX_RATE = 0.25  # For franking credit calculations
TRUST_PENALTY_RATE = 0.45  # Undistributed income tax
MINOR_PENALTY_RATE = 0.66  # Under 18 years old


@dataclass
class Beneficiary:
    """Represents a potential trust beneficiary."""
    name: str
    current_income: float  # Income from other sources
    marginal_rate: float  # Current marginal tax rate (0-45%)
    relationship: str  # family/friend/charity
    minor: bool = False  # Under 18 years old


def get_supabase_client() -> Client:
    """Initialize Supabase client."""
    if not SUPABASE_KEY:
        print("❌ Error: SUPABASE_KEY environment variable not set")
        print("\nSet it with:")
        print("  export SUPABASE_KEY='your-service-role-key'")
        sys.exit(1)

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_trust_entity_by_name(supabase: Client, name: str) -> Optional[Dict]:
    """Fetch trust entity from Supabase by name."""
    try:
        response = supabase.table("entities").select("*").ilike("name", f"%{name}%").execute()

        if not response.data:
            return None

        if len(response.data) > 1:
            print(f"⚠️  Multiple entities found matching '{name}':")
            for entity in response.data:
                print(f"   - {entity['name']} (ABN: {entity.get('abn', 'N/A')})")
            print("\nPlease specify ABN with --trust-abn flag")
            sys.exit(1)

        return response.data[0]
    except Exception as e:
        print(f"❌ Error fetching entity: {e}")
        sys.exit(1)


def get_trust_entity_by_abn(supabase: Client, abn: str) -> Optional[Dict]:
    """Fetch trust entity from Supabase by ABN."""
    try:
        response = supabase.table("entities").select("*").eq("abn", abn).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"❌ Error fetching entity: {e}")
        sys.exit(1)


def calculate_trust_income_from_db(supabase: Client, entity_id: str) -> Dict[str, float]:
    """
    Calculate rolling 12-month trust income from Supabase transactions and invoices.

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

    # Total income (use max to avoid double-counting)
    total_income = max(transaction_income, invoice_income)

    return {
        "transaction_income": transaction_income,
        "invoice_income": invoice_income,
        "total_income": total_income,
    }


def get_beneficiaries_from_db(supabase: Client) -> List[Beneficiary]:
    """
    Fetch beneficiary data from Supabase entities table.
    Returns individuals who are potential trust beneficiaries.
    """
    try:
        # Get individual entities (potential beneficiaries)
        response = supabase.table("entities")\
            .select("*")\
            .eq("entity_type", "individual")\
            .execute()

        beneficiaries = []
        for entity in response.data:
            # Calculate current income from transactions (simple estimate)
            income_data = calculate_trust_income_from_db(supabase, entity["id"])
            current_income = income_data["total_income"]

            # Calculate marginal rate based on income
            marginal_rate = calculate_marginal_rate(current_income)

            beneficiaries.append(Beneficiary(
                name=entity["name"],
                current_income=current_income,
                marginal_rate=marginal_rate,
                relationship=entity.get("relationship", "family"),
                minor=entity.get("is_minor", False)
            ))

        return beneficiaries
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch beneficiaries from database: {e}")
        print("    Falling back to default beneficiaries")
        return []


def save_distribution_to_db(
    supabase: Client,
    trust_entity_id: str,
    result: Dict
):
    """Save optimal distribution results to trust_distributions table."""
    current_fy = f"FY{datetime.now().year % 100:02d}"

    # Find recommended scenario
    recommended_scenario = next(
        s for s in result["scenarios"]
        if s["name"] == result["recommended"]
    )

    # Save each allocation
    for alloc in recommended_scenario["allocations"]:
        if alloc["beneficiary"] == "Trust Entity":
            continue  # Skip undistributed scenario

        data = {
            "trust_entity_id": trust_entity_id,
            "financial_year": current_fy,
            "beneficiary_name": alloc["beneficiary"],
            "distribution_amount": alloc["distribution"],
            "franked_amount": alloc.get("franked", 0),
            "tax_payable": alloc["tax"],
            "effective_rate": alloc["effective_rate"],
            "strategy": result["recommended"],
            "created_at": datetime.now().isoformat(),
        }

        try:
            supabase.table("trust_distributions").insert(data).execute()
        except Exception as e:
            print(f"⚠️  Warning: Could not save distribution for {alloc['beneficiary']}: {e}")

    print(f"✅ Saved distribution plan to database")


def calculate_tax_on_income(income: float, include_medicare: bool = True) -> float:
    """Calculate individual tax on given income."""
    base_tax = 0.0
    remaining_income = income
    previous_threshold = 0

    for threshold, rate in TAX_BRACKETS:
        if remaining_income <= 0:
            break
        taxable_in_bracket = min(remaining_income, threshold - previous_threshold)
        base_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
        previous_threshold = threshold

    medicare_levy = income * MEDICARE_LEVY_RATE if include_medicare and income >= 26000 else 0.0

    # LITO calculation
    if income <= 37500:
        lito = 700
    elif income <= 51500:
        lito = max(0, 700 - ((income - 37500) * 0.05))
    else:
        lito = 0.0

    total_tax = max(0, base_tax + medicare_levy - lito)
    return total_tax


def calculate_marginal_rate(income: float) -> float:
    """Determine marginal tax rate for given income level."""
    for threshold, rate in TAX_BRACKETS:
        if income <= threshold:
            return rate
    return TAX_BRACKETS[-1][1]


def calculate_franking_benefit(
    distribution: float,
    franked_amount: float,
    recipient_income: float
) -> Dict[str, float]:
    """
    Calculate tax benefit from franked dividends.

    Args:
        distribution: Cash distribution amount
        franked_amount: Portion that is franked
        recipient_income: Beneficiary's other income

    Returns:
        Dict with gross_up, tax_payable, franking_credit, net_benefit
    """
    # Gross up franked portion (add back company tax paid)
    franking_credit = franked_amount * (COMPANY_TAX_RATE / (1 - COMPANY_TAX_RATE))
    gross_distribution = distribution + franking_credit

    # Calculate tax on total income including grossed-up dividend
    total_income = recipient_income + gross_distribution
    tax_on_total = calculate_tax_on_income(total_income)
    tax_without_dividend = calculate_tax_on_income(recipient_income)
    tax_on_dividend = tax_on_total - tax_without_dividend

    # Net tax after franking credit refund
    net_tax = max(0, tax_on_dividend - franking_credit)

    # Effective tax rate on cash received
    effective_rate = (net_tax / distribution * 100) if distribution > 0 else 0

    return {
        "franking_credit": franking_credit,
        "gross_distribution": gross_distribution,
        "tax_on_dividend": tax_on_dividend,
        "net_tax": net_tax,
        "effective_rate": effective_rate,
        "after_tax_cash": distribution - net_tax,
    }


def optimize_distribution(
    trust_income: float,
    beneficiaries: List[Beneficiary],
    franked_amount: float = 0.0
) -> Dict:
    """
    Find optimal distribution strategy to minimize total household tax.

    Returns:
        Dict with optimal allocation and tax comparison
    """
    scenarios = []

    # Scenario 1: Distribute to lowest marginal rate beneficiaries
    sorted_beneficiaries = sorted(beneficiaries, key=lambda b: b.marginal_rate)
    scenario_1 = {
        "name": "Lowest Marginal Rate Priority",
        "allocations": [],
        "total_household_tax": 0.0,
    }

    remaining = trust_income
    for ben in sorted_beneficiaries:
        if remaining <= 0:
            break

        # Calculate how much to allocate to this beneficiary
        allocation = remaining  # Start with all remaining

        # Determine portion that is franked
        franked_portion = min(allocation, franked_amount) if franked_amount > 0 else 0

        # Calculate tax impact
        if ben.minor:
            # Minor beneficiary - 66% penalty rate
            tax = allocation * MINOR_PENALTY_RATE
            after_tax = allocation - tax
            effective_rate = MINOR_PENALTY_RATE * 100
        elif franked_portion > 0:
            # Franked dividend calculation
            result = calculate_franking_benefit(allocation, franked_portion, ben.current_income)
            tax = result["net_tax"]
            after_tax = result["after_tax_cash"]
            effective_rate = result["effective_rate"]
        else:
            # Unfranked income
            total_income = ben.current_income + allocation
            tax_with = calculate_tax_on_income(total_income)
            tax_without = calculate_tax_on_income(ben.current_income)
            tax = tax_with - tax_without
            after_tax = allocation - tax
            effective_rate = (tax / allocation * 100) if allocation > 0 else 0

        scenario_1["allocations"].append({
            "beneficiary": ben.name,
            "current_income": ben.current_income,
            "marginal_rate": ben.marginal_rate * 100,
            "distribution": allocation,
            "franked": franked_portion,
            "tax": tax,
            "after_tax": after_tax,
            "effective_rate": effective_rate,
        })

        scenario_1["total_household_tax"] += tax
        remaining = 0  # All allocated in this simple scenario

    # Scenario 2: Even split
    scenario_2 = {
        "name": "Even Split Among All Beneficiaries",
        "allocations": [],
        "total_household_tax": 0.0,
    }

    per_person = trust_income / len(beneficiaries)
    for ben in beneficiaries:
        franked_portion = (per_person / trust_income * franked_amount) if franked_amount > 0 else 0

        if ben.minor:
            tax = per_person * MINOR_PENALTY_RATE
            after_tax = per_person - tax
            effective_rate = MINOR_PENALTY_RATE * 100
        elif franked_portion > 0:
            result = calculate_franking_benefit(per_person, franked_portion, ben.current_income)
            tax = result["net_tax"]
            after_tax = result["after_tax_cash"]
            effective_rate = result["effective_rate"]
        else:
            total_income = ben.current_income + per_person
            tax_with = calculate_tax_on_income(total_income)
            tax_without = calculate_tax_on_income(ben.current_income)
            tax = tax_with - tax_without
            after_tax = per_person - tax
            effective_rate = (tax / per_person * 100)

        scenario_2["allocations"].append({
            "beneficiary": ben.name,
            "current_income": ben.current_income,
            "marginal_rate": ben.marginal_rate * 100,
            "distribution": per_person,
            "franked": franked_portion,
            "tax": tax,
            "after_tax": after_tax,
            "effective_rate": effective_rate,
        })

        scenario_2["total_household_tax"] += tax

    # Scenario 3: Keep in trust (worst case)
    scenario_3 = {
        "name": "Undistributed (Penalty Rate)",
        "allocations": [{
            "beneficiary": "Trust Entity",
            "current_income": 0,
            "marginal_rate": TRUST_PENALTY_RATE * 100,
            "distribution": trust_income,
            "franked": 0,
            "tax": trust_income * TRUST_PENALTY_RATE,
            "after_tax": trust_income * (1 - TRUST_PENALTY_RATE),
            "effective_rate": TRUST_PENALTY_RATE * 100,
        }],
        "total_household_tax": trust_income * TRUST_PENALTY_RATE,
    }

    scenarios = [scenario_1, scenario_2, scenario_3]

    # Find best scenario (lowest total tax)
    best_scenario = min(scenarios, key=lambda s: s["total_household_tax"])

    return {
        "trust_income": trust_income,
        "franked_amount": franked_amount,
        "scenarios": scenarios,
        "recommended": best_scenario["name"],
        "tax_saved": scenario_3["total_household_tax"] - best_scenario["total_household_tax"],
    }


def format_currency(amount: float) -> str:
    """Format as Australian currency."""
    return f"${amount:,.2f}"


def print_separator(char: str = "─", length: int = 80):
    """Print separator line."""
    print(char * length)


def print_optimization_report(result: Dict, trust_entity: Optional[Dict] = None):
    """Print detailed optimization report."""
    print_separator("═")
    print("TRUST DISTRIBUTION OPTIMIZATION REPORT - FY2025-26")
    print_separator("═")
    print()

    # Trust entity info (if from database)
    if trust_entity:
        print(f"Trust Entity:        {trust_entity['name']}")
        if trust_entity.get('abn'):
            print(f"ABN:                 {trust_entity['abn']}")
        print()

    # Trust details
    print(f"Trust Net Income:    {format_currency(result['trust_income'])}")
    if result['franked_amount'] > 0:
        print(f"Franked Amount:      {format_currency(result['franked_amount'])}")
        franking_pct = (result['franked_amount'] / result['trust_income'] * 100)
        print(f"Franking %:          {franking_pct:.1f}%")
    print()

    # Compare scenarios
    for i, scenario in enumerate(result['scenarios'], 1):
        is_recommended = scenario['name'] == result['recommended']
        marker = "✅ RECOMMENDED" if is_recommended else ""

        print_separator()
        print(f"SCENARIO {i}: {scenario['name']} {marker}")
        print_separator()
        print()

        # Table header
        print(f"{'Beneficiary':<20s} {'Current':<12s} {'Distribution':<12s} {'Tax':<12s} {'After-Tax':<12s} {'Rate':<8s}")
        print(f"{'':20s} {'Income':12s} {'':12s} {'':12s} {'':12s} {'':8s}")
        print_separator("-")

        for alloc in scenario['allocations']:
            print(
                f"{alloc['beneficiary']:<20s} "
                f"{format_currency(alloc['current_income']):<12s} "
                f"{format_currency(alloc['distribution']):<12s} "
                f"{format_currency(alloc['tax']):<12s} "
                f"{format_currency(alloc['after_tax']):<12s} "
                f"{alloc['effective_rate']:.1f}%"
            )

            # Show franking benefit if applicable
            if alloc.get('franked', 0) > 0:
                print(f"  └─ Franked: {format_currency(alloc['franked'])} (franking credits reduce tax)")

        print_separator("-")
        print(f"{'TOTAL HOUSEHOLD TAX:':<20s} {' ':<12s} {' ':<12s} {format_currency(scenario['total_household_tax']):<12s}")
        print()

    # Summary
    print_separator("═")
    print("SUMMARY")
    print_separator("═")
    print()
    print(f"✅ Recommended Strategy: {result['recommended']}")
    print(f"💰 Total Tax Saved vs Undistributed: {format_currency(result['tax_saved'])}")
    print()

    # Implementation notes
    print_separator()
    print("📋 IMPLEMENTATION NOTES")
    print_separator()
    print()
    print("1. Trustee Resolution Required:")
    print("   • Must be executed before 30 June FY2025-26")
    print("   • Document beneficiary entitlements")
    print("   • File with trust records")
    print()
    print("2. Distribution Payments:")
    print("   • Must be 'presently entitled' by 30 June")
    print("   • Payment can occur after year end")
    print("   • Consider trust distribution statement")
    print()
    print("3. Beneficiary Tax Returns:")
    print("   • Each beneficiary includes trust distribution")
    print("   • Attach trust distribution statement")
    print("   • Franking credits claimed by beneficiary")
    print()
    print("⚠️  Warning: Do NOT leave income undistributed (45% penalty rate)")
    print()
    print_separator()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Optimize trust income distributions for FY2025-26 with Supabase integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  SUPABASE_URL    Supabase project URL (default: gshsshaodoyttdxippwx.supabase.co)
  SUPABASE_KEY    Supabase service role key (required)

Examples:
  # Query trust income from Supabase
  python optimize_trust_distribution.py --trust-entity "HS Family Trust"

  # Query by ABN
  python optimize_trust_distribution.py --trust-abn "12 345 678 901"

  # Manual trust income (beneficiaries from database)
  python optimize_trust_distribution.py --trust-income 50000

  # With franked dividends
  python optimize_trust_distribution.py --trust-entity "HS Family Trust" --franked 30000

  # Save distribution to database
  python optimize_trust_distribution.py --trust-entity "HS Family Trust" --save-distribution

  # Custom beneficiary (override database)
  python optimize_trust_distribution.py --trust-income 50000 --custom-beneficiary "Sister,35000,0.19"
        """,
    )

    parser.add_argument(
        "--trust-entity",
        type=str,
        help="Trust entity name to query from Supabase",
    )

    parser.add_argument(
        "--trust-abn",
        type=str,
        help="Trust entity ABN to query from Supabase",
    )

    parser.add_argument(
        "--trust-income",
        type=float,
        help="Manual trust net income amount (if not querying from database)",
    )

    parser.add_argument(
        "--franked",
        type=float,
        default=0.0,
        help="Amount that is franked dividends (default: 0)",
    )

    parser.add_argument(
        "--custom-beneficiary",
        type=str,
        action='append',
        help="Add custom beneficiary: Name,CurrentIncome,MarginalRate (can be used multiple times)",
    )

    parser.add_argument(
        "--save-distribution",
        action="store_true",
        help="Save distribution plan to trust_distributions table in Supabase",
    )

    args = parser.parse_args()

    # Validate arguments
    if not any([args.trust_entity, args.trust_abn, args.trust_income]):
        parser.error("Must provide --trust-entity, --trust-abn, or --trust-income")

    # Initialize Supabase
    supabase = get_supabase_client()

    # Fetch trust entity and income
    trust_entity = None
    trust_income = args.trust_income

    if args.trust_entity or args.trust_abn:
        # Query trust entity from database
        if args.trust_abn:
            trust_entity = get_trust_entity_by_abn(supabase, args.trust_abn)
        else:
            trust_entity = get_trust_entity_by_name(supabase, args.trust_entity)

        if not trust_entity:
            print(f"❌ No trust entity found")
            sys.exit(1)

        # Calculate trust income from database
        income_data = calculate_trust_income_from_db(supabase, trust_entity["id"])
        trust_income = income_data["total_income"]

        if trust_income == 0:
            print(f"⚠️  Warning: No income found for {trust_entity['name']} in last 12 months")
            if not args.trust_income:
                print("     Use --trust-income to manually specify income")
                sys.exit(1)

    # Get beneficiaries
    beneficiary_list = []

    # Try to get beneficiaries from database
    if not args.custom_beneficiary:
        db_beneficiaries = get_beneficiaries_from_db(supabase)
        if db_beneficiaries:
            beneficiary_list = db_beneficiaries
            print(f"✅ Loaded {len(beneficiary_list)} beneficiaries from database")
        else:
            print("⚠️  No beneficiaries found in database")
            print("    Use --custom-beneficiary to add beneficiaries manually")
            sys.exit(1)

    # Add custom beneficiaries (override or supplement)
    if args.custom_beneficiary:
        beneficiary_list = []  # Clear database beneficiaries if custom ones provided
        for custom_ben in args.custom_beneficiary:
            try:
                parts = custom_ben.split(",")
                if len(parts) != 3:
                    parser.error("--custom-beneficiary must be: Name,CurrentIncome,MarginalRate")
                custom_name = parts[0].strip()
                custom_income = float(parts[1].strip())
                custom_rate = float(parts[2].strip())
                beneficiary_list.append(
                    Beneficiary(custom_name, custom_income, custom_rate, "custom")
                )
            except ValueError:
                parser.error(f"Invalid --custom-beneficiary format: {custom_ben}")

    if not beneficiary_list:
        parser.error("No valid beneficiaries provided")

    # Validate franked amount
    if args.franked > trust_income:
        parser.error("Franked amount cannot exceed trust income")

    # Run optimization
    result = optimize_distribution(trust_income, beneficiary_list, args.franked)

    # Print report
    print_optimization_report(result, trust_entity)

    # Save to database if requested
    if args.save_distribution and trust_entity:
        save_distribution_to_db(supabase, trust_entity["id"], result)


if __name__ == "__main__":
    main()
