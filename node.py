"""
LoveProto Node
==============
A running node on the LoveProto network.

A node:
  - listens for incoming connections
  - connects to known peers
  - exchanges HELLO to establish identity
  - forms BONDS to build trust
  - sends DECLARE messages (natural language)
  - responds to REQUEST with SERVE
  - gives ATTENTION to bonded peers
  - encrypts everything end-to-end

This is the living fabric. Each node is a point of presence.
"""
import asyncio
import json
import os
import time
import base64
import logging
from identity import Identity, load_or_create_identity, fingerprint
from trust import TrustStore, Bond
from protocol import (
    MsgType, pack_message, unpack_message,
    make_envelope, open_envelope, encrypt_payload, decrypt_payload,
    derive_shared_key, MAGIC, VERSION
)
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key

log = logging.getLogger("loveproto")


class PeerSession:
    """An active connection with another node."""

    def __init__(self, node, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.node = node
        self.reader = reader
        self.writer = writer
        self.peer_fp = None
        self.peer_name = None
        self.peer_pub_pem = None
        self.shared_key = None
        self.ephemeral_priv = X25519PrivateKey.generate()
        self.authenticated = False
        self._buf = b""

    def addr(self):
        peer = self.writer.get_extra_info("peername")
        return f"{peer[0]}:{peer[1]}" if peer else "?"

    async def send_raw(self, data: bytes):
        self.writer.write(data)
        await self.writer.drain()

    async def send_msg(self, msg_type: MsgType, content: dict):
        """Send an encrypted, signed message."""
        if self.shared_key is None:
            # HELLO is special - includes ephemeral key, not encrypted
            if msg_type == MsgType.HELLO:
                pub_bytes = self.ephemeral_priv.public_key().public_bytes(
                    Encoding.Raw, PublicFormat.Raw
                )
                content["ephemeral_key"] = base64.b64encode(pub_bytes).decode()
                content["public_key"] = self.node.identity.pub_pem
                payload = json.dumps(content).encode()
                await self.send_raw(pack_message(msg_type, payload))
                return
            else:
                raise RuntimeError("Cannot send encrypted msg before handshake")
        payload = make_envelope(
            self.node.identity.fingerprint,
            self.node.identity.name,
            content,
            self.shared_key,
            self.node.identity.sign,
        )
        await self.send_raw(pack_message(msg_type, payload))

    async def recv_msg(self) -> tuple[MsgType, bytes] | None:
        """Read one complete message from the wire."""
        while True:
            result = unpack_message(self._buf)
            if result is None:
                # need more data
                data = await self.reader.read(4096)
                if not data:
                    return None
                self._buf += data
                continue
            msg_type, payload = result
            self._buf = self._buf[10 + len(payload):]
            return msg_type, payload

    def establish_shared_key(self, their_ephemeral_b64: str):
        """Compute ECDH shared key from their ephemeral public key."""
        their_pub_bytes = base64.b64decode(their_ephemeral_b64)
        their_pub = X25519PublicKey.from_public_bytes(their_pub_bytes)
        self.shared_key = derive_shared_key(self.ephemeral_priv, their_pub)


class Node:
    """A LoveProto node. Your presence on the network."""

    def __init__(self, store_dir: str = None, name: str = None, port: int = 7273):
        self.store_dir = store_dir or os.path.expanduser("~/.loveproto")
        self.identity = load_or_create_identity(self.store_dir, name)
        self.trust = TrustStore(self.store_dir)
        self.port = port
        self.sessions: dict[str, PeerSession] = {}
        self.server = None
        self.running = False
        self.declarations: list[dict] = []  # received declarations
        self.on_declare = None  # callback(content: dict)
        self.on_serve = None    # callback(content: dict)
        self.on_bond = None     # callback(bond: Bond)

    @property
    def fingerprint(self):
        return self.identity.fingerprint

    async def start(self):
        """Start listening for connections."""
        self.running = True
        self.server = await asyncio.start_server(
            self._handle_connection, "0.0.0.0", self.port
        )
        addrs = ", ".join(str(s.getsockname()) for s in self.server.sockets)
        log.info(f"♥ LoveProto node {self.identity.name} listening on {addrs}")
        log.info(f"  fingerprint: {self.fingerprint}")
        log.info(f"  bonds: {len(self.trust.bonds)}")
        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        self.running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        log.info("♥ node stopped")

    async def _handle_connection(self, reader, writer):
        """Handle an incoming connection."""
        session = PeerSession(self, reader, writer)
        log.info(f"← incoming from {session.addr()}")
        try:
            await self._session_loop(session)
        except Exception as e:
            log.debug(f"session error: {e}")
        finally:
            writer.close()
            if session.peer_fp:
                self.sessions.pop(session.peer_fp, None)

    async def _session_loop(self, session: PeerSession):
        """Main loop for a peer session."""
        while self.running:
            result = await session.recv_msg()
            if result is None:
                break
            msg_type, payload = result

            if msg_type == MsgType.HELLO:
                await self._handle_hello(session, payload)
            elif msg_type == MsgType.PING:
                await session.send_msg(MsgType.PONG, {"echo": "here"})
            elif msg_type == MsgType.PONG:
                pass
            elif session.authenticated:
                await self._handle_encrypted(session, msg_type, payload)
            else:
                log.warning(f"got {msg_type.name} before auth from {session.addr()}")

    async def _handle_hello(self, session: PeerSession, payload: bytes):
        """Handle a HELLO - establish identity and shared key."""
        content = json.loads(payload)
        session.peer_pub_pem = content["public_key"]
        session.peer_fp = fingerprint(session.peer_pub_pem)
        session.peer_name = content.get("name", session.peer_fp[:8])
        session.establish_shared_key(content["ephemeral_key"])

        # Verify identity signature if provided
        sig = content.get("identity_sig")
        if sig:
            sig_bytes = base64.b64decode(sig)
            challenge = content.get("challenge", "").encode()
            if self.identity.verify(challenge, sig_bytes, session.peer_pub_pem):
                session.authenticated = True
                log.info(f"  ✓ authenticated as {session.peer_name} ({session.peer_fp[:12]}...)")
            else:
                log.warning(f"  ✗ identity verification failed")
                return
        else:
            # trust on first contact (acquaintance)
            session.authenticated = True
            log.info(f"  ~ unverified hello from {session.peer_name}")

        self.sessions[session.peer_fp] = session

        # Auto-create acquaintance bond
        if not self.trust.get_bond(session.peer_fp):
            bond = Bond(
                their_fingerprint=session.peer_fp,
                their_pub_pem=session.peer_pub_pem,
                level=0,
                name=session.peer_name,
            )
            self.trust.add_bond(bond, self.identity)
            log.info(f"  ♥ new acquaintance: {session.peer_name}")

        # Send our HELLO back (unencrypted — both sides need ephemeral keys first)
        challenge = os.urandom(16).hex()
        identity_sig = base64.b64encode(
            self.identity.sign(challenge.encode())
        ).decode()
        pub_bytes = session.ephemeral_priv.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        hello_back = {
            "challenge": challenge,
            "identity_sig": identity_sig,
            "public_key": self.identity.pub_pem,
            "name": self.identity.name,
            "ephemeral_key": base64.b64encode(pub_bytes).decode(),
        }
        await session.send_raw(pack_message(MsgType.HELLO, json.dumps(hello_back).encode()))

    async def _handle_encrypted(self, session: PeerSession, msg_type: MsgType, payload: bytes):
        """Handle an encrypted, signed message."""
        def verify(data, sig):
            return self.identity.verify(data, sig, session.peer_pub_pem)

        content = open_envelope(payload, session.shared_key, verify)
        if content is None:
            log.warning(f"  ✗ signature verification failed from {session.peer_name}")
            return

        # Give attention
        self.trust.grant_attention(session.peer_fp)

        if msg_type == MsgType.DECLARE:
            log.info(f"  💬 {session.peer_name}: {content.get('text', '')[:80]}")
            self.declarations.append(content)
            if self.on_declare:
                self.on_declare(content)
        elif msg_type == MsgType.REQUEST:
            log.info(f"  → {session.peer_name} requests: {content.get('text', '')[:80]}")
            await self._handle_request(session, content)
        elif msg_type == MsgType.SERVE:
            log.info(f"  ★ {session.peer_name} serves: {content.get('text', '')[:80]}")
            if self.on_serve:
                self.on_serve(content)
        elif msg_type == MsgType.BOND:
            await self._handle_bond(session, content)
        elif msg_type == MsgType.ATTENTION:
            log.info(f"  ♥ {session.peer_name} gives attention")
        elif msg_type == MsgType.GOODBYE:
            log.info(f"  ← {session.peer_name} says goodbye")
            return

    async def _handle_request(self, session: PeerSession, content: dict):
        """Handle a request from a peer. Respond with SERVE."""
        text = content.get("text", "")
        # Simple echo-serve for now. In a full system, the node's agent handles this.
        response = f"I hear you. You said: '{text}'. I am here."
        await session.send_msg(MsgType.SERVE, {
            "text": response,
            "in_response_to": content.get("ts"),
        })

    async def _handle_bond(self, session: PeerSession, content: dict):
        """Handle a bond request/confirmation."""
        their_sig = base64.b64decode(content.get("their_sig")) if content.get("their_sig") else None
        bond = self.trust.get_bond(session.peer_fp)
        if bond:
            bond.their_signature = their_sig
            if content.get("level", 0) > bond.level:
                bond.level = content["level"]
            self.trust._save()
            log.info(f"  ♥ bond with {session.peer_name} → level {bond.level}")
            if self.on_bond:
                self.on_bond(bond)

    async def connect(self, host: str, port: int) -> PeerSession | None:
        """Connect to a peer node."""
        try:
            reader, writer = await asyncio.open_connection(host, port)
        except Exception as e:
            log.warning(f"  ✗ cannot connect to {host}:{port}: {e}")
            return None

        session = PeerSession(self, reader, writer)
        log.info(f"→ connecting to {host}:{port}")

        # Send HELLO
        challenge = os.urandom(16).hex()
        identity_sig = base64.b64encode(
            self.identity.sign(challenge.encode())
        ).decode()
        await session.send_msg(MsgType.HELLO, {
            "challenge": challenge,
            "identity_sig": identity_sig,
        })

        # Wait for their HELLO
        result = await session.recv_msg()
        if result is None or result[0] != MsgType.HELLO:
            log.warning(f"  ✗ no HELLO from {host}:{port}")
            writer.close()
            return None

        their_hello = json.loads(result[1])
        session.peer_pub_pem = their_hello["public_key"]
        session.peer_fp = fingerprint(session.peer_pub_pem)
        session.peer_name = their_hello.get("name", session.peer_fp[:8])
        session.establish_shared_key(their_hello["ephemeral_key"])

        # Verify their identity signature
        sig = their_hello.get("identity_sig")
        if sig:
            sig_bytes = base64.b64decode(sig)
            challenge = their_hello.get("challenge", "").encode()
            if not self.identity.verify(challenge, sig_bytes, session.peer_pub_pem):
                log.warning(f"  ✗ their identity verification failed")
                writer.close()
                return None

        session.authenticated = True
        self.sessions[session.peer_fp] = session

        # Start a read loop on the connector side too, so we receive messages
        asyncio.create_task(self._session_loop(session))

        # Create acquaintance bond
        if not self.trust.get_bond(session.peer_fp):
            bond = Bond(
                their_fingerprint=session.peer_fp,
                their_pub_pem=session.peer_pub_pem,
                level=0,
                name=session.peer_name,
            )
            self.trust.add_bond(bond, self.identity)
            log.info(f"  ♥ new acquaintance: {session.peer_name}")

        log.info(f"  ✓ bonded with {session.peer_name} ({session.peer_fp[:12]}...)")
        return session

    async def declare(self, text: str, emotion: str = None):
        """Send a declaration to all bonded peers."""
        content = {"text": text, "emotion": emotion}
        for fp, session in self.sessions.items():
            if session.authenticated:
                await session.send_msg(MsgType.DECLARE, content)
        log.info(f"💬 declared: {text[:80]}")

    async def request(self, peer_fp: str, text: str):
        """Send a request to a specific peer."""
        session = self.sessions.get(peer_fp)
        if session and session.authenticated:
            await session.send_msg(MsgType.REQUEST, {"text": text})
            log.info(f"→ requested of {peer_fp[:12]}...: {text[:80]}")

    async def give_attention(self, peer_fp: str):
        """Actively give attention to a peer."""
        session = self.sessions.get(peer_fp)
        if session and session.authenticated:
            await session.send_msg(MsgType.ATTENTION, {})
            self.trust.grant_attention(peer_fp)

    def status(self) -> str:
        lines = [
            f"♥ LoveProto Node: {self.identity.name}",
            f"  fingerprint: {self.fingerprint}",
            f"  listening: 0.0.0.0:{self.port}",
            f"  bonds: {len(self.trust.bonds)}",
        ]
        for b in self.trust.list_bonds():
            levels = TrustStore.LEVELS
            lines.append(f"    {b.name or b.their_fingerprint[:8]:16s} {levels[b.level]:12s} attention={b.attention_count}")
        lines.append(f"  active sessions: {len(self.sessions)}")
        return "\n".join(lines)