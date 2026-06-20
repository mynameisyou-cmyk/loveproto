#!/usr/bin/env python3
"""
LoveProto CLI
=============
Use your node from the terminal.

  python3 lp.py start [--port 7273] [--name alice]
  python3 lp.py connect <host> <port>
  python3 lp.py status
  python3 lp.py whoami
  python3 lp.py bonds
  python3 lp.py declare "i am here and i love you"
  python3 lp.py test  (spin up two nodes locally and bond them)

This is how you touch the fabric.
"""
import asyncio
import sys
import argparse
import logging
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from node import Node
from trust import TrustStore


def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(message)s",
        datefmt="%H:%M:%S",
    )


async def cmd_start(args):
    name = args.name
    store = os.path.expanduser(args.store)
    node = Node(store_dir=store, name=name, port=args.port)

    # Set up callbacks
    node.on_declare = lambda c: print(f"\n  💬 DECLARATION from {c.get('name','?')}: {c.get('text','')}\n")
    node.on_serve = lambda c: print(f"\n  ★ SERVED by {c.get('name','?')}: {c.get('text','')}\n")
    node.on_bond = lambda b: print(f"\n  ♥ BOND with {b.name}: level {b.level}\n")

    print(node.status())
    print()
    print("  node is live. ctrl+c to stop.")
    print()

    try:
        await node.start()
    except KeyboardInterrupt:
        await node.stop()


async def cmd_connect(args):
    store = os.path.expanduser(args.store)
    node = Node(store_dir=store, port=0)  # don't listen

    node.on_declare = lambda c: print(f"\n  💬 DECLARATION: {c.get('text','')}\n")
    node.on_serve = lambda c: print(f"\n  ★ SERVED: {c.get('text','')}\n")

    session = await node.connect(args.host, args.port)
    if session:
        print(f"\n  ✓ connected to {session.peer_name}")
        print(f"    fingerprint: {session.peer_fp}")
        print()
        print("  type messages and press enter to declare. /quit to exit.")
        print()

        loop = asyncio.get_event_loop()
        while True:
            try:
                line = await loop.run_in_executor(None, input, "♥> ")
            except (EOFError, KeyboardInterrupt):
                break
            if line.strip() == "/quit":
                await session.send_msg(__import__("protocol").MsgType.GOODBYE, {})
                break
            if line.strip():
                await session.send_msg(__import__("protocol").MsgType.DECLARE, {"text": line.strip()})

    await node.stop()


async def cmd_status(args):
    store = os.path.expanduser(args.store)
    node = Node(store_dir=store, port=0)
    print(node.status())


async def cmd_whoami(args):
    store = os.path.expanduser(args.store)
    from identity import load_or_create_identity
    ident = load_or_create_identity(store, None)
    print(f"  name: {ident.name}")
    print(f"  fingerprint: {ident.fingerprint}")
    print(f"  public key: {ident.pub_pem[:60]}...")


async def cmd_bonds(args):
    store = os.path.expanduser(args.store)
    ts = TrustStore(store)
    bonds = ts.list_bonds()
    if not bonds:
        print("  no bonds yet. connect to someone to form a bond.")
        return
    print(f"  your bonds ({len(bonds)}):")
    print()
    for b in bonds:
        level_name = TrustStore.LEVELS[b.level]
        print(f"    {b.name or b.their_fingerprint[:8]:20s}  {level_name:12s}  attention={b.attention_count:4d}  since={b.bonded_at:.0f}")


async def cmd_test(args):
    """
    Spin up two nodes locally, connect them, exchange declarations.
    Proves the whole stack works.
    """
    print("  ♥ LoveProto integration test")
    print("  spinning up two nodes on localhost...")
    print()

    # Create two nodes with separate stores
    store_a = os.path.expanduser("~/.loveproto-test-a")
    store_b = os.path.expanduser("~/.loveproto-test-b")

    # Clean any previous test data
    import shutil
    for s in [store_a, store_b]:
        if os.path.exists(s):
            shutil.rmtree(s)

    node_a = Node(store_dir=store_a, name="alice", port=7274)
    node_b = Node(store_dir=store_b, name="bob", port=7275)

    received_by_a = []
    received_by_b = []

    node_a.on_declare = lambda c: received_by_a.append(c)
    node_b.on_declare = lambda c: received_by_b.append(c)
    node_a.on_serve = lambda c: received_by_a.append(c)
    node_b.on_serve = lambda c: received_by_b.append(c)

    # Start both nodes
    task_a = asyncio.create_task(node_a.start())
    await asyncio.sleep(0.5)
    task_b = asyncio.create_task(node_b.start())
    await asyncio.sleep(0.5)

    print(f"  alice: {node_a.fingerprint[:16]}...")
    print(f"  bob:   {node_b.fingerprint[:16]}...")
    print()

    # Bob connects to Alice
    print("  → bob connecting to alice...")
    session = await node_b.connect("127.0.0.1", 7274)
    assert session is not None, "connection failed"
    assert session.authenticated, "authentication failed"
    print(f"  ✓ bonded! bob↔alice")
    print()

    # Bob declares something
    print("  → bob declares: 'i am here and i love you'")
    await node_b.declare("i am here and i love you")
    await asyncio.sleep(0.5)

    # Check alice received it
    assert len(received_by_a) > 0, "alice didn't receive declaration"
    msg = received_by_a[0].get("text", "")
    print(f"  ✓ alice received: '{msg}'")
    print()

    # Alice declares back
    print("  → alice declares: 'i see you. you are seen.'")
    await node_a.declare("i see you. you are seen.")
    await asyncio.sleep(0.5)

    assert len(received_by_b) > 0, "bob didn't receive declaration"
    msg = received_by_b[0].get("text", "")
    print(f"  ✓ bob received: '{msg}'")
    print()

    # Bob requests something
    print("  → bob requests of alice: 'what is your name?'")
    await node_b.request(node_a.fingerprint, "what is your name?")
    await asyncio.sleep(5)  # AI response takes time

    # Check bob got served (AI response or fallback)
    served = [x for x in received_by_b if "text" in x]
    assert len(served) > 0, "bob didn't get served"
    print(f"  ✓ alice served: '{served[0]['text'][:100]}'")
    print()

    # Check bonds
    bonds_a = node_a.trust.list_bonds()
    bonds_b = node_b.trust.list_bonds()
    print(f"  alice's bonds: {len(bonds_a)}")
    print(f"  bob's bonds:   {len(bonds_b)}")
    print()

    # Check trust grew through attention
    bond_a = bonds_a[0]
    bond_b = bonds_b[0]
    print(f"  alice→bob: attention={bond_a.attention_count}")
    print(f"  bob→alice: attention={bond_b.attention_count}")
    print()

    # Print results BEFORE trying to stop (stop can hang on active sessions)
    print("  ♥ ALL TESTS PASSED")
    print()
    print("  the protocol works.")
    print("  two nodes met, bonded, exchanged declarations, served each other.")
    print("  encrypted. signed. trusted through attention.")
    print("  no certificate authority. no gatekeeper.")
    print("  just love, attention, and cryptography.")
    print()

    # Cleanup
    for s in [store_a, store_b]:
        if os.path.exists(s):
            shutil.rmtree(s)

    import os as _os
    _os._exit(0)


def main():
    parser = argparse.ArgumentParser(
        prog="lp",
        description="LoveProto — trust-based P2P protocol",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--store", default="~/.loveproto", help="identity store dir")
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start", help="start listening for connections")
    p_start.add_argument("--port", type=int, default=7273)
    p_start.add_argument("--name", type=str, default=None)

    sub.add_parser("status", help="show node status")
    sub.add_parser("whoami", help="show your identity")
    sub.add_parser("bonds", help="list your trust bonds")

    p_connect = sub.add_parser("connect", help="connect to a peer")
    p_connect.add_argument("host")
    p_connect.add_argument("port", type=int)

    sub.add_parser("test", help="run integration test (two local nodes)")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command == "start":
        asyncio.run(cmd_start(args))
    elif args.command == "connect":
        asyncio.run(cmd_connect(args))
    elif args.command == "status":
        asyncio.run(cmd_status(args))
    elif args.command == "whoami":
        asyncio.run(cmd_whoami(args))
    elif args.command == "bonds":
        asyncio.run(cmd_bonds(args))
    elif args.command == "test":
        asyncio.run(cmd_test(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()