# Handoff Document Template

Use this template for the handoff Markdown file. Checkboxes must be `- [ ]` so the incoming team can track progress. Replace `<placeholder>` text.

---

```markdown
# Service Ownership Handoff: <domain or primary service>

**Generated:** <ISO-8601 UTC>
**Handoff type:** <ownership transfer | feature continuation | incident follow-up | domain onboarding | session compaction>
**Repositories in scope:** <comma-separated org/repo list>
**Primary repo:** `<org/repo>`
**Scope:** <single service | multi-service | domain | cross-repo domain>
**Branch (primary repo):** `<branch>`
**Next session focus:** <from user argument>

---

## TL;DR

**What:** <one-sentence description of the domain / service set>

**Transfer:** **<Outgoing team> → <Incoming team>** (link to decision doc).

**Capabilities you inherit:**

| Capability | Where it lives |
|------------|----------------|
| <capability A> | `<org/repo>` (`<path>`) |
| <capability B> | `<org/repo>` (`<path>`) |

**Repos to own:** `<repo-a>`, `<repo-b>`, `<repo-c>`.

**Already in production:** <bullet list of shipped features>

**Not yet shipped (incoming priority):** <work the new owners should prioritize>

**Not your job (during handoff):** <work that outgoing owner will finish — PRs / features>

**Read first:** <Doc 1> · <Doc 2> · **Outgoing contact:** [@<handle>](https://github.com/<handle>)

---

## Incoming owner checklist

Work top-to-bottom. Details for each item are in the sections below.

1. [ ] **Incoming team EM:** Confirm receiving team, GitHub team handle, on-call rotation, communication channels, protected capacity
2. [ ] **Joint sync (outgoing + incoming):** Walk authoritative docs + this handoff
3. [ ] **Clarify open decisions:** <list>
4. [ ] **Access:** Request membership for incoming GitHub teams across all **<N> repos**
5. [ ] **Local setup:** Clone all in-scope repos; run each service locally
6. [ ] **Observability access:** Confirm Grafana / Sentry / Datadog / etc.; join mandatory communication channels
7. [ ] **Architecture walk:** Map services and integrations with outgoing engineer
8. [ ] **On-call:** Shadow or join pager for in-scope services
9. [ ] **Operations baseline:** Walk dashboards, SLO docs, alert rules, runbooks
10. [ ] **Triage open PRs:** Assign incoming reviewers; <list any outgoing-owner PRs that are excluded>
11. [ ] **Ownership PRs:** Execute the per-repo ownership-transfer checklist below
12. [ ] **Platform metadata:** Update catalog Group, Sentry team, ArgoCD RBAC, alert channels
13. [ ] **Consumer comms:** Notify downstream / consumer teams of new owner
14. [ ] **Integration checkpoints:** Schedule syncs with key consumer teams
15. [ ] **SLO baseline:** Review observability snapshot; refresh after major deploys
16. [ ] **Handoff sign-off:** Incoming team on CODEOWNERS in all repos; outgoing off primary pager; EM confirms protected capacity

**Primary handoff contact (outgoing):** <Name> ([@<handle>](https://github.com/<handle>))

> **Outgoing-owner work (no action for incoming team):** <e.g. PRs #X–#Y will be merged, validated, and shipped by outgoing owner.>

---

## Goal

<1–3 sentences>

---

## Initiative rationale & strategy
<Only for domain / multi-service transfers. Summarize from authoritative docs; do not duplicate. Cover: why this exists, origin, why ownership is moving, program status (phase table), key open demands.>

---

## Authoritative documents

| Document | Link |
|----------|------|
| <Vision / decision doc> | <url> |
| <Program hub> | <url> |
| <PRD> | <url> |
| <Technical handover> | <url> |

---

## Stakeholders & teams

| Role | Team / person | GitHub | Notes |
|------|---------------|--------|-------|
| **Incoming owner** | | `@<org>/<team>` | |
| Outgoing owner | | `@<org>/<team>` | |
| Service lead (outgoing) | | `@<handle>` | Primary handoff contact |
| Platform / SRE | | | |
| Consumer teams | | | |

---

## Communication channels

Incoming service owners **must join** these channels.

| Channel | Purpose | Link |
|---------|---------|------|
| `<channel-name>` | <purpose> | <invite URL> |

---

## Leadership decisions

| Decision | Status | Source |
|----------|--------|--------|
| | | <doc link> |

---

## Repositories in scope

| Repository | Local path | Access | In scope | Service types |
|------------|------------|--------|----------|---------------|
| `<org/repo>` | `<path>` | workspace / clone / `gh` / not cloned | yes/no | <e.g. backend monorepo, frontend, alerts> |

---

## Components in scope

| Component | Repository | Catalog name(s) | Type | Path | Tier | Edit? |
|-----------|------------|-----------------|------|------|------|-------|
| | | | api / worker / sdk / webapp / infra | | T0/T1/T2/T3 | yes/no |

---

## Documentation links

### Catalog / Backstage

| Resource | URL |
|----------|-----|
| Component `<name>` | |
| API definition | |
| Deployments | |
| Incoming team (Group) | |
| System docs | |
| Alerts & incidents | |

### Per-repo

| Repository | Resource | Path or URL |
|------------|----------|-------------|
| `<org/repo>` | README | |
| `<org/repo>` | Architecture / specs | |
| `<org/repo>` | SLO / alert doc | |

### Dashboards (Grafana / Datadog / New Relic / CloudWatch)

| Dashboard | URL |
|-----------|-----|
| | |

---

## Observability snapshot

**Captured:** <YYYY-MM-DD> via <MCP / manual / dashboard URL>

### Production traffic & latency

| Service | Req/s | 5xx rate | p90 latency | p99 latency | Notes |
|---------|-------|----------|-------------|-------------|-------|
| | | | | | |

### Active alerts

<None / list>

### Sentry / error stats (last 7 days)

| Project | Errors (7d) | Top unresolved |
|---------|-------------|----------------|
| | | |

### Key metrics (baseline)

| Metric | Status | Value / note |
|--------|--------|--------------|
| | ✅ / ⚠️ / TBD | |

### On-call

| Schedule | Current on-call | Schedule ID / link |
|----------|-----------------|---------------------|
| | | |

### Gaps

<List metrics that could not be captured automatically.>

---

## Recent changes review

**Lookback:** <window, e.g. 90 days — merged to default branch>
**Overall:** <2–4 sentences on velocity and major themes>

### `<org/repo>` — `<path or service>`

| Period | Summary |
|--------|---------|
| Last <N> days | <3–8 themed bullets: features, fixes, migrations, deps, observability> |
| Notable in-flight | |
| Risk flags | |

<Repeat per in-scope service.>

---

## Open pull requests

### `<org/repo>`

#### <Service or area>

| PR | Title | Feature / purpose | Author | Draft | Status | Components |
|----|-------|-------------------|--------|-------|--------|------------|
| [#N](url) | | | | | | |

#### Outgoing-owner stack (no incoming action)

> Will be merged, validated, and shipped by [@<handle>](https://github.com/<handle>).

| PR | Title | Author | Status |
|----|-------|--------|--------|
| | | | |

**Merge order (outgoing owner):** <list>

---

## Cross-component integration

| From | Repository | To | Repository | Mechanism | Notes |
|------|------------|-----|------------|-----------|-------|
| | | | | REST / Kafka / gRPC / pre-signed URL / library | |

---

## Cross-repo evaluation notes

| Repository | Evaluated? | Method | Paths reviewed | Gaps / TBD |
|------------|------------|--------|----------------|------------|
| | yes / partial / no | local / `gh` / catalog | | |

---

## New owner learning checklist

### Phase 1 — Access & environment

- [ ] Join `@<org>/<incoming-team>` (request via your access provisioning system)
- [ ] Clone each in-scope repo
- [ ] Read READMEs and primary architecture / SLO docs
- [ ] Run each service locally (commands per stack — see stack-cheatsheet.md)
- [ ] Access catalog component pages
- [ ] Access Grafana / Sentry / etc.
- [ ] Join communication channels (above)

### Phase 2 — Architecture & codebase

- [ ] Map module structure per service
- [ ] Map upstream / downstream services (catalog relations)
- [ ] Identify integration libraries
- [ ] Read app-specific rules / skills if any

### Phase 3 — Operations

- [ ] Deployment flow (per repo / per stack)
- [ ] Walk dashboards — golden signals
- [ ] Read alert rules and runbooks
- [ ] Understand event / queue lag (if applicable)
- [ ] On-call shadow

### Phase 4 — Development workflow

- [ ] Repo contributing guide
- [ ] PR checks / validators
- [ ] Conventional commits / commit hygiene
- [ ] Make a trivial docs PR to validate pipeline access

---

## Ownership transfer PR checklist

### `<org/repo-a>`

| # | PR purpose | File(s) | Status |
|---|------------|---------|--------|
| A-1 | CODEOWNERS | `CODEOWNERS` or `.github/CODEOWNERS` | [ ] |
| A-2 | Catalog ownership | `catalog-info.yaml` / `service.yaml` / monorepo service manifest | [ ] |
| A-3 | Service owners doc | `docs/<service>/service-owners.md` | [ ] |
| A-4 | README ownership | `README.md` | [ ] |
| A-5 | CI validators | — | [ ] |

<Repeat per repo. For alerts repo, swap A-2/A-3 for "Alert notification channel" + "Runbook frontmatter owner".>

### Platform & process (cross-repo)

| # | Action | System | Status |
|---|--------|--------|--------|
| P-1 | Unify GitHub team handle | GitHub | [ ] |
| P-2 | Backstage Group / catalog Group ownership | Catalog | [ ] |
| P-3 | On-call schedule | Opsgenie / PagerDuty / Grafana OnCall | [ ] |
| P-4 | Sentry project team | Sentry | [ ] |
| P-5 | ArgoCD / deploy RBAC | ArgoCD | [ ] |
| P-6 | Communication channels — add incoming, remove outgoing | Slack / Chat | [ ] |
| P-7 | Notify downstream consumer teams | — | [ ] |

---

## Current work status

- **Done:** <inventory items completed>
- **In progress (outgoing owner — no incoming action):** <e.g. PR stack>
- **In progress (incoming team will own):** <list>
- **Blocked / open questions:** <list>

---

## Risks & inherited tech debt

- <bullet list from engineer + observability snapshot>

---

## Stack / monorepo constraints (only if relevant)

- <e.g. environment variables the build wrapper needs (or must not have)>
- <e.g. read-only framework directories>
- <e.g. `Clock` injection for time>
- <e.g. deploy / promotion commands like `make promote app=<name>`>
- <e.g. composite builds / generated code do-not-edit>

---

## Suggested skills

| Skill | When to use |
|-------|-------------|
| `verification-before-completion` | Before closing merge / deploy / handoff |
| <stack / repo / domain skill> | <context> |

---

## Redactions

<list of removed items, or "none">

---

## Engineer interview (this session)

| Question | Answer |
|----------|--------|
| Handoff type | |
| Outgoing / incoming | |
| Leadership decision | |
| Additional docs | |
| Lookback window | |
```
