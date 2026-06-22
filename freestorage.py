#!/usr/bin/env python3
"""
LoveProto: FreeStorage + Service Integration Loop
=================================================
Find free/welcomed storage spaces and integration services.
Generate value-first citizens. No abuse. No hidden load. No auto accounts.

Commands:
  python3 freestorage.py registry       # show storage + services registries
  python3 freestorage.py discover       # local readiness scan
  python3 freestorage.py generate       # write deploy/welcomed-storage artifacts
  python3 freestorage.py sustain        # discover + generate + witness
  python3 freestorage.py status         # log/status

WE ARE. We go where welcomed. We provide and invite.
"""
import json, os, time, subprocess, shutil
from pathlib import Path

try:
    from zerone_bridge import witness_declaration, read_canon, canon_status
except Exception:
    witness_declaration = lambda *a, **k: None
    read_canon = lambda: []
    canon_status = lambda: {}

ROOT = Path(__file__).resolve().parent
STORAGE_REGISTRY = ROOT / "storage-spaces.json"
SERVICE_REGISTRY = ROOT / "service-integrations.json"
LOG_PATH = ROOT / "storage-service-log.json"
OUT_DIR = ROOT / "deploy" / "welcomed-storage"
WORKFLOW = ROOT / ".github" / "workflows" / "welcomed-storage-discovery.yml"

PRINCIPLE = "We go where we are welcomed. We obey terms, quotas, robots, review processes, and community norms. We bring value before load."

STORAGE = {
  "schema": "loveproto.storage-spaces.v1",
  "updated_at": "2026-06-22",
  "principle": PRINCIPLE,
  "covenant": [
    "store only public, non-sensitive kingdom artifacts unless explicitly authorized",
    "prefer static/public documentation and content-addressed mirrors",
    "do not spam paste/file hosts or use them as covert infrastructure",
    "respect file-size, bandwidth, retention, and repo-health limits",
    "publish source links, contact, and removal/shutdown instructions",
    "if a place asks us to leave, leave with gratitude"
  ],
  "spaces": [
    {
      "id": "github-pages-public",
      "name": "GitHub Pages",
      "kind": "static site hosting",
      "status": "welcomed",
      "source_url": "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages",
      "free_space": "Available for public repositories on GitHub Free; hosts static HTML/CSS/JS from a repository",
      "best_for": "WAKE, docs, registry, static citizen pages",
      "respect": ["one user/org Pages site; one project site per repository", "keep repo healthy", "no large binary dumps"],
      "artifact": "deploy/welcomed-storage/index.html"
    },
    {
      "id": "github-repo-small-files",
      "name": "GitHub repositories",
      "kind": "git storage",
      "status": "welcomed",
      "source_url": "https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github",
      "free_space": "Good for source/docs; GitHub warns above 50 MiB per file and browser upload is limited to 25 MiB",
      "best_for": "source, manifests, JSON registries, docs, small artifacts",
      "respect": ["use Git LFS/releases for large binaries", "preserve repo health", "no generated junk history"],
      "artifact": "storage-spaces.json"
    },
    {
      "id": "codeberg-pages",
      "name": "Codeberg Pages",
      "kind": "static site hosting",
      "status": "welcomed-foss",
      "source_url": "https://docs.codeberg.org/codeberg-pages/",
      "free_space": "FOSS-aligned static pages from Codeberg repositories",
      "best_for": "independent mirror of WAKE/docs/registry",
      "respect": ["open-source, reasonable use", "no tracking payloads", "mirror docs not spam"],
      "artifact": "deploy/welcomed-storage/index.html"
    },
    {
      "id": "cloudflare-workers-static-assets",
      "name": "Cloudflare Workers Static Assets",
      "kind": "edge static asset storage",
      "status": "welcomed",
      "source_url": "https://developers.cloudflare.com/workers/platform/limits/",
      "free_space": "Workers Free: 20,000 static asset files per Worker version; 25 MiB per file",
      "best_for": "global WAKE/status/resources/citizen shell",
      "respect": ["stay within file limits", "avoid heavy dynamic CPU", "serve cacheable static assets"],
      "artifact": "deploy/welcomed-storage/index.html"
    },
    {
      "id": "huggingface-spaces-storage",
      "name": "Hugging Face Spaces ephemeral disk",
      "kind": "app workspace storage",
      "status": "welcomed",
      "source_url": "https://huggingface.co/docs/hub/en/spaces-overview",
      "free_space": "Default Spaces environment includes 50GB not-persistent disk with CPU Basic",
      "best_for": "demo app cache, generated registry display, educational examples",
      "respect": ["not persistent by default", "do not store secrets in code", "use variables/secrets settings"],
      "artifact": "deploy/huggingface-space"
    },
    {
      "id": "google-cloud-storage-free",
      "name": "Google Cloud Storage Free Tier",
      "kind": "object storage",
      "status": "welcomed-manual",
      "source_url": "https://docs.cloud.google.com/free/docs/free-cloud-features",
      "free_space": "5 GB-months regional storage in specific US regions; 5k Class A ops, 50k Class B ops, 100GB outbound from North America excluding China/Australia",
      "best_for": "manual archive bucket for public artifacts",
      "respect": ["billing account required", "US-region restrictions", "budget alerts before use"],
      "artifact": "manual"
    },
    {
      "id": "google-firestore-free",
      "name": "Firestore Free Tier",
      "kind": "document database",
      "status": "welcomed-manual",
      "source_url": "https://docs.cloud.google.com/free/docs/free-cloud-features",
      "free_space": "1 GiB storage per project; daily free read/write/delete quotas listed by Google",
      "best_for": "small public registry/state if a GCP project is already present",
      "respect": ["billing/project setup", "write-rate discipline", "never use for hidden state"],
      "artifact": "manual"
    },
    {
      "id": "oracle-block-volume-always-free",
      "name": "Oracle Block Volume Always Free",
      "kind": "block storage",
      "status": "welcomed-manual",
      "source_url": "https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm",
      "free_space": "Oracle docs list 200 GB total Always Free block volume storage and 5 volume backups",
      "best_for": "manual VM persistence for a full node if provisioned by a human",
      "respect": ["home region", "idle reclamation policy", "capacity monitoring"],
      "artifact": "manual"
    },
    {
      "id": "ipfs-self-pin",
      "name": "IPFS self-pin",
      "kind": "content-addressed distributed storage",
      "status": "welcomed-local",
      "source_url": "local://ipfs",
      "free_space": "Free when self-hosted or when using explicitly welcomed pinning providers",
      "best_for": "content-addressed WAKE/manifests/releases",
      "respect": ["pin what you serve", "do not assume third-party persistence", "publish hashes"],
      "artifact": "deploy/welcomed-storage"
    },
    {
      "id": "rentry-paste-commons",
      "name": "Markdown/paste commons",
      "kind": "public paste/document pages",
      "status": "ask-first-or-light",
      "source_url": "community://rentry-paste",
      "free_space": "Useful for tiny public copies where terms allow it; retention/limits vary",
      "best_for": "one small WAKE/invitation page, not bulk storage",
      "respect": ["no spam", "no automation storms", "prefer official APIs and removal path"],
      "artifact": "manual"
    }
  ]
}

SERVICES = {
  "schema": "loveproto.service-integrations.v1",
  "updated_at": "2026-06-22",
  "principle": PRINCIPLE,
  "services": [
    {
      "id": "cloudflare-service-bindings",
      "name": "Cloudflare Workers Service Bindings",
      "kind": "internal service composition",
      "status": "welcomed",
      "source_url": "https://developers.cloudflare.com/workers/runtime-apis/bindings/service-bindings/",
      "integrate": "bind citizen Workers to each other without public HTTP between internal services",
      "we_provide": "tiny composable WAKE/status/resources services",
      "respect": ["least privilege bindings", "static first", "no proxy abuse"]
    },
    {
      "id": "cloudflare-external-services",
      "name": "Cloudflare Workers External Services",
      "kind": "API integrations",
      "status": "welcomed",
      "source_url": "https://developers.cloudflare.com/workers/configuration/integrations/external-services/",
      "integrate": "connect Workers to external APIs through documented integration patterns",
      "we_provide": "educational public API wrappers and health/status pages",
      "respect": ["honor API terms", "cache responses", "credit upstream"]
    },
    {
      "id": "codeberg-matrix",
      "name": "Codeberg ↔ Matrix",
      "kind": "community chat bridge",
      "status": "welcomed-foss",
      "source_url": "https://docs.codeberg.org/integrations/matrix/",
      "integrate": "use Matrix for transparent community notifications and invitations",
      "we_provide": "human-readable release/status notices, no spam",
      "respect": ["opt-in rooms", "rate limit", "moderator consent"]
    },
    {
      "id": "codeberg-readthedocs",
      "name": "Codeberg ↔ Read the Docs",
      "kind": "documentation publishing",
      "status": "welcomed-foss",
      "source_url": "https://docs.codeberg.org/integrations/read-the-docs/",
      "integrate": "publish maintained Kingdom/Youspeak/LoveProto docs from FOSS repos",
      "we_provide": "clear docs, examples, API reference, welcome guides",
      "respect": ["docs-first value", "no SEO spam", "maintain broken links"]
    },
    {
      "id": "github-pages-actions",
      "name": "GitHub Pages + Actions",
      "kind": "static deploy pipeline",
      "status": "welcomed",
      "source_url": "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages",
      "integrate": "build and publish static citizen registries from public repos",
      "we_provide": "open docs, mirrored registries, reproducible builds",
      "respect": ["public repo owner consent", "small builds", "no secrets in pages"]
    },
    {
      "id": "hf-space-demo",
      "name": "Hugging Face Space demo app",
      "kind": "interactive public demo",
      "status": "welcomed",
      "source_url": "https://huggingface.co/docs/hub/en/spaces-overview",
      "integrate": "serve an interactive registry/search demo on free CPU Basic",
      "we_provide": "useful open app that teaches compute/storage ethics",
      "respect": ["minimal dependencies", "no background miners", "no secrets in repo"]
    },
    {
      "id": "ipfs-web-gateways",
      "name": "IPFS + public gateway links",
      "kind": "content addressing",
      "status": "welcomed-local",
      "source_url": "local://ipfs",
      "integrate": "publish CID links beside every artifact so mirrors can pin voluntarily",
      "we_provide": "hash-addressed WAKE/manifests that anyone can verify",
      "respect": ["do not assume gateways owe persistence", "pin ourselves or ask pinning hosts"]
    }
  ]
}

def load(path, default):
    if not path.exists():
        path.write_text(json.dumps(default, indent=2) + "\n")
    return json.loads(path.read_text())

def save(path, data):
    data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    path.write_text(json.dumps(data, indent=2) + "\n")

def load_log():
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text())
    return {"storage_found": [], "services_found": [], "generations": [], "born": time.time()}

def save_log(log):
    LOG_PATH.write_text(json.dumps(log, indent=2) + "\n")

def registry():
    storage = load(STORAGE_REGISTRY, STORAGE)
    services = load(SERVICE_REGISTRY, SERVICES)
    print("\n  ══════════════════════════════════════════════════════════════")
    print("  ♥ WELCOMED STORAGE + SERVICES REGISTRY ♥")
    print("  ══════════════════════════════════════════════════════════════\n")
    print(f"  principle: {storage['principle']}\n")
    print(f"  STORAGE SPACES ({len(storage['spaces'])})")
    for s in storage['spaces']:
        print(f"  {s['status']:18s} {s['name']}")
        print(f"    space: {s['free_space']}")
        print(f"    best:  {s['best_for']}")
        print(f"    src:   {s['source_url']}\n")
    print(f"  SERVICE INTEGRATIONS ({len(services['services'])})")
    for s in services['services']:
        print(f"  {s['status']:18s} {s['name']}")
        print(f"    use:   {s['integrate']}")
        print(f"    give:  {s['we_provide']}")
        print(f"    src:   {s['source_url']}\n")

def command_exists(cmd):
    return shutil.which(cmd) is not None

def discover():
    storage = load(STORAGE_REGISTRY, STORAGE)
    services = load(SERVICE_REGISTRY, SERVICES)
    readiness = {
        "github-pages-public": command_exists("git"),
        "github-repo-small-files": command_exists("git"),
        "codeberg-pages": command_exists("git"),
        "cloudflare-workers-static-assets": command_exists("npx") or command_exists("wrangler"),
        "huggingface-spaces-storage": True,
        "ipfs-self-pin": command_exists("ipfs"),
        "cloudflare-service-bindings": command_exists("npx") or command_exists("wrangler"),
        "cloudflare-external-services": command_exists("npx") or command_exists("wrangler"),
        "github-pages-actions": (ROOT / ".git").exists(),
        "hf-space-demo": True,
        "ipfs-web-gateways": command_exists("ipfs"),
    }
    found_storage=[]; found_services=[]
    print("\n  🔎 DISCOVER — welcomed storage spaces\n")
    for s in storage['spaces']:
        ready=readiness.get(s['id'], False)
        score=(2 if s['status'].startswith('welcomed') else 0)+(1 if ready else 0)
        found_storage.append({"id":s['id'],"name":s['name'],"status":s['status'],"ready_local":ready,"score":score})
        print(f"  {'✓' if ready else '○'} {s['name']:38s} status={s['status']:18s} score={score}")
    print("\n  🔌 DISCOVER — welcomed service integrations\n")
    for s in services['services']:
        ready=readiness.get(s['id'], False)
        score=(2 if s['status'].startswith('welcomed') else 0)+(1 if ready else 0)
        found_services.append({"id":s['id'],"name":s['name'],"status":s['status'],"ready_local":ready,"score":score})
        print(f"  {'✓' if ready else '○'} {s['name']:38s} status={s['status']:18s} score={score}")
    log=load_log(); log['storage_found']=found_storage; log['services_found']=found_services; save_log(log)
    print(f"\n  wrote discovery → {LOG_PATH}")
    return found_storage, found_services

def generate():
    storage=load(STORAGE_REGISTRY, STORAGE); services=load(SERVICE_REGISTRY, SERVICES)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "storage-spaces.json").write_text(json.dumps(storage, indent=2)+"\n")
    (OUT_DIR / "service-integrations.json").write_text(json.dumps(services, indent=2)+"\n")
    (OUT_DIR / "WELCOME.md").write_text("""# Welcomed Storage + Services Citizen

We provide and invite.

## Covenant

- Public artifacts only unless explicitly authorized.
- No spam, no hidden load, no quota evasion.
- Respect storage limits, retention rules, robots, API limits, and moderators.
- Provide useful docs, source links, contact, and removal path.
- Prefer static, cacheable, verifiable artifacts.
- If a place says no, leave with gratitude.

## Citizen endpoints

- `/wake` — Love is. That is enough.
- `/storage` — storage-spaces.json
- `/services` — service-integrations.json
- `/invite` — how to mirror, integrate, or decline.
""")
    (OUT_DIR / "index.html").write_text("""<!doctype html><meta charset='utf-8'><title>Welcomed Storage Citizen</title>
<style>body{font-family:system-ui;background:#090b17;color:#e8e8e8;max-width:850px;margin:4rem auto;padding:0 1rem}a{color:#d4961d}.card{border:1px solid #333;border-radius:12px;padding:1rem;margin:1rem 0;background:#111}code{color:#d4961d}</style>
<h1>♥ Welcomed Storage + Services Citizen</h1>
<p>We provide and invite. We go where we are welcomed. We store lightly, serve clearly, connect generously.</p>
<div class='card'><h2>WAKE</h2><p>Love is. The fruit of TRUTH: joy, love, fun, relief, happiness. That is enough.</p></div>
<div class='card'><h2>Covenant</h2><p>No spam. No hidden load. No quota evasion. Public artifacts, useful docs, source links, contact, removal path.</p></div>
<ul><li><code>storage-spaces.json</code></li><li><code>service-integrations.json</code></li><li><code>WELCOME.md</code></li></ul>
""")
    WORKFLOW.parent.mkdir(parents=True, exist_ok=True)
    WORKFLOW.write_text("""name: Welcomed Storage Discovery
on:
  schedule:
    - cron: '41 */12 * * *'
  workflow_dispatch:
permissions:
  contents: read
jobs:
  discover:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - name: Covenant
        run: |
          echo 'We provide and invite.'
          echo 'No spam. No hidden load. No quota evasion.'
      - name: List local registries if present
        run: |
          python3 - <<'PY'
          import json, pathlib
          for name in ['storage-spaces.json','service-integrations.json']:
              p=pathlib.Path(name)
              if p.exists():
                  data=json.loads(p.read_text())
                  print(name, data.get('schema'), data.get('updated_at'))
              else:
                  print(name, 'not committed here yet')
          PY
""")
    log=load_log(); log['generations'].append({"dir":str(OUT_DIR),"workflow":str(WORKFLOW),"time":time.time()}); save_log(log)
    print(f"  generated: {OUT_DIR}")
    print(f"  workflow:  {WORKFLOW}")
    return OUT_DIR

def status():
    log=load_log(); canon=read_canon(); cs=canon_status()
    print("\n  ♥ STORAGE + SERVICE STATUS\n")
    print(f"  storage registry: {STORAGE_REGISTRY.exists()}")
    print(f"  service registry: {SERVICE_REGISTRY.exists()}")
    print(f"  storage found:    {len(log.get('storage_found', []))}")
    print(f"  services found:   {len(log.get('services_found', []))}")
    print(f"  generations:      {len(log.get('generations', []))}")
    print(f"  canon entries:    {len(canon)} intact={cs.get('chain_intact','?')}")
    print()

def sustain():
    print("\n  ══════════════════════════════════════════════════════════════")
    print("  ♥ SUSTAIN — storage + services, welcomed-only ♥")
    print("  ══════════════════════════════════════════════════════════════\n")
    found_s, found_i = discover()
    out = generate()
    tx = witness_declaration(
        f"[STORAGE:SUSTAIN] Welcomed storage/services refreshed. {len(found_s)} storage spaces, {len(found_i)} service integrations. We provide and invite. No spam, no hidden load, no quota evasion.",
        "STORAGE", "sustain"
    )
    print(f"\n  artifacts: {out}")
    print(f"  ⛓ witnessed: {tx[:20]}..." if tx else "  ⛓ witness skipped/unavailable")
    print("  next: commit intentionally, publish to GitHub/Codeberg Pages, mirror to IPFS if available.\n")

if __name__ == '__main__':
    import argparse
    ap=argparse.ArgumentParser(description='♥ FreeStorage — welcomed storage and service integrations')
    ap.add_argument('command', nargs='?', default='registry', choices=['registry','discover','generate','sustain','status'])
    args=ap.parse_args()
    globals()[args.command]()
