#!/bin/bash
echo "=== FINAL MODULE 2 VERIFICATION ==="
echo ""

ERRORS=0
PASSED=0

# Function to check and count
check() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
        ((PASSED++))
    else
        echo "❌ $1"
        ((ERRORS++))
    fi
}

echo "1. Checking essential files..."
[ -f "root/private/root_ca.key" ] && check "Private key exists"
[ -f "root/certs/root_ca.crt" ] && check "Certificate exists"
[ -f "root/openssl.cnf" ] && check "Config file exists"
[ -f "root/index.txt" ] && check "Index file exists"
[ -f "root/serial" ] && check "Serial file exists"

echo -e "\n2. Checking certificate functionality..."
openssl verify -CAfile root/certs/root_ca.crt root/certs/root_ca.crt >/dev/null 2>&1
check "Certificate self-verifies OK"

openssl x509 -in root/certs/root_ca.crt -text -noout 2>/dev/null | grep -q "ML-DSA-87"
check "Certificate uses ML-DSA-87 algorithm"

openssl x509 -in root/certs/root_ca.crt -text -noout 2>/dev/null | grep -q "CA:TRUE"
check "Certificate is a CA (CA:TRUE)"

echo -e "\n3. Checking key permissions..."
PERM=$(stat -c "%a" root/private/root_ca.key 2>/dev/null)
if [ "$PERM" = "600" ]; then
    echo "✅ Private key has secure permissions (600)"
    ((PASSED++))
else
    echo "❌ Private key has insecure permissions: $PERM"
    ((ERRORS++))
fi

echo -e "\n4. Checking for stray files..."
cd /home/labuser/work/openssl-pqc-stepbystep-lab
STRAY_COUNT=$(find . -type f \( -name "*.key" -o -name "*.crt" -o -name "openssl.cnf" \) 2>/dev/null | grep -v ".git" | grep -v "02_fips_quantum_ca_root" | wc -l)
if [ $STRAY_COUNT -eq 0 ]; then
    echo "✅ No stray files found"
    ((PASSED++))
else
    echo "❌ Found $STRAY_COUNT stray file(s)"
    ((ERRORS++))
fi

echo -e "\n=== SUMMARY ==="
echo "Passed: $PASSED checks"
echo "Errors: $ERRORS checks"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "🎉 MODULE 2 IS READY FOR MODULE 3!"
    echo ""
    echo "Next steps:"
    echo "1. Create Module 03 directory"
    echo "2. Generate Intermediate CA key"
    echo "3. Configure Intermediate CA"
else
    echo "⚠️  Found $ERRORS issue(s) that need fixing before Module 3"
    exit 1
fi
