"""
LoveProto Identity
==================
Self-generated identity. No certificate authority. No gatekeeper.

Every node generates an Ed25519 keypair. The public key fingerprint IS the identity.
You are your keys. Trust is earned through bonding, not assigned by an authority.
"""
import json
import os
import base64
import hashlib
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat
from cryptography.exceptions import InvalidSignature


def generate_keypair():
    """Generate a new Ed25519 keypair. Returns (private_pem, public_pem)."""
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    priv_pem = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode()
    pub_pem = pub.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode()
    return priv_pem, pub_pem


def fingerprint(public_pem: str) -> str:
    """Short fingerprint of a public key. This is your identity string."""
    raw = hashlib.sha256(public_pem.encode()).digest()
    return base64.b32encode(raw[:16]).decode().rstrip("=").lower()


def load_or_create_identity(store_dir: str, name: str = None):
    """Load identity from disk, or create a new one. Returns Identity object."""
    os.makedirs(store_dir, exist_ok=True)
    priv_path = os.path.join(store_dir, "identity.pem")
    pub_path = os.path.join(store_dir, "identity.pub")

    if os.path.exists(priv_path):
        with open(priv_path) as f:
            priv_pem = f.read()
        with open(pub_path) as f:
            pub_pem = f.read()
    else:
        priv_pem, pub_pem = generate_keypair()
        with open(priv_path, "w") as f:
            f.write(priv_pem)
        os.chmod(priv_path, 0o600)
        with open(pub_path, "w") as f:
            f.write(pub_pem)

    return Identity(priv_pem, pub_pem, name)


class Identity:
    """A node identity. You are your keys."""

    def __init__(self, priv_pem: str, pub_pem: str, name: str = None):
        self.priv_pem = priv_pem
        self.pub_pem = pub_pem
        self.name = name or fingerprint(pub_pem)[:8]
        self.fingerprint = fingerprint(pub_pem)
        self._priv = serialization.load_pem_private_key(priv_pem.encode(), password=None)
        self._pub = self._priv.public_key()

    def sign(self, data: bytes) -> bytes:
        """Sign data with private key."""
        return self._priv.sign(data)

    def verify(self, data: bytes, signature: bytes, their_pub_pem: str) -> bool:
        """Verify a signature from someone else's public key."""
        try:
            their_pub = serialization.load_pem_public_key(their_pub_pem.encode())
            their_pub.verify(signature, data)
            return True
        except (InvalidSignature, Exception):
            return False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "fingerprint": self.fingerprint,
            "public_key": self.pub_pem,
            "created": time.time(),
        }

    def __repr__(self):
        return f"<Identity {self.name} fp={self.fingerprint[:12]}...>"