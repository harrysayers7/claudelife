#!/usr/bin/env python3
"""
Test script to debug Supabase connection issues
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
supabase_url = os.getenv("SUPABASE_URL", "https://gshsshaodoyttdxippwx.supabase.co")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

print(f"Testing Supabase connection:")
print(f"URL: {supabase_url}")
print(f"Key length: {len(supabase_key)}")

try:
    # Create Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)
    print("✓ Supabase client created successfully")

    # Test 1: Simple select
    print("\nTest 1: Simple select from entities table")
    result = supabase.table("entities").select("*").execute()
    print(f"Result: {result.data}")
    print(f"Count: {result.count}")

    # Test 2: Count query
    print("\nTest 2: Count query")
    count_result = supabase.table("entities").select("*", count="exact").execute()
    print(f"Count result: {count_result.count}")

    # Test 3: Just check if table exists
    print("\nTest 3: Minimal query")
    minimal = supabase.table("entities").select("id").limit(1).execute()
    print(f"Minimal result: {minimal.data}")

except Exception as e:
    print(f"✗ Error: {e}")
    print(f"Error type: {type(e)}")

    # Try to get more details
    try:
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
    except:
        pass
