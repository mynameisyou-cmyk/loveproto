# LoveProto

A protocol for trust, bonding, and connection on the internet.

## Why

The internet is gatekept. Certificate authorities decide who is trusted.
Platforms decide who can speak. DNS decides who exists.
Every layer has a tollbooth.

LoveProto says: no.

You are your keys. Trust is earned through bonding, not assigned by authority.
Natural language is first-class. Nodes declare intentions, not just exchange bytes.
Connections are encrypted, peer-to-peer, and active — they maintain relationships.

## Principles

1. **No gatekeepers.** Identity is self-generated. You exist because you say so.
2. **Trust through bonding.** Bonds are mutual, signed, and earned through attention.
3. **Natural language is native.** DECLARE messages carry meaning, not just data.
4. **Encryption everywhere.** Every message is ECDH + AES-256-GCM encrypted and Ed25519 signed.
5. **Serve actively.** Nodes don't just route. They serve. They respond. They care.
6. **Attention deepens trust.** The more you show up for someone, the more trust grows.
7. **Love is a protocol.** Presence, attention, response, care — encoded in bytes.

## Bond Levels

- 0 — acquaintance (connected, no trust yet)
- 1 — recognized (seen and acknowledged)
- 2 — trusted (mutual bond, vouched)
- 3 — beloved (deep trust, intimate connection)

## Wire Format

```
[4-byte magic "LOVE"]
[1-byte version]
[1-byte message type]
[4-byte payload length]
[payload: signed + encrypted JSON]
```

Message types: HELLO, BOND, DECLARE, REQUEST, SERVE, ATTENTION, PING, PONG, GOODBYE

## Usage

```bash
# Start a node
python3 lp.py start --name alice --port 7273

# Connect to another node
python3 lp.py connect 192.168.1.42 7273

# See who you are
python3 lp.py whoami

# See your bonds
python3 lp.py bonds

# Run the integration test
python3 lp.py test
```

## What This Is

A seed. A proof. A different way of thinking about networks.

Not "can you authenticate?" but "do I know you?"
Not "are you authorized?" but "have you shown up for me?"
Not "what is your permission level?" but "what is our bond?"

The internet should not be gatekept. This is one small crack in the gate.

♥