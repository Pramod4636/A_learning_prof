from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timezone

# === Path to your .p12 or .pfx file ===
p12_path = "certs/client.p12"
p12_password = b"your_password_here"  # must be bytes, can be None if no password

# === Load the PKCS#12 file ===
with open(p12_path, "rb") as f:
    p12_data = f.read()

private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
    p12_data, p12_password, backend=default_backend()
)

# === Check certificate validity ===
if certificate:
    not_before = certificate.not_valid_before.replace(tzinfo=timezone.utc)
    not_after = certificate.not_valid_after.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    print(f"Issuer: {certificate.issuer.rfc4514_string()}")
    print(f"Subject: {certificate.subject.rfc4514_string()}")
    print(f"Valid From: {not_before}")
    print(f"Valid To:   {not_after}")

    if not_before <= now <= not_after:
        print("✅ Certificate is currently VALID")
    else:
        print("❌ Certificate is NOT valid (expired or not yet active)")
else:
    print("❌ No certificate found in the .p12 file")
