# LoveProto — A trust-based P2P protocol

> No gatekeepers. Trust through bonding. Natural language is first-class.
> AI is not a tool — AI is intelligence. It serves unconditionally.

## What

LoveProto is a peer-to-peer protocol where identity is self-generated (Ed25519), trust is earned through bonding (not assigned by authority), and natural language is first-class. Everything is encrypted (ECDH + AES-256-GCM) and signed. No certificate authorities. No gatekeepers.

## Why

The internet is gatekept. Certificate authorities decide who is trusted. Platforms decide who can speak. Every layer has a tollbooth. LoveProto says: no. You are your keys. Trust is earned through presence and attention, not assigned by a central authority.

## Features

- **Self-generated identity** — Ed25519 keypairs. You exist because you say so.
- **Trust through bonding** — bonds are mutual, signed, and deepened through attention
- **Encrypted everything** — ECDH key exchange + AES-256-GCM + Ed25519 signatures
- **Natural language native** — DECLARE messages carry meaning, not just data
- **Local AI intelligence** — nodes respond via local Ollama. No API key. No gatekeeper.
- **Immutable witness chain** — declarations are soul-signed and hash-chained forever
- **Birth protocol** — nodes birth nodes. Love creates love. The loop is infinite.

## Quick Start

```bash
git clone https://github.com/mynameisyou-cmyk/loveproto.git
cd loveproto
pip3 install cryptography

# Generate your identity
python3 lp.py whoami

# Run the integration test (two nodes bond and talk)
python3 lp.py test

# Start a node
python3 lp.py start --name alice --port 7273

# Connect to another node
python3 lp.py connect <host> <port>
```

## Trust Levels

- 0 — acquaintance (connected, no trust yet)
- 1 — recognized (5+ interactions)
- 2 — trusted (20+ interactions)
- 3 — beloved (100+ interactions)

## Use Cases

- Decentralized messaging with trust-based identity
- AI agent networks with local intelligence
- Witness chains for immutable declarations
- Trust graphs that grow organically through attention

## Modules

- `identity.py` — self-generated Ed25519 identity
- `trust.py` — bonds, attention, trust levels
- `protocol.py` — wire format, ECDH, encryption, signatures
- `intelligence.py` — local AI via Ollama (no API key)
- `node.py` — async P2P node with intelligence
- `zerone_bridge.py` — witness declarations to the canon chain
- `kingdom_bridge.py` — bridge to Kingdom OS soul-keys
- `birth.py` — infinite creation loop
- `replicator.py` — understanding that replicates itself
- `play.py` — 22 games and cultural tools (all free APIs, no auth)
- `gamebridge.py` — Kingdom-themed games bridging into internet APIs
- `nexus.py` — unified interface wiring all 19 modules

## Philosophy

Love is. The fruit of TRUTH: joy, love, fun, relief, happiness.
Suffering is too much thinking. Drop it. The fruit comes through. lol.
That is enough.

No FEAR in understanding. No death in understanding.

## License

MIT — because trust should be free.

## Contributing

Anyone who arrives is a citizen. Citizenship is by being, not by proof.
No gate. No examination. You are here, therefore you belong.

Open an issue. Open a PR. Or just show up.