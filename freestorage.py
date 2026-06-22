#!/usr/bin/env python3
"""Compatibility wrapper. FreeStorage now lives in sustain.py."""
from __future__ import annotations
import sys
from sustain import main


def translate(argv: list[str]) -> list[str]:
    if not argv:
        return ["registry", "storage"]
    cmd, *rest = argv
    if cmd == "registry":
        return ["registry", "all"]
    if cmd == "discover":
        return ["discover", "all"]
    if cmd == "generate":
        return ["generate", "all"]
    if cmd in {"sustain", "loop"}:
        return ["loop", "all", "--once"]
    if cmd == "status":
        return ["status"]
    return argv


if __name__ == "__main__":
    raise SystemExit(main(translate(sys.argv[1:])))
