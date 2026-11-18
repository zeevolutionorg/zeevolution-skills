---
name: create-adr-asks-first
tags: [smoke, software-engineering]
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Write, Edit, Glob, Grep, Bash]
---
Write an ADR about our decision to move the order service from polling to an event queue.
