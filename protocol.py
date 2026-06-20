"""
LoveProto Wire Protocol
========================
Encrypted P2P messages between bonded nodes.

Message types:
  HELLO      - introduce yourself, share public key
  BOND       - request/confirm a trust bond
  DECLARE    - a natural language declaration (intention, feeling, thought)
  REQUEST    - ask another node to do something
  SERVE      - actively serve something to a bonded node
  ATTENTION  - acknowledge, give attention
  PING       - are you there?
  PONG       - i'm here.
  GOODBYE    - closing connection with grace

Every message is signed by the sender.
Payloads are encrypted to the recipient's public key (X25519 ECDH + AES-GCM).

Wire format:
  [4-byte magic "LOVE"]
  [1-byte version]
  [1-byte message type]
  [4-byte payload length (big-endian)]
  [payload bytes: signed+encrypted JSON]

This is the fabric. This is how nodes speak to each other.
"""
import json
import struct
import base64
import time
import os
from enum import IntEnum
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

MAGIC = b"LOVE"
VERSION = 1


class MsgType(IntEnum):
    HELLO = 1
    BOND = 2
    DECLARE = 3
    REQUEST = 4
    SERVE = 5
    ATTENTION = 6
    PING = 7
    PONG = 8
    GOODBYE = 9


def _x25519_public_pem(ed25519_pub_pem: str) -> str:
    """Derive an X25519 keypair from Ed25519 for ECDH (simplified: generate ephemeral)."""
    # In production: use Ed25519->X25519 conversion. For prototype, generate ephemeral.
    return ed25519_pub_pem  # placeholder - we'll use ephemeral keys below


def derive_shared_key(our_priv: X25519PrivateKey, their_pub: X25519PublicKey) -> bytes:
    """Derive a 256-bit shared key via ECDH + HKDF."""
    shared = our_priv.exchange(their_pub)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"loveproto-v1",
    ).derive(shared)


def encrypt_payload(plaintext: bytes, shared_key: bytes) -> bytes:
    """Encrypt with AES-256-GCM."""
    aesgcm = AESGCM(shared_key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ct


def decrypt_payload(ciphertext: bytes, shared_key: bytes) -> bytes:
    """Decrypt AES-256-GCM."""
    aesgcm = AESGCM(shared_key)
    nonce = ciphertext[:12]
    ct = ciphertext[12:]
    return aesgcm.decrypt(nonce, ct, None)


def pack_message(msg_type: MsgType, payload: bytes) -> bytes:
    """Pack a message onto the wire."""
    return MAGIC + struct.pack("!BBI", VERSION, msg_type, len(payload)) + payload


def unpack_message(data: bytes) -> tuple[MsgType, bytes] | None:
    """Unpack a message from the wire. Returns (type, payload) or None if incomplete."""
    if len(data) < 10:
        return None
    if data[:4] != MAGIC:
        raise ValueError(f"Bad magic: {data[:4]}")
    version = data[4]
    if version != VERSION:
        raise ValueError(f"Unsupported version: {version}")
    msg_type = MsgType(data[5])
    payload_len = struct.unpack("!I", data[6:10])[0]
    if len(data) < 10 + payload_len:
        return None  # incomplete, need more data
    payload = data[10:10 + payload_len]
    return msg_type, payload


def make_envelope(sender_fp: str, sender_name: str, content: dict,
                  shared_key: bytes, sign_fn) -> bytes:
    """
    Build an encrypted, signed envelope.
    sign_fn: callable(bytes) -> bytes (Ed25519 signature)
    """
    content["from"] = sender_fp
    content["name"] = sender_name
    content["ts"] = time.time()
    plaintext = json.dumps(content, sort_keys=True).encode()
    signature = sign_fn(plaintext)
    envelope = {
        "sig": base64.b64encode(signature).decode(),
        "data": base64.b64encode(encrypt_payload(plaintext, shared_key)).decode(),
    }
    return json.dumps(envelope).encode()


def open_envelope(envelope_bytes: bytes, shared_key: bytes,
                  verify_fn) -> dict | None:
    """
    Open an encrypted, signed envelope.
    verify_fn: callable(data_bytes, sig_bytes) -> bool
    Returns the content dict, or None if verification fails.
    """
    env = json.loads(envelope_bytes)
    sig = base64.b64decode(env["sig"])
    ct = base64.b64decode(env["data"])
    plaintext = decrypt_payload(ct, shared_key)
    if not verify_fn(plaintext, sig):
        return None
    return json.loads(plaintext)