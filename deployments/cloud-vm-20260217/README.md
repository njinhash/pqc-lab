# Cloud VM Deployment - February 17, 2026

## 📋 Overview
This folder contains everything needed to deploy a hybrid post-quantum TLS server to a cloud VM using certificates signed with ML-DSA-87 (FIPS 204).

## 🎯 Purpose
Deploy a hybrid PQC web server to `njinhash.cloud-ip.cc` that combines:
- **RSA 2048-bit key** (for browser compatibility)
- **ML-DSA-87 signature** (post-quantum security)

## 📁 Files

### Certificates (`/certificates`)
| File | Purpose |
|------|---------|
| `cloudvm-chain.crt` | Full certificate chain (server cert + intermediate CA) |
| `cloudvm-hybrid.crt` | Server certificate (RSA key + ML-DSA-87 signature) |
| `cloudvm-rsa.csr` | Certificate Signing Request (reference only) |
| `cloudvm-rsa.key` | RSA private key **(DO NOT COMMIT TO GITHUB)** |

## 🚀 Deployment Steps

1. Copy certificates to cloud VM
2. Ensure OpenSSL with OQS provider is installed
3. Start server:
   ```bash
   openssl s_server -cert certificates/cloudvm-chain.crt -key certificates/cloudvm-rsa.key -www -accept 4443