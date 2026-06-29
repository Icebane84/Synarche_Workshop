# phoenix_keygen.py
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def generate_node_identity():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    private_hex = private_key.private_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption()
    ).hex()
    
    public_hex = public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    ).hex()
    
    print("========================================")
    print("[+] PHOENIX NODE IDENTITY GENERATED")
    print("========================================")
    print(f"PRIVATE KEY (DO NOT SHARE) : {private_hex}")
    print(f"PUBLIC KEY (ADD TO SERVER) : {public_hex}")
    print("========================================")

if __name__ == "__main__":
    generate_node_identity()