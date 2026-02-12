# My Post-Quantum Cryptography Lab Journey
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

## **Key Learnings**

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
 **12 steps completed successfully** 
 **Intermediate CA created with ML-DSA-87** 
 **Certificate chain established with Root CA** 
 **All configuration and policy issues resolved** 
 **Ready for production certificate issuance** 
 **Prepared for Module 4: End-entity Certificate Issuance**


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

## **Key Learnings**
1. **End-entity vs CA Certificates:** End-entity certificates have `CA:FALSE` and specific key usages, unlike CAs which have `CA:TRUE`
2. **Subject Alternative Names (SANs):** Modern certificates require SANs for multiple domain/IP coverage
3. **Certificate Purpose Restrictions:** Different certificate types (serverAuth, clientAuth, codeSigning) have specific extension requirements
4. **Signing Workflow:** Must run `openssl ca` from CA directory for config file paths to work correctly
5. **Chain Validation:** OpenSSL can validate entire certificate chain with single command using chain file

## **Module 4 Progress Status**
 **Web server certificate created and signed** 
 **Complete quantum-resistant certificate chain established** 
 **Certificate verification successful with openssl verify** 
 **Organized structure ready for additional certificate types** 
 **Ready to create user authentication certificates** 
 **Ready to create code signing certificates** 
 **Foundation for production PQC deployment complete**


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

## **Key Learnings**
1. **User vs Server Certificates:** User certificates use `clientAuth` extensions and often have email addresses as subjects
2. **Validity Differences:** User certificates typically have shorter validity (90-180 days) vs server certificates (1-2 years)
3. **Extension Flexibility:** When CA config lacks specific extension sections, custom extensions files can override
4. **Path Dependencies:** OpenSSL `ca` command requires execution from CA directory due to relative path configurations
5. **Client Authentication Use Cases:** `clientAuth` enables mutual TLS, VPN authentication, and secure user identification

## **Module 4 Part 2 Completion Status**
 **User authentication certificate created and signed** 
 **Custom extensions file created for clientAuth requirements** 
 **90-day validity period applied (standard for user certs)** 
 **Certificate chain validation successful** 
 **Complete quantum-resistant client authentication solution** 
 **Ready to create code signing certificates** 
 **All end-entity certificate types will be completed** 
 **Production-ready PQC certificate hierarchy established**

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

## **Key Learnings**
1. **Code Signing Specifics:** Code signing certificates have unique requirements with limited key usage
2. **Organizational Structure:** Different departments (Software Development, Authentication) help categorize certificate purposes
3. **Extension Files:** Creating separate extensions files provides flexibility when CA configs lack specific sections
4. **One-Year Validity:** Code signing certificates typically have 1-3 year validity depending on organizational policy
5. **Digital Signature Only:** Code signing only requires `digitalSignature` key usage, unlike server certificates

## **Module 4 Part 3 Completion Status**
 **Code signing certificate created and signed with ML-DSA-87** 
 **Proper extensions applied (codeSigning, digitalSignature)** 
 **One-year validity period applied (standard for code signing)** 
 **Complete certificate chain validated and created** 
 **All three end-entity certificate types now complete** 
 **Module 4 fully completed: Web Server, User Auth, and Code Signing certificates** 
 **Complete quantum-resistant PKI hierarchy established** 
 **Ready for production deployment or Module 5** 

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

[x] Vault server directory structure created with certs/, csr/, private/ subdirectories
[x] Configuration file created with proper SANs and security infrastructure OU
[x] ML-DSA-87 private key generated with secure 600 permissions
[x] Certificate Signing Request created and verified
[x] Custom extensions file created for signing process
[x] Certificate signed by Intermediate CA with 2-year validity (serial 1003)
[x] Certificate extensions verified (SANs, key usage, EKU)
[x] Certificate chain validated with openssl verify
[x] CA database updated with new certificate entry
[x] Complete chain file created and verified (3 certificates)
[ ] Ready for Module 4 Part 5: Certificate Export Formats (PEM, DER, PKCS#12)

---