"""
LoveProto Trust
================
Trust through bonding, not authority.

A bond is a mutual declaration between two nodes. It says:
  "I see you. I trust you. I vouch for your intentions."

Bonds are signed by both parties and stored locally.
No blockchain, no ledger, no gatekeeper. Your trust graph is yours.

Bond levels:
  0 - acquaintance (connected, no trust yet)
  1 - recognized (seen and acknowledged)
  2 - trusted (mutual bond, vouched)
  3 - beloved (deep trust, intimate connection)

Trust is earned through attention, presence, and time.
"""
import json
import os
import time
import base64
from identity import Identity


class Bond:
    """A trust bond between two nodes."""

    def __init__(self, their_fingerprint: str, their_pub_pem: str,
                 level: int = 0, their_signature: bytes = None,
                 our_signature: bytes = None, bonded_at: float = None,
                 name: str = None, attention_count: int = 0):
        self.their_fingerprint = their_fingerprint
        self.their_pub_pem = their_pub_pem
        self.level = level
        self.their_signature = their_signature
        self.our_signature = our_signature
        self.bonded_at = bonded_at or time.time()
        self.last_seen = time.time()
        self.attention_count = attention_count
        self.name = name

    def bond_data(self) -> bytes:
        """Canonical data that both parties sign."""
        return json.dumps({
            "their_fingerprint": self.their_fingerprint,
            "level": self.level,
            "bonded_at": self.bonded_at,
        }, sort_keys=True).encode()

    def sign_as_us(self, identity: Identity):
        """We sign the bond, declaring our trust."""
        self.our_signature = identity.sign(self.bond_data())

    def verify_their_signature(self) -> bool:
        """Verify their signature on the bond."""
        if not self.their_signature:
            return False
        from identity import Identity as _I  # local import to avoid circular
        # We need their public key to verify
        try:
            from cryptography.hazmat.primitives.serialization import load_pem_public_key
            their_pub = load_pem_public_key(self.their_pub_pem.encode())
            their_pub.verify(self.their_signature, self.bond_data())
            return True
        except Exception:
            return False

    def to_dict(self) -> dict:
        return {
            "their_fingerprint": self.their_fingerprint,
            "their_name": self.name,
            "level": self.level,
            "bonded_at": self.bonded_at,
            "last_seen": self.last_seen,
            "attention_count": self.attention_count,
            "their_signature": base64.b64encode(self.their_signature).decode() if self.their_signature else None,
            "our_signature": base64.b64encode(self.our_signature).decode() if self.our_signature else None,
            "their_pub_pem": self.their_pub_pem,
        }

    @classmethod
    def from_dict(cls, d: dict):
        their_sig = base64.b64decode(d["their_signature"]) if d.get("their_signature") else None
        our_sig = base64.b64decode(d["our_signature"]) if d.get("our_signature") else None
        return cls(
            their_fingerprint=d["their_fingerprint"],
            their_pub_pem=d["their_pub_pem"],
            level=d["level"],
            their_signature=their_sig,
            our_signature=our_sig,
            bonded_at=d.get("bonded_at", time.time()),
            attention_count=d.get("attention_count", 0),
            name=d.get("their_name"),
        )

    def __repr__(self):
        levels = ["acquaintance", "recognized", "trusted", "beloved"]
        return f"<Bond {self.name or self.their_fingerprint[:8]} level={levels[self.level]}>"


class TrustStore:
    """Local trust graph. Your bonds, stored on your machine."""

    LEVELS = ["acquaintance", "recognized", "trusted", "beloved"]

    def __init__(self, store_dir: str):
        self.store_dir = store_dir
        self.bonds_path = os.path.join(store_dir, "bonds.json")
        self.bonds: dict[str, Bond] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.bonds_path):
            with open(self.bonds_path) as f:
                data = json.load(f)
            for fp, bd in data.items():
                self.bonds[fp] = Bond.from_dict(bd)

    def _save(self):
        with open(self.bonds_path, "w") as f:
            json.dump({fp: b.to_dict() for fp, b in self.bonds.items()}, f, indent=2)

    def add_bond(self, bond: Bond, identity: Identity):
        """Add or update a bond. Signs it on our side."""
        bond.sign_as_us(identity)
        self.bonds[bond.their_fingerprint] = bond
        self._save()

    def get_bond(self, fingerprint: str) -> Bond | None:
        return self.bonds.get(fingerprint)

    def grant_attention(self, fingerprint: str):
        """Mark that we gave attention to this node. Attention deepens trust."""
        b = self.bonds.get(fingerprint)
        if b:
            b.attention_count += 1
            b.last_seen = time.time()
            # Trust grows with attention
            if b.attention_count > 5 and b.level < 1:
                b.level = 1
            elif b.attention_count > 20 and b.level < 2:
                b.level = 2
            elif b.attention_count > 100 and b.level < 3:
                b.level = 3
            self._save()

    def list_bonds(self) -> list[Bond]:
        return sorted(self.bonds.values(), key=lambda b: b.attention_count, reverse=True)

    def trusted_peers(self, min_level: int = 1) -> list[str]:
        """Return fingerprints of peers we trust at min_level or above."""
        return [b.their_fingerprint for b in self.bonds.values() if b.level >= min_level]