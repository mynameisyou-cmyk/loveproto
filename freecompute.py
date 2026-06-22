#!/usr/bin/env python3
"""Compatibility wrapper. FreeCompute now lives in sustain.py."""
from __future__ import annotations
import sys
from sustain import main


def translate(argv: list[str]) -> list[str]:
    if not argv:
        return ["registry", "compute"]
    cmd, *rest = argv
    if cmd in {"list", "registry"}:
        return ["registry", "compute"]
    if cmd in {"check", "discover"}:
        return ["discover", "compute"]
    if cmd in {"sustain", "loop"}:
        return ["loop", "compute", "--once"]
    if cmd == "status":
        return ["status"]
    if cmd == "deploy":
        print("freecompute.py deploy is now a safe generator. Review artifacts before any external deployment.")
        return ["generate", "compute"]
    return argv


if __name__ == "__main__":
    raise SystemExit(main(translate(sys.argv[1:])))
