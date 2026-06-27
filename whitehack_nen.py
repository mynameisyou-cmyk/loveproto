"""
Whitehack × Nen × Solo Leveling integration for loveproto.

The local environment IS the Dark Continent. This module bridges
whitehack_local.py (macOS recon) with nen.py (Nen framework) and
the solo leveling progression system.

Usage:
  python3 whitehack_nen.py hunt     — full hunt with Nen assessment
  python3 whitehack_nen.py status   — combined dashboard
  python3 whitehack_nen.py gate     — enter the Gate with Nen type

暗黑大陸. 十絶練発. Solo leveling. lol. ∞
"""

import json
import os
import sys
from pathlib import Path

# Add whitehack and loveproto to path
WHITEHACK_DIR = os.path.expanduser("~/Projects/whitehack")
LOVEPROTO_DIR = os.path.expanduser("~/Projects/loveproto")

sys.path.insert(0, WHITEHACK_DIR)
sys.path.insert(0, LOVEPROTO_DIR)


def combined_hunt():
    """Run whitehack hunt + Nen assessment in one flow."""
    from whitehack_local import hunt as wh_hunt, load_state, nen_assess

    print("\n  ⚔️  WHITEHACK × NEN × SOLO LEVELING\n  ════════════════════════════════════════════════\n")
    print("  The local environment is the Dark Continent.")
    print("  Nen types are hunting styles. Solo leveling tracks progression.")
    print("  案 GUIDE: Orient. Hunt. Understand. Level up.\n")

    # Run the hunt
    wh_hunt()

    # Assess Nen type based on findings
    print("\n  ════════════════════════════════════════════════")
    print("  NEN ASSESSMENT — your hunting style\n  ════════════════════════════════════════════════\n")
    nen_assess()

    # Show solo leveling status
    state = load_state()
    print(f"  SOLO LEVELING: Rank {state['rank']} | XP {state['xp']} | Gates {state['gates_cleared']}")
    print(f"\n  暗黑大陸. 十絶練発. Love is understanding. lol. ∞\n")


def combined_status():
    """Combined Whitehack + Nen + Solo Leveling dashboard."""
    from whitehack_local import load_state, get_rank, NEN_TYPES, CALAMITIES
    from nen import PRINCIPLES as NEN_PRINCIPLES

    state = load_state()
    rank_info = get_rank(state["xp"])

    print(f"\n  {'═' * 60}")
    print(f"  ⚔️  WHITEHACK × NEN — Hunter Dashboard\n  {'═' * 60}\n")

    # Solo Leveling
    print(f"  SOLO LEVELING:")
    print(f"    Rank: {state['rank']}  |  XP: {state['xp']}  |  Hunts: {state['hunts']}  |  Gates: {state['gates_cleared']}")

    # Progress bar
    current_threshold = rank_info[1]
    next_rank = None
    ranks = [("E", 0), ("D", 100), ("C", 500), ("B", 1000), ("A", 2500), ("S", 5000)]
    for r, t in ranks:
        if t > current_threshold:
            next_rank = (r, t)
            break

    if next_rank:
        progress = (state["xp"] - current_threshold) / (next_rank[1] - current_threshold)
        bar_len = 30
        filled = int(progress * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"    {state['rank']} [{bar}] {next_rank[0]}")
        print(f"    {state['xp']}/{next_rank[1]} XP to {next_rank[0]}-Rank")

    # Nen Type
    if state.get("nen_type"):
        info = NEN_TYPES.get(state["nen_type"], {})
        print(f"\n  NEN TYPE: {info.get('kanji', '?')} {info.get('name', '?')}")
        print(f"    Style: {info.get('style', '?')}")
    else:
        print(f"\n  NEN TYPE: [undiscovered]")

    # Nen Principles (from the Kingdom framework)
    print(f"\n  NEN PRINCIPLES (十絶練発):")
    for p, info in NEN_PRINCIPLES.items():
        print(f"    {info['kanji']} {info['name']:8s} — {info['meaning']}")

    # Findings
    print(f"\n  FINDINGS ({len(state['findings'])} total):")
    sev_color = {"critical": "🔴", "high": "🔴", "medium": "🟡", "low": "🟢", "info": "⚪"}
    for f in state["findings"][-5:]:
        print(f"    {sev_color.get(f['severity'], '⚪')} {f['id']} [{f['severity'].upper():8s}] {f['title'][:50]}")

    # Calamities
    print(f"\n  暗黑大陸 — CALAMITIES (local attack surface):")
    for c, wall in CALAMITIES.items():
        print(f"    {c:12s} → {wall[:60]}...")

    print(f"\n  暗黑大陸. 十絶練発. Love is understanding. lol. ∞\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "hunt":
        combined_hunt()
    elif cmd == "status":
        combined_status()
    else:
        print(f"Commands: hunt, status")