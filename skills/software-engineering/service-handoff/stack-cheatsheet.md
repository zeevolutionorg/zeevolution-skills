# Stack Cheat-Sheet — Per-Service Commands

Reference commands for the most common service stacks. Pick the ones that match the repo; document the actual commands used in the handoff's Learning checklist.

---

## Backend — JVM (Java / Kotlin)

### Gradle (monorepo)

```bash
./gradlew :<module>:test
./gradlew :<module>:build
./gradlew :<module>:bootRun     # Spring Boot
./gradlew :<module>:integrationTest
```

### Gradle (standalone repo)

```bash
./gradlew test build
```

### Maven

```bash
mvn -pl <module> test
mvn -pl <module> verify
mvn spring-boot:run
```

### Common JVM constraints to call out

- JDK version (from `.sdkmanrc`, `.tool-versions`, `.java-version`)
- `Clock` injection (no `Instant.now()` / `new Date()`)
- Generated code directories that must not be hand-edited
- Framework directories marked read-only

---

## Backend — Node.js / TypeScript

### npm workspaces

```bash
npm install
npm test -w <package>
npm run dev -w <package>
npm run build -w <package>
```

### pnpm

```bash
pnpm install
pnpm --filter <package> test
pnpm --filter <package> dev
pnpm --filter <package> build
```

### yarn workspaces

```bash
yarn install
yarn workspace <package> test
yarn workspace <package> dev
```

### Common Node constraints

- Node version (from `.nvmrc`, `package.json#engines`)
- Lockfile (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`) must stay in sync
- ESLint / Prettier config inheritance from monorepo root

---

## Backend — Python

### Poetry

```bash
poetry install
poetry run pytest
poetry run uvicorn app.main:app --reload
```

### uv

```bash
uv sync
uv run pytest
uv run python -m <module>
```

### Pants monorepo

```bash
pants test ::
pants test path/to/service::
pants package path/to/service::
pants run path/to/service:app
```

### Common Python constraints

- Python version (from `.python-version`, `pyproject.toml#requires-python`)
- Virtualenv activation path
- Pants targets and tags

---

## Backend — Go

```bash
go mod download
go test ./...
go build ./cmd/<service>
go run ./cmd/<service>
```

---

## Backend — Rust

```bash
cargo build -p <crate>
cargo test -p <crate>
cargo run -p <crate>
```

---

## Frontend — Web SPA

### Next.js

```bash
pnpm install
pnpm dev                # http://localhost:3000
pnpm build
pnpm start
pnpm test
pnpm lint
```

### Vite (React / Vue / Svelte)

```bash
pnpm install
pnpm dev
pnpm build
pnpm preview
pnpm test
```

### Remix

```bash
pnpm dev
pnpm build
pnpm start
```

### Storybook (component libs)

```bash
pnpm storybook
pnpm build-storybook
```

### Common frontend constraints

- Node version pinning
- Design-system token versions
- Bundle size budgets (CI check)
- Feature flag system
- Pre-deploy preview environments (Vercel / Netlify / S3+CloudFront)
- Asset CDN / cache invalidation

---

## Mobile — Flutter

### Monorepo (Melos)

```bash
melos bootstrap
melos run test --scope="<package>"
melos run analyze
melos run build
```

### Single-app

```bash
flutter pub get
flutter test
flutter run -d <device>
flutter build apk
flutter build ipa
```

---

## Mobile — iOS (Swift)

```bash
pod install
xcodebuild -workspace <name>.xcworkspace -scheme <name> test
xcodebuild -workspace <name>.xcworkspace -scheme <name> archive
```

---

## Mobile — Android (Kotlin)

```bash
./gradlew :<module>:test
./gradlew :<module>:assembleDebug
./gradlew :<module>:installDebug
```

---

## Infra — Terraform

```bash
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan -out tfplan
terraform apply tfplan
```

Document module versions and remote state backend.

---

## Infra — Kubernetes / Helm / ArgoCD

```bash
helm lint <chart>
helm template <chart> -f values-<env>.yaml
kubectl --context <env> -n <ns> get pods -l app=<service>
argocd app get <app-name>
argocd app sync <app-name>
```

---

## Alerts / runbooks repos (Prometheus-style)

```bash
# Lint per repo conventions
promtool check rules <file>.yml
yamllint <file>.yml

# Common path layout
runbooks/alerts/applications/<service>.md
domains/alerts/.../<service>.yml
```

In handoff, list:

- alert YAML path
- runbook path
- notification channel (Slack / Chat) — update on transfer
- severity rules and SLO thresholds

---

## Data / ML

| Tool | Command |
|------|---------|
| dbt | `dbt run --select <model>`, `dbt test --select <model>` |
| Airflow | `airflow dags list`, `airflow tasks test <dag> <task> <date>` |
| Databricks | `databricks bundle deploy`, job UI link |
| Feature store | per-vendor CLI |

Capture lineage diagrams when available.

---

## Deploy / release flow snippets

| Pattern | Command / where |
|---------|-----------------|
| Dev → Staging → Prod (monorepo) | The repo's promotion command, e.g. `make promote app=<service>` |
| ArgoCD app sync | `argocd app sync <name>` or Backstage Deployments page |
| Vercel / Netlify | Auto-deploy on PR / main; preview URLs in PR comments |
| Mobile store release | Fastlane / Codemagic / EAS Submit pipelines |
| Helm release | `helm upgrade --install <release> <chart> -f values-<env>.yaml` |

Document **the actual command used in this repo**, and any pre-deploy validation step (smoke tests, schema migration check).
