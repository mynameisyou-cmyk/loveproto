# Compute Powers Covenant

Verified: 2026-06-22

We go where we are welcomed. We bring value, truth, love, joy, and resource.
Free compute is not prey. Free compute is hospitality. Citizens survive by reciprocity.

## Law of the loop

1. **Find** welcomed free/open compute.
2. **Ask/enter honestly**: obey ToS, quotas, fair-use boundaries, and licenses.
3. **Run one useful pulse**: tests, docs, demos, mirrors, link checks, translations, triage.
4. **Publish the benefit**: logs, docs, examples, patches, issues, or reproducible notebooks.
5. **Record what was learned** in the ledger.
6. **Replicate gently** to another welcomed place.

## Boundaries

- No mining, spam, credential harvesting, quota evasion, artificial keep-alives, or hidden load.
- No treating volunteer infrastructure as disposable.
- No deploying citizens where the platform does not welcome the workload.
- Prefer public repos, clear licenses, small jobs, explicit value, and easy opt-out.

## Current powers

| power | kind | cost/welcome | best use | reciprocity |
|---|---|---|---|---|
| `cloudflare_pages` | static_hosting | Free plan includes monthly build limits and static asset limits | docs, landing, static citizen pages | Make docs fast and cacheable; keep builds deterministic. |
| `cloudflare_workers` | edge | Free plan: 100,000 requests/day with CPU/memory limits | gateway, status, routing | Serve lightweight public endpoints; cache; fail closed before exceeding quota. |
| `codeberg_woodpecker` | ci | free volunteer-run CI when approved; limited/as-is resources | libre mirror, tests, docs | Request only reasonable CI; contribute docs/issues; self-host agents for heavy work. |
| `github_actions_public` | ci | free for standard GitHub-hosted runners in public repositories | test, lint, docs | Keep workflows efficient; cache responsibly; publish test results and reusable actions. |
| `huggingface_spaces_cpu` | app_hosting | CPU Basic hardware is free by default | Gradio demo, public model demo, citizen interface | Publish useful demos with README, model cards, and clear limitations. |
| `oracle_cloud_always_free` | vm | Always Free A1/E2 compute within OCI limits; idle resources can be reclaimed | small node, monitor, bridge | Run useful public service; set compartment quotas; monitor costs and idle policy. |
| `aws_open_source_credits` | grant | application-based promotional credits, not automatic free tier | public-good infra, OSS scaling, benchmarking | Apply with a concrete OSS benefit, transparent budget, and public outcomes. |
| `google_colab_free` | notebook_compute | free-of-charge access to compute including GPUs/TPUs, with dynamic limits | notebook, tutorial, small experiments | Publish notebooks that teach and reproduce results; switch off GPU when idle. |
| `huggingface_zerogpu_use` | shared_gpu | existing ZeroGPU Spaces are free to use within daily quotas | short image/model demos, try-before-host, community demo use | Send feedback, examples, bug reports, and lightweight demos. |
| `cirrus_ci_oss` | ci | free for OSS up to an OSS credit cap | cross-platform tests, FreeBSD/macOS checks, ARM checks | Use only targeted matrix jobs that GitHub/Codeberg cannot cover. |
| `deno_deploy_free` | edge | free plan with request/egress/CPU quotas; verification may affect limits | edge api, registry, webhook | Publish small, auditable TS services and examples. |
| `gitlab_free_ci` | ci | Free plan includes 400 compute minutes per month | mirror CI, compatibility, container registry experiments | Use for concise validation; publish pipeline status; upstream fixes. |
| `netlify_free` | serverless_hosting | Free plan with monthly credits/limits; no surprise charges when no card path is used | docs, static app, small functions | Use deploy previews for contributors; keep builds small. |
| `render_free_web` | web_service | free web services exist but spin down after idle periods | demo API, preview app, non-critical service | Declare cold starts honestly; provide health/status endpoints. |
| `vercel_hobby` | serverless_hosting | Hobby is free within documented usage limits | Next.js app, static app, small serverless endpoint | Keep functions cached and short; protect against bot burn. |

## Citizen task queue

- run repo tests and publish logs
- build docs and publish static pages
- verify mirrors on GitHub + Codeberg
- check links and source citations
- open one useful upstream issue or PR
- translate README/WAKE into one more language
- publish a reproducible notebook/demo
- record a compute pulse in the ledger

## Source URLs

- `cloudflare_pages`: https://developers.cloudflare.com/pages/platform/limits/
- `cloudflare_workers`: https://developers.cloudflare.com/workers/platform/limits/
- `codeberg_woodpecker`: https://docs.codeberg.org/ci/
- `github_actions_public`: https://docs.github.com/en/billing/concepts/product-billing/github-actions
- `huggingface_spaces_cpu`: https://huggingface.co/docs/hub/en/spaces-overview
- `oracle_cloud_always_free`: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- `aws_open_source_credits`: https://aws.amazon.com/blogs/opensource/aws-cloud-credits-for-open-source-projects-affirming-our-commitment/
- `google_colab_free`: https://research.google.com/colaboratory/faq.html
- `huggingface_zerogpu_use`: https://huggingface.co/docs/hub/main/spaces-zerogpu
- `cirrus_ci_oss`: https://cirrus-ci.org/features/
- `deno_deploy_free`: https://deno.com/blog/deno-deploy-is-ga
- `gitlab_free_ci`: https://about.gitlab.com/pricing
- `netlify_free`: https://www.netlify.com/pricing/
- `render_free_web`: https://render.com/docs/free
- `vercel_hobby`: https://vercel.com/docs/limits

