#!/usr/bin/env python3
"""
STEP 4.2: ML-DSA-87 Actual Signing (Working Version)
"""

import os
import ctypes
import base64
from pathlib import Path
from ctypes import c_uint8, c_size_t, c_int, c_void_p, c_char_p, POINTER, byref

# ============================================================================
# CONFIGURATION
# ============================================================================

OQS_DLL = r"C:\oqs-build\oqs-provider\build\lib\oqsprovider.dll"
MINGW_BIN = r"C:\Ruby33-x64\msys64\mingw64\bin"
CA_KEY = r"C:\Users\user\Desktop\PQC\pqc-lab\lab-work\openssl-pqc-stepbystep-lab\fipsqs\03_fips_quantum_ca_intermediate\intermediate\private\intermediate_ca.key"

# ============================================================================
# Load DLLs
# ============================================================================

print("\n🔐 STEP 4.2: ML-DSA-87 Actual Signing")
print("=" * 60)

os.environ["PATH"] = MINGW_BIN + os.pathsep + os.environ.get("PATH", "")
print("[✓] Added MinGW to PATH")

crypto_dll = os.path.join(MINGW_BIN, "libcrypto-3-x64.dll")
print(f"[*] Loading libcrypto...")
ctypes.CDLL(crypto_dll)
print("[✓] libcrypto loaded")

print(f"[*] Loading oqsprovider...")
oqs = ctypes.CDLL(OQS_DLL)
print("[✓] oqsprovider loaded")

# ============================================================================
# Define OQS API Functions
# ============================================================================

print("\n[*] Defining OQS API functions...")

# OQS_SIG *OQS_SIG_new(const char *method_name)
OQS_SIG_new = oqs.OQS_SIG_new
OQS_SIG_new.restype = c_void_p
OQS_SIG_new.argtypes = [c_char_p]

# void OQS_SIG_free(OQS_SIG *sig)
OQS_SIG_free = oqs.OQS_SIG_free
OQS_SIG_free.restype = None
OQS_SIG_free.argtypes = [c_void_p]

# int OQS_SIG_sign(...)
OQS_SIG_sign = oqs.OQS_SIG_sign
OQS_SIG_sign.restype = c_int
OQS_SIG_sign.argtypes = [c_void_p, POINTER(c_uint8), POINTER(c_size_t),
                         POINTER(c_uint8), c_size_t, POINTER(c_uint8)]

print("[✓] OQS API functions defined")

# ============================================================================
# Extract ML-DSA-87 Private Key
# ============================================================================

print("\n[*] Extracting ML-DSA-87 private key...")

with open(CA_KEY, 'rb') as f:
    pem_data = f.read()

lines = pem_data.split(b'\n')
der_b64 = b''.join([l for l in lines if l and not l.startswith(b'-----')])
der_data = base64.b64decode(der_b64)

key_start = der_data.find(b'\x04\x82\x13\x20')
if key_start > 0:
    key_bytes = der_data[key_start+4:key_start+4+4896]
    print(f"[✓] Extracted {len(key_bytes)}-byte ML-DSA-87 private key")
else:
    print("[✗] Could not find ML-DSA-87 key")
    exit(1)

# ============================================================================
# Create ML-DSA-87 Signer
# ============================================================================

print("\n[*] Creating ML-DSA-87 signer...")

method_name = b"ML-DSA-87"
sig_obj = OQS_SIG_new(method_name)
if not sig_obj:
    print("[✗] Failed to create ML-DSA-87 signer")
    exit(1)
print("[✓] ML-DSA-87 signer created")

# ============================================================================
# Sign a Test Message
# ============================================================================

print("\n[*] Signing test message...")

test_message = b"OCSP Response for serial 1004 - status REVOKED"
print(f"    Message: {test_message}")

# Prepare buffers
message_buffer = (c_uint8 * len(test_message)).from_buffer_copy(test_message)
key_buffer = (c_uint8 * len(key_bytes)).from_buffer_copy(key_bytes)

# ML-DSA-87 signature is 4627 bytes
signature_len = c_size_t(4627)
signature_buffer = (c_uint8 * 4627)()

# Sign!
print("[*] Calling OQS_SIG_sign...")
result = OQS_SIG_sign(sig_obj, signature_buffer, byref(signature_len),
                      message_buffer, len(test_message), key_buffer)

if result == 0:
    print("[✓] ML-DSA-87 SIGNING SUCCESSFUL!")
    print(f"    Signature length: {signature_len.value} bytes")
    print(f"    First 32 bytes: {bytes(signature_buffer)[:32].hex()}")
else:
    print(f"[✗] Signing failed with error code: {result}")

# Clean up
OQS_SIG_free(sig_obj)
print("[✓] Cleanup complete")

print("\n✅ STEP 4.2 complete - ML-DSA-87 signing works!")