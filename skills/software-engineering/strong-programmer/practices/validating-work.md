# Validating your work

Don't claim it works until you've seen it work. Run what the project's CI runs — locally first, then on the pull request — and report exactly what you ran.

## Find the project's checks

| Look in | For |
|---|---|
| `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `.woodpecker.yml`, `azure-pipelines.yml` | What CI runs on a pull request, and in what order |
| `Makefile`, `justfile`, `Taskfile.yml` | Shortcuts that bundle the checks (`make check`, `make test`) |
| `build.gradle.kts`, `pom.xml` | `./gradlew check`, `test`, `ktlintCheck`, `detekt`; `mvn verify` |
| `package.json` | `scripts` such as `lint`, `test`, `build` |
| `.pre-commit-config.yaml`, `.husky/` | Checks that run before every commit |
| `CONTRIBUTING.md`, `README.md`, `AGENTS.md` | What the project asks contributors to run |

CI is the source of truth: when the Makefile and the CI workflow disagree, run what CI runs — and mention the gap.

## Run them locally

1. Run the narrowest check first — the test for the code you changed — then the whole suite and the linters CI runs.
2. For a behavior change, write or update a test that fails without your change and passes with it. A tidying keeps the existing tests green.
3. If a check can't run here (a missing tool, service or credential), say which one and why. Don't skip it silently, and never work around a security control to make it run.
4. A red check you didn't cause still matters: confirm it also fails on the base branch, and say so.

## Follow the pull request's CI

- Push the branch and open the pull request as a draft, so nobody spends review time on it before its checks have run.
- Watch the checks: `gh pr checks <number> --watch` on GitHub, or the pipeline page on other hosts.
- On a failure, read the log (`gh run view <run-id> --log-failed`), fix the cause, push again, and watch again.
- Mark the PR ready for review only when every required check is green.

## Report what you ran

In the PR description and in your answer:

- the commands you ran and their results — counts, not "looks good";
- what CI showed, with the check names;
- what couldn't run here, and what covers it instead.

Never report done on red or unverified checks.
