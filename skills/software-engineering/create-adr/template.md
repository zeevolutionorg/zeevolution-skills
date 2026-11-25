# ADR Template — Nygard + MADR (Alternatives considered)

This is the canonical body the `create-adr` skill renders into the destination folder. Copy verbatim, then fill in every `<…>` placeholder. Remove any optional section that doesn't apply (e.g. `Validation`, `Superseded by`).

The structure follows:

- **Base:** [Nygard ADR — Markdown rendering](https://github.com/architecture-decision-record/architecture-decision-record/blob/main/architecture-decision-record.github.io/src/content/locales/en-us/templates/decision-record-template-by-michael-nygard.md)
- **`Alternatives considered`:** [MADR 4.0.0 — full template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md?plain=1)

---

# ADR-<NNN>: <Decision title in the imperative, ≤ 60 chars>

- **Status:** <Proposed | Accepted | Accepted — implemented and rolled out to production. | Superseded by [ADR-<NNN>](./<NNN>-…md)>
- **Date decided:** <YYYY-MM-DD>
- **Date in production (approx.):** <YYYY-MM-DDTHH:MM:SS±HH:MM> — <how this was determined, e.g. "merge timestamp of `<commit>` on `<branch>`; refine with ArgoCD if available">
- **Deciders:** <names / teams>
- **Consulted:** <reviewers / stakeholders / other teams>

> Drop the `Supersedes` / `Superseded by` lines entirely when empty — do not keep `: —` placeholders.

---

## Context

<2–4 short paragraphs. What is the forcing function? What constraints (regulatory, performance, cost, security, organisational) apply? What did the system look like before this decision? Reference dashboards / runbooks / tickets by URL where useful.>

### Prior state (only for `supersede` mode)

<What was previously decided and why it no longer holds. Link the old ADR.>

---

## Decision

<One paragraph: the decision in the active voice ("We will …"). Anyone reading only this section should be able to paraphrase the decision in one sentence.>

Follow the **anchor-classes pattern**: name the **1–2 classes** that anchor the design and stop. Typically:

- **`<WritePathDTO>.<field>`** on **writes** — <one-line behaviour change>, and
- the persisted **`<ReadPathEntity>.<column>`** on **reads / commits** — <one-line behaviour change>.

<One short paragraph on any non-obvious topology choice (e.g. "The dev environment collapses both regions onto the same bucket; resolution happens through config, not code branching.").>

> Concrete wiring — <list 3–5 mechanical items in one sentence, e.g. dependency-injection wiring, exception classes, observability tags, cloud permission scoping, local emulator parity> — read the code. The PRs in **Related artifacts** above link the exact diffs.

> **Anti-pattern (do not do this):** a numbered list of 8–10 bullets describing beans, configs, migrations, exceptions, and HTTP statuses. That is code restated as prose, and it makes the ADR longer than it needs to be without adding decision-level information. Trim ruthlessly.

---

## Alternatives considered

> From MADR 4.0.0 — include at least two rejected options, each with explicit Pros / Cons. Mark the chosen option clearly.

### Option A — <Short name> *(chosen)*

<One-line description.>

- **Pros:**
  - <…>
- **Cons:**
  - <…>

### Option B — <Short name>

<One-line description.>

- **Pros:**
  - <…>
- **Cons:**
  - <…>

### Option C — <Short name>

<One-line description.>

- **Pros:**
  - <…>
- **Cons:**
  - <…>

---

## Consequences

### Positive

- <…>

### Negative

- <…>

### Mitigations

- <How we lessen the negatives — feature flags, monitoring, runbooks, rollback plan.>

### Neutral

- <Tradeoffs that aren't clearly good or bad but are worth recording.>

---

## Validation

<How we know this decision is working. Link metrics dashboards, SLO dashboards, alert rules, or describe the success criteria and how they will be measured. Remove this section if not applicable.>

---

## Related artifacts

> Sort in **infrastructure-first** rollout order: deployments → infrastructure (IRSA / KMS / S3) → application code → docs. Link each PR with its full URL (`[#NNNN](https://…/pull/NNNN)`) so the table is meaningful when read outside the repo.

| Order | Repository | PR | Title | Merged |
|------:|------------|----|-------|--------|
| 1 | <org/repo> | <PR link> | <title> | <YYYY-MM-DD> |
| 2 | <org/repo> | <PR link> | <title> | <YYYY-MM-DD> |
| 3 | <org/repo> | <PR link> | <title> | <YYYY-MM-DD> |

Additional artifacts (optional):

- Runbook: <url>
- Dashboard: <url>
- Original design discussion: <url>

---

## References

- **ADR template used:** Nygard ([source](https://github.com/architecture-decision-record/architecture-decision-record/blob/main/architecture-decision-record.github.io/src/content/locales/en-us/templates/decision-record-template-by-michael-nygard.md)) extended with the `Alternatives considered` section from MADR 4.0.0 ([source](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md?plain=1)). See [adr.github.io/adr-templates](https://adr.github.io/adr-templates/) for the broader catalogue.
- <Any standards, RFCs, papers, blog posts that informed the decision.>

---

## Changelog / Metadata

- <YYYY-MM-DD> — Initial draft (compressed from `<spec.md>` + `<plan.md>`, both subsequently deleted) by <author>.
- <YYYY-MM-DD> — Accepted; implementation merged via the PRs listed under **Related artifacts**.
- <YYYY-MM-DD> — Rolled out to production.
