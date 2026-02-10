#!/bin/bash
echo "=== FINAL STRUCTURE VALIDATION ==="
echo ""
echo "Checking from: $(pwd)"
echo ""

ERRORS=0
WARNINGS=0

# Check 1: No stray root directory
if [ -d "root" ]; then
    echo "❌ ERROR: Stray 'root' directory at top level"
    ((ERRORS++))
fi

if [ -d "fipsqs/root" ]; then
    echo "❌ ERROR: Stray 'root' directory in fipsqs/"
    ((ERRORS++))
fi

# Check 2: Module 02 exists and has correct structure
if [ ! -d "fipsqs/02_fips_quantum_ca_root" ]; then
    echo "❌ ERROR: Module 02 directory missing"
    ((ERRORS++))
else
    echo "✅ Module 02 directory exists"
    
    # Check essential files
    ESSENTIAL_FILES=(
        "fipsqs/02_fips_quantum_ca_root/root/private/root_ca.key"
        "fipsqs/02_fips_quantum_ca_root/root/certs/root_ca.crt"
        "fipsqs/02_fips_quantum_ca_root/root/openssl.cnf"
        "fipsqs/02_fips_quantum_ca_root/root/index.txt"
        "fipsqs/02_fips_quantum_ca_root/root/serial"
    )
    
    for file in "${ESSENTIAL_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $(basename $file) exists"
        else
            echo "❌ ERROR: $(basename $file) missing"
            ((ERRORS++))
        fi
    done
    
    # Check directories
    ESSENTIAL_DIRS=(
        "fipsqs/02_fips_quantum_ca_root/root/certs"
        "fipsqs/02_fips_quantum_ca_root/root/private"
        "fipsqs/02_fips_quantum_ca_root/root/crl"
        "fipsqs/02_fips_quantum_ca_root/root/newcerts"
    )
    
    for dir in "${ESSENTIAL_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            echo "✅ $(basename $dir)/ directory exists"
        else
            echo "❌ ERROR: $(basename $dir)/ directory missing"
            ((ERRORS++))
        fi
    done
fi

# Check 3: No duplicate files in wrong places
echo ""
echo "=== Checking for duplicate/misplaced files ==="

DUPLICATE_FILES=$(find . -type f \( -name "root_ca.key" -o -name "root_ca.crt" -o -name "openssl.cnf" \) 2>/dev/null | grep -v ".git" | grep -v "02_fips_quantum_ca_root")
if [ -n "$DUPLICATE_FILES" ]; then
    echo "⚠️  WARNING: Found duplicate files:"
    echo "$DUPLICATE_FILES"
    ((WARNINGS++))
else
    echo "✅ No duplicate key/cert/config files found"
fi

# Check 4: Module 03 (optional)
if [ -d "fipsqs/03_fips_quantum_ca_intermediate" ]; then
    echo ""
    echo "=== Module 03 directory exists ==="
    echo "✅ Module 03 directory present"
    # Don't check contents as it might be in progress
fi

# Final summary
echo ""
echo "=== VALIDATION SUMMARY ==="
if [ $ERRORS -eq 0 ]; then
    echo "✅ SUCCESS: All files and folders are in the proper place!"
    if [ $WARNINGS -gt 0 ]; then
        echo "⚠️  Note: $WARNINGS warning(s) found (non-critical)"
    fi
else
    echo "❌ FAILURE: Found $ERRORS error(s) that need to be fixed"
    exit 1
fi
