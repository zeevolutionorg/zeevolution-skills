# 🚀 Release checklist — v0.1.0

Everything below needs a human with **personal** accounts. Tick the boxes in order.

> [!IMPORTANT]
> Automated checks must already pass: run `make check` first. Use **personal** Google and Microsoft accounts and **fictional** people only — never a work workspace.

## 📑 Contents

- [🔐 Step 1 — Personal identity and repo (once)](#-step-1--personal-identity-and-repo-once)
- [🔌 Step 2 — Verify on real platforms](#-step-2--verify-on-real-platforms)
- [✋ Step 3 — Manual path test (no AI)](#-step-3--manual-path-test-no-ai)
- [🎉 Step 4 — Launch](#-step-4--launch)

---

## 🔐 Step 1 — Personal identity and repo (once)

- [ ] `gh auth login` with the **zeevolution** account; `gh auth status` shows it as active.
- [ ] Personal SSH key + `~/.ssh/config` host alias `github-zeevolution`.
- [ ] In this folder: `git config user.name "Zeevolution"` and `git config user.email "<id>+zeevolution@users.noreply.github.com"` (GitHub › Settings › Emails shows the exact address).
- [ ] If the first local commit was made with a different email: `git commit --amend --reset-author --no-edit`.
- [ ] `gh repo create zeevolution/zeevolution-skills --private --source . --remote origin --description "Skills for Technologists — agent skills for Claude and Cursor, usable without AI too"`
- [ ] `git remote set-url origin git@github-zeevolution:zeevolution/zeevolution-skills.git` and `git push -u origin main`.
- [ ] GitHub settings: topics (`agent-skills`, `claude`, `claude-code`, `cursor`, `career-management`, `technologists`); protect `main` (PR required, `ci` must pass, no force-push); Actions secret **`LEAK_DENYLIST`** with the denylist contents; account email privacy on ("Keep my email private" + "Block command line pushes that expose my email").
- [ ] Local denylist at `~/.config/zeevolution/denylist.txt` (same contents as the secret).
- [ ] Branch protection on `main`: require the CI checks `lint`, `consistency`, `tests`, `e2e`, `sheets`, `security`.
- [ ] Create the PR label **`run-evals`** (opt-in behavioral evals).
- [ ] Secret **`ANTHROPIC_API_KEY`** for evals — a key from your personal Anthropic account, with a spend limit. Optional: without it, skip the `evals` stage.
- [ ] `make install` locally (pre-commit hooks).
- [ ] Before the first PR: run `claude plugin eval . --tag smoke --runs 1` once locally and check the grader format against the official "Test plugins with evals" page for your Claude Code version.

## 🔌 Step 2 — Verify on real platforms

Use a **personal** Google account and a **personal** Microsoft account. Never a work workspace.

- [ ] Google Drive connector (Claude app): does it create files and convert `.docx` → Google Docs and `.xlsx` → Google Sheets? Note the tool names.
- [ ] Google Drive MCP server (Claude Code and Cursor): same check.
- [ ] Microsoft 365 connector / MCP: can it upload? If not, Files fallback is the v0.1 path (expected).
- [ ] Upload `05 - 🪜 Ladder Assessment.xlsx` to Google Drive and open as Google Sheets: dropdowns, conditional colors, formulas (expectations update when the level changes), the chart, protected ranges, frozen rows. Write down anything lost and fix the spec.
- [ ] Google Docs: **Tools › Preferences › Enable Markdown** + **Paste from Markdown** with `00-career-hub.md`; menu names still correct?
- [ ] Run `/career-hub-toolkit me` and `/career-hub-toolkit <fictional name>` from Claude app, Claude Code and Cursor; Hub created with working links in under 2 minutes; re-run asks question F2 and doesn't overwrite.
- [ ] Install paths: Claude Code `/plugin marketplace add` + `/plugin install`; Claude app `.skill` upload; Cursor GitHub import; `npx skills add … -a cursor`. Update `docs/INSTALL.md` if any command or menu changed.

## ✋ Step 3 — Manual path test (no AI)

- [ ] Someone who didn't write the guide follows `docs/MANUAL.md` on Google, timed (target ≤ 30 min).
- [ ] Same on Microsoft 365.
- [ ] Master copy path (target ≤ 10 min per person).
- [ ] Screenshots for MANUAL.md: personal accounts, fictional data, EXIF stripped; `scripts/check_leaks.py` passes on them.

## 🎉 Step 4 — Launch

- [ ] Read every template once, end to end, in both languages.
- [ ] `scripts/build.sh` green; CI green on `main`.
- [ ] CHANGELOG: set the date of 0.1.0.
- [ ] `gh repo edit zeevolution/zeevolution-skills --visibility public --accept-visibility-change-consequences`
- [ ] `git tag v0.1.0 && git push --tags` → the release workflow publishes the Manual Kits and `.skill` files.
- [ ] Create one real hub in your own workspace.
- [ ] Uncomment the **CI badge** at the top of `README.md` (it only works once the repo is public and CI has run).
- [ ] Later (not v0.1): submit to the Cursor Marketplace once the repo is stable.
