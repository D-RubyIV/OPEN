from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

# Hypothetical private key (replace with your actual private key)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Get the public key
public_key = private_key.public_key()

# Concatenate data
data_string = "5d3531b362b74a4cb152315161591b2d" + str(1710487869)

# Hashing (recommended for signing)
hasher = hashes.SHA256()
hasher.update(data_string.encode('utf-8'))
digest = hasher.finalize()

# Signing with private key (use your actual private key)
signature = private_key.sign(
    digest,
    hashes.SHA256(),
    padding=rsa.PSS.with_MGF1(hashes.SHA256())
)

# Verification with public key (replace with the recipient's public key)
try:
    public_key.verify(
        signature,
        digest,
        hashes.SHA256(),
        padding=rsa.PSS.with_MGF1(hashes.SHA256())
    )
    print("Signature is valid!")
except Exception:
    print("Signature is invalid!")