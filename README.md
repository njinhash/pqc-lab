# Post-Quantum Cryptography Lab

## Overview
A hands-on implementation of quantum-resistant Public Key Infrastructure (PKI) using ML-DSA-87 (NIST FIPS 203/204 standard). This project demonstrates practical post-quantum cryptography through certificate authority creation and management.

## 🚀 Features
- ✅ **Root Certificate Authority** with ML-DSA-87 (10-year validity)
- ✅ **Intermediate CA** with 5-year validity and pathlen:0 restriction
- ✅ **End-entity certificate** issuance for web servers
- ✅ **Complete certificate chain** validation
- ✅ **Dockerized environment** for reproducible experiments
- ✅ **Quantum-resistant algorithms** throughout the PKI hierarchy

## 🛠️ Technology Stack
- **OpenSSL 3.5.3** with native PQC algorithm support
- **ML-DSA-87** (Module-Lattice Digital Signature Algorithm, FIPS 204)
- **Docker** with Ubuntu 25.10 container
- **GitHub** for documentation and version control

## 📁 Project Structure
```
pqc-lab/
├── My-Lab-Journal.md          # Complete lab documentation
├── README.md                  # This file
├── .gitignore                 # Security: prevents pushing secrets
└── [Future: scripts/, docs/, samples/]

## 📖 Documentation
The complete step-by-step learning journey is documented in [My-Lab-Journal.md](My-Lab-Journal.md), covering:
- Docker environment setup
- Root CA creation with ML-DSA-87
- Intermediate CA establishment
- End-entity certificate issuance
- Verification and testing procedures

## 🔒 Security Considerations
- Private keys (`.key` files) are **never** stored in this repository
- Sensitive files are excluded via `.gitignore`
- This repository contains documentation and templates only
- All cryptographic operations use quantum-resistant ML-DSA-87 algorithm

## 🎯 Learning Outcomes
- Understanding post-quantum cryptography fundamentals
- Practical PKI implementation with quantum-resistant algorithms
- Certificate authority hierarchy management
- Docker containerization for crypto experiments
- Security best practices for cryptographic key management

## 📈 Next Steps
- User authentication certificates
- Code signing certificates
- Certificate revocation lists (CRL)
- Hybrid certificate strategies
- Performance analysis of PQC algorithms

## 🤝 Contributing
This is a personal learning project. For educational purposes only.

## 📄 License
Educational use - refer to individual module licenses for lab materials.

## 🔗 Related Resources
- [NIST FIPS 203/204 Standards](https://csrc.nist.gov/pubs/fips/203/final)
- [OpenSSL PQC Support](https://www.openssl.org/docs/man3.0/man7/pqc.html)
- [F5 PQC Lab Guide](https://github.com/f5devcentral/openssl-pqc-stepbystep-lab)
