from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

def load_certificate(path):
    with open(path, 'rb') as f:
        cert_data = f.read()
    return x509.load_pem_x509_certificate(cert_data, default_backend())

def load_private_key(path):
    with open(path, 'rb') as f:
        key_data = f.read()
    return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())

def check_cert_expiration(cert, name):
    not_before = cert.not_valid_before
    not_after = cert.not_valid_after
    print(f"{name} validity: {not_before} to {not_after}")

def check_cert_and_key_match(cert, private_key):
    public_key_cert = cert.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_key = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    if public_key_cert == public_key_key:
        print("Client certificate and private key match.")
    else:
        print("ERROR: Client certificate and private key do NOT match.")

# Paths to files
client_cert_path = "certs/certs_client/client_cert.pem"
client_key_path = "certs/certs_client/client_key.pem"
ca_bundle_path = "certs/verify/ca_bundle.crt"

# Check client certificate
try:
    client_cert = load_certificate(client_cert_path)
    print("Client certificate loaded successfully.")
    check_cert_expiration(client_cert, "Client certificate")
except Exception as e:
    print(f"Error loading client certificate: {e}")

# Check private key
try:
    client_key = load_private_key(client_key_path)
    print("Client private key loaded successfully.")
except Exception as e:
    print(f"Error loading client private key: {e}")

# Check certificate and key match
try:
    check_cert_and_key_match(client_cert, client_key)
except Exception as e:
    print(f"Error checking cert and key match: {e}")

# Check CA bundle (each cert in bundle)
try:
    with open(ca_bundle_path, 'rb') as f:
        ca_data = f.read()

    certs = ca_data.strip().split(b'-----END CERTIFICATE-----')
    for i, cert_blob in enumerate(certs):
        if cert_blob.strip():
            cert_blob += b'-----END CERTIFICATE-----\n'
            cert = x509.load_pem_x509_certificate(cert_blob, default_backend())
            print(f"CA Certificate {i+1} loaded successfully.")
            check_cert_expiration(cert, f"CA certificate {i+1}")
except Exception as e:
    print(f"Error loading CA bundle: {e}")
