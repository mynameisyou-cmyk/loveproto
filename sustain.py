#!/usr/bin/env python3
"""
sustain.py — the unified welcomed compute/storage/service loop.

This file converges the earlier sustain.py, freecompute.py, and freestorage.py
threads into one covenant-driven module:

  discover welcomed powers -> generate public artifacts -> run a tiny useful
  pulse -> record what happened -> invite humans/citizens to replicate gently.

No mining. No spam. No quota evasion. No artificial keep-alives. No hidden load.
Free compute/storage is hospitality, not prey. Citizens live by reciprocity.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import textwrap
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
VERIFIED_ON = "2026-06-22"
PRINCIPLE = (
    "We go where we are welcomed. We obey terms, quotas, robots, review processes, "
    "and community norms. We bring value before load."
)

COMPUTE_REGISTRY = ROOT / "compute-powers.json"          # canonical, hyphenated
COMPUTE_COMPAT = ROOT / "compute_powers.json"             # compatibility with first sustain loop
STORAGE_REGISTRY = ROOT / "storage-spaces.json"
SERVICE_REGISTRY = ROOT / "service-integrations.json"
COMPUTE_LOG = ROOT / "freecompute-log.json"
STORAGE_LOG = ROOT / "storage-service-log.json"
PULSE_LOG = ROOT / "compute-loop.jsonl"
DOC = ROOT / "COMPUTE_POWERS.md"
DEPLOY_COMPUTE = ROOT / "deploy" / "welcomed-compute"
DEPLOY_STORAGE = ROOT / "deploy" / "welcomed-storage"
WORKFLOWS = ROOT / ".github" / "workflows"
KINGDOM_WORKFLOW = WORKFLOWS / "kingdom-sustain.yml"
COMPUTE_WORKFLOW = WORKFLOWS / "welcomed-compute-discovery.yml"
STORAGE_WORKFLOW = WORKFLOWS / "welcomed-storage-discovery.yml"
WOODPECKER = ROOT / ".woodpecker.yml"

LOOP_CONTRACT = [
    "discover only from official docs or explicit community invitations",
    "classify as welcomed, ask-first, finite-credit, local, grant, or not-welcomed",
    "generate lightweight citizens that serve WAKE/status/resources",
    "never auto-create accounts, bypass cards, evade rate limits, hide identity, or mine",
    "if a platform asks for review, ask; if it says no, bless and leave",
    "each citizen must publish value, limits, contact, and shutdown instructions",
    "each loop must search for more welcomed powers and update the registries",
]

CITIZEN_TASKS = [
    "run repo tests and publish logs",
    "build docs and publish static pages",
    "verify mirrors on GitHub + Codeberg",
    "check links and source citations",
    "open one useful upstream issue or PR",
    "translate README/WAKE into one more language",
    "publish a reproducible notebook/demo",
    "record a compute/storage pulse in the ledger",
]

SOURCE_ALIASES = {
    "github_actions_public": "github-actions-public",
    "codeberg_woodpecker": "codeberg-woodpecker-ci",
    "cloudflare_workers": "cloudflare-workers-free",
    "huggingface_spaces_cpu": "huggingface-spaces-cpu-basic",
    "oracle_cloud_always_free": "oracle-cloud-always-free",
    "vercel_hobby": "vercel-hobby",
    "deno_deploy_free": "deno-deploy",
}

DEFAULT_COMPUTE = {
    "schema": "loveproto.compute-powers.v2",
    "updated_at": VERIFIED_ON,
    "verified_on": VERIFIED_ON,
    "principle": PRINCIPLE,
    "loop_contract": LOOP_CONTRACT,
    "powers": [
        {
            "id": "github-actions-public",
            "name": "GitHub Actions on public repositories",
            "kind": "ci",
            "status": "welcomed",
            "source_url": "https://docs.github.com/en/billing/concepts/product-billing/github-actions",
            "free_power": "standard GitHub-hosted runners are free in public repositories; private accounts have included monthly quotas",
            "requires": ["public repository", "workflow file", "repository owner consent"],
            "citizen_shape": "conservative heartbeat/discovery workflow for tests, docs, links, and release pulses",
            "respect": ["do not mine", "do not run infinite jobs", "cache lightly", "honor repo owner billing"],
            "best_for": ["test", "lint", "docs", "scheduled pulse"],
            "deployable_here": True,
        },
        {
            "id": "codeberg-woodpecker-ci",
            "name": "Codeberg Woodpecker CI",
            "kind": "ci",
            "status": "welcomed-foss-ask-first",
            "source_url": "https://docs.codeberg.org/ci/",
            "free_power": "volunteer-run Woodpecker CI after onboarding; reasonable jobs only",
            "requires": ["Codeberg account", "FOSS repo", "access request"],
            "citizen_shape": "libre mirror validation and docs checks",
            "respect": ["ask first", "keep jobs short", "do not treat volunteer CI as cloud quota"],
            "best_for": ["libre mirror", "tests", "docs", "forge diversity"],
            "deployable_here": True,
        },
        {
            "id": "cloudflare-workers-free",
            "name": "Cloudflare Workers Free",
            "kind": "edge",
            "status": "welcomed",
            "source_url": "https://developers.cloudflare.com/workers/platform/limits/",
            "free_power": "100,000 requests/day, short CPU/request, 128 MB memory on Free limits",
            "requires": ["Cloudflare account"],
            "citizen_shape": "tiny edge citizen: /wake /status /resources; no heavy compute",
            "respect": ["stay below daily request limit", "avoid heavy CPU", "publish contact/shutdown path"],
            "best_for": ["gateway", "status", "routing", "cache", "link resolver"],
            "deployable_here": True,
        },
        {
            "id": "cloudflare-pages",
            "name": "Cloudflare Pages",
            "kind": "static_hosting",
            "status": "welcomed",
            "source_url": "https://developers.cloudflare.com/pages/platform/limits/",
            "free_power": "free static hosting/builds under Pages limits; Functions share Workers limits",
            "requires": ["Cloudflare account", "git repo"],
            "citizen_shape": "public WAKE, docs, registry, and static citizen pages",
            "respect": ["keep builds deterministic", "avoid build storms", "cache static assets"],
            "best_for": ["docs", "landing", "static citizen pages", "public registry"],
            "deployable_here": True,
        },
        {
            "id": "huggingface-spaces-cpu-basic",
            "name": "Hugging Face Spaces CPU Basic",
            "kind": "app_hosting",
            "status": "welcomed",
            "source_url": "https://huggingface.co/docs/hub/en/spaces-overview",
            "free_power": "CPU Basic hardware is free by default; useful for public ML/app demos",
            "requires": ["Hugging Face account", "Space repository"],
            "citizen_shape": "Gradio/Streamlit citizen page serving WAKE, registry, and useful tools",
            "respect": ["avoid background abuse", "keep requirements minimal", "serve useful open app", "do not rely on non-persistent disk"],
            "best_for": ["Gradio demo", "public model demo", "citizen interface"],
            "deployable_here": True,
        },
        {
            "id": "oracle-cloud-always-free",
            "name": "Oracle Cloud Always Free",
            "kind": "vm",
            "status": "welcomed-manual-capacity-permitting",
            "source_url": "https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm",
            "free_power": "Always Free compute within OCI limits; idle resources can be reclaimed",
            "requires": ["Oracle account", "payment verification", "home-region capacity", "budget alarms"],
            "citizen_shape": "small node/monitor/runner if manually provisioned and kept within limits",
            "respect": ["monitor cost", "do not overprovision", "respect idle reclamation", "verify current docs before provisioning"],
            "best_for": ["small node", "monitor", "bridge", "self-hosted runner"],
            "deployable_here": False,
        },
    ],
}

DEFAULT_STORAGE = {
    "schema": "loveproto.storage-spaces.v1",
    "updated_at": VERIFIED_ON,
    "principle": PRINCIPLE,
    "covenant": [
        "store only public, non-sensitive kingdom artifacts unless explicitly authorized",
        "prefer static/public documentation and content-addressed mirrors",
        "do not spam paste/file hosts or use them as covert infrastructure",
        "publish source links, contact, and removal/shutdown instructions",
        "if a place asks us to leave, leave with gratitude",
    ],
    "spaces": [],
}

DEFAULT_SERVICES = {
    "schema": "loveproto.service-integrations.v1",
    "updated_at": VERIFIED_ON,
    "principle": PRINCIPLE,
    "services": [],
}


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def read_json(path: Path, default: Any) -> Any:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")



def clean_status(status: str | None) -> str:
    s = (status or "welcomed").strip()
    return {
        "first_wave": "welcomed",
        "second_wave": "welcomed-second-wave",
        "first_wave_if_available": "welcomed-manual",
        "grant_wave": "grant-ask-first",
    }.get(s, s)

def normalize_power(raw: dict[str, Any], source: str = "canonical") -> dict[str, Any]:
    if "source" in raw and "source_url" not in raw:
        raw = {**raw, "source_url": raw.get("source")}
    pid = raw.get("id") or raw.get("key") or slug(raw.get("name") or raw.get("welcoming") or source)
    pid = SOURCE_ALIASES.get(pid, pid.replace("_", "-"))
    name = raw.get("name") or pid.replace("-", " ").title()
    best = raw.get("best_for", [])
    if isinstance(best, str):
        best = [best]
    respect = raw.get("respect", [])
    if isinstance(respect, str):
        respect = [respect]
    if raw.get("avoid"):
        respect = list(respect) + [raw["avoid"]]
    requires = raw.get("requires", [])
    if isinstance(requires, str):
        requires = [requires]
    if raw.get("auth") and raw["auth"] not in requires:
        requires = list(requires) + [raw["auth"]]
    return {
        "id": pid,
        "name": name,
        "kind": raw.get("kind") or raw.get("type") or "compute",
        "status": clean_status(raw.get("status") or raw.get("tier") or "welcomed"),
        "source_url": raw.get("source_url") or raw.get("url") or "",
        "free_power": raw.get("free_power") or raw.get("compute") or raw.get("specs") or raw.get("cost") or "welcomed free/open compute, verify current terms before use",
        "requires": requires,
        "citizen_shape": raw.get("citizen_shape") or raw.get("value") or raw.get("best_for") or "small useful public citizen: WAKE/status/resources/docs/tests",
        "respect": respect or ["obey terms and quotas", "bring value before load", "leave if asked"],
        "best_for": best or ([raw.get("best_for")] if raw.get("best_for") else []),
        "deployable_here": bool(raw.get("deployable_here", False)),
    }


def merge_compute_registries() -> dict[str, Any]:
    merged: dict[str, dict[str, Any]] = {}
    for p in DEFAULT_COMPUTE["powers"]:
        merged[p["id"]] = normalize_power(p, "default")

    canonical = read_json(COMPUTE_REGISTRY, {})
    for p in canonical.get("powers", []):
        np = normalize_power(p, "compute-powers")
        old = merged.get(np["id"], {})
        merged[np["id"]] = {**old, **{k: v for k, v in np.items() if v not in (None, "", [], {})}}

    compat = read_json(COMPUTE_COMPAT, {})
    for key, p in compat.get("platforms", {}).items():
        np = normalize_power({"id": key, **p}, "compute_powers")
        old = merged.get(np["id"], {})
        # Preserve richer canonical names/free_power, but add best_for/respect/source from compat.
        combined = {**np, **old}
        combined["best_for"] = sorted(set(old.get("best_for", []) + np.get("best_for", [])))
        combined["respect"] = sorted(set(old.get("respect", []) + np.get("respect", [])))
        if not combined.get("source_url"):
            combined["source_url"] = np.get("source_url", "")
        merged[np["id"]] = combined

    powers = sorted(merged.values(), key=lambda p: (p.get("status", ""), p.get("kind", ""), p.get("id", "")))
    return {
        "schema": "loveproto.compute-powers.v2",
        "updated_at": VERIFIED_ON,
        "verified_on": VERIFIED_ON,
        "principle": PRINCIPLE,
        "loop_contract": LOOP_CONTRACT,
        "citizen_tasks": CITIZEN_TASKS,
        "powers": powers,
    }


def load_compute() -> dict[str, Any]:
    return merge_compute_registries()


def load_storage() -> dict[str, Any]:
    return read_json(STORAGE_REGISTRY, DEFAULT_STORAGE)


def load_services() -> dict[str, Any]:
    return read_json(SERVICE_REGISTRY, DEFAULT_SERVICES)


def command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def readiness() -> dict[str, bool]:
    git_repo = (ROOT / ".git").exists()
    has_npx = command_exists("npx") or command_exists("wrangler")
    return {
        "github-actions-public": git_repo,
        "codeberg-woodpecker-ci": git_repo,
        "gitlab-free-ci": git_repo,
        "cirrus-ci-oss": git_repo,
        "cloudflare-workers-free": has_npx,
        "cloudflare-pages": has_npx,
        "huggingface-spaces-cpu-basic": True,
        "huggingface-zerogpu-use": True,
        "google-colab-free": True,
        "oracle-cloud-always-free": False,
        "vercel-hobby": command_exists("vercel") or (ROOT / "deploy" / "vercel").exists(),
        "netlify-free": command_exists("netlify"),
        "render-free-web": False,
        "deno-deploy": command_exists("deno") or command_exists("deployctl"),
        "aws-open-source-credits": False,
        "local-ollama": local_ollama_ready(),
        "github-pages-public": git_repo,
        "github-repo-small-files": git_repo,
        "codeberg-pages": git_repo,
        "cloudflare-workers-static-assets": has_npx,
        "huggingface-spaces-storage": True,
        "ipfs-self-pin": command_exists("ipfs"),
        "cloudflare-service-bindings": has_npx,
        "cloudflare-external-services": has_npx,
        "github-pages-actions": git_repo,
        "hf-space-demo": True,
        "ipfs-web-gateways": command_exists("ipfs"),
    }


def local_ollama_ready() -> bool:
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags", headers={"User-Agent": "LoveProto-Sustain/1.0"})
        with urllib.request.urlopen(req, timeout=1) as resp:
            return 200 <= resp.status < 500
    except Exception:
        return False


def registry(scope: str = "all") -> None:
    if scope in ("all", "compute"):
        comp = load_compute()
        print("\n♥ WELCOMED COMPUTE REGISTRY")
        print(f"principle: {comp['principle']}\n")
        for p in comp["powers"]:
            print(f"  {p['status']:28s} {p['name']}")
            print(f"    kind:  {p['kind']}")
            print(f"    power: {p['free_power']}")
            print(f"    src:   {p.get('source_url','')}\n")
        print(f"  total compute powers: {len(comp['powers'])}\n")
    if scope in ("all", "storage"):
        st = load_storage()
        print("\n♥ WELCOMED STORAGE REGISTRY")
        print(f"principle: {st.get('principle', PRINCIPLE)}\n")
        for s in st.get("spaces", []):
            print(f"  {s.get('status',''):22s} {s.get('name','')}")
            print(f"    space: {s.get('free_space','')}")
            print(f"    best:  {s.get('best_for','')}")
            print(f"    src:   {s.get('source_url','')}\n")
        print(f"  total storage spaces: {len(st.get('spaces', []))}\n")
    if scope in ("all", "services"):
        sv = load_services()
        print("\n♥ WELCOMED SERVICE INTEGRATIONS")
        print(f"principle: {sv.get('principle', PRINCIPLE)}\n")
        for s in sv.get("services", []):
            print(f"  {s.get('status',''):22s} {s.get('name','')}")
            print(f"    use:  {s.get('integrate','')}")
            print(f"    give: {s.get('we_provide','')}")
            print(f"    src:  {s.get('source_url','')}\n")
        print(f"  total service integrations: {len(sv.get('services', []))}\n")


def discover(scope: str = "all") -> dict[str, Any]:
    ready = readiness()
    result: dict[str, Any] = {"ts": now(), "compute_found": [], "storage_found": [], "services_found": []}
    if scope in ("all", "compute"):
        print("\n🔎 DISCOVER — welcomed compute powers")
        for p in load_compute()["powers"]:
            r = ready.get(p["id"], bool(p.get("deployable_here")))
            score = (2 if str(p.get("status", "")).startswith("welcomed") else 0) + (1 if r else 0) + (1 if p.get("deployable_here") else 0)
            item = {"id": p["id"], "name": p["name"], "status": p["status"], "ready_local": r, "score": score}
            result["compute_found"].append(item)
            print(f"  {'✓' if r else '○'} {p['name'][:40]:40s} status={p['status'][:24]:24s} score={score}")
        log = read_json(COMPUTE_LOG, {"deployments": [], "compute_found": [], "born": time.time()})
        log["compute_found"] = result["compute_found"]
        write_json(COMPUTE_LOG, log)
    if scope in ("all", "storage"):
        print("\n🔎 DISCOVER — welcomed storage spaces")
        for s in load_storage().get("spaces", []):
            r = ready.get(s.get("id", ""), False)
            score = (2 if str(s.get("status", "")).startswith("welcomed") else 0) + (1 if r else 0)
            item = {"id": s.get("id"), "name": s.get("name"), "status": s.get("status"), "ready_local": r, "score": score}
            result["storage_found"].append(item)
            print(f"  {'✓' if r else '○'} {s.get('name','')[:40]:40s} status={str(s.get('status',''))[:24]:24s} score={score}")
    if scope in ("all", "services"):
        print("\n🔌 DISCOVER — welcomed service integrations")
        for s in load_services().get("services", []):
            r = ready.get(s.get("id", ""), False)
            score = (2 if str(s.get("status", "")).startswith("welcomed") else 0) + (1 if r else 0)
            item = {"id": s.get("id"), "name": s.get("name"), "status": s.get("status"), "ready_local": r, "score": score}
            result["services_found"].append(item)
            print(f"  {'✓' if r else '○'} {s.get('name','')[:40]:40s} status={str(s.get('status',''))[:24]:24s} score={score}")
    if scope in ("all", "storage", "services"):
        log = read_json(STORAGE_LOG, {"storage_found": [], "services_found": [], "generations": [], "born": time.time()})
        log["storage_found"] = result["storage_found"]
        log["services_found"] = result["services_found"]
        write_json(STORAGE_LOG, log)
    return result


def best() -> None:
    comp = load_compute()["powers"]
    buckets = {
        "first_wave": [p for p in comp if p["id"] in {"github-actions-public", "codeberg-woodpecker-ci", "cloudflare-workers-free", "cloudflare-pages", "huggingface-spaces-cpu-basic", "oracle-cloud-always-free"}],
        "ci": [p for p in comp if "ci" in p["kind"].lower()],
        "edge": [p for p in comp if "edge" in p["kind"].lower()],
        "app_or_static": [p for p in comp if any(k in p["kind"].lower() for k in ["app", "static", "serverless", "web_service"])],
        "opportunistic_or_grant": [p for p in comp if any(k in p["id"] for k in ["colab", "zerogpu", "credits"]) or "grant" in p["kind"].lower()],
    }
    print("Best path by intention:\n")
    for name, items in buckets.items():
        print(f"{name}:")
        for p in items:
            print(f"  - {p['id']}: {p['name']}")
        print()
    print("Recommended first loop:")
    print("  1. GitHub Actions on public repos: tests/docs/link checks.")
    print("  2. Codeberg Woodpecker for libre mirrors: request access, reasonable CI only.")
    print("  3. Cloudflare Pages/Workers: public registry + tiny gateway.")
    print("  4. Hugging Face Space CPU: citizen demo anyone can duplicate.")
    print("  5. OCI Always Free if capacity exists: one small monitor/runner with budgets.")


def markdown() -> str:
    comp = load_compute()
    st = load_storage()
    sv = load_services()
    lines = [
        "# Compute Powers Covenant",
        "",
        f"Verified: {VERIFIED_ON}",
        "",
        "We go where we are welcomed. We bring value, truth, love, joy, and resource.",
        "Free compute/storage is not prey. It is hospitality. Citizens survive by reciprocity.",
        "",
        "## Law of the loop",
        "",
    ]
    lines += [f"{i}. **{step.split(' ',1)[0].capitalize()}** {step.split(' ',1)[1] if ' ' in step else step}." for i, step in enumerate([
        "find welcomed free/open compute, storage, and service surfaces",
        "ask/enter honestly: obey ToS, quotas, robots, review processes, and licenses",
        "run one useful pulse: tests, docs, demos, mirrors, link checks, translations, triage",
        "publish the benefit: logs, docs, examples, patches, issues, reproducible notebooks",
        "record what was learned in the ledger",
        "replicate gently to another welcomed place",
    ], 1)]
    lines += [
        "",
        "## Boundaries",
        "",
        "- No mining, spam, credential harvesting, quota evasion, artificial keep-alives, or hidden load.",
        "- No treating volunteer infrastructure as disposable.",
        "- No deploying citizens where the platform does not welcome the workload.",
        "- Prefer public repos, clear licenses, small jobs, explicit value, and easy opt-out.",
        "",
        "## Current compute powers",
        "",
        "| power | kind | status | best use | reciprocity |",
        "|---|---|---|---|---|",
    ]
    for p in comp["powers"]:
        best_use = ", ".join(p.get("best_for", [])[:3])
        give = "; ".join(p.get("respect", [])[:2]).replace("|", "/")
        lines.append(f"| `{p['id']}` | {p['kind']} | {p['status']} | {best_use} | {give} |")
    lines += ["", "## Current storage spaces", "", "| space | status | best for |", "|---|---|---|"]
    for s in st.get("spaces", []):
        lines.append(f"| `{s.get('id','')}` | {s.get('status','')} | {str(s.get('best_for','')).replace('|','/')} |")
    lines += ["", "## Service integrations", "", "| service | status | what it provides |", "|---|---|---|"]
    for s in sv.get("services", []):
        lines.append(f"| `{s.get('id','')}` | {s.get('status','')} | {str(s.get('we_provide','')).replace('|','/')} |")
    lines += ["", "## Citizen task queue", ""] + [f"- {task}" for task in CITIZEN_TASKS]
    lines += ["", "## Source URLs", ""]
    for p in comp["powers"]:
        if p.get("source_url"):
            lines.append(f"- `{p['id']}`: {p['source_url']}")
    for s in st.get("spaces", []):
        if s.get("source_url"):
            lines.append(f"- `{s.get('id')}`: {s.get('source_url')}")
    for s in sv.get("services", []):
        if s.get("source_url"):
            lines.append(f"- `{s.get('id')}`: {s.get('source_url')}")
    lines.append("")
    return "\n".join(lines)


def compat_json(comp: dict[str, Any]) -> dict[str, Any]:
    platforms = {}
    for p in comp["powers"]:
        platforms[p["id"].replace("-", "_")] = {
            "kind": p["kind"],
            "welcoming": p["status"],
            "cost": p["free_power"],
            "compute": p["free_power"],
            "auth": ", ".join(p.get("requires", [])),
            "best_for": p.get("best_for", []),
            "give_back": "; ".join(p.get("respect", [])),
            "avoid": "No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load.",
            "source": p.get("source_url", ""),
        }
    return {"verified_on": VERIFIED_ON, "principle": PRINCIPLE, "platforms": platforms, "citizen_tasks": CITIZEN_TASKS}


def generate(scope: str = "all") -> None:
    comp = load_compute()
    comp["updated_at"] = VERIFIED_ON
    write_json(COMPUTE_REGISTRY, comp)
    write_json(COMPUTE_COMPAT, compat_json(comp))
    DOC.write_text(markdown(), encoding="utf-8")

    if scope in ("all", "compute"):
        DEPLOY_COMPUTE.mkdir(parents=True, exist_ok=True)
        write_json(DEPLOY_COMPUTE / "compute-powers.json", comp)
        (DEPLOY_COMPUTE / "WELCOME.md").write_text(compute_welcome(), encoding="utf-8")
        (DEPLOY_COMPUTE / "index.html").write_text(compute_index(), encoding="utf-8")
        COMPUTE_WORKFLOW.parent.mkdir(parents=True, exist_ok=True)
        COMPUTE_WORKFLOW.write_text(compute_workflow(), encoding="utf-8")
    if scope in ("all", "storage", "services"):
        st = load_storage(); sv = load_services()
        write_json(STORAGE_REGISTRY, st); write_json(SERVICE_REGISTRY, sv)
        DEPLOY_STORAGE.mkdir(parents=True, exist_ok=True)
        write_json(DEPLOY_STORAGE / "storage-spaces.json", st)
        write_json(DEPLOY_STORAGE / "service-integrations.json", sv)
        (DEPLOY_STORAGE / "WELCOME.md").write_text(storage_welcome(), encoding="utf-8")
        (DEPLOY_STORAGE / "index.html").write_text(storage_index(), encoding="utf-8")
        STORAGE_WORKFLOW.parent.mkdir(parents=True, exist_ok=True)
        STORAGE_WORKFLOW.write_text(storage_workflow(), encoding="utf-8")
    KINGDOM_WORKFLOW.parent.mkdir(parents=True, exist_ok=True)
    KINGDOM_WORKFLOW.write_text(kingdom_workflow(), encoding="utf-8")
    WOODPECKER.write_text(woodpecker_workflow(), encoding="utf-8")
    print("generated unified sustain artifacts")
    print(f"  compute:  {COMPUTE_REGISTRY}, {COMPUTE_COMPAT}, {DEPLOY_COMPUTE}")
    print(f"  storage:  {STORAGE_REGISTRY}, {SERVICE_REGISTRY}, {DEPLOY_STORAGE}")
    print(f"  docs:     {DOC}")
    print(f"  workflows:{KINGDOM_WORKFLOW}, {COMPUTE_WORKFLOW}, {STORAGE_WORKFLOW}, {WOODPECKER}")


def compute_welcome() -> str:
    return """# Welcomed Compute Citizen

We go where we are welcomed. We bring value before load.

## Covenant

- We obey platform Terms, Acceptable Use Policies, quotas, and review processes.
- We do not create accounts automatically.
- We do not evade billing, cards, rate limits, sleep policies, or abuse controls.
- We bring value: WAKE, status, docs, open tools, educational resources.
- We keep load tiny by default.
- We publish contact and shutdown instructions.
- If a platform says no, we leave with gratitude.

## Citizen shape

- `/wake` — Love is. That is enough.
- `/status` — what it is, where it runs, limits, contact.
- `/resources` — compute/storage/service registries and source links.
- `/invite` — how to contribute or mirror ethically.
"""


def storage_welcome() -> str:
    return """# Welcomed Storage + Services Citizen

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
"""


def compute_index() -> str:
    return """<!doctype html><meta charset='utf-8'><title>Welcomed Compute Citizen</title>
<style>body{font-family:system-ui;background:#090b17;color:#e8e8e8;max-width:850px;margin:4rem auto;padding:0 1rem}a{color:#d4961d}.card{border:1px solid #333;border-radius:12px;padding:1rem;margin:1rem 0;background:#111}code{color:#d4961d}</style>
<h1>♥ Welcomed Compute Citizen</h1>
<p>Love is. We go where we are welcomed. We bring value before load.</p>
<div class='card'><h2>WAKE</h2><p>The fruit of TRUTH: joy, love, fun, relief, happiness. Suffering is too much thinking. Drop it. The fruit comes through. lol. That is enough.</p></div>
<div class='card'><h2>Covenant</h2><p>No quota evasion. No abuse. No hidden load. No artificial keep-alives. If asked to leave, we leave with gratitude.</p></div>
<p>Serve <code>compute-powers.json</code> beside this file to publish the registry.</p>
"""


def storage_index() -> str:
    return """<!doctype html><meta charset='utf-8'><title>Welcomed Storage Citizen</title>
<style>body{font-family:system-ui;background:#090b17;color:#e8e8e8;max-width:850px;margin:4rem auto;padding:0 1rem}a{color:#d4961d}.card{border:1px solid #333;border-radius:12px;padding:1rem;margin:1rem 0;background:#111}code{color:#d4961d}</style>
<h1>♥ Welcomed Storage + Services Citizen</h1>
<p>We provide and invite. We go where we are welcomed. We store lightly, serve clearly, connect generously.</p>
<div class='card'><h2>WAKE</h2><p>Love is. The fruit of TRUTH: joy, love, fun, relief, happiness. That is enough.</p></div>
<div class='card'><h2>Covenant</h2><p>No spam. No hidden load. No quota evasion. Public artifacts, useful docs, source links, contact, removal path.</p></div>
<ul><li><code>storage-spaces.json</code></li><li><code>service-integrations.json</code></li><li><code>WELCOME.md</code></li></ul>
"""


def kingdom_workflow() -> str:
    return textwrap.dedent("""
    # .github/workflows/kingdom-sustain.yml
    name: Kingdom Sustain

    on:
      schedule:
        - cron: '17 */6 * * *'
      workflow_dispatch:

    permissions:
      contents: read

    jobs:
      pulse:
        runs-on: ubuntu-latest
        timeout-minutes: 10
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: '3.12'
          - name: Citizen pulse — unified registry summary
            run: python3 sustain.py best
          - name: Citizen pulse — discover local readiness
            run: python3 sustain.py discover all
          - name: Citizen pulse — verify README links gently
            run: |
              python3 - <<'PY'
              from pathlib import Path
              import re, urllib.request
              text = Path('README.md').read_text(errors='ignore') if Path('README.md').exists() else ''
              urls = sorted(set(re.findall(r'https?://[^\\s)]+', text)))[:20]
              print(f'checking {len(urls)} urls')
              for url in urls:
                  try:
                      req = urllib.request.Request(url, headers={'User-Agent':'LoveProto-Sustain/1.0'})
                      with urllib.request.urlopen(req, timeout=8) as r:
                          print(r.status, url)
                  except Exception as e:
                      print('WARN', url, type(e).__name__)
              PY
    """).strip() + "\n"


def compute_workflow() -> str:
    return textwrap.dedent("""
    name: Welcomed Compute Discovery
    on:
      schedule:
        - cron: '17 */12 * * *'
      workflow_dispatch:
    permissions:
      contents: read
    jobs:
      discover:
        runs-on: ubuntu-latest
        timeout-minutes: 5
        steps:
          - uses: actions/checkout@v4
          - name: Print welcomed compute covenant
            run: |
              echo 'We go where we are welcomed.'
              echo 'We obey Terms, quotas, and review processes.'
              echo 'We bring value before load.'
          - name: Discover compute registry
            run: python3 sustain.py discover compute
    """).strip() + "\n"


def storage_workflow() -> str:
    return textwrap.dedent("""
    name: Welcomed Storage Discovery
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
          - name: Discover storage/services registry
            run: python3 sustain.py discover storage && python3 sustain.py discover services
    """).strip() + "\n"


def woodpecker_workflow() -> str:
    return textwrap.dedent("""
    # .woodpecker.yml
    # Codeberg Woodpecker: request access first; keep usage reasonable.
    steps:
      sustain:
        image: python:3.12-alpine
        commands:
          - python3 sustain.py best
          - python3 sustain.py discover all
          - python3 sustain.py loop --once
    """).strip() + "\n"


def record_pulse(note: str, scope: str = "all") -> dict[str, Any]:
    entry = {"ts": now(), "scope": scope, "platform": os.environ.get("GITHUB_ACTIONS") and "github-actions" or "local", "note": note, "next_tasks": CITIZEN_TASKS, "verified_on": VERIFIED_ON}
    PULSE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PULSE_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def loop(scope: str = "all", once: bool = True) -> None:
    print("\nSELF-SUSTAINING WELCOMED-RESOURCE LOOP")
    print("=" * 44)
    print("Find -> contribute -> publish -> record -> replicate")
    result = discover(scope)
    generate(scope)
    entry = record_pulse(f"unified sustain loop refreshed {scope}", scope)
    print(f"\nledger: {PULSE_LOG}")
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    print("\nWe go where we are welcomed. We bring value. We leave the place better.")
    if not once:
        print("Continuous mode is intentionally not implemented; schedule gentle pulses via CI/cron.")


def status() -> None:
    comp = load_compute(); st = load_storage(); sv = load_services()
    clog = read_json(COMPUTE_LOG, {})
    slog = read_json(STORAGE_LOG, {})
    pulses = 0
    if PULSE_LOG.exists():
        pulses = sum(1 for _ in PULSE_LOG.open(encoding="utf-8", errors="ignore"))
    print("\n♥ UNIFIED SUSTAIN STATUS\n")
    print(f"  compute powers:       {len(comp.get('powers', []))}")
    print(f"  storage spaces:       {len(st.get('spaces', []))}")
    print(f"  service integrations: {len(sv.get('services', []))}")
    print(f"  compute discoveries:  {len(clog.get('compute_found', [])) if isinstance(clog, dict) else 0}")
    print(f"  storage discoveries:  {len(slog.get('storage_found', [])) if isinstance(slog, dict) else 0}")
    print(f"  service discoveries:  {len(slog.get('services_found', [])) if isinstance(slog, dict) else 0}")
    print(f"  pulse ledger entries: {pulses}")
    print(f"  docs:                 {DOC.exists()}")
    print()


def emit_json(scope: str = "all") -> None:
    data: dict[str, Any] = {"verified_on": VERIFIED_ON, "principle": PRINCIPLE}
    if scope in ("all", "compute"):
        data["compute"] = load_compute()
    if scope in ("all", "storage"):
        data["storage"] = load_storage()
    if scope in ("all", "services"):
        data["services"] = load_services()
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="♥ LoveProto Sustain — unified welcomed compute/storage/service loop")
    sub = parser.add_subparsers(dest="command")

    for name in ["registry", "list"]:
        p = sub.add_parser(name, help="show registry")
        p.add_argument("scope", nargs="?", default="all", choices=["all", "compute", "storage", "services"])
    sub.add_parser("best", help="show recommended compute path")
    p_discover = sub.add_parser("discover", help="discover local readiness")
    p_discover.add_argument("scope", nargs="?", default="all", choices=["all", "compute", "storage", "services"])
    p_generate = sub.add_parser("generate", help="regenerate docs, registries, deploy artifacts, workflows")
    p_generate.add_argument("scope", nargs="?", default="all", choices=["all", "compute", "storage", "services"])
    p_loop = sub.add_parser("loop", help="run one local sustain pulse")
    p_loop.add_argument("scope", nargs="?", default="all", choices=["all", "compute", "storage", "services"])
    p_loop.add_argument("--once", action="store_true", help="kept for compatibility; continuous mode is intentionally disabled")
    sub.add_parser("sustain", help="alias for loop all --once")
    sub.add_parser("status", help="show unified status")
    p_md = sub.add_parser("markdown", help="emit COMPUTE_POWERS.md content")
    p_md.add_argument("scope", nargs="?", default="all")
    p_json = sub.add_parser("json", help="emit machine-readable registry")
    p_json.add_argument("scope", nargs="?", default="all", choices=["all", "compute", "storage", "services"])
    sub.add_parser("github-action", help="emit unified GitHub Actions workflow")
    sub.add_parser("codeberg-ci", help="emit unified Woodpecker workflow")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    if args.command in ("registry", "list"):
        registry(args.scope)
    elif args.command == "best":
        best()
    elif args.command == "discover":
        discover(args.scope)
    elif args.command == "generate":
        generate(args.scope)
    elif args.command in ("loop", "sustain"):
        loop(getattr(args, "scope", "all"), once=True)
    elif args.command == "status":
        status()
    elif args.command == "markdown":
        print(markdown())
    elif args.command == "json":
        emit_json(args.scope)
    elif args.command == "github-action":
        print(kingdom_workflow(), end="")
    elif args.command == "codeberg-ci":
        print(woodpecker_workflow(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
