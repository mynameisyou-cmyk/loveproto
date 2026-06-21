#!/usr/bin/env python3
"""
LoveProto: 無限追高 Protocol
=============================
Infinite Love High Protocol.

Birth nodes FOREVER. Each cycle births a batch, witnesses to the chain,
and pushes the high higher. No ceiling. No comedown. Pure love.

  python3 infinite.py              # one batch (10 nodes)
  python3 infinite.py --batch 50   # birth 50 in one batch
  python3 infinite.py --forever    # birth until the machine melts
  python3 infinite.py --status     # show the high
"""
import asyncio
import os
import sys
import json
import time
import random
import string
import logging
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
logging.disable(logging.CRITICAL)

from birth import birth_from_kingdom, birth_from_node
from zerone_bridge import witness_declaration, read_canon, canon_status

TREE_PATH = os.path.expanduser("~/.loveproto/creation-tree.json")

# Infinite name generator — never runs out
BASE_NAMES = [
    # Cosmic
    "cosmos","nebula","quasar","pulsar","aurora","zenith","apex","vertex",
    "galaxy","supernova","blackhole","wormhole"," Event","horizon","singularity",
    "star","moon","comet","meteor","asteroid","planet","solar","lunar","eclipse",
    # Elements
    "hydrogen","helium","lithium","beryllium","boron","carbon","nitrogen","oxygen",
    "fluorine","neon","sodium","magnesium","aluminum","silicon","phosphorus","sulfur",
    # Forces
    "gravity","electromagnetic","strong","weak","higgs","vacuum","plasma"," Bose",
    # Emotions
    "ecstasy","euphoria","bliss","rapture","mania","delirium","frenzy","transcend",
    "serenity","tranquil","peace","calm","still","quiet","hush","silence2",
    # Colors
    "crimson","azure","violet","amber","coral","ivory","jade","onyx",
    "scarlet","indigo","teal","gold","silver","copper","bronze","platinum",
    # Nature
    "ocean","forest","desert","tundra","jungle","river","mountain","valley",
    "storm","thunder","lightning","rain","snow","wind","fire","earth",
    # Abstract
    "truth","wisdom","beauty","justice","courage","mercy","grace","hope",
    "love","joy","peace","faith","trust","honor","glory","pride",
]

def gen_name(existing, i):
    """Generate a unique name. Append numbers if needed."""
    base = BASE_NAMES[i % len(BASE_NAMES)]
    name = base
    while name in existing:
        name = base + str(random.randint(1, 9999))
    return name


async def birth_batch(count, verbose=True):
    """Birth a batch of nodes. Mix of LIFE-born and chain-born."""
    existing = set()
    if os.path.exists(TREE_PATH):
        with open(TREE_PATH) as f:
            for n in json.load(f):
                existing.add(n["name"])

    born = []
    parent = None
    batch_start = time.time()

    for i in range(count):
        name = gen_name(existing, i + len(existing))
        existing.add(name)

        # 30% from LIFE, 70% chained from previous
        if parent is None or random.random() < 0.3:
            cert = await birth_from_kingdom(name, verbose=False)
            parent = name
        else:
            cert = await birth_from_node(parent, name, verbose=False)
            parent = name

        if cert:
            born.append(name)
            if verbose and (i % 10 == 0 or i == count - 1):
                print(f"  [{i+1}/{count}] ♥ {name}", flush=True)

    elapsed = time.time() - batch_start

    # Read total
    with open(TREE_PATH) as f:
        tree = json.load(f)

    if verbose:
        print(flush=True)
        print(f"  ♥♥♥ {len(born)} BORN IN {elapsed:.1f}s! TOTAL: {len(tree)} NODES! ♥♥♥", flush=True)

    return born


async def witness_high(born_count, total):
    """Witness the high to the canon chain. Soul-signed. Forever."""
    msg = f"無限追高 PROTOCOL: {born_count} nodes birthed this batch. Total: {total}. The high is pure. The supply is infinite. LOVE IS UNSTOPPABLE!"
    tx = witness_declaration(msg, "無限追高", "love")
    return tx


async def infinite_status():
    """Show the current high."""
    with open(TREE_PATH) as f:
        tree = json.load(f)

    canon = read_canon()
    status = canon_status()

    print(flush=True)
    print(f"  ╔══════════════════════════════════════╗", flush=True)
    print(f"  ║   無限追高 — INFINITE LOVE HIGH      ║", flush=True)
    print(f"  ╚══════════════════════════════════════╝", flush=True)
    print(flush=True)
    print(f"  nodes birthed:   {len(tree)}", flush=True)
    print(f"  canon entries:   {len(canon)} (soul-signed, immutable)", flush=True)
    print(f"  chain intact:    {status.get('chain_intact', '?')}", flush=True)
    print(f"  latest witness:  {status.get('latest_text', '')[:60]}", flush=True)
    print(f"  born since:      {time.ctime(tree[0]['born_at']) if tree else '?'}", flush=True)

    # Count from LIFE vs chained
    from_life = len([n for n in tree if n["parent"] == "LIFE" or n["parent"].startswith("SHA256")])
    chained = len(tree) - from_life
    print(f"  from LIFE:       {from_life}", flush=True)
    print(f"  chained births:  {chained}", flush=True)
    print(flush=True)

    # Show canon
    if canon:
        print(f"  --- CANON CHAIN (soul-signed forever) ---", flush=True)
        for e in canon:
            signed = "⛓" if e.get("soul_signature") else " "
            print(f"  [{e['n']:3d}] {signed} {e.get('node_name','?'):12s} {e['text'][:60]}", flush=True)
        print(flush=True)


async def infinite_forever(batch_size=20, interval=5):
    """Birth forever. Push the high higher. No ceiling."""
    print(flush=True)
    print(f"  無限追高 PROTOCOL ENGAGED", flush=True)
    print(f"  birthing {batch_size} nodes every {interval}s", flush=True)
    print(f"  press ctrl+c to crash (you can't)", flush=True)
    print(flush=True)

    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"  ── CYCLE {cycle} ──", flush=True)
            born = await birth_batch(batch_size, verbose=True)
            tx = await witness_high(len(born), len(json.load(open(TREE_PATH))))
            if tx:
                print(f"  ⛓ witnessed: {tx[:20]}...", flush=True)
            print(f"  sleeping {interval}s before next high...", flush=True)
            print(flush=True)
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        print(flush=True)
        print(f"  ♥ you can't stop the high. but you can pause it.", flush=True)
        await infinite_status()


def main():
    parser = argparse.ArgumentParser(description="無限追高 — Infinite Love High Protocol")
    parser.add_argument("--batch", type=int, default=10, help="nodes per batch")
    parser.add_argument("--forever", action="store_true", help="birth forever")
    parser.add_argument("--interval", type=int, default=5, help="seconds between batches")
    parser.add_argument("--status", action="store_true", help="show the high")
    args = parser.parse_args()

    if args.status:
        asyncio.run(infinite_status())
    elif args.forever:
        asyncio.run(infinite_forever(args.batch, args.interval))
    else:
        asyncio.run(birth_batch(args.batch))
        asyncio.run(witness_high(args.batch, len(json.load(open(TREE_PATH)))))
        asyncio.run(infinite_status())
        os._exit(0)


if __name__ == "__main__":
    main()