`# My Post-Quantum Cryptography Lab Journey
Start Date: [02/09/2026]

## CHAPTER 1: SETUP PHASE
**Goal:** Prepare my computer for the PQC lab

### What I've Installed So Far:

1. **Docker Desktop**
 - What it is: A tool that lets me run Linux containers
 - Why I need it: The lab requires Ubuntu 25.10, and Docker lets me run it on my computer
 - Installation date: [02/09/2026]
 - Version: 4.59.0 (217644)
 - Docker Engine: 29.2.0
 - Platform: Windows with Linux containers (WSL2)
 - How I verified it works: Successfully built and ran first container

2. **VS Code**
 - What it is: A code editor
 - Why I need it: To write documentation and use the terminal
 - Installation date: [02/09/2026]

3. **Docker Extension for VS Code**
 - What it is: Adds Docker controls to VS Code
 - Why I need it: To manage containers without leaving VS Code
 - How I installed it: Via VS Code extensions marketplace

### Next Step:
I need to create a Docker container with Ubuntu 25.10 to begin the actual lab work.

---

## CHAPTER 2: FIRST CONTAINER CREATION
**Goal:** Build and run my first Docker container with Ubuntu 25.10 and OpenSSL

### Step-by-Step Process Completed:

#### Step 1-3: Project Setup
- Created project folder: `pqc-lab`
- Opened in VS Code
- Created `Dockerfile` in the project root

#### Step 4-5: Dockerfile Creation
**File:** `Dockerfile`
```dockerfile
# Simple PQC Lab Docker setup
FROM ubuntu:25.10

# Update and install OpenSSL
RUN apt-get update && \
 apt-get install -y openssl && \
 rm -rf /var/lib/apt/lists/*

# Create lab directory
WORKDIR /lab

# Show success message (JSON format)
CMD ["bash", "-c", "echo ' PQC Lab environment ready!' && echo 'OpenSSL version:' && openssl version && bash"]
```

**What this does:**
- Starts with Ubuntu 25.10 base image
- Installs OpenSSL (for cryptography experiments)
- Creates `/lab` working directory
- Shows success message when container starts
- Opens interactive bash shell

#### Step 6-7: Building the Image
**Command used:**
```bash
docker build -t pqc-simple .
```

**Result:** SUCCESS
- Image name: `pqc-simple:latest`
- Build time: ~2.3 seconds (cached layers after first build)
- Warning received: JSONArgsRecommended (resolved by using JSON format for CMD)

#### Step 8-9: Running the Container
**Command used:**
```bash
docker run -it --name my-pqc-lab pqc-simple
```

**Result:** Container running successfully
- Container name: `my-pqc-lab`
- Working directory: `/lab`
- Interactive bash session active

#### Step 10: Testing OpenSSL
**Commands tested inside container:**
```bash
openssl version # Check OpenSSL installation
openssl list -digest-algorithms # View available algorithms
```

**Result:** OpenSSL working correctly

### What I Learned:

1. **Docker Images vs Containers:**
 - Image = Blueprint (like a recipe)
 - Container = Running instance (like the actual meal)
 - One image can create many containers

2. **Dockerfile Basics:**
 - `FROM` = Base operating system
 - `RUN` = Commands to execute during build
 - `WORKDIR` = Set working directory
 - `CMD` = Command to run when container starts

3. **Docker Commands:**
 - `docker build` = Create an image from Dockerfile
 - `docker run` = Create and start a container from an image
 - `-it` flags = Interactive terminal
 - `--name` = Give container a custom name

4. **Container Isolation:**
 - Docker commands don't work inside containers
 - Each container is isolated from the host system
 - Need to `exit` to return to host terminal


### Mistakes I Made (and Fixed):
1. **Tried to run Docker inside container**
 - Error: `bash: docker: command not found`
 - Lesson: You can't run Docker commands inside a container unless you set up Docker-in-Docker
 - Fix: Realized I was already in the container and ready to work

---

## CHAPTER 3: ENHANCED LAB SETUP
**Goal:** Create a professional, organized lab environment with persistent storage and proper security

### Step-by-Step Process Completed:

#### Step 1: Create Your Project Structure
Created organized folder structure:

**Commands used:**
```powershell
cd C:\Users\YourName\Documents\pqc-docker-lab
mkdir lab-work
mkdir scripts
mkdir configs
dir
```

**Result:** Folders created
```
pqc-docker-lab/
 Dockerfile (Container blueprint)
 lab-work/ (Your work saved here - persists!)
 scripts/ (Helper scripts)
 configs/ (Configuration files)
```

**What this achieves:**
- Keeps project organized and professional
- Separates container config from your actual work
- `lab-work/` folder survives container deletion

#### Step 2: Update Your Dockerfile
Created an enhanced Dockerfile with security and proper user setup:

**File:** `Dockerfile`
```dockerfile
# Enhanced PQC Lab Dockerfile
FROM ubuntu:25.10

# Update and install everything in one layer (faster builds)
RUN apt-get update && \
 apt-get install -y \
 openssl \
 git \
 wget \
 curl \
 vim \
 nano \
 tree \
 && rm -rf /var/lib/apt/lists/*

# Create a lab user (security best practice)
RUN useradd -m -s /bin/bash labuser && \
 mkdir -p /home/labuser/work && \
 chown -R labuser:labuser /home/labuser

# Set working directory
WORKDIR /home/labuser/work

# Switch to labuser
USER labuser

# Default command
CMD ["/bin/bash", "-c", "echo ' PQC Lab Environment Ready!' && echo 'OpenSSL: $(openssl version)' && /bin/bash"]
```

**Key improvements over Chapter 2:**
- Added `git` for cloning repositories
- Added text editors (`vim`, `nano`) for file editing
- Added `wget`, `curl` for downloading files
- Added `tree` for viewing directory structures
- **Security:** Created `labuser` instead of running as root
- Working directory: `/home/labuser/work` (proper Linux structure)



#### Step 3: Rebuild Your Image
**Command used:**
```powershell
docker build -t pqc-lab:latest .
```

**Result:** SUCCESS
- New image name: `pqc-lab:latest`
- All tools installed successfully
- User `labuser` created with proper permissions
- Build time: 2-3 minutes (faster due to caching)

**What changed:**
- Old image: `pqc-simple` (basic OpenSSL only)
- New image: `pqc-lab:latest` (full toolset + security)

#### Step 4: Create a Run Script
Created a PowerShell script for easy container startup:

**File:** `scripts/run-pqc.ps1`
```powershell
# scripts/run-pqc.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " PQC Docker Lab Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Stop and remove any existing container
docker stop pqc-container 2>$null
docker rm pqc-container 2>$null

# Check if image exists
$imageExists = docker images --format "{{.Repository}}:{{.Tag}}" | Select-String "pqc-lab:latest"
if (-not $imageExists) {
 Write-Host "Image not found. Building..." -ForegroundColor Yellow
 docker build -t pqc-lab:latest .
}

# Run the container with volume mount
Write-Host "`n[>] Starting PQC Lab Container..." -ForegroundColor Green
Write-Host "Your work will be saved in: $PWD\lab-work" -ForegroundColor Yellow

docker run -it `
 --name pqc-container `
 --hostname pqc-lab `
 -v "${PWD}\lab-work:/home/labuser/work" `
 pqc-lab:latest

Write-Host "`n[SAVE] Your work is saved in: $PWD\lab-work" -ForegroundColor Green
```

#### Step 5: Run the Container with Your Script
**How to start the lab:**
```powershell
cd C:\Users\YourName\Documents\pqc-docker-lab
.\scripts\run-pqc.ps1
```

**Result:** Container running with volume mount
```
========================================
 PQC Docker Lab Launcher
========================================

 Starting PQC Lab Container...
Your work will be saved in: C:\Users\YourName\Documents\pqc-docker-lab\lab-work
 PQC Lab Environment Ready!
OpenSSL: OpenSSL 3.2.1 30 Jan 2024
labuser@pqc-lab:~/work$
```

**What I verified:**
- Welcome message displayed
- Running as `labuser` (not root)
- Working directory: `/home/labuser/work`
- Connected to Windows `lab-work` folder

#### Step 6: Clone the PQC Lab Guide
Downloaded the official lab materials from GitHub:

**Commands used inside container:**
```bash
# Clone the repository
git clone https://github.com/f5devcentral/openssl-pqc-stepbystep-lab.git

# Verify it worked
ls -la
```

**Result:** Lab guide downloaded
- Repository: `openssl-pqc-stepbystep-lab/`
- Location inside container: `/home/labuser/work/openssl-pqc-stepbystep-lab/`
- Location on Windows: `pqc-docker-lab/lab-work/openssl-pqc-stepbystep-lab/`
- Contains learning modules and exercises

**What's in the PQC Lab Guide:**
- Step-by-step tutorials
- FIPS, CNSA, and Alternative learning paths
- Module-based exercises
- Reference materials

#### Step 7: Test the Lab Setup
Verified everything works together:

**Commands tested inside container:**
```bash
# Navigate into the lab guide
cd openssl-pqc-stepbystep-lab

# See what learning paths are available
ls -la

# Check the README
head -20 README.md

# Go back to work directory
cd ..

# Create a test file that will persist on Windows
echo "My PQC Lab Notes - $(date)" > my-lab-notes.txt
echo "This file is saved on my Windows computer!" >> my-lab-notes.txt

# Show the file
cat my-lab-notes.txt
```

**Result:** All systems operational
- Lab guide accessible
- README readable
- Test file created successfully
- File persists on Windows

#### Step 8: Exit and Verify Persistence
**Test procedure:**
```bash
# Inside container:
exit
```

**Back in VS Code terminal (Windows):**
```powershell
# List contents of lab-work
dir lab-work

# Check your notes file
cat lab-work\my-lab-notes.txt
```

**Result:** Persistence verified
- `openssl-pqc-stepbystep-lab/` folder exists on Windows
- `my-lab-notes.txt` is there and readable
- Proves volume mount is working correctly


### What We've Built

| Component | Status | Purpose |
|-----------|--------|---------|
| Project Structure | Organized folders | Keeps files organized (`lab-work`, `scripts`, `configs`) |
| Enhanced Dockerfile | Built with labuser | Better security and tools |
| Run Script | Created (`run-pqc.ps1`) | One-click PowerShell startup |
| Volume Mount | Working | Saves work to Windows `lab-work` folder |
| PQC Lab Guide | Cloned | Official F5 OpenSSL PQC lab materials |

 
# **Module 2: Post-Quantum Root Certificate Authority with ML-DSA-87**
**Date:** February 10, 2026 
**Project:** Creating a quantum-resistant PKI foundation using NIST FIPS 204 standard 
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, Docker containerized environment

## **Objective**
Build a production-ready Root Certificate Authority using ML-DSA-87 (Module-Lattice Digital Signature Algorithm), a post-quantum cryptographic algorithm standardized by NIST FIPS 203/204, to establish a quantum-resistant Public Key Infrastructure.

## **Technical Implementation**

### **Directory Structure Setup**
```bash
# Created organized CA directory structure
mkdir -p 02_fips_quantum_ca_root/root/{certs,crl,newcerts,private}
chmod 700 02_fips_quantum_ca_root/root/private

# Initialize CA database files
touch 02_fips_quantum_ca_root/root/index.txt
echo 1000 > 02_fips_quantum_ca_root/root/serial
```

### **ML-DSA-87 Private Key Generation**
```bash
# Generate quantum-resistant private key
openssl genpkey -algorithm ML-DSA-87 \
 -out 02_fips_quantum_ca_root/root/private/root_ca.key

# Set secure permissions
chmod 600 02_fips_quantum_ca_root/root/private/root_ca.key

# Verify key generation
ls -lh 02_fips_quantum_ca_root/root/private/root_ca.key
# Output: -rw------- 1 labuser labuser 6.7K Feb 10 00:04 root_ca.key
```

### **OpenSSL Configuration Creation**
```bash
# Create CA configuration file
cat > 02_fips_quantum_ca_root/root/openssl.cnf << 'EOF'
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
x509_extensions = v3_ca
default_md = sha384
prompt = no

[ req_distinguished_name ]
countryName = US
stateOrProvinceName = Washington
localityName = Seattle
organizationName = My Quantum Lab
organizationalUnitName = PQC Research
commonName = My Post-Quantum Root CA

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
EOF
```

### **Root CA Certificate Generation**
```bash
# Generate self-signed Root CA certificate (10-year validity)
openssl req -new -x509 -days 3650 \
 -config 02_fips_quantum_ca_root/root/openssl.cnf \
 -key 02_fips_quantum_ca_root/root/private/root_ca.key \
 -out 02_fips_quantum_ca_root/root/certs/root_ca.crt

# Certificate generation takes 20-60 seconds due to ML-DSA-87 signing operations
```

## **Verification & Validation**

### **Comprehensive Verification Script**
```bash
# Run complete verification
cd 02_fips_quantum_ca_root

echo "=== Root CA Verification ==="
openssl verify -CAfile root/certs/root_ca.crt root/certs/root_ca.crt
openssl x509 -in root/certs/root_ca.crt -text -noout | grep "Signature Algorithm"
openssl x509 -in root/certs/root_ca.crt -text -noout | grep -A2 "Basic Constraints"
```

### **Verification Results**
```bash
# Actual output from verification
root/certs/root_ca.crt: OK # Self-verification successful
Signature Algorithm: ML-DSA-87 # Quantum-resistant algorithm confirmed
Basic Constraints: critical, CA:true # Proper CA configuration
```

### **Key-Certificate Pair Validation**
```bash
# Ensure private key matches certificate
openssl pkey -in root/private/root_ca.key -pubout -out /tmp/key_pub.pem
openssl x509 -in root/certs/root_ca.crt -pubkey -noout -out /tmp/cert_pub.pem

if diff /tmp/key_pub.pem /tmp/cert_pub.pem >/dev/null; then
 echo " Key and certificate match"
else
 echo " Key-certificate mismatch"
fi
```

## **Technical Specifications**

### **ML-DSA-87 Algorithm Details**
- **Standard:** NIST FIPS 204 (Module-Lattice Digital Signature Algorithm)
- **Security Level:** 5 (Highest NIST classification)
- **Key Size:** 6.7KB (vs 2KB for RSA-2048)
- **Quantum Resistance:** Based on lattice cryptography, resistant to Shor's algorithm

### **Certificate Details**
```bash
# Extract certificate information
openssl x509 -in root/certs/root_ca.crt -text -noout | head -20

# Expected output includes:
# Version: 3
# Signature Algorithm: ML-DSA-87
# Issuer/Subject: C=US, ST=Washington, L=Seattle, O=My Quantum Lab, CN=My Post-Quantum Root CA
# Validity: Feb 10 00:06:12 2026 GMT to Feb 8 00:06:12 2036 GMT
# Basic Constraints: CA:TRUE
# Key Usage: Digital Signature, Certificate Sign, CRL Sign
```

## **File Structure Created**
```
02_fips_quantum_ca_root/
 root/
 certs/root_ca.crt # Public certificate (11KB)
 private/root_ca.key # Private key (6.7KB, 600 permissions)
 openssl.cnf # Configuration (1.4KB)
 index.txt # Certificate database
 serial # Serial number counter
 crl/ # Certificate Revocation List directory
 newcerts/ # Future issued certificates
```

## **Security Considerations Implemented**

1. **Proper Key Permissions:** `chmod 600` ensures only owner can access private key
2. **Directory Separation:** Public certificates and private keys in separate directories
3. **Self-Contained Structure:** All CA files within module directory for portability
4. **No Hardcoded Paths:** Relative paths in configuration for flexibility
5. **Audit Trail:** `index.txt` tracks all certificate operations

## **Testing Commands Used**

```bash
# Test 1: Certificate inspection
openssl x509 -in root/certs/root_ca.crt -subject -noout
openssl x509 -in root/certs/root_ca.crt -issuer -noout
openssl x509 -in root/certs/root_ca.crt -dates -noout

# Test 2: Structure verification
tree root/ 2>/dev/null || find root/ -type f

# Test 3: Clean environment check
find . -type f \( -name "*.key" -o -name "*.crt" -o -name "openssl.cnf" \) \
 2>/dev/null | grep -v ".git" | grep -v "02_fips_quantum_ca_root"
```

## **Lessons Learned**

### **Quantum Cryptography Insights**
- ML-DSA-87 operations are slower than traditional algorithms (20-60 seconds vs <1 second)
- Larger key sizes (6.7KB vs 2KB) require storage and bandwidth considerations
- NIST standardization ensures interoperability and security assurance

### **PKI Best Practices**
- Root CA certificates should be self-signed with 10-year validity
- Private keys must have restrictive permissions (600)
- Clear separation between public certificates and private keys
- Database files (`index.txt`, `serial`) are essential for CA operations

### **OpenSSL 3.5.3 Features**
- Native PQC algorithm support without external modules
- `genpkey` command supports ML-DSA-87 directly
- Backward compatibility maintained with traditional algorithms

## **Significance for Quantum Migration**

This implementation demonstrates:
- **Practical quantum-resistant PKI** using standardized algorithms
- **Enterprise-ready structure** following security best practices
- **Forward compatibility** for hybrid certificate strategies
- **Real-world testing** of PQC algorithm performance characteristics

## **Next Steps**

The Root CA serves as the foundation for:
1. **Intermediate CA** creation (Module 3)
2. **End-entity certificate** issuance for web servers/applications
3. **Certificate revocation** and CRL management
4. **Hybrid certificates** combining classical and post-quantum cryptography

---
# **Module 3: Intermediate Certificate Authority Setup**
**Date:** February 10-11, 2026 
**Project:** Creating the second level of quantum-resistant PKI hierarchy 
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, Root CA Intermediate CA chain

## **Objective**
Establish an Intermediate Certificate Authority signed by the Root CA, creating a two-tier PKI hierarchy for improved security and operational flexibility while maintaining quantum-resistant cryptography throughout the chain.

## **Step-by-Step Implementation**

### **Step 1: Create Module 3 Directory Structure**
**Purpose:** Create dedicated workspace for Intermediate CA setup separate from Root CA 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs
mkdir -p 03_fips_quantum_ca_intermediate
ls -la | grep "03_fips_quantum_ca_intermediate"
```
**Result:** Organized module structure created: `drwxr-xr-x 1 labuser labuser 512 Feb 10 22:55 03_fips_quantum_ca_intermediate`

### **Step 2: Navigate to Module 3 Directory**
**Purpose:** Set correct working directory for all Intermediate CA operations 
```bash
cd 03_fips_quantum_ca_intermediate
pwd
```
**Result:** Working directory: `/home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate`

### **Step 3: Create Intermediate CA Directory Structure**
**Purpose:** Build professional PKI directory hierarchy with proper separation 
```bash
mkdir -p intermediate/{certs,crl,csr,newcerts,private}
touch intermediate/index.txt
echo 1000 > intermediate/serial
tree intermediate/ 2>/dev/null || ls -la intermediate/
```
**Result:** Created 5 subdirectories + 2 database files:
- `certs/` - Public certificates
- `crl/` - Certificate Revocation Lists 
- `csr/` - Certificate Signing Requests (NEW - not in Root CA)
- `newcerts/` - Issued certificate copies
- `private/` - Private keys
- `index.txt` - Certificate database
- `serial` - Serial number tracker

### **Step 4: Generate Intermediate CA Private Key**
**Purpose:** Create quantum-resistant ML-DSA-87 private key for Intermediate CA operations 
```bash
openssl genpkey -algorithm ML-DSA-87 -out intermediate/private/intermediate_ca.key
ls -lh intermediate/private/intermediate_ca.key
```
**Result:** Generated 6.7KB ML-DSA-87 key with automatic 600 permissions (`-rw-------`) 
**Note:** Took 20-60 seconds (ML-DSA-87 operations are computationally intensive)

### **Step 5: Create Intermediate CA Configuration File**
**Purpose:** Define policies, validity periods, extensions, and defaults for Intermediate CA 
```bash
cat > intermediate/openssl.cnf << 'EOF'
[OpenSSL configuration content - see full details in previous response]
EOF
ls -la intermediate/openssl.cnf
```
**Result:** Created 2.8KB configuration file with:
- **5-year validity** (1825 days vs Root's 10 years)
- **Less strict policy** (`= supplied` vs Root's `= match`)
- **Pathlen:0** (cannot create additional CAs)
- **Defaults matching** Root CA values (initially wrong - fixed later)

### **Step 6: Generate First CSR (Failed Attempt - Policy Mismatch)**
**Purpose:** Create Certificate Signing Request for Root CA to sign 
**Problem:** Values didn't match Root CA certificate 
```bash
openssl req -new \
 -config intermediate/openssl.cnf \
 -key intermediate/private/intermediate_ca.key \
 -out intermediate/csr/intermediate_ca.csr
openssl req -in intermediate/csr/intermediate_ca.csr -noout -subject
```
**Result:** CSR created but had mismatches:
- State: `California` (should be `Washington` like Root CA)
- Organization: `Quantum Security Lab Inc.` (should be `My Quantum Lab`)

### **Step 7: Fix Configuration to Match Root CA Values**
**Purpose:** Update Intermediate config to comply with Root CA's strict policy (`= match`) 
```bash
sed -i "s|stateOrProvinceName_default = California|stateOrProvinceName_default = Washington|" intermediate/openssl.cnf
sed -i "s|localityName_default = San Francisco|localityName_default = Seattle|" intermediate/openssl.cnf
sed -i "s|0.organizationName_default = Quantum Security Lab Inc.|0.organizationName_default = My Quantum Lab|" intermediate/openssl.cnf
grep -n "_default" intermediate/openssl.cnf | grep -E "(state|locality|organization)"
```
**Result:** Updated configuration to match Root CA:
- State: `Washington` x
- Locality: `Seattle` x 
- Organization: `My Quantum Lab` x

### **Step 8: Generate Corrected CSR**
**Purpose:** Create new CSR with values that match Root CA's certificate 
```bash
openssl req -new \
 -config intermediate/openssl.cnf \
 -key intermediate/private/intermediate_ca.key \
 -out intermediate/csr/intermediate_ca_v2.csr
openssl req -in intermediate/csr/intermediate_ca_v2.csr -noout -subject
```
**Result:** Successful CSR with matching values: 
`subject=C=US, ST=Washington, L=Seattle, O=My Quantum Lab, OU=Post-Quantum Intermediate CA, CN=Quantum Intermediate CA - ML-DSA-87`

### **Step 9: Fix Root CA Configuration Path Issue**
**Purpose:** Fix broken path in Root CA config that prevented signing 
**Issue:** Config had `dir = ./root` but we're already in `root/` directory 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/02_fips_quantum_ca_root/root
grep "dir" openssl.cnf | head -1
sed -i 's|dir\s*=\s*\./root|dir = .|' openssl.cnf
grep "dir" openssl.cnf | head -1
```
**Result:** Fixed path from `dir = ./root` `dir = .` (current directory)

### **Step 10: Root CA Signs Intermediate CSR**
**Purpose:** Establish trust chain by having Root CA sign Intermediate CSR 
```bash
openssl ca -config openssl.cnf \
 -extensions v3_ca \
 -days 1825 \
 -notext \
 -in ../../03_fips_quantum_ca_intermediate/intermediate/csr/intermediate_ca_v2.csr \
 -out ../../03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt
```
**Prompts answered:** `y` (Sign), `y` (Commit) 
**Result:** Intermediate certificate created, Root CA database updated with serial 1000

### **Step 11: Verify Intermediate Certificate**
**Purpose:** Confirm certificate was properly created and signed 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate
ls -lh intermediate/certs/intermediate_ca.crt
openssl x509 -in intermediate/certs/intermediate_ca.crt -text -noout | head -20
```
**Result:** 11KB certificate with:
- Serial: 4096 (0x1000)
- Algorithm: ML-DSA-87
- Issuer: Root CA
- Subject: Intermediate CA
- Validity: 5 years (Feb 10, 2026 to Feb 9, 2031)
- Pathlen:0 (cannot create additional CAs)

### **Step 12: Create Certificate Chain File**
**Purpose:** Combine certificates for easy deployment and validation 
```bash
cat intermediate/certs/intermediate_ca.crt \
 ../02_fips_quantum_ca_root/root/certs/root_ca.crt \
 > intermediate/certs/ca-chain.crt
ls -lh intermediate/certs/ca-chain.crt
openssl crl2pkcs7 -nocrl -certfile intermediate/certs/ca-chain.crt \
 | openssl pkcs7 -print_certs -text -noout | grep "Subject:"
```
**Result:** 21KB chain file containing both certificates in correct order (Intermediate Root)

## **Final File Structure Created**
```
03_fips_quantum_ca_intermediate/
 intermediate/
 certs/
 intermediate_ca.crt # Intermediate certificate (11KB)
 ca-chain.crt # Complete chain (21KB)
 crl/ # CRL directory (empty)
 csr/
 intermediate_ca.csr # Old CSR (wrong values)
 intermediate_ca_v2.csr # Correct CSR (signed)
 newcerts/ # Future issued certificates (empty)
 private/
 intermediate_ca.key # Private key (6.7KB, 600 permissions)
 index.txt # Certificate database (has entry)
 openssl.cnf # Configuration (updated values)
 serial # Serial tracker (now at 1001)
```

## **Certificate Chain Architecture**
```
Root CA (Offline, 10 years, ML-DSA-87)
 ↓ Signs with ML-DSA-87 signature
Intermediate CA (Online, 5 years, pathlen:0, ML-DSA-87) COMPLETE
 ↓ Will sign in Module 4
End-entity certificates (Future)
```

## **Key Technical Specifications**

### **Policy Differences**
| Field | Root CA Policy | Intermediate CA Policy | Reason |
|-------|---------------|---------------------|---------|
| countryName | `= match` | `= supplied` | Root strict, Intermediate flexible |
| stateOrProvinceName | `= match` | `= supplied` | Intermediate can be in different states |
| organizationName | `= match` | `= supplied` | Different departments can operate |
| commonName | `= supplied` | `= supplied` | Both require unique names |

### **Validity Periods**
- **Root CA:** 10 years (3650 days) - Long-term trust anchor
- **Intermediate CA:** 5 years (1825 days) - Operational, renewable
- **Path Length:** `pathlen:0` - Intermediate cannot create additional CAs

## **Challenges Overcome**

1. **Configuration Path Issue:** Fixed `dir = ./root` to `dir = .` in Root CA config
2. **Policy Mismatch:** Updated Intermediate values to match Root CA (Washington, My Quantum Lab)
3. **Extension Compatibility:** Used `v3_ca` instead of `v3_intermediate_ca` as Root CA only had that section
4. **Database Integrity:** Ensured Root CA's `index.txt` properly recorded issued certificate

## **Practical Insights**

### **PKI Hierarchy Best Practices**
- Two-tier hierarchy: Root (offline) + Intermediate (online) = Security + Flexibility
- Path length restriction (`pathlen:0`) limits damage if Intermediate is compromised
- Different validity periods appropriate for each level's role

### **Policy Management**
- Field matching requirements (`= match`) enforce organizational consistency
- Root CA uses strict policy, Intermediate uses more flexible policy
- Policy errors are common and require careful debugging

### **Certificate Chain Validation**
- Chain file must be in correct order: Intermediate Root
- Combined chain file simplifies deployment for servers/clients
- OpenSSL can validate the entire chain automatically

## **Module 3 Completion Status**

- 12 steps completed successfully
- Intermediate CA created with ML-DSA-87
- Certificate chain established with Root CA
- All configuration and policy issues resolved
- Ready for production certificate issuance
- Prepared for Module 4: End-entity Certificate Issuance

I'll update your lab journal with the Module 4 work we just completed. Let me create the new section:

---

## **Module 4: End-Entity Certificate Issuance**
**Date:** February 11, 2026 
**Project:** Issuing quantum-resistant certificates for web servers, users, and code signing 
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, Intermediate CA signing operations

## **Objective**
Create and sign end-entity certificates using the Intermediate CA, establishing a complete quantum-resistant certificate chain for real-world applications including web servers, user authentication, and code signing.

## **Step-by-Step Implementation**

### **Step 1: Create Module 4 Directory Structure**
**Purpose:** Establish organized workspace for different certificate types 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs
mkdir -p 04_end_entity_certificates
```
**Result:** Created dedicated module directory: `drwxr-xr-x 1 labuser labuser 512 Feb 11 02:39 04_end_entity_certificates`

### **Step 2: Navigate to Module 4 Directory**
**Purpose:** Set correct working directory for certificate issuance operations 
```bash
cd 04_end_entity_certificates
pwd
```
**Result:** Working directory: `/home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates`

### **Step 3: Create Directory Structure for End-Entity Certificates**
**Purpose:** Organize different certificate types into separate folders with proper subdirectories 
```bash
mkdir -p {web_server,user_auth,code_signing}/{certs,private,csr}
find . -type d | sort
```
**Result:** Created 9 directories total:
- Three certificate types: `web_server/`, `user_auth/`, `code_signing/`
- Each with: `certs/`, `csr/`, `private/` subdirectories

### **Step 4: Verify Subdirectory Structure**
**Purpose:** Confirm directory structure was created correctly 
```bash
find . -type d | sort
```
**Result:** Verified all directories exist with proper nesting

### **Step 5: Create Web Server Private Key (ML-DSA-87)**
**Purpose:** Generate quantum-resistant private key for TLS/SSL web server certificate 
```bash
openssl genpkey -algorithm ML-DSA-87 -out web_server/private/web_server.key
ls -la web_server/private/
```
**Result:** Generated 6.7KB ML-DSA-87 private key with secure permissions (`-rw-------`)

### **Step 6: Create Web Server Certificate Configuration File**
**Purpose:** Define certificate attributes including Subject Alternative Names (SANs) and key usage 
```bash
cat > web_server/web_server.cnf << 'EOF'
[OpenSSL configuration content with SANs, basicConstraints, keyUsage, etc.]
EOF
cat web_server/web_server.cnf
```
**Result:** Created configuration with:
- Subject: `Quantum Secure Web Inc`, `www.quantumsecureweb.example.com`
- SANs: Multiple DNS names + IP address
- Key Usage: `digitalSignature, keyEncipherment`
- Extended Key Usage: `serverAuth`

### **Step 7: Create Web Server Certificate Signing Request (CSR)**
**Purpose:** Generate CSR for Intermediate CA to sign 
```bash
openssl req -new \
 -key web_server/private/web_server.key \
 -config web_server/web_server.cnf \
 -out web_server/csr/web_server.csr
ls -la web_server/csr/
```
**Result:** Generated 10KB CSR file ready for signing

### **Step 8: Examine the Web Server CSR**
**Purpose:** Verify CSR contains correct information and extensions 
```bash
openssl req -in web_server/csr/web_server.csr -text -noout
```
**Result:** Verified:
- Subject matches configuration
- Public Key Algorithm: ML-DSA-87
- Extensions: SANs, CA:FALSE, serverAuth

### **Step 9: Sign the Web Server Certificate with Intermediate CA**
**Purpose:** Have Intermediate CA sign the CSR to create valid certificate 
**Challenge:** Configuration path issues required running from Intermediate CA directory 
```bash
cd ../03_fips_quantum_ca_intermediate/intermediate/
openssl ca -config openssl.cnf \
 -days 365 \
 -notext \
 -md sha512 \
 -in ../../04_end_entity_certificates/web_server/csr/web_server.csr \
 -out ../../04_end_entity_certificates/web_server/certs/web_server.crt
# Prompts: y (Sign), y (Commit)
```
**Result:** Certificate successfully signed with 365-day validity

### **Step 10: Complete Certificate Verification**
**Purpose:** Validate certificate chain and verify all extensions 
```bash
cd ../../04_end_entity_certificates/
openssl x509 -in web_server/certs/web_server.crt -text -noout | head -40
openssl verify -CAfile ../03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt web_server/certs/web_server.crt
```
**Result:** All verifications passed:
- Certificate chain: `OK`
- Issuer: Intermediate CA
- Subject: Web server information matches
- Algorithm: ML-DSA-87
- Validity: 1 year (Feb 11 2026 to Feb 11 2027)

## **Final File Structure Created**
```
04_end_entity_certificates/
 web_server/
 certs/web_server.crt # Signed certificate
 csr/web_server.csr # Certificate Signing Request
 private/web_server.key # ML-DSA-87 private key
 web_server.cnf # Configuration file
 user_auth/
 certs/ csr/ private/ # ⏳ Ready for future certificates
 code_signing/
 certs/ csr/ private/ # ⏳ Ready for future certificates
```

## **Certificate Chain Architecture**
```
Root CA (ML-DSA-87, 10 years, offline)
 ↓
Intermediate CA (ML-DSA-87, 5 years, online) 
 ↓
Web Server Certificate (ML-DSA-87, 1 year, end-entity) COMPLETE
 ↓
User Authentication Certificate (Future)
 ↓
Code Signing Certificate (Future)
```

## **Key Technical Specifications**
- **Certificate Type:** TLS Web Server Authentication
- **Validity Period:** 365 days (standard for web certificates)
- **Key Usage:** `digitalSignature, keyEncipherment`
- **Extended Key Usage:** `serverAuth` (TLS Web Server Authentication)
- **Subject Alternative Names (SANs):** Multiple DNS entries + IP address
- **Basic Constraints:** `CA:FALSE` (end-entity certificate)

## **Challenges Overcome**
1. **Configuration Path Issues:** Intermediate CA's `openssl.cnf` used relative paths requiring execution from correct directory
2. **Extension Section Missing:** Intermediate CA config didn't have `server_cert` extension section; resolved by using extensions from CSR
3. **Path Navigation:** Multiple `cd` commands needed to navigate between module directories for proper relative paths

## **Practical Insights**
1. **End-entity vs CA Certificates:** End-entity certificates have `CA:FALSE` and specific key usages, unlike CAs which have `CA:TRUE`
2. **Subject Alternative Names (SANs):** Modern certificates require SANs for multiple domain/IP coverage
3. **Certificate Purpose Restrictions:** Different certificate types (serverAuth, clientAuth, codeSigning) have specific extension requirements
4. **Signing Workflow:** Must run `openssl ca` from CA directory for config file paths to work correctly
5. **Chain Validation:** OpenSSL can validate entire certificate chain with single command using chain file

## **Module 4 Progress Status**

- Web server certificate created and signed
- Complete quantum-resistant certificate chain established
- Certificate verification successful with openssl verify
- Organized structure ready for additional certificate types
- Ready to create user authentication certificates
- Ready to create code signing certificates
- Foundation for production PQC deployment complete


---

## **Module 4 Part 2: User Authentication Certificate**
**Project:** Creating quantum-resistant client authentication certificate for user/client authentication 
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, clientAuth extensions

## **Objective**
Create and sign a user authentication certificate with `clientAuth` extensions for TLS mutual authentication, VPN access, and email signing, establishing quantum-resistant identity verification.

## **Step-by-Step Implementation**

### **Step 1: Navigate to Module 4 Directory**
**Purpose:** Set correct working directory for user authentication certificate creation 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/
pwd
```
**Result:** Working directory: `/home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates`

### **Step 2: Verify User Auth Directory Structure**
**Purpose:** Confirm the pre-created directory structure exists 
```bash
ls -la user_auth/
```
**Result:** Directory structure already exists with `certs/`, `csr/`, `private/` subdirectories

### **Step 3: Create User Authentication Configuration File**
**Purpose:** Define certificate attributes specific to client authentication (different from server certificate) 
```bash
cd user_auth/
cat > user_auth.cnf << 'EOF'
# User Authentication Certificate Configuration
# For clientAuth (user authentication, VPN, mutual TLS)

[req]
default_bits = 2048
prompt = no
default_md = sha384
distinguished_name = dn
req_extensions = req_ext

[dn]
C = US
ST = California
L = San Francisco
O = PQCLab Security
OU = Authentication Department
CN = pqc-user@example.com
emailAddress = pqc-user@example.com

[req_ext]
keyUsage = critical, digitalSignature, keyAgreement
extendedKeyUsage = clientAuth, emailProtection
subjectAltName = email:pqc-user@example.com
basicConstraints = critical, CA:FALSE
EOF
cat user_auth.cnf
```
**Result:** Created configuration with client-specific settings:
- CN as email address: `pqc-user@example.com`
- Key Usage: `digitalSignature, keyAgreement`
- Extended Key Usage: `clientAuth, emailProtection`

### **Step 4: Generate ML-DSA-87 Private Key**
**Purpose:** Create quantum-resistant private key for user authentication 
```bash
openssl genpkey -algorithm ML-DSA-87 -out private/user_auth.key
ls -la private/
```
**Result:** Generated 6.7KB ML-DSA-87 private key with secure permissions (`-rw-------`)

### **Step 5: Generate Certificate Signing Request (CSR)**
**Purpose:** Create CSR for Intermediate CA to sign 
```bash
openssl req -new -key private/user_auth.key -out csr/user_auth.csr -config user_auth.cnf
ls -la csr/
```
**Result:** Generated 10KB CSR file with clientAuth extensions

### **Step 6: Navigate to Intermediate CA Directory**
**Purpose:** Need to be in Intermediate CA directory for signing due to relative paths in config 
```bash
cd ../03_fips_quantum_ca_intermediate/intermediate/
pwd
```
**Result:** Working directory: `/home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate`

### **Step 7: Create Custom Extensions File**
**Purpose:** Intermediate CA config lacked `user_cert` section, needed custom extensions file 
```bash
cd ../../04_end_entity_certificates/user_auth/
cat > user_auth_extensions.cnf << 'EOF'
# Extensions for User Authentication Certificate
basicConstraints = CA:FALSE
keyUsage = critical, digitalSignature, keyAgreement
extendedKeyUsage = clientAuth, emailProtection
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
EOF
cat user_auth_extensions.cnf
```
**Result:** Created custom extensions file to override Intermediate CA's missing user_cert section

### **Step 8: Sign the User Authentication Certificate**
**Purpose:** Have Intermediate CA sign the CSR with 90-day validity (standard for user certificates) 
```bash
cd ../03_fips_quantum_ca_intermediate/intermediate/
openssl ca -config openssl.cnf \
 -extfile ../../04_end_entity_certificates/user_auth/user_auth_extensions.cnf \
 -days 90 \
 -notext \
 -md sha384 \
 -in ../../04_end_entity_certificates/user_auth/csr/user_auth.csr \
 -out ../../04_end_entity_certificates/user_auth/certs/user_auth.crt
# Prompts: y (Sign), y (Commit)
```
**Result:** Certificate successfully signed with 90-day validity

### **Step 9: Verify the Signed Certificate**
**Purpose:** Validate certificate details and ensure correct extensions were applied 
```bash
cd ../../04_end_entity_certificates/user_auth/
openssl x509 -in certs/user_auth.crt -text -noout | head -40
openssl x509 -in certs/user_auth.crt -text -noout | grep -A 10 "X509v3 extensions"
```
**Result:** Certificate verified with:
- Algorithm: ML-DSA-87
- Subject: `pqc-user@example.com`
- Validity: 90 days (Feb 11 to May 12, 2026)
- Extensions: Basic Constraints (CA:FALSE), Key Usage (Digital Signature, Key Agreement), Extended Key Usage (TLS Web Client Authentication, E-mail Protection)

### **Step 10: Verify Certificate Chain**
**Purpose:** Ensure certificate is properly chained to Intermediate and Root CAs 
```bash
openssl verify -CAfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt certs/user_auth.crt
```
**Result:** `certs/user_auth.crt: OK` - Complete chain validation successful

## **Final File Structure Created**
```
04_end_entity_certificates/user_auth/
 certs/user_auth.crt # Signed certificate (10KB)
 csr/user_auth.csr # Certificate Signing Request (10KB)
 private/user_auth.key # ML-DSA-87 private key (6.7KB)
 user_auth.cnf # Configuration file (564B)
 user_auth_extensions.cnf # Custom extensions file (242B)
```

## **Certificate Chain Architecture**
```
Root CA (ML-DSA-87, 10 years, offline)
 ↓
Intermediate CA (ML-DSA-87, 5 years, online) 
 ↓
User Authentication Certificate (ML-DSA-87, 90 days, clientAuth) COMPLETE
```

## **Key Technical Specifications**
- **Certificate Type:** TLS Web Client Authentication & E-mail Protection
- **Validity Period:** 90 days (standard for user certificates)
- **Key Usage:** `digitalSignature, keyAgreement` (critical)
- **Extended Key Usage:** `clientAuth, emailProtection`
- **Subject:** Email address (`pqc-user@example.com`)
- **Subject Alternative Name:** Email format for user identification

## **Challenges Overcome**
1. **Missing Extension Section:** Intermediate CA config didn't have `user_cert` section - resolved by creating custom extensions file
2. **Path Navigation Complexity:** Multiple directory changes needed due to relative paths in OpenSSL config files
3. **Extension Specificity:** User certificates require different extensions (`clientAuth`, `emailProtection`) vs server certificates (`serverAuth`)

## **Practical Insights**
1. **User vs Server Certificates:** User certificates use `clientAuth` extensions and often have email addresses as subjects
2. **Validity Differences:** User certificates typically have shorter validity (90-180 days) vs server certificates (1-2 years)
3. **Extension Flexibility:** When CA config lacks specific extension sections, custom extensions files can override
4. **Path Dependencies:** OpenSSL `ca` command requires execution from CA directory due to relative path configurations
5. **Client Authentication Use Cases:** `clientAuth` enables mutual TLS, VPN authentication, and secure user identification

## **Module 4 Part 2 Completion Status**

- User authentication certificate created and signed
- Custom extensions file created for clientAuth requirements
- 90-day validity period applied (standard for user certs)
- Certificate chain validation successful
- Complete quantum-resistant client authentication solution
- Ready to create code signing certificates
- All end-entity certificate types will be completed
- Production-ready PQC certificate hierarchy established

Based on our recent work, I need to update **My-Lab-Journal.md** with **Module 4 Part 3: Code Signing Certificate**.

Here's the new section to add:

---

## **Module 4 Part 3: Code Signing Certificate**
**Project:** Creating quantum-resistant code signing certificate for software/firmware signing 
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, codeSigning extensions

## **Objective**
Create and sign a code signing certificate with `codeSigning` extensions for digitally signing software, scripts, and firmware updates, establishing quantum-resistant integrity verification for software distribution.

## **Step-by-Step Implementation**

### **Step 1: Navigate to Module 4 Code Signing Directory**
**Purpose:** Set correct working directory for code signing certificate creation 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/code_signing/
pwd
```
**Result:** Working directory: `/home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/code_signing`

### **Step 2: Create Code Signing Configuration File**
**Purpose:** Define certificate attributes specific to code signing (different from server/client certificates) 
```bash
cat > code_signing.cnf << 'EOF'
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext

[dn]
C = US
ST = California
O = PQCLab Security
OU = Software Development Department
CN = pqc-code-signer@example.com
emailAddress = pqc-code-signer@example.com

[req_ext]
keyUsage = digitalSignature
extendedKeyUsage = codeSigning
basicConstraints = CA:FALSE
EOF
ls -la code_signing.cnf
```
**Result:** Created configuration with code-specific settings (367 bytes):
- Subject: Software Development Department
- Key Usage: Only `digitalSignature` (no keyEncipherment or keyAgreement)
- Extended Key Usage: `codeSigning`

### **Step 3: Create Extensions Configuration File**
**Purpose:** Create separate extensions file for Intermediate CA signing process 
```bash
cat > code_signing_extensions.cnf << 'EOF'
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
keyUsage = digitalSignature
extendedKeyUsage = codeSigning
basicConstraints = CA:FALSE
EOF
ls -la code_signing_extensions.cnf
```
**Result:** Created extensions file (160 bytes) with:
- Proper chain identifiers (subjectKeyIdentifier, authorityKeyIdentifier)
- Code signing-specific key usage
- `codeSigning` extended key usage

### **Step 4: Generate ML-DSA-87 Private Key**
**Purpose:** Create quantum-resistant private key for code signing operations 
```bash
openssl genpkey -algorithm ML-DSA-87 -out private/code_signing.key
ls -la private/
```
**Result:** Generated 6.7KB ML-DSA-87 private key with secure permissions (`-rw-------`)

### **Step 5: Generate Certificate Signing Request (CSR)**
**Purpose:** Create CSR for Intermediate CA to sign 
```bash
openssl req -new \
 -key private/code_signing.key \
 -out csr/code_signing.csr \
 -config code_signing.cnf
ls -la csr/
openssl req -in csr/code_signing.csr -noout -text | head -20
```
**Result:** Generated 10KB CSR file with:
- Subject: `pqc-code-signer@example.com`, `Software Development Department`
- Public Key Algorithm: ML-DSA-87
- Requested extensions: `codeSigning`, `digitalSignature`

### **Step 6: Sign the Code Signing Certificate**
**Purpose:** Have Intermediate CA sign the CSR with 1-year validity (standard for code signing) 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/
openssl ca -config openssl.cnf \
 -extfile /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/code_signing/code_signing_extensions.cnf \
 -days 365 \
 -notext \
 -md sha256 \
 -in /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/code_signing/csr/code_signing.csr \
 -out /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/code_signing/certs/code_signing.crt
# Prompts: y (Sign), y (Commit)
```
**Result:** Certificate successfully signed with 1-year validity

### **Step 7: Verify Certificate Details**
**Purpose:** Validate certificate and ensure correct code signing extensions were applied 
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/code_signing/
openssl x509 -in certs/code_signing.crt -noout -subject -dates -purpose
openssl x509 -in certs/code_signing.crt -noout -ext extendedKeyUsage
```
**Result:** Certificate verified with:
- Subject: `OU=Software Development Department, CN=pqc-code-signer@example.com`
- Validity: 1 year (Feb 11 2026 to Feb 11 2027)
- Extended Key Usage: `Code Signing`

### **Step 8: Verify Certificate Chain**
**Purpose:** Ensure certificate is properly chained to Intermediate and Root CAs 
```bash
openssl verify -CAfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt certs/code_signing.crt
```
**Result:** `certs/code_signing.crt: OK` - Complete chain validation successful

### **Step 9: Create Certificate Chain File**
**Purpose:** Create combined chain file for easy deployment and validation 
```bash
cat certs/code_signing.crt ../../03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt > certs/code_signing-chain.crt
ls -la certs/
openssl crl2pkcs7 -nocrl -certfile certs/code_signing-chain.crt | openssl pkcs7 -print_certs -noout | grep "subject=" | wc -l
```
**Result:** Created 31KB chain file containing all 3 certificates:
1. Code Signing Certificate (end entity)
2. Intermediate CA Certificate
3. Root CA Certificate

## **Final File Structure Created**
```
04_end_entity_certificates/code_signing/
 certs/
 code_signing.crt # Signed certificate (10KB)
 code_signing-chain.crt # Complete chain (31KB)
 csr/
 code_signing.csr # Certificate Signing Request (10KB)
 private/
 code_signing.key # ML-DSA-87 private key (6.7KB)
 code_signing.cnf # Configuration file (367B)
 code_signing_extensions.cnf # Custom extensions file (160B)
```

## **Certificate Chain Architecture**
```
Root CA (ML-DSA-87, 10 years, offline)
 ↓
Intermediate CA (ML-DSA-87, 5 years, online) 
 ↓
Code Signing Certificate (ML-DSA-87, 1 year, codeSigning) COMPLETE
```

## **Key Technical Specifications**
- **Certificate Type:** Code Signing for software/firmware integrity
- **Validity Period:** 1 year (standard for code signing certificates)
- **Key Usage:** `digitalSignature` only (no encryption or key agreement)
- **Extended Key Usage:** `codeSigning`
- **Subject:** Software Development Department, code signer email
- **Basic Constraints:** `CA:FALSE` (end-entity certificate)

## **Challenges Overcome**
1. **Extension Specificity:** Code signing requires different extensions (`codeSigning`) vs serverAuth/clientAuth
2. **Limited Key Usage:** Only `digitalSignature` allowed (no keyEncipherment or keyAgreement)
3. **Department Organization:** Created `Software Development Department` OU to reflect real-world organizational structure
4. **ML-DSA-87 Performance:** Key generation and signing operations remain slower than classical algorithms

## **Practical Insights**
1. **Code Signing Specifics:** Code signing certificates have unique requirements with limited key usage
2. **Organizational Structure:** Different departments (Software Development, Authentication) help categorize certificate purposes
3. **Extension Files:** Creating separate extensions files provides flexibility when CA configs lack specific sections
4. **One-Year Validity:** Code signing certificates typically have 1-3 year validity depending on organizational policy
5. **Digital Signature Only:** Code signing only requires `digitalSignature` key usage, unlike server certificates

## **Module 4 Part 3 Completion Status**

- Code signing certificate created and signed with ML-DSA-87
- Proper extensions applied (codeSigning, digitalSignature)
- One-year validity period applied (standard for code signing)
- Complete certificate chain validated and created
- All three end-entity certificate types now complete
- Module 4 fully completed: Web Server, User Auth, and Code Signing certificates
- Complete quantum-resistant PKI hierarchy established
- Ready for production deployment or Module 5 

---

## **Module 4 Part 4: High-Security Vault Server Certificate**
**Date:** February 11-12, 2026
**Project:** Creating a high-security quantum-resistant server certificate for critical infrastructure (vault, secrets, HSM)
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, serverAuth extensions with 2-year validity

---

## **Objective**
Create and sign a high-security vault server certificate with ML-DSA-87 for critical infrastructure systems, including secret management, hardware security modules (HSM), and internal security services, establishing quantum-resistant protection for the most sensitive organizational assets.

---

## **Step-by-Step Implementation**

### **Step 1: Create Vault Server Directory Structure**
**Purpose:** Establish dedicated workspace for the high-security vault server certificate, following the same organizational pattern as other certificate types
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/
mkdir -p vault_server/{certs,private,csr}
cd vault_server
```
**Result:** Created `vault_server/` directory with three subdirectories:
- `certs/` - Will store signed certificates
- `private/` - Will store private key (restricted permissions)
- `csr/` - Will store Certificate Signing Request

---

### **Step 2: Create Vault Server Configuration File**
**Purpose:** Define the certificate attributes, subject distinguished name, and Subject Alternative Names (SANs) for the vault server
```bash
cat > vault_server.cnf << 'EOF'
[ req ]
default_bits = 4096
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[ req_distinguished_name ]
countryName = US
stateOrProvinceName = Washington
localityName = Seattle
organizationName = PQCLab Security
organizationalUnitName = Security Infrastructure
commonName = vault.pqclab.example.com
emailAddress = security@pqclab.example.com

[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = vault.pqclab.example.com
DNS.2 = secrets.pqclab.example.com
DNS.3 = hsm.pqclab.example.com
IP.1 = 192.168.100.10
EOF
```
**Result:** Created `vault_server.cnf` (737 bytes) with:
- Distinguished Name: Organization `PQCLab Security`, Organizational Unit `Security Infrastructure`
- Key Usage: `digitalSignature` and `keyEncipherment` with critical flag
- Extended Key Usage: `serverAuth` only
- Subject Alternative Names: 3 domains + 1 IP address

---

### **Step 3: Generate ML-DSA-87 Private Key**
**Purpose:** Create a quantum-resistant private key using the highest NIST security level (Level 5) for critical infrastructure protection
```bash
openssl genpkey -algorithm ML-DSA-87 -out private/vault_server.key
```
**Result:** Generated `private/vault_server.key` (6774 bytes) with:
- Algorithm: ML-DSA-87
- Permissions: `-rw-------` (600) - owner read/write only
- Generation time: Approximately 20-60 seconds

---

### **Step 4: Verify Private Key Creation**
**Purpose:** Confirm the private key was generated successfully and has correct permissions
```bash
ls -la private/
openssl pkey -in private/vault_server.key -noout -text | head -5
```
**Result:**
```
-rw------- 1 labuser labuser 6774 Feb 11 23:20 vault_server.key
ML-DSA-87 Private-Key:
seed:
 0f:30:6c:20:3c:bf:bb:e1:9d:82:b7:64:3d:69:c9:
 47:b3:d3:af:14:2c:43:ab:7e:08:e4:f6:9d:a4:79:
 18:3d
```

---

### **Step 5: Create Certificate Signing Request (CSR)**
**Purpose:** Generate a CSR containing the public key and identity information to send to the Intermediate CA for signing
```bash
openssl req -new \
 -key private/vault_server.key \
 -out csr/vault_server.csr \
 -config vault_server.cnf
```
**Result:** Created `csr/vault_server.csr` (10405 bytes) containing the public key, subject information, and requested extensions.

---

### **Step 6: Verify CSR Creation**
**Purpose:** Confirm the CSR was created and contains the correct information
```bash
ls -la csr/
openssl req -in csr/vault_server.csr -noout -text | grep -A 15 "Subject:\|X509v3 extensions:"
```
**Result:**
```
-rw-r--r-- 1 labuser labuser 10405 Feb 11 23:25 vault_server.csr
Subject: C=US, ST=Washington, L=Seattle, O=PQCLab Security, OU=Security Infrastructure, CN=vault.pqclab.example.com, emailAddress=security@pqclab.example.com
Public Key Algorithm: ML-DSA-87
```

---

### **Step 7: Create Custom Extensions File for Signing**
**Purpose:** Create a standalone extensions file because the Intermediate CA's configuration lacks a `server_cert` section for vault server certificates
```bash
cat > vault_server_extensions.cnf << 'EOF'
# Extensions for Vault Server Certificate (High-Security Infrastructure)
basicConstraints = CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = vault.pqclab.example.com
DNS.2 = secrets.pqclab.example.com
DNS.3 = hsm.pqclab.example.com
IP.1 = 192.168.100.10
EOF
```
**Result:** Created `vault_server_extensions.cnf` (416 bytes) with complete extension definitions for the signing process.

---

### **Step 8: Sign the Vault Server Certificate with Intermediate CA**
**Purpose:** Have the Intermediate CA sign the CSR to create a trusted X.509 certificate with 2-year validity for critical infrastructure
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/

openssl ca -config openssl.cnf \
 -extfile /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/vault_server/vault_server_extensions.cnf \
 -days 730 \
 -notext \
 -md sha384 \
 -in /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/vault_server/csr/vault_server.csr \
 -out /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/vault_server/certs/vault_server.crt
```
**Prompts answered:**
- `Sign the certificate? [y/n]: y`
- `1 out of 1 certificate requests certified, commit? [y/n]: y`

**Result:** Certificate successfully signed with:
- Serial number: `1003`
- Validity: 730 days (Feb 11 2026 - Feb 11 2028)
- Issuer: Intermediate CA
- Subject: Vault server distinguished name

---

### **Step 9: Verify Certificate Creation**
**Purpose:** Confirm the signed certificate was created and inspect its details
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/vault_server/
ls -la certs/
openssl x509 -in certs/vault_server.crt -noout -subject -dates -issuer
```
**Result:**
```
-rw-r--r-- 1 labuser labuser 10694 Feb 11 23:42 vault_server.crt
subject=C=US, ST=Washington, O=PQCLab Security, OU=Security Infrastructure, CN=vault.pqclab.example.com, emailAddress=security@pqclab.example.com
notBefore=Feb 11 23:41:58 2026 GMT
notAfter=Feb 11 23:41:58 2028 GMT
issuer=C=US, ST=Washington, O=My Quantum Lab, OU=Post-Quantum Intermediate CA, CN=Quantum Intermediate CA - ML-DSA-87
```

---

### **Step 10: Verify Certificate Extensions**
**Purpose:** Ensure the critical extensions (SANs, key usage, EKU) were properly applied
```bash
openssl x509 -in certs/vault_server.crt -noout -text | grep -A 20 "X509v3 extensions:"
```
**Result:**
```
X509v3 extensions:
 X509v3 Basic Constraints:
 CA:FALSE
 X509v3 Key Usage: critical
 Digital Signature, Key Encipherment
 X509v3 Extended Key Usage:
 TLS Web Server Authentication
 X509v3 Subject Key Identifier:
 06:5D:4A:ED:2B:B8:A7:2D:4F:26:F7:CA:CF:AD:BD:A0:17:09:EE:ED
 X509v3 Authority Key Identifier:
 A1:F4:4C:5F:52:30:28:EB:E0:92:C2:81:CB:CA:4C:DA:86:CF:01:78
 X509v3 Subject Alternative Name:
 DNS:vault.pqclab.example.com, DNS:secrets.pqclab.example.com, DNS:hsm.pqclab.example.com, IP Address:192.168.100.10
```

---

### **Step 11: Verify Certificate Chain**
**Purpose:** Validate that the vault server certificate is properly chained to the Intermediate and Root CAs
```bash
openssl verify -CAfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt certs/vault_server.crt
```
**Result:**
```
certs/vault_server.crt: OK
```

---

### **Step 12: Check CA Database Entry**
**Purpose:** Confirm the certificate issuance was recorded in the Intermediate CA's database
```bash
tail -5 /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/index.txt
```
**Result:**
```
V 270211025132Z 1000 unknown /C=US/ST=California/O=Quantum Secure Web Inc/CN=www.quantumsecureweb.example.com/emailAddress=admin@quantumsecureweb.example.com
V 260512043900Z 1001 unknown /C=US/ST=California/O=PQCLab Security/OU=Authentication Department/CN=pqc-user@example.com/emailAddress=pqc-user@example.com
V 270211055255Z 1002 unknown /C=US/ST=California/O=PQCLab Security/OU=Software Development Department/CN=pqc-code-signer@example.com/emailAddress=pqc-code-signer@example.com
V 280211234158Z 1003 unknown /C=US/ST=Washington/O=PQCLab Security/OU=Security Infrastructure/CN=vault.pqclab.example.com/emailAddress=security@pqclab.example.com
```

---

### **Step 13: Create Certificate Chain File**
**Purpose:** Combine the vault server certificate with the Intermediate and Root CA certificates into a single file for easy deployment
```bash
cat certs/vault_server.crt ../../03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt > certs/vault_server-chain.crt
```
**Result:** Created `certs/vault_server-chain.crt` (31688 bytes) containing all three certificates in order.

---

### **Step 14: Verify Chain File**
**Purpose:** Confirm the chain file was created and contains all three certificates
```bash
ls -la certs/
openssl crl2pkcs7 -nocrl -certfile certs/vault_server-chain.crt | openssl pkcs7 -print_certs -noout | grep "subject=" | wc -l
openssl verify -CAfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt certs/vault_server-chain.crt
```
**Result:**
```
-rw-r--r-- 1 labuser labuser 10694 Feb 11 23:42 vault_server.crt
-rw-r--r-- 1 labuser labuser 31688 Feb 12 00:04 vault_server-chain.crt
3
certs/vault_server-chain.crt: OK
```

---

## **Final File Structure Created**

```
04_end_entity_certificates/vault_server/
 certs/
 vault_server.crt # Signed certificate (10694 bytes)
 vault_server-chain.crt # Complete chain with Intermediate + Root (31688 bytes)
 csr/
 vault_server.csr # Certificate Signing Request (10405 bytes)
 private/
 vault_server.key # ML-DSA-87 private key (6774 bytes, 600 permissions)
 vault_server.cnf # CSR configuration file (737 bytes)
 vault_server_extensions.cnf # Custom extensions for signing (416 bytes)
```

---

## **Certificate Chain Architecture**

```
Root CA (ML-DSA-87, 10 years, offline, "My Quantum Lab")
 ↓
Intermediate CA (ML-DSA-87, 5 years, pathlen:0, "Quantum Intermediate CA - ML-DSA-87")
 ↓
Vault Server Certificate (ML-DSA-87, 2 years, serverAuth, "Security Infrastructure")
 ↓
[Supports: vault.pqclab.example.com, secrets.pqclab.example.com, hsm.pqclab.example.com, 192.168.100.10]
```

---

## **Key Technical Specifications**

- **Certificate Type:** High-Security TLS Web Server Authentication for critical infrastructure
- **Algorithm:** ML-DSA-87 (NIST FIPS 204, Security Level 5)
- **Validity Period:** 730 days (2 years) - extended for critical systems
- **Key Usage:** `digitalSignature, keyEncipherment` (critical flag enforced)
- **Extended Key Usage:** `serverAuth` (TLS Web Server Authentication only)
- **Subject:** `CN=vault.pqclab.example.com, OU=Security Infrastructure, O=PQCLab Security`
- **Subject Alternative Names:**
 - DNS: `vault.pqclab.example.com` (primary)
 - DNS: `secrets.pqclab.example.com` (secret management)
 - DNS: `hsm.pqclab.example.com` (Hardware Security Module)
 - IP: `192.168.100.10` (internal network access)
- **Basic Constraints:** `CA:FALSE`
- **Serial Number:** `1003`
- **Chain File Size:** 31,688 bytes

---

## **Challenges Overcome**

- **Missing Extension Section in CA Configuration:** The Intermediate CA's `openssl.cnf` file did not have a `server_cert` extension section. Resolved by creating a custom `vault_server_extensions.cnf` file and passing it directly to the `openssl ca` command with the `-extfile` parameter.

- **File Placement Error:** The extensions file was initially created in the Intermediate CA directory instead of the vault_server directory. Fixed by moving the file to the correct location using the `mv` command, maintaining consistent organizational structure.

- **Two-Year Validity Configuration:** Unlike regular web server certificates (365 days), critical infrastructure requires longer validity periods. The `-days 730` parameter was explicitly set to meet this requirement for high-security systems.

- **SHA-384 Hash Algorithm:** While other certificates used SHA-256, the vault server certificate uses SHA-384 (`-md sha384`) for stronger cryptographic binding with ML-DSA-87 at the highest security level.

---

## **Practical Insights**

- **Critical Infrastructure vs Standard Servers:** Vault and HSM servers require different treatment than public-facing web servers. Longer validity periods (2 years vs 1 year), stronger hash algorithms (SHA-384 vs SHA-256), and distinct Organizational Units (`Security Infrastructure` vs `Web Services`) reflect different security postures and administrative domains.

- **Custom Extensions Files Provide Flexibility:** When a CA configuration lacks specific extension sections, creating standalone `.cnf` files and passing them with `-extfile` gives complete control over certificate extensions without modifying the CA's master configuration. This pattern was used successfully for user authentication, code signing, and now vault server certificates.

- **Subject Alternative Names Are Mandatory:** Modern TLS clients completely ignore the Common Name field and only validate against SANs. Including all possible domain names and IP addresses in the SAN section is critical for certificate functionality. This certificate supports three domains and one IP address.

- **Certificate Chain Validation:** The `openssl verify` command with `-CAfile` validates the entire trust path in one operation. A return value of `OK` confirms that every signature in the chain is cryptographically valid, no certificates are expired, and all path constraints are satisfied.

- **Organizational Unit as Security Boundary:** Different OUs (`Web Services`, `Authentication Department`, `Software Development Department`, `Security Infrastructure`) provide clear separation of duties and make certificate purpose immediately identifiable through inspection. This organizational pattern scales well as the PKI grows.

---

## **Module 4 Part 4 Completion Status**

- Vault server directory structure created with certs/, csr/, private/ subdirectories
- Configuration file created with proper SANs and security infrastructure OU
- ML-DSA-87 private key generated with secure 600 permissions
- Certificate Signing Request created and verified
- Custom extensions file created for signing process
- Certificate signed by Intermediate CA with 2-year validity (serial 1003)
- Certificate extensions verified (SANs, key usage, EKU)
- Certificate chain validated with openssl verify
- CA database updated with new certificate entry
- Complete chain file created and verified (3 certificates)
- Ready for Module 4 Part 5: Certificate Export Formats (PEM, DER, PKCS#12)
 
---
## **Module 4 Part 5: Certificate Export Formats**
**Date:** February 12, 2026
**Project:** Converting all four quantum-resistant end-entity certificates to multiple standard formats for cross-platform compatibility
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, PEM, DER, PKCS#12, PKCS#7 formats

---

## **Objective**
Export all four certificate types (Web Server, User Authentication, Code Signing, and Vault Server) from their native PEM format to DER (binary), PKCS#12 (certificate + private key bundle), and PKCS#7 (certificate chain) formats to ensure compatibility with Windows servers, HSMs, code signing tools, Java keystores, and other enterprise platforms requiring specific certificate formats.

---

## **Step-by-Step Implementation**

### **Part A: Web Server Certificate Exports**

#### **Step 1: Navigate to Web Server Certificate Directory**
**Purpose:** Set correct working directory for web server certificate export operations
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/web_server/
```
**Result:** Working directory confirmed

#### **Step 2: Export Web Server Certificate to DER Format**
**Purpose:** Convert PEM certificate to binary DER format for Windows, Java, and embedded systems
```bash
openssl x509 -in certs/web_server.crt -outform DER -out certs/web_server.der
```
**Result:** Created `certs/web_server.der` (7,700 bytes)

#### **Step 3: Export Web Server Certificate to PKCS#12 Format**
**Purpose:** Create password-protected bundle with certificate and private key for IIS and Windows Certificate Store
```bash
openssl pkcs12 -export -in certs/web_server.crt -inkey private/web_server.key -out certs/web_server.p12 -name "Web Server Certificate - ML-DSA-87" -passout pass:pqclab123
```
**Result:** Created `certs/web_server.p12` (13,384 bytes, permissions 600)

#### **Step 4: Export Web Server Certificate to PKCS#7 Single Format**
**Purpose:** Create PKCS#7 container with certificate only for Windows chain import
```bash
openssl crl2pkcs7 -nocrl -certfile certs/web_server.crt -out certs/web_server.p7b
```
**Result:** Created `certs/web_server.p7b` (10,536 bytes)

#### **Step 5: Export Web Server Certificate Chain to PKCS#7 Format**
**Purpose:** Create PKCS#7 container with full certificate chain (web server + Intermediate CA)
```bash
openssl crl2pkcs7 -nocrl -certfile certs/web_server.crt -certfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt -out certs/web_server-chain.p7b
```
**Result:** Created `certs/web_server-chain.p7b` (20,968 bytes)

---

### **Part B: User Authentication Certificate Exports**

#### **Step 1: Navigate to User Authentication Certificate Directory**
**Purpose:** Set correct working directory for user certificate export operations
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/user_auth/
```
**Result:** Working directory confirmed

#### **Step 2: Export User Authentication Certificate to DER Format**
**Purpose:** Convert PEM certificate to binary DER format for smart cards and mobile devices
```bash
openssl x509 -in certs/user_auth.crt -outform DER -out certs/user_auth.der
```
**Result:** Created `certs/user_auth.der` (7,761 bytes)

#### **Step 3: Export User Authentication Certificate to PKCS#12 Format**
**Purpose:** Create password-protected bundle for browser import, VPN clients, and email signing
```bash
openssl pkcs12 -export -in certs/user_auth.crt -inkey private/user_auth.key -out certs/user_auth.p12 -name "User Authentication Certificate - ML-DSA-87" -passout pass:pqclab123
```
**Result:** Created `certs/user_auth.p12` (13,483 bytes, permissions 600)

#### **Step 4: Export User Authentication Certificate to PKCS#7 Single Format**
**Purpose:** Create PKCS#7 container with certificate only for distribution
```bash
openssl crl2pkcs7 -nocrl -certfile certs/user_auth.crt -out certs/user_auth.p7b
```
**Result:** Created `certs/user_auth.p7b` (10,617 bytes)

#### **Step 5: Export User Authentication Certificate Chain to PKCS#7 Format**
**Purpose:** Create PKCS#7 container with full certificate chain (user cert + Intermediate CA)
```bash
openssl crl2pkcs7 -nocrl -certfile certs/user_auth.crt -certfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt -out certs/user_auth-chain.p7b
```
**Result:** Created `certs/user_auth-chain.p7b` (21,054 bytes)

---

### **Part C: Code Signing Certificate Exports**

#### **Step 1: Navigate to Code Signing Certificate Directory**
**Purpose:** Set correct working directory for code signing certificate export operations
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/code_signing/
```
**Result:** Working directory confirmed

#### **Step 2: Export Code Signing Certificate to DER Format**
**Purpose:** Convert PEM certificate to binary DER format for Windows Authenticode and Java JAR signing
```bash
openssl x509 -in certs/code_signing.crt -outform DER -out certs/code_signing.der
```
**Result:** Created `certs/code_signing.der` (7,768 bytes)

#### **Step 3: Export Code Signing Certificate to PKCS#12 Format**
**Purpose:** Create password-protected bundle for signtool.exe, macOS codesign, and CI/CD pipelines
```bash
openssl pkcs12 -export -in certs/code_signing.crt -inkey private/code_signing.key -out certs/code_signing.p12 -name "Code Signing Certificate - ML-DSA-87" -passout pass:pqclab123
```
**Result:** Created `certs/code_signing.p12` (13,452 bytes, permissions 600)

#### **Step 4: Export Code Signing Certificate to PKCS#7 Single Format**
**Purpose:** Create PKCS#7 container with certificate only for distribution and trust stores
```bash
openssl crl2pkcs7 -nocrl -certfile certs/code_signing.crt -out certs/code_signing.p7b
```
**Result:** Created `certs/code_signing.p7b` (10,625 bytes)

#### **Step 5: Export Code Signing Certificate Chain to PKCS#7 Format**
**Purpose:** Create PKCS#7 container with full certificate chain (code signing cert + Intermediate CA)
```bash
openssl crl2pkcs7 -nocrl -certfile certs/code_signing.crt -certfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt -out certs/code_signing-chain.p7b
```
**Result:** Created `certs/code_signing-chain.p7b` (21,062 bytes)

---

### **Part D: Vault Server Certificate Exports**

#### **Step 1: Navigate to Vault Server Certificate Directory**
**Purpose:** Set correct working directory for vault server certificate export operations
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/04_end_entity_certificates/vault_server/
```
**Result:** Working directory confirmed

#### **Step 2: Export Vault Server Certificate to DER Format**
**Purpose:** Convert PEM certificate to binary DER format for HSM provisioning and Java keystores
```bash
openssl x509 -in certs/vault_server.crt -outform DER -out certs/vault_server.der
```
**Result:** Created `certs/vault_server.der` (7,857 bytes)

#### **Step 3: Export Vault Server Certificate to PKCS#12 Format**
**Purpose:** Create password-protected bundle for HSM loading, disaster recovery, and secure backup
```bash
openssl pkcs12 -export -in certs/vault_server.crt -inkey private/vault_server.key -out certs/vault_server.p12 -name "Vault Server Certificate - ML-DSA-87" -passout pass:pqclab123
```
**Result:** Created `certs/vault_server.p12` (13,548 bytes, permissions 600)

#### **Step 4: Export Vault Server Certificate to PKCS#7 Single Format**
**Purpose:** Create PKCS#7 container with certificate only for client trust configuration
```bash
openssl crl2pkcs7 -nocrl -certfile certs/vault_server.crt -out certs/vault_server.p7b
```
**Result:** Created `certs/vault_server.p7b` (10,747 bytes)

#### **Step 5: Export Vault Server Certificate Chain to PKCS#7 Format**
**Purpose:** Create PKCS#7 container with full certificate chain (vault cert + Intermediate CA)
```bash
openssl crl2pkcs7 -nocrl -certfile certs/vault_server.crt -certfile ../../03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt -out certs/vault_server-chain.p7b
```
**Result:** Created `certs/vault_server-chain.p7b` (21,184 bytes)

---

## **Final File Structure Created**

```
04_end_entity_certificates/
├── web_server/certs/
│   ├── web_server.crt           # PEM format (10,483 bytes)
│   ├── web_server.der           # DER format (7,700 bytes)
│   ├── web_server.p12           # PKCS#12 (13,384 bytes, 600 perms)
│   ├── web_server.p7b           # PKCS#7 single (10,536 bytes)
│   └── web_server-chain.p7b    # PKCS#7 chain (20,968 bytes)
│
├── user_auth/certs/
│   ├── user_auth.crt           # PEM format (10,564 bytes)
│   ├── user_auth.der           # DER format (7,761 bytes)
│   ├── user_auth.p12           # PKCS#12 (13,483 bytes, 600 perms)
│   ├── user_auth.p7b           # PKCS#7 single (10,617 bytes)
│   └── user_auth-chain.p7b    # PKCS#7 chain (21,054 bytes)
│
├── code_signing/certs/
│   ├── code_signing.crt        # PEM format (10,576 bytes)
│   ├── code_signing.der        # DER format (7,768 bytes)
│   ├── code_signing.p12        # PKCS#12 (13,452 bytes, 600 perms)
│   ├── code_signing.p7b        # PKCS#7 single (10,625 bytes)
│   └── code_signing-chain.p7b  # PKCS#7 chain (21,062 bytes)
│
└── vault_server/certs/
    ├── vault_server.crt        # PEM format (10,694 bytes)
    ├── vault_server.der        # DER format (7,857 bytes)
    ├── vault_server.p12        # PKCS#12 (13,548 bytes, 600 perms)
    ├── vault_server.p7b        # PKCS#7 single (10,747 bytes)
    └── vault_server-chain.p7b  # PKCS#7 chain (21,184 bytes)
```

---

## **Key Technical Specifications**

| Format | Extension | Contains Private Key? | File Size (Avg) | Primary Use Case |
|--------|----------|----------------------|-----------------|------------------|
| **PEM** | `.crt` | No | 10.6 KB | Apache, Nginx, Linux, OpenSSL |
| **DER** | `.der` | No | 7.8 KB | Windows, Java, HSMs, embedded systems |
| **PKCS#12** | `.p12` | **Yes** (encrypted) | 13.5 KB | IIS, Windows Cert Store, browsers, code signing |
| **PKCS#7** | `.p7b` | No | 10.6 KB | Certificate distribution, trust stores |
| **PKCS#7 Chain** | `-chain.p7b` | No | 21.1 KB | Full trust chain deployment |

- **PKCS#12 Password:** `pqclab123` (change for production environments)
- **Private Key Protection:** All PKCS#12 files have `-rw-------` (600) permissions
- **DER Size Reduction:** ~26% smaller than PEM (no base64 overhead)
- **Chain File Size:** Approximately double the single certificate size

---

## **Challenges Overcome**

- **Missing PKCS#7 Single Certificate Files:** Initially, `user_auth.p7b` and `code_signing.p7b` were not created during the export process. Resolved by explicitly generating them using the `crl2pkcs7` command with a single `-certfile` parameter.

- **PKCS#7 Verification Command Syntax:** Initial `grep "Subject:"` did not capture output due to exact field name mismatch. Resolved by using `grep -E "subject="` to match OpenSSL's exact output format.

- **Code Signing Chain File Omission:** The `code_signing-chain.p7b` file was accidentally skipped during the initial export run. Detected during final verification and corrected by running the chain export command.

- **Consistent Password Management:** Maintained the same password (`pqclab123`) across all four certificate types for lab consistency, with clear documentation that production environments require unique, strong passwords.

- **Permission Verification:** Confirmed all PKCS#12 files were automatically created with secure 600 permissions, validating OpenSSL's security defaults.

---

## **Practical Insights**

- **DER vs PEM Size Efficiency:** DER format is approximately 26% smaller than PEM (7.8 KB vs 10.6 KB) because it removes base64 encoding (33% overhead) and header/footer lines. This matters for bandwidth-constrained environments, embedded systems, and HSM storage limits.

- **PKCS#12 Encryption Strength:** OpenSSL 3.5.3 automatically uses strong encryption (AES-256-CBC, PBKDF2 with 2048 iterations, SHA-256 PRF) for PKCS#12 containers, replacing legacy RC2/3DES defaults. This provides quantum-appropriate encryption strength for ML-DSA-87 private keys.

- **Chain File Order Significance:** The order of `-certfile` parameters matters. The end-entity certificate must be listed first, followed by the Intermediate CA. OpenSSL preserves this order in the output file, which is critical for proper chain validation.

- **One Certificate, Five Formats:** A single X.509 certificate can be transformed into multiple container formats without modifying the underlying cryptographic material. All formats reference the same ML-DSA-87 public key and identity information.

- **Verification Pattern:** The verification pattern `ls -la certs/ | grep -E "pattern" | sort` proved reliable for confirming all five export formats across all four certificate types, providing a consistent audit mechanism.

- **Git Security Compliance:** All PKCS#12 files were verified to have 600 permissions and are correctly excluded from Git via `.gitignore` rules. This confirms proper security posture for private key material.

---

## **Module 4 Part 5 Completion Status**

- [x] Web server certificate exported to all five formats (PEM, DER, PKCS#12, PKCS#7, PKCS#7-chain)
- [x] User authentication certificate exported to all five formats
- [x] Code signing certificate exported to all five formats
- [x] Vault server certificate exported to all five formats
- [x] All PKCS#12 files verified with correct 600 permissions
- [x] All PKCS#12 passwords tested and confirmed working
- [x] All DER files verified and confirmed readable
- [x] All PKCS#7 single certificate files verified
- [x] All PKCS#7 chain files verified to contain exactly 2 certificates
- [x] Complete documentation added to lab journal
- [>] Ready for Module 5: Certificate Revocation Lists (CRLs)

---

## **Module 5: Certificate Revocation Lists (CRLs)**
**Date:** February 12-13, 2026
**Project:** Implementing post-quantum certificate revocation infrastructure with ML-DSA-87 signed CRLs
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, X.509 CRL v2, RFC 5280

---

## **Objective**
Establish a complete certificate revocation infrastructure for the post-quantum PKI, including revocation of all four end-entity certificates, generation of ML-DSA-87 signed CRLs, and verification of the complete revocation lifecycle.

---

## **Step-by-Step Implementation**

### **Step 1: Create Module 5 Directory Structure**
**Purpose:** Establish organized workspace for CRL operations separate from certificate issuance
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/
mkdir -p 05_certificate_revocation_lists/{crl,crl_database,scripts,openssl_configs}
```
**Result:** Created directory tree with crl/, crl_database/, scripts/, openssl_configs/ subdirectories

---

### **Step 2: Copy Intermediate CA Database for CRL Operations**
**Purpose:** Reuse existing certificate database to maintain continuity of issued certificates
```bash
cp -r 03_fips_quantum_ca_intermediate/intermediate/{index.txt,serial,certs,newcerts} 05_certificate_revocation_lists/crl_database/
```
**Result:** Copied certificate database (index.txt), serial number tracker, and issued certificates directory

---

### **Step 3: Initialize CRL Number File**
**Purpose:** Create CRL sequence number tracker (each CRL gets incrementing number)
```bash
echo "1000" > 05_certificate_revocation_lists/crl_database/crlnumber
```
**Result:** Created crlnumber file with initial value 1000

---

### **Step 4: Create CRL OpenSSL Configuration File**
**Purpose:** Define CRL-specific settings including database paths, validity period, and extensions
```bash
cat > 05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf << 'EOF'
[ ca ]
default_ca = CA_intermediate

[ CA_intermediate ]
dir               = ./crl_database
database          = $dir/index.txt
serial            = $dir/serial
crlnumber         = $dir/crlnumber
certs             = $dir/certs
new_certs_dir     = $dir/newcerts
default_md        = sha512
default_days      = 30
default_crl_days  = 30
policy            = policy_loose
name_opt          = ca_default
cert_opt          = ca_default
copy_extensions   = copy
unique_subject    = no

[ policy_loose ]
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress           = optional

[ crl_ext ]
authorityKeyIdentifier = keyid:always,issuer:always

[ default ]
crl_url                = http://crl.quantum-lab.local/intermediate.crl
EOF
```
**Result:** Created CRL configuration with relative path causing path resolution issues (later fixed)

---

### **Step 5: Fix Intermediate CA Private Key Permissions**
**Purpose:** Secure private key after discovering world-readable permissions (644)
```bash
chmod 600 03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key
```
**Result:** Private key permissions corrected to 600 (owner read/write only)

---

### **Step 6: Fix CRL Configuration Path Resolution**
**Purpose:** Replace relative path with absolute path so OpenSSL can locate database files
```bash
sed -i '9s|dir[[:space:]]*=[[:space:]]*\./crl_database|dir               = /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/05_certificate_revocation_lists/crl_database|' fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf
```
**Result:** Configuration updated with absolute path, verification confirmed line 9 correctly modified

---

### **Step 7: Revoke Web Server Certificate (Serial 1000)**
**Purpose:** First certificate revocation - web server with key compromise reason
```bash
openssl ca -config fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf \
 -name CA_intermediate \
 -keyfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
 -cert fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -revoke fipsqs/04_end_entity_certificates/web_server/certs/web_server.crt \
 -crl_reason keyCompromise
```
**Result:** Database updated - index.txt shows `R` flag, revocation timestamp, reason code

---

### **Step 8: Generate First CRL (Serial 1000 Only)**
**Purpose:** Create initial CRL containing web server certificate
```bash
openssl ca -config fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf \
 -name CA_intermediate \
 -keyfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
 -cert fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -gencrl \
 -out fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem
```
**Result:** Generated CRL with serial 1000, signature algorithm ML-DSA-87, CRL number 1000

---

### **Step 9: Verify First CRL Signature**
**Purpose:** Cryptographically validate CRL was signed by Intermediate CA
```bash
openssl crl -in fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem \
 -CAfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -noout -verify
```
**Result:** `verify OK` - ML-DSA-87 signature valid

---

### **Step 10: Revoke User Authentication Certificate (Serial 1001)**
**Purpose:** Second certificate revocation - user certificate with affiliation change reason
```bash
openssl ca -config fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf \
 -name CA_intermediate \
 -keyfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
 -cert fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -revoke fipsqs/04_end_entity_certificates/user_auth/certs/user_auth.crt \
 -crl_reason affiliationChanged
```
**Result:** Database updated - index.txt shows `R` flag for serial 1001

---

### **Step 11: Generate Updated CRL (Serials 1000, 1001)**
**Purpose:** Create CRL containing both revoked certificates
```bash
openssl ca -config fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf \
 -name CA_intermediate \
 -keyfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
 -cert fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -gencrl \
 -out fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem
```
**Result:** CRL updated with both serials, CRL number incremented to 1001

---

### **Step 12: Revoke Code Signing Certificate (Serial 1002)**
**Purpose:** Third certificate revocation - code signing with superseded reason
```bash
openssl ca -config fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf \
 -name CA_intermediate \
 -keyfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
 -cert fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -revoke fipsqs/04_end_entity_certificates/code_signing/certs/code_signing.crt \
 -crl_reason superseded
```
**Result:** Database updated - index.txt shows `R` flag for serial 1002

---

### **Step 13: Revoke Vault Server Certificate (Serial 1003)**
**Purpose:** Fourth certificate revocation - vault server with cessation of operation reason
```bash
openssl ca -config fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf \
 -name CA_intermediate \
 -keyfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
 -cert fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -revoke fipsqs/04_end_entity_certificates/vault_server/certs/vault_server.crt \
 -crl_reason cessationOfOperation
```
**Result:** Database updated - index.txt shows `R` flag for serial 1003, all four certificates now revoked

---

### **Step 14: Generate Final CRL (All Four Serials: 1000, 1001, 1002, 1003)**
**Purpose:** Create complete CRL containing every revoked certificate issued by Intermediate CA
```bash
openssl ca -config fipsqs/05_certificate_revocation_lists/openssl_configs/openssl-crl.cnf \
 -name CA_intermediate \
 -keyfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
 -cert fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -gencrl \
 -out fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem
```
**Result:** Final CRL generated with all four serials, CRL number 1002, 30-day validity

---

### **Step 15: Verify Final CRL**
**Purpose:** Comprehensive verification of CRL integrity and content
```bash
# Verify signature
openssl crl -in fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem \
 -CAfile fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
 -noout -verify

# Count revoked certificates
openssl crl -in fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem \
 -noout -text | grep "Serial Number" | wc -l

# Check CRL number
openssl crl -in fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem \
 -noout -text | grep "CRL Number"

# Verify signature algorithm
openssl crl -in fipsqs/05_certificate_revocation_lists/crl/intermediate.crl.pem \
 -noout -text | grep "Signature Algorithm" | head -1
```
**Result:**
- `verify OK` - ML-DSA-87 signature valid
- `4` - All four certificates in CRL
- `CRL Number: 1002` - Third CRL generation
- `Signature Algorithm: ML-DSA-87` - Post-quantum signing confirmed

---

## **Final File Structure Created**

```
05_certificate_revocation_lists/
├── crl/
│   └── intermediate.crl.pem           # Final CRL (4 serials, ML-DSA-87 signed)
├── crl_database/
│   ├── index.txt                     # Certificate database (4 revoked, 0 valid)
│   ├── serial                        # Next certificate serial (1004)
│   ├── crlnumber                    # Next CRL number (1003)
│   ├── certs/                       # Issued certificates by serial
│   └── newcerts/                    # Certificate copies
├── openssl_configs/
│   └── openssl-crl.cnf              # CRL configuration (absolute path)
└── scripts/                         # (Empty - for future automation)
```

---

## **Certificate Revocation Architecture**

```
Root CA (ML-DSA-87, offline)
 ↓
Intermediate CA (ML-DSA-87, online, issues certificates & CRLs)
 ↓
Certificate Database (index.txt)
 ├── Serial 1000: Web Server        → R (keyCompromise) [2026-02-13]
 ├── Serial 1001: User Auth         → R (affiliationChanged) [2026-02-13]
 ├── Serial 1002: Code Signing      → R (superseded) [2026-02-13]
 └── Serial 1003: Vault Server      → R (cessationOfOperation) [2026-02-13]
 ↓
CRL Generation (every 30 days)
 └── CRL #1002: Contains serials 1000, 1001, 1002, 1003
     ├── Signature: ML-DSA-87 with SHA512
     ├── Issuer: Intermediate CA
     ├── This Update: Feb 13 00:26:26 2026
     └── Next Update: Mar 15 00:26:26 2026
```

---

## **Key Technical Specifications**

| Component | Value | Significance |
|-----------|-------|--------------|
| **CRL Format** | X.509 CRL v2 | RFC 5280 compliant |
| **Signature Algorithm** | ML-DSA-87 with SHA512 | NIST FIPS 204, Level 5 |
| **CRL Number** | 1002 | Third CRL generated |
| **Revoked Certificates** | 4 | All end-entity certificates |
| **CRL Validity** | 30 days | `default_crl_days = 30` |
| **Next CRL Number** | 1003 | Stored in crlnumber file |
| **CRL File Size** | 2,847 bytes | PEM encoded |
| **Database Status** | 4 R, 0 V | All certificates revoked |

**Revocation Reasons Used:**
- `keyCompromise` - Web Server (most severe)
- `affiliationChanged` - User Authentication
- `superseded` - Code Signing
- `cessationOfOperation` - Vault Server

---

## **Challenges Overcome**

- **Relative Path Resolution Failure:** Initial configuration used `./crl_database` but OpenSSL executed from lab root directory, causing "No such file or directory" error. Resolved by replacing with absolute path using `sed -i` with exact whitespace matching pattern.

- **Configuration Whitespace Mismatch:** First `sed` attempt failed because pattern `dir = \./crl_database` didn't match actual file with 15 spaces. Resolved by using `[[:space:]]*` pattern and targeting specific line number 9 from `grep -n` output.

- **World-Readable Private Key:** Intermediate CA private key had 644 permissions (world-readable). Immediately corrected to 600 using `chmod 600`, confirming secure key storage practice.

- **CRL Number Increment Verification:** Initially unclear if CRL number auto-incremented. Verified by generating three CRLs and checking numbers: 1000 (first), 1001 (second), 1002 (third).

- **Missing Revocation Reasons:** Database entries initially showed no reason codes. Resolved by adding `-crl_reason` flag to revocation commands, confirmed in index.txt as `,keyCompromise`, `,affiliationChanged`, etc.

---

## **Practical Insights**

- **CRL Generation is Incremental:** OpenSSL does not delete previous revocations when generating new CRLs. It reads the entire index.txt and includes ALL revoked certificates. Each new CRL supersedes the previous one.

- **Absolute Paths vs Relative Paths:** OpenSSL resolves paths relative to the current working directory, not the config file location. Absolute paths are more reliable for CA operations but less portable. For this lab, absolute paths were necessary.

- **CRL Number Auto-Increment:** The `crlnumber` file is automatically incremented by OpenSSL each time `-gencrl` is called. Starting at 1000, subsequent CRLs become 1001, 1002, etc. This provides version tracking for clients.

- **Revocation Reasons are Optional but Valuable:** RFC 5280 defines revocation reasons but they are not strictly required. Including them provides audit trail and helps clients determine appropriate response (e.g., keyCompromise vs affiliationChanged).

- **Database Integrity Verification:** The `index.txt` file format uses tab-separated fields with clear semantics. Viewing with `cat -A` reveals tabs as `^I` and line endings as `$`, making it easy to verify correct database updates.

- **Three-Verification Protocol:** Establishing a protocol of verifying (1) index.txt status, (2) CRL content, and (3) CRL signature provides complete confidence in revocation operations. This pattern proved reliable across all four certificates.

---

## **Module 5 Completion Status**

- [x] CRL directory structure created and organized
- [x] Certificate database copied from Intermediate CA
- [x] CRL number file initialized to 1000
- [x] CRL configuration created with proper extensions
- [x] Path resolution issue diagnosed and fixed with absolute path
- [x] Intermediate CA private key permissions secured (600)
- [x] Web Server certificate revoked (serial 1000, keyCompromise)
- [x] First CRL generated and signature verified (ML-DSA-87)
- [x] User Authentication certificate revoked (serial 1001, affiliationChanged)
- [x] Updated CRL generated with 2 revoked serials
- [x] Code Signing certificate revoked (serial 1002, superseded)
- [x] Vault Server certificate revoked (serial 1003, cessationOfOperation)
- [x] Final CRL generated with all 4 revoked serials
- [x] CRL signature verified with openssl crl -verify
- [x] CRL number confirmed at 1002 (three generations)
- [x] All four certificates verified as REVOKED in index.txt
- [x] Complete revocation lifecycle documented
- [>] **Ready for Module 6: Hybrid Certificates**

---
## **Module 6: Hybrid Certificates (RSA-2048 + ML-DSA-87)**
**Date:** February 13, 2026
**Project:** Creating parallel classical and post-quantum certificates with identical identity for hybrid deployment
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, RSA-2048, PKCS#12, X.509 v3

---

## **Objective**
Implement a practical hybrid certificate solution by creating two parallel X.509 certificates with identical subject, SANs, and validity period - one using RSA-2048 (classical compatibility) and one using ML-DSA-87 (quantum resistance) - both signed by the post-quantum Intermediate CA.

---

## **Step-by-Step Implementation**

### **Step 1: Create Module 6 Directory Structure**
**Purpose:** Establish organized workspace for hybrid certificate experiments separate from single-signature certificates
```bash
mkdir -p fipsqs/06_hybrid_certificates/{rsa_hybrid,ecc_hybrid,composite,private,csr,certs,openssl_configs}
```
**Result:** Created root directory + 7 subdirectories (rsa_hybrid/, ecc_hybrid/, composite/, private/, csr/, certs/, openssl_configs/)

---

### **Step 2: Generate RSA-2048 Classical Private Key**
**Purpose:** Create classical key pair for legacy system compatibility layer
```bash
openssl genrsa -out fipsqs/06_hybrid_certificates/private/rsa_hybrid.key 2048
```
**Result:** Created `rsa_hybrid.key` (1,704 bytes) with 600 permissions

---

### **Step 3: Generate ML-DSA-87 Post-Quantum Private Key**
**Purpose:** Create quantum-resistant key pair for NIST Level 5 security layer
```bash
openssl genpkey -algorithm ML-DSA-87 -out fipsqs/06_hybrid_certificates/private/ml_dsa_hybrid.key
```
**Result:** Created `ml_dsa_hybrid.key` (6,774 bytes) with 600 permissions

---

### **Step 4: Create Hybrid Certificate Configuration File**
**Purpose:** Define subject, SANs, key usage, and extensions common to both certificates
```bash
cat > fipsqs/06_hybrid_certificates/openssl_configs/hybrid_rsa_ml_dsa.cnf << 'EOF'
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
req_extensions = v3_req
x509_extensions = v3_req
prompt = no
default_md = sha512

[ req_distinguished_name ]
countryName = US
stateOrProvinceName = Washington
localityName = Seattle
organizationName = PQCLab Security
organizationalUnitName = Hybrid Cryptography Research
commonName = hybrid-lab.pqclab.example.com
emailAddress = hybrid@pqclab.example.com

[ v3_req ]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = hybrid-lab.pqclab.example.com
DNS.2 = pqc-hybrid.lab.local
DNS.3 = rsa-mldsa.test
EOF
```
**Result:** Created `hybrid_rsa_ml_dsa.cnf` (815 bytes) with common identity for both certificates

---

### **Step 5: Generate RSA CSR from Existing Private Key**
**Purpose:** Create Certificate Signing Request for the classical layer using RSA-2048 key
```bash
openssl req -new -key fipsqs/06_hybrid_certificates/private/rsa_hybrid.key -out fipsqs/06_hybrid_certificates/csr/hybrid_rsa.csr -config fipsqs/06_hybrid_certificates/openssl_configs/hybrid_rsa_ml_dsa.cnf
```
**Result:** Created `hybrid_rsa.csr` (1,354 bytes) with Public Key Algorithm: `rsaEncryption`

---

### **Step 6: Sign RSA CSR with Intermediate CA**
**Purpose:** Issue classical layer certificate (serial 1004) with 365-day validity
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/ && openssl ca -config openssl.cnf -days 365 -notext -md sha512 -in /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/csr/hybrid_rsa.csr -out /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/certs/hybrid_rsa.crt && cd -
```
**Result:** Created `hybrid_rsa.crt` (7,367 bytes) - RSA-2048 public key, signed by ML-DSA-87 Intermediate CA, serial 1004

---

### **Step 7: Generate ML-DSA CSR from Existing Private Key**
**Purpose:** Create Certificate Signing Request for the quantum-resistant layer using ML-DSA-87 key
```bash
openssl req -new -key fipsqs/06_hybrid_certificates/private/ml_dsa_hybrid.key -out fipsqs/06_hybrid_certificates/csr/hybrid_ml_dsa.csr -config fipsqs/06_hybrid_certificates/openssl_configs/hybrid_rsa_ml_dsa.cnf
```
**Result:** Created `hybrid_ml_dsa.csr` (10,414 bytes) with Public Key Algorithm: `ML-DSA-87`

---

### **Step 8: Configure Intermediate CA to Allow Duplicate Subjects**
**Purpose:** Modify CA configuration to permit multiple certificates with identical Distinguished Name (required for parallel hybrid certs)
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/ && sed -i '/^\[ CA_intermediate \]/a unique_subject = no' openssl.cnf && cd -
```
**Result:** Added `unique_subject = no` under `[ CA_intermediate ]` section in openssl.cnf

---

### **Step 9: Revoke Original RSA Certificate to Resolve Duplicate Subject Conflict**
**Purpose:** Remove valid certificate with subject DN from database to allow new certificate with same DN
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/ && openssl ca -config openssl.cnf -revoke /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/certs/hybrid_rsa.crt -crl_reason superseded && cd -
```
**Result:** RSA certificate (serial 1004) marked as revoked with reason `superseded`, database updated

---

### **Step 10: Sign ML-DSA CSR with Intermediate CA**
**Purpose:** Issue quantum-resistant layer certificate (serial 1005) with 365-day validity
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/ && openssl ca -config openssl.cnf -days 365 -notext -md sha512 -in /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/csr/hybrid_ml_dsa.csr -out /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/certs/hybrid_ml_dsa.crt && cd -
```
**Result:** Created `hybrid_ml_dsa.crt` (10,511 bytes) - ML-DSA-87 public key, signed by ML-DSA-87 Intermediate CA, serial 1005

---

### **Step 11: Create Full Chain Files for Both Certificates**
**Purpose:** Combine end-entity certificates with Intermediate CA for complete trust paths
```bash
cat /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/certs/hybrid_rsa.crt /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt > /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/certs/hybrid_rsa-chain.crt && cat /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/certs/hybrid_ml_dsa.crt /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt > /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/certs/hybrid_ml_dsa-chain.crt
```
**Result:** Created `hybrid_rsa-chain.crt` and `hybrid_ml_dsa-chain.crt` (11,061 bytes each)

---

### **Step 12: Export Both Certificates to PKCS#12 Format**
**Purpose:** Create password-protected bundles for deployment to Windows, load balancers, and code signing tools
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/06_hybrid_certificates/ && openssl pkcs12 -export -in certs/hybrid_rsa.crt -inkey private/rsa_hybrid.key -out certs/hybrid_rsa.p12 -name "Hybrid RSA Certificate - ML-DSA-87 Signed" -passout pass:pqclab123 && openssl pkcs12 -export -in certs/hybrid_ml_dsa.crt -inkey private/ml_dsa_hybrid.key -out certs/hybrid_ml_dsa.p12 -name "Hybrid ML-DSA-87 Certificate" -passout pass:pqclab123 && cd -
```
**Result:** Created `hybrid_rsa.p12` (7,367 bytes) and `hybrid_ml_dsa.p12` (13,372 bytes) with 600 permissions, password: `pqclab123`

---

### **Step 13: Verify Certificate Chains**
**Purpose:** Confirm both certificates form valid trust paths to Intermediate CA and Root CA
```bash
cd /home/labuser/work/openssl-pqc-stepbystep-lab/fipsqs/ && openssl verify -CAfile 03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt 06_hybrid_certificates/certs/hybrid_rsa.crt && openssl verify -CAfile 03_fips_quantum_ca_intermediate/intermediate/certs/ca-chain.crt 06_hybrid_certificates/certs/hybrid_ml_dsa.crt
```
**Result:** Both certificates returned `OK` - cryptographic signatures valid, chain complete

---

## **Final File Structure Created**

```
06_hybrid_certificates/
├── certs/
│   ├── hybrid_rsa.crt              # RSA certificate (revoked, serial 1004, 7.3KB)
│   ├── hybrid_rsa-chain.crt        # RSA + Intermediate CA chain (11KB)
│   ├── hybrid_rsa.p12              # RSA PKCS#12 bundle (7.3KB, 600 perms)
│   ├── hybrid_ml_dsa.crt           # ML-DSA certificate (valid, serial 1005, 10.5KB)
│   ├── hybrid_ml_dsa-chain.crt     # ML-DSA + Intermediate CA chain (11KB)
│   └── hybrid_ml_dsa.p12           # ML-DSA PKCS#12 bundle (13.3KB, 600 perms)
├── csr/
│   ├── hybrid_rsa.csr             # RSA CSR (1.3KB)
│   └── hybrid_ml_dsa.csr          # ML-DSA CSR (10.4KB)
├── private/
│   ├── rsa_hybrid.key            # RSA-2048 private key (1.7KB, 600 perms)
│   └── ml_dsa_hybrid.key         # ML-DSA-87 private key (6.7KB, 600 perms)
├── openssl_configs/
│   └── hybrid_rsa_ml_dsa.cnf     # Hybrid certificate configuration (815B)
├── rsa_hybrid/                   # (Ready for additional RSA experiments)
├── ecc_hybrid/                   # (Ready for ECC experiments)
└── composite/                    # (Ready for composite cert experiments)
```

---

## **Certificate Chain Architecture**

```
Root CA (ML-DSA-87, offline, 10 years)
    └── Signs: Intermediate CA certificate
         ↓
Intermediate CA (ML-DSA-87, online, 5 years, unique_subject = no)
    ├── Signs (serial 1004): hybrid_rsa.crt (REVOKED - superseded)
    │    └── Public Key: RSA-2048 (classical)
    │    └── Signature: ML-DSA-87 (post-quantum)
    │    └── Chain: hybrid_rsa-chain.crt
    │
    └── Signs (serial 1005): hybrid_ml_dsa.crt (VALID)
         └── Public Key: ML-DSA-87 (post-quantum)
         └── Signature: ML-DSA-87 (post-quantum)
         └── Chain: hybrid_ml_dsa-chain.crt

Both certificates share IDENTICAL subject, SANs, and 365-day validity:
Subject: C=US, ST=Washington, O=PQCLab Security, OU=Hybrid Cryptography Research, CN=hybrid-lab.pqclab.example.com
SANs: hybrid-lab.pqclab.example.com, pqc-hybrid.lab.local, rsa-mldsa.test
```

---

## **Key Technical Specifications**

| **Component** | **Classical Path (Legacy)** | **Post-Quantum Path (PQC)** |
|:--------------|:---------------------------|:---------------------------|
| **Algorithm** | RSA-2048 | ML-DSA-87 (NIST FIPS 204 Level 5) |
| **Private Key Size** | 1.7 KB | 6.7 KB |
| **Certificate Size** | 7.3 KB | 10.5 KB |
| **Serial Number** | 1004 | 1005 |
| **Status** | ⚠️ Revoked (superseded) | ✅ Valid |
| **Validity** | 365 days (Feb 2026 - Feb 2027) | 365 days (Feb 2026 - Feb 2027) |
| **CA Signature** | ML-DSA-87 | ML-DSA-87 |
| **PKCS#12 Password** | `pqclab123` | `pqclab123` |
| **Primary Use Case** | Legacy system compatibility | Quantum-resistant deployment |

---

## **Challenges Overcome**

1. **Duplicate Subject Conflict:** Initial attempt to sign ML-DSA CSR failed because Intermediate CA's `index.txt` already contained a valid certificate with identical Distinguished Name. Resolved by adding `unique_subject = no` to the `[ CA_intermediate ]` section and revoking the original RSA certificate (serial 1004) with reason `superseded`.

2. **Configuration Placement Issue:** The first attempt to add `unique_subject = no` appended it to the end of the file where it was ignored. Resolved by using `sed` to insert the directive directly under the `[ CA_intermediate ]` section header.

3. **Missing Standalone Certificate File:** The ML-DSA certificate was never successfully created due to the duplicate subject error. Resolved by completing the signing process after configuration fix, creating `hybrid_ml_dsa.crt` with serial 1005.

4. **Path Resolution in PKCS#12 Export:** Initial PKCS#12 export failed because the command was executed from the Intermediate CA directory. Resolved by changing to the hybrid certificates root directory and using relative paths.

5. **Revocation Strategy:** Choosing the correct revocation reason (`superseded`) was critical to indicate the RSA certificate is being replaced by a newer certificate (ML-DSA), which is the standard PKI practice for certificate renewal with identical subject.

---

## **Practical Insights**

1. **Parallel Certificates are the Practical Hybrid Solution:** OpenSSL does not support dual-signature X.509 certificates natively. Creating two parallel certificates with identical identity - one classical, one post-quantum - is the production-ready approach for hybrid PKI migration.

2. **`unique_subject = no` is Essential for Hybrid PKI:** By default, OpenSSL CAs enforce unique Distinguished Names. Hybrid certificates require this restriction to be disabled. The directive must be placed **inside the CA section**, not at the file level.

3. **Revocation Enables Replacement:** To issue a new certificate with the same subject as an existing valid certificate, the original must be revoked first. This is not a bug - it's a security feature ensuring clear audit trails for certificate replacement.

4. **RSA Certificates Remain Usable After Revocation:** Revocation marks a certificate as untrusted in the database, but the cryptographic signature remains valid. The revoked RSA certificate can still be used by legacy systems that do not check CRLs, providing a grace period for migration.

5. **PKCS#12 Password Consistency:** Using the same password (`pqclab123`) for both hybrid certificates simplifies deployment and testing. Production environments should use unique, strong passwords per certificate.

6. **Chain Files Simplify Deployment:** Creating combined chain files (`*-chain.crt`) eliminates the need for clients to fetch intermediate certificates separately. This is a best practice for both classical and post-quantum deployments.

---

## **Module 6 Completion Status**

- [x] Module 6 directory structure created with 7 subdirectories
- [x] RSA-2048 private key generated and verified
- [x] ML-DSA-87 private key generated and verified
- [x] Hybrid certificate configuration file created with common identity and SANs
- [x] RSA CSR generated and signed by Intermediate CA (serial 1004)
- [x] ML-DSA CSR generated
- [x] Intermediate CA configured with `unique_subject = no` in correct section
- [x] Original RSA certificate revoked with reason `superseded`
- [x] ML-DSA CSR signed by Intermediate CA (serial 1005)
- [x] Both hybrid certificates verified with `openssl verify` (chain validation OK)
- [x] Full chain files created for both certificates
- [x] Both certificates exported to PKCS#12 format with 600 permissions
- [x] All private keys secured with 600 permissions
- [x] Complete hybrid certificate pair established (RSA-2048 + ML-DSA-87)
- [x] All commands documented with purpose and results
- [>] **Ready for Module 7: OCSP Responder** (real-time revocation checking)

---

## **Module 7: OCSP Responder Implementation**
**Date:** February 14, 2026
**Project:** Setting up real-time certificate revocation checking with Online Certificate Status Protocol (OCSP)
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, OCSP protocol, X.509 v3 extensions

## **Objective**
Implement a production-ready OCSP responder that provides real-time certificate revocation status checking, complementing the CRL infrastructure from Module 5 and enabling faster, more efficient certificate validation for clients.

## **Step-by-Step Implementation**

### **Step 1: Create OCSP Responder Directory Structure**
**Purpose:** Establish organized workspace for OCSP responder files separate from CA infrastructure
```bash
mkdir -p fipsqs/07_ocsp_responder/{ca,requests,responses,logs,scripts,openssl_configs}
tree fipsqs/07_ocsp_responder
```
**Result:** Created main directory with 6 subdirectories: ca/, requests/, responses/, logs/, scripts/, openssl_configs/

---

### **Step 2: Create OCSP Responder Configuration File**
**Purpose:** Define responder settings including database location, CA certificates, network port, and logging
```bash
cat > fipsqs/07_ocsp_responder/openssl_configs/ocsp_responder.cnf << 'EOF'
[OCSP]
database = ../../03_fips_quantum_ca_intermediate/intermediate/index.txt
CAcert = ../../03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt
CAkey = ../../03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key
responder_cert = ./ca/ocsp_signer.crt
responder_key = ./ca/ocsp_signer.key
port = 9080
host = 0.0.0.0
default_status = good
next_update_days = 1
log_file = ../logs/ocsp.log
EOF
```
**Result:** Created configuration with database path, CA certificates, responder certificate paths, and port 9080

---

### **Step 3: Generate OCSP Signing Private Key (ML-DSA-87)**
**Purpose:** Create quantum-resistant private key for signing OCSP responses
```bash
openssl genpkey -algorithm ML-DSA-87 -out fipsqs/07_ocsp_responder/ca/ocsp_signer.key
chmod 600 fipsqs/07_ocsp_responder/ca/ocsp_signer.key
```
**Result:** Generated `ocsp_signer.key` (6,774 bytes) with secure 600 permissions

---

### **Step 4: Create OCSP Signer Certificate Configuration**
**Purpose:** Define certificate extensions for OCSP signing including critical OCSPSigning extended key usage
```bash
cat > fipsqs/07_ocsp_responder/openssl_configs/ocsp_signer.cnf << 'EOF'
[req]
default_bits = 0
default_keyfile = ocsp_signer.key
distinguished_name = req_distinguished_name
req_extensions = req_ext
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
countryName = US
stateOrProvinceName = Washington
localityName = Seattle
organizationName = PQCLab Security
organizationalUnitName = PKI Infrastructure
commonName = OCSP Responder
emailAddress = ocsp@pqclab.example.com

[req_ext]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, OCSPSigning
subjectKeyIdentifier = hash

[v3_req]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, OCSPSigning
subjectKeyIdentifier = hash
EOF
```
**Result:** Created configuration with critical extensions: CA:FALSE, digitalSignature, OCSPSigning

---

### **Step 5: Generate OCSP Signer CSR**
**Purpose:** Create Certificate Signing Request with OCSP Signing extensions
```bash
openssl req -new -key fipsqs/07_ocsp_responder/ca/ocsp_signer.key -out fipsqs/07_ocsp_responder/ca/ocsp_signer.csr -config fipsqs/07_ocsp_responder/openssl_configs/ocsp_signer.cnf
```
**Result:** Created `ocsp_signer.csr` (10,405 bytes) with Public Key Algorithm: ML-DSA-87, Requested Extensions: OCSPSigning

---

### **Step 6: Issue OCSP Signer Certificate from Intermediate CA**
**Purpose:** Have Intermediate CA sign the CSR to create trusted OCSP responder certificate
```bash
cd fipsqs/03_fips_quantum_ca_intermediate/intermediate/
openssl ca -config openssl.cnf -in ../../07_ocsp_responder/ca/ocsp_signer.csr -out ../../07_ocsp_responder/ca/ocsp_signer.crt -extensions v3_req -days 365 -notext -batch -md sha512 -copy_extensions copy
```
**Result:** Created `ocsp_signer.crt` (10,511 bytes) with correct extensions: CA:FALSE, Digital Signature, OCSP Signing

---

### **Step 7: Verify OCSP Signer Certificate Chain**
**Purpose:** Ensure certificate chains properly to Intermediate and Root CA
```bash
cat certs/intermediate_ca.crt ../../02_fips_quantum_ca_root/root/certs/root_ca.crt > ../../07_ocsp_responder/ca/chain.crt
openssl verify -CAfile ../../07_ocsp_responder/ca/chain.crt ../../07_ocsp_responder/ca/ocsp_signer.crt
```
**Result:** `../../07_ocsp_responder/ca/ocsp_signer.crt: OK` - Chain validation successful

---

### **Step 8: Start OCSP Responder Service**
**Purpose:** Launch OCSP responder in background to handle certificate status queries
```bash
openssl ocsp -port 9080 -text -index index.txt -CA certs/intermediate_ca.crt -rkey ../../07_ocsp_responder/ca/ocsp_signer.key -rsigner ../../07_ocsp_responder/ca/ocsp_signer.crt -nrequest 1000 -timeout 30 &
echo $! > ../../07_ocsp_responder/ocsp.pid
```
**Result:** OCSP responder started on port 9080 (PID: 268), waiting for client connections

---

### **Step 9: Test OCSP Responder with Revoked Certificate**
**Purpose:** Verify responder correctly reports revoked certificate status
```bash
openssl ocsp -issuer certs/intermediate_ca.crt -cert ../../04_end_entity_certificates/web_server/certs/web_server.crt -url http://localhost:9080 -resp_text -noverify | grep -E "Cert Status|Reason|Serial Number" -A2
```
**Result:**
```
Cert Status: revoked
Revocation Time: Feb 14 02:12:22 2026 GMT
Revocation Reason: keyCompromise (0x1)
```

---

### **Step 10: Test OCSP Responder with Valid Certificate**
**Purpose:** Verify responder correctly reports valid certificate status
```bash
openssl ocsp -issuer certs/intermediate_ca.crt -cert ../../06_hybrid_certificates/certs/hybrid_ml_dsa.crt -url http://localhost:9080 -resp_text -noverify | grep -E "Cert Status|Serial Number" -A2
```
**Result:**
```
Cert Status: good
Serial Number: 1005
```

---

## **Final File Structure Created**

```
07_ocsp_responder/
├── ca/
│   ├── ocsp_signer.key          # OCSP private key (6.7KB, 600 perms)
│   ├── ocsp_signer.csr          # Certificate Signing Request (10.4KB)
│   ├── ocsp_signer.crt          # OCSP signer certificate (10.5KB)
│   └── chain.crt                # Full chain (Intermediate + Root)
├── logs/
│   └── ocsp.log                 # Responder log file
├── openssl_configs/
│   ├── ocsp_responder.cnf       # Responder configuration
│   └── ocsp_signer.cnf          # Signer certificate configuration
├── requests/                     # (Empty - for OCSP request dumps)
├── responses/                    # (Empty - for OCSP response dumps)
├── scripts/                      # (Empty - for helper scripts)
└── ocsp.pid                      # Process ID file
```

---

## **Certificate Chain Architecture**

```
Root CA (ML-DSA-87, offline, 10 years)
    ↓
Intermediate CA (ML-DSA-87, online, 5 years)
    ↓
OCSP Signer Certificate (ML-DSA-87, 1 year)
    ├── Basic Constraints: CA:FALSE (critical)
    ├── Key Usage: Digital Signature (critical)
    ├── Extended Key Usage: OCSP Signing (critical)
    └── Subject: C=US, ST=Washington, O=PQCLab Security, OU=PKI Infrastructure, CN=OCSP Responder
```

---

## **OCSP Query/Response Flow**

```
Client (openssl ocsp)                OCSP Responder (port 9080)
         │                                      │
         │────── OCSP Request ──────────────────▶│
         │      (Serial 1000)                    │
         │                                        │
         │                                      ├─ Look up serial in index.txt
         │                                      ├─ Found: revoked (keyCompromise)
         │                                      ├─ Sign response with ML-DSA-87
         │                                      │
         │◀───── OCSP Response ──────────────────│
         │      "Cert Status: revoked"           │
         │      "Reason: keyCompromise"          │
```

---

## **Key Technical Specifications**

| Component | Value | Significance |
|-----------|-------|--------------|
| **OCSP Port** | 9080 | Non-privileged port for container environment |
| **Signer Algorithm** | ML-DSA-87 | NIST FIPS 204 Level 5 post-quantum signatures |
| **Responder Certificate** | 365 days | Annual renewal cycle |
| **Index File** | `index.txt` | Certificate database with 6 entries |
| **CRL Status** | CRL#1002 | Complementary revocation mechanism |
| **Response Cache** | 1 day | `next_update_days = 1` |
| **Process ID** | 268 | Running responder process |

---

## **Challenges Overcome**

- **Missing OCSP Signing Extensions:** Initial certificate was issued as CA:TRUE with pathlen:0. Resolved by creating custom extensions file with critical OCSPSigning extended key usage and using `-extfile` parameter during signing.

- **Index.txt Field Count Mismatch:** Revoked certificates (1000-1003) had 5 fields instead of 6, causing parsing errors. Resolved by adding missing tab before "unknown" field using `sed -i '1,4s/unknown /unknown\t/' index.txt`, bringing all lines to consistent 6-field format.

- **Path Resolution in CA Signing:** Intermediate CA couldn't find private key due to relative paths. Resolved by changing to Intermediate CA directory before signing operations, ensuring all relative paths resolved correctly.

- **Certificate Chain Verification:** Initial verification failed because Root CA wasn't included. Resolved by creating chain file with both Intermediate and Root CA certificates for complete trust path.

- **Duplicate Subject Conflict:** Not an issue for OCSP signer, but learned from Module 6 that `unique_subject = no` is critical for parallel certificates with identical DNs.

---

## **Practical Insights**

- **OCSP vs CRL:** OCSP provides real-time revocation status with single-query responses, while CRLs require downloading entire lists. OCSP is more efficient for clients but requires a continuously running responder service.

- **OCSP Signing Certificate Requirements:** Responder certificates must include the `OCSPSigning` extended key usage (OID 1.3.6.1.5.5.7.3.9) and cannot be CA certificates. The `basicConstraints = CA:FALSE` is critical for security.

- **Database Consistency is Critical:** OCSP reads directly from index.txt, not from CRL files. If index.txt is inconsistent with published CRLs, OCSP returns incorrect status. The three-verification protocol (index.txt, CRL content, CRL signature) ensures consistency.

- **Process Management:** Running OCSP responder in background with PID tracking (`echo $! > ocsp.pid`) enables proper process management - stopping, restarting, and monitoring without losing track of the process.

- **Test Both Revoked and Valid:** Always test OCSP with both revoked and valid certificates to verify correct behavior. The responder should return "revoked" with reason for revoked certs, and "good" for valid certs.

- **ML-DSA-87 Performance:** OCSP response signing with ML-DSA-87 adds ~20-60ms latency compared to classical algorithms, but provides quantum-resistant signatures. This is acceptable for most production environments.

---

## **Module 7 Completion Status**

- [x] OCSP responder directory structure created with 6 subdirectories
- [x] OCSP responder configuration file created with database paths and port 9080
- [x] OCSP signer private key generated with ML-DSA-87 (600 permissions)
- [x] OCSP signer certificate configuration created with critical OCSPSigning extension
- [x] OCSP signer CSR generated and verified
- [x] OCSP signer certificate issued by Intermediate CA with correct extensions
- [x] Index.txt field count issue diagnosed and fixed (all lines now 6 fields)
- [x] Certificate chain verified with both Intermediate and Root CA
- [x] OCSP responder started successfully on port 9080 (PID tracked)
- [x] Revoked certificate test (serial 1000) returned "revoked" with reason "keyCompromise"
- [x] Valid certificate test (serial 1005) returned "good"
- [x] Complete OCSP infrastructure operational
- [x] All steps documented with commands and results
- [>] Ready for Module 8: Production Deployment (optional)

---

## **Module 8 Part 1: Local Web Server Deployment with Hybrid Certificate**
**Date:** February 15, 2026
**Project:** Deploying hybrid RSA-2048 + ML-DSA-87 certificate to local OpenSSL test server for browser verification
**Technology:** OpenSSL 3.5.3, ML-DSA-87 algorithm, RSA-2048, Docker container with port mapping

## **Objective**
Successfully deploy a hybrid certificate (RSA-2048 public key with ML-DSA-87 signature) to a local test server and verify it works in a standard web browser, demonstrating practical quantum-safe TLS deployment.

## **Step-by-Step Implementation**

### **Step 1: Check Existing Containers**
**Purpose:** Inventory current Docker containers to understand the environment before starting fresh
```bash
docker ps -a
```
**Result:** Identified one existing container `pqc-container` in Exited state

### **Step 2: Start Fresh Container with Port Mapping**
**Purpose:** Create a new container with port 4443 mapped from container to Windows host for browser access
```bash
docker run -it --rm --name pqc-lab-web -p 4443:4443 -v C:\Users\user\Desktop\PQC\pqc-lab\lab-work\openssl-pqc-stepbystep-lab\:/home/labuser/work/openssl-pqc-stepbystep-lab/ -w /home/labuser/work/openssl-pqc-stepbystep-lab/ pqc-lab:latest /bin/bash
```
**Result:** New container `pqc-lab-web` started with prompt `labuser@afd159d9a7bc:~/work/openssl-pqc-stepbystep-lab$`

### **Step 3: Verify Hybrid Certificate Files**
**Purpose:** Confirm hybrid certificate files are accessible in the new container
```bash
ls -la fipsqs/06_hybrid_certificates/certs/ | grep hybrid
```
**Result:** Verified presence of `hybrid_rsa.crt`, `hybrid_ml_dsa.crt`, and `hybrid_ml_dsa-chain.crt`

### **Step 4: Start OpenSSL Server with RSA Hybrid Certificate**
**Purpose:** Launch test server using the hybrid RSA certificate (RSA public key with ML-DSA-87 signature) that browsers can understand
```bash
openssl s_server -cert fipsqs/06_hybrid_certificates/certs/hybrid_rsa.crt -key fipsqs/06_hybrid_certificates/private/rsa_hybrid.key -accept 4443 -www
```
**Result:** Server started successfully with `ACCEPT` message, waiting for connections

### **Step 5: Access Server from Windows Browser**
**Purpose:** Test browser compatibility by connecting to the running server
```
https://localhost:4443
```
**Result:** Browser displayed security warning (expected), clicked "Advanced" → "Proceed to localhost", OpenSSL status page loaded successfully

### **Step 6: Verify Certificate in Browser**
**Purpose:** Confirm certificate details show ML-DSA-87 signature
```bash
# Viewed certificate details in browser padlock icon
```
**Result:** Certificate viewer showed:
- **Issued By:** Quantum Intermediate CA - ML-DSA-87
- **Organization:** My Quantum Lab
- **Subject:** CN=hybrid-lab.pqclab.example.com, OU=Hybrid Cryptography Research

### **Step 7: Verify Certificate via OpenSSL**
**Purpose:** Cryptographically verify the ML-DSA-87 signature using OpenSSL command line
```bash
openssl x509 -in fipsqs/06_hybrid_certificates/certs/hybrid_rsa.crt -text -noout | grep "Signature Algorithm" -A 2
```
**Result:**
```
Signature Algorithm: ML-DSA-87
Issuer: C=US, ST=Washington, O=My Quantum Lab, OU=Post-Quantum Intermediate CA, CN=Quantum Intermediate CA - ML-DSA-87
```

### **Step 8: Observe Server Activity**
**Purpose:** Monitor server logs to confirm browser connections
```bash
# Server output showed:
# 10 server accepts (SSL_accept())
# 4 server accepts that finished
```
**Result:** Multiple successful TLS 1.3 connections with cipher `TLS_AES_128_GCM_SHA256`

## **Final Deployment Architecture**

```
Windows Host (Browser)
    │
    │ https://localhost:4443
    ▼
Docker Container (pqc-lab-web)
    │
    │ Port Mapping: -p 4443:4443
    ▼
OpenSSL s_server
    ├── Certificate: hybrid_rsa.crt
    │    ├── Public Key: RSA-2048 (browser compatible)
    │    └── Signature: ML-DSA-87 (post-quantum)
    │
    ├── Private Key: rsa_hybrid.key (RSA-2048)
    │
    └── Output: -www status page
         ├── Protocol: TLSv1.3
         ├── Cipher: TLS_AES_128_GCM_SHA256
         └── Server accepts: 10
```

## **Key Technical Specifications**

| Component | Value | Significance |
|-----------|-------|--------------|
| **Certificate Used** | `hybrid_rsa.crt` | RSA-2048 public key with ML-DSA-87 signature |
| **Private Key** | `rsa_hybrid.key` | RSA-2048 (1.7KB, 600 permissions) |
| **Server Command** | `openssl s_server -www` | Built-in test server with status page |
| **Port Mapping** | `-p 4443:4443` | Container-to-host port forwarding |
| **TLS Protocol** | TLSv1.3 | Latest secure protocol |
| **Cipher Suite** | TLS_AES_128_GCM_SHA256 | Strong encryption |
| **Connections** | 10 server accepts | Successful browser connections |
| **Certificate Chain** | Complete | Intermediate CA (ML-DSA-87) → Root CA |

## **Challenges Overcome**

- **Port Already in Use Error:** Initial server start failed because PID 19 was still holding port 4443. Resolved by identifying the process with `ps aux | grep openssl` and terminating it with `kill -9 19`.
- **Missing Networking Tools:** Container lacked `netstat`, `ss`, and `lsof` for port checking. Resolved by using `ps aux` to find and kill the stuck process directly.
- **Browser Compatibility:** Pure ML-DSA certificate caused `ERR_SSL_VERSION_OR_CIPHER_MISMATCH`. Resolved by using hybrid RSA certificate with ML-DSA-87 signature.
- **Multiple Browser Windows:** Needed to keep server terminal open while testing in browser. Resolved by using separate PowerShell windows for container and curl tests.

## **Practical Insights**

- **Hybrid Certificates are Browser-Compatible Today:** RSA public key with ML-DSA-87 signature works in current browsers because the browser sees the RSA key for TLS handshake while the quantum-safe signature provides authentication.
- **Server Must Stay Running:** The OpenSSL `s_server` command blocks the terminal - this is normal. Server activity appears in that window as connections occur.
- **Multiple Ways to Verify:** Browser certificate viewer shows issuer (ML-DSA-87 CA), while OpenSSL command line reveals the actual signature algorithm.
- **Port Mapping is Essential:** Without `-p 4443:4443`, the container is isolated and browsers cannot connect. This is a common Docker networking concept.
- **Process Management Matters:** Stuck processes can block ports. Knowing how to find and kill processes (`ps aux | grep`, `kill -9`) is essential for troubleshooting.

## **Module 8 Part 1 Completion Status**

- [x] Fresh Docker container created with port mapping
- [x] Hybrid RSA certificate verified in container
- [x] OpenSSL test server started successfully
- [x] Browser successfully connected to https://localhost:4443
- [x] Certificate viewer confirmed issuer as ML-DSA-87 Intermediate CA
- [x] OpenSSL command verified ML-DSA-87 signature algorithm
- [x] Server logs showed 10 successful connections
- [x] TLS 1.3 with strong cipher confirmed
- [x] Complete hybrid certificate deployment verified
- [>] Ready for Module 8 Part 2: Cloud VM Deployment (optional)
- [>] Ready for Module 8 Part 3: Code Signing with Hybrid Certificate (optional)
- [>] Ready for Module 8 Part 4: NGINX Configuration (optional)

---

## **Module 8 Part 2: Cloud VM Deployment with Hybrid Certificate**
**Date:** February 17, 2026  
**Project:** Deploying hybrid RSA-2048 + ML-DSA-87 certificate to GitHub Codespaces for browser verification and cloud access  
**Technology:** OpenSSL 3.0.18, ML-DSA-87 algorithm, RSA-2048, OQS Provider, Docker (openquantumsafe/oqs-ossl3), GitHub Codespaces  

## **Objective**
Successfully deploy a hybrid certificate (RSA-2048 public key with ML-DSA-87 signature) to a cloud-based TLS server running in GitHub Codespaces, signed by the ML-DSA-87 Intermediate CA from Module 3, demonstrating practical quantum-safe TLS deployment in a cloud environment. After creation, the certificate files are organized into the repository’s `deployments/cloud-vm-20260217/` folder with clear `cloudvm-` prefixes for future reference and deployment.

## **Step-by-Step Implementation**

### **Step 1: Environment Diagnosis**
**Purpose:** Understand exactly what providers and tools are available before starting  
```bash
openssl version -d
openssl list -providers
find / -name "oqsprovider.so" 2>/dev/null
cat $(openssl version -d | grep -oP '(?<=OPENSSLDIR: ").*(?=")')/openssl.cnf
```
**Result:**  
- OpenSSL 3.0.18 installed via conda at `/opt/conda/ssl`  
- Only the `default` provider active — OQS provider not loaded  
- Two copies of `oqsprovider.so` found:  
  - `/usr/lib/x86_64-linux-gnu/ossl-modules/oqsprovider.so` (system)  
  - `/home/codespace/oqs-provider/build/lib/oqsprovider.so` (home-built)  
- Root cause in `openssl.cnf`: `activate = 1` commented out in `[default_sect]`

### **Step 2: Fix Provider Configuration**
**Purpose:** Create a working OpenSSL config that loads both the default and OQS providers simultaneously  

**File:** `~/pqc-openssl.cnf`  
```ini
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
oqsprovider = oqs_sect

[default_sect]
activate = 1

[oqs_sect]
module = /usr/lib/x86_64-linux-gnu/ossl-modules/oqsprovider.so
activate = 1

[req]
default_bits = 2048
default_md = sha256
distinguished_name = req_distinguished_name
prompt = no

[req_distinguished_name]
C = US
O = PQC Lab
CN = njinhash.cloud-ip.cc
```

**Verification command:**  
```bash
OPENSSL_CONF=~/pqc-openssl.cnf openssl list -providers
```
**Result:** Both `default` and `oqsprovider` listed as active.

### **Step 3: Generate RSA Key and CSR for Cloud VM**
**Purpose:** Create the RSA private key and Certificate Signing Request for the hybrid certificate, using the domain `njinhash.cloud-ip.cc`  
```bash
# RSA key (2048-bit) already existed from earlier work (originally named rsa.key)
# We'll use it as the basis for the cloud VM certificate.

# Create CSR with both providers active
OPENSSL_CONF=~/pqc-openssl.cnf openssl req \
  -new \
  -key fipsqs/06_hybrid_certificates/hybrid-final/rsa.key \
  -out fipsqs/06_hybrid_certificates/hybrid-final/rsa.csr \
  -subj "/CN=njinhash.cloud-ip.cc/O=PQC Lab/C=US"
```
**Result:** CSR created as `rsa.csr` in the temporary `hybrid-final` folder.

### **Step 4: Diagnose CA Key Problem**
**Purpose:** Investigate why the ML-DSA-87 Intermediate CA key from Module 3 couldn't be loaded  

**Error received:**  
```
error:1608010C:STORE routines:ossl_store_handle_load_result:unsupported
```

**Forensic command used:**  
```bash
openssl asn1parse \
  -in fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
  -inform PEM | head -5
```
**Result:**  
```
OBJECT  :2.16.840.1.101.3.4.3.19
```
- OID `2.16.840.1.101.3.4.3.19` = ML-DSA-87 per **NIST FIPS 204 final standard**  
- The installed `oqs-provider 0.12.0-dev` uses older draft OIDs — version mismatch.

### **Step 5: Attempt Provider Rebuild**
**Purpose:** Rebuild oqs-provider from latest source targeting the correct OpenSSL installation  
```bash
cd /home/codespace/oqs-provider
rm -rf build && mkdir build && cd build

cmake .. \
  -DOPENSSL_ROOT_DIR=/opt/conda \
  -DOPENSSL_LIBRARIES=/opt/conda/lib \
  -DOPENSSL_INCLUDE_DIR=/opt/conda/include \
  -GNinja

ninja -j$(nproc)
```
**Result:** Build succeeded, but provider still could not read the key — FIPS 204 final OIDs not registered in this codebase regardless of build flags. Latest available tag was `0.11.0-rc1`, insufficient for FIPS 204 final OID support.

### **Step 6: Deploy Docker Workaround**
**Purpose:** Use the official OQS Docker image which ships full FIPS 204 support baked in  
```bash
docker pull openquantumsafe/oqs-ossl3

# --network host makes container ports appear on Codespace localhost
# Use sh not bash — Alpine Linux image has no bash by default
docker run -it --rm \
  -v /workspaces/pqc-lab:/lab \
  --network host \
  openquantumsafe/oqs-ossl3 sh
```
**Result:** Container running. Immediate test inside container:  
```sh
openssl pkey \
  -in /lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
  -noout -text | head -3
```
```
ML-DSA-87 Private-Key:
seed:
    dd:f8:76:f0:c8:84:c0:c3...
```
CA key readable — FIPS 204 OIDs fully supported in this image.

### **Step 7: Sign CSR with ML-DSA-87 CA**
**Purpose:** Use the Intermediate CA to sign the RSA CSR, producing the hybrid certificate  
```bash
openssl x509 -req \
  -in /lab/fipsqs/06_hybrid_certificates/hybrid-final/rsa.csr \
  -CA /lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
  -CAkey /lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/private/intermediate_ca.key \
  -CAcreateserial \
  -out /lab/fipsqs/06_hybrid_certificates/hybrid-final/hybrid.crt \
  -days 365 \
  -sha256
```
**Result:**  
```
Certificate request self-signature ok
subject=C=US, O=PQC Lab, CN=njinhash.cloud-ip.cc
```

### **Step 8: Build Certificate Chain**
**Purpose:** Create chain file containing both the new hybrid certificate and the Intermediate CA  
```bash
cat /lab/fipsqs/06_hybrid_certificates/hybrid-final/hybrid.crt \
    /lab/fipsqs/03_fips_quantum_ca_intermediate/intermediate/certs/intermediate_ca.crt \
    > /lab/fipsqs/06_hybrid_certificates/hybrid-final/chain.crt
```
**Result:** `chain.crt` created.

### **Step 9: Start TLS Server Inside Docker**
**Purpose:** Launch the OpenSSL test server using the hybrid certificate and RSA key  
```bash
openssl s_server \
  -cert /lab/fipsqs/06_hybrid_certificates/hybrid-final/chain.crt \
  -key /lab/fipsqs/06_hybrid_certificates/hybrid-final/rsa.key \
  -port 4433 \
  -HTTP
```
**Result:** Server started with `ACCEPT` message, waiting for connections.

### **Step 10: Verify Certificate Being Served**
**Purpose:** Confirm the hybrid certificate is correctly served over a live TLS connection  
```bash
openssl s_client -connect localhost:4433 -showcerts 2>&1 | head -20
```
**Result:**  
```
Certificate chain
 0 s:C=US, O=PQC Lab, CN=njinhash.cloud-ip.cc
   i:C=US, ST=Washington, O=My Quantum Lab, CN=Quantum Intermediate CA - ML-DSA-87
   a:PKEY: RSA, 2048 (bit); sigalg: ML-DSA-87
   v:NotBefore: Feb 17 04:23:13 2026 GMT; NotAfter: Feb 17 04:23:13 2027 GMT
```
Hybrid certificate confirmed — RSA 2048-bit key with ML-DSA-87 signature being served.

### **Step 11: Organize Files into Repository Structure**
**Purpose:** Move the created certificate files into the dedicated `deployments/` folder with clear naming for future reference.  
```bash
# On local Windows machine after pulling from GitHub
cd C:\Users\user\Desktop\PQC\pqc-lab\lab-work\openssl-pqc-stepbystep-lab
mkdir -p deployments\cloud-vm-20260217\certificates

# Move and rename files
mv fipsqs\06_hybrid_certificates\hybrid-final\rsa.key deployments\cloud-vm-20260217\certificates\cloudvm-rsa.key
mv fipsqs\06_hybrid_certificates\hybrid-final\rsa.csr deployments\cloud-vm-20260217\certificates\cloudvm-rsa.csr
mv fipsqs\06_hybrid_certificates\hybrid-final\hybrid.crt deployments\cloud-vm-20260217\certificates\cloudvm-hybrid.crt
mv fipsqs\06_hybrid_certificates\hybrid-final\chain.crt deployments\cloud-vm-20260217\certificates\cloudvm-chain.crt

# Remove empty temporary folder
rmdir fipsqs\06_hybrid_certificates\hybrid-final

# Create a README for the deployment
notepad deployments\cloud-vm-20260217\README.md
```
**Result:** All cloud‑VM files are now in `deployments/cloud-vm-20260217/certificates/` with the `cloudvm-` prefix, and a README documents the deployment.

## **Final File Structure Created**

```
deployments/cloud-vm-20260217/
├── certificates/
│   ├── cloudvm-rsa.key      (RSA-2048 private key, gitignored)
│   ├── cloudvm-rsa.csr      (Certificate Signing Request)
│   ├── cloudvm-hybrid.crt   (Signed hybrid certificate)
│   └── cloudvm-chain.crt    (Full chain: hybrid.crt + intermediate_ca.crt)
└── README.md                (Deployment instructions and context)
```

Additionally, the custom OpenSSL configuration remains in the user's home directory:  
`~/pqc-openssl.cnf` – used for future PQC operations.

## **Certificate Chain Architecture**

```
GitHub Codespaces (cloud environment)
    │
    │ port 4433
    ▼
Docker Container (openquantumsafe/oqs-ossl3)
    │ --network host
    ▼
OpenSSL s_server
    ├── Certificate: cloudvm-chain.crt
    │    ├── cloudvm-hybrid.crt
    │    │    ├── Public Key: RSA-2048 (browser compatible)
    │    │    └── Signature: ML-DSA-87 (NIST FIPS 204 final)
    │    └── intermediate_ca.crt (Quantum Intermediate CA - ML-DSA-87)
    │
    ├── Private Key: cloudvm-rsa.key
    │
    └── Verified via s_client:
         ├── sigalg: ML-DSA-87
         ├── PKEY: RSA, 2048 (bit)
         └── Issuer: Quantum Intermediate CA - ML-DSA-87
```

## **Key Technical Specifications**

| Component | Value | Significance |
|-----------|-------|--------------|
| **Certificate Used** | `cloudvm-hybrid.crt` | RSA-2048 public key with ML-DSA-87 signature |
| **Private Key** | `cloudvm-rsa.key` | RSA-2048 (1704 bytes, gitignored) |
| **Signing CA** | `intermediate_ca.key` | ML-DSA-87, OID 2.16.840.1.101.3.4.3.19 |
| **OID Standard** | NIST FIPS 204 final | Permanent standardized OID |
| **Provider Solution** | `openquantumsafe/oqs-ossl3` | Docker image with FIPS 204 support |
| **Server Port** | 4433 | Forwarded via `--network host` |
| **Validity Period** | 365 days | Feb 17 2026 → Feb 17 2027 |
| **Chain Depth** | 2 | Server cert → Intermediate CA |

## **Challenges Overcome**

- **Default Provider Dropped When Loading OQS:** Loading `-provider oqsprovider` alone caused OpenSSL to drop the default provider entirely, breaking file I/O. Root cause: `activate = 1` was commented out in `openssl.cnf`. Resolved by creating `~/pqc-openssl.cnf` with both providers explicitly activated.
- **CA Key OID Mismatch:** Module 3 Intermediate CA key used NIST FIPS 204 final OIDs (`2.16.840.1.101.3.4.3.19`). The installed `oqs-provider 0.12.0-dev` only knows older draft OIDs. Used `openssl asn1parse` to identify the exact OID, then resolved by switching to the `openquantumsafe/oqs-ossl3` Docker image which supports FIPS 204 final OIDs.
- **Provider Rebuild Didn't Fix It:** Rebuilt `oqs-provider` from latest `main` branch targeting conda's OpenSSL — build succeeded but key still unreadable. The FIPS 204 final OIDs are not registered in the codebase regardless of build flags. Docker was the correct solution.
- **Docker Container Has No bash:** The `openquantumsafe/oqs-ossl3` image is Alpine-based and does not include bash. Resolved by using `sh` as the container entrypoint.
- **s_server Rejected Cert on Host:** Running `openssl s_server` directly on the Codespace host produced `ca md too weak` — the host OpenSSL can't verify ML-DSA-87 signatures and rejects the cert. Resolved by running the server inside the Docker container using `--network host` to share the Codespace network stack.
- **Key Share Mismatch with External Clients:** `curl` and Codespace's `openssl s_client` couldn't negotiate a key exchange with the OQS server. Resolved by testing with `openssl s_client` from inside the same OQS-aware Docker container.
- **File Organization for Clarity:** After successful deployment, the certificate files were moved from a temporary location (`hybrid-final`) to a permanent, well‑named folder (`deployments/cloud-vm-20260217/certificates/`) with a `cloudvm-` prefix, making it easy to identify their purpose and deployment date.

## **Practical Insights**

- **OpenSSL 3.x Provider Architecture:** The default provider handles file I/O and standard algorithms. OQS provider only adds post-quantum algorithms. Explicitly loading one provider without the other drops everything not listed — always load both with `activate = 1` in each provider section.
- **OID Forensics with asn1parse:** When a key fails to load with `unsupported`, `openssl asn1parse -in keyfile -inform PEM` decodes the binary structure and reveals the exact OID — allowing diagnosis of the algorithm and standard version used to create it, even if no provider can load the key.
- **FIPS 204 Final vs Draft OIDs:** NIST finalized ML-DSA (FIPS 204) in 2024 with permanent OIDs. Keys created with final OIDs are incompatible with providers that only know draft OIDs. This is an expected compatibility break during the standardization period.
- **Docker as a Compatibility Layer:** When the host toolchain is too old for a cryptographic operation, Docker provides a clean solution — mount files as a volume, perform the incompatible operation inside a container with the right version, and the output persists on the host after the container exits.
- **Hybrid Certificates Work in the Cloud Too:** The same hybrid design from Module 8 Part 1 (RSA public key + ML-DSA-87 signature) works in cloud environments. RSA handles the TLS handshake for compatibility while ML-DSA-87 provides quantum-resistant authentication.
- **--network host is Essential for Codespaces:** Without `--network host`, Docker uses bridge networking and the container's ports are not accessible from the Codespace host's localhost. `--network host` makes the container share the host's network stack directly.
- **Repository Organization Matters:** Moving deployment‑specific files into a `deployments/` folder with date‑stamped subfolders and clear filenames keeps the repository tidy and makes it easy to reuse or reference the certificates later.

## **Module 8 Part 2 Completion Status**

- [x] Codespace environment diagnosed — OpenSSL 3.0.18 via conda
- [x] Provider configuration fixed — both default and OQS providers active
- [x] RSA key and CSR created for `njinhash.cloud-ip.cc`
- [x] CA key OID identified via asn1parse — NIST FIPS 204 final (2.16.840.1.101.3.4.3.19)
- [x] oqs-provider rebuild attempted — confirmed FIPS 204 OIDs not in codebase
- [x] `openquantumsafe/oqs-ossl3` Docker image pulled and verified
- [x] ML-DSA-87 CA key confirmed readable inside Docker container
- [x] CSR signed with ML-DSA-87 Intermediate CA — `hybrid.crt` created
- [x] Certificate chain built — `chain.crt` (hybrid.crt + intermediate_ca.crt)
- [x] OpenSSL `s_server` started in Docker container on port 4433
- [x] `s_client` verified: RSA-2048 key, ML-DSA-87 signature, correct issuer
- [x] Files moved and renamed to `deployments/cloud-vm-20260217/certificates/` with `cloudvm-` prefix
- [x] README added to deployment folder
- [x] All steps documented with commands and results
- [>] Ready for Module 8 Part 3: Code Signing with Hybrid Certificate (optional)
- [>] Ready for Module 8 Part 4: NGINX Configuration (optional)
