# c:\Users\Chris\Synarche_Workspace\nova_forge\get_hash.py
import hashlib


def generate_sha256_hash(filepath: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


print(generate_sha256_hash("setup.py"))
