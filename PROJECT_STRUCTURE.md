# Project Structure Explained

## Files in This Project

| File | What it is |
|------|-----------|
| `Claude.md` | Instructions Claude reads automatically at the start of every conversation in this project. Rules, context, how you want Claude to behave. |
| `.claude/agents/playwright-test-engineer.md` | The **subagent** definition. When Claude uses the playwright-test-engineer agent, this file tells that agent how to behave (rules, patterns, conventions). |
| `agents/runner_agent.py` | A plain **Python script** — not a Claude agent. You run it manually with `python3 agents/runner_agent.py`. |

---

## What Are Skills?

Skills live in `~/.claude/plugins/` and are reusable behaviors you can trigger with slash commands like `/commit`, `/simplify`, etc.
They are **not** in your project folder — they are global to Claude Code on your machine.

---

## Simple Summary

```
Claude.md                →  Rules and context for Claude in this project
.claude/agents/*.md      →  Claude subagent definitions (internal AI helpers)
agents/*.py              →  Your own Python scripts you run yourself
~/.claude/plugins/       →  Skills (slash commands like /commit)
```

---

## The Key Difference

| Looks like an agent | Actually is... |
|---------------------|---------------|
| `agents/runner_agent.py` | A Python script you run manually |
| `.claude/agents/playwright-test-engineer.md` | A real Claude subagent |

The naming is confusing — `runner_agent.py` has "agent" in the name but it is just a Python automation script that runs tests and publishes to Notion.
