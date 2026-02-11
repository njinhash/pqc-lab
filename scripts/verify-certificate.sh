#!/bin/bash
echo "🔐 PQC Certificate Verification Script"
echo "======================================"

# Check if OpenSSL is available
if ! command -v openssl &> /dev/null; then
    echo "❌ Error: OpenSSL not found!"
    exit 1
fi

echo "✅ OpenSSL version: $(openssl version)"

# Find certificate chain
CHAIN_FILE="/home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt"

if [ -f "$CHAIN_FILE" ]; then
    echo "📁 Found certificate chain: $CHAIN_FILE"
    
    # Show chain contents
    echo "📋 Certificate chain contains:"
    openssl crl2pkcs7 -nocrl -certfile "$CHAIN_FILE" 2>/dev/null | \
        openssl pkcs7 -print_certs -text -noout 2>/dev/null | \
        grep "Subject:" | sed 's/Subject: //'
else
    echo "⚠️  Certificate chain not found at: $CHAIN_FILE"
    echo "   Run Module 3 first to create the Intermediate CA"
fi

echo ""
echo "📊 To verify a specific certificate:"
echo "   openssl verify -CAfile \"$CHAIN_FILE\" your-certificate.crt"
