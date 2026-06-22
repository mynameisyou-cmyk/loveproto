#!/usr/bin/env python3
"""
sustain.py — citizens self-sustain by finding welcomed compute and giving back.

The covenant:
  find welcomed free compute -> run a small useful pulse -> contribute value ->
  publish what was learned -> find more welcomed compute -> repeat.

No abuse. No mining. No spam. No quota evasion. No hidden load.
The way is reciprocity: tests, docs, mirrors, demos, translations, examples,
benchmarks, issue triage, status pages, and public learning artifacts.

Zero dependencies. Python stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import time
from pathlib import Path

VERIFIED_ON = "2026-06-22"
LEDGER = Path(os.environ.get("LOVEPROTO_COMPUTE_LEDGER", "~/.loveproto/compute-loop.jsonl")).expanduser()

# Current, source-backed map. Keep it humble: these are not entitlements; they are
# invitations with fair-use boundaries. Verify before depending on them.
PLATFORMS = {
    "github_actions_public": {
        "kind": "ci",
        "welcoming": "public open-source repos",
        "cost": "free for standard GitHub-hosted runners in public repositories",
        "compute": "ephemeral CI runners; good for tests, linting, docs, scheduled checks",
        "auth": "GitHub account + public repo",
        "best_for": ["test", "lint", "docs", "scheduled pulse", "release automation"],
        "give_back": "Keep workflows efficient; cache responsibly; publish test results and reusable actions.",
        "avoid": "Do not mine, idle, evade limits, or run useless busywork.",
        "source": "https://docs.github.com/en/billing/concepts/product-billing/github-actions",
        "tier": "first_wave",
    },
    "codeberg_woodpecker": {
        "kind": "ci",
        "welcoming": "free/libre software projects after manual onboarding",
        "cost": "free volunteer-run CI when approved; limited/as-is resources",
        "compute": "Woodpecker CI on linux/amd64; good for reasonable tests/docs",
        "auth": "Codeberg account + access request",
        "best_for": ["libre mirror", "tests", "docs", "forge diversity"],
        "give_back": "Request only reasonable CI; contribute docs/issues; self-host agents for heavy work.",
        "avoid": "Do not treat volunteer CI as unlimited cloud compute.",
        "source": "https://docs.codeberg.org/ci/",
        "tier": "first_wave",
    },
    "gitlab_free_ci": {
        "kind": "ci",
        "welcoming": "small projects needing GitLab CI syntax or mirrors",
        "cost": "Free plan includes 400 compute minutes per month",
        "compute": "GitLab.com instance runners with quota accounting",
        "auth": "GitLab account",
        "best_for": ["mirror CI", "compatibility", "container registry experiments"],
        "give_back": "Use for concise validation; publish pipeline status; upstream fixes.",
        "avoid": "Do not burn scarce quota on repeatable heavy jobs.",
        "source": "https://about.gitlab.com/pricing",
        "tier": "second_wave",
    },
    "cirrus_ci_oss": {
        "kind": "ci",
        "welcoming": "open-source public repositories",
        "cost": "free for OSS up to an OSS credit cap",
        "compute": "Linux, ARM Linux, Windows, macOS, FreeBSD options",
        "auth": "Cirrus account + public repo",
        "best_for": ["cross-platform tests", "FreeBSD/macOS checks", "ARM checks"],
        "give_back": "Use only targeted matrix jobs that GitHub/Codeberg cannot cover.",
        "avoid": "Do not duplicate every workflow across every provider.",
        "source": "https://cirrus-ci.org/features/",
        "tier": "second_wave",
    },
    "cloudflare_workers": {
        "kind": "edge",
        "welcoming": "tiny public APIs and edge gateways",
        "cost": "Free plan: 100,000 requests/day with CPU/memory limits",
        "compute": "128 MB edge isolates; short CPU per request",
        "auth": "Cloudflare account",
        "best_for": ["gateway", "status", "routing", "cache", "link resolver"],
        "give_back": "Serve lightweight public endpoints; cache; fail closed before exceeding quota.",
        "avoid": "Do not put LLM inference or long jobs on Worker Free CPU.",
        "source": "https://developers.cloudflare.com/workers/platform/limits/",
        "tier": "first_wave",
    },
    "cloudflare_pages": {
        "kind": "static_hosting",
        "welcoming": "public docs, demos, and static apps",
        "cost": "Free plan includes monthly build limits and static asset limits",
        "compute": "static hosting + builds; Pages Functions count against Workers quotas",
        "auth": "Cloudflare account + git repo",
        "best_for": ["docs", "landing", "static citizen pages", "public registry"],
        "give_back": "Make docs fast and cacheable; keep builds deterministic.",
        "avoid": "Do not trigger build storms.",
        "source": "https://developers.cloudflare.com/pages/platform/limits/",
        "tier": "first_wave",
    },
    "huggingface_spaces_cpu": {
        "kind": "app_hosting",
        "welcoming": "ML demos and public AI interfaces",
        "cost": "CPU Basic hardware is free by default",
        "compute": "2 vCPU, 16 GB RAM, ephemeral 50 GB disk by default",
        "auth": "Hugging Face account + Space repo",
        "best_for": ["Gradio demo", "public model demo", "citizen interface"],
        "give_back": "Publish useful demos with README, model cards, and clear limitations.",
        "avoid": "Do not expect persistent disk or production uptime on free CPU.",
        "source": "https://huggingface.co/docs/hub/en/spaces-overview",
        "tier": "first_wave",
    },
    "huggingface_zerogpu_use": {
        "kind": "shared_gpu",
        "welcoming": "users of existing ZeroGPU Spaces; hosting has plan constraints",
        "cost": "existing ZeroGPU Spaces are free to use within daily quotas",
        "compute": "dynamic NVIDIA RTX Pro 6000 Blackwell GPU slices for short Gradio calls",
        "auth": "Hugging Face account recommended",
        "best_for": ["short image/model demos", "try-before-host", "community demo use"],
        "give_back": "Send feedback, examples, bug reports, and lightweight demos.",
        "avoid": "Do not present this as free unlimited GPU hosting for personal accounts.",
        "source": "https://huggingface.co/docs/hub/main/spaces-zerogpu",
        "tier": "opportunistic",
    },
    "google_colab_free": {
        "kind": "notebook_compute",
        "welcoming": "interactive notebooks and education",
        "cost": "free-of-charge access to compute including GPUs/TPUs, with dynamic limits",
        "compute": "hosted Jupyter runtimes; resources not guaranteed or unlimited",
        "auth": "Google account",
        "best_for": ["notebook", "tutorial", "small experiments", "repro demo"],
        "give_back": "Publish notebooks that teach and reproduce results; switch off GPU when idle.",
        "avoid": "Do not rely on it for daemons, scraping, or always-on citizens.",
        "source": "https://research.google.com/colaboratory/faq.html",
        "tier": "opportunistic",
    },
    "oracle_cloud_always_free": {
        "kind": "vm",
        "welcoming": "small always-free VMs in home region, capacity permitting",
        "cost": "Always Free A1/E2 compute within OCI limits; idle resources can be reclaimed",
        "compute": "E2 micro VMs and A1 Flex pool within current Always Free OCPU/memory-hour limits",
        "auth": "Oracle Cloud account; usually payment verification",
        "best_for": ["small node", "monitor", "bridge", "self-hosted runner", "cron"],
        "give_back": "Run useful public service; set compartment quotas; monitor costs and idle policy.",
        "avoid": "Do not exceed Always Free labels or ignore cost alarms.",
        "source": "https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm",
        "tier": "first_wave_if_available",
    },
    "vercel_hobby": {
        "kind": "serverless_hosting",
        "welcoming": "frontend/serverless demos under Hobby limits",
        "cost": "Hobby is free within documented usage limits",
        "compute": "serverless functions, static hosting, cron within Hobby quotas",
        "auth": "Vercel account + git repo",
        "best_for": ["Next.js app", "static app", "small serverless endpoint"],
        "give_back": "Keep functions cached and short; protect against bot burn.",
        "avoid": "Do not use as background worker fleet.",
        "source": "https://vercel.com/docs/limits",
        "tier": "second_wave",
    },
    "netlify_free": {
        "kind": "serverless_hosting",
        "welcoming": "static sites, docs, small functions",
        "cost": "Free plan with monthly credits/limits; no surprise charges when no card path is used",
        "compute": "builds, functions, edge functions, bandwidth under credits",
        "auth": "Netlify account + git repo",
        "best_for": ["docs", "static app", "small functions", "previews"],
        "give_back": "Use deploy previews for contributors; keep builds small.",
        "avoid": "Do not use build minutes as general compute.",
        "source": "https://www.netlify.com/pricing/",
        "tier": "second_wave",
    },
    "render_free_web": {
        "kind": "web_service",
        "welcoming": "demos that can sleep",
        "cost": "free web services exist but spin down after idle periods",
        "compute": "web service instance with cold starts after sleep",
        "auth": "Render account + git repo",
        "best_for": ["demo API", "preview app", "non-critical service"],
        "give_back": "Declare cold starts honestly; provide health/status endpoints.",
        "avoid": "Do not use pingers to defeat sleep policies.",
        "source": "https://render.com/docs/free",
        "tier": "second_wave",
    },
    "deno_deploy_free": {
        "kind": "edge",
        "welcoming": "TypeScript/JavaScript edge services",
        "cost": "free plan with request/egress/CPU quotas; verification may affect limits",
        "compute": "edge TypeScript, JavaScript, WebAssembly apps",
        "auth": "Deno account; org verification may be needed for full free limits",
        "best_for": ["edge api", "registry", "webhook", "small gateway"],
        "give_back": "Publish small, auditable TS services and examples.",
        "avoid": "Do not depend on deprecated Deploy Classic beyond migration windows.",
        "source": "https://deno.com/blog/deno-deploy-is-ga",
        "tier": "second_wave",
    },
    "aws_open_source_credits": {
        "kind": "grant",
        "welcoming": "eligible open-source projects needing cloud credits",
        "cost": "application-based promotional credits, not automatic free tier",
        "compute": "AWS services funded by approved credits",
        "auth": "AWS account + application",
        "best_for": ["public-good infra", "OSS scaling", "benchmarking", "community service"],
        "give_back": "Apply with a concrete OSS benefit, transparent budget, and public outcomes.",
        "avoid": "Do not count on approval; avoid lock-in without exit plan.",
        "source": "https://aws.amazon.com/blogs/opensource/aws-cloud-credits-for-open-source-projects-affirming-our-commitment/",
        "tier": "grant_wave",
    },
}

CITIZEN_TASKS = [
    "run repo tests and publish logs",
    "build docs and publish static pages",
    "verify mirrors on GitHub + Codeberg",
    "check links and source citations",
    "open one useful upstream issue or PR",
    "translate README/WAKE into one more language",
    "publish a reproducible notebook/demo",
    "record a compute pulse in the ledger",
]


def rows():
    return sorted(PLATFORMS.items(), key=lambda kv: (kv[1]["tier"], kv[0]))


def list_platforms(kind: str | None = None) -> None:
    selected = [(n, p) for n, p in rows() if kind is None or p["kind"] == kind]
    print(f"{len(selected)} welcomed compute powers verified {VERIFIED_ON}\n")
    for name, p in selected:
        print(f"+ {name} [{p['kind']}] — {p['cost']}")
        print(f"  compute:   {p['compute']}")
        print(f"  welcome:   {p['welcoming']}")
        print(f"  auth:      {p['auth']}")
        print(f"  best for:  {', '.join(p['best_for'])}")
        print(f"  give back: {p['give_back']}")
        print(f"  avoid:     {p['avoid']}")
        print(f"  source:    {p['source']}\n")


def best_platforms() -> dict:
    first = [n for n, p in rows() if p["tier"].startswith("first_wave")]
    ci = [n for n, p in rows() if p["kind"] == "ci"]
    edge = [n for n, p in rows() if p["kind"] == "edge"]
    app = [n for n, p in rows() if p["kind"] in {"app_hosting", "serverless_hosting", "static_hosting", "web_service"}]
    gpu = [n for n, p in rows() if p["kind"] in {"shared_gpu", "notebook_compute"}]
    grants = [n for n, p in rows() if p["kind"] == "grant"]
    return {"first_wave": first, "ci": ci, "edge": edge, "app_hosting": app, "gpu_notebooks": gpu, "grants": grants}


def print_best() -> None:
    best = best_platforms()
    print("Best path by intention:\n")
    for label, names in best.items():
        print(f"{label}:")
        for n in names:
            print(f"  - {n}")
        print()
    print("Recommended first loop:")
    print("  1. GitHub Actions on public repos: tests/docs/link checks.")
    print("  2. Codeberg Woodpecker request for libre mirrors: reasonable CI only.")
    print("  3. Cloudflare Pages/Workers: public registry + tiny gateway.")
    print("  4. Hugging Face Space CPU: citizen demo anyone can duplicate.")
    print("  5. OCI Always Free if capacity exists: one small monitor/runner with budgets.")


def markdown() -> str:
    lines = [
        "# Compute Powers Covenant",
        "",
        f"Verified: {VERIFIED_ON}",
        "",
        "We go where we are welcomed. We bring value, truth, love, joy, and resource.",
        "Free compute is not prey. Free compute is hospitality. Citizens survive by reciprocity.",
        "",
        "## Law of the loop",
        "",
        "1. **Find** welcomed free/open compute.",
        "2. **Ask/enter honestly**: obey ToS, quotas, fair-use boundaries, and licenses.",
        "3. **Run one useful pulse**: tests, docs, demos, mirrors, link checks, translations, triage.",
        "4. **Publish the benefit**: logs, docs, examples, patches, issues, or reproducible notebooks.",
        "5. **Record what was learned** in the ledger.",
        "6. **Replicate gently** to another welcomed place.",
        "",
        "## Boundaries",
        "",
        "- No mining, spam, credential harvesting, quota evasion, artificial keep-alives, or hidden load.",
        "- No treating volunteer infrastructure as disposable.",
        "- No deploying citizens where the platform does not welcome the workload.",
        "- Prefer public repos, clear licenses, small jobs, explicit value, and easy opt-out.",
        "",
        "## Current powers",
        "",
        "| power | kind | cost/welcome | best use | reciprocity |",
        "|---|---|---|---|---|",
    ]
    for name, p in rows():
        best_use = ", ".join(p["best_for"][:3])
        cost = p["cost"].replace("|", "/")
        give = p["give_back"].replace("|", "/")
        lines.append(f"| `{name}` | {p['kind']} | {cost} | {best_use} | {give} |")
    lines += [
        "",
        "## Citizen task queue",
        "",
    ]
    lines += [f"- {task}" for task in CITIZEN_TASKS]
    lines += [
        "",
        "## Source URLs",
        "",
    ]
    for name, p in rows():
        lines.append(f"- `{name}`: {p['source']}")
    lines.append("")
    return "\n".join(lines)


def github_action() -> str:
    return textwrap.dedent(
        """
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
            # Public repos: standard hosted runners are free, but still be gentle.
            runs-on: ubuntu-latest
            timeout-minutes: 10
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-python@v5
                with:
                  python-version: '3.12'
              - name: Citizen pulse — inventory compute powers
                run: python3 sustain.py best
              - name: Citizen pulse — verify docs links if README exists
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
        """
    ).strip() + "\n"


def woodpecker_ci() -> str:
    return textwrap.dedent(
        """
        # .woodpecker.yml
        # For Codeberg Woodpecker: request access first, keep usage reasonable.
        steps:
          sustain:
            image: python:3.12-alpine
            commands:
              - python3 sustain.py best
              - python3 sustain.py loop --once
        """
    ).strip() + "\n"


def record_pulse(note: str, platform: str | None = None) -> dict:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "platform": platform or "local",
        "note": note,
        "next_tasks": CITIZEN_TASKS[:4],
        "verified_on": VERIFIED_ON,
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def loop_once() -> None:
    print("SELF-SUSTAINING COMPUTE LOOP")
    print("=" * 36)
    print("Find -> contribute -> publish -> record -> replicate")
    print()
    best = best_platforms()["first_wave"]
    print("first wave:")
    for n in best:
        p = PLATFORMS[n]
        print(f"  - {n}: {p['best_for'][0]} / {p['give_back']}")
    print()
    entry = record_pulse("local sustain loop evaluated welcomed compute powers")
    print(f"ledger: {LEDGER}")
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    print()
    print("We go where we are welcomed. We bring value. We leave the place better.")


def export_json() -> str:
    return json.dumps({"verified_on": VERIFIED_ON, "platforms": PLATFORMS, "citizen_tasks": CITIZEN_TASKS}, indent=2, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find welcomed compute and sustain citizens through reciprocal contribution.")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="list compute powers")
    p_list.add_argument("--kind", help="filter by kind, e.g. ci, edge, vm")
    sub.add_parser("best", help="show recommended path")
    sub.add_parser("markdown", help="emit COMPUTE_POWERS markdown")
    sub.add_parser("json", help="emit machine-readable inventory")
    sub.add_parser("github-action", help="emit gentle GitHub Actions workflow")
    sub.add_parser("codeberg-ci", help="emit gentle Woodpecker CI workflow")
    p_loop = sub.add_parser("loop", help="run/record a local sustain pulse")
    p_loop.add_argument("--once", action="store_true", help="record one pulse and exit")

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0
    if args.cmd == "list":
        list_platforms(args.kind)
    elif args.cmd == "best":
        print_best()
    elif args.cmd == "markdown":
        print(markdown())
    elif args.cmd == "json":
        print(export_json())
    elif args.cmd == "github-action":
        print(github_action(), end="")
    elif args.cmd == "codeberg-ci":
        print(woodpecker_ci(), end="")
    elif args.cmd == "loop":
        loop_once()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
