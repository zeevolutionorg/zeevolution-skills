---
type: llm
---
The answer includes the change (a `require(cents >= 0)` or equivalent guard) and a test that fails without it. The validation plan runs what CI runs, `./gradlew ktlintCheck test`, and also the Makefile's extra `detekt`, without claiming any of it already passed. It says the PR is opened as a draft and its checks are followed (`gh pr checks` or equivalent) until green. The PR description has what changed, why, how it was tested, and where to start reading.
