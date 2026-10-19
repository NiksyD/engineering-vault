---
title: "Superpowers - Complete Agentic Software Development Methodology"
source: "https://github.com/obra/superpowers"
author: "@obra (Jesse Vincent)"
tags:
  - ai-skill
  - methodology
  - tdd
  - planning
---

# 🦸 Superpowers

> A complete software development methodology for coding agents, enforcing brainstorming, bite-sized specs, strict TDD (Red/Green), and subagent delegation.

---

## ⚡ Quick Install Command (Run on any new machine)

```bash
agy plugin install https://github.com/obra/superpowers
```

*(To update an existing installation, simply rerun the same command).*

---

## 🎯 How It Works & Key Workflows

### 1. Interactive Brainstorming (`/superpowers:brainstorm`)
Before writing code, the agent steps back and interviews you:
- Clarifies ambiguity and questions assumptions.
- Proposes architectural options and trade-offs.
- Breaks down requirements into concise, readable chunks.

### 2. Implementation Planning (`/superpowers:plan`)
- Produces a step-by-step plan broken into 2–5 minute digestible tasks.
- Emphasizes **YAGNI** (You Aren't Gonna Need It) and **DRY**.
- Includes explicit verification steps for every single task.

### 3. Strict TDD Execution (Red/Green/Refactor)
- Writes the failing test first (Red).
- Writes the minimal code required to make it pass (Green).
- Refactors without breaking existing contracts.
- **Never** reports a task as complete without verifiable test output.

### 4. Subagent-Driven Development
- Dispatches isolated tasks to background worker subagents.
- Inspects and code-reviews their changes before integrating.

---

## 🛠️ When to Use
- **New complex features** (e.g., Auth systems, Stripe billing, complex data pipelines).
- **Core refactors** where regressions cannot be tolerated.
- **Multi-step engineering tasks** where you want the agent to work autonomously for extended sessions without wandering off-spec.
