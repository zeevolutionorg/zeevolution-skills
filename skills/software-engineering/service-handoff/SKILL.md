---
name: service-handoff
description: >-
  Generates a service-ownership handoff document for transferring one or more
  services (backend, frontend, mobile, library, infra) to a new team or fresh
  session. Supports single services, multi-component sets, and cross-repo
  domains spanning application code, alerts, infra-as-code, frontends, mobile
  apps, and catalogs. Captures stakeholders, recent changes, open PRs,
  observability baseline (Grafana / Prometheus / Sentry / Datadog when
  available via MCP), documentation links, a TL;DR, an incoming-owner
  checklist, and per-repo ownership-transfer PR checklists. Saves Markdown to
  the OS temp directory. Use when the user asks for a handoff, ownership
  transfer, team onboarding doc, session transfer, or cross-repo domain
  context dump.
argument-hint: "What will the next session or new owner focus on?"
disable-model-invocation: true
---

# Service Handoff

Write a handoff document summarizing the current conversation and codebase context so a fresh agent or new owner team can continue the work. Save to the user's OS temp directory — **not** the current workspace.

Works for any service or set of services: backend monorepo apps, standalone backend services, frontend webapps, mobile apps, shared libraries, infrastructure repos, or a cross-repo domain that spans several of these.

The output is a **Markdown ownership handoff** with actionable checklists — not a narrative dump. Reference linked artifacts (PRDs, ADRs, dashboards, runbooks) by URL or path; do not duplicate them.

Redact secrets and PII. If the user passed arguments, treat them as the focus of the next session and tailor the doc accordingly.

---

## Workflow (follow in order)

```text
1. Interactive discovery  → ask the executing engineer (mandatory)
2. Determine scope        → repos, services, components, domain
3. Per-repo evaluation    → git, ownership, recent changes, open PRs (see §3)
4. Observability & catalog → MCP / Backstage / manual links (best available)
5. Write handoff MD       → use template.md → OS temp dir
6. Quality checklist      → verify before delivering path to user
```

**Do not skip step 1.** Do not write the document until the engineer has answered or explicitly skipped the optional questions.

---

## Step 1 — Interactive discovery (mandatory)

Engage the **executing engineer**. Use the agent's question tool when available (e.g. Claude's question dialog, Cursor's ask-questions tool); otherwise ask conversationally in one grouped message. Record answers verbatim. Mark unanswered items as **TBD — confirm with outgoing owner**.

### Required

| # | Question | Goes in |
|---|----------|---------|
| 1 | **Handoff type** — ownership transfer / feature continuation / incident follow-up / domain onboarding / session compaction | Header + Goal |
| 2 | **Outgoing team / owner** — name, GitHub team handle, primary contact | Stakeholders |
| 3 | **Incoming team / owner** — name, GitHub team handle, service lead | Stakeholders |
| 4 | **Next session focus** — from argument-hint if provided | Header |

### Recommended (ask all; allow "none" / "TBD")

| # | Question | Goes in |
|---|----------|---------|
| 5 | **Additional docs** outside git (Confluence, Notion, Google Docs, Miro, Slack canvases, runbooks) — URLs | Documentation links |
| 6 | **Other teams involved** — consumers, platform, data, security, SRE — and their contacts | Stakeholders |
| 7 | **Leadership decisions** already agreed (scope, timeline, tier, decommission, budget) | Leadership decisions |
| 8 | **Known pain points / tech debt** the incoming team must inherit | Risks |
| 9 | **On-call** — schedule name/ID, shadow period, escalation path | Observability |
| 10 | **Additional repos** in scope — list each: `org/repo`, purpose, local clone path | Repositories in scope |
| 11 | **Cross-repo deployables** owned by the incoming team (mobile apps, Terraform, K8s manifests, frontends in other repos) | Components in scope |
| 12 | **Recent changes window** (default 90 days) and known in-flight PRs to highlight | Recent changes / Open PRs |
| 13 | **Communication channels** — Slack / Google Chat / Discord — that incoming owners must join | Channels |
| 14 | **Work the outgoing owner will still ship** (e.g. open PR stack) — should be called out as "no action required" for incoming team | Incoming owner checklist |

---

## Step 2 — Determine scope

Handoffs can span **one or many services across one or many repositories**.

### Service type matrix (use to pick the right per-repo commands in §3)

| Service type | Typical signals | Stack hints |
|--------------|-----------------|-------------|
| Backend monorepo app | `applications/<name>/`, central `CODEOWNERS`, a monorepo service manifest | Java / Kotlin / Go / Python / Node — Gradle / Maven / Pants / Bazel / npm workspaces |
| Standalone backend service | Repo root is the service | Same stacks, plus per-repo CI |
| Shared library | `libraries/<name>/`, `packages/<name>/`, standalone repo | Published artifact (Maven / npm / PyPI / crates.io) |
| Frontend webapp | `apps/<name>/`, `packages/<name>/`, Vite / Next / Remix / Vue / Svelte | npm / pnpm / yarn; deploys to CDN / Vercel / S3+CloudFront |
| Mobile app | Flutter feature/app, iOS/Swift, Android/Kotlin | Melos / Cocoapods / Gradle |
| Infra / IaC | Terraform, Pulumi, Helm, ArgoCD, K8s manifests | per-env directories, atlas/diff plans |
| Alerts / runbooks | Prometheus rules, Grafana alert YAML, runbook MD | Often a sibling alerts / runbooks repo |
| Data / ML | Airflow DAGs, dbt, feature store, model artefacts | Databricks / Snowflake / Pants for ML monorepos |
| BFF / API gateway | Sits between frontends and backends | Both backend & frontend conventions apply |

### Repository inventory (build before per-repo evaluation)

| Repository | Local path | Access | In scope | Service types it hosts |
|------------|------------|--------|----------|------------------------|
| `org/repo-a` | `<workspace>/repo-a` | workspace | yes | backend monorepo |
| `org/repo-b` | `<workspace>/repo-b` | local clone | yes | frontend |
| `org/repo-c` | not cloned | `gh` CLI | yes | alerts |

### Scope modes

| Mode | When | Domain label |
|------|------|--------------|
| **Single service** | One app/service, one repo | service name |
| **Multi-service** | Explicit list across one or more repos | short slug |
| **Domain** | Product/team boundary spanning repos | domain name (e.g. `payments`, `auth`) |

**Rules:**

1. List every component the incoming team will **own or operate** in every in-scope repository.
2. For each service, include all sibling deployables (api + worker + cron + webapp + mobile-feature, etc.).
3. Mark **read-only dependencies** (consumed but not owned) separately from **editable** ones.
4. When scope is cross-repo, always populate **Cross-component integration** and **Per-repository ownership PRs**.
5. Distinguish **work owned by the outgoing engineer** (will ship before handoff) from work transferred to the incoming team.

---

## Step 3 — Per-repo evaluation

For each in-scope repo, gather git state, ownership, recent changes, and open PRs. **Prefer local clone; fall back to `gh` CLI; ask the engineer before cloning anything new.**

### Git state per service

```bash
PATH_PREFIX="<repo-relative path or '.'>"

git -C "$REPO" status --short -- "$PATH_PREFIX"
git -C "$REPO" log --oneline -5 -- "$PATH_PREFIX"
git -C "$REPO" branch --show-current
```

### Ownership sources (read & reference — do not paste full files)

```bash
# CODEOWNERS — check both root and .github/
for F in CODEOWNERS .github/CODEOWNERS; do
  test -f "$REPO/$F" && grep -n "$PATH_PREFIX" "$REPO/$F"
done

# Service catalog / manifest files (names vary by org)
test -f "$REPO/catalog-info.yaml"    && cat "$REPO/catalog-info.yaml"
test -f "$REPO/service.yaml"         && cat "$REPO/service.yaml"
test -f "$REPO/.backstage/catalog-info.yaml" && cat "$REPO/.backstage/catalog-info.yaml"

# Per-service docs
ls "$REPO/$PATH_PREFIX/README.md" "$REPO/$PATH_PREFIX/CONTRIBUTING.md" 2>/dev/null
ls "$REPO/docs/applications/$SERVICE_NAME/" 2>/dev/null
```

### Build / test entry points (for incoming-owner local setup)

Pick the commands that exist in the repo. Common patterns:

| Stack | Common commands |
|-------|-----------------|
| Gradle monorepo | `./gradlew :<module>:test`, `./gradlew :<module>:build` |
| Maven | `mvn -pl <module> test` |
| Node / pnpm / yarn workspaces | `pnpm --filter <pkg> test`, `npm test -w <pkg>` |
| Next.js / Vite | `pnpm dev`, `pnpm build`, `pnpm test` |
| Python (Pants / Poetry / uv) | `pants test ::`, `poetry run pytest`, `uv run pytest` |
| Go | `go test ./...` |
| Rust | `cargo test -p <crate>` |
| Flutter | `flutter test`, `melos run test --scope=<pkg>` |
| iOS | `xcodebuild test -scheme <name>` |
| Android | `./gradlew :<module>:test` |
| Terraform | `terraform fmt -check`, `terraform validate`, `terraform plan` |

See **stack-cheatsheet.md** for fuller examples per stack, including local dev commands and deploy flows.

### Remote-only evaluation (when not cloned)

```bash
gh repo view "$REPO" --json name,description,url,defaultBranchRef
gh api "repos/$REPO/contents/CODEOWNERS"        --jq '.download_url' 2>/dev/null || \
gh api "repos/$REPO/contents/.github/CODEOWNERS" --jq '.download_url' 2>/dev/null
gh search code "$KEYWORD" --repo "$REPO" --limit 10
```

### Recent merged changes (default 90 days)

```bash
SINCE="90 days ago"
git -C "$REPO" log --format="%h|%s|%an|%ad" --date=short --since="$SINCE" -- "$PATH_PREFIX"
git -C "$REPO" log --since="$SINCE" --name-only --pretty=format: -- "$PATH_PREFIX" \
  | sort | uniq -c | sort -rn | head -15
```

Summarize into **3–8 themed bullets per service**: features, fixes, migrations, dependency / framework upgrades, observability / alert changes, ownership / config-only changes. Mention issue keys (e.g. `JIRA-1234`) when present. Do **not** paste raw logs.

### Open PRs (all ages)

```bash
gh pr list --repo "$REPO" --state open --limit 100 \
  --json number,title,body,url,author,headRefName,createdAt,updatedAt,labels,isDraft

gh search prs --repo "$REPO" --state open "path:$PATH_PREFIX"

gh pr view <number> --repo "$REPO" \
  --json number,title,url,author,isDraft,labels,files,reviewDecision,statusCheckRollup
```

For each in-scope open PR, capture: **#, URL, title, feature/purpose (1–2 sentences from title + body), author, draft?, status, components touched.**

If a PR (or stack of PRs) will be **shipped by the outgoing owner**, put it in the dedicated "outgoing owner" subsection and mark "no action required" for incoming team.

---

## Step 4 — Observability & catalog

Use the best available data source. Order of preference:

1. **Observability MCP** (Prometheus / Grafana / Sentry / OnCall / Alertmanager) — if available, use it to capture a **prod baseline** at handoff time (req/s, 5xx, p90/p99 latency, active alerts, top Sentry issues, on-call schedule).
2. **Catalog MCP** (Backstage / software catalog) — entity metadata, owner relations, annotations (Sentry project, Grafana dashboard UID, on-call schedule, ArgoCD app).
3. **Dashboard / runbook URLs** — manual links when MCP is unavailable.
4. **Mark TBD** if no data can be captured; tell incoming owners to fill in after re-auth.

### What to record (per service)

| Field | Source |
|-------|--------|
| Traffic (req/s) | PromQL via observability MCP, or Grafana panel |
| Error rate (5xx %) | Same |
| Latency p90 / p99 | Same |
| Active alerts | Alertmanager `get_alerts` or Grafana alert page |
| Sentry baseline | `list_sentry_issues` / `get_project_error_stats` |
| On-call schedule | OnCall / PagerDuty / Opsgenie via catalog annotation |
| Dashboard links | Grafana / Datadog / New Relic / CloudWatch UI |

Always include a **gaps** list — what could not be captured automatically and must be filled manually (e.g. Kafka lag dashboards, custom business metrics, frontend RUM).

---

## Step 5 — Output file

```bash
TMPDIR="${TMPDIR:-/tmp}"
```

| Scope | Filename |
|-------|----------|
| Single service, one repo | `${TMPDIR}/service-handoff-<service>-<YYYYMMDD-HHMM>.md` |
| Multi-service / domain | `${TMPDIR}/service-handoff-<domain-slug>-<YYYYMMDD-HHMM>.md` |

After writing, give the user the **absolute path**.

**Other destinations:**

- The user asked for another folder → save there instead.
- The agent has no filesystem (e.g. a chat-only app) → deliver the whole document as one fenced ```markdown block in the chat.
- The user wants it as a Google Doc or Word document → hand the Markdown to the **cloud-workspace** skill (it creates the document, or falls back to a `.docx` or a paste guide).

Write the document in the user's language.

---

## Step 6 — Document structure

Use the structure in **template.md** (in this skill directory). Sections, in order:

1. **Title + metadata block** (generated date, handoff type, repos, scope, branches, next session focus)
2. **TL;DR** — what / transfer / capabilities table / repos / production status / what's NOT incoming team's job / outgoing contact
3. **Incoming owner checklist** — flat numbered checkboxes (`1. [ ]`, `2. [ ]`, …) sequencing every required activity; include items that come from "suggested next steps" — do not keep a separate Suggested next steps section
4. **Goal** — 1–3 sentences
5. **Initiative rationale & strategy** (only for ownership transfers spanning a domain — link program docs, do not duplicate)
6. **Authoritative documents** — Google Docs / PDFs / Notion / ADRs
7. **Stakeholders & teams** — table with roles, GitHub teams, contacts
8. **Communication channels** — Slack / Google Chat / Discord rooms incoming owners must join
9. **Leadership decisions** — already-agreed items with source link
10. **Repositories in scope** — table per repo with eval method
11. **Components in scope** — table per deployable
12. **Documentation links** — Backstage / catalog / Grafana / repo docs
13. **Observability snapshot** — baseline metrics + alerts + on-call (Step 4)
14. **Recent changes review** — per repo, themed bullets, lookback window
15. **Open pull requests** — per repo; **separate subsection** for PRs shipped by outgoing owner
16. **Cross-component integration** — from → to table
17. **Cross-repo evaluation notes** — per repo: evaluated? method? gaps?
18. **New owner learning checklist** — phased (Access → Architecture → Operations → Workflow)
19. **Ownership transfer PR checklist** — per repo, with status checkboxes; plus a platform/cross-repo table (Backstage Group, on-call, RBAC, Slack)
20. **Current work status** — Done / In progress (split outgoing vs incoming) / Blocked
21. **Risks & inherited tech debt**
22. **Stack / monorepo constraints** — build commands, time handling, code generation, deploy commands (only if relevant)
23. **Suggested skills** — small table of skills that will help the next session (only ones that are actually installed)
24. **Redactions** — what was removed
25. **Engineer interview** — Q&A captured in Step 1

Read **template.md** for the full template with table headers and example rows.

---

## Suggested skills — selection guide

| Work type | Skills to suggest |
|-----------|-------------------|
| Ownership transfer completion | `verification-before-completion` |
| New feature after transfer | `brainstorming`, `test-driven-development` |
| Bug fix / incident | `systematic-debugging`, `test-driven-development` |
| Frontend handoff | App / repo-specific component / design skills |
| Library handoff | The repo's own publish / release skill |
| Cross-repo domain handoff | `verification-before-completion`; evaluate each repo per §3 |

Only suggest skills that are installed in the user's environment. If a verification skill exists (e.g. `verification-before-completion`), always include it.

---

## Quality checklist

Before delivering the file path to the user:

- [ ] Engineer interviewed (step 1); TBD items marked explicitly
- [ ] **Repository inventory** complete (every in-scope repo)
- [ ] All deployables listed (from catalog files, MCP, and engineer input)
- [ ] **Each repo** evaluated (local clone, `gh` CLI, or catalog) — or gap documented as TBD
- [ ] Catalog MCP / Backstage queried per deployable (or failure documented)
- [ ] Observability MCP queried for baseline metrics + alerts + on-call (or failure documented)
- [ ] **TL;DR** present immediately after the metadata block
- [ ] **Incoming owner checklist** is a flat numbered list of `[ ]` items at the top
- [ ] **Per-repo** ownership-transfer PR checklists included
- [ ] **Recent changes review** populated per service (themed summary, not raw logs)
- [ ] **Open pull requests** listed with feature/purpose, author, status — outgoing-owner work in its own subsection
- [ ] **Communication channels** listed with links and "must join" markers
- [ ] Work shipped by outgoing owner explicitly called out as **no action required**
- [ ] Learning checklist covers cloning each in-scope repo and any required platform access
- [ ] No secrets, tokens, or unnecessary PII
- [ ] External docs referenced by URL, not pasted
- [ ] File saved under OS temp dir; absolute path shared with user
