```markdown
# Uberspace Deployment Notes - February 18, 2026

## Connection Details
- **Host:** klemola.uberspace.de
- **User:** njinhash
- **Port allocated:** 50920
- **Domain:** njinhash.cloud-ip.cc

## Environment Setup

### SSH Connection
```bash
ssh njinhash@klemola.uberspace.de
```

### Allocate Port
```bash
uberspace port add
uberspace port list
# Output: 50920
```

### Create Project Directory
```bash
mkdir -p ~/pqc-lab/certificates
cd ~/pqc-lab
```

## Building the PQC Stack (from source, no root)

### 1. Install CMake locally
```bash
wget https://github.com/Kitware/CMake/releases/download/v3.28.1/cmake-3.28.1-linux-x86_64.tar.gz
tar -xzf cmake-3.28.1-linux-x86_64.tar.gz
mv cmake-3.28.1-linux-x86_64 cmake
rm cmake-3.28.1-linux-x86_64.tar.gz
~/pqc-lab/cmake/bin/cmake --version
```

### 2. Build liboqs
```bash
cd ~/pqc-lab
git clone --depth 1 --branch main https://github.com/open-quantum-safe/liboqs.git
cd liboqs && mkdir build && cd build
~/pqc-lab/cmake/bin/cmake -DCMAKE_INSTALL_PREFIX=~/pqc-lab/oqs-install -DOQS_USE_OPENSSL=OFF ..
make -j2 && make install
```

### 3. Build OpenSSL 3.3.1
```bash
cd ~/pqc-lab
wget https://www.openssl.org/source/openssl-3.3.1.tar.gz
tar xzf openssl-3.3.1.tar.gz
cd openssl-3.3.1
./config --prefix=/home/njinhash/pqc-lab/openssl3 --openssldir=/home/njinhash/pqc-lab/openssl3/ssl
make -j2 && make install
```

### 4. Build oqs-provider
```bash
cd ~/pqc-lab
git clone --depth 1 https://github.com/open-quantum-safe/oqs-provider.git
cd oqs-provider && mkdir build && cd build
~/pqc-lab/cmake/bin/cmake -DOPENSSL_ROOT_DIR=/home/njinhash/pqc-lab/openssl3 -Dliboqs_DIR=/home/njinhash/pqc-lab/oqs-install/lib64/cmake/liboqs ..
make -j2 && make install
```

## Configuration

### Create OpenSSL config with both providers
```bash
mkdir -p ~/pqc-lab/openssl3/ssl
cat > ~/pqc-lab/openssl3/ssl/openssl.cnf << 'EOF'
openssl_conf = openssl_init

[openssl_init]
providers = provider_section

[provider_section]
oqsprovider = oqsprovider_section
default = default_section

[oqsprovider_section]
module = /home/njinhash/pqc-lab/openssl3/lib64/ossl-modules/oqsprovider.so
activate = 1

[default_section]
activate = 1
EOF
```

### Set environment variables
```bash
export LD_LIBRARY_PATH=/home/njinhash/pqc-lab/openssl3/lib64:$LD_LIBRARY_PATH
export OPENSSL_CONF=~/pqc-lab/openssl3/ssl/openssl.cnf
```

### Verify providers are loaded
```bash
~/pqc-lab/openssl3/bin/openssl list -providers
# Should show: default, oqsprovider
```

### Verify ML-DSA-87 support
```bash
~/pqc-lab/openssl3/bin/openssl list -signature-algorithms | grep mldsa87
# Output: mldsa87 @ oqsprovider
```

## Certificate Deployment

### Upload certificates from local machine
```powershell
# From Windows PowerShell
cd C:\Users\user\Desktop\PQC\pqc-lab\lab-work\openssl-pqc-stepbystep-lab\deployments\cloud-vm-20260217\certificates\
scp * njinhash@klemola.uberspace.de:~/pqc-lab/certificates/
```

### Verify certificates on Uberspace
```bash
ls -la ~/pqc-lab/certificates/
~/pqc-lab/openssl3/bin/openssl x509 -in ~/pqc-lab/certificates/cloudvm-hybrid.crt -text -noout | grep "Signature Algorithm"
# Expected: Signature Algorithm: ML-DSA-87
```

## Starting the Server

### Start OpenSSL server with ML-DSA-87 certificate
```bash
cd ~/pqc-lab/certificates
~/pqc-lab/openssl3/bin/openssl s_server -cert cloudvm-hybrid.crt -key cloudvm-rsa.key -cert_chain cloudvm-chain.crt -accept 50920 -www -tls1_3
# Should show: ACCEPT
```

### Test locally (in another SSH session)
```bash
export LD_LIBRARY_PATH=/home/njinhash/pqc-lab/openssl3/lib64:$LD_LIBRARY_PATH
export OPENSSL_CONF=~/pqc-lab/openssl3/ssl/openssl.cnf
~/pqc-lab/openssl3/bin/openssl s_client -connect localhost:50920 -servername njinhash.cloud-ip.cc
```

## Uberspace Configuration

### Add domain to Uberspace
```bash
uberspace web domain add njinhash.cloud-ip.cc
uberspace web domain list
```

### Configure backend (HTTP mode)
```bash
uberspace web backend set / --http --port 50920
uberspace web backend list
# Should show: / http:50920 => OK
```

## DNS Configuration (ClouDNS)
- **A record:** 185.26.156.87
- **AAAA record:** 2a00:d0c0:200:0:b9:1a:9c:56

## Testing & Verification

### Expected s_client output
```
Certificate chain
 0 s:C=US, O=PQC Lab, CN=njinhash.cloud-ip.cc
   i:C=US, ST=Washington, O=My Quantum Lab, CN=Quantum Intermediate CA - ML-DSA-87
   a:PKEY: RSA, 2048 (bit); sigalg: ML-DSA-87
...
Negotiated TLS1.3 group: X25519MLKEM768
```

### Python HTTP server test (diagnostic)
```bash
# Test if Uberspace proxy works with plain HTTP
cat > ~/pqc-lab/serve.py << 'EOF'
#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import time

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = f"""<html>
<head><title>PQC Lab Demo</title></head>
<body>
<h1>✅ Uberspace Proxy Working!</h1>
<p>This page is served by a plain HTTP server on port 50920.</p>
<p>Uberspace's nginx is successfully proxying HTTPS → HTTP.</p>
<hr>
<p><b>Server time:</b> {time.time()}</p>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    def log_message(self, *args):
        pass

print("Starting HTTP server on ALL interfaces (0.0.0.0:50920)...")
HTTPServer(("0.0.0.0", 50920), Handler).serve_forever()
EOF

python3 ~/pqc-lab/serve.py &
```

## Platform Limitation Noted
Uberspace terminates TLS at their edge with Let's Encrypt. The browser shows Let's Encrypt certificate, but the OpenSSL server locally serves the ML-DSA-87 signature correctly. This is a platform limitation, not a failure of the PQC implementation.


```

## Final Status
- ✅ OpenSSL 3.3.1 with oqs-provider built
- ✅ ML-DSA-87 support verified
- ✅ Server running on port 50920
- ✅ Local s_client shows ML-DSA-87 signature
- ✅ Uberspace backend configured (OK)
- ⚠️ Browser shows Let's Encrypt cert (platform limitation)
```