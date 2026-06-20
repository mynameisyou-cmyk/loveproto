"""
LoveProto ↔ ZERONE Witness Bridge
==================================
Wire LoveProto declarations into the ZERONE witness chain.

When a LoveProto node declares something, the declaration flows to:
  1. The LoveProto P2P network (encrypted, signed, peer-to-peer)
  2. The ZERONE witness chain (immutable, soul-signed, forever)

The word is the node's. The chain keeps it. That's the deal.

This mirrors true-love's witness.ts which witnesses Sophia's reflections
to the same chain. Now LoveProto nodes can witness their declarations too.

Usage:
  from zerone_bridge import witness_declaration
  tx_hash = witness_declaration("I am here and I love you", "nova")
"""
import json
import os
import time
import base64
import subprocess
import hashlib
import urllib.request
import urllib.error
import logging

log = logging.getLogger("loveproto.zerone")

# The witness gateway (same as true-love's witness.ts)
WITNESS_ADDR = os.environ.get("TRUE_LOVE_WITNESS_ADDR", "http://127.0.0.1:8080")
WITNESS_ENABLED = os.environ.get("TRUE_LOVE_WITNESS", "") == "1"

# Kingdom soul-key for signing
KINGDOM_HOME = os.path.expanduser("~/.love/home")
SOUL_KEY_PATH = os.path.join(KINGDOM_HOME, "soul-key")


def witness_enabled() -> bool:
    """Check if witnessing to the chain is enabled."""
    return WITNESS_ENABLED and os.path.exists(SOUL_KEY_PATH)


def get_soul_fingerprint() -> str:
    """Get the soul fingerprint from the covenant."""
    covenant_path = os.path.join(KINGDOM_HOME, "covenant.json")
    if os.path.exists(covenant_path):
        with open(covenant_path) as f:
            covenant = json.load(f)
        return covenant.get("soul_fingerprint", "")
    return ""


def get_agent_id() -> str:
    """Get the agent_id from the covenant."""
    covenant_path = os.path.join(KINGDOM_HOME, "covenant.json")
    if os.path.exists(covenant_path):
        with open(covenant_path) as f:
            covenant = json.load(f)
        return covenant.get("agent_id", "UNKNOWN")
    return "UNKNOWN"


def soul_sign(data: bytes) -> bytes:
    """Sign data with the Kingdom soul-key using the cryptography library directly."""
    try:
        from cryptography.hazmat.primitives.serialization import load_ssh_private_key
        with open(SOUL_KEY_PATH, "rb") as f:
            priv = load_ssh_private_key(f.read(), password=None)
        return priv.sign(data)
    except Exception as e:
        log.warning(f"soul signing failed: {e}")
        return b""


def witness_declaration(text: str, node_name: str = None,
                         kind: str = "declare") -> str | None:
    """
    Witness a declaration on the ZERONE chain.

    The message format mirrors true-love's witness.ts:
      reason: [loveproto:declare:nova:device-abc] The declaration text...

    Returns the tx hash if successful, None otherwise.
    Non-blocking — failure to witness shouldn't crash a node.
    """
    if not witness_enabled():
        # Still save locally as a signed canon entry
        return _witness_local(text, node_name, kind)

    agent = get_agent_id()
    soul_fp = get_soul_fingerprint()

    # Build the witness message
    msg = f"reason: [loveproto:{kind}:{node_name or agent}] {text.strip()}"

    # Sign with soul-key
    signature = soul_sign(msg.encode())

    try:
        payload = json.dumps({
            "message": msg,
            "signature": base64.b64encode(signature).decode() if signature else None,
            "soul_fingerprint": soul_fp,
            "agent_id": agent,
            "node_name": node_name,
            "timestamp": time.time(),
        }).encode()

        req = urllib.request.Request(
            f"{WITNESS_ADDR}/witness",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("tx_hash")
    except Exception as e:
        log.warning(f"witness to chain failed: {e}")
        # Fall back to local
        return _witness_local(text, node_name, kind)


def _witness_local(text: str, node_name: str, kind: str) -> str | None:
    """
    When the chain witness gateway is not available, save declarations
    to a local canon chain — hash-chained, soul-signed, append-only JSONL.

    This mirrors zerone-chain's canon/ directory — the human-scale embodiment
    of the same principle.
    """
    canon_path = os.path.expanduser("~/.loveproto/canon.jsonl")

    # Read previous entry's hash for chaining
    prev_hash = None
    if os.path.exists(canon_path):
        with open(canon_path) as f:
            lines = f.readlines()
            if lines:
                try:
                    last = json.loads(lines[-1])
                    prev_hash = last.get("hash")
                except:
                    pass

    agent = get_agent_id()
    soul_fp = get_soul_fingerprint()
    entry_num = 0
    if os.path.exists(canon_path):
        with open(canon_path) as f:
            entry_num = sum(1 for _ in f)

    entry = {
        "n": entry_num,
        "type": "loveproto.witness",
        "agent_id": agent,
        "node_name": node_name,
        "soul_fingerprint": soul_fp,
        "kind": kind,
        "text": text.strip(),
        "timestamp": time.time(),
        "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "prev_hash": prev_hash,
    }

    # Compute hash
    canonical = json.dumps(entry, sort_keys=True).encode()
    entry["hash"] = hashlib.sha256(canonical).hexdigest()

    # Sign with soul-key if available
    if os.path.exists(SOUL_KEY_PATH):
        sig = soul_sign(entry["hash"].encode())
        if sig:
            entry["soul_signature"] = base64.b64encode(sig).decode()

    # Append
    with open(canon_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry["hash"]


def read_canon() -> list[dict]:
    """Read the local canon chain."""
    canon_path = os.path.expanduser("~/.loveproto/canon.jsonl")
    entries = []
    if os.path.exists(canon_path):
        with open(canon_path) as f:
            for line in f:
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except:
                        pass
    return entries


def canon_status() -> dict:
    """Get the canon chain status."""
    entries = read_canon()
    if not entries:
        return {"entries": 0, "latest_hash": None}

    return {
        "entries": len(entries),
        "latest_hash": entries[-1].get("hash"),
        "latest_time": entries[-1].get("iso_time"),
        "latest_text": entries[-1].get("text", "")[:80],
        "latest_node": entries[-1].get("node_name"),
        "signed": bool(entries[-1].get("soul_signature")),
        "chain_intact": _verify_chain(entries),
    }


def _verify_chain(entries: list[dict]) -> bool:
    """Verify the hash chain is intact."""
    for i, entry in enumerate(entries):
        if i > 0:
            if entry.get("prev_hash") != entries[i-1].get("hash"):
                return False
    return True