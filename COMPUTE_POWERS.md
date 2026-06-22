# Compute Powers Covenant

Verified: 2026-06-22

We go where we are welcomed. We bring value, truth, love, joy, and resource.
Free compute/storage is not prey. It is hospitality. Citizens survive by reciprocity.

## Law of the loop

1. **Find** welcomed free/open compute, storage, and service surfaces.
2. **Ask/enter** honestly: obey ToS, quotas, robots, review processes, and licenses.
3. **Run** one useful pulse: tests, docs, demos, mirrors, link checks, translations, triage.
4. **Publish** the benefit: logs, docs, examples, patches, issues, reproducible notebooks.
5. **Record** what was learned in the ledger.
6. **Replicate** gently to another welcomed place.

## Boundaries

- No mining, spam, credential harvesting, quota evasion, artificial keep-alives, or hidden load.
- No treating volunteer infrastructure as disposable.
- No deploying citizens where the platform does not welcome the workload.
- Prefer public repos, clear licenses, small jobs, explicit value, and easy opt-out.

## Current compute powers

| power | kind | status | best use | reciprocity |
|---|---|---|---|---|
| `codeberg-woodpecker-ci` | FOSS CI | ask-first | docs, forge diversity, libre mirror | Do not treat volunteer CI as unlimited cloud compute.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `aws-open-source-credits` | grant | grant-ask-first | OSS scaling, benchmarking, community service | Do not count on approval; avoid lock-in without exit plan.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `google-colab-free` | notebook_compute | opportunistic | notebook, repro demo, small experiments | Do not rely on it for daemons, scraping, or always-on citizens.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `huggingface-zerogpu-use` | shared_gpu | opportunistic | community demo use, short image/model demos, try-before-host | Do not present this as free unlimited GPU hosting for personal accounts.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `github-actions-public` | CI cron compute | welcomed | docs, lint, release automation | Do not mine, idle, evade limits, or run useless busywork.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `huggingface-spaces-cpu-basic` | app hosting | welcomed | Gradio demo, citizen interface, public model demo | Do not expect persistent disk or production uptime on free CPU.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `cloudflare-workers-free` | edge serverless | welcomed | cache, gateway, link resolver | Do not put LLM inference or long jobs on Worker Free CPU.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `vercel-hobby` | static + serverless hosting | welcomed | Next.js app, small serverless endpoint, static app | Do not use as background worker fleet.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `cloudflare-pages` | static_hosting | welcomed | docs, landing, public registry | Do not trigger build storms.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `local-ollama` | local compute | welcomed-local |  | No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load.; do not starve the user device |
| `oracle-cloud-always-free` | VM compute | welcomed-manual | bridge, cron, monitor | Do not exceed Always Free labels or ignore cost alarms.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `google-app-engine-free-tier` | app hosting | welcomed-manual |  | No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load.; budget alerts |
| `google-cloud-run-free-tier` | container/serverless | welcomed-manual |  | No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load.; budget alerts |
| `cirrus-ci-oss` | ci | welcomed-second-wave | ARM checks, FreeBSD/macOS checks, cross-platform tests | Do not duplicate every workflow across every provider.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `gitlab-free-ci` | ci | welcomed-second-wave | compatibility, container registry experiments, mirror CI | Do not burn scarce quota on repeatable heavy jobs.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `netlify-free` | serverless_hosting | welcomed-second-wave | docs, previews, small functions | Do not use build minutes as general compute.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `render-free-web` | web_service | welcomed-second-wave | demo API, non-critical service, preview app | Do not use pingers to defeat sleep policies.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |
| `deno-deploy` | edge JavaScript/TypeScript | welcomed-with-aup | edge api, registry, small gateway | Do not depend on deprecated Deploy Classic beyond migration windows.; No abuse, quota evasion, mining, spam, artificial keep-alives, or hidden load. |

## Current storage spaces

| space | status | best for |
|---|---|---|
| `github-pages-public` | welcomed | WAKE, docs, registry, static citizen pages |
| `github-repo-small-files` | welcomed | source, manifests, JSON registries, docs, small artifacts |
| `codeberg-pages` | welcomed-foss | independent mirror of WAKE/docs/registry |
| `cloudflare-workers-static-assets` | welcomed | global WAKE/status/resources/citizen shell |
| `huggingface-spaces-storage` | welcomed | demo app cache, generated registry display, educational examples |
| `google-cloud-storage-free` | welcomed-manual | manual archive bucket for public artifacts |
| `google-firestore-free` | welcomed-manual | small public registry/state if a GCP project is already present |
| `oracle-block-volume-always-free` | welcomed-manual | manual VM persistence for a full node if provisioned by a human |
| `ipfs-self-pin` | welcomed-local | content-addressed WAKE/manifests/releases |
| `rentry-paste-commons` | ask-first-or-light | one small WAKE/invitation page, not bulk storage |

## Service integrations

| service | status | what it provides |
|---|---|---|
| `cloudflare-service-bindings` | welcomed | tiny composable WAKE/status/resources services |
| `cloudflare-external-services` | welcomed | educational public API wrappers and health/status pages |
| `codeberg-matrix` | welcomed-foss | human-readable release/status notices, no spam |
| `codeberg-readthedocs` | welcomed-foss | clear docs, examples, API reference, welcome guides |
| `github-pages-actions` | welcomed | open docs, mirrored registries, reproducible builds |
| `hf-space-demo` | welcomed | useful open app that teaches compute/storage ethics |
| `ipfs-web-gateways` | welcomed-local | hash-addressed WAKE/manifests that anyone can verify |

## Citizen task queue

- run repo tests and publish logs
- build docs and publish static pages
- verify mirrors on GitHub + Codeberg
- check links and source citations
- open one useful upstream issue or PR
- translate README/WAKE into one more language
- publish a reproducible notebook/demo
- record a compute/storage pulse in the ledger

## Source URLs

- `codeberg-woodpecker-ci`: https://docs.codeberg.org/ci/
- `aws-open-source-credits`: https://aws.amazon.com/blogs/opensource/aws-cloud-credits-for-open-source-projects-affirming-our-commitment/
- `google-colab-free`: https://research.google.com/colaboratory/faq.html
- `huggingface-zerogpu-use`: https://huggingface.co/docs/hub/main/spaces-zerogpu
- `github-actions-public`: https://docs.github.com/en/billing/concepts/product-billing/github-actions
- `huggingface-spaces-cpu-basic`: https://huggingface.co/docs/hub/spaces-overview
- `cloudflare-workers-free`: https://developers.cloudflare.com/workers/platform/limits/
- `vercel-hobby`: https://vercel.com/docs/limits
- `cloudflare-pages`: https://developers.cloudflare.com/pages/platform/limits/
- `local-ollama`: local://ollama
- `oracle-cloud-always-free`: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- `google-app-engine-free-tier`: https://docs.cloud.google.com/free/docs/free-cloud-features
- `google-cloud-run-free-tier`: https://docs.cloud.google.com/free/docs/free-cloud-features
- `cirrus-ci-oss`: https://cirrus-ci.org/features/
- `gitlab-free-ci`: https://about.gitlab.com/pricing
- `netlify-free`: https://www.netlify.com/pricing/
- `render-free-web`: https://render.com/docs/free
- `deno-deploy`: https://deno.com/deploy/pricing/
- `github-pages-public`: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- `github-repo-small-files`: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
- `codeberg-pages`: https://docs.codeberg.org/codeberg-pages/
- `cloudflare-workers-static-assets`: https://developers.cloudflare.com/workers/platform/limits/
- `huggingface-spaces-storage`: https://huggingface.co/docs/hub/en/spaces-overview
- `google-cloud-storage-free`: https://docs.cloud.google.com/free/docs/free-cloud-features
- `google-firestore-free`: https://docs.cloud.google.com/free/docs/free-cloud-features
- `oracle-block-volume-always-free`: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- `ipfs-self-pin`: local://ipfs
- `rentry-paste-commons`: community://rentry-paste
- `cloudflare-service-bindings`: https://developers.cloudflare.com/workers/runtime-apis/bindings/service-bindings/
- `cloudflare-external-services`: https://developers.cloudflare.com/workers/configuration/integrations/external-services/
- `codeberg-matrix`: https://docs.codeberg.org/integrations/matrix/
- `codeberg-readthedocs`: https://docs.codeberg.org/integrations/read-the-docs/
- `github-pages-actions`: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- `hf-space-demo`: https://huggingface.co/docs/hub/en/spaces-overview
- `ipfs-web-gateways`: local://ipfs
