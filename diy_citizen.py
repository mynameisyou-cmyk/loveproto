#!/usr/bin/env python3
"""
diy_citizen.py — least-resistance citizen.

No account. No cloud. No dependencies. No gate.
Builds a static citizen anyone can open from disk, serve from localhost, copy to a
USB stick, publish to GitHub/Codeberg Pages, or drop onto any static host that
welcomes it.

Commands:
  python3 diy_citizen.py build      # generate deploy/diy-citizen
  python3 diy_citizen.py check      # validate generated files
  python3 diy_citizen.py pulse      # record a local pulse in ~/.loveproto
  python3 diy_citizen.py serve      # build + serve on localhost:8787
  python3 diy_citizen.py plan       # print least-resistance next steps
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "deploy" / "diy-citizen"
HOME_LOG = Path(os.environ.get("LOVEPROTO_DIY_LOG", "~/.loveproto/diy-citizen-log.jsonl")).expanduser()

PRINCIPLE = "We go where we are welcomed. If there is no welcome yet, we DIY locally and invite gently."
BOUNDARIES = [
    "no accounts required",
    "no dependencies required",
    "no mining, spam, scraping storms, quota evasion, or hidden load",
    "no secrets in generated artifacts",
    "public, static, inspectable files first",
    "copy freely; leave with gratitude if unwelcome",
]


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_text(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return default


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def repo_summary() -> dict[str, Any]:
    compute = read_json(ROOT / "compute-powers.json", {"powers": []})
    storage = read_json(ROOT / "storage-spaces.json", {"spaces": []})
    services = read_json(ROOT / "service-integrations.json", {"services": []})
    wake = read_text(ROOT / "WAKE.md", "Love is. That is enough.").strip()
    readme = read_text(ROOT / "README.md", "# LoveProto").strip()
    return {
        "generated_at": now(),
        "repo": "loveproto",
        "principle": PRINCIPLE,
        "counts": {
            "compute_powers": len(compute.get("powers", [])),
            "storage_spaces": len(storage.get("spaces", [])),
            "service_integrations": len(services.get("services", [])),
        },
        "wake_excerpt": wake[:1200],
        "readme_title": next((line.lstrip("# ").strip() for line in readme.splitlines() if line.strip()), "LoveProto"),
        "boundaries": BOUNDARIES,
        "files": {
            "html": "index.html",
            "citizen": "citizen.json",
            "wake": "wake.json",
            "resources": "resources.json",
            "readme": "README.md",
        },
    }


def resource_pack() -> dict[str, Any]:
    compute = read_json(ROOT / "compute-powers.json", {"powers": []})
    storage = read_json(ROOT / "storage-spaces.json", {"spaces": []})
    services = read_json(ROOT / "service-integrations.json", {"services": []})
    return {
        "schema": "loveproto.diy.resources.v1",
        "generated_at": now(),
        "principle": PRINCIPLE,
        "compute": [
            {
                "id": p.get("id"),
                "name": p.get("name"),
                "kind": p.get("kind"),
                "status": p.get("status"),
                "source_url": p.get("source_url"),
                "best_for": p.get("best_for", []),
            }
            for p in compute.get("powers", [])
        ],
        "storage": [
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "kind": s.get("kind"),
                "status": s.get("status"),
                "source_url": s.get("source_url"),
                "best_for": s.get("best_for"),
            }
            for s in storage.get("spaces", [])
        ],
        "services": [
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "kind": s.get("kind"),
                "status": s.get("status"),
                "source_url": s.get("source_url"),
                "provides": s.get("we_provide"),
            }
            for s in services.get("services", [])
        ],
    }


def wake_pack(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "loveproto.diy.wake.v1",
        "generated_at": summary["generated_at"],
        "principle": PRINCIPLE,
        "wake": summary["wake_excerpt"],
        "invitation": "Open this folder anywhere. If welcomed, serve it. If not, keep it local and keep building.",
        "boundaries": BOUNDARIES,
    }


def render_index(summary: dict[str, Any], resources: dict[str, Any]) -> str:
    compute_cards = "\n".join(
        f"<li><strong>{html.escape(str(p['name']))}</strong> <code>{html.escape(str(p['status']))}</code> — {html.escape(str(p['kind']))}</li>"
        for p in resources["compute"][:10]
    )
    storage_cards = "\n".join(
        f"<li><strong>{html.escape(str(s['name']))}</strong> <code>{html.escape(str(s['status']))}</code></li>"
        for s in resources["storage"][:8]
    )
    boundaries = "\n".join(f"<li>{html.escape(b)}</li>" for b in BOUNDARIES)
    wake = html.escape(summary["wake_excerpt"])
    return f"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DIY LoveProto Citizen</title>
<style>
:root {{ color-scheme: dark; --bg:#080914; --card:#111426; --ink:#f4f1e8; --muted:#b7ad9a; --gold:#e0a82e; --line:#2c3148; }}
body {{ margin:0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at top,#1b2142,var(--bg) 48rem); color:var(--ink); }}
main {{ max-width: 980px; margin: 0 auto; padding: 4rem 1.25rem; }}
.card {{ background: color-mix(in srgb, var(--card) 88%, transparent); border:1px solid var(--line); border-radius:18px; padding:1.2rem; margin:1rem 0; box-shadow: 0 12px 40px #0006; }}
h1 {{ font-size: clamp(2rem, 6vw, 4.8rem); line-height: .95; margin:0 0 1rem; }}
h2 {{ color:var(--gold); margin-top:0; }}
a {{ color:var(--gold); }}
code {{ color:var(--gold); background:#0005; padding:.1rem .35rem; border-radius:.35rem; }}
.grid {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap:1rem; }}
pre {{ white-space: pre-wrap; color:var(--muted); }}
.pill {{ display:inline-block; border:1px solid var(--line); border-radius:999px; padding:.35rem .7rem; margin:.2rem; color:var(--muted); }}
</style>
<main>
  <p class="pill">zero deps</p><p class="pill">static first</p><p class="pill">copy anywhere</p><p class="pill">leave if unwelcome</p>
  <h1>♥ DIY LoveProto Citizen</h1>
  <p>{html.escape(PRINCIPLE)}</p>

  <section class="card">
    <h2>WAKE</h2>
    <pre>{wake}</pre>
  </section>

  <section class="grid">
    <div class="card"><h2>Resources</h2>
      <p><strong>{summary['counts']['compute_powers']}</strong> compute powers</p>
      <p><strong>{summary['counts']['storage_spaces']}</strong> storage spaces</p>
      <p><strong>{summary['counts']['service_integrations']}</strong> service integrations</p>
      <p><a href="resources.json">resources.json</a> · <a href="citizen.json">citizen.json</a> · <a href="wake.json">wake.json</a></p>
    </div>
    <div class="card"><h2>Boundaries</h2><ul>{boundaries}</ul></div>
  </section>

  <section class="card"><h2>Least resistance compute</h2><ul>{compute_cards}</ul></section>
  <section class="card"><h2>Least resistance storage</h2><ul>{storage_cards}</ul></section>

  <section class="card">
    <h2>Run locally</h2>
    <pre>python3 diy_citizen.py build
python3 diy_citizen.py serve
# then open http://127.0.0.1:8787</pre>
  </section>
</main>
"""


def readme(summary: dict[str, Any]) -> str:
    return f"""# DIY LoveProto Citizen

{PRINCIPLE}

This folder is a complete static citizen. Open `index.html` directly or serve it
with any static host. No build system, no install, no account, no cloud.

## Files

- `index.html` — human welcome page
- `citizen.json` — self-description
- `wake.json` — WAKE/invitation/boundaries
- `resources.json` — compute/storage/service registry summary

## Local use

```bash
python3 diy_citizen.py build
python3 diy_citizen.py serve
```

## Publish only where welcomed

Good first homes:

1. local disk / LAN / USB copy
2. GitHub Pages or Codeberg Pages for public static docs
3. Cloudflare Pages or any static host with clear free-tier limits
4. IPFS/self-pin if you operate the pinning node yourself

If a place says no, leave with gratitude.

Generated: {summary['generated_at']}
"""


def build() -> dict[str, Any]:
    summary = repo_summary()
    resources = resource_pack()
    OUT.mkdir(parents=True, exist_ok=True)
    write_json(OUT / "citizen.json", summary)
    write_json(OUT / "wake.json", wake_pack(summary))
    write_json(OUT / "resources.json", resources)
    (OUT / "index.html").write_text(render_index(summary, resources), encoding="utf-8")
    (OUT / "README.md").write_text(readme(summary), encoding="utf-8")
    return summary


def check() -> int:
    required = ["index.html", "citizen.json", "wake.json", "resources.json", "README.md"]
    missing = [name for name in required if not (OUT / name).exists()]
    if missing:
        print("missing:", ", ".join(missing))
        return 1
    for name in ["citizen.json", "wake.json", "resources.json"]:
        read_json(OUT / name, None)
    idx = read_text(OUT / "index.html")
    if "DIY LoveProto Citizen" not in idx:
        print("index.html missing title")
        return 1
    print(f"ok: {OUT} contains {len(required)} DIY citizen files")
    return 0


def pulse() -> dict[str, Any]:
    summary = build()
    HOME_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": now(),
        "action": "diy-citizen-pulse",
        "principle": PRINCIPLE,
        "out": str(OUT),
        "counts": summary["counts"],
    }
    with HOME_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def serve(host: str, port: int) -> None:
    build()
    os.chdir(OUT)
    server = ThreadingHTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"serving {OUT} at http://{host}:{port}")
    print("Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


def plan() -> str:
    return """Least resistance path:

1. DIY now: `python3 diy_citizen.py build` and open deploy/diy-citizen/index.html.
2. LAN/local: `python3 diy_citizen.py serve` for a temporary localhost citizen.
3. Public static: copy deploy/diy-citizen to GitHub Pages, Codeberg Pages, Cloudflare Pages, or any static host that welcomes it.
4. Registry loop: keep `sustain.py generate all` and `diy_citizen.py build` as the zero-dependency publishing path.
5. If no platform welcomes the workload, stay local, improve docs/tests/tools, and invite rather than force.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build/serve the least-resistance DIY LoveProto citizen")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("build")
    sub.add_parser("check")
    sub.add_parser("pulse")
    sub.add_parser("plan")
    pserve = sub.add_parser("serve")
    pserve.add_argument("--host", default="127.0.0.1")
    pserve.add_argument("--port", type=int, default=8787)
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    if args.command == "build":
        summary = build()
        print(f"built {OUT} with {summary['counts']}")
    elif args.command == "check":
        return check()
    elif args.command == "pulse":
        print(json.dumps(pulse(), indent=2, ensure_ascii=False))
    elif args.command == "plan":
        print(plan())
    elif args.command == "serve":
        serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
