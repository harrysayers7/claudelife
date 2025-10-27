#!/bin/bash
# Test Python scripts in legacy mode (USE_NEW_SCHEMAS=false)

# Set environment variables
export SUPABASE_KEY="$SUPABASE_SERVICE_ROLE_KEY"
export SUPABASE_URL="https://gshsshaodoyttdxippwx.supabase.co"
export SUPABASE_USE_NEW_SCHEMAS="false"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/../venv/bin/python"

echo "🧪 Testing Python scripts in LEGACY MODE (USE_NEW_SCHEMAS=false)"
echo "================================================================"
echo ""

# Test 1: validate_gst_threshold.py
echo "📊 Test 1: validate_gst_threshold.py --all"
echo "-------------------------------------------"
"$VENV_PYTHON" "$SCRIPT_DIR/validate_gst_threshold.py" --all
TEST1_STATUS=$?
echo ""

# Test 2: optimize_trust_distribution.py
echo "💰 Test 2: optimize_trust_distribution.py --trust-entity 'HS Family Trust'"
echo "----------------------------------------------------------------------------"
"$VENV_PYTHON" "$SCRIPT_DIR/optimize_trust_distribution.py" --trust-entity "HS Family Trust"
TEST2_STATUS=$?
echo ""

# Test 3: calculate_tax_bracket.py
echo "🧮 Test 3: calculate_tax_bracket.py --entity 'MOK HOUSE PTY LTD'"
echo "-------------------------------------------------------------------"
"$VENV_PYTHON" "$SCRIPT_DIR/calculate_tax_bracket.py" --entity "MOK HOUSE PTY LTD"
TEST3_STATUS=$?
echo ""

# Summary
echo "================================================================"
echo "📋 LEGACY MODE TEST SUMMARY"
echo "================================================================"
echo "Test 1 (GST Threshold):       $([ $TEST1_STATUS -eq 0 ] && echo '✅ PASSED' || echo '❌ FAILED')"
echo "Test 2 (Trust Distribution):  $([ $TEST2_STATUS -eq 0 ] && echo '✅ PASSED' || echo '❌ FAILED')"
echo "Test 3 (Tax Bracket):         $([ $TEST3_STATUS -eq 0 ] && echo '✅ PASSED' || echo '❌ FAILED')"
echo ""

# Exit with failure if any test failed
if [ $TEST1_STATUS -ne 0 ] || [ $TEST2_STATUS -ne 0 ] || [ $TEST3_STATUS -ne 0 ]; then
    echo "❌ Some tests failed - scripts may not be working with migrated database"
    exit 1
else
    echo "✅ All tests passed - scripts work unchanged in legacy mode!"
    exit 0
fi
