#!/usr/bin/env python3
"""
PQC CRL Generator v2 - Uses oqsprovider.dll directly via ctypes
Bypasses OpenSSL STORE entirely. Calls OQS_SIG_ml_dsa_87_sign directly.
"""

import ctypes
import ctypes.util
import os
import sys
import base64
from datetime import datetime, timezone, timedelta
from asn1crypto import pem as asn1_pem, core as asn1core, x509 as asn1x509

# ── CONFIGURATION ────────────────────────────────────────────────────────────
BASE_DIR    = r"C:\Users\user\Desktop\PQC\pqc-lab\lab-work\openssl-pqc-stepbystep-lab\fipsqs\03_fips_quantum_ca_intermediate\intermediate"
INDEX_FILE  = os.path.join(BASE_DIR, "index.txt")
KEY_FILE    = os.path.join(BASE_DIR, "private", "intermediate_ca.key")
CERT_FILE   = os.path.join(BASE_DIR, "certs", "intermediate_ca.crt")
OUTPUT_CRL  = os.path.join(BASE_DIR, "intermediate.crl.pem")
OQS_DLL     = r"C:\Ruby33-x64\msys64\mingw64\lib\ossl-modules\oqsprovider.dll"

# ML-DSA-87 parameters (from FIPS 204)
MLDSA87_SK_LEN  = 4896   # secret key bytes
MLDSA87_SIG_LEN = 4627   # max signature bytes
MLDSA87_OID     = "2.16.840.1.101.3.4.3.18"

CRL_DAYS = 30
# ─────────────────────────────────────────────────────────────────────────────

def load_oqs_dll():
    """Load oqsprovider.dll and set up ML-DSA-87 sign function."""
    print(f"[*] Loading OQS DLL: {OQS_DLL}")
    try:
        mingw_bin = r"C:\Ruby33-x64\msys64\mingw64\bin"
        os.environ["PATH"] = mingw_bin + os.pathsep + os.environ.get("PATH", "")
        # Pre-load libcrypto so oqsprovider can find its dependency
        libcrypto_path = os.path.join(mingw_bin, "libcrypto-3-x64.dll")
        ctypes.CDLL(libcrypto_path)
        print(f"[*] libcrypto pre-loaded")
        lib = ctypes.CDLL(OQS_DLL)
        print(f"[✓] DLL loaded successfully")
        return lib
    except OSError as e:
        print(f"[!] Failed to load DLL: {e}")
        raise

def setup_sign_function(lib):
    """Configure OQS_SIG_ml_dsa_87_sign ctypes signature."""
    # int OQS_SIG_ml_dsa_87_sign(
    #     uint8_t *sig, size_t *siglen,
    #     const uint8_t *msg, size_t msglen,
    #     const uint8_t *sk
    # )
    fn = lib.OQS_SIG_ml_dsa_87_sign
    fn.restype  = ctypes.c_int
    fn.argtypes = [
        ctypes.POINTER(ctypes.c_uint8),   # sig output buffer
        ctypes.POINTER(ctypes.c_size_t),  # siglen (in/out)
        ctypes.POINTER(ctypes.c_uint8),   # message
        ctypes.c_size_t,                  # message length
        ctypes.POINTER(ctypes.c_uint8),   # secret key
    ]
    return fn

def extract_private_key_bytes(key_file):
    """
    Extract raw ML-DSA-87 secret key bytes from PKCS#8 PEM file.
    
    PKCS#8 structure:
      SEQUENCE {
        INTEGER 0                    (version)
        SEQUENCE { OID mldsa87 }     (algorithmIdentifier)
        OCTET STRING {               (privateKey)
          SEQUENCE {
            OCTET STRING <32-byte seed>
            OCTET STRING <4864-byte expanded key>  <- this is the full SK
          }
        }
      }
    
    liboqs expects the full expanded secret key (4896 bytes).
    """
    print(f"[*] Extracting private key from: {key_file}")
    
    with open(key_file, "rb") as f:
        key_data = f.read()
    
    # Decode PEM
    if b"BEGIN" in key_data:
        _, _, der = asn1_pem.unarmor(key_data)
    else:
        der = key_data
    
    # Scan DER directly for the 4896-byte ML-DSA-87 secret key
    # oqsprovider encodes it as OCTET STRING: 04 82 13 20 <4896 bytes>
    print(f"[*] Scanning DER for {MLDSA87_SK_LEN}-byte key material...")
    
    # Try OCTET STRING with 3-byte length: 04 82 13 20 (4896 = 0x1320)
    target = bytes([0x04, 0x82, 0x13, 0x20])
    idx = der.find(target)
    if idx != -1:
        candidate = der[idx + 4: idx + 4 + MLDSA87_SK_LEN]
        if len(candidate) == MLDSA87_SK_LEN:
            print(f"[*] Found SK at DER offset {idx}")
            return candidate

    # Try seed+expanded pattern:
    # seed = 04 20 <32 bytes>, expanded = 04 82 13 00 <4864 bytes>
    target2 = bytes([0x04, 0x82, 0x13, 0x00])
    idx2 = der.find(target2)
    if idx2 != -1:
        chunk = der[max(0, idx2-40):idx2]
        seed_pos = chunk.rfind(bytes([0x04, 0x20]))
        if seed_pos != -1:
            abs_seed = max(0, idx2-40) + seed_pos
            seed = der[abs_seed + 2: abs_seed + 34]
            expanded = der[idx2 + 4: idx2 + 4 + 4864]
            full_sk = seed + expanded
            if len(full_sk) == MLDSA87_SK_LEN:
                print(f"[*] Assembled SK from seed+expanded ({len(full_sk)} bytes)")
                return full_sk

    # Debug output
    print(f"[!] DER length: {len(der)} bytes, first bytes: {der[:20].hex()}")
    octet_strs = []
    i = 0
    while i < len(der) - 4:
        if der[i] == 0x04 and der[i+1] == 0x82:
            length = (der[i+2] << 8) | der[i+3]
            if length > 100:
                octet_strs.append((i, length))
        i += 1
    print(f"[!] Large OCTET STRINGs: {octet_strs}")
    raise ValueError(f"Could not find {MLDSA87_SK_LEN}-byte ML-DSA-87 secret key in key file")

def sign_tbs(lib, tbs_der, sk_bytes):
    """Sign TBS bytes using OQS_SIG_ml_dsa_87_sign via ctypes."""
    sign_fn = setup_sign_function(lib)
    
    sig_buf = (ctypes.c_uint8 * MLDSA87_SIG_LEN)()
    sig_len = ctypes.c_size_t(MLDSA87_SIG_LEN)
    
    msg_buf = (ctypes.c_uint8 * len(tbs_der))(*tbs_der)
    sk_buf  = (ctypes.c_uint8 * len(sk_bytes))(*sk_bytes)
    
    print(f"[*] Calling OQS_SIG_ml_dsa_87_sign ({len(tbs_der)} byte TBS, {len(sk_bytes)} byte SK)...")
    rc = sign_fn(sig_buf, ctypes.byref(sig_len), msg_buf, len(tbs_der), sk_buf)
    
    if rc != 0:
        raise RuntimeError(f"OQS_SIG_ml_dsa_87_sign failed with return code {rc}")
    
    actual_len = sig_len.value
    signature = bytes(sig_buf[:actual_len])
    print(f"[✓] Signature generated: {actual_len} bytes")
    return signature

def parse_index(index_path):
    """Parse OpenSSL CA index.txt, return list of revoked entries."""
    reason_map = {
        "unspecified": 0, "keyCompromise": 1, "cACompromise": 2,
        "affiliationChanged": 3, "superseded": 4, "cessationOfOperation": 5,
        "certificateHold": 6, "removeFromCRL": 8, "privilegeWithdrawn": 9,
        "aACompromise": 10,
    }
    revoked = []
    with open(index_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 6 or parts[0] != "R":
                continue
            rev_field = parts[2]
            if "," in rev_field:
                rev_date_str, reason_str = rev_field.split(",", 1)
            else:
                rev_date_str, reason_str = rev_field, "unspecified"
            serial_hex = parts[3]
            try:
                rev_time = datetime.strptime(rev_date_str, "%y%m%d%H%M%SZ").replace(tzinfo=timezone.utc)
            except ValueError:
                rev_time = datetime.strptime(rev_date_str, "%Y%m%d%H%M%SZ").replace(tzinfo=timezone.utc)
            revoked.append({
                "serial": int(serial_hex, 16),
                "revocation_time": rev_time,
                "reason": reason_str.strip(),
                "reason_int": reason_map.get(reason_str.strip(), 0),
            })
    return revoked

# ── DER helpers ──────────────────────────────────────────────────────────────
def encode_oid_bytes(oid_str):
    parts = [int(x) for x in oid_str.split(".")]
    first = parts[0] * 40 + parts[1]
    body = bytearray()
    for p in [first] + parts[2:]:
        if p == 0:
            body.append(0)
        else:
            enc = []
            while p:
                enc.append(p & 0x7f)
                p >>= 7
            enc.reverse()
            for i, b in enumerate(enc):
                body.append(b | (0x80 if i < len(enc) - 1 else 0))
    return bytes(body)

def der_len(n):
    if n < 0x80:   return bytes([n])
    if n < 0x100:  return bytes([0x81, n])
    if n < 0x10000: return bytes([0x82, n >> 8, n & 0xff])
    return bytes([0x83, n >> 16, (n >> 8) & 0xff, n & 0xff])

def tag(t, content):   return bytes([t]) + der_len(len(content)) + content
def seq(c):            return tag(0x30, c)
def oid(s):            return tag(0x06, encode_oid_bytes(s))
def integer(n):
    if n == 0: return tag(0x02, b"\x00")
    b = n.to_bytes((n.bit_length() + 8) // 8, "big").lstrip(b"\x00")
    if b[0] & 0x80: b = b"\x00" + b
    return tag(0x02, b)
def octet_str(b):      return tag(0x04, b)
def bit_str(b):        return tag(0x03, b"\x00" + b)
def enumerated(n):     return tag(0x0a, bytes([n]))
def gentime(dt):       return tag(0x18, dt.strftime("%Y%m%d%H%M%SZ").encode())
def explicit(n, c):    return tag(0xa0 | n, c)
def boolean_true():    return tag(0x01, b"\xff")

def make_extension(extn_oid, critical, value_der):
    parts = oid(extn_oid)
    if critical:
        parts += boolean_true()
    parts += octet_str(value_der)
    return seq(parts)

def build_tbs_crl(issuer_cert_path, revoked_list, now, next_update, crl_num):
    """Build TBSCertList DER."""
    # Load issuer cert
    with open(issuer_cert_path, "rb") as f:
        cert_data = f.read()
    if b"BEGIN" in cert_data:
        _, _, cert_der = asn1_pem.unarmor(cert_data)
    else:
        cert_der = cert_data

    cert = asn1x509.Certificate.load(cert_der)
    issuer_der = cert["tbs_certificate"]["subject"].dump()

    # Get Subject Key Identifier for AKI
    ski_bytes = None
    try:
        for ext in cert["tbs_certificate"]["extensions"]:
            if ext["extn_id"].native == "subject_key_identifier":
                ski_hex = ext["extn_value"].parsed.native
                if isinstance(ski_hex, str):
                    ski_bytes = bytes.fromhex(ski_hex.replace(":", "").replace(" ", ""))
                else:
                    ski_bytes = bytes(ski_hex)
    except Exception:
        pass

    # AlgorithmIdentifier for ML-DSA-87
    alg_id = seq(oid(MLDSA87_OID))

    # Build revoked certificates block
    rev_items = b""
    for r in revoked_list:
        reason_ext = make_extension("2.5.29.21", False, enumerated(r["reason_int"]))
        rc = seq(
            integer(r["serial"]) +
            gentime(r["revocation_time"]) +
            seq(reason_ext)
        )
        rev_items += rc
    revoked_block = tag(0x30, rev_items)

    # Extensions
    crl_num_ext = make_extension("2.5.29.20", False, integer(crl_num))
    if ski_bytes:
        aki_value = seq(tag(0x80, ski_bytes))
        aki_ext = make_extension("2.5.29.35", False, aki_value)
        exts_content = crl_num_ext + aki_ext
    else:
        exts_content = crl_num_ext
    extensions = explicit(0, seq(exts_content))

    # TBSCertList
    tbs_content = (
        alg_id +
        issuer_der +
        gentime(now) +
        gentime(next_update) +
        revoked_block +
        extensions
    )
    return seq(tbs_content), alg_id

def der_to_pem(der_bytes, label="X509 CRL"):
    b64 = base64.encodebytes(der_bytes).decode()
    return f"-----BEGIN {label}-----\n{b64}-----END {label}-----\n"

def main():
    print("=" * 60)
    print("  PQC CRL Generator v2 — Direct liboqs ctypes signing")
    print("=" * 60)
    print()

    # Verify files
    for path, label in [(INDEX_FILE,"index.txt"), (KEY_FILE,"private key"), (CERT_FILE,"issuer cert"), (OQS_DLL,"oqsprovider.dll")]:
        if not os.path.exists(path):
            print(f"[!] ERROR: {label} not found: {path}")
            sys.exit(1)
        print(f"[✓] Found {label}")
    print()

    # Load DLL
    lib = load_oqs_dll()
    print()

    # Parse index
    print("[*] Parsing index.txt...")
    revoked = parse_index(INDEX_FILE)
    print(f"[*] Found {len(revoked)} revoked certificates:")
    for r in revoked:
        print(f"    Serial {r['serial']:04X} ({r['serial']}) — {r['reason']} — {r['revocation_time'].strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    # Timestamps
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    next_update = now + timedelta(days=CRL_DAYS)
    print(f"[*] This Update: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"[*] Next Update: {next_update.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # CRL number
    crl_number_file = os.path.join(BASE_DIR, "crlnumber")
    crl_num = 1
    if os.path.exists(crl_number_file):
        with open(crl_number_file) as f:
            crl_num = int(f.read().strip(), 16)
    print(f"[*] CRL Number: {crl_num}")
    print()

    # Extract private key
    sk_bytes = extract_private_key_bytes(KEY_FILE)
    print()

    # Build TBS
    print("[*] Building TBSCertList...")
    tbs_der, alg_id = build_tbs_crl(CERT_FILE, revoked, now, next_update, crl_num)
    print(f"[*] TBSCertList: {len(tbs_der)} bytes")
    print()

    # Sign
    signature = sign_tbs(lib, tbs_der, sk_bytes)
    print()

    # Assemble CRL
    print("[*] Assembling CRL...")
    crl_der = seq(tbs_der + alg_id + bit_str(signature))
    crl_pem = der_to_pem(crl_der)

    with open(OUTPUT_CRL, "w") as f:
        f.write(crl_pem)
    print(f"[✓] CRL written to: {OUTPUT_CRL}")
    print(f"[*] CRL size: {len(crl_der)} bytes")
    print()

    # Increment CRL number
    with open(crl_number_file, "w") as f:
        f.write(f"{crl_num + 1:02X}\n")
    print(f"[*] CRL number incremented to {crl_num + 1}")
    print()

    # Quick verify — check PEM structure at least
    print("[*] Verifying output PEM structure...")
    with open(OUTPUT_CRL) as f:
        content = f.read()
    if "BEGIN X509 CRL" in content and "END X509 CRL" in content:
        print("[✓] PEM structure valid")
    print()
    print("=" * 60)
    print("  DONE! Copy intermediate.crl.pem to your Docker container")
    print("  and verify with:")
    print("  openssl crl -in intermediate.crl.pem -text -noout")
    print("=" * 60)

if __name__ == "__main__":
    main()
