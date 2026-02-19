#!/usr/bin/env python3
"""
OCSP Responder with REAL ML-DSA-87 Signing - FINAL WORKING VERSION
Module 7 PQC Lab - Simplified but Functional
"""

import os
import sys
import socket
import ctypes
import base64
import hashlib
from datetime import datetime, timezone
from ctypes import c_uint8, c_size_t, c_int, c_void_p, c_char_p, POINTER, byref
from typing import Optional, Tuple, Dict

# ============================================================================
# CONFIGURATION
# ============================================================================

OQS_DLL = r"C:\oqs-build\oqs-provider\build\lib\oqsprovider.dll"
MINGW_BIN = r"C:\Ruby33-x64\msys64\mingw64\bin"
INDEX_TXT = r"C:\Users\user\Desktop\PQC\pqc-lab\lab-work\openssl-pqc-stepbystep-lab\fipsqs\03_fips_quantum_ca_intermediate\intermediate\index.txt"
CA_KEY = r"C:\Users\user\Desktop\PQC\pqc-lab\lab-work\openssl-pqc-stepbystep-lab\fipsqs\03_fips_quantum_ca_intermediate\intermediate\private\intermediate_ca.key"
HOST = "127.0.0.1"
PORT = 2560

# ============================================================================
# ML-DSA-87 SIGNER
# ============================================================================

class MLDSA87Signer:
    """Handles ML-DSA-87 signing using oqsprovider"""
    
    def __init__(self):
        self.oqs = None
        self.key_bytes = None
        self._load_dlls()
        self._extract_key()
        self._setup_functions()
        print("[✓] ML-DSA-87 Signer initialized")
    
    def _load_dlls(self):
        """Load libcrypto and oqsprovider"""
        os.environ["PATH"] = MINGW_BIN + os.pathsep + os.environ.get("PATH", "")
        crypto_dll = os.path.join(MINGW_BIN, "libcrypto-3-x64.dll")
        ctypes.CDLL(crypto_dll)
        self.oqs = ctypes.CDLL(OQS_DLL)
    
    def _extract_key(self):
        """Extract raw ML-DSA-87 private key from PEM"""
        with open(CA_KEY, 'rb') as f:
            pem_data = f.read()
        
        lines = pem_data.split(b'\n')
        der_b64 = b''.join([l for l in lines if l and not l.startswith(b'-----')])
        der_data = base64.b64decode(der_b64)
        
        key_start = der_data.find(b'\x04\x82\x13\x20')
        if key_start > 0:
            self.key_bytes = der_data[key_start+4:key_start+4+4896]
            print(f"[✓] Extracted {len(self.key_bytes)}-byte ML-DSA-87 key")
        else:
            raise Exception("Could not find ML-DSA-87 key")
    
    def _setup_functions(self):
        """Setup OQS API function signatures"""
        self.OQS_SIG_new = self.oqs.OQS_SIG_new
        self.OQS_SIG_new.restype = c_void_p
        self.OQS_SIG_new.argtypes = [c_char_p]
        
        self.OQS_SIG_free = self.oqs.OQS_SIG_free
        self.OQS_SIG_free.restype = None
        self.OQS_SIG_free.argtypes = [c_void_p]
        
        self.OQS_SIG_sign = self.oqs.OQS_SIG_sign
        self.OQS_SIG_sign.restype = c_int
        self.OQS_SIG_sign.argtypes = [c_void_p, POINTER(c_uint8), POINTER(c_size_t),
                                      POINTER(c_uint8), c_size_t, POINTER(c_uint8)]
    
    def sign(self, message: bytes) -> bytes:
        """Sign a message with ML-DSA-87"""
        method_name = b"ML-DSA-87"
        sig_obj = self.OQS_SIG_new(method_name)
        if not sig_obj:
            raise Exception("Failed to create ML-DSA-87 signer")
        
        try:
            msg_buf = (c_uint8 * len(message)).from_buffer_copy(message)
            key_buf = (c_uint8 * len(self.key_bytes)).from_buffer_copy(self.key_bytes)
            
            sig_len = c_size_t(4627)
            sig_buf = (c_uint8 * 4627)()
            
            result = self.OQS_SIG_sign(sig_obj, sig_buf, byref(sig_len),
                                       msg_buf, len(message), key_buf)
            
            if result != 0:
                raise Exception(f"Signing failed with code {result}")
            
            return bytes(sig_buf)[:sig_len.value]
            
        finally:
            self.OQS_SIG_free(sig_obj)
    
    def cleanup(self):
        """Free resources"""
        pass

# ============================================================================
# CERTIFICATE DATABASE
# ============================================================================

class CertificateDatabase:
    """Parse and query index.txt for certificate status"""
    
    def __init__(self, index_path: str):
        self.index_path = index_path
        self.certs = {}
        self._load()
    
    def _load(self):
        """Load index.txt and parse certificate entries"""
        with open(self.index_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) >= 6:
                    status = parts[0]
                    revocation_field = parts[2] if len(parts) > 2 else ""
                    
                    if ',' in revocation_field:
                        revocation_date, revocation_reason = revocation_field.split(',', 1)
                    else:
                        revocation_date = revocation_field
                        revocation_reason = ""
                    
                    serial_raw = parts[3] if len(parts) > 3 else ""
                    
                    if serial_raw and serial_raw != "unknown":
                        self.certs[serial_raw] = {
                            'status': status,
                            'revocation_reason': revocation_reason,
                            'revocation_date': revocation_date
                        }
    
    def get_status(self, serial_str: str) -> Tuple[str, Optional[str]]:
        """Get certificate status"""
        cert = self.certs.get(serial_str.strip())
        
        if not cert:
            return ('unknown', None)
        
        if cert['status'] == 'V':
            return ('good', None)
        elif cert['status'] == 'R':
            reason_map = {
                'keyCompromise': 'Key Compromise',
                'affiliationChanged': 'Affiliation Changed',
                'superseded': 'Superseded',
                'cessationOfOperation': 'Cessation of Operation'
            }
            return ('revoked', reason_map.get(cert['revocation_reason'], 'Unspecified'))
        else:
            return ('unknown', None)

# ============================================================================
# OCSP RESPONDER
# ============================================================================

class OCSPResponder:
    """OCSP responder with ML-DSA-87 signing"""
    
    def __init__(self, db: CertificateDatabase, signer: MLDSA87Signer):
        self.db = db
        self.signer = signer
        self.running = False
        self.socket = None
    
    def build_response(self, serial: str, status: str, reason: Optional[str]) -> Tuple[str, bytes]:
        """Build response message and sign it"""
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%SZ')
        
        if status == 'good':
            msg = f"OCSP|{serial}|GOOD|{timestamp}"
            status_text = "GOOD"
        elif status == 'revoked':
            msg = f"OCSP|{serial}|REVOKED|{reason}|{timestamp}"
            status_text = f"REVOKED ({reason})"
        else:
            msg = f"OCSP|{serial}|UNKNOWN|{timestamp}"
            status_text = "UNKNOWN"
        
        signature = self.signer.sign(msg.encode())
        
        response = f"""╔═══════════════════════════════════════════════════════════╗
║  OCSP Response - ML-DSA-87 Quantum-Safe Signature        ║
╠═══════════════════════════════════════════════════════════╣
║  Serial:     {serial}
║  Status:     {status_text}
║  Timestamp:  {timestamp}
║  Signed:     ML-DSA-87 (4627 bytes)
║  Signature:  {signature.hex()[:64]}...
║  Hash:       {hashlib.sha256(signature).hexdigest()[:32]}...
╚═══════════════════════════════════════════════════════════╝"""
        
        return response, signature
    
    def handle_client(self, client_socket, address):
        """Handle a single client connection"""
        try:
            data = client_socket.recv(1024)
            if not data:  # ✅ FIXED LINE
                return
            
            print(f"\n[+] Request from {address[0]}:{address[1]}")
            
            request_text = data.decode('utf-8').strip()
            print(f"[*] Request: {request_text}")
            
            if request_text.startswith('serial='):
                serial = request_text.split('=')[1]
            else:
                serial = "1005"
            
            print(f"[*] Serial: {serial}")
            
            status, reason = self.db.get_status(serial)
            print(f"[*] Status: {status.upper()}")
            
            response, signature = self.build_response(serial, status, reason)
            print(f"[✓] Signed with ML-DSA-87 ({len(signature)} bytes)")
            
            client_socket.send(response.encode())
            print(f"[✓] Response sent")
            
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client_socket.close()
    
    def start(self):
        """Start the OCSP responder server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket.bind((HOST, PORT))
            self.socket.listen(5)
            self.running = True
            
            print(f"\n{'='*70}")
            print(f"🚀 OCSP Responder - ML-DSA-87 Quantum-Safe")
            print(f"{'='*70}")
            print(f"📡 Listening: {HOST}:{PORT}")
            print(f"📋 Certificates: {len(self.db.certs)}")
            print(f"🔐 Signing: ML-DSA-87 (4627-byte signatures)")
            print(f"{'='*70}\n")
            
            while self.running:
                try:
                    client, addr = self.socket.accept()
                    self.handle_client(client, addr)
                except KeyboardInterrupt:
                    print("\n[!] Shutting down...")
                    self.running = False
                    break
                    
        except Exception as e:
            print(f"[!] Server error: {e}")
        finally:
            if self.socket:
                self.socket.close()
            print("[✓] Server stopped")

# ============================================================================
# TEST CLIENT
# ============================================================================

def test_client(serial="1005"):
    """Test client to query the OCSP responder"""
    print(f"\n🔍 Testing serial {serial}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        request = f"serial={serial}"
        print(f"[*] Sending: {request}")
        sock.send(request.encode())
        
        response = sock.recv(4096)
        print(f"[✓] Response received ({len(response)} bytes)")
        print("\n" + response.decode())
        
        sock.close()
        
    except Exception as e:
        print(f"[!] Client error: {e}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n🔐 PQC Lab - Module 7: ML-DSA-87 OCSP Responder")
    print("=" * 70)
    
    print("[*] Initializing ML-DSA-87 signer...")
    try:
        signer = MLDSA87Signer()
    except Exception as e:
        print(f"[✗] Failed: {e}")
        return
    
    print("[*] Loading certificate database...")
    db = CertificateDatabase(INDEX_TXT)
    print(f"[✓] Loaded {len(db.certs)} certificates")
    
    print("\n🧪 Pre-Testing:")
    for s in ["1000", "1001", "1002", "1003", "1004"]:
        status, reason = db.get_status(s)
        print(f"  {s}: {status.upper()} {f'({reason})' if reason else ''}")
    
    print("\n🔧 Options:")
    print("  1. Start OCSP responder")
    print("  2. Test client")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        responder = OCSPResponder(db, signer)
        responder.start()
    elif choice == "2":
        serial = input("Enter serial (default: 1004): ").strip() or "1004"
        test_client(serial)
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()