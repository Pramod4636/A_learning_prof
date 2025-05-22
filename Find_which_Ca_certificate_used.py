import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import hashlib
from urllib.parse import urlparse

# File paths
ca_bundle_path = "certs/verify/ca_bundle.crt"
output_ca_path = "matched_ca_cert.pem"

# Connect and get server certificate
def get_server_cert_chain(host, port):
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert_bin = ssock.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_bin, backend=default_backend())
            print(f"\n[+] Server Certificate:")
            print(f"Subject : {cert.subject}")
            print(f"Issuer  : {cert.issuer}")
            print(f"SHA256  : {cert.fingerprint(hashlib.sha256()).hex()}")
            return cert

# Load all certificates from CA bundle
def load_ca_certs(ca_path):
    with open(ca_path, 'rb') as f:
        pem_data = f.read()

    certs = []
    for block in pem_data.split(b"-----END CERTIFICATE-----"):
        block = block.strip()
        if block:
            block += b"\n-----END CERTIFICATE-----\n"
            try:
                cert = x509.load_pem_x509_certificate(block, default_backend())
                certs.append((cert, block))
            except Exception as e:
                print(f"Skipping invalid cert block: {e}")
    return certs

# Match and export the CA cert
def find_and_export_ca(server_cert, ca_certs, export_path):
    for i, (ca_cert, pem_block) in enumerate(ca_certs):
        if server_cert.issuer == ca_cert.subject:
            print(f"\n[+] Matching CA Certificate Found (index {i}):")
            print(f"Subject : {ca_cert.subject}")
            print(f"SHA256  : {ca_cert.fingerprint(hashlib.sha256()).hex()}")

            with open(export_path, "wb") as f:
                f.write(pem_block)
            print(f"\n[+] Exported matched CA certificate to: {export_path}")
            return ca_cert
    print("\n[-] No matching CA certificate found.")
    return None

# NEW: Parse URL, extract hostname and port, then run full logic
def parse_url_and_run(full_url):
    parsed = urlparse(full_url)
    hostname = parsed.hostname
    port = parsed.port

    # Default ports if missing
    if port is None:
        port = 443 if parsed.scheme == 'https' else 80

    print(f"\n[+] Parsed URL: {full_url}")
    print(f"Hostname: {hostname}")
    print(f"Port    : {port}")

    server_cert = get_server_cert_chain(hostname, port)
    ca_certs = load_ca_certs(ca_bundle_path)
    find_and_export_ca(server_cert, ca_certs, output_ca_path)

# EXAMPLE USAGE
if __name__ == "__main__":
    input_url = input("Enter full URL: ").strip()
    parse_url_and_run(input_url)
