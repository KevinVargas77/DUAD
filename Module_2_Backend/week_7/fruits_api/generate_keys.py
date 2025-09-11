from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pathlib import Path

priv_path = Path("private.pem")
pub_path = Path("public.pem")

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

private_pem = key.private_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PrivateFormat.PKCS8,
	encryption_algorithm=serialization.NoEncryption(),
)
public_pem = key.public_key().public_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

priv_path.write_bytes(private_pem)
pub_path.write_bytes(public_pem)
print(f"Wrote {priv_path} and {pub_path}")
